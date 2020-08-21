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
