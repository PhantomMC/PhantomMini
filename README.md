# Phantom Standalone Edition
> **THIS PROJECT IS ON HOLD**

> !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!<br>
> THIS PROJECT IS A **WORK IN PROGRESS**.<br>DO __**NOT**__ USE IT IN PRODUCTION CIRCUMSTANCES<br><br>
>                              No stable releases are available at this time.<br>
> !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!<br>

### The self-hosted, single instance, version of Phantom [PhantomHost](https://phantomhost.cc)
[![Phantom Banner](https://i.imgur.com/sXXxwez.jpg)](https://phantomhost.cc)
### [Support Discord](https://discord.gg/ASgcxVvhU9) | [Documentation](https://github.com/PhantomMC/PhantomMini/wiki)

# Description
## What is Phantom?
Phantom is a MineCraft protocol responder that forgoes all of the game's [mechanical](https://minecraft.fandom.com/wiki/Gameplay) functionalities.<br>
This is therefore, by its very definition, the lightest possible MineCraft ["server"](https://wiki.vg/Server_List) implementation.
### What does Phantom do?
Functionally, Phantom is a MineCraft broadcaster that delivers configurable messages to all users who interact with your server's IP.<br>
### How does Phantom work?
Whenever a user interacts with your server's IP, their client will request to establish a [TCP or UDP](https://en.wikipedia.org/wiki/Communication_protocol) connection.<br>
Phantom is equipped to respond to such requests across all versions of every edition of MineCraft (including Bedrock, Java, Pi, & China)

For users viewing your server in their client's server list, Phantom will respond with a customisable MOTD, hover message, upper message, and/or icon.
If users attempt to join your server, Phantom will accept the connection and immediately kick them with a customisable message.
### When is Phantom Useful?
Phantom has five primary use cases:
Temporary Events | Upcoming Servers
:---: | :---:
Ephemeral servers that are infrequently online. <br> Perfect for periodically repeated (or one-time) events! | Servers that aren't quite ready yet. <br> Helpful for building hype around your next project!

Defunct Servers | Parked Domains
:---: | :---:
 Past servers that are no longer operating. <br> Perfect for informing and reconnecting playerbases! | Held domains that are not currently in use. <br> Suitable for holding advertisments and contact information.
 
 Downtime Management
 :---:
 Servers facing downtime on account of hardware migration or maintenance.<br> A DNS-level solution to keep your users informed amidst service outages.
 
 ## How does one use Phantom?
 Phantom can be used through one of two setups: [PhantomMini](https://github.com/PhantomMC/PhantomMini/releases) and [PhantomHost](https://phantomhost.cc).
 ### What is [PhantomMini](https://github.com/PhantomMC/PhantomMini/releases)?
 PhantomMini is our self-hosted, single instance, edition of Phantom.<br>
 If you have a basic understanding of unix, you should find that it is relatively easy to install.
 
 Although optimised for [SBMs](https://en.wikipedia.org/wiki/Single-board_microcontroller), PhantomMini should be able to run in most environments.<br> 
 ([minimum specs](https://github.com/wemos/docs/blob/master/docs/en/w600/w600_pico.rst#w600-pico) - [suggested specs](https://www.friendlyarm.com/index.php?route=product/product&product_id=132))
 
 ### What is [PhantomHost](https://phantomhost.cc)
 When deployed at scale, Phantom instances so ultralightweight that they can be hosted at next to no cost.<br>
 To that end, PhantomMC operates a free hosting service at [PhantomHost.cc](https://phantomhost.cc).
 
 Through the PhantomHost service, you can set up five free server instances that:
 - Display a customisable MOTD, icon, hover message, and/or upper message to players when viewed.
 - Display a customisable kick message whenever a user tries to join.
 - Provide you with a basic metrics report on your server's view/join rates and activity.
 - Provides you with a free domain that you can point your DNS to, for example, YourServerName.PhantomHost.cc.
  
 All costs are supported by a single unobtrusive advertisment banner on your (admin-side) control panel.
 
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