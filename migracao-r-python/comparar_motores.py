"""Reestima a etapa 05 em R (fixest) e compara com o resultado do Python (pyfixest).

A etapa 05 foi migrada de R para Python no commit 0bca695. Este script refaz a
verificação de forma reproduzível, sem tocar em nada da estimação oficial:

1. confere o sha256 do arquivo de estimação contra o que está no job da etapa 05,
   para garantir que os dois motores leram exatamente os mesmos dados;
2. roda `R/legado/modelos.R` com uma cópia do job apontando a saída para
   `migracao-r-python/resultados/motor-r/`, e não para `output/modelos/`;
3. compara termo a termo com os CSV que o Python já gravou em `output/modelos/`.

    uv run python migracao-r-python/comparar_motores.py

Saídas em `migracao-r-python/resultados/`: os arquivos brutos do motor R, a tabela
`comparacao_coeficientes.csv` e o `resumo.json` com as diferenças máximas.
"""
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

import pandas as pd
import yaml

RAIZ = Path(__file__).resolve().parents[1]
PASTA = Path(__file__).resolve().parent
JOB = RAIZ / 'data' / 'interim' / 'estimacao' / '05_pnadc.json'
SCRIPT_R = RAIZ / 'R' / 'legado' / 'modelos.R'
PYTHON_OUT = RAIZ / 'output' / 'modelos'
RESULTADOS = PASTA / 'resultados'
SAIDA_R = RESULTADOS / 'motor-r'

CHAVES = ['estimativa', 'erro_padrao', 'p_valor_conservador',
          'ic95_inferior_conservador', 'ic95_superior_conservador']


def sha256(caminho, bloco=1 << 20):
    h = hashlib.sha256()
    with open(caminho, 'rb') as f:
        for pedaco in iter(lambda: f.read(bloco), b''):
            h.update(pedaco)
    return h.hexdigest()


def termo_canonico(termo):
    """R escreve pos:telework, pyfixest escreve telework:pos. Mesma interação."""
    return ':'.join(sorted(termo.split(':')))


def rscript():
    caminho = yaml.safe_load((RAIZ / 'config.yaml').read_text(encoding='utf-8')) \
        .get('estimacao', {}).get('rscript')
    if not caminho or not Path(caminho).exists():
        sys.exit(f'Rscript não encontrado em {caminho!r}. Ajuste estimacao.rscript no config.yaml.')
    return caminho


def roda_r():
    job = json.loads(JOB.read_text(encoding='utf-8'))
    dados = Path(job['dados'])
    if not dados.exists():
        sys.exit(f'O arquivo de estimação não está no disco: {dados}\n'
                 'Rode a etapa 05 antes de comparar os motores.')

    print('conferindo o sha256 do arquivo de estimação (822 MB, leva um minuto)...')
    atual = sha256(dados)
    igual = atual == job['sha256_dados']
    print(f'  job      : {job["sha256_dados"]}')
    print(f'  no disco : {atual}  {"confere" if igual else "NÃO CONFERE"}')
    if not igual:
        sys.exit('Os dados mudaram desde a estimação em Python. A comparação não seria justa.')

    SAIDA_R.mkdir(parents=True, exist_ok=True)
    job['output'] = str(SAIDA_R)
    job_r = RESULTADOS / 'job_motor_r.json'
    job_r.write_text(json.dumps(job, ensure_ascii=False, indent=2), encoding='utf-8')

    print(f'\nrodando {SCRIPT_R.relative_to(RAIZ)} nos 7 modelos...')
    t0 = time.time()
    r = subprocess.run([rscript(), str(SCRIPT_R), str(job_r)], cwd=RAIZ,
                       capture_output=True, text=True, encoding='utf-8', errors='replace')
    minutos = (time.time() - t0) / 60
    print((r.stdout or '').strip()[-2000:])
    if r.returncode != 0:
        print((r.stderr or '').strip()[-3000:])
        sys.exit(f'O motor R terminou com erro (código {r.returncode}).')
    print(f'motor R concluído em {minutos:.1f} minutos')
    return igual, minutos


def compara():
    linhas = []
    for csv_r in sorted(SAIDA_R.glob('05_pnadc_*.csv')):
        if csv_r.name.endswith('_vcov.csv'):
            continue
        csv_py = PYTHON_OUT / csv_r.name
        if not csv_py.exists():
            print(f'sem par em output/modelos: {csv_r.name}')
            continue
        r = pd.read_csv(csv_r).assign(chave=lambda d: d.termo.map(termo_canonico))
        p = pd.read_csv(csv_py).assign(chave=lambda d: d.termo.map(termo_canonico))
        j = r.merge(p, on='chave', suffixes=('_r', '_py'), validate='one_to_one')
        for _, x in j.iterrows():
            linha = {'modelo': x.modelo_r.replace('05_pnadc_', ''),
                     'termo': x.chave,
                     'termo_no_r': x.termo_r, 'termo_no_python': x.termo_py,
                     'n_r': int(x.n_r), 'n_python': int(x.n_py),
                     'clusters_r': int(x.graus_liberdade_conservador_r) + 1,
                     'clusters_python': int(x.graus_liberdade_conservador_py) + 1}
            for c in CHAVES:
                a, b = float(x[f'{c}_r']), float(x[f'{c}_py'])
                linha[f'{c}_r'] = a
                linha[f'{c}_python'] = b
                linha[f'{c}_diferenca'] = b - a
            linhas.append(linha)

    t = pd.DataFrame(linhas)
    t.to_csv(RESULTADOS / 'comparacao_coeficientes.csv', index=False, encoding='utf-8-sig')
    return t


def main():
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    RESULTADOS.mkdir(parents=True, exist_ok=True)
    mesmo_dado, minutos = roda_r()
    t = compara()

    meta_r = json.loads((SAIDA_R / '05_pnadc_muda_ocupacao_2_metadados.json').read_text(encoding='utf-8'))
    meta_py = json.loads((PYTHON_OUT / '05_pnadc_muda_ocupacao_2_metadados.json').read_text(encoding='utf-8'))
    resumo = {
        'data_da_comparacao': time.strftime('%Y-%m-%d'),
        'mesmo_arquivo_de_dados': bool(mesmo_dado),
        'sha256_dados': json.loads(JOB.read_text(encoding='utf-8'))['sha256_dados'],
        'motor_r': meta_r['pacote'],
        'motor_python': meta_py['pacote'],
        'minutos_do_motor_r': round(minutos, 1),
        'modelos': int(t.modelo.nunique()),
        'termos_comparados': int(len(t)),
        'mesma_amostra': bool((t.n_r == t.n_python).all()),
        'mesmos_clusters': bool((t.clusters_r == t.clusters_python).all()),
        'diferenca_maxima': {c: float(t[f'{c}_diferenca'].abs().max()) for c in CHAVES},
    }
    (RESULTADOS / 'resumo.json').write_text(
        json.dumps(resumo, ensure_ascii=False, indent=2), encoding='utf-8')

    print('\n' + json.dumps(resumo, ensure_ascii=False, indent=2))
    colunas = ['modelo', 'termo', 'estimativa_r', 'estimativa_python', 'estimativa_diferenca']
    print('\n' + t[colunas].to_string(index=False))


if __name__ == '__main__':
    main()
