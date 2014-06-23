#!/usr/bin/python3

"""Simple GTK exit prompt (logout, suspend, power off...).
Based on `cb-exit` script from CrunchBang.

If you're on either XFCE4, KDE, ArchBang or CrunchBang, you can use the
corresponding presets option.

Otherwise, you can customize the actions using manually.

It's also possible to combine both methods, and customize one of the presets
(ie. use cusom hibernate command).

To see what commands are bound to what buttons, use the --debug option.

(C) Ondřej Hruška, 2014

Usage:
    adios (--xfce | --kde | --ab | --cb | --upower | --systemd) [(--lock <cmd> | --nolock | --lock-cb | --lock-i3)] [(--logout <cmd> | --openbox)] [--shutdown <cmd>] [--reboot <cmd>] [--suspend <cmd>] [--hibernate <cmd>] [--debug]
    adios -h
    adios -v

Options:
    --xfce         Presets for XFCE4 workspace
    --kde          Presets for KDE workspace
    --ab           Presets for ArchBang (OpenBox, systemctl)
    --cb           Presets for CrunchBang (OpenBox, upower, cb-lock)

    --upower       Use UPower and KonsoleKit for power management
    --systemd      Use systemctl for power management

    --lock <cmd>   Custom screen lock command (for hibernate and suspend)
    --nolock       Use no lock in suspend and hibernate
    --lock-cb      Use crunchbang screen lock (cb-lock)
    --lock-i3      Use i3 screen lock (i3lock)

    --openbox      Use openbox for logout

    --logout <cmd>     Custom log-out command
    --suspend <cmd>    Custom suspend command
    --hibernate <cmd>  Custom hibernate command
    --shutdown <cmd>   Custom hibernate command
    --reboot <cmd>     Custom reboot command

    --debug        Show debug info
    -h, --help     Show this screen.
    -v, --version  Show version.

"""

import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk
import os
import getpass
from docopt import docopt


def is_exe(fpath):
	""" Check if file is executable """
	return os.path.isfile(fpath) and os.access(fpath, os.X_OK)


def which(program):
	"""
	Find executable if exists, return None if not.
	"""

	fpath, fname = os.path.split(program)
	if fpath:
		if is_exe(program):
			return program
	else:
		for path in os.environ["PATH"].split(os.pathsep):
			path = path.strip('"')
			exe_file = os.path.join(path, program)
			if is_exe(exe_file):
				return exe_file

	return None


class exit_dialog:
	"""
	Exit dialog main class
	"""

	def disable_buttons(self):
		""" Gray out all buttons """
		self.cancel.set_sensitive(False)
		self.logout.set_sensitive(False)
		self.suspend.set_sensitive(False)
		self.reboot.set_sensitive(False)
		self.shutdown.set_sensitive(False)


	def cancel_action(self,btn):
		""" User clicked 'Cancel' """
		self.disable_buttons()
		Gtk.main_quit()


	def logout_action(self,btn):
		""" User clicked 'Log out' """
		self.disable_buttons()
		self.status.set_label("Logging out, please standby...")

		for c in self.cmd['logout']:
			os.system(c)


	def suspend_action(self,btn):
		""" User clicked 'Suspend' """
		self.disable_buttons()
		self.status.set_label("Suspending, please standby...")

		for c in self.cmd['suspend']:
			os.system(c)

		Gtk.main_quit()


	def hibernate_action(self,btn):
		""" User clicked 'Hibernate' """
		self.disable_buttons()
		self.status.set_label("Hibernating, please standby...")

		for c in self.cmd['suspend']:
			os.system(c)

		Gtk.main_quit()


	def reboot_action(self,btn):
		""" User clicked 'Reboot' """
		self.disable_buttons()
		self.status.set_label("Rebooting, please standby...")

		for c in self.cmd['reboot']:
			os.system(c)


	def shutdown_action(self,btn):
		""" User clicked 'Shutdown' """
		self.disable_buttons()
		self.status.set_label("Shutting down, please standby...")

		for c in self.cmd['shutdown']:
			os.system(c)


	def create_window(self):
		""" Make the GUI """
		self.window = Gtk.Window()
		title = "Log out " + getpass.getuser() + "? Choose an option:"
		self.window.set_title(title)
		self.window.set_border_width(5)
		self.window.set_size_request(324, 120)
		self.window.set_resizable(False)
		self.window.set_keep_above(True)
		self.window.stick
		self.window.set_position(1)
		self.window.connect("delete_event", Gtk.main_quit)
		windowicon = self.window.render_icon(Gtk.STOCK_QUIT, Gtk.IconSize.MENU)
		self.window.set_icon(windowicon)

		def make_button(box, label, action):
			""" Helper fn for making GTK buttons """

			btn = Gtk.Button(label)
			btn.set_border_width(4)
			btn.set_size_request(100, 50)
			btn.connect("clicked", action)
			box.pack_start(btn, True, True, 0)
			btn.show()
			return btn


		# Box for first row
		self.button_box = Gtk.HBox()
		self.button_box.show()

		# Cancel button
		self.cancel = make_button(self.button_box, "Cancel", self.cancel_action)

		# Logout button
		self.logout = make_button(self.button_box, "Log out", self.logout_action)
		self.logout.set_sensitive(len(self.cmd['logout']) > 0)

		# Suspend button
		self.suspend = make_button(self.button_box, "Suspend", self.suspend_action)
		self.suspend.set_sensitive(len(self.cmd['suspend']) > 0)

		# Box for second row
		self.button_box2 = Gtk.HBox()
		self.button_box2.show()

		# Hibernate button
		self.hibernate = make_button(self.button_box2, "Hibernate", self.hibernate_action)
		self.hibernate.set_sensitive(len(self.cmd['hibernate']) > 0)

		# Reboot button
		self.reboot = make_button(self.button_box2, "Reboot", self.reboot_action)
		self.reboot.set_sensitive(len(self.cmd['reboot']) > 0)

		# Shutdown button
		self.shutdown = make_button(self.button_box2, "Power off", self.shutdown_action)
		self.shutdown.set_sensitive(len(self.cmd['shutdown']) > 0)

		# Status label
		self.label_box = Gtk.HBox()
		self.label_box.show()
		self.status = Gtk.Label()
		self.status.show()
		self.label_box.pack_start(self.status, True, True, 0)


		# Main vertical layout
		self.vbox = Gtk.VBox()
		self.vbox.pack_start(self.button_box, True, True, 0)
		self.vbox.pack_start(self.button_box2, True, True, 0)
		self.vbox.pack_start(self.label_box, True, True, 0)
		self.vbox.show()


		# hide based on hardware support
		if os.system("pm-is-supported --hibernate") != 0:
			self.hibernate.set_sensitive(False)

		if os.system("pm-is-supported --suspend") != 0:
			self.suspend.set_sensitive(False)

		# close on Esc
		accelgroup = Gtk.AccelGroup()
		key, modifier = Gtk.accelerator_parse('Escape')
		accelgroup.connect(key, modifier, Gtk.AccelFlags.VISIBLE, Gtk.main_quit)
		self.window.add_accel_group(accelgroup)

		self.window.add(self.vbox)
		self.window.show()


	def __init__(self):

		args = docopt(__doc__, version="0.2")

		cmd = {
			'logout': [],
			'shutdown': [],
			'reboot': [],
			'hibernate': [],
			'suspend': []
		}

		# flags
		use_upower  = False
		use_sysctl  = False
		use_ksm     = False
		use_xfsm    = False
		use_openbox = False

		# alt commands to be used
		alt_lock = None
		alt_logout = None
		alt_shutdown = None
		alt_reboot = None
		alt_suspend = None
		alt_hibernate = None

		# flag that all is initialized properly
		ok = False

		if args['--kde']:
			use_ksm = True
			ok = True

		if args['--xfce']:
			use_xfsm = True
			ok = True

		if args['--ab']:
			use_sysctl = True
			use_openbox = True
			ok = True

		if args['--cb']:
			use_upower = True
			use_openbox = True

			alt_lock = "cb-lock"
			ok = True

		if args['--openbox']:
			use_openbox = True

		if args['--upower']:
			use_sysctl = False
			use_upower = True
			ok = True

		if args['--systemd']:
			use_sysctl = True
			use_upower = False
			ok = True

		if not ok:
			print("Warning: Missing options. Using ArchBang setup.")
			print("See help for more info.")

			use_sysctl = True
			use_openbox = True
			ok = True

		if args['--lock'] != None:
			alt_lock = args['--lock']

		if args['--logout'] != None:
			alt_logout = args['--logout']

		if args['--suspend'] != None:
			alt_suspend = args['--suspend']

		if args['--hibernate'] != None:
			alt_hibernate = args['--hibernate']

		if args['--reboot'] != None:
			alt_reboot = args['--reboot']

		if args['--shutdown'] != None:
			alt_shutdown = args['--shutdown']


		if args['--nolock']:
			alt_lock = None

		if args['--lock-cb']:
			alt_lock = 'cb-lock'

		if args['--lock-i3']:
			alt_lock = 'i3lock'

		# apply group flags

		if use_xfsm:
			cmd['logout']    = ["xfce4-session-logout --logout"]
			cmd['shutdown']  = ["xfce4-session-logout --halt"]
			cmd['reboot']    = ["xfce4-session-logout --reboot"]
			cmd['hibernate'] = ["xfce4-session-logout --hibernate"]
			cmd['suspend']   = ["xfce4-session-logout --suspend"]

		if use_ksm:
			cmd['logout']    = ["qdbus org.kde.ksmserver /KSMServer org.kde.KSMServerInterface.logout 0 1 3"]
			cmd['shutdown']  = ["qdbus org.kde.ksmserver /KSMServer org.kde.KSMServerInterface.logout 0 1 2"]
			cmd['reboot']    = ["qdbus org.kde.ksmserver /KSMServer org.kde.KSMServerInterface.logout 0 1 1"]
			cmd['hibernate'] = ["qdbus org.kde.Solid.PowerManagement /org/freedesktop/PowerManagement Hibernate"]
			cmd['suspend']   = ["qdbus org.kde.Solid.PowerManagement /org/freedesktop/PowerManagement Suspend"]

		if use_upower:
			cmd['shutdown']  = ["dbus-send --system --print-reply --dest=\"org.freedesktop.ConsoleKit\" /org/freedesktop/ConsoleKit/Manager org.freedesktop.ConsoleKit.Manager.Stop"]
			cmd['reboot']    = ["dbus-send --system --print-reply --dest=\"org.freedesktop.ConsoleKit\" /org/freedesktop/ConsoleKit/Manager org.freedesktop.ConsoleKit.Manager.Restart"]
			cmd['hibernate'] = ["dbus-send --system --print-reply --dest=\"org.freedesktop.UPower\" /org/freedesktop/UPower org.freedesktop.UPower.Hibernate"]
			cmd['suspend']   = ["dbus-send --system --print-reply --dest=\"org.freedesktop.UPower\" /org/freedesktop/UPower org.freedesktop.UPower.Suspend"]

		if use_sysctl:
			cmd['shutdown']  = ["systemctl poweroff"]
			cmd['reboot']    = ["systemctl reboot"]
			cmd['hibernate'] = ["systemctl hibernate"]
			cmd['suspend']   = ["systemctl suspend"]

		if use_openbox:
			alt_logout = "openbox --exit"


		# apply alt commands

		if alt_logout != None:
			cmd['logout']    = [alt_logout]

		if alt_shutdown != None:
			cmd['shutdown']    = [alt_shutdown]

		if alt_suspend != None:
			cmd['suspend']    = [alt_suspend]

		if alt_hibernate != None:
			cmd['hibernate']    = [alt_hibernate]

		if alt_reboot != None:
			cmd['reboot']    = [alt_reboot]

		# append lock if needed
		if alt_lock != None:
			cmd['hibernate'].insert(0, alt_lock)
			cmd['suspend'].insert(0, alt_lock)

		self.cmd = cmd

		# debug info
		self.debug = args['--debug']

		if self.debug:
			print('Commands: ')
			for a,c in cmd.items():
				print("=== " + str(a) + " ===")
				for cc in c:
					print(" * " + str(cc))
				print()

		self.create_window()


def main():
	Gtk.main()

if __name__ == "__main__":
	go = exit_dialog()
	main()
