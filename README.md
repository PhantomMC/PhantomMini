# Description
A lightweight [MicroPython](http://docs.micropython.org/en/latest/unix/quickref.html) program that responds to minecraft java clients' pings with a MOTD message and an icon.
Designed to run on extreme low-end VPSs; Phantom works by responding to [Server List Pings](https://wiki.vg/Server_List_Ping); it therefore doesn't function as a playable server.

### Features
- Extremely lightweight -- designed to be run on extreme low-end systems.
- Customizable MOTD and server icon.
- Customizable Port.

## Background
- This project was made to broadcast on the IP of a defunct (but formerly large) server.
  - Broadcasted information included a farewell message and a link to a discord server.
  - The above was hosted on an extreme low-end dedicated server rented for several decades.

# Instructions
## Installing:
This is a python program designed to be interpreted via [MicroPython](https://github.com/micropython/micropython/blob/master/README.md).
Specifically, it has been tested on the [MicroPython Unix Port](http://docs.micropython.org/en/latest/unix/quickref.html).

To install MicroPython on Unix, see [this guide](https://github.com/micropython/micropython/wiki/Getting-Started#unix).
To run this program, use `micropython phantom.py`

# Configuration
|Name|Type|Description|
--- | --- | ---
|MOTD|STRING|generated from [this website](https://minecraft.tools/en/motd.php)|
|image_link|string|path to a 64x64 pixel png file|
|port|integer|The port from which Phantom will respond to clients requests.|

# Changelog
```
Version 0.0.0
        | | |_ Development Iteration (Changes the code in some way)
        | |_ Feature Release (Adds a new feature)
        |_ Milestone Release (Adds a major feature from /PhantomServer/milestones)
```
#### [Version 0.0.0]
 - Structured Project
 - Added initial documentation and licencing.
