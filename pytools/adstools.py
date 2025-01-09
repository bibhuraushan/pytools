import requests
import bibtexparser
import os
from tqdm.autonotebook import tqdm
from urllib.parse import urlencode


def bibtex_to_dict(bibtex):
    """
    Converts a BibTeX string into a dictionary representation.

    Parameters
    ----------
    bibtex : str
        The BibTeX string to be converted.

    Returns
    -------
    dict
        A dictionary containing parsed BibTeX fields.
    """
    entry = bibtexparser.parse_string(bibtex)
    for field in entry.entries:
        authors = field.fields_dict["author"].value
        names = []
        dc = {}
        for i in authors.split("and"):
            a = i.replace(r"{", "").replace(r"}", "").split(",")
            a = [ii.strip() for ii in a]
            a.reverse()
            names.append(f"{a[0]} {a[-1]}")
    dc["authors"] = names
    dc["title"] = field.fields_dict["title"].value.replace(r"{", "").replace(r"}", "")
    skip = ["author", "title", "keywords", "adsnote", "primaryClass", "archivePrefix"]
    for key in field.fields_dict:
        if key in skip:
            continue
        dc[key] = field.fields_dict[key].value
    return dc


class ADSPro:
    """
    A class to interact with the ADS API for fetching BibTeX entries.

    Attributes
    ----------
    api_token : str
        ADS API token.

    Methods
    -------
    from_bibcode(bibcode):
        Fetches the BibTeX entry for a given bibcode.

    from_doi(doi):
        Fetches the BibTeX entry for a given DOI and retrieves the corresponding bibcode.

    from_library(library_id, max_results=None, rawstring=False):
        Fetches all BibTeX entries from a given library.
    """

    def __init__(self, token=os.environ.get("ADS_API_TOKEN"), from_file=False):
        """
        Initializes the ADSPro class with an API token.

        Parameters
        ----------
        token : str
            API token or path to the token file.
        from_file : bool, optional
            Whether the token is provided as a file path (default is False).
        """
        self.api_token = token
        if from_file:
            try:
                with open(token, "r") as file:
                    self.api_token = file.read().strip()
            except FileNotFoundError:
                raise FileNotFoundError(f"Error: {token} not found.")

    def from_bibcode(self, bibcode):
        """
        Fetches the BibTeX entry for a given bibcode.

        Parameters
        ----------
        bibcode : str
            The ADS bibcode.

        Returns
        -------
        str
            The BibTeX entry as a string.
        """
        url = f"https://api.adsabs.harvard.edu/v1/export/bibtex/{bibcode}"
        headers = {"Authorization": f"Bearer {self.api_token}"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            print(
                f"Error: Unable to fetch BibTeX for bibcode {bibcode}. Status code: {response.status_code}"
            )
            return None

    def from_doi(self, doi):
        """
        Fetches the BibTeX entry for a given DOI and retrieves its bibcode.

        Parameters
        ----------
        doi : str
            The DOI to query.

        Returns
        -------
        dict
            A dictionary containing the BibTeX entry and the bibcode.
        """
        # Encode DOI query
        encoded_query = urlencode(
            {"q": f"doi:{doi.strip()}", "fl": "bibcode", "rows": 1}
        )
        url = f"https://api.adsabs.harvard.edu/v1/search/query?{encoded_query}"
        headers = {"Authorization": f"Bearer {self.api_token}"}
        response = requests.get(url, headers=headers)
        jsn = response.json()
        try:
            bibcode = jsn["response"]["docs"][0]["bibcode"]
        except (KeyError, IndexError):
            raise ValueError("Unable to find the DOI.")
        return self.from_bibcode(bibcode)

    def from_library(self, library_id, max_results=None, rawstring=False):
        """
        Fetches all BibTeX entries from a given library.

        Parameters
        ----------
        library_id : str
            ID of the ADS library.
        max_results : int, optional
            Maximum number of results to fetch (default is all documents in the library).
        rawstring : bool, optional
            Whether to return raw BibTeX strings or parsed dictionaries (default is False).

        Returns
        -------
        list
            List of BibTeX entries or dictionaries.
        """
        # Determine the maximum number of results
        if max_results is None:
            url = f"https://api.adsabs.harvard.edu/v1/biblib/libraries/{library_id}"
            headers = {"Authorization": f"Bearer {self.api_token}"}
            response = requests.get(url, headers=headers)
            max_results = response.json()["metadata"]["num_documents"]

        # Fetch the library content
        url = f"https://api.adsabs.harvard.edu/v1/biblib/libraries/{library_id}/?rows={max_results}&sort=date_created&order=des"
        headers = {"Authorization": f"Bearer {self.api_token}"}
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise Exception(
                f"Error: Unable to fetch library {library_id}. Status code: {response.status_code}"
            )

        # Parse and process BibTeX entries
        bibcodes = response.json().get("documents", [])
        bibtex_entries = []
        for bibcode in tqdm(bibcodes, desc="Fetching BibTeX", total=max_results):
            bibtex = self.from_bibcode(bibcode)
            if not rawstring:
                bibtex = bibtex_to_dict(bibtex)
                bibtex["bibcode"] = bibcode
            bibtex_entries.append(bibtex)
        return bibtex_entries


# Example Usage
if __name__ == "__main__":
    # Initialize the ADSPro class with an API token
    ads_processor = ADSPro(token="/path/to/token_file", from_file=True)

    # Get BibTeX entry from a DOI
    doi = "10.1234/example.doi"
    try:
        bibtex_data = ads_processor.from_doi(doi)
        print(f"BibTeX:\n{bibtex_data}")
    except ValueError as e:
        print(e)
