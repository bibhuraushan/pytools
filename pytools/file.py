import os
import numpy as np
def file_search(path, fileext=None):

    """
    Search for files with a specific extension in a directory tree.

    Parameters:
        path (str): The directory path to search for files.
        fileext (str, optional): The file extension to filter files.
            If None, all files will be included. Defaults to None.

    Returns:
        numpy.ndarray: An array of sorted file paths matching the criteria.
    """
    files = []
    for dr, _, file in os.walk(path):
        for f in file:
            if fileext is None:
                files.append(os.path.join(dr, f))
            elif f.endswith(fileext):
                files.append(os.path.join(dr, f))
    return np.sort(files)
