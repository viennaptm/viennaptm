def raise_with_logging_error(message, logger, exception_type):
    logger.error(message)
    raise exception_type(message)

def raise_with_logging_warning(message, logger, exception_type):
    logger.warning(message)
    raise exception_type(message)


