# Relatorio dos trabalhos praticos de Metodos Numericos

**Autor:** Nuno Antunes  
**Implementacao:** Python 3, NumPy e Matplotlib

Os resultados completos e nao arredondados encontram-se em `results/results.json`.
Os tres enunciados originais encontram-se na pasta `enunciados/`.

## Trabalho pratico 1 - aritmetica de ponto flutuante e series

### 1. Epsilon da maquina

O algoritmo comeca em `eps=1` e divide sucessivamente por dois enquanto
`1 + eps/2 != 1`. Em precisao dupla IEEE 754 obteve-se

`eps = 2.220446049250313e-16`,

coincidente com `numpy.finfo(float).eps`. Este valor e a distancia entre 1 e o
numero representavel seguinte; nao e um limite uniforme para todo o eixo real.

### 2. Serie baseada em arcsin(1/2)

Foi usada diretamente a serie pedida,

`S = 6 sum [(2k)! / (4^k (k!)^2 (2k+1))] (0.5)^(2k+1)`.

Para evitar fatoriais muito grandes, cada termo e obtido do anterior pela razao

`t_(k+1)/t_k = ((2k+1)^2 / (2(k+1)(2k+3))) * 1/4`.

Todas estas razoes sao inferiores a 1/4. Logo, depois do termo `k`, a cauda
positiva e inferior a `(4/3)t_(k+1)`, que fornece o criterio de paragem.

| Tolerancia | Termos | Aproximacao | Erro efetivo |
|---:|---:|---:|---:|
| 1e-5 | 7 | 3.141589425319 | 3.2283e-6 |
| 1e-10 | 14 | 3.141592653515 | 7.4456e-11 |
| 1e-15 | 22 | 3.141592653590 | 8.8818e-16 |

### 3. Serie de Leibniz

Por ser alternada, a cauda depois de `n` termos e majorada por `4/(2n+1)`.
Assim, sao necessarios 200 000 termos para `1e-5`, 20 000 000 000 para `1e-10`
e 2 000 000 000 000 000 para `1e-15`. O primeiro calculo produz erro efetivo
aproximadamente `5.0e-6`. Os dois restantes sao assinalados pelo programa como
computacionalmente inviaveis, em vez de ocultar o custo ou declarar uma precisao
que nao foi atingida. Para `1e-15`, o numero pedido tambem se aproxima do limite
em que os efeitos de arredondamento em `float64` dominam.

A primeira serie e claramente superior: alcanca precisao proxima da maquina com
22 termos, enquanto a serie de Leibniz converge a uma taxa extremamente lenta.

## Trabalho pratico 2 - equacoes nao lineares

### 1. Zero de F

Para `F(x)=sin(x^2)+1.1-exp(-x)`, o grafico separa a menor raiz em
`I=[-0.2,-0.1]`, intervalo de amplitude `0.1`. Tem-se
`F(-0.2)=-0.0814134` e `F(-0.1)=0.00482892`, logo existe uma raiz por continuidade.

Em todo o intervalo, `min |F'(x)|` e aproximadamente `0.821723`, pelo que `F'`
nao se anula e a raiz e unica. Alem disso, `F''` permanece positiva, entre
`0.770599` e `0.894329`. Estas verificacoes sustentam a aplicabilidade dos dois
metodos. Para Newton escolhe-se o extremo que satisfaz `F(x0)F''(x0)>0`.

| Metodo | Aproximacao | Iteracoes | Garantia de erro |
|---|---:|---:|---:|
| Bissecao | -0.1053488523 | 25 | semi-amplitude < 5e-9 |
| Newton | -0.1053488514 | 2 | `|F(x)|/min|F'| < 5e-9` |

Newton e muito mais rapido neste problema, mas exige derivada, escolha adequada do
ponto inicial e controlo de que a iteracao permanece na regiao analisada.

### 2. Iteracao simples

As cinco formas foram executadas desde `x0=1.5` antes de analisar a convergencia,
como pedido. Para erro estimado `1e-12`:

| Forma | Resultado | Iteracoes | Explicacao |
|---|---|---:|---|
| g1 | diverge | 5 | iteradas crescem rapidamente |
| g2 | falha de dominio | 2 | o radicando torna-se negativo |
| g3 | converge | 43 | contracao, mas lenta |
| g4 | converge | 14 | contracao mais forte |
| g5 | converge | 5 | corresponde a iteracao de Newton |

As formas convergentes aproximam a raiz `1.365230013414`. Entre as apresentadas,
`g5` e a melhor pela convergencia quadratica local e pelo menor numero de iteracoes.

## Trabalho pratico 3 - interpolacao

### 1. Funcao x^2 + sin(6x)

Foram usados oito nos equidistantes `x_i=-1+2i/7`. O polinomio foi construido
pelas diferencas divididas de Newton. Para o spline natural, as incognitas
`M_i=s''(x_i)` satisfazem `M_0=M_7=0` e, nos nos interiores,

`h_(i-1)M_(i-1) + 2(h_(i-1)+h_i)M_i + h_i M_(i+1)
= 6[(f_(i+1)-f_i)/h_i - (f_i-f_(i-1))/h_(i-1)]`.

O sistema efetivamente construido esta guardado em `results/results.json`.

| x | Erro polinomial | Majorante polinomial | Erro spline | Majorante spline |
|---:|---:|---:|---:|---:|
| 0.1 | 0.001418 | 0.037289 | 0.005548 | 0.112453 |
| 0.9 | 0.299304 | 1.173471 | 0.094240 | 0.112453 |

Para o polinomio usou-se `max|f^(8)| <= 6^8` no resto de Lagrange. Para o spline
natural em malha uniforme usou-se o majorante classico `5 h^4 max|f''''|/384`,
com `max|f''''| <= 6^4`. Os majorantes sao conservadores, mas cobrem os erros
observados. Junto da extremidade (`x=0.9`) o spline e consideravelmente mais estavel.

### 2. Evaporacao em Adelaide

O polinomio global de grau 11 passa por todas as medicoes, mas oscila entre meses,
sobretudo junto das extremidades. O spline cubico natural preserva melhor a evolucao
sazonal gradual, usa informacao local e apresenta uma curva visualmente plausivel.
Por isso, o spline e a aproximacao mais aceitavel para estes dados. Nenhum dos dois
modelos deve ser extrapolado para fora dos meses 1 a 12.

## Conclusoes

Os exercicios mostram tres ideias comuns: uma formula matematicamente correta pode
ser numericamente ineficiente; garantias de convergencia importam tanto como uma
aproximacao; e interpolar exatamente os dados nao garante um comportamento razoavel
entre os nos. O codigo separa algoritmos, experiencias, graficos e testes para tornar
cada conclusao reproduzivel.
