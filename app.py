import streamlit as st
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor

# ==========================================
# CONFIGURACIÓN Y TÍTULOS
# ==========================================
st.set_page_config(page_title="Proyecto de Integrales", layout="wide")

st.title("Modelado Matemático: Integrales Definidas e Indefinidas")
st.markdown("""
**Autor:** Rodvin Eduardo García Sutuj (090-21-16867)  
**Asignatura:** Matemática Avanzada / Cálculo  
""")

# ==========================================
# TECLADO VIRTUAL Y MEMORIA
# ==========================================
if "ecuacion" not in st.session_state:
    st.session_state.ecuacion = "1/x + cos(x) - x^2"

def agregar_texto(texto):
    st.session_state.ecuacion += texto

def limpiar_texto():
    st.session_state.ecuacion = ""

st.markdown("### Teclado Matemático Rápido")
col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    st.button("x²", on_click=agregar_texto, args=("x^2",), use_container_width=True)
    st.button("sin( )", on_click=agregar_texto, args=("sin(",), use_container_width=True)
    st.button("arcsin( )", on_click=agregar_texto, args=("asin(",), use_container_width=True)
with col2:
    st.button("x³", on_click=agregar_texto, args=("x^3",), use_container_width=True)
    st.button("cos( )", on_click=agregar_texto, args=("cos(",), use_container_width=True)
    st.button("arccos( )", on_click=agregar_texto, args=("acos(",), use_container_width=True)
with col3:
    st.button("√x", on_click=agregar_texto, args=("sqrt(x)",), use_container_width=True)
    st.button("tan( )", on_click=agregar_texto, args=("tan(",), use_container_width=True)
    st.button("arctan( )", on_click=agregar_texto, args=("atan(",), use_container_width=True)
with col4:
    st.button("eˣ", on_click=agregar_texto, args=("exp(x)",), use_container_width=True)
    st.button("π", on_click=agregar_texto, args=("pi",), use_container_width=True)
    st.button("| x |", on_click=agregar_texto, args=("Abs(",), use_container_width=True)
with col5:
    st.button("ln( )", on_click=agregar_texto, args=("log(",), use_container_width=True)
    st.button("( )", on_click=agregar_texto, args=("()",), use_container_width=True)
    st.button(" , ", on_click=agregar_texto, args=(",",), use_container_width=True)
with col6:
    st.button("1/x", on_click=agregar_texto, args=("1/x",), use_container_width=True)
    st.button(" x ", on_click=agregar_texto, args=("x",), use_container_width=True)
    st.button("Limpiar 🗑️", on_click=limpiar_texto, use_container_width=True)

# ==========================================
# ENTRADA VISUAL DE LA FUNCIÓN
# ==========================================
st.markdown("### Ingresa la función f(x):")
col_simbolo, col_entrada, col_dx = st.columns([0.5, 5, 0.5])

with col_simbolo:
    st.markdown("<h1 style='text-align: right; margin-top: -15px;'>∫</h1>", unsafe_allow_html=True)
with col_entrada:
    funcion_input = st.text_input("f(x)", key="ecuacion", label_visibility="collapsed")
with col_dx:
    st.markdown("<h3 style='text-align: left; margin-top: 5px;'>dx</h3>", unsafe_allow_html=True)

# Guía desplegable de ayuda
with st.expander("💡 Guía para escribir funciones manualmente"):
    st.markdown(r"""
    Si prefieres usar tu teclado físico en lugar de los botones rápidos, utiliza este formato:
    * **Trigonometría:** Para $\int \sin(2x) dx$, ingresa **`sin(2x)`**.
    * **Trigonometría Inversa:** Para $\int \arcsin(x) dx$, ingresa **`asin(x)`**, **`acos(x)`** o **`atan(x)`**.
    * **Logaritmo Natural:** Para $\int \ln(x) dx$, ingresa **`log(x)`** (el sistema lo toma como base *e*).
    * **Exponenciales:** Para $\int e^{3x} dx$, ingresa **`exp(3x)`**.
    * **Raíces Cuadradas:** Para $\int \sqrt{x} dx$, ingresa **`sqrt(x)`**.
    * **Valor Absoluto:** Para $\int |x| dx$, ingresa **`Abs(x)`**.
    * **Fracciones y Términos:** Para $\int (\frac{1}{x} + 4x^3) dx$, ingresa **`1/x + 4x^3`**.
    """)

# Reglas de traducción matemática
transformaciones = standard_transformations + (implicit_multiplication_application, convert_xor)
x = sp.Symbol('x')

st.markdown("---")

# ==========================================
# PESTAÑAS DE CÁLCULO
# ==========================================
tab_indefinida, tab_definida = st.tabs(["1. Integrales Indefinidas (Antiderivadas)", "2. Integrales Definidas (Área y Trabajo)"])

with tab_indefinida:
    st.header("Análisis Analítico: Antiderivadas Familiares")
    try:
        if funcion_input:
            f = parse_expr(funcion_input, transformations=transformaciones)
            F = sp.integrate(f, x)
            
            st.markdown("**1. Procedimiento Analítico:**")
            
            paso_actual = 1
            
            # Paso 1: Planteamiento original de la integral
            st.latex(rf"\text{{Paso {paso_actual}: Planteamiento formal}}")
            integral_original = sp.Integral(f, x)
            st.latex(sp.latex(integral_original))
            paso_actual += 1
            
            # Paso condicional: Propiedad de linealidad
            if f.is_Add:
                st.latex(rf"\text{{Paso {paso_actual}: Aplicar linealidad (separar términos)}}")
                terminos = f.args
                integral_separada = sum(sp.Integral(t, x) for t in terminos)
                st.latex(f"= {sp.latex(integral_separada)}")
                paso_actual += 1
                
            # Último Paso: Resultado final
            st.latex(rf"\text{{Paso {paso_actual}: Integración analítica y constante }} C")
            st.latex(f"= {sp.latex(F)} + C")
            
            st.markdown("---")
            st.markdown("**2. Análisis Técnico y Conclusiones:**")
            st.info("""
            * **Interpretación Matemática (Ausencia de Unidades):** A diferencia de las integrales definidas, este resultado **no posee unidades físicas** (como u² o Joules) porque no representa una magnitud escalar ni un área delimitada. Representa un **modelo algebraico abstracto**: una familia infinita de curvas.
            * **Justificación del Método y Rigor Formal:** Se aplicaron algoritmos de integración simbólica exacta. La adición de la constante de integración ($C$) es un requerimiento teórico indispensable que modela la pérdida de información ocurrida durante la derivación original de la función.
            * **Implicaciones Prácticas:** Este análisis analítico general es el pilar de la ingeniería diferencial. Sin modelar primero la antiderivada abstracta correcta, es matemáticamente imposible aplicar condiciones de frontera o estados iniciales para resolver problemas de cinemática, dinámica o circuitos.
            """)
            
    except Exception as e:
        st.error(f"Error matemático o de sintaxis: {e}")

with tab_definida:
    st.header("Análisis Físico y Geométrico: Área Bajo la Curva")
    
    colA, colB = st.columns(2)
    with colA:
        a_val = st.number_input("Límite inferior (a):", value=1.0)
    with colB:
        b_val = st.number_input("Límite superior (b):", value=5.0)

    try:
        if funcion_input:
            f = parse_expr(funcion_input, transformations=transformaciones)
            F = sp.integrate(f, x)
            resultado_exacto = sp.integrate(f, (x, a_val, b_val))
            
            st.markdown("**1. Procedimiento Analítico (Teorema Fundamental del Cálculo):**")
            F_b = F.subs(x, b_val)
            F_a = F.subs(x, a_val)
            
            st.latex(f"\int_{{{a_val}}}^{{{b_val}}} ({sp.latex(f)}) dx = \left[ {sp.latex(F)} \\right]_{{{a_val}}}^{{{b_val}}}")
            st.latex(f"= \left( {sp.latex(F_b)} \\right) - \left( {sp.latex(F_a)} \\right)")
            st.latex(f"= {sp.latex(resultado_exacto)} \\approx {resultado_exacto.evalf():.4f}")
            
            st.markdown("**2. Representación Gráfica e Interpretación:**")
            f_num = sp.lambdify(x, f, "numpy")
            x_graf = np.linspace(a_val - 1, b_val + 1, 400)
            y_graf = f_num(x_graf) if not isinstance(f, sp.Number) else np.full_like(x_graf, float(f))
            x_fill = np.linspace(a_val, b_val, 200)
            y_fill = f_num(x_fill) if not isinstance(f, sp.Number) else np.full_like(x_fill, float(f))

            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(x_graf, y_graf, color="blue", label="f(x)")
            ax.fill_between(x_fill, y_fill, alpha=0.3, color="blue", label=f"Magnitud = {resultado_exacto.evalf():.4f} u²")
            ax.axhline(0, color='black', linewidth=1)
            ax.axvline(a_val, color='red', linestyle='--', label=f"Límite a = {a_val}")
            ax.axvline(b_val, color='green', linestyle='--', label=f"Límite b = {b_val}")
            
            ax.set_xlabel("Distancia / Tiempo (Unidades Lineales X)")
            ax.set_ylabel("Fuerza / Tasa de Cambio (Unidades Y)")
            ax.legend()
            ax.grid(True)
            st.pyplot(fig)
            
            st.markdown("---")
            st.markdown("**3. Análisis Técnico y Conclusiones:**")
            st.info(f"""
            * **Interpretación Física:** El valor obtenido de **{resultado_exacto.evalf():.4f} unidades cuadradas (u²)** representa geométricamente el área exacta bajo la curva. En un contexto de ingeniería, si el eje Y representa Fuerza (Newtons) y el eje X Distancia (metros), este resultado equivale al **Trabajo total realizado (Joules)**.
            * **Justificación del Método:** Se seleccionó la integración analítica aplicando el **Teorema Fundamental del Cálculo** por encima de métodos de aproximación numérica (como Sumas de Riemann). Esto garantiza una precisión absoluta del modelo matemático sin margen de error iterativo.
            * **Validación Computacional:** El algoritmo procesa la antiderivada exacta $F(x)$ y la evalúa rigurosamente en las condiciones de frontera mediante la diferencia $F(b) - F(a)$, cumpliendo con el rigor analítico exigido para el diseño de sistemas físicos.
            """)
            
    except Exception as e:
        st.error(f"Error matemático o de sintaxis: {e}")