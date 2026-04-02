import sympy as sp

# Formata a exibição de números complexos ou expressões simbólicas para uma string legível
def format_root_display(r):
    if isinstance(r, sp.Expr) and not isinstance(r, sp.Float):
        try:
            ex = sp.simplify(r)
            ap = sp.N(r, 12)
            return f"{ex} ≈ {ap}"
        except:
            return str(r)
    
    try:
        c = complex(r.evalf()) if hasattr(r, 'evalf') else complex(r)
    except:
        return str(r)
        
    if abs(c.imag) < 1e-10:
        return str(round(c.real, 12))
        
    return f"{round(c.real, 12)} {'+' if c.imag >= 0 else '-'} {abs(round(c.imag, 12))}j"