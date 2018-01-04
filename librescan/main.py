#!/usr/bin/python3
import os

import sys
import setup
from api.libreScanWeb import LibreScanWeb
from api.app import app

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('You most provide at least one argument.')
        print('Usted debe de proveer al menos un argumento.')
        sys.exit(0)

    if sys.argv[1] == 'web':
        os.environ["LS_DEV_MODE"] = "False"
        if len(sys.argv) > 2:
            os.environ["LS_DEV_MODE"] = str(sys.argv[2] == '--dev')
        setup.run_config()
        app.run()
    else:
        print('Argument not valid.')
        print('El argumento ingresado no es válido.')
