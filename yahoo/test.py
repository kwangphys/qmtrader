
if __name__ == '__main__':
    import pickle
    import os
    folder = "X:/Trading/USFundamentals"
    filename = 'er_nasdaq_20180615.pkl'
    data = pickle.load(open(os.path.join(folder, filename), 'rb'))
    print(data)
