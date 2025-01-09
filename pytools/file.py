import os
import fnmatch
import numpy as np


class Files:
    def __init__(self, directory=".", pattern="*", hidden=False):
        """
        Initialize the Files class.

        Parameters
        ----------
        directory : str, optional
            The directory to search for files (default is the current directory).
        pattern : str, optional
            The Unix-style pattern to match files (default is "*").
        hidden : bool, optional
            Whether to include hidden files and directories (default is False).
        """
        self.directory = directory
        self.pattern = pattern
        self.hidden = hidden
        self.__hiddenchar = [".", "_"]

    def __call__(self):
        """
        Return the list of files when the class instance is called.

        Returns
        -------
        numpy.ndarray
            Sorted array of file paths matching the pattern.
        """
        return self.files

    @property
    def files(self):
        """
        List all files in the directory matching the Unix-style pattern.

        Returns
        -------
        numpy.ndarray
            Sorted array of file paths matching the pattern.
        """
        files = []
        for root, dirs, filenames in os.walk(self.directory):
            # Skip hidden directories if hidden=False
            if not self.hidden:
                dirs[:] = [d for d in dirs if d[0] not in self.__hiddenchar]
                filenames = [f for f in filenames if f[0] not in self.__hiddenchar]

            for filename in filenames:
                if fnmatch.fnmatch(filename, self.pattern):
                    files.append(os.path.join(root, filename))
        return np.sort(files)

    def __repr__(self):
        """
        Standard representation of the Files instance.

        Returns
        -------
        str
            Representation of the Files instance.
        """
        return f"Files(directory={self.directory}, pattern={self.pattern})"

    def __len__(self):
        """
        Return the count of files in the directory matching the Unix-style pattern.

        Returns
        -------
        int
            The number of files matching the pattern.
        """
        return self.counts

    @property
    def counts(self):
        """
        Count all files in the directory matching the Unix-style pattern.

        Returns
        -------
        int
            The number of files matching the pattern.
        """
        return len(self.files)

    @property
    def sizes(self):
        """
        Return a dictionary with filenames as keys and their sizes in bytes as values.

        Returns
        -------
        dict
            A dictionary with file paths as keys and their sizes in bytes as values.
        """
        files = self.files
        return {file: os.path.getsize(file) / (1024 * 1024) for file in files}

    @property
    def totalsize(self):
        """
        Return the total size of all files in the directory matching the Unix-style pattern.

        Returns
        -------
        int
            The total size of all files in bytes.
        """
        sizes = self.file_sizes().values()
        return sum(sizes)

    def file_info_dict(self):
        """
        Convert the list of files into a dictionary containing basic information about each file.

        Returns
        -------
        dict
            A dictionary with file paths as keys and a dictionary of basic information (size, last modified) as values.
        """
        file_info = {}
        for file in self.files:
            file_info[file] = {
                "size": os.path.getsize(file),
                "last_modified": os.path.getmtime(file),
            }
        return file_info

    def list_by_extension(self):
        """
        Group files by their extension.

        Returns
        -------
        dict
            A dictionary where each key is a file extension (without leading dot) and the value is a list of file paths with that extension.
        """
        files_by_ext = {}
        for file in self.files:
            ext = (
                os.path.splitext(file)[1].lower().lstrip(".")
            )  # Get file extension without leading dot
            if ext not in files_by_ext:
                files_by_ext[ext] = []
            files_by_ext[ext].append(file)
        return files_by_ext

    def extension_stats(self):
        """
        Provide statistics for each file extension, including the number of files and total size in megabytes.

        Returns
        -------
        dict
            A dictionary where each key is a file extension (without leading dot) and the value is another dictionary with 'count' and 'total_size_mb'.
        """
        stats = {}
        for ext, files in self.list_by_extension().items():
            total_size = sum(os.path.getsize(file) for file in files) / (
                1024 * 1024
            )  # Convert size to MB
            stats[ext] = {"count": len(files), "total_size_mb": round(total_size, 2)}
        return stats

    def __str__(self):
        """
        Return a string representation of file details.

        Returns
        -------
        str
            A formatted string with file details (path and size).
        """
        output = ""
        for file in self.files:
            output += f"File: {file}\n"
            output += f"Size: {os.path.getsize(file)/(1024*1024)} MB\n"
            output += "----------------------------------------\n"
        return output


# Example usage:
if __name__ == "__main__":
    directory = "."  # Default is current directory
    pattern = "*"  # Default is to match all files

    fm = Files(
        directory, pattern, hidden=False
    )  # Set hidden=True to include hidden files/directories

    print("List of files (matching pattern):", fm())
    print("Count of files:", fm.counts)
    print("File sizes:", fm.sizes)
    print("Total size of files:", fm.totalsize)
    print("File details:")
    print(fm)

    # Test extension_stats method
    print("Extension Stats Dictionary:")
    print(fm.extensions_stats())


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
