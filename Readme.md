# Interconnection of Systems Simulator

A Python-based simulator for analyzing continuous-time Linear Time-Invariant (LTI) systems and their interconnections. It allows you to quickly evaluate transfer functions, combine systems in different topologies (series, parallel, feedback), and visualize their stability and time/frequency responses.

## Features

- **System Interconnection:** Easily combine LTI systems in **Series**, **Parallel**, or **Feedback** (positive, negative, and unity feedback).
- **Time-Domain Analysis:** Plot **Step Responses** and **Impulse Responses** matching system outputs under various input conditions.
- **Frequency-Domain Analysis:** Visualize frequency behaviors using **Bode Plots** and **Nyquist Plots**.
- **Stability Analysis:** View stability information cleanly through **Pole-Zero Maps** and programmatic `.is_stable()` checks.
- **Beautiful Visualizations:** Built-in modular `visualization.py` leveraging Matplotlib for dark-mode, high-contrast, informative graphs.

## Project Structure

The codebase is organized into modules for easy modification and analysis:

* `main.py` - The entry point script showing an end-to-end example of creating, connecting, and plotting various systems (LPF, BPF, gain blocks).
* `system.py` - Core logic containing the `System` class representing transfer functions and wrapping `scipy.signal`.
* `visualization.py` - Dedicated plotting library decoupled from system logic, keeping analysis functions clean and maintainable.

## Requirements

Ensure you have Python installed along with the required third-party libraries. If you have a `requirements.txt`:

```bash
pip install -r requirements.txt
```

*(Key libraries consist of `numpy`, `scipy`, and `matplotlib`)*

## Usage

You can run the existing simulation suite to see all plots generated sequentially:

```bash
python main.py
```

*Note: Since the plots are drawn to a single UI thread sequentially, you will need to close the active Matplotlib window before the next graph is rendered.*

## Example

```python
from system import System

# Define a 1st-order Low-Pass Filter: H(s) = 1 / (s + 2)
H1 = System(num=[1], den=[1, 2], name="LPF")

# Define a basic proportional Gain block: K = 5
K = System(num=[5], den=[1], name="Gain")

# Connect them in negative feedback
H_feedback = H1.feedback(K, sign=-1)

# Check stability
print("Is the feedback loop stable?", H_feedback.is_stable())
```
