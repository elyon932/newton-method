import sympy as sp
import mpmath as mp
import re

# Traduz termos matemáticos em português para a sintaxe em inglês compatível com as bibliotecas
def traduz_funcoes(expr_str):
    traducoes = {
        r"\\bsen\\b": "sin",
        r"\\btg\\b": "tan",
        r"\\btangente\\b": "tan",
        r"\\bcotg\\b": "cot",
        r"\\bsec\\b": "sec",
        r"\\bcossec\\b": "csc",
        r"\\blogaritmo\\b": "log",
        r"\\bln\\b": "log",
        r"\\braiz\\b": "sqrt",
        r"π": "pi",
    }
    for padrao, repl in traducoes.items():
        expr_str = re.sub(padrao, repl, expr_str, flags=re.IGNORECASE)
    return expr_str

# Interpreta a string de entrada e converte para uma expressão simbólica do SymPy
def interpretar_expressao(expr_str):
    expr_str = traduz_funcoes(expr_str).replace('^', '**').replace('ln(', 'log(')
    try:
        if '=' in expr_str:
            L, R = expr_str.split('=', 1)
            return sp.Eq(sp.sympify(L), sp.sympify(R))
        return sp.sympify(expr_str)
    except Exception as e:
        raise ValueError(f"Erro ao interpretar expressão: {e}")

# Executa o algoritmo numérico de Newton-Raphson para encontrar a raiz aproximada
def newton_method(f, df, x0, tol, max_iter):
    x = x0
    for _ in range(max_iter):
        fx, dfx = f(x), df(x)
        if dfx == 0:
            raise ZeroDivisionError("Derivada igual a zero.")
        x_new = x - fx / dfx
        if abs(x_new - x) < tol:
            return x_new
        x = x_new
    raise Exception("Máximo de iterações atingido.")

# Realiza uma varredura numérica no intervalo para identificar intervalos que contêm raízes
def find_roots_numeric(expr_func, search_range=(0, 100), samples=2000, max_roots=10):
    a, b = search_range
    xs = [a + (b - a) * i / samples for i in range(samples + 1)]
    vals = []
    
    # Avalia a função em múltiplos pontos do intervalo discretizado
    for x in xs:
        try:
            v = expr_func(x)
            vals.append(v if mp.isfinite(v) else None)
        except:
            vals.append(None)

    intervals = []
    
    # Identifica mudanças de sinal que indicam a presença de uma raiz
    for i in range(len(xs) - 1):
        v1, v2 = vals[i], vals[i+1]
        if v1 is None or v2 is None:
            continue
        if v1 == 0:
            intervals.append((xs[i], xs[i]))
        elif v1 * v2 < 0:
            intervals.append((xs[i], xs[i+1]))

    roots = []
    
    # Refina a busca da raiz dentro dos intervalos identificados usando Secante ou Newton
    for (l, r) in intervals:
        if len(roots) >= max_roots:
            break
        guess = (l + r) / 2 if l != r else l
        root = None
        for shift in (0, 1e-6, -1e-6, 1e-3, -1e-3):
            try:
                root = mp.findroot(expr_func, guess + shift, method='secant', tol=1e-12)
                break
            except:
                try:
                    root = mp.findroot(expr_func, guess + shift, method='newton', tol=1e-12)
                    break
                except:
                    pass
        
        # Armazena a raiz se ela for válida e única
        if root is not None:
            try:
                r_approx = float(mp.nstr(root, 12))
                if not any(abs(r_approx - rr) < 1e-8 for rr in roots):
                    roots.append(r_approx)
            except:
                pass
                
    return sorted(roots)[:max_roots]