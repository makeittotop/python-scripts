import os, sys, time
setting = raw_input('Please input your time setting:')
newpid = os.fork()
if newpid == 0:
    while True:
        time.sleep(10)
        if setting <= time.strftime("%H%M",time.localtime(time.time())):
            os.system('kdialog --error "Alert!"')
            break
