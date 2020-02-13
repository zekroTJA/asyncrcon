class InvalidPacketException(Exception):
    """
    Commonly thrown when a package does not
    fit the right format of an RCON response package.
    """

    def __init__(self):
        super(InvalidPacketException, self).__init__(
            'invalid padding data')


class AuthenticationException(Exception):
    """
    Thrown when login authentication to the
    RCON server failed.
    """

    def __init__(self):
        super(AuthenticationException, self).__init__(
            'login failed')


class NulLResponseException(Exception):
    """
    Thrown when a package response contains
    no data.
    This exception is only used internally
    and will not be thrown using the asyncrcon
    API interface.
    """

    def __init__(self):
        super(NulLResponseException, self).__init__(
            'null response')


class MaxRetriesExceedException(Exception):
    """
    Thrown when the maximum ammount of retries
    of command executions was exceed.
    """

    def __init__(self):
        super(MaxRetriesExceedException, self).__init__(
            'maximum ammount of command retries was exceed')
