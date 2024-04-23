import abc


class AbsClient2(abc.ABC):
    """
    This is an abstract class, which gives a template to other classes that must implement a Python Client.
    """

    @staticmethod
    @abc.abstractmethod
    def __authenticate(credentials_path):
        """
        The abstract method should retrieve the credentials to authenticate to the service.
        """

        raise NotImplementedError

    @abc.abstractmethod
    def client(self):
        """
        This method should instantiate the client
        """
        raise NotImplementedError

    @abc.abstractmethod
    def find(self):
        """
        This method should try to find the object wanted using the client and returning the APIs response
        """

        raise NotImplementedError