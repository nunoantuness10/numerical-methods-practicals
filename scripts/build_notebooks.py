"""Build three executed notebooks without requiring a Jupyter server."""

from __future__ import annotations

import ast
import contextlib
import io
import os
from pathlib import Path

import nbformat as nbf

ROOT = Path(__file__).resolve().parents[1]


def execute(source: str, namespace: dict, count: int) -> list:
    tree = ast.parse(source)
    final_expression = (
        tree.body.pop() if tree.body and isinstance(tree.body[-1], ast.Expr) else None
    )
    stream = io.StringIO()
    outputs = []
    with contextlib.redirect_stdout(stream):
        exec(compile(tree, "<notebook>", "exec"), namespace)
        if final_expression:
            value = eval(
                compile(ast.Expression(final_expression.value), "<notebook>", "eval"), namespace
            )
            if value is not None:
                outputs.append(
                    nbf.v4.new_output(
                        "execute_result",
                        data={"text/plain": repr(value)},
                        execution_count=count,
                    )
                )
    if stream.getvalue():
        outputs.insert(0, nbf.v4.new_output("stream", name="stdout", text=stream.getvalue()))
    return outputs


NOTEBOOKS = [
    (
        "01_ponto_flutuante_e_series",
        "Trabalho pratico 1 - ponto flutuante e series",
        [
            (
                "markdown",
                "## Epsilon da maquina\n\nDividimos por dois ate `1 + eps/2` ser arredondado para 1.",
            ),
            (
                "code",
                "from numerical_methods.floating_point import machine_epsilon\nimport numpy as np\n{'algoritmo': machine_epsilon(), 'NumPy': np.finfo(float).eps}",
            ),
            (
                "markdown",
                "## Comparacao das series\n\nA primeira usa um majorante geometrico da cauda; Leibniz usa o teorema das series alternadas.",
            ),
            (
                "code",
                "from numerical_methods.series import arcsin_pi, leibniz_pi\nfrom dataclasses import asdict\ntolerancias = (1e-5, 1e-10, 1e-15)\n[{'tolerancia': t, 'arcsin': asdict(arcsin_pi(t)), 'leibniz': asdict(leibniz_pi(t))} for t in tolerancias]",
            ),
            (
                "markdown",
                "A enorme contagem teorica de Leibniz explica por que as duas menores tolerancias nao sao executadas por forca bruta.",
            ),
        ],
    ),
    (
        "02_equacoes_nao_lineares",
        "Trabalho pratico 2 - equacoes nao lineares",
        [
            (
                "markdown",
                "## Separacao e aplicabilidade\n\nO intervalo `[-0.2,-0.1]` tem amplitude 0.1 e mudanca de sinal. As derivadas nao mudam de sinal nesse intervalo.",
            ),
            (
                "code",
                "from numerical_methods.experiments import practical_2\nr = practical_2()\n{k: r[k] for k in ['interval', 'endpoint_values', 'derivative_minimum', 'second_derivative_range']}",
            ),
            (
                "markdown",
                "## Bissecao e Newton\n\nA bissecao usa a semi-amplitude; Newton usa o majorante residual `|F(x)|/m`.",
            ),
            ("code", "{k: r[k] for k in ['bisection', 'newton']}"),
            (
                "markdown",
                "![Separacao da raiz](../figures/tp2_root_separation.png)\n\n## Iteracoes simples\n\nExecutamos primeiro todas as formas desde `x0=1.5`, incluindo as que divergem.",
            ),
            (
                "code",
                "{name: {'convergiu': item['converged'], 'iteracoes': item['iterations'], 'motivo': item['reason'], 'valor': item['value']} for name, item in r['fixed_point'].items()}",
            ),
        ],
    ),
    (
        "03_interpolacao_e_splines",
        "Trabalho pratico 3 - interpolacao e splines",
        [
            (
                "markdown",
                "## Construcao\n\nO polinomio usa diferencas divididas de Newton. O spline natural resulta do sistema para os momentos `M_i=s''(x_i)`, com `M_0=M_n=0`.",
            ),
            (
                "code",
                "from numerical_methods.experiments import practical_3\nr = practical_3()\n{'nos': r['nodes'], 'coeficientes_Newton': r['newton_coefficients'], 'momentos_spline': r['spline_second_derivatives']}",
            ),
            ("markdown", "## Estimativas e majorantes"),
            ("code", "r['point_estimates']"),
            (
                "markdown",
                "![Funcao, aproximacoes e erros](../figures/tp3_function_interpolation.png)\n\n## Evaporacao\n\nO spline e mais plausivel entre os meses porque evita as oscilacoes do polinomio global de grau 11.",
            ),
            (
                "code",
                "{'coeficientes_Newton': r['evaporation_newton_coefficients'], 'momentos_spline': r['evaporation_spline_second_derivatives']}",
            ),
            ("markdown", "![Interpolacao da evaporacao](../figures/tp3_evaporation.png)"),
        ],
    ),
]


def build() -> None:
    original = Path.cwd()
    os.chdir(ROOT)
    try:
        for filename, title, specification in NOTEBOOKS:
            notebook = nbf.v4.new_notebook()
            notebook.cells.append(
                nbf.v4.new_markdown_cell(
                    f"# {title}\n\n**Nuno Antunes**\n\nNotebook executado e reproduzivel. O enunciado original esta em `../enunciados/`."
                )
            )
            namespace = {"__name__": "__main__"}
            execution_count = 0
            for kind, source in specification:
                if kind == "markdown":
                    notebook.cells.append(nbf.v4.new_markdown_cell(source))
                    continue
                execution_count += 1
                notebook.cells.append(
                    nbf.v4.new_code_cell(
                        source,
                        execution_count=execution_count,
                        outputs=execute(source, namespace, execution_count),
                    )
                )
            notebook.metadata.kernelspec = {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            }
            notebook.metadata.language_info = {"name": "python", "version": "3.12"}
            nbf.validate(notebook)
            nbf.write(notebook, ROOT / "notebooks" / f"{filename}.ipynb")
            print("built", filename)
    finally:
        os.chdir(original)


if __name__ == "__main__":
    build()
