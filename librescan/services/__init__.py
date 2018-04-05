from os import getenv
from .output_service import OutputService
from .project_service import ProjectService
from .image_service import ImageService
from .queue_service import queue_service

if getenv('LS_DEV_MODE'):
    from .dev_scanner_service import DevScannerService as ScannerService
else:
    from .scanner_service import ScannerService
