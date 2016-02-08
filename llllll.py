# coding: utf-8

import sys, os, re
from subprocess import *

def main():
    selected_d = 0
    d = devices()
    if len(d) > 1:
        w = "Please select device [0-%d].\n" % (len(d) - 1)
        for i in range(0, len(d)):
            w += str(i) + ":" + d[i] +" "
        w += "> "
        selected_d = raw_input(w)

    selected_t = 0
    t = task_affinities(d[int(selected_d)])
    if len(t) > 1:
        w = "Please select task [0-%d].\n" % (len(t) - 1)
        for i in range(0, len(t)):
            w += str(i) + ":" + t[i] +" "
        w += "> "
        selected_t = raw_input(w)

    # print(activity_hists(d[int(selected_d)], t[int(selected_t)]))
    hist_number = 1;
    print("")
    print("#" * 50)
    print("## selectedTaskAffinity=" + t[int(selected_t)])
    print("#" * 50)
    for acticity_hist in reversed(activity_hists(d[int(selected_d)], t[int(selected_t)])):
        print("")
        print("Hist #" + str(hist_number))
        for val in acticity_hist:
            print val
        hist_number = hist_number + 1

def adb_version(device_id):
    """
    """
    return check_output('adb -s ' + device_id +' version', shell=True)

def adb_dump_sys_activity(device_id):
    """
    """
    return check_output('adb -s ' + device_id +' shell dumpsys activity activities', shell=True)

def task_affinities(device_id):
    """
    """
    pattern = re.compile("\\* TaskRecord{.+ #\d+ A[ =](.+) U.+}", re.MULTILINE)
    # print(adb_dump_sys_activity(device_id))
    return pattern.findall(adb_dump_sys_activity(device_id))

def activity_hists(device_id, task_afinity):
    """
    """
    pattern = re.compile("\* Hist #\d+: ActivityRecord{.+?}.*?(processName=.+?)\s.*?(Intent {.+?})\s.+?taskAffinity=" + task_afinity + "\s.*?(realActivity=.*?)\s.*?(state=(?:RESUMED|PAUSED|STOPPED|DESTROYED|PAUSING|STOPPING|FINISHING|DESTROYING|INITIALIZING))\s.*?(finishing=(?:true|false))\s.*?(visible=(?:true|false))\s", re.MULTILINE | re.DOTALL)
    return pattern.findall(adb_dump_sys_activity(device_id))

def devices():
    """
    """
    devices = check_output('adb devices', shell=True)
    pattern = re.compile("^(.+)\tdevice", re.MULTILINE)
    return pattern.findall(devices)

if __name__ == "__main__":
    main()