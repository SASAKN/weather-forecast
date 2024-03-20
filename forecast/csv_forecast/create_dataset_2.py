import numpy as np

if __name__ == "__main__":
    np.set_printoptions(precision=3,suppress=True)
    array = np.load('./npz_data/dataset.npz')
    print(array['dataset'])
