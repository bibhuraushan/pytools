import requests
import os
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urlparse

def download_from_url(url, filepath=None, outpath="./downloaded_data", verbose=True):
    """
    Download a file from a given URL and save it to a specified directory.

    Parameters
    ----------
    url : str
        The URL of the file to download.
    filepath : str, optional
        The name of the file to save. If None, the filename is extracted from the URL. Default is None.
    outpath : str, optional
        The output directory where the file will be saved. Default is "./downloaded_data".
    verbose : bool, optional
        If True, prints download progress and status. Default is True.

    Returns
    -------
    bool
        True if the download was successful, False otherwise.
    """
    try:
        # Validate the URL
        parsed_url = urlparse(url)
        if not parsed_url.scheme or not parsed_url.netloc:
            raise ValueError("Invalid URL provided.")
        
        # Extract filename from URL if not provided
        if filepath is None:
            filepath = os.path.basename(parsed_url.path)
            if not filepath:  # Handle cases where URL ends with a slash
                raise ValueError("Unable to extract filename from URL.")

        # Create the output directory if it doesn't exist
        os.makedirs(outpath, exist_ok=True)

        # Perform the file download with streaming
        if verbose:
            print(f"Downloading: {filepath}....", end=" ")
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an HTTPError for bad responses

        # Save the file to the specified path
        full_path = os.path.join(outpath, filepath)
        with open(full_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        if verbose:
            print("Done!")
        return True
    except requests.exceptions.RequestException as e:
        if verbose:
            print(f"Failed!")
    except Exception as e:
        if verbose:
            print(f"An error occurred: {e}")
    return False
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def get_hmi_nrt(date, return_datetime=False):
    """
    Fetches a list of HMI NRT FITS files for a given date from the JSOC server.

    Parameters
    ----------
    date : datetime.date
        The date for which to retrieve the HMI FITS files.

    Returns
    -------
    list of tuple
        A list of tuples where each tuple contains:
        - ISO 8601 timestamp of the FITS file.
        - Full URL to the FITS file.
    """
    # Format base URL with the given date
    base_url = f"https://jsoc1.stanford.edu/data/hmi/fits/{date.year:04}/{date.month:02}/{date.day:02}/"
    try:
        # Make an HTTP GET request
        response = requests.get(base_url)
        response.raise_for_status()  # Raise an error for non-2xx status codes

        # Parse HTML response
        soup = BeautifulSoup(response.text, 'html.parser')
        links = [link.text for link in soup.find_all("a") if link.text.endswith("fits")]

        # Extract times and create the output list
        times = []
        for link in links:
            try:
                # Try matching the standard FITS pattern
                times.append(datetime.strptime(link, "hmi.M_720s.%Y%m%d_%H%M%S_TAI.fits"))
            except ValueError:
                # Fall back to the NRT FITS pattern
                times.append(datetime.strptime(link, "hmi.M_720s_nrt.%Y%m%d_%H%M%S_TAI.fits"))

        # Combine times with full URLs
        full_links = [base_url + link for link in links]
        if not return_datetime:
            times = [t.isoformat() for t in times]
        return list(zip(times, full_links))

    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch data from {base_url}. Error: {e}")
        return []
    except Exception as e:
        print(f"An error occurred while processing links. Error: {e}")
        return []