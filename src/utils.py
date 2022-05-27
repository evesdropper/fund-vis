# utility functions

def save_entry(obj):
    with open('fund.txt', 'wb') as handle:
        pickle.dump(obj, handle, protocol=pickle.HIGHEST_PROTOCOL)
        
def load_entry():
    with open('fund.txt', 'rb') as handle:
        load = pickle.load(handle)
    return load