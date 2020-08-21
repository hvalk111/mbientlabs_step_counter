# Hardware

9-axis gyrometer, accelerometer, magnetometer
* [mbientlab MMR](https://mbientlab.com/store/metamotionr/)

Bluetooth LE Dongle
* [Wavlink Nano Wireless Bluetooth CSR 4.0 Dongle](https://www.newegg.com/p/1GK-004B-00001)

MacBook Pro

# Setup

> Mostly followed mbientlab's [Python API tutorial](https://mbientlab.com/tutorials/PyLinux.html) for Linux

### Virtual Linux Machine

>  Oracle VM VirtualBox Manager + Extension Pack were used to run Ubuntu Linux on a MacBook Pro running MacOS Catalina 10.15.5
>> I'm not certain that the Extension Pack was necessary, but some forums seemed to think it helped with bluetooth connectivity issues

### Installations

> **It is very important to install everything using sudo**. The bluetooth protocols require root access, so if python and your python packages are installed locally, none of the MetaWear API scripts will work.

### Connectivity Issues

> Connecting the MMR to my linux virtual machine proved extraordinarily difficult. Some or all of these troubleshooting steps may have fixed the issues, but I'm not sure which.
>
> Under Linux VirtualBox Settings > Ports > USB. Bluetooth dongle was added to USB device filters. This supposedly makes the dongle available for use by Linux, but I still encountered problems. When plugging in the dongle the MacOS automatically switches from looking for bt devices through its drivers to looking for bt devices through the dongles drivers. Therefore when you start your virtual machine the dongle is already in use by the MacOS and cannot be used by Linux. However, you can override the automatic switching by your MacOS with the following command in your MacOS terminal
```
sudo nvram bluetoothHostControllerSwitchBehavior=never
```
> Solution was found on [Oliver Jobson's blog](https://www.oliverjobson.co.uk/technology/solved-mac-os-host-usb-bluetooth-device-not-available-for-guest-os-virtual-machine/). My airpods no longer work but oh well

### Start-Up

> Assuming you've gotten everything to work previously, to connect from fresh Linux reboot
> 1) Plug in dongle
> 2) Run the following code in terminal
```
sudo hciconfig hci0 up
```
> 3) Check that the device is found
```
sudo hcitool dev
```
> Output should look like this:
```
Devices:
      hci0     00:1A:7D:DA:71:13
```
> If that doesn't work, run
```
sudo hciconfig -a
```
> Output should look like this
```
hci0:	Type: Primary  Bus: USB
	BD Address: 00:1A:7D:DA:71:13  ACL MTU: 310:10  SCO MTU: 64:8
	UP RUNNING 
	RX bytes:676 acl:0 sco:0 events:47 errors:0
	TX bytes:3157 acl:0 sco:0 commands:47 errors:0
	Features: 0xff 0xff 0x8f 0xfe 0xdb 0xff 0x5b 0x87
	Packet type: DM1 DM3 DM5 DH1 DH3 DH5 HV1 HV2 HV3 
	Link policy: RSWITCH HOLD SNIFF PARK 
	Link mode: SLAVE ACCEPT 
	Name: 'hvalk111-VirtualBox'
	Class: 0x0c0000
	Service Classes: Rendering, Capturing
	Device Class: Miscellaneous, 
	HCI Version: 4.0 (0x6)  Revision: 0x22bb
	LMP Version: 4.0 (0x6)  Subversion: 0x22bb
	Manufacturer: Cambridge Silicon Radio (10)
```
> If it looks like this ...
```
hci0:	Type: Primary  Bus: USB
	BD Address: 00:00:00:00:00:00  ACL MTU: 0:0  SCO MTU: 0:0
	DOWN 
	RX bytes:0 acl:0 sco:0 events:0 errors:0
	TX bytes:6 acl:0 sco:0 commands:2 errors:0
	Features: 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00
	Packet type: DM1 DH1 HV1 
	Link policy: 
	Link mode: SLAVE ACCEPT 
```
> ... then Linux is picking up your dongle but not connecting to the MMR. Unplugging your dongle and plugging it back in sometimes fixes this problem.

# Data

### Gyroscope

> gyro data is angular velocity in degrees per second. x, y, and z field represent the amount of spin around each axis.

>
