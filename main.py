from system import System
from visualization import *


def main():
    # 1. Define two distinct systems
    # System 1: Low-Pass Filter (LPF)
    H1 = System([1], [1, 2], "LPF_H1")
    
    # System 2: Band-Pass Filter (BPF) or another LTI system
    H2 = System([1, 0], [1, 3, 9], "BPF_H2")

    # 2. Demonstrate Series Interconnection: H_series = H1 * H2
    H_series = H1.series(H2)
    
    # 3. Demonstrate Parallel Interconnection: H_parallel = H1 + H2
    H_parallel = H1.parallel(H2)

    # 4. Group systems for comparison
    systems = [H1, H2, H_series, H_parallel]

    print("--- System Interconnection Analysis ---")
    for s in systems:
        stability = "Stable" if s.is_stable() else "Unstable"
        print(f"System: {s.name:15} | Status: {stability}")

    # 5. Visualize and compare the fundamental responses
    import matplotlib.pyplot as plt
    
    # Time Response (Step)
    plot_step(systems)
    
    # Time Response (Impulse)
    plot_impulse(systems)
    
    plt.show()


if __name__ == "__main__":
    main()