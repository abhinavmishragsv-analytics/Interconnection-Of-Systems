import streamlit as st
import numpy as np
from system import System
from visualization import plot_step, plot_impulse

st.set_page_config(page_title="Signals & Systems Dashboard", page_icon="🎛️", layout="wide")

# Custom CSS for a more premium look
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #58a6ff;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #c9d1d9;
        margin-bottom: 2rem;
    }
    .system-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 1.2rem;
        margin-bottom: 1rem;
    }
    .system-label {
        color: #58a6ff;
        font-weight: 600;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">🎛️ Signals & Systems Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">In-Depth Series and Parallel Interconnection Analysis</div>', unsafe_allow_html=True)

def parse_coeffs(coeff_str):
    """Parse comma-separated string into a list of floats."""
    try:
        return [float(x.strip()) for x in coeff_str.split(',') if x.strip()]
    except ValueError:
        return None

# Sidebar for inputs
with st.sidebar:
    st.header("⚙️ System Configuration")
    
    st.subheader("System 1 (H1)")
    h1_name = st.text_input("Name", value="LPF_H1", key="h1_name")
    h1_num_str = st.text_input("Numerator Coefficients", value="1", key="h1_num", help="Comma-separated values, e.g., 1, 2")
    h1_den_str = st.text_input("Denominator Coefficients", value="1, 2", key="h1_den")
    
    st.markdown("---")
    
    st.subheader("System 2 (H2)")
    h2_name = st.text_input("Name", value="BPF_H2", key="h2_name")
    h2_num_str = st.text_input("Numerator Coefficients", value="1, 0", key="h2_num")
    h2_den_str = st.text_input("Denominator Coefficients", value="1, 3, 9", key="h2_den")

# Parse inputs
h1_num = parse_coeffs(h1_num_str)
h1_den = parse_coeffs(h1_den_str)
h2_num = parse_coeffs(h2_num_str)
h2_den = parse_coeffs(h2_den_str)

if not all([h1_num, h1_den, h2_num, h2_den]):
    st.error("❌ Please enter valid comma-separated numeric coefficients for System 1 and System 2.")
    st.stop()

# Instantiate Systems
try:
    H1 = System(h1_num, h1_den, h1_name)
    H2 = System(h2_num, h2_den, h2_name)

    H_series = H1.series(H2)
    H_parallel = H1.parallel(H2)

    systems_list = [H1, H2, H_series, H_parallel]
except Exception as e:
    st.error(f"❌ Error instantiating systems: {e}")
    st.stop()

# Dashboard Content
st.markdown("### 📋 Interconnection Overview")
cols = st.columns(4)
for i, sys in enumerate(systems_list):
    with cols[i]:
        st.markdown(f"""
        <div class="system-card">
            <div class="system-label">{sys.name}</div>
            <code style="font-size: 0.75rem;">Num: {sys.num.tolist()}</code><br>
            <code style="font-size: 0.75rem;">Den: {sys.den.tolist()}</code>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

tab1, tab2 = st.tabs([
    "👟 Step Response (Time Domain)", 
    "⚡ Impulse Response (Time Domain)"
])

with tab1:
    st.markdown("#### Step Response Comparison")
    st.caption("The step response demonstrates how the systems react to a sudden change in input.")
    fig_step = plot_step(systems_list)
    st.pyplot(fig_step)

with tab2:
    st.markdown("#### Impulse Response Comparison")
    st.caption("The impulse response shows the system's inherent behavior and damping characteristics.")
    fig_impulse = plot_impulse(systems_list)
    st.pyplot(fig_impulse)
