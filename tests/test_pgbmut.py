import os
import pickle
import pytest
import functools

try:
    import pycuda
except ImportError:
    #ans = input('PyCUDA not found.  Regression tests will take forever.  Do you want to continue? [y/n] ')
    print('PyCUDA not found. Regression tests will run on CPU and may take several minutes.')
    #if ans in ['Y', 'y']:
    #    pass
    #else:
    #    sys.exit()

from pygbe.main import main

@pytest.mark.parametrize('key', ['total_elements',
                                 'E_solv_kJ',
                                 'E_coul_kcal',
                                 'E_coul_kJ',
                                 'E_solv_kcal'])
def test_PGB_mut_sensor(key):
    results = get_results()

    with open('pgbmut.pickle', 'rb') as f:
        base_results = pickle.load(f)

    assert abs(base_results[key] - results[key]) / abs(base_results[key]) < 1e-12

def test_pgbmut_iterations():
    results = get_results()
    with open('pgbmut.pickle', 'rb') as f:
        base_results = pickle.load(f)

    assert base_results['iterations'] == results['iterations']

@functools.lru_cache(6)
def get_results():
    print('Generating results for 1PGBmut example...')
    if os.getcwd().rsplit('/', 1)[1] == 'tests':
        results = main(['','../examples/1PGBmut_sensor'],
                        log_output=False,
                        return_results_dict=True)
    elif os.getcwd().rsplit('/', 1)[1] == 'pygbe':
        results = main(['','./examples/1PGBmut_sensor'],
                        log_output=False,
                        return_results_dict=True)
    else:
        print("Run tests from either the main repo directory or the tests directory")

    return results
