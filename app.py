import streamlit as st
import numpy as np
from system import System
from visualization import plot_bode, plot_step, plot_impulse, plot_pz, plot_nyquist

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
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    .stability-stable {
        color: #3fb950;
        font-weight: bold;
    }
    .stability-unstable {
        color: #f78166;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">🎛️ Signals & Systems Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Interactive LTI System Analysis and Visualization</div>', unsafe_allow_html=True)

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
    h1_name = st.text_input("Name", value="LPF", key="h1_name")
    h1_num_str = st.text_input("Numerator Coefficients", value="1", key="h1_num", help="Comma-separated values, e.g., 1, 2")
    h1_den_str = st.text_input("Denominator Coefficients", value="1, 2", key="h1_den")
    
    st.markdown("---")
    
    st.subheader("System 2 (H2)")
    h2_name = st.text_input("Name", value="BPF", key="h2_name")
    h2_num_str = st.text_input("Numerator Coefficients", value="1, 0", key="h2_num")
    h2_den_str = st.text_input("Denominator Coefficients", value="1, 3, 9", key="h2_den")
    
    st.markdown("---")
    
    st.subheader("Feedback Gain (K)")
    k_name = st.text_input("Name", value="Gain", key="k_name")
    k_num_str = st.text_input("Numerator Coefficients", value="5", key="k_num")
    k_den_str = st.text_input("Denominator Coefficients", value="1", key="k_den")

# Parse inputs
h1_num = parse_coeffs(h1_num_str)
h1_den = parse_coeffs(h1_den_str)
h2_num = parse_coeffs(h2_num_str)
h2_den = parse_coeffs(h2_den_str)
k_num = parse_coeffs(k_num_str)
k_den = parse_coeffs(k_den_str)

if not all([h1_num, h1_den, h2_num, h2_den, k_num, k_den]):
    st.error("❌ Please enter valid comma-separated numeric coefficients for all systems.")
    st.stop()

# Instantiate Systems
try:
    H1 = System(h1_num, h1_den, h1_name)
    H2 = System(h2_num, h2_den, h2_name)
    K  = System(k_num, k_den, k_name)

    H_series = H1.series(H2)
    H_parallel = H1.parallel(H2)
    H_feedback = H1.feedback(K)

    systems_list = [H1, H2, H_series, H_parallel]
except Exception as e:
    st.error(f"❌ Error instantiating systems: {e}")
    st.stop()

# Dashboard Content
st.markdown("### 📊 System Stability Overview")
cols = st.columns(4)
for i, sys in enumerate(systems_list + [H_feedback]):
    with cols[i % 4]:
        stability = "Stable" if sys.is_stable() else "Unstable"
        css_class = "stability-stable" if sys.is_stable() else "stability-unstable"
        
        st.markdown(f"""
        <div class="system-card">
            <h4>{sys.name}</h4>
            <span class="{css_class}">Status: {stability}</span>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Bode Plot", 
    "👟 Step Response", 
    "⚡ Impulse Response", 
    "🎯 Pole-Zero Map", 
    "🌀 Nyquist Plot"
])

with tab1:
    st.markdown("#### Frequency Response (Bode)")
    fig_bode = plot_bode(systems_list)
    st.pyplot(fig_bode)

with tab2:
    st.markdown("#### Time Domain: Step Response")
    fig_step = plot_step(systems_list)
    st.pyplot(fig_step)

with tab3:
    st.markdown("#### Time Domain: Impulse Response")
    fig_impulse = plot_impulse(systems_list)
    st.pyplot(fig_impulse)

with tab4:
    st.markdown("#### Pole-Zero Mapping")
    col1, col2 = st.columns([1, 2])
    with col1:
        st.info("Select the system to view its Pole-Zero map.")
        pz_sys_name = st.selectbox("System for P-Z Map", [s.name for s in systems_list + [H_feedback]])
        pz_sys = next(s for s in systems_list + [H_feedback] if s.name == pz_sys_name)
    with col2:
        fig_pz = plot_pz(pz_sys)
        st.pyplot(fig_pz)

with tab5:
    st.markdown("#### Nyquist Stability Criterion")
    col1, col2 = st.columns([1, 2])
    with col1:
        st.info("Select the system to view its Nyquist plot.")
        nyq_sys_name = st.selectbox("System for Nyquist", [s.name for s in systems_list + [H_feedback]], index=len(systems_list))
        nyq_sys = next(s for s in systems_list + [H_feedback] if s.name == nyq_sys_name)
    with col2:
        fig_nyq = plot_nyquist(nyq_sys)
        st.pyplot(fig_nyq)
