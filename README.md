<div align="center">

# Newton Method — Professional Suite

</div>

<div align="center">

![Project Status](https://img.shields.io/badge/Status-Completed-brightgreen?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)

</div>

---

A high-precision numerical analysis desktop application designed for finding and refining roots of non-linear functions. This suite combines the symbolic power of SymPy with the high-precision numerical capabilities of mpmath, wrapped in a modern, user-centric interface.

---

## Technical Overview

The application implements the **Newton-Raphson method** and the **Secant method** to solve equations. It distinguishes itself by performing an initial global sweep to identify root-containing intervals before applying iterative refinement, ensuring high convergence reliability even for complex functions.

### Key Components

* **Symbolic Engine**: Utilizes SymPy for automated differentiation and symbolic root solving.
* **Numerical Kernel**: Employs mpmath for arbitrary-precision floating-point arithmetic.
* **Expression Translation**: Includes a translation layer that maps Portuguese mathematical notation (e.g., `bsen`, `tg`, `raiz`) to standard Python/SymPy syntax.
* **Graphical Interface**: A custom-styled Tkinter implementation featuring a modern flat-design aesthetic and asynchronous-style result reporting.

---

## Project Structure

The project is organized into modular components to separate logic from the presentation layer:

| Module | Responsibility |
| :--- | :--- |
| `math_core.py` | Handles expression parsing, symbolic differentiation, and numerical solvers (Newton/Secant). |
| `main.py` | Execute the program. |
| `utils.py` | Provides auxiliary formatting functions for mathematical output. |
| `interface.py` | Create the interface with Tkinter for the software. |

---

## Core Functionalities

### 1. Robust Expression Parsing
The system interprets raw string inputs, handles power notation (`^` to `**`), and supports equality expressions (e.g., `sin(x) = x/2`). It includes a localized dictionary to ensure accessibility for users familiar with Portuguese mathematical shorthand.

### 2. Intelligent Root Discovery
Instead of relying solely on a single initial guess, the suite performs a discretized sweep of the function's domain to detect sign changes. This allows the application to identify multiple roots within a specified range automatically.

### 3. Iterative Refinement
Once a potential root is identified, the Newton-Raphson algorithm refines the value until it meets the user-defined tolerance (defaulting to 1e-10). If the derivative is zero or convergence fails, the system provides detailed diagnostic feedback in the output console.

### 4. Advanced Filtering
Users can filter results based on real-value properties:
* **All**: Returns every discovered root.
* **Positive**: Filters for x > 0.
* **Negative**: Filters for x < 0.

---

## Installation and Setup

The project uses `uv` for modern, fast Python package management.

### Prerequisites
* Python 3.10 or higher
* `uv` package manager

### Environment Configuration

1. **Initialize the virtual environment:**
```bash
uv venv
```

3. **Activate the environment:**
* Windows: ``` .venv\Scripts\activate ```
* macOS/Linux: ``` source .venv/bin/activate ```

3. **Install dependencies:**
```bash
uv add sympy mpmath
```

---

## Usage

To launch the application, execute the main script:

```bash
python app.py
```

### Input Parameters
* **Function f(x)**: The equation to be solved.
* **Initial Guess (x₀)**: The starting point for the numerical refinement.
* **Max Iterations**: Limits the solver to prevent infinite loops in divergent cases.
* **Tolerance**: The desired precision for the final root.

---

## Development Standards

The codebase follows standard PEP 8 guidelines for Python. The UI implementation leverages `ttk` (Themed Tkinter) with custom style mapping to provide a professional look and feel consistent with modern operating systems without the overhead of heavy web-based frameworks.

## Author

**Elyon Oliveira dos Santos**  
Software Developer
