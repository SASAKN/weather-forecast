import numpy as np

if __name__ == "__main__":
    array = np.load('./npz_data/dataset.npz')
    np.set_printoptions(suppress=False, precision=2)
    print(array['dataset'])
    print(array['dataset'].dtype)