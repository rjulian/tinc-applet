#!/usr/bin/python3


import os
from distutils.core import setup


RESOURCES_DIRECTORY_PATH="/usr/share/tinc-applet"

def find_resources(resource_dir):
    target_path = os.path.join(RESOURCES_DIRECTORY_PATH, resource_dir)
    resource_names = os.listdir(resource_dir)
    resource_list = [os.path.join(resource_dir, file_name) for file_name in resource_names]
    return (target_path, resource_list)


setup(name="tincapplet",
      version="1.0",
      description="Tinc Applet Indicator for Ubuntu",
      url='https://github.com/rjulian/tinc-applet',
      author='rjulian',
      author_email='richard@rjulian.net',
      license='GPL',
      packages=["tincapplet"],
      data_files=[
          ('/usr/share/applications', ['tinc-applet.desktop']),
          find_resources("img/")],
      scripts=["bin/tinc-applet"]
)
