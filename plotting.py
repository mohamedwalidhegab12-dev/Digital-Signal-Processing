
import matplotlib.pyplot as plt


def PlotSignal(signal, title="Signal"):
    """
    Plot a signal as discrete and continuous representations.
    signal format: [(index, amplitude), ...]
    """

    if not signal:
        raise ValueError("Signal cannot be empty.")

    indices = [sample[0] for sample in signal]
    amplitudes = [sample[1] for sample in signal]

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Discrete representation
    axes[0].stem(indices, amplitudes)
    axes[0].set_title("Discrete Signal (Stem)")
    axes[0].set_xlabel("Sample Index")
    axes[0].set_ylabel("Amplitude")
    axes[0].grid(True)

    # Continuous-looking representation
    axes[1].plot(indices, amplitudes, marker="o")
    axes[1].set_title("Continuous Representation (Line)")
    axes[1].set_xlabel("Sample Index")
    axes[1].set_ylabel("Amplitude")
    axes[1].grid(True)

    fig.suptitle(title)
    fig.tight_layout()
    plt.show()