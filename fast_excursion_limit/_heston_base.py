import numpy as np

from fast_excursion_limit import defaults


class HestonBase:
    _EXAMPLE_PARAMS = defaults.EXAMPLE_PARAMS_FEH

    def __init__(
        self,
        spot_price,
        domestic_rate,
        foreign_rate,
        sigma,
        rho,
        gamma,
    ):
        self.spot_price = spot_price
        self.domestic_rate = domestic_rate
        self.foreign_rate = foreign_rate
        self.sigma = sigma
        self.rho = rho
        self.gamma = gamma
        self._check_params()

    def _check_params(self):
        assert self.spot_price > 0
        assert self.sigma >= 0
        assert -1 <= self.rho <= 1
        assert self.gamma >= 0

    @classmethod
    def example(cls):
        return cls(**cls._EXAMPLE_PARAMS)

    @property
    def _drift(self):
        return self.domestic_rate - self.foreign_rate

    def simulate(self, maturity, step_size, full_output=False):
        Y, W, x = self._simulate_time(maturity, step_size)
        Z = self._simulate_price(Y, W, x)
        if full_output:
            return Z, Y, W, x
        return Z, Y

    def _simulate_price(self, Y, W, x):
        B = (1.0 - self.rho**2) ** 0.5 * W[:, 0] + self.rho * W[:, 1]
        Z = self.spot_price * np.exp(
            self._drift * Y + self.sigma * B - 0.5 * self.sigma**2 * x
        )
        return Z

    def _simulate_time(self, maturity, step_size):
        Y, W, x = [0.0], [(0.0, 0.0)], [0.0]
        # Iterate until Y strictly exceeds maturity
        while Y[-1] <= maturity:
            time_next, brownian_next, space_next = self._simulate_next(
                time_prev=Y[-1],
                brownian_prev=W[-1],
                space_prev=x[-1],
                step_size=step_size,
            )
            Y.append(time_next)
            W.append(brownian_next)
            x.append(space_next)
        return np.array(Y), np.array(W), np.array(x)

    def _simulate_next(self, time_prev, brownian_prev, space_prev, step_size):
        # This is where HestonRandomODE and FastExcursionHeston differ, although both
        # make use of the following (inefficient) _brownian_next method in order to keep
        # random numbers aligned.
        raise NotImplementedError

    def _brownian_next(self, brownian_prev, step_size):
        brownian_step = np.random.standard_normal(2) * step_size**0.5
        W0 = brownian_prev[0] + brownian_step[0]
        W1 = brownian_prev[1] + brownian_step[1]
        return W0, W1

    def __eq__(self, other) -> bool:
        return type(self) is type(other) and vars(self) == vars(other)

    def __str__(self) -> str:
        param_lines = [f'    "{k}": {v:.4f},' for k, v in vars(self).items()]
        lines = [
            "params = {",
            *param_lines,
            "}",
            f"model = {self.__class__.__name__}(**params)",
        ]
        return "\n".join(lines)
