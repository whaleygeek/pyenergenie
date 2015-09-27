# pyenergenie
A python interface to the Energenie line of products


This is the beginnings of an open source library to access the Energine range of
power control and monitoring products from within Python.

The Energenie product line uses the HopeRF radio transciever, and the OpenHEMS 
protocol from Sentec. Energenie have built a RaspberryPi add-on board that 
interfaces to the HopeRF RFM69, and allows both control and monitoring of their 
products from a Raspberry Pi.

There are some existing Python libraries for some Energenie products, but they
do not support the full radio interface and full product range.

Energenie also have a modified set of C test code based on the HopeRF test harness,
but this does not support all products, all variants of Raspberry Pi hardware,
or all versions of the Raspbian OS.

This project aims to develop an open source Python module, providing 
access to many or all of the features of the OpenHEMS, HopeRF and Energenie 
product line.


Purpose
====

This release, as of 27/09/2015, is the beginnings of this work.
It is not representative of the final API, but it is a starting point for me to
start experimenting with ideas and testing out reliability, with a view to using
these products to integrate into an Internet of Things solution provided by
Iotic-Labs Ltd.

With it, you can receive monitor payloads from an Energenie MiHome Adaptor Plus,
directly within Python programs. This type of plug can be used for energy monitoring
and also for relay control of the socket.

I've tried to make this a 'zero install' and 'zero configuration' experience.
In theory (at least) you should be able to download the zip or git-clone,
plug in your Energenie radio, plug in your MiHome Adapter Plus, and run the code
to see data coming back.


Getting Going
====

1. Plug in your ENER314-RT-VER01 board from energine onto the 26 pin connector of
your Raspberry Pi. At the moment I have only tested this with a Raspberry Pi B,
although there is no reason why it should not work with any of the models currently
available on the market. The underlying GPIO and SPI has been tested in other
projects on a Pi2 for example.

2. Use the Download As Zip link to the right, and unzip the files onto your
Raspberry Pi. 

3. unzip the software

    unzip pyenergenie-master.zip
    cd pyenergenie-master
    cd assets/src

4. run the monitor test program

    sudo python monitor.py

After a few seconds, you should see some packet dumps appearing on the screen.
The last few bytes will be 0x73 0x01 0x01 or 0x73 0x01 0x00 and these indicate
the switch state of the plug. Press the button on the front of the plug to
turn the switch on and off, and you should see the 0x01 change to 0x00 and
back again.

If it crashes, it sometimes leaves the radio in an indeterminite state, remove
and replace the radio board and it should reset it (but see notes below about this).


Plans
====

1. Add RESET support - the radio sometimes gets into an unknown and unrecoverable
state and I have to remove the board to reset the radio. There might be a RESET
line or a RESET command that can be sent at startup to solve this.

2. Write an OpenHEMS decoder to decode the messages for friendly display. I will
probably decode the hex buffer into a pydict, and then write a pydict to text
formatter. This will expose the whole of OpenHEMS in a really nice Python structure
to improve further innovation within Python.

3. Write an OpenHEMS encoder to encode friendly messages. I will probably
take a pydict with header and records in it and encode into a buffer that is
then transmitted via the radio interface. As above, this will expose message
creation in a really nice Python structure to improve further innovation within
Python.

4. Construct commands for switch-on and switch-off, and test sending these to a
specific sensorid.

5. Write a discovery service that sends a monitor command, then collects all
the receive messages and builds an internal dictionary of devices that respond.
I will probably at this point build a Python object for each device that responds,
and this object will be a proxy that can be used to monitor and control that device,
thus allowing any number of devices to be monitored and controlled in a 'Pythonic'
way.

6. Push a fair amount of the radio interface and some of OpenHEMS back down into
a C library that implements the same interface as what we have at this point in the
Python. Write a ctypes wrapper around this, so that the identical Python internal
API is presented. The idea being that the first pass of Python coding defines the
API we want to use, and the second pass turns this into a single library that
does everything, exposed to Python via ctypes, but linkable to other applications
and languages too.


David Whale

@whaleygeek

September 2015
