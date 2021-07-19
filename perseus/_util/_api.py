import requests
import json
from ._erros import APIConnectionError, APIPathNotFoundError, APIReturnError
from ._lang import Lang

class _APIObject():
    def __init__(self, url: str) -> None:
        self.url = url

    def _getFromAPI(self,directory: str):
        try:
            res = requests.get(self.url+"/"+directory)
        except:
            raise APIConnectionError(f"Could not connect to API server [{self.url}]. Service may be down or URL may be incorrect.")
        if res.status_code == 200:
            #Throw error if there is one
            res_json = json.loads(res.content)
            if "error" in res_json:
                raise APIReturnError(res_json["error"])
            return res_json
        elif res.status_code == 404:
            raise APIPathNotFoundError("Invalid directory")
        else:
            raise APIConnectionError(f"Error Code: {res.status_code}")