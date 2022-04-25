import logging, io

# static
class Log(object):
    logging.basicConfig(format='[%(levelname)s] %(asctime)s: %(message)s', level=logging.INFO)
    logger = logging.getLogger('clockin')
    log_stream = io.StringIO()
    logger.addHandler(logging.StreamHandler(log_stream))
