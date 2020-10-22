import os
import dill


def get_blobs():
    blobs = {}
    relevant_path = "./player-blobs/"
    included_extensions = ['blob']
    file_names = [fn for fn in os.listdir(relevant_path)
                  if any(fn.endswith(ext) for ext in included_extensions)]
    for f in file_names:
        blob_name = f.split(".")[0]
        try:
            with open(relevant_path + f, 'rb') as infile:
                decision_function = dill.load(infile)
                blobs[blob_name] = decision_function
        except Exception as e:
            print("failed to load blob:", blob_name, "error:", e)
    return blobs
