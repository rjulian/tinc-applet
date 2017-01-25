# tinc-applet
A minimalist gtk taskbar applet for [tinc-vpn](https://tinc-vpn.org/).

tinc-applet will:
* list all nodes connected to your network
* notify when nodes connect or disconnect
* allow retry of all connections


Only works with the tinc 1.1 branch.

## For Unity Ubuntu Users

Unfortunately, because of [Unity's permissions "bug"](https://bugs.launchpad.net/indicator-appmenu/+bug/592842), you cannot start the applet with the root permissions it needs to access the tinc executables. The fix for this is setting the pidfile in the tincd process with `--pidfile=/path/to/dir/tinc.pid` and recursively set the owner of that directory to be you (e.g. `sudo chown youruser:youruser /path/to/dir/`). Hopefully, we can fix this in the future.  
