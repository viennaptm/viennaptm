def raise_with_logging_error(message, logger, exception_type, exp=None):
    """
    Log an error message and raise an exception.

    The message is logged at error level before raising the specified
    exception type. If an originating exception is provided, it is
    attached as the cause.

    :param message:
        Error message to log and attach to the raised exception.
    :type message: str
    :param logger:
        Logger instance used to emit the message.
    :type logger: logging.Logger
    :param exception_type:
        Exception class to raise.
    :type exception_type: type[Exception]
    :param exp:
        Optional original exception to be chained.
    :type exp: Exception or None
    :raises Exception:
        Always raises the specified exception type.
    """

    logger.error(message)
    if exp is not None:
        raise exception_type(message) from exp
    else:
        raise exception_type(message)

def raise_with_logging_warning(message, logger, exception_type):
    """
    Log a warning message and raise an exception.

    The message is logged at warning level before raising the specified
    exception type.

    :param message:
        Warning message to log and attach to the raised exception.
    :type message: str
    :param logger:
        Logger instance used to emit the message.
    :type logger: logging.Logger
    :param exception_type:
        Exception class to raise.
    :type exception_type: type[Exception]
    :raises Exception:
        Always raises the specified exception type.
    """

    logger.warning(message)
    raise exception_type(message)

def raise_with_logging_debug(message, logger, exception_type):
    """
    Log a debug message and raise an exception.

    The message is logged at debug level before raising the specified
    exception type.

    :param message:
        Debug message to log and attach to the raised exception.
    :type message: str
    :param logger:
        Logger instance used to emit the message.
    :type logger: logging.Logger
    :param exception_type:
        Exception class to raise.
    :type exception_type: type[Exception]
    :raises Exception:
        Always raises the specified exception type.
    """

    logger.debug(message)
    raise exception_type(message)


