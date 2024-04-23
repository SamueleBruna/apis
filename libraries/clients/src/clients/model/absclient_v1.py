import abc


class AbsClient1(abc.ABC):
    """
    This is an abstract class, which gives a template to other classes that must implement a Python Client.
    It is based on the fact that the user must have a Google Cloud SDK active and configured to the correct project
    """
    client : None

    @property
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