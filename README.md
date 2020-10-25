# How to use a Huawei surfstick in modem mode under Windows to send and receive SMS (with python)

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
These are the values that the operating system uses to determine which drivers 
to load when inserting the device. You can see that in my case the combination
12d1:1f01 (as written in linux terms vid:pid) matches [this list][1].
2. The user runs the `AutoRun.exe` and two things get installed:
   1. A tool called `mbbService`, which will look for the mass-storage device by
   means of its vid and pid
   2. The driver for the "high-speed" mode
3. Now a bit of magic happens. The freshly installed `mbbService` will identify
the attached surfstick in "mass-storage" mode. It will the send a "magic"
message to the surfstick which will immediately trigger a so called mode-switch
in the surfstick. It will briefly reset the connection and the reappear as a new
kind of device to the operation system. This happens very quickly, but sometimes
the user can quickly see the fake "CD" appearing before the actual surfstick
loads. Since the `mbbService` places itself in autostart, this will also happen
after the system is restarted or the surfstick is reinserted.
4. From the perspective of the device manager, the device now has a new ID (in
my case 12d1:14dc). It therefore loads the actual driver for the "high-speed"
mode and a webpage will open, querying the user to connect, provied a PIN etc.

This works well for actually connecting to the internet, but sometimes it is not
desired to have a fully fledged high-speed connection. In my case, I just wanted
to send SMS using a python script. It seems possible to directly talk to the
HTML pages in the background, but this appeared rather complicated to me. (There
seems to be a project which does exactly this though 
[huawei-modem-python-api-client][3])

It is however well known, that there is the other "modem mode" which provides an
easy to use interface for sending SMS. There are also some python libraries
which directly target this mode (see [python-gsmmodem-new][4] and [pyhumod][5]).
To me this seems to have the following advantages:

* More direct approach; less vulnearble to mistakes in the implementation
* Translates well to other modems of similar kind (even if the HTML changes)
* I don't want or need a mobile data connection
* I like to emply FOSS as far as possible (it seems more future-proof)

There is

The main remaining challenges for this guide are therefore mainly:
* Mode-switching the surfstick under Windows, ideally without using the
proprietary Huawei software

## Doing the mode switch using python

There is a similar guide [here][6], which I couldn't get working.

## Final thoughs

If someone ever feels like porting the "options" Linux driver to Windows it
would make the whole thing using FOSS.

## Some hints and troubleshooting

* Make sure the SIM card is inserted the correct way... Seriously, this cost me
multiple hours of debugging. There is a small engraving in the surfstick showing
the orientation.
* Use a USB 2.0 port with no in-between USB switches.
* If you are using this the first time, I'd recommend to use the full driver
installation first (maybe in a virtual machine) and see if your stick e.g. has
a SIM lock. This will save you hours of work.
* Linux will load the option driver to provide the serial ports on 
´/dev/ttyUSB0´ to 
* If you are using VirtualBox with USB passthrough (e.g. to test under Linux)
  * Use the "USB 2.0 (OHCI, EHCI)" mode from the extension pack. Neither
  * Make plenty use of the `lsusb` and `usb-device` commands to see, which VID
  and PID are currently loaded.
* If you want to uninstall the driver and `mbbService` once installed do the
following:
  1. Run the uninstaller from `C:\Program Files (x86)\MobileBrServ` or 
  `C:\Program Files (x86)\mbbService` (or similar)
  2. Uninstall the various Huawei devices from the device manager. You can 
  easily find all of them if susing View->Device by container. There should be 
  a category called "Huawei Mobile" which lists the various described modes as 
  explained in this guide. Usually you can just uninstall all of them.
  3. It should not be necessary to restart Windows. If done correctly, the next
  time you attach the srufstick, it will be in "mass-storage" mode again.
* If the stick is in "mass-storage" mode, but no files show up in the explorer?
This could happen after using Zadig or installing the official drivers.
  * There are actually two drivers to choose from
  * Go to the device manager
  * Right click the mass-storage device which is your Huawei surfstick
  * Select "Update driver"
  * Select "Browser my computer for files"
  * Select "Let me pick from a list of installed drivers on this computer"
  * Usually there will be two drivers. One of them works ;)

## References
This is simply a collection of all references for better display on the GITHub
page.

1. [https://wiki.ubuntuusers.de/USB_ModeSwitch/][1]
2. [https://en.wikipedia.org/wiki/Hayes_command_set][2]
3. [https://github.com/pablo/huawei-modem-python-api-client][3]
4. [https://github.com/babca/python-gsmmodem][4]
5. [https://github.com/oozie/pyhumod][5]
6. [https://zedt.eu/tech/hardware/switch-huawei-e3131-hilink-modem-mode/][6]

[1]: https://wiki.ubuntuusers.de/USB_ModeSwitch/
[2]: https://en.wikipedia.org/wiki/Hayes_command_set
[3]: https://github.com/pablo/huawei-modem-python-api-client
[4]: https://github.com/babca/python-gsmmodem
[5]: https://github.com/oozie/pyhumod
[6]: https://zedt.eu/tech/hardware/switch-huawei-e3131-hilink-modem-mode/