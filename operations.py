
def AddSignals(signal1, signal2):
    """
    Add two time-domain signals sample by sample.
    """

    if len(signal1) != len(signal2):
        raise ValueError("Signals must have the same number of samples.")

    result = []

    for sample1, sample2 in zip(signal1, signal2):
        index1, value1 = sample1
        index2, value2 = sample2

        if index1 != index2:
            raise ValueError("Signal sample indices must match.")

        result.append((index1, value1 + value2))

    return result




def MultiplySignalByConst(signal, constant):
    """
    Multiply every sample amplitude by a constant.
    """

    result = []

    for index, amplitude in signal:
        result.append((index, amplitude * constant))

    return result