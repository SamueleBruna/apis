from clients.model.absclient_v1 import AbsClient1
from clients.model.blob import Blob
from google.cloud.storage import Client


class GCSFinder(AbsClient1):
    """
    This class aims to instantiate a connection to Bigquery and find a Blob.
    target is an instance of the Blob class
    """

    def __init__(self, target: Blob = None):
        """
        The constructor creates the instance with the number of series elements that should be evaluated.
        """
        self.client = Client()
        self.target = target

    @property
    def client(self):
        """
        This method should instantiate the client
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
        if target is not None and isinstance(target, Blob):
            self._target = target

        else:
            bucket = input('Please insert the name of the bucket: ')
            path = input('Please insert the path to the blob: ')
            self._target = Blob(bucket, path)

    def find(self) -> bool:
        """
        This method should try to find the object wanted using the client and returning the APIs response
        """

        try:
            # Retrieve a blob, and its metadata, from Google Cloud Storage.
            # Note that `get_blob` differs from `Bucket.blob`, which does not
            # make an HTTP request.
            bucket = self.client.bucket(self.target.bucket)
            blob = bucket.get_blob(self.target.path)

            print(f"The blob exists! Here are some of is metadata")
            print(f"Blob: {blob.name}")
            print(f"Bucket: {blob.bucket.name}")
            print(f"Storage class: {blob.storage_class}")
            print(f"ID: {blob.id}")
            print(f"Size: {blob.size / 1048576:0.6f} Mb")
            print(f"Updated: {blob.updated}")

            return True

        except Exception as e:
            print(f"The blob'{self.target.bucket}'/'{self.target.path}'.' doesn't exists!")
            print(e)
            return False


def main():
    bucket_name = "skyita-da-daita-test-application"
    blob_name = "data-model-mapper/conf/marketing_cloud.dynamic_event/map.json"
    table = Blob(bucket_name, blob_name)

    gcsfind1 = GCSFinder(table)
    exists1 = gcsfind1.find()
    print(exists1)

    gcsfind2 = GCSFinder()
    exists2 = gcsfind2.find()
    print(exists2)


if __name__ == "__main__":
    main()
