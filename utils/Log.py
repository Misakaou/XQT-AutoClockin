import logging, io

# static
logging.basicConfig(format='[%(name)s-%(levelname)s] %(asctime)s: %(message)s', level=logging.DEBUG)

def Streamhandler(stream, level, format='[%(name)s-%(levelname)s] %(asctime)s: %(message)s'):
    stream = logging.StreamHandler(stream)
    stream.setLevel(level)
    formatter = logging.Formatter(format)
    stream.setFormatter(formatter)
    return stream
    
logger = logging.getLogger('CLOCKIN_LOG')
log_stream_info = io.StringIO()
log_stream_warning = io.StringIO()
log_stream_error = io.StringIO()
logger.addHandler(Streamhandler(log_stream_info, logging.INFO))
logger.addHandler(Streamhandler(log_stream_warning, logging.WARNING))
logger.addHandler(Streamhandler(log_stream_error, logging.ERROR))
