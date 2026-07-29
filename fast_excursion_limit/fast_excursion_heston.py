import numpy as np
from scipy.stats import norminvgauss

from fast_excursion_limit._heston_base import HestonBase


class FastExcursionHeston(HestonBase):
    def _simulate_next(self, time_prev, brownian_prev, space_prev, step_size):
        space_next = space_prev + step_size
        brownian_next = self._brownian_next(brownian_prev, step_size)
        # Exact simulation of this running maximum of Brownian motion is of course
        # possible via a Brownian bridge (using an additional uniform variable). But
        # this defeats the main point here, which is to keep random numbers aligned
        # between the two simulation schemes, so that we can visualise convergence on
        # a pathwise basis (as in Figure 1).
        time_next = max(time_prev, space_next - self.gamma * brownian_next[1])
        return time_next, brownian_next, space_next

    def cdf(self, strike, maturity):
        # This is the CDF of any / all of the four OHLC processes (any selection
        # process of the model for that matter)
        x = np.log(np.asarray(strike) / self.spot_price)
        return norminvgauss.cdf(x, **self._norminvgauss_kwargs(maturity))

    def ppf(self, probability, maturity):
        # Similarly, the PPF for any / all of the OHLC processes
        x = norminvgauss.ppf(probability, **self._norminvgauss_kwargs(maturity))
        return self.spot_price * np.exp(x)

    def _norminvgauss_kwargs(self, maturity):
        alpha, beta, delta, mu = self._norminvgauss_params()
        loc = (mu + self._drift) * maturity
        scale = delta * maturity
        return {"a": scale * alpha, "b": scale * beta, "loc": loc, "scale": scale}

    def _norminvgauss_params(self):
        if self.gamma == 0 or self.sigma == 0 or abs(self.rho) == 1:
            raise ValueError(
                "norminvgauss params are undefined at gamma=0, sigma=0, or rho=+-1"
            )
        nu = self.gamma * self.sigma
        # From Mechkov (2015) p.5 without the time scaling
        alpha = 0.5 * (4 - 4 * self.rho * nu + nu**2) ** 0.5 / nu / (1 - self.rho**2)
        beta = -0.5 * (nu - 2 * self.rho) / nu / (1 - self.rho**2)
        delta = self.sigma * (1 - self.rho**2) ** 0.5 / self.gamma
        mu = -self.sigma * self.rho / self.gamma
        return alpha, beta, delta, mu

    def digital_put_forward_price(self, strike, maturity):
        return self.cdf(strike, maturity)
