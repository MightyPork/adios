Adios!
======

Adios is a simple exit dialog, similar to `cb-exit` from CrunchBang.

It supports various desktop environment and is highly customizable (see help for details).

The tool contains presets for ArchBang, CrunchBang and universal ones for KDE and XFCE.

Installing to OpenBox
---------------------

To install it to OpenBox, put the file into `/usr/bin` (or anywhere else, but you'll have to write the full path), and modify OpenBox's `rc.xml` file as so:

Example with `adios --ab` (preset for ArchBang)

~~~xml
<keybind key="XF86PowerOff">
  <action name="Execute">
    <command>
      adios --ab
    </command>
  </action>
</keybind>
~~~

After adding that, restart OpenBox with `openbox --restart` for the change to take effect.
