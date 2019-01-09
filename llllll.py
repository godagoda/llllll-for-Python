# coding: utf-8

import sys, os, re
from subprocess import *

def main():
    has_peco = True;
    try:
        check_call('which peco', shell=True)
    except CalledProcessError, e:
        has_peco = False

    d = devices()
    selected_d = d[0]
    if len(d) > 1:
        w = "List of devices attached\n"
        for v in d:
            w += v +"\n"
        p = Popen(['peco'], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
        selected_d = p.communicate(input=w)[0].strip()

    t = map(lambda x: re.sub(" .+?$", "", x), task_affinities(selected_d))
    selected_t_name = t[0]
    if len(t) > 1:
        w = "List of task affinities\n"
        for v in t:
            w += v +"\n"
        p = Popen(['peco'], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
        selected_t_name = p.communicate(input=w)[0].strip()

    hist_number = 1;
    print("")
    print("#" * 100)
    print("## taskAffinity=" + selected_t_name)
    print("#" * 100)
    for acticity_hist in reversed(activity_hists(selected_d)):
        if acticity_hist[2].split("=")[1] == selected_t_name:
            print("")
            print("Hist #" + str(hist_number))
            print(acticity_hist[3]) #realActivity
            print(acticity_hist[4]) #state
            print(acticity_hist[0]) #processName
            print(acticity_hist[1]) #Intent
            hist_number += 1
    print("")

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
    # print(adb_dump_sys_activity(device_id))
    pattern = re.compile("\\* TaskRecord{.{7,8} #\d+ A[ =](.+?)}", re.MULTILINE)
    return pattern.findall(adb_dump_sys_activity(device_id))

def activity_hists(device_id):
    """
    """
    pattern = re.compile("\* Hist #\d+: (?:ActivityRecord|HistoryRecord){.+?}.*?(processName=.+?)\s.*?(Intent {.+?})\s.*?(taskAffinity=.+?)\s.*?(realActivity=.*?)\s.*?(state=(?:RESUMED|PAUSED|STOPPED|DESTROYED|PAUSING|STOPPING|FINISHING|DESTROYING|INITIALIZING))\s.*?(finishing=(?:true|false))\s.*?(visible=(?:true|false))\s", re.MULTILINE | re.DOTALL)
    return pattern.findall(adb_dump_sys_activity(device_id))

def devices():
    """
    """
    devices = check_output('adb devices', shell=True)
    pattern = re.compile("^(.+)\tdevice", re.MULTILINE)
    return pattern.findall(devices)

if __name__ == "__main__":
    main()