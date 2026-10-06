
def ReadSignalFile(file_path):
    """
    Read a DSP signal from a text file.

    File format:
    Line 1: SignalType (0 = Time, 1 = Frequency)
    Line 2: IsPeriodic (0 = Non-periodic, 1 = Periodic)
    Line 3: Number of samples
    Remaining lines: Sample data
    """

    with open(file_path, "r") as file:
        lines = [
            line.strip()
            for line in file
            if line.strip()
        ]

    if len(lines) < 3:
        raise ValueError("Invalid signal file: missing header.")

    signal_type = int(lines[0])
    is_periodic = int(lines[1])
    number_of_samples = int(lines[2])

    if signal_type not in (0, 1):
        raise ValueError("SignalType must be 0 or 1.")

    if is_periodic not in (0, 1):
        raise ValueError("IsPeriodic must be 0 or 1.")

    if number_of_samples < 0:
        raise ValueError("Number of samples cannot be negative.")

    samples = []

    for line in lines[3:]:
        values = line.split()

        if signal_type == 0:
            # Time domain: index, amplitude
            if len(values) < 2:
                raise ValueError(f"Invalid time-domain sample: {line}")

            index = int(values[0])
            amplitude = float(values[1])

            samples.append((index, amplitude))

        else:
            # Frequency domain: frequency, amplitude, phase
            if len(values) < 2:
                raise ValueError(f"Invalid frequency-domain sample: {line}")

            frequency = float(values[0])
            amplitude = float(values[1])
            phase = float(values[2]) if len(values) >= 3 else 0.0

            samples.append((frequency, amplitude, phase))

    if len(samples) != number_of_samples:
        raise ValueError(
            f"Expected {number_of_samples} samples, "
            f"but found {len(samples)}."
        )

    return signal_type, is_periodic, samples





def SaveSignalFile(file_path, signal_type, is_periodic, samples):
    """
    Save a DSP signal to a text file.
    """

    with open(file_path, "w") as file:
        file.write(f"{signal_type}\n")
        file.write(f"{is_periodic}\n")
        file.write(f"{len(samples)}\n")

        for sample in samples:
            file.write(" ".join(map(str, sample)) + "\n")