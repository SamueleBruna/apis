from clients.model.absclient_v1 import AbsClient1
from clients.model.blob import Blob
from google.cloud.storage import Client
from logger.logger import Logger


class GCSFinder(AbsClient1):
    """
    This class aims to instantiate a connection to Bigquery and find a Blob.
    target is an instance of the Blob class
    """

    def __init__(self, target: Blob = None,  logger: Logger = Logger()):
        """
        The constructor creates the instance using the setter method of client, a function should be passed.
        It creates the target attribute, which is a Blob object.
        If the latter is None, it will be asked to the user to define it
        """
        self.client = Client()
        self.target = target
        self.logger = logger

    @property
    def client(self):
        """
        This method should instantiate the client
        """
        return self._client

    @client.setter
    def client(self, client_obj):
        """
        This method should instantiate the client
        """
        self._client = client_obj

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
        if target is not None and isinstance(target, Blob):
            self._target = target

        else:
            bucket = input('Please insert the name of the bucket: ')
            path = input('Please insert the path to the blob: ')
            self._target = Blob(bucket, path)

    @property
    def logger(self):
        """
        This method should return the logger
        """
        return self._logger

    @logger.setter
    def logger(self, logger_obj):
        """
        This method should instantiate the logger
        """
        self._logger = logger_obj

    def find(self) -> bool:
        """
        This method should try to find the target table
        using the client proper function and returning the APIs response.
        """

        try:
            # Retrieve a blob, and its metadata, from Google Cloud Storage.
            # Note that `get_blob` differs from `Bucket.blob`, which does not
            # make an HTTP request.
            bucket = self.client.bucket(self.target.bucket)
            blob = bucket.get_blob(self.target.path)

            self.logger.info(f"The blob exists! Here are some of is metadata")
            self.logger.info(f"Blob: {blob.name}")
            self.logger.info(f"Bucket: {blob.bucket.name}")
            self.logger.info(f"Storage class: {blob.storage_class}")
            self.logger.info(f"ID: {blob.id}")
            self.logger.info(f"Size: {blob.size / 1048576:0.6f} Mb")
            self.logger.info(f"Updated: {blob.updated}")

            return True

        except Exception as e:
            self.logger.error(f"The blob'{self.target.bucket}'/'{self.target.path}'.' doesn't exists!")
            self.logger.exception(e)
            return False


def main():
    bucket_name = "skyita-da-daita-test-application"
    blob_name = "data-model-mapper/conf/marketing_cloud.dynamic_event/map.json"
    table = Blob(bucket_name, blob_name)

    gcsfind1 = GCSFinder(table)
    print(gcsfind1.client)
    exists1 = gcsfind1.find()
    print(exists1)

    gcsfind2 = GCSFinder()
    exists2 = gcsfind2.find()
    print(exists2)


if __name__ == "__main__":
    main()
