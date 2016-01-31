# coding: utf-8

import sys, os, re
from subprocess import *

def main():
    for device in devices():
        print(device.decode())

def devices():
    """
    """
    devices = check_output(['adb', 'devices'])
    pattern = re.compile(b"^(.+)\tdevice", re.MULTILINE);
    return pattern.findall(devices)

if __name__ == "__main__":
    main()
