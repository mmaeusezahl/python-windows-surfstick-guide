# How to use a Huawei surfstick under Windows with python to send and receive SMS

## Scope of this guide

This guide is meant as starting point for users who want to send SMS from a
python script under Windows. There are quite some tutorials out there for
Linux and MacOS but nothing that worked for my specific circumstances.

This guide was written for a E3135 surfstick by Huawei. I believe that the
information provided here might help for other similar surfsticks as well.
There is quite a good list of similar devices in the [USB ModeSwitch article][1]
together with some starting point information in the ubuntuusers forum.

Possible applications (partially beyond the scope of this guide) include:
* Sending and receiving SMS with a Huawei surfstick
* Modeswitching the surfstick under Windows
* Doing other things a surf stick can do (e.g. phone calls, reading SIM contacts
using the surfstick)
* ... ?

## Background

Using a Huawei surfstick from python becomes possible, since the surfstick
supports multiple modes. There are e.g.(to my knowledge):

* A USB "mass-storage" device mode, which is initially employed whenever the stick
gets powered
* A "high-speed" mode (for example called Hi-Link on Huawei surfsticks)
* A "modem"  mode with support for traditional modem commands (also known as 
[Hayes commands][2])

A "normal" use-case for a Windows user would therefore look like this:

1. The surfstick is attached to the computer. It identifies itself as a
"mass-storage" device and Windows treats it like a CD.
![Screenshot of the Windows Explorer showing the "CD"](https://github.com/mmaeusezahl/python-windows-surfstick-guide/blob/master/screenshots/mass-storage-device-explorer.PNG?raw=true)
From the perspective of the device manager this device looks like this:
![Screenshot of the Device Manager showing the "CD"](https://github.com/mmaeusezahl/python-windows-surfstick-guide/blob/master/screenshots/mass-storage-device-device-manager.PNG?raw=true)
Notice the identifying parameters (so to say the fingerprint) of this device to
the system. A "vendor ID" (called VID) unique to Huawei and a "product ID" 
(called PID) unique to this particular srufstick (a E3135). As a side note: 
These are the values that the operating system uses to determine which drivers to load when inserting the device.
2. The user runs the `AutoRun.exe` and two things get installed:
   1. A tool called `mbbService`, which will look for the mass-storage device by
   means of its vid and pid
   2. The driver for the "high-speed" mode
3. Now a bit of magic happens. The freshly installed `mbbService` will identify
the attached surfstick in "mass-storage" mode. 

## References
This is simply a collection of all references for better display on the GITHub
page.

1. [https://wiki.ubuntuusers.de/USB_ModeSwitch/][1]
2. [https://en.wikipedia.org/wiki/Hayes_command_set][2]

[1]: https://wiki.ubuntuusers.de/USB_ModeSwitch/
[2]: https://en.wikipedia.org/wiki/Hayes_command_set