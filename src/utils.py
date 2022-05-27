# utility functions
import pickle, os

def save_entry(obj, file):
    with open(file, 'wb') as handle:
        pickle.dump(obj, handle, protocol=pickle.HIGHEST_PROTOCOL)
        
def load_entry(file):
    with open(file, 'rb') as handle:
        load = pickle.load(handle)
    return load

# typical gitlet behavior
def join(path, file):
    return os.path.join(path, file)

def clean_dirs(dir):
    for file in os.listdir(dir):
        os.remove(join(dir, file))