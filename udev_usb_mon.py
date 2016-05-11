import glib

from pyudev import Context, Monitor
import pyudev
import subprocess 

def get_block_infos(dev_name):
    dev = pyudev.Device.from_device_file(context, dev_name)


    try:
        objProc = subprocess.Popen('lsblk --nodeps %s | grep -v SIZE  | awk \'{ print $4 }\'' % dev.get('DEVNAME'), shell=True, bufsize=0, executable="/bin/bash", stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except OSError, e:
        print(e)

    #  stdOut.communicate() --> dimension [0]: stdout, dimenstion [1]: stderr
    stdOut = objProc.communicate()

    print('<BLOCK INFORMATION>')
    print('Device name: %s' % dev.get('DEVNAME'))
    print('Device type: %s' % dev.get('DEVTYPE'))
    print('Bus system: %s' % dev.get('ID_BUS'))
    print('Partition label: %s' % dev.get('ID_FS_LABEL'))
    print('FS: %s' % dev.get('ID_FS_SYSTEM_ID'))
    print('FS type: %s' % dev.get('ID_FS_TYPE'))
    print('Device usage: %s' % dev.get('ID_FS_USAGE'))
    print('Device model: %s' % dev.get('ID_MODEL'))
    print('Partition type: %s' % dev.get('ID_PART_TABLE_TYPE'))
    print('USB driver: %s' % dev.get('ID_USB_DRIVER'))
    print('Path id: %s' % dev.get('ID_PATH'))
    print('Capacity: %s' % stdOut[0].strip())
    print('</BLOCK INFORMATION>')

def get_usb_infos(dev_path):
    print('<USB INFORMATION>')

    usb_removable_device = None

    # deprecated and removed from dbus
    # print(pyudev.Device.from_path(context, id_path))  
    # because I found no other documented way, I iterate
    # over all  devices and match my pci path..
    for device in context.list_devices(subsystem='usb'):
        usb_dev_path = device.get('DEVPATH')

        if dev_path.startswith(usb_dev_path):
            # this matches the usb hub,
            # the usb controller and
            # in third place the usb stick
            # so lets watch out for the
            # longest/most precise match

            try:
                if len(usb_dev_path) > len(usb_removable_device.get('DEVPATH')):
                    usb_removable_device = device
            except AttributeError:
                # ignore because in first loop
                # usb_removable_device is None and
                # there is no usb_removable_device.get() attrib
                usb_removable_device = device

            # get more information with usb_removable_device.items()
            print('Vendor: %s' % usb_removable_device.get('ID_VENDOR_FROM_DATABASE'))
            print('</USB INFORMATION>')

try:
    from pyudev.glib import MonitorObserver

    def device_event(observer, device):
        get_block_infos(device.get('DEVNAME'))
        get_usb_infos(device.get('DEVPATH'))
except:
    from pyudev.glib import GUDevMonitorObserver as MonitorObserver

    def device_event(observer, action, device):
        get_block_infos(device.get('DEVNAME'))
        get_usb_infos(device.get('DEVPATH'))


context = Context()
monitor = Monitor.from_netlink(context)

monitor.filter_by(subsystem='block')
observer = MonitorObserver(monitor)

observer.connect('device-event', device_event)
monitor.start()

glib.MainLoop().run()
