

import numpy as np
from getOffsets import getOffsets
if __name__ == "__main__":


    boxes = [[(210, 211), (620, 211), (620, 621), (210, 621)], [(291, 332), (378, 332), (378, 419), (291, 419)], [(434, 331), (520, 331), (520, 417), (434, 417)]];
    mask = np.zeros((242,153));
    getOffsets(boxes,mask,0);
