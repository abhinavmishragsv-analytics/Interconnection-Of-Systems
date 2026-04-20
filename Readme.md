# Interconnection of Systems Simulator

A Python-based simulator for analyzing continuous-time Linear Time-Invariant (LTI) systems and their interconnections. This tool focuses on **Series** and **Parallel** system topologies, providing in-depth visualizations of their time and frequency domain behaviors.

Featuring an **interactive Streamlit dashboard** for real-time analysis and comparison.

## Features

- **🚀 Interactive Dashboard:** A modern UI to configure systems and visualize interconnected responses instantly.
- **🔗 System Interconnection:** Seamlessly combine LTI systems in **Series** (H1 * H2) and **Parallel** (H1 + H2).
- **👟 Time-Domain Analysis:** Visualize system dynamics with **Step Responses** and **Impulse Responses**.
- **🎨 Professional Visualizations:** Modular `visualization.py` leveraging Matplotlib for dark-mode, high-contrast graphs.

## Project Structure

* `app.py` - The Streamlit dashboard for interactive, in-depth interconnection analysis.
* `main.py` - CLI entry point demonstrating deep comparisons between systems.
* `system.py` - Core logic containing the `System` class for transfer function manipulation.
* `visualization.py` - Plotting library focused on Step and Impulse responses.

## Requirements

```bash
pip install -r requirements.txt
```

*(Includes `streamlit`, `numpy`, `scipy`, and `matplotlib`)*

## Usage

### Option 1: Interactive Dashboard (Recommended)
```bash
streamlit run app.py
```

### Option 2: CLI Simulation
```bash
python main.py
```

## Example

```python
from system import System

# Define a Low-Pass Filter: H1(s) = 1 / (s + 2)
H1 = System(num=[1], den=[1, 2], name="LPF")

# Define another system: H2(s) = s / (s^2 + 3s + 9)
H2 = System(num=[1, 0], den=[1, 3, 9], name="BPF")

# Connect them in series
H_series = H1.series(H2)

# Connect them in parallel
H_parallel = H1.parallel(H2)
```

