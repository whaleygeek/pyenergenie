# pyenergenie
A python interface to the Energenie line of products

This is a placeholder repo, for the development of an open source set of Python Libraries
to access the Energenie range of power control and monitoring products.

The Energenie product line uses the HopeRF radio transciever, and the OpenHEMS protocol
from Sentec. Energenie have built a RaspberryPi add-on board that interfaces to the HopeRF
RFM69, and allows both control and monitoring of their products from a Raspberry Pi.

This code project aims to develop an open source python module, providing access to many or all
of the features of the OpenHEMS, HopeRF and Energenie product line.

Plans
====

1. Write a minimal ctypes wrapper and build process for the existing bcm2835/HopeRF software distribution
2. Create a proof of concept demo application using the Iotic-Labs IoT infrastructure
3. Enhance the library design to support other features such as new message types, new product types
4. Hopefully provide a platform that could be further innovated on using ScratchGPIO

Purpose
====

I have a whole range of plans for building demo applications using the Energenie product line in the future,
and want to help seed further innovations using this technology in schools and in industry. To do this, I believe
that the code needs to be more flexible, accessible to all, and better structured and documented, 
so I plan to develop via a series of progressive releases an open source python wrapper that others can fork and further innovate with.

Notes
====

Sharing of SPI/GPIO with this library will be an interesting challenge,
often it is useful to also use other GPIO's and to use other SPI devices
with an alternative chip select. The bcm2835 library doesn't seem to be
provided or wrapped in a way conjucive to sharing. This might be addressed
in the second pass of coding, it's too much to chew on in the first pass.

I'm hoping to publish a low level C API to the devices that others can code
to via foreign function interfaces, and possibly a high level API that
implements basic device classes, with higher level abstractions written
in the python.

Getting perfect reuse for all on the first pass is going to be impossible.

David Whale

@whaleygeek

July 2015
