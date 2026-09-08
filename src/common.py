"""Persistência atômica, auditoria de consultas e execução de etapas."""
import hashlib
import json
import logging
import os
import re
import time
from datetime import datetime, timezone
from pathlib import Path
import pandas as pd
from .config import CFG, ROOT, INTERIM, LOGS, TABLES


def json_write(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + '.tmp')
    tmp.write_text(json.dumps(value, ensure_ascii=False, indent=2, default=str), encoding='utf-8')
    os.replace(tmp, path)


def parquet_write(frame, path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix('.tmp.parquet')
    frame.to_parquet(tmp, index=False)
    os.replace(tmp, path)


def table(frame, name):
    """Toda tabela sai nos três formatos: CSV para reuso, TXT para leitura, TeX para o paper."""
    frame.to_csv(TABLES / f'{name}.csv', index=False)
    (TABLES / f'{name}.txt').write_text(frame.to_string(index=False), encoding='utf-8')
    (TABLES / f'{name}.tex').write_text(frame.to_latex(index=False, escape=True, float_format='%.6g'), encoding='utf-8')


def note(stage, message):
    path = LOGS / 'NOTAS_DECISOES.md'
    with path.open('a', encoding='utf-8') as stream:
        stream.write(f'\n### {datetime.now(timezone.utc).isoformat()} — {stage}\n\n{message}\n')


def required(path):
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f'Insumo necessário ausente: {path.relative_to(ROOT)}')
    return path


def unique(frame, keys, label):
    if frame[keys].isna().any().any() or frame.duplicated(keys).any():
        raise ValueError(f'{label}: chave ausente ou duplicada ({keys}).')


def codes(series, digits):
    result = series.astype('string').str.replace(r'\.0$', '', regex=True).str.strip()
    if (~result.str.fullmatch(r'\d{1,' + str(digits) + '}', na=False)).any():
        raise ValueError('Código ocupacional inválido; verifique o insumo.')
    return result.str.zfill(digits)


def client():
    from google.cloud import bigquery
    import google.auth
    credentials, _ = google.auth.default(quota_project_id=CFG['bigquery']['projeto'])
    return bigquery.Client(project=CFG['bigquery']['projeto'], credentials=credentials,
                           location=CFG['bigquery']['localizacao'])


def query(sql, name, *, metadata=False):
    """Microdados nunca são baixados: só consultas agregadas ou dicionários/diretórios."""
    from google.cloud import bigquery
    if not metadata and 'GROUP BY' not in sql.upper():
        raise ValueError('Download de microdados proibido: consulta sem agregação.')
    (LOGS / 'sql').mkdir(exist_ok=True)
    (LOGS / 'sql' / f'{name}.sql').write_text(sql, encoding='utf-8')
    cli = client()
    dry = cli.query(sql, job_config=bigquery.QueryJobConfig(dry_run=True, use_query_cache=False))
    limit = CFG['bigquery']['max_bytes_por_consulta']
    if dry.total_bytes_processed is not None and dry.total_bytes_processed > limit:
        raise RuntimeError(f'Consulta {name} supera o limite de bytes configurado: {dry.total_bytes_processed}.')
    job = cli.query(sql, job_config=bigquery.QueryJobConfig(maximum_bytes_billed=limit))
    frame = job.result().to_dataframe(create_bqstorage_client=True)
    for column in frame:
        if str(frame[column].dtype) == 'dbdate':
            frame[column] = pd.to_datetime(frame[column])
    json_write(LOGS / f'{name}_consulta.json', {
        'projeto': cli.project, 'job_id': job.job_id, 'bytes_processados': job.total_bytes_processed,
        'bytes_cobrados': job.total_bytes_billed, 'cache': job.cache_hit,
        'sha256_sql': hashlib.sha256(sql.encode()).hexdigest(), 'linhas': len(frame),
        'executado_em': datetime.now(timezone.utc).isoformat()})
    return frame


def run(stage, function):
    """Trava por etapa: uma retomada simultânea espera em vez de duplicar trabalho."""
    import psutil
    lock = INTERIM / f'execucao_{stage}.lock'
    waited = False
    while True:
        try:
            with lock.open('x') as stream:
                stream.write(str(os.getpid()))
            break
        except FileExistsError:
            waited = True
            try:
                pid = int(lock.read_text())
            except (ValueError, FileNotFoundError):
                time.sleep(1)
                continue
            if not psutil.pid_exists(pid):
                lock.unlink(missing_ok=True)
                continue
            time.sleep(5)
    try:
        status_path = INTERIM / f'status_{stage}.json'
        if waited and status_path.exists():
            if json.loads(status_path.read_text(encoding='utf-8')).get('status') == 'concluido':
                return
        return _run_unlocked(stage, function)
    finally:
        lock.unlink(missing_ok=True)


def _run_unlocked(stage, function):
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s', handlers=[
        logging.FileHandler(LOGS / f'{stage}.log', encoding='utf-8'), logging.StreamHandler()])
    status = {'etapa': stage, 'inicio': datetime.now(timezone.utc).isoformat()}
    json_write(INTERIM / f'status_{stage}.json', dict(status, status='em_execucao'))
    try:
        logging.info('Iniciando etapa %s', stage)
        result = function()
        status.update(status='concluido', resultado=result)
        logging.info('Etapa %s concluída: %s', stage, result)
    except Exception as exc:
        status.update(status='bloqueado', erro=f'{type(exc).__name__}: {exc}')
        logging.exception('Etapa %s interrompida', stage)
        raise
    finally:
        status['fim'] = datetime.now(timezone.utc).isoformat()
        json_write(INTERIM / f'status_{stage}.json', status)
