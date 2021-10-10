
> This project is a work in progress. The first working release will probably be posted in late December.

# Description
A lightweight [C](https://www.iso.org/standard/74528.html) server that responds to requests from MC clients with a MOTD and an icon.
<br />Note that Phantom instances only *appear* as servers; by design, they do not support [gameplay](https://minecraft.fandom.com/wiki/Gameplay).

### Features
- Extremely lightweight -- ([minimum specs](https://github.com/wemos/docs/blob/master/docs/en/w600/w600_pico.rst#w600-pico) - [suggested spects](https://www.friendlyarm.com/index.php?route=product/product&product_id=132))
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
1. Extract the program to a directory on a UNIX os
   - *Only Debian has been tested; other systems may work as well.*
2. Edit the `config.yml` file.
3. While in the directory with phantom.c, run `make`
   - *Phantom was designed with [gcc](https://gcc.gnu.org/) and [make](https://www.gnu.org/software/make/manual/make.html)*
   - *They are installed by default on most OS systems*.
4. Run `./PhantomServer`

# Configuration
The default config has been commented for clarity.
You can find a copy of it [here](https://github.com/the-lockedcraft-legacy-organization/PhantomServer/blob/c/config.yml).

# Changelog
```
Version 0.0.0
        | | |_ Development Iteration (Changes the code in some way)
        | |_ Feature Release (Adds a new feature)
        |_ Milestone Release (Adds a major feature from /PhantomServer/milestones)
        
```
#### [Version 0.0.0]
 - Made a basic project structure and updated readme.
