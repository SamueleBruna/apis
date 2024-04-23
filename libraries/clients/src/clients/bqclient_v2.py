import os

from clients.model.absclient_v2 import AbsClient
from google.oauth2 import service_account
from google.cloud import bigquery
from pathlib import Path

CRED_PATH = '../../s_acc/s_acc.json'



class BQClient(AbsClient):
    """
    This class aims to instantiate a connection to Bigquery and get some info.
    target is an instance of the Table class
    """

    def __init__(self, target):
        """
        The constructor creates the instance with the number of series elements that should be evaluated.
        """
        self._auth = self.__authenticate(CRED_PATH)
        self.client = self.client(self._auth)
        self.table = target

    @staticmethod
    def __authenticate(credentials_path):
        """
        The abstract method should retrieve the credentials to authenticate to the service.
        """

        s_acc_path = os.getcwd() / Path(credentials_path)
        auth = service_account.Credentials.from_service_account_file(s_acc_path)
        return auth

    def client(self):
        """
        This method should instantiate the client
        """
        raise NotImplementedError

    def find(self):
        """
        This method should try to find the object wanted using the client and returning the APIs response
        """

        raise NotImplementedError









