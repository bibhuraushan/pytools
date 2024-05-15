import yaml
import os
from pathlib import Path


def is_hidden(name):
    """
    To check if a named file is a hidden file or not.
    Parameters
    ----------
    name: str

    Returns
    -------
    _: bool
    Weather or not a hidden file.

    """
    if name.startswith('.') | (name.startswith('_')):
        return True
    else:
        return False


def orgfilebytype(path: str = None, outpath: str = None,
                  move: bool = True, verbose: bool = True):
    """
    A function to organize files in a given folder to an organized folders
    based on the type of the file.

    Parameters
    ----------
    path: str
    Input directory in which files are located and need to be organized.
    Defaults to cwd
    outpath: str
    Output directory in which file need to be organized. Defaults to cwd
    move: bool
    Whether to move or copy all files to the output directory. Defaults to True
    verbose: bool
    Whether to show the progress of the organized files. Defaults to True.
    """
    this_dir = Path(__file__).parent
    process = "mv" if move else "cp"
    processstr = "Moving" if move else "Copying"
    path = os.getcwd() if path is None else path

    if outpath is None:
        outpath = path

    # look for configuration file
    try:
        with open(f"{this_dir}/data/config.yml") as fl:
            dirstr = yaml.safe_load(fl)
    except FileNotFoundError:
        raise FileNotFoundError("Config file not found.")
    # Scan Directory
    files = os.scandir(path)
    for i in files:
        extn = ""
        if i.is_dir() or is_hidden(i.name):
            if verbose:
                print(f"{i.name} is not a file, Skipping...")
            continue
        extn = os.path.basename(i.name).split(".")[-1]
        for ii in dirstr.keys():
            if extn in dirstr[ii]:
                folder = ii
                break
        else:
            folder = "others"

        # Copy file to directory with properties
        outdir = os.path.join(outpath, folder)
        if os.path.exists(outdir):
            os.system(f'{process} "{i.path}" {outdir}')
        else:
            os.mkdir(outdir)
            a = os.system(f'{process} "{i.path}" {outdir}')

        if verbose:
            print(f"{processstr} {i.name} to {outdir}.")


def getoutofdir(path: str = None, outpath: str = None,
                move: bool = True, verbose: bool = True):
    process = "mv" if move else "cp"
    processstr = "Moving" if move else "Copying"
    path = os.getcwd() if path is None else path

    if outpath is None:
        outpath = path

    for root, dirs, files in os.walk(path):
        for filename in files:
            if os.path.isfile(os.path.join(path, filename)) & (root == path):
                continue
            os.system(f"{process} '{os.path.join(root, filename)}' {outpath}")
            if verbose:
                print(f"{processstr} {os.path.join(root, filename)}")


def rmemptydir(path: str = ".", verbose: bool = True, rec_depth=10):
    path = os.getcwd() if path is None else path
    for i in range(rec_depth):
        count = 0
        for root, dirs, files in os.walk(path):
            if (len(files) == 0) & (len(dirs) == 0):
                os.system(f"rmdir '{root}'")
                print(f"Removed empty directory {root}")
                count = count + 1

        if count == 0:
            break


def refile_ext(ext, path: str = None):
    path = os.getcwd() if path is None else path
    for root, dirs, files in os.walk(path):
        for filename in files:
            if filename.endswith("." + ext):
                os.system(f"rm '{filename}'")


def copy_ext(ext, path: str = None, outpath: str = None):
    path = os.getcwd() if path is None else path
    if outpath is None:
        outpath = os.path.join(path, ext)
        os.makedirs(outpath, exist_ok=True)
    for root, dirs, files in os.walk(path):
        for filename in files:
            exist = os.path.isfile(os.path.join(root, filename))
            if filename.endswith(ext) and (not exist):
                os.system(f"cp '{os.path.join(root, filename)}' {outpath}")
