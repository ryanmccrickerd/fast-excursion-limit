# Fast-excursion limit of the Heston model

[![CI](https://github.com/ryanmccrickerd/fast-excursion-limit/actions/workflows/ci.yml/badge.svg)](https://github.com/ryanmccrickerd/fast-excursion-limit/actions/workflows/ci.yml)

Code and notebooks accompanying the article *Fast-excursion limit of the Heston model* ([arXiv:2606.06737](https://arxiv.org/abs/2606.06737)). The notebooks in `notebooks/figures/` generate the article's figures, saved to `plots/`. For example:

<p align="center"><img src="plots/figure-1.png" alt="Figure 1" width="600"></p>
<p align="center">Figure 1: Two classical Heston price paths (dark) converging to their <em>interval-valued</em> 'fast-excursion limit' (light) as reversion speed goes to infinity.</p>

## Setup

```sh
pip install -e "."
```

Notebooks assume you have a way to open `.ipynb` files (VS Code with the Jupyter extension, JupyterLab, classic Notebook, etc.).

Figures use Latin Modern Roman, bundled in `fonts/` and registered by `plot_config`. These fonts are separately licensed.

## Usage

Start with [`notebooks/intro.ipynb`](notebooks/intro.ipynb), which simulates `FastExcursionHeston`. The package also provides `HestonRandomODE`, which is a random ODE formulation of the Heston model that facilitates visualisation of pathwise (i.e. almost sure) convergence, as in Figure 1 above.

The notebooks in `notebooks/figures/` are written for humans. [`notebooks/figures.ipynb`](notebooks/figures.ipynb) is rather for the [`figures.yml`](.github/workflows/figures.yml) workflow.

Generally, simulation schemes are slow. Comments in the code explain why. Claude can e.g. speed up Figure 5 by 20x, but models' connections are compromised.

## Citation and contact

To cite this work, see [`CITATION.cff`](CITATION.cff). Questions and comments to [ryan.mccrickerd@gmail.com](mailto:ryan.mccrickerd@gmail.com).

Developed with [Claude Code](https://claude.com/claude-code) (Anthropic).
