import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText
import sympy as sp
import math_core
import utils

# Define a classe principal da interface gráfica herdando de Tk
class NewtonApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Método de Newton — Professional Suite")
        self.geometry("1000x680")
        self.configure(bg="#f4f6f9")
        self.style = ttk.Style(self)
        self._setup_style()
        self._build_ui()

    # Configura o tema visual, paleta de cores e tipografia para um visual 'Flat' moderno
    def _setup_style(self):
        try:
            self.style.theme_use('clam')
        except:
            pass

        # Cores e Fontes
        bg_color = "#f4f6f9"
        card_bg = "#ffffff"
        primary_color = "#2563eb"
        primary_hover = "#1d4ed8"
        secondary_color = "#64748b"
        secondary_hover = "#475569"
        text_color = "#1e293b"
        muted_text = "#64748b"
        border_color = "#cbd5e1"

        # Configurações gerais
        self.style.configure('TFrame', background=bg_color)
        self.style.configure('Card.TFrame', background=card_bg, relief='flat', borderwidth=0)
        
        # Labels
        self.style.configure('Header.TLabel', background=bg_color, foreground=text_color, font=('Segoe UI', 18, 'bold'))
        self.style.configure('Label.TLabel', background=card_bg, foreground=muted_text, font=('Segoe UI', 10, 'bold'))
        self.style.configure('ResultHeader.TLabel', background=card_bg, foreground=text_color, font=('Segoe UI', 12, 'bold'))

        # Inputs (Entry e Combobox)
        self.style.configure('Entry.TEntry', 
            fieldbackground='#f8fafc', 
            foreground=text_color, 
            padding=5, 
            relief='flat',
            borderwidth=1,
            bordercolor=border_color
        )
        self.style.map('Entry.TEntry',
            bordercolor=[('focus', primary_color)],
            lightcolor=[('focus', primary_color)]
        )

        # Botão Primário (Calcular) - Azul Sólido
        self.style.configure('Primary.TButton',
            background=primary_color,
            foreground='white',
            font=('Segoe UI', 10, 'bold'),
            borderwidth=0,
            focuscolor='none',
            padding=(20, 10)
        )
        self.style.map('Primary.TButton', 
            background=[('active', primary_hover), ('pressed', primary_hover)]
        )

        # Botão Secundário (Limpar) - Cinza Discreto
        self.style.configure('Secondary.TButton',
            background='#e2e8f0',
            foreground=secondary_color,
            font=('Segoe UI', 10, 'bold'),
            borderwidth=0,
            focuscolor='none',
            padding=(15, 10)
        )
        self.style.map('Secondary.TButton', 
            background=[('active', '#cbd5e1'), ('pressed', '#94a3b8')],
            foreground=[('active', '#334155')]
        )

    # Constrói a estrutura de layouts com foco em espaçamento e hierarquia visual
    def _build_ui(self):
        # Container principal com margens generosas
        main_container = ttk.Frame(self, padding=30)
        main_container.pack(fill='both', expand=True)

        # Cabeçalho da Aplicação
        header_frame = ttk.Frame(main_container)
        header_frame.pack(fill='x', pady=(0, 20))
        ttk.Label(header_frame, text="Análise Numérica / Newton-Raphson", style='Header.TLabel').pack(anchor='w')
        ttk.Label(header_frame, text="Insira os parâmetros abaixo para calcular as raízes.", background="#f4f6f9", foreground="#64748b", font=('Segoe UI', 10)).pack(anchor='w')

        # Cartão de Entradas (Card Branco com sombra simulada via borda sutil)
        input_card = ttk.Frame(main_container, style='Card.TFrame', padding=25)
        input_card.pack(fill='x', pady=(0, 20))

        # Configuração do Grid do Input
        input_card.columnconfigure(0, weight=2) # Coluna da função maior
        input_card.columnconfigure(1, weight=1)
        input_card.columnconfigure(2, weight=1)

        # Linha 1: Função (Ocupa mais espaço)
        ttk.Label(input_card, text="FUNÇÃO f(x)", style='Label.TLabel').grid(row=0, column=0, sticky='w', pady=(0, 5))
        self.func_entry = ttk.Entry(input_card, style='Entry.TEntry', font=('Consolas', 11))
        self.func_entry.insert(0, 'sin(x) - x/2')
        self.func_entry.grid(row=1, column=0, sticky='ew', padx=(0, 15), ipady=4)

        # Linha 1: Chute Inicial
        ttk.Label(input_card, text="CHUTE INICIAL (x₀)", style='Label.TLabel').grid(row=0, column=1, sticky='w', pady=(0, 5))
        self.x0_entry = ttk.Entry(input_card, style='Entry.TEntry', font=('Consolas', 11))
        self.x0_entry.insert(0, '1')
        self.x0_entry.grid(row=1, column=1, sticky='ew', padx=(0, 15), ipady=4)

        # Linha 1: Iterações
        ttk.Label(input_card, text="MÁX. ITERAÇÕES", style='Label.TLabel').grid(row=0, column=2, sticky='w', pady=(0, 5))
        self.max_iter_entry = ttk.Entry(input_card, style='Entry.TEntry', font=('Consolas', 11))
        self.max_iter_entry.insert(0, '50')
        self.max_iter_entry.grid(row=1, column=2, sticky='ew', ipady=4)

        # Separador visual (espaço em branco)
        ttk.Frame(input_card, style='Card.TFrame', height=20).grid(row=2, column=0, columnspan=3)

        # Linha 2: Derivada (Readonly)
        ttk.Label(input_card, text="DERIVADA f'(x) (Calculada)", style='Label.TLabel').grid(row=3, column=0, sticky='w', pady=(0, 5))
        self.deriv_var = tk.StringVar()
        deriv_entry = ttk.Entry(input_card, textvariable=self.deriv_var, state='readonly', style='Entry.TEntry', font=('Consolas', 10))
        deriv_entry.grid(row=4, column=0, sticky='ew', padx=(0, 15), ipady=4)

        # Linha 2: Tolerância
        ttk.Label(input_card, text="TOLERÂNCIA", style='Label.TLabel').grid(row=3, column=1, sticky='w', pady=(0, 5))
        self.tol_entry = ttk.Entry(input_card, style='Entry.TEntry', font=('Consolas', 11))
        self.tol_entry.insert(0, '1e-10')
        self.tol_entry.grid(row=4, column=1, sticky='ew', padx=(0, 15), ipady=4)

        # Linha 2: Filtro
        ttk.Label(input_card, text="FILTRO DE RAÍZES", style='Label.TLabel').grid(row=3, column=2, sticky='w', pady=(0, 5))
        self.filtro_var = tk.StringVar(value='Todas')
        combo = ttk.Combobox(input_card, textvariable=self.filtro_var, values=['Todas', 'Positivas', 'Negativas'], state='readonly', font=('Segoe UI', 10))
        combo.grid(row=4, column=2, sticky='ew', ipady=4)

        # Área de Ações (Botões) - Alinhada à direita e separada
        action_frame = ttk.Frame(input_card, style='Card.TFrame')
        action_frame.grid(row=5, column=0, columnspan=3, sticky='e', pady=(25, 0))

        # Botão Limpar (Estratégico: Limpa os campos para nova análise)
        self.btn_clear = ttk.Button(action_frame, text="LIMPAR DADOS", style='Secondary.TButton', cursor='hand2', command=self.limpar_campos)
        self.btn_clear.pack(side='left', padx=(0, 10))

        # Botão Calcular (Destaque principal)
        self.btn_calc = ttk.Button(action_frame, text="CALCULAR RAÍZES", style='Primary.TButton', cursor='hand2', command=self.calcular)
        self.btn_calc.pack(side='left')

        # Área de Resultados
        result_container = ttk.Frame(main_container, style='Card.TFrame', padding=25)
        result_container.pack(fill='both', expand=True)

        ttk.Label(result_container, text="Console de Saída", style='ResultHeader.TLabel').pack(anchor='w', pady=(0, 10))

        self.output = ScrolledText(result_container, font=('Consolas', 11), wrap='word', bd=0, bg="#f8fafc", fg="#334155", highlightthickness=0)
        self.output.pack(fill='both', expand=True)

    # Reseta todos os campos para os valores padrão e limpa o console
    def limpar_campos(self):
        self.func_entry.delete(0, tk.END)
        self.func_entry.insert(0, '')
        
        self.deriv_var.set('')
        
        self.x0_entry.delete(0, tk.END)
        self.x0_entry.insert(0, '1')
        
        self.tol_entry.delete(0, tk.END)
        self.tol_entry.insert(0, '1e-10')
        
        self.max_iter_entry.delete(0, tk.END)
        self.max_iter_entry.insert(0, '50')
        
        self.filtro_var.set('Todas')
        
        self.output.configure(state='normal')
        self.output.delete('1.0', tk.END)
        self.output.configure(state='disabled')
        
        # Foca no primeiro campo para agilizar a digitação
        self.func_entry.focus()

    # Atualiza a área de texto com os resultados processados
    def print_results(self, lines):
        self.output.configure(state='normal')
        self.output.delete('1.0', tk.END)
        for line in lines:
            self.output.insert(tk.END, line + '\n')
        self.output.configure(state='disabled')

    # Orquestra a captura de dados, cálculo matemático e exibição dos resultados
    def calcular(self):
        try:
            expr_str = self.func_entry.get()
            if not expr_str.strip():
                messagebox.showwarning("Atenção", "Por favor, insira uma função.")
                return

            expr = math_core.interpretar_expressao(expr_str)
            x = sp.Symbol('x')

            # Calcula a derivada simbolicamente
            expr_temp = expr.lhs - expr.rhs if isinstance(expr, sp.Equality) else expr
            deriv = sp.simplify(sp.diff(expr_temp, x))
            self.deriv_var.set(str(deriv))

            # Captura e converte os parâmetros da interface
            try:
                x0 = complex(self.x0_entry.get().replace('j', 'J'))
            except:
                x0 = 1
            tol = float(self.tol_entry.get())
            max_iter = int(self.max_iter_entry.get())
            filtro = self.filtro_var.get()

            # Tenta encontrar raízes simbólicas exatas
            try:
                if isinstance(expr, sp.Equality):
                    raizes_s = sp.solve(expr, x)
                else:
                    raizes_s = sp.roots(expr, multiple=True)
            except:
                raizes_s = []

            # Busca raízes numéricas caso a solução simbólica falhe ou seja insuficiente
            if not raizes_s:
                f_mpf = sp.lambdify(x, expr_temp, modules=['mpmath', 'sympy'])
                lim = 60
                if filtro == 'Positivas':
                    rnums = math_core.find_roots_numeric(f_mpf, (1e-6, lim))
                elif filtro == 'Negativas':
                    rnums = math_core.find_roots_numeric(f_mpf, (-lim, -1e-6))
                else:
                    rnums = sorted(math_core.find_roots_numeric(f_mpf, (-lim, -1e-6)) + math_core.find_roots_numeric(f_mpf, (1e-6, lim)))
                raizes_s = [sp.N(r) for r in rnums]

            # Aplica o filtro selecionado pelo usuário nas raízes encontradas
            filtradas = []
            for r in raizes_s:
                try:
                    c = complex(r)
                except:
                    continue
                if filtro == 'Positivas' and c.real > 0 and abs(c.imag) < 1e-8:
                    filtradas.append(r)
                elif filtro == 'Negativas' and c.real < 0 and abs(c.imag) < 1e-8:
                    filtradas.append(r)
                elif filtro == 'Todas':
                    filtradas.append(r)

            if not filtradas:
                self.print_results(["Status: Nenhuma raiz encontrada no intervalo padrão de busca."])
                return

            # Prepara as funções numéricas para o método de Newton
            f_num = sp.lambdify(x, expr_temp, modules=['cmath', 'sympy'])
            df_num = sp.lambdify(x, deriv, modules=['cmath', 'sympy'])

            linhas = [
                "─" * 60,
                f" ANÁLISE DA FUNÇÃO: {expr_str}",
                f" DERIVADA: {deriv}",
                "─" * 60,
                ""
            ]

            # Itera sobre as raízes encontradas para refinar e formatar a saída
            for i, r in enumerate(filtradas, 1):
                exato = utils.format_root_display(r)
                try:
                    chute = float(r.evalf())
                except:
                    chute = x0
                
                try:
                    newt = math_core.newton_method(f_num, df_num, chute, tol, max_iter)
                    newt_disp = utils.format_root_display(newt)
                except Exception as e:
                    newt_disp = f"Erro na convergência: {e}"
                
                try:
                    dfv = df_num(chute)
                    dfv_disp = utils.format_root_display(dfv)
                except:
                    dfv_disp = 'n/a'

                linhas.append(f"RAIZ #{i}")
                linhas.append(f"  • Aproximação Inicial: {round(float(r.evalf()), 12)}")
                linhas.append(f"  • Refinamento Newton : {newt_disp}")
                linhas.append(f"  • Solução Simbólica  : {exato}")
                linhas.append(f"  • f'(raiz)           : {dfv_disp}")
                linhas.append("-" * 40)
                linhas.append("")

            self.print_results(linhas)

        except Exception as e:
            messagebox.showerror("Erro de Execução", f"Ocorreu um erro ao processar:\n{str(e)}")