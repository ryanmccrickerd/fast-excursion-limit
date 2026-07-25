import numpy as np
from scipy.stats import norminvgauss

from fast_excursion_limit._heston_base import HestonBase


class FastExcursionHeston(HestonBase):
    def _simulate_next(self, time_prev, brownian_prev, space_prev, step_size):
        space_next = space_prev + step_size
        brownian_next = brownian_prev + np.random.normal() * step_size**0.5
        time_next = max(time_prev, space_next - self.gamma * brownian_next)
        return time_next, brownian_next, space_next

    def cdf(self, strike, maturity):
        x = np.log(np.asarray(strike) / self.spot_price)
        return norminvgauss.cdf(x, **self._norminvgauss_kwargs(maturity))

    def ppf(self, probability, maturity):
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
        # straight from Mechkov (2015) p.5 without the time scaling
        nu = self.gamma * self.sigma
        alpha = 0.5 * (4 - 4 * self.rho * nu + nu**2) ** 0.5 / nu / (1 - self.rho**2)
        beta = -0.5 * (nu - 2 * self.rho) / nu / (1 - self.rho**2)
        delta = self.sigma * (1 - self.rho**2) ** 0.5 / self.gamma
        mu = -self.sigma * self.rho / self.gamma
        return alpha, beta, delta, mu

    def digital_put_forward_price(self, strike, maturity):
        return self.cdf(strike, maturity)
