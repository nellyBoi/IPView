import pathlib

import numpy as np
import matplotlib.pyplot as plt

MIN_COUNTS = 0x8000
MAX_COUNTS = 0x4000


########################################################################################################################
def read(filename: str,
         noiseMean: float = 0.0,
         noiseStd: float = 0.0,
         randomSeed: int = 666,
         doPlot: bool = False) -> np.ndarray:
    """
    Parses the data out of a fred file

    Args:
        filename: the full filename
        noiseMean: the mean background noise to add
        noiseStd: the standard deviation of background noise to add
        randomSeed: the random seed to use for the background noise
        doPlot: whether or not to plot the image

    Returns:
        np.ndarray
    """
    with open(filename, 'r') as f:
        data = list()
        dataBegin = False
        for lineNumber, line in enumerate(f):
            if not dataBegin:
                if line.startswith('BeginData'):
                    dataBegin = True
                continue

            strippedLine = line.strip()
            if len(strippedLine) == 0:
                continue

            values = strippedLine.split(' ')
            data.append([float(value) for value in values if value != ''])

    # Scale the image
    image = np.array(data).T
    image /= image.max()
    image *= MAX_COUNTS
    image += MIN_COUNTS

    # add some noise
    np.random.seed(randomSeed)
    image += np.random.randn(*image.shape) * noiseStd + noiseMean

    # quantize and clip
    image = np.round(image)
    image = np.clip(image, 0, MIN_COUNTS + MAX_COUNTS)
    image = np.flipud(image.astype(np.uint16))

    if doPlot:
        plt.figure()
        plt.imshow(image, cmap='gray', interpolation='bilinear')
        plt.xlabel('Cols')
        plt.ylabel('Rows')
        plt.title(pathlib.Path(filename).name)
        cmin = int(image.min())
        cmax = int(image.min() + image.max() * 0.02)
        if cmin == cmax:
            cmax = cmin + 1
        plt.clim([cmin, cmax])

    return image


