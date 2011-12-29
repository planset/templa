# -*- encoding: utf-8 -*-
"""
    :copyright: (c) 2011 by daisuke igarashi.
"""
import subprocess

def save1280x720(url, savefilepath):
    save(url, savefilepath, width=1280, crop_h=720)

def save(url, savefilepath, 
         width=None, crop_h=None,
         wkhtmltoimage_path="/bin/wkhtmltoimage"):
    cmd = [wkhtmltoimage_path]
    if width:
        cmd.append(" --width {width}".format(width=width))
    if crop_h:
        cmd.append(" --crop-h {crop_h} ".format(crop_h=crop_h))
    cmd.append(url)
    cmd.append(savefilepath)
    
    proc = subprocess.Popen(" ".join(cmd),
                    stderr=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    shell=True)
    stdout_value, stderr_value = proc.communicate()
    #print '\tpass through:', repr(stdout_value)
    #print '\tstderr      :', repr(stderr_value)
    if stdout_value == '\n\n\n\n\n\n\n':
        raise Exception("wkhtmltoimage parameter error")
    if "Error" in stderr_value:
        raise Exception(stderr_value[stderr_value.index("Error"):])
    return 
    

