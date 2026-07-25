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
        Y, W1, x = self._simulate_time(maturity, step_size)
        Z, W0 = self._simulate_price(Y, W1, x)
        if full_output:
            return Z, Y, W0, W1, x
        return Z, Y

    def _simulate_price(self, Y, W1, x):
        step_sizes = np.diff(x)
        num_steps = len(step_sizes)
        brownian_steps = np.random.normal(size=num_steps) * step_sizes**0.5
        W0 = np.zeros_like(W1)
        W0[1:] = np.cumsum(brownian_steps)
        W = self.rho * W1 + (1.0 - self.rho**2) ** 0.5 * W0
        Z = self.spot_price * np.exp(
            self._drift * Y + self.sigma * W - 0.5 * self.sigma**2 * x
        )
        return Z, W0

    def _simulate_time(self, maturity, step_size):
        Y, W1, x = [0.0], [0.0], [0.0]
        # Iterate until Y strictly exceeds maturity
        while Y[-1] <= maturity:
            time_next, brownian_next, space_next = self._simulate_next(
                time_prev=Y[-1],
                brownian_prev=W1[-1],
                space_prev=x[-1],
                step_size=step_size,
            )
            Y.append(time_next)
            W1.append(brownian_next)
            x.append(space_next)
        return np.array(Y), np.array(W1), np.array(x)

    def _simulate_next(self, time_prev, brownian_prev, space_prev, step_size):
        # This is where HestonRandomODE and FastExcursionHeston differ
        raise NotImplementedError

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
