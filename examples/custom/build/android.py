'''
Created on May 26, 2016

@author: jrm
'''
import os
import subprocess
if __name__ == '__main__':
    cmd = "buildozer -v android_new debug deploy run logcat"
    print cmd
    p = subprocess.Popen(cmd.split(),stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in iter(p.stdout.readline, b''):
        print line,
    p.stdout.close()
    p.wait()