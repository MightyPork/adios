exit-prompt
===========

Exit dialog for systemctl / openbox (intended for Arch)

The code is based on `cb-exit` from CrunchBang, and it's primarily a port of this feature to ArchBang.

To install it to OpenBox, put the file into `/usr/bin` (or anywhere else, but you'll have to write the full path), and modify OpenBox's `rc.xml` file as so:

~~~xml
<keybind key="XF86PowerOff">
  <action name="Execute">
    <command>
      <!-- put command or path to the script here -->
      edit-dialog
    </command>
  </action>
</keybind>
~~~

This entry should be there already, just search for `XF86PowerOff`.

After that, restart OpenBox with `openbox --restart` for the change to take effect.
