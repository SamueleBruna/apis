import abc


class AbsFinder1(abc.ABC):
    """
    This is an abstract class, which gives a template to other classes that must implement a Client and find method.
    It is based on the fact that the user must have a Google Cloud SDK active and configured to the correct project
    """
    client: None
    target: None
    logger: None

    @property
    @abc.abstractmethod
    def client(self):
        """
        This method should return the client
        """
        raise NotImplementedError

    @client.setter
    @abc.abstractmethod
    def client(self, client_func):
        """
        This method should instantiate the client
        """
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def target(self):
        """
        This method should return the target
        """
        raise NotImplementedError

    @target.setter
    @abc.abstractmethod
    def target(self, target):
        """
        This method should instantiate the target to search
        """
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def logger(self):
        """
        This method should return the logger
        """
        raise NotImplementedError

    @logger.setter
    @abc.abstractmethod
    def logger(self, target):
        """
        This method should instantiate the logger
        """
        raise NotImplementedError

    @abc.abstractmethod
    def find(self):
        """
        This method should try to find the object wanted using the client and returning the APIs response
        Best practice is to find and be sure that the target exists before applying other methods.
        This is why I want that this method should always be implemented.
        """

        raise NotImplementedError
