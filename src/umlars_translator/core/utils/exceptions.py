class IdMismatchException(Exception):
    """
    Exception thrown when no matching ID is found during the objects binding.

    Error message structure:
        Parser Error: {error_message}

    """
