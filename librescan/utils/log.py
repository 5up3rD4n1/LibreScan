import logging
import os.path


class Log:
    def __init__(self):
        homedir = os.path.expanduser('~')
        logging.basicConfig(filename=homedir + '/.librescan/librescan.log',
                            format='%(asctime) - s %(levelname)s:%(message)s', level=logging.DEBUG)
        self.log = logging

    def debug(self, p_message):
        self.log.debug(p_message)

# logger types
# logging.debug('debug message')
# logging.info('info message')
# logging.warn('warn message')
# logging.error('error message')
# logging.critical('critical message')
