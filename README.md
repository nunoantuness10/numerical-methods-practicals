# Numerical Methods Practicals

Reproducible Python solutions to three practical sheets from *Metodos Numericos
(M2039)*. The repository focuses on transparent algorithms, numerical error bounds,
diagnostic plots and repeatable results.

## Contents

- `enunciados/`: the three original assignment PDFs
- `src/numerical_methods/`: reusable implementations
- `notebooks/`: executed, step-by-step analyses in Portuguese
- `docs/relatorio.md`: consolidated discussion and conclusions
- `figures/`: generated root-finding and interpolation plots
- `results/results.json`: machine-readable numerical results
- `tests/`: automated correctness tests

The interpolation polynomial uses Newton divided differences. The natural cubic
spline is assembled directly from its tridiagonal moment equations; `numpy.linalg.solve`
is used only to solve that linear system, following the assignment constraint.

## macOS setup

```bash
brew install python@3.12
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e '.[dev]'
```

Run every experiment and regenerate the figures:

```bash
numerical-lab
```

Rebuild the executed notebooks:

```bash
python scripts/build_notebooks.py
```

Run quality checks:

```bash
ruff check .
pytest -q
```

## Important numerical observation

The Leibniz series has a rigorous remainder bound of `4/(2n+1)` after `n` terms.
It therefore needs roughly 20 billion terms for `1e-10` and 2 quadrillion for
`1e-15`. The program reports those requirements instead of pretending that an
impractical computation completed. This slow convergence is itself a central result.

## Author

Nuno Antunes

