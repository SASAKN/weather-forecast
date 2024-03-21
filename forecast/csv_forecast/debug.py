import numpy as np
import pandas as pd

if __name__ == "__main__":
    np.set_printoptions(threshold=100, suppress=True)
    pd.options.display.max_columns = 100
    array = np.load('./npz_data/dataset.npz')['dataset']
    print(pd.DataFrame(array[0]))
