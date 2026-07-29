from fast_excursion_limit import defaults
from fast_excursion_limit._heston_base import HestonBase
from fast_excursion_limit.fast_excursion_heston import FastExcursionHeston


class HestonRandomODE(HestonBase):
    _EXAMPLE_PARAMS = defaults.EXAMPLE_PARAMS_ODE

    def __init__(
        self,
        spot_price,
        domestic_rate,
        foreign_rate,
        sigma,
        rho,
        gamma,
        reversion,
    ):
        self.reversion = reversion
        super().__init__(spot_price, domestic_rate, foreign_rate, sigma, rho, gamma)

    def _check_params(self):
        assert self.reversion >= 0
        super()._check_params()

    def _simulate_next(self, time_prev, brownian_prev, space_prev, step_size):
        # Evaluate the Heston / integrated CIR ODE function to get the ODE solution's
        # gradient
        gradient = (
            self.reversion * (time_prev - space_prev + self.gamma * brownian_prev[1])
            + 1  # The 1 here keeps a flat forward variance of \sigma^2, same as FEH
        )
        # Now we take a forward Euler step for the *inverse* of the ODE solution (using
        # the inverse function theorem). This is the secret sauce that achieves
        # stability under arbitrarily high reversion. Establishing the legitimacy of
        # this, including the floor epsilon, is non-trivial. (See the article.)
        time_next = time_prev + step_size / max(gradient, defaults.EPSILON)
        brownian_next = self._brownian_next(brownian_prev, step_size)
        space_next = space_prev + step_size
        return time_next, brownian_next, space_next

    def fast_excursion_limit(self) -> FastExcursionHeston:
        params = {k: v for k, v in vars(self).items() if k != "reversion"}
        return FastExcursionHeston(**params)
