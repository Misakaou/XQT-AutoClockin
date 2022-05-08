import logging, io, os

logging.basicConfig(format='[%(name)s-%(levelname)s] %(asctime)s: %(message)s', level=logging.INFO)

class Log:
    _logger = None
    _name = None
    _log_stream_info = None
    _log_stream_warning = None
    _log_stream_error = None
    
    def __init__(self, name:str) -> None:
        self._logger = logging.getLogger('CLOCKIN_LOG_' + name)
        self._name = name
        self._init_action()
        self._log_stream_info = io.StringIO()
        self._log_stream_warning = io.StringIO()
        self._log_stream_error = io.StringIO()
        self._init_add_handler()
    
    def _init_action(self) -> None:
        if os.environ.get('ACTION_ENABLED', 'false') == 'true':
            self._logger.propagate = False
            self._logger.info('ACTION_ENABLED is true, log will not output to standard stream.')
        elif os.environ.get('ACTION_ENABLED', 'false') == 'debug':
            self._logger.info('ACTION_ENABLED is debug, log will output to standard stream.')
        else:
            self._logger.info('ACTION_ENABLED is false, log will output to standard stream.')
    
    def _init_add_handler(self) -> None:
        self._logger.addHandler(self._get_stream_handler(self._log_stream_info, logging.INFO))
        self._logger.addHandler(self._get_stream_handler(self._log_stream_warning, logging.WARNING))
        self._logger.addHandler(self._get_stream_handler(self._log_stream_error, logging.ERROR))
    
    def _get_stream_handler(self, stream, level, format='[%(name)s-%(levelname)s] %(asctime)s: %(message)s') -> None:
        stream = logging.StreamHandler(stream)
        stream.setLevel(level)
        formatter = logging.Formatter(format)
        stream.setFormatter(formatter)
        return stream
    
    def add_stringio_handler(self, stringIO:io.StringIO):
        stream = self._get_stream_handler(stringIO, logging.DEBUG)
        self._logger.addHandler(stream)
        return stream
        
    def remove_stringio_handler(self, io) -> None:
        self._logger.removeHandler(io)
    
    def get_logger(self) -> logging.Logger:
        return self._logger
    
    def get_info(self) -> str:
        return self._log_stream_info.getvalue()
    
    def get_warning(self) -> str:
        return self._log_stream_warning.getvalue()
    
    def get_error(self) -> str:
        return self._log_stream_error.getvalue()
    
    def get_name(self) -> str:
        return self._name


if __name__ == '__main__': # test
    log = Log('test')
    log.get_logger().info('test1')
    print('-------------')
    current_string_io = io.StringIO()
    current_stream = log.add_stringio_handler(current_string_io)
    log.get_logger().info('123123123')
    print('-------------')
    print(log.get_info())
    print('-------------')
    print(current_string_io.getvalue())
    print('-------------')
    log.remove_stringio_handler(current_stream)
    log.get_logger().info('456456456')
    print('-------------')
    print(current_string_io.getvalue())
    print('-------------')
    print(log.get_info())