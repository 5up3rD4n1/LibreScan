import sys
import logging
import logging.config
from librescan.config import config


def get_logger():
    format_string = '%(asctime) - s %(levelname)s %(message)s'
    ls_logger = logging.getLogger('librescan')

    if ls_logger.hasHandlers():
        ls_logger.handlers.clear()

    ls_logger.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler(sys.stdout)
    file_handler = logging.FileHandler(filename=config.get_config_folder() + '/librescan.log', encoding='UTF-8')

    formatter = logging.Formatter(fmt=format_string)
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    ls_logger.addHandler(console_handler)
    ls_logger.addHandler(file_handler)
    return ls_logger


logger = get_logger()
