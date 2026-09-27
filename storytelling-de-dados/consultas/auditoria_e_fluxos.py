"""
auditoria_e_fluxos.py — Reunião com Danny (22/09/2026), tópicos 1 e 2
  1) Auditoria do painel final ANTES do DiD
  2) Descritivas de fluxos: para onde as pessoas estão migrando?
Saídas em out/: auditoria.md, CSVs das tabelas e dashboard_data.json
(insumo único do HTML de Storytelling de Dados — tópico 3).

Uso:  python auditoria_e_fluxos.py   (requer pandas, numpy, pyarrow, tabulate)
Ajuste apenas o bloco CONFIG para os nomes de colunas do seu painel.
"""
import json
from pathlib import Path
import numpy as np
import pandas as pd

# ============================ CONFIG ============================
PANEL_PATH = Path("data/painel_final.parquet")   # .parquet ou .csv
OUT = Path("out")
C = {
    "id": "id_individuo",   # chave do indivíduo (UPA+V1008+V1014+V2003/V2007/V2008...)
    "ano": "Ano", "tri": "Trimestre",
    "peso": "V1028",
    "cod": "V4010",         # COD da ocupação (4 dígitos)
    "aioe": "aioe",         # escore C-AIOE da ocupação
    "vd4001": "VD4001",     # 1 = na força de trabalho, 2 = fora
    "vd4002": "VD4002",     # 1 = ocupado, 2 = desocupado
    "sexo": "V2007", "idade": "V2009",
    "visita": "V1016",      # nº da entrevista (1 a 5) — opcional
}
POS_INICIO = (2023, 1)      # primeiro trimestre pós-ChatGPT
EXCLUIR = [(2022, 4)]       # trimestre do lançamento (30/11/2022): fora do pré/pós
N_Q = 4                     # quartis de exposição
N_MIN = 30                  # células com menos obs. são sinalizadas
# ================================================================

GRUPOS = {
    "0": "Forças armadas e policiais", "1": "Dirigentes e gerentes",
    "2": "Profissionais das ciências e intelectuais", "3": "Técnicos de nível médio",
    "4": "Apoio administrativo", "5": "Serviços e vendas",
    "6": "Agropecuária", "7": "Indústria, construção e ofícios",
    "8": "Operadores de máquinas", "9": "Ocupações elementares",
}
DEST = ["Mesmo grupo", "Outro grupo", "Desocupado", "Fora da força"]


def wquantiles(x, w, qs):
    o = np.argsort(x); x, w = np.asarray(x)[o], np.asarray(w)[o]
    cw = np.cumsum(w) / w.sum()
    return np.interp(qs, cw, x)


def carregar():
    f = pd.read_parquet if PANEL_PATH.suffix == ".parquet" else pd.read_csv
    df = f(PANEL_PATH)
    faltam = [v for k, v in C.items() if v not in df.columns and k != "visita"]
    if faltam:
        raise SystemExit(f"Colunas não encontradas (ajuste CONFIG): {faltam}")
    df["t"] = df[C["ano"]] * 4 + df[C["tri"]] - 1
    df["status"] = np.select(
        [df[C["vd4001"]] == 2, df[C["vd4002"]] == 1, df[C["vd4002"]] == 2],
        ["Fora da força", "Ocupado", "Desocupado"], default=None)
    cod = pd.to_numeric(df[C["cod"]], errors="coerce")
    df["grupo"] = np.where((df.status == "Ocupado") & cod.notna(),
                           cod.fillna(0).astype(int).astype(str).str.zfill(4).str[0], None)
    df["grupo"] = df["grupo"].map(GRUPOS)
    t_pos = POS_INICIO[0] * 4 + POS_INICIO[1] - 1
    excl = {a * 4 + q - 1 for a, q in EXCLUIR}
    df["periodo"] = np.where(df.t.isin(excl), "excluído",
                             np.where(df.t >= t_pos, "pós", "pré"))
    return df.sort_values([C["id"], "t"]).reset_index(drop=True)


# ----------------------------- 1. AUDITORIA -----------------------------
def auditoria(df):
    i, t = C["id"], "t"
    g = df.groupby(i)
    dif = g[t].diff().dropna()
    oc = df[df.status == "Ocupado"]
    r = {
        "linhas": int(len(df)),
        "individuos": int(df[i].nunique()),
        "trimestres": f"{df[C['ano']].min()}T{df.loc[df.t.idxmin(), C['tri']]} a "
                      f"{df[C['ano']].max()}T{df.loc[df.t.idxmax(), C['tri']]}",
        "duplicatas_id_trimestre": int(df.duplicated([i, t]).sum()),
        "obs_por_individuo": g.size().value_counts().sort_index().to_dict(),
        "saltos_entre_obs": dif.value_counts().sort_index().astype(int).to_dict(),
        "pct_sexo_inconsistente": round(100 * (g[C["sexo"]].nunique() > 1).mean(), 2),
        "pct_idade_inconsistente": round(100 * (
            (g[C["idade"]].max() - g[C["idade"]].min()) >
            ((g[t].max() - g[t].min()) / 4 + 1.5)).mean(), 2),
        "pct_status_nulo": round(100 * df.status.isna().mean(), 2),
        "pct_ocupados_sem_cod": round(100 * oc[C["cod"]].isna().mean(), 2),
        "pct_ocupados_sem_aioe": round(100 * oc[C["aioe"]].isna().mean(), 2),
        "cods_sem_aioe_top10": oc.loc[oc[C["aioe"]].isna(), C["cod"]]
                                 .value_counts().head(10).astype(int).to_dict(),
    }
    if C["visita"] in df.columns:
        v1 = df.loc[df[C["visita"]] == 1, i].unique()
        v5 = set(df.loc[df[C["visita"]] == 5, i])
        r["pct_retencao_v1_ate_v5"] = round(100 * np.mean([x in v5 for x in v1]), 1) if len(v1) else None
    tri = df.groupby([C["ano"], C["tri"]]).agg(
        obs=(i, "size"), pop_mi=(C["peso"], lambda w: w.sum() / 1e6),
        pct_ocupado=("status", lambda s: 100 * (s == "Ocupado").mean()))
    r["obs_por_trimestre"] = tri.round(2).reset_index().to_dict("records")
    comp = oc[oc.periodo != "excluído"].groupby("periodo").apply(
        lambda d: pd.Series({"aioe_medio": np.average(d[C["aioe"]].fillna(d[C["aioe"]].mean()),
                                                      weights=d[C["peso"]]),
                             "n": len(d)}), include_groups=False)
    r["composicao_pre_pos"] = comp.round(4).reset_index().to_dict("records")

    alertas = []
    if r["duplicatas_id_trimestre"]: alertas.append("Há duplicatas id×trimestre — a chave do indivíduo não é única.")
    if r["pct_sexo_inconsistente"] > 1: alertas.append("Sexo varia dentro do id (>1%) — pareamento suspeito.")
    if r["pct_idade_inconsistente"] > 2: alertas.append("Idade incompatível com o tempo decorrido (>2%).")
    if r["pct_ocupados_sem_aioe"] > 5: alertas.append("Mais de 5% dos ocupados sem AIOE — revisar crosswalk.")
    if any(k > 1 for k in r["saltos_entre_obs"]): alertas.append("Há saltos >1 trimestre: transições usam só pares consecutivos.")
    r["alertas"] = alertas

    with open(OUT / "auditoria.md", "w", encoding="utf-8") as f:
        f.write("# Auditoria do painel final\n\n")
        for k, v in r.items():
            if k in ("obs_por_trimestre", "composicao_pre_pos"): continue
            f.write(f"- **{k}**: {v}\n")
        f.write("\n## Observações por trimestre\n\n" + tri.round(2).to_markdown() + "\n")
        f.write("\n## Composição pré/pós (ocupados)\n\n" + comp.round(4).to_markdown() + "\n")
    return r


# ------------------------------ 2. FLUXOS ------------------------------
def transicoes(df):
    i = C["id"]
    nx = df.groupby(i)[["t", "status", "grupo", C["aioe"]]].shift(-1)
    nx.columns = ["t1", "status1", "grupo1", "aioe1"]
    p = pd.concat([df, nx], axis=1)
    p = p[(p.t1 - p.t == 1) & (p.status == "Ocupado") & p[C["aioe"]].notna()
          & p.status1.notna() & (p.periodo != "excluído")].copy()
    # quartis de exposição fixados na distribuição PRÉ (ponderada) — não contamina com o pós
    pre = p[p.periodo == "pré"]
    cuts = wquantiles(pre[C["aioe"]], pre[C["peso"]], np.linspace(0, 1, N_Q + 1)[1:-1])
    p["q"] = "Q" + (np.searchsorted(cuts, p[C["aioe"]], side="right") + 1).astype(str)
    p["q1"] = np.where(p.aioe1.notna(),
                       "Q" + (np.searchsorted(cuts, p.aioe1.fillna(0), side="right") + 1).astype(str), None)
    p["destino"] = np.select(
        [p.status1 == "Desocupado", p.status1 == "Fora da força", p.grupo1 == p.grupo],
        ["Desocupado", "Fora da força", "Mesmo grupo"], default="Outro grupo")
    return p, cuts


def matriz(p, linha, col, extra=()):
    k = [*extra, linha]
    m = p.pivot_table(index=k, columns=col, values=C["peso"], aggfunc="sum", fill_value=0)
    n = p.groupby(k).size().rename("n_obs")
    return (100 * m.div(m.sum(axis=1), axis=0)).round(2).join(n)


def fluxos(p):
    # A) Destino por quartil de exposição, pré vs pós (+ diferença em p.p.)
    A = matriz(p, "q", "destino", ("periodo",)).reindex(columns=DEST + ["n_obs"], fill_value=0)
    dA = (A.loc["pós", DEST] - A.loc["pré", DEST]).round(2)
    # B) Para qual grupo vão os que mudam de grupo, por quartil de origem
    mud = p[p.destino == "Outro grupo"]
    B = matriz(mud, "q", "grupo1", ("periodo",))
    # C) Direção da mudança em exposição (sobe/desce de quartil)
    mud = mud[mud.q1.notna()].copy()
    mud["direcao"] = np.select([mud.q1 > mud.q, mud.q1 < mud.q],
                               ["Mais exposta", "Menos exposta"], "Mesmo quartil")
    D = matriz(mud, "q", "direcao", ("periodo",))
    # E) Série trimestral: Q4 (mais exposto) vs Q1 — leitura visual de pré-tendência
    p["tri_lbl"] = (p.t // 4).astype(str) + "T" + (p.t % 4 + 1).astype(str)
    e = p[p.q.isin(["Q1", f"Q{N_Q}"])]
    E = (e.groupby(["tri_lbl", "q"]).apply(lambda d: pd.Series({
            "pct_muda_grupo": 100 * np.average(d.destino == "Outro grupo", weights=d[C["peso"]]),
            "pct_vai_desocupado": 100 * np.average(d.destino == "Desocupado", weights=d[C["peso"]]),
            "pct_sai_forca": 100 * np.average(d.destino == "Fora da força", weights=d[C["peso"]]),
            "n_obs": len(d)}), include_groups=False).round(2).reset_index())
    # Sankey grupo→grupo (pós), fluxo médio por trimestre em milhares
    mp = mud[mud.periodo == "pós"]
    nq = max(mp.t.nunique(), 1)
    S = (mp.groupby(["grupo", "grupo1"])[C["peso"]].sum() / nq / 1e3).round(1)
    S = S[S > 0].sort_values(ascending=False).head(25).reset_index()
    S.columns = ["origem", "destino", "mil_pessoas_por_trimestre"]
    return A, dA, B, D, E, S


def main():
    OUT.mkdir(exist_ok=True)
    df = carregar()
    aud = auditoria(df)
    p, cuts = transicoes(df)
    A, dA, B, D, E, S = fluxos(p)
    for nome, t in {"A_destino_por_quartil": A, "A_diferenca_pos_menos_pre": dA,
                    "B_grupo_destino_dos_que_mudam": B, "D_direcao_exposicao": D,
                    "E_serie_Q1_vs_Q4": E, "S_sankey_pos": S}.items():
        t.to_csv(OUT / f"{nome}.csv", encoding="utf-8-sig")
    rec = lambda t: json.loads(t.reset_index().to_json(orient="records", force_ascii=False))
    json.dump({
        "meta": {"pos_inicio": POS_INICIO, "excluidos": EXCLUIR, "cortes_quartis_aioe": list(map(float, cuts)),
                 "n_transicoes": int(len(p)), "n_min_celula": N_MIN},
        "auditoria": aud, "destino_por_quartil": rec(A), "dif_pos_pre": rec(dA),
        "grupo_destino": rec(B), "direcao_exposicao": rec(D),
        "serie_q1_q4": rec(E), "sankey_pos": rec(S),
    }, open(OUT / "dashboard_data.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    print("\n".join(["ALERTAS:"] + (aud["alertas"] or ["nenhum"])))
    print(f"\nTransições consecutivas válidas (ocupado na origem): {len(p):,}")
    print("\nDiferença pós − pré (p.p.) por quartil de exposição:\n", dA)
    pequenas = A[A.n_obs < N_MIN]
    if len(pequenas): print(f"\n⚠ {len(pequenas)} células com n < {N_MIN}")
    print(f"\nArquivos em {OUT.resolve()}")


if __name__ == "__main__":
    main()
