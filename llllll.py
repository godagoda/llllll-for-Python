# coding: utf-8

import sys, os, re
from subprocess import *

def main():
    has_peco = True;
    try:
        check_call('which peco', shell=True)
    except CalledProcessError, e:
        has_peco = False

    selected_d = 0
    d = devices()
    if len(d) > 1:
        w = "Please select device [0-%d]\n" % (len(d) - 1)
        for i, v in enumerate(d):
            w += str(i) + "::" + v +"\n"
        w += "> "
        selected_d = raw_input(w)


    t = map(lambda x: re.sub(" .+?$", "", x), task_affinities(d[int(selected_d)]))
    selected_t_name = t[0]
    if len(t) > 1:
        w = ""
        for v in t:
            w += v +"\n"
        p = Popen(['peco'], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
        selected_t_name = p.communicate(input=w)[0].strip()

    hist_number = 1;
    print("")
    print("#" * 80)
    print("## taskAffinity=" + selected_t_name)
    print("#" * 80)
    for acticity_hist in reversed(activity_hists(d[int(selected_d)])):
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