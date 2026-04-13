from system import System
from visualization import *


def main():
    H1 = System([1], [1, 2], "LPF")
    H2 = System([1, 0], [1, 3, 9], "BPF")
    K  = System([5], [1], "Gain")

    H_series = H1.series(H2)
    H_parallel = H1.parallel(H2)
    H_feedback = H1.feedback(K)

    systems = [H1, H2, H_series, H_parallel]

    plot_bode(systems)
    plot_step(systems)
    plot_impulse(systems)

    plot_pz(H_series)
    plot_nyquist(H_feedback)

    print("Stability:")
    for s in systems:
        print(s.name, s.is_stable())


if __name__ == "__main__":
    main()