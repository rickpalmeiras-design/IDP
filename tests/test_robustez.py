import numpy as np
from scipy import stats
from src.robustez import holm, bh, trimestre


def test_holm_valores_conhecidos():
    assert np.allclose(holm([0.01, 0.04, 0.03, 0.005]), [0.03, 0.06, 0.06, 0.02])


def test_bh_valores_conhecidos_e_scipy():
    p = [0.01, 0.04, 0.03, 0.005]
    assert np.allclose(bh(p), [0.02, 0.04, 0.04, 0.02])
    assert np.allclose(bh(p), stats.false_discovery_control(p))


def test_trimestre_relativo_ao_marco():
    assert trimestre(0) == '2022T4'
    assert trimestre(-1) == '2022T3'
    assert trimestre(-15) == '2019T1'
