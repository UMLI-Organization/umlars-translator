class ServiceConnectionError(Exception):
    """Service outage error."""


class QueueUnavailableError(Exception):
    """Queue outage error."""


class NotYetAvailableError(Exception):
    """Service not yet available error."""


class ServiceUnexpectedBehaviorError(Exception):
    """
    Service behaviour was different than expected.
    Can be raised when received response didn't contain the required fieelds.
    """


class ExternalServiceOperationError(Exception):
    """External service failure error."""


class InputDataError(Exception):
    """Input data error."""
