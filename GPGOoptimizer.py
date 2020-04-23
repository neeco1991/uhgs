import numpy as np
from pyGPGO.covfunc import squaredExponential
from pyGPGO.acquisition import Acquisition
from pyGPGO.surrogates.GaussianProcess import GaussianProcess
from pyGPGO.GPGO import GPGO
from main import uhgs


def f(x):
    return (np.sin(x) - 2)


sexp = squaredExponential(sigman=100)
gp = GaussianProcess(sexp)
acq = Acquisition(mode='ExpectedImprovement')
param = {'minSol': ('int', [10, 50]), 'maxSol': ('int', [60, 100]), 'omega': (
    'int', [5, 500]), 'muelite': ('cont', [0.5, 2]), 'itDiv': ('cont', [0.1, 0.51])}
np.random.seed(7)
gpgo = GPGO(gp, acq, uhgs, param, n_jobs=1)
gpgo.run(init_evals=6, max_iter=60)
