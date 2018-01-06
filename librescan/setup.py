#!/usr/bin/python3

import os
import yaml
from shutil import copyfile
from setuptools import setup, find_packages
from api.i18n.PoParser import PoParser

USERHOME = os.environ["HOME"]
RESOURCESPATH = './config'
LIBRESCANPATH = USERHOME + "/LibreScanProjects"
LSCONFIGPATH = USERHOME + "/.librescan"


def create_folders():
    try:
        os.mkdir(LIBRESCANPATH)
    except OSError:
        print("warning: Folder "+LIBRESCANPATH+" already exists")

    try:
        os.mkdir(LSCONFIGPATH)
    except OSError:
        print("warning: Folder "+LSCONFIGPATH+" already exists")


def create_config_files():
    template_path = "/defaultProjectConfig.yaml"
    project_template = RESOURCESPATH + template_path
    copyfile(project_template, LSCONFIGPATH + template_path)

    if os.path.exists(LSCONFIGPATH+"/projects.yaml"):
        # os.remove(LSCONFIGPATH+"/projects.yaml")
        print("warning: projects.yaml already exists")
    else:
        os.mknod(LSCONFIGPATH+"/projects.yaml")

    if os.path.exists(LSCONFIGPATH+"/config.yaml"):
        # os.remove(LSCONFIGPATH+"/config.yaml")
        print("warning: config.yaml already exits")
    else:
        os.mknod(LSCONFIGPATH+"/config.yaml")
        data_map = {
            'email-receiver': 'librescan@gmail.com',
            'project': {
                'last-id': 0,
                'path': LIBRESCANPATH
            }
        }

        f = open(LSCONFIGPATH+"/config.yaml", 'w')
        f.write(yaml.dump(data_map, default_flow_style=False, allow_unicode=True))
        f.close()


def run_config():
    print("INFO: Running initial config")
    create_folders()
    create_config_files()
    PoParser.compile_po_files()
    print("INFO: Initial config finished")


if __name__ == '__main__':
    run_config()
