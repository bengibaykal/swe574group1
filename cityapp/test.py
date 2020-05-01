import requests
from certifi import where

def main():
    SEARCHPAGE = "cat"
    PARAMS = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch": "Nelson Mandela"
    }
    URL = "https://www.mediawiki.org/w/api.php"
    R = requests.get(url=URL, params=PARAMS, verify=where())

    print(R.url)


if __name__ == "__main__":
    main()
