from fast_excursion_limit.fast_excursion_heston import FastExcursionHeston
from fast_excursion_limit.heston_random_ode import HestonRandomODE


def test_fast_excursion_limit():
    heston_limit = HestonRandomODE.example().fast_excursion_limit()
    assert heston_limit == FastExcursionHeston.example()
