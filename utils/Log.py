import logging, io, os

logging.basicConfig(format='[%(name)s-%(levelname)s] %(asctime)s: %(message)s', level=logging.INFO)

def Streamhandler(stream, level, format='[%(name)s-%(levelname)s] %(asctime)s: %(message)s'):
    stream = logging.StreamHandler(stream)
    stream.setLevel(level)
    formatter = logging.Formatter(format)
    stream.setFormatter(formatter)
    return stream
    
logger = logging.getLogger('CLOCKIN_LOG')
if os.environ.get('ACTION_ENABLED', 'false') == 'true':
    logger.propagate = False
    logger.info('ACTION_ENABLED is true, log will not output to standard stream.')
else:
    logger.info('ACTION_ENABLED is false, log will output to standard stream.')
log_stream_info = io.StringIO()
log_stream_warning = io.StringIO()
log_stream_error = io.StringIO()
logger.addHandler(Streamhandler(log_stream_info, logging.INFO))
logger.addHandler(Streamhandler(log_stream_warning, logging.WARNING))
logger.addHandler(Streamhandler(log_stream_error, logging.ERROR))
