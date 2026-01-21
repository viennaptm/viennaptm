def raise_with_logging_error(message, logger, exception_type, exp=None):
    logger.error(message)
    if exp is not None:
        raise exception_type(message) from exp
    else:
        raise exception_type(message)

def raise_with_logging_warning(message, logger, exception_type):
    logger.warning(message)
    raise exception_type(message)

def raise_with_logging_debug(message, logger, exception_type):
    logger.debug(message)
    raise exception_type(message)


