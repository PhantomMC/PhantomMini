
> This project is a work in progress. The first working release will probably be posted in late April.

# Description
A lightweight [MicroPython](http://docs.micropython.org/en/latest/unix/quickref.html) program that responds to minecraft java clients' pings with a MOTD message and an icon.
<br />Note that Phantom instances only *appear* as servers; by design, they do not support [gameplay](https://minecraft.fandom.com/wiki/Gameplay).

### Features
- Extremely lightweight -- ([minimum specs](https://github.com/wemos/docs/blob/master/docs/en/w600/w600_pico.rst#w600-pico))
- Customizable Server icon, MOTD messages, MOTD overlay, and player list preview.
- Customizable kick messages
- Customizable port.
- Options for statistics and logs.

## Background
- This project was made to broadcast on the IP of a defunct (but formerly large) server.
  - Broadcasted information included a farewell message and a link to a discord server.
  - The above was hosted on an extreme low-end dedicated server rented for several decades.

# Instructions
## Installing:
This program was designed to be interpreted with [MicroPython](https://github.com/micropython/micropython/blob/master/README.md).<br />
```diff
- Phantom has primarily been tested on Debian-based systems... minimal support for non-UNIX systems.
 ```

**To install MicroPython on most linux distros, see [this guide](https://www.raspberrypi.org/forums/viewtopic.php?p=1456736).**<br /><br />
To install MicroPython on a [SBM](https://en.wikipedia.org/wiki/Single-board_microcontroller), see [this guide](https://docs.wemos.cc/en/latest/tutorials/w600/get_started_with_micropython_w600.html).<br />
To install MicroPython for Mac, Slackware, or RHEL based systems, see [this guide](https://github.com/micropython/micropython/wiki/Getting-Started#unix).<br />
To install MicroPython for Windows, see [this guide](https://github.com/micropython/micropython/tree/master/ports/windows#building-under-cygwin)

**Once MicroPython has been installed, to run phantom, use `python phantom.py`**

# Configuration
The default config has been commented for clarity.
You can find a copy of it [here](https://github.com/the-lockedcraft-legacy-organization/PhantomServer/blob/main/config.yml).

# Changelog
```
Version 0.0.0
        | | |_ Development Iteration (Changes the code in some way)
        | |_ Feature Release (Adds a new feature)
        |_ Milestone Release (Adds a major feature from /PhantomServer/milestones)
        
```
#### [Version 0.7.0]
 - Added bstats
 - Some refactoring
 - More solid looking console messages
 - Added infastructure for upcomming userList.yml storage
#### [Version 0.6.1]
 - Async threading (not stresstested)
 - Command interpretation (currently stop and exit)
 - Fancier console messages
#### [Version 0.5.8]
 - Stores logging information
 - Added debug option in config
#### [Version 0.5.5]
 - Propper logging information
 - Major refactor
 - Improved data interpretation
#### [Version 0.5.0]
 - Working config
 - 3 different serverstyles
 - Can replace old config
#### [Version 0.3.0]
 - Send disconnect message
 - Code structure improvements
#### [Version 0.2.0]
 - Send logo to client
 - Establish connection with multiple clients syncronously (poor but working solution)
#### [Version 0.1.3]
 - Establish connection with client
 - Write proper json response
 - Respond client ping with a pong
#### [Version 0.0.0]
 - Structured Project
 - Added initial documentation and licencing.
