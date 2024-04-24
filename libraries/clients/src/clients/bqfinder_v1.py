from clients.model.absclient_v1 import AbsClient1
from clients.model.table import Table
from google.cloud.bigquery.client import Client


class BQFinder(AbsClient1):
    """
    This class aims to instantiate a connection to Bigquery and find a table.
    target is an instance of the Table class
    """

    def __init__(self, target: Table = None):
        """
        The constructor creates the instance using the setter method of client, a function should be passed.
        It creates the target attribute, which is a Table object.
        If the latter is None, it will be asked to the user to define it
        """
        self.client = Client()
        self.target = target

    @property
    def client(self):
        """
        This method should return the client
        """
        return self._client

    @client.setter
    def client(self, client_func):
        """
        This method should instantiate the client
        """
        self._client = client_func

    @property
    def target(self):
        """
        This method should return the target
        """
        return self._target

    @target.setter
    def target(self, target):
        """
        This method should instantiate the target to search
        """
        if target is not None and isinstance(target, Table):
            self._target = target

        else:
            table_name = input('Please insert the name of the table: ')
            dataset = input('Please insert the name of the dataset of the table: ')
            project = input('Please insert the name of the project of the table: ')
            self._target = Table(project, dataset, table_name)

    def find(self) -> bool:
        """
        This method should try to find the target table
        using the client proper function and returning the APIs response.
        """

        target_table = f"{self.target.project}.{self.target.dataset}.{self.target.table_name}"

        try:
            self.client.get_table(target_table)
            print(f"The table'{self.target.project}':'{self.target.dataset}'.'{self.target.table_name}' exists!")
            return True

        except Exception as e:
            print(
                f"The table'{self.target.project}':'{self.target.dataset}'.'{self.target.table_name}' doesn't exists!")
            print(e)
            return False


def main():
    project_id = "skyita-da-daita-test"
    dataset_id = "contract"
    table_id = "contract"
    table = Table(project_id, dataset_id, table_id)

    bqfind1 = BQFinder(table)
    print(bqfind1.client)
    exists1 = bqfind1.find()
    print(exists1)

    bqfind2 = BQFinder()
    exists2 = bqfind2.find()
    print(exists2)


if __name__ == "__main__":
    main()
