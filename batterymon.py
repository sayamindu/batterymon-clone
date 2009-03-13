#!/usr/bin/env python
#
#       batman.py
#       
#       Copyright 2008 Matthew Horsell <matthew.horsell@googlemail.com>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

import gtk
import gobject
import sys, os
VERSION="0.5.0"

#basepath="/home/matthew/Projects/batman/"

basepath = os.path.abspath(os.path.dirname(__file__))

batpath="/sys/class/power_supply/"
interval=30000
#batpath="/home/matthew/Projects/systray/"
class systray:

    def alert( self, widget, data=None):
        stat            = self.status()
        perc            = self.percent()
        dialog = gtk.MessageDialog(
        parent         = None,
        flags          = gtk.DIALOG_DESTROY_WITH_PARENT,
        type           = gtk.MESSAGE_INFO,
        buttons        = gtk.BUTTONS_OK,
        message_format = "Battery Status %s\nCurrent Charge %d\
          %%\nBattery level is low please plug in your mains adaptor"   \
          % (stat, perc)
        )
        dialog.set_title('Batterymon')
        dialog.connect('response', self.show_hide)
        dialog.show()
    
    def set_icon(self, name):
        print "%s/icons/battery_%s.png" % (basepath, name)
        self.test.set_from_file("%s/icons/battery_%s.png" % (basepath, name))
    
    def __init__(self):
        self.test= gtk.StatusIcon()
        self.set_icon("full")
        self.test.set_blinking(False)
        self.test.connect("activate", self.activate)
        self.test.connect("popup_menu", self.popup)
        self.test.set_visible(True)
        gobject.timeout_add(interval, self.update)
        gtk.main()

    def status(self):
        FILE=open(batpath+"BAT0/status","r")
        CMD=FILE.read()
        FILE.close
        return CMD

    def percent(self):
        
        FILE=open(batpath+"BAT0/charge_full","r")
        MAX=FILE.read()
        FILE.close
        FILE=open(batpath+"BAT0/charge_now","r")
        NOW=FILE.read()
        FILE.close
        
        # only the int value is ever used
        per = int(round(float(NOW) / float(MAX) * 100))
        return (per)

    def activate( self, widget, data=None):
        stat            = self.status()
        perc            = self.percent()
        perc1=perc
        dialog = gtk.MessageDialog(
        parent         = None,
        flags          = gtk.DIALOG_DESTROY_WITH_PARENT,
        type           = gtk.MESSAGE_INFO,
        buttons        = gtk.BUTTONS_OK,
        message_format = "Battery Status %s\nCurrent Charge %d%%" % (stat, perc))
        dialog.set_title('Batterymon')
        dialog.connect('response', self.show_hide)
        dialog.show()
    
    def  show_hide(self, widget,response_id, data= None):
        if response_id == gtk.RESPONSE_YES:
            widget.hide()
        else:
            widget.hide()


    # destroyer callback
    def  destroyer(self, widget,response_id, data= None):
        if response_id == gtk.RESPONSE_OK:
            gtk.main_quit()
        else:
            widget.hide()
            
    def popup(self, button, widget, data=None):
        dialog = gtk.MessageDialog(
        parent         = None,
        flags          = gtk.DIALOG_DESTROY_WITH_PARENT,
        type           = gtk.MESSAGE_INFO,
        buttons        = gtk.BUTTONS_OK_CANCEL,
        message_format = "Do you want to close me?")
        dialog.set_title('Batterymon')
        dialog.connect('response', self.destroyer)
        dialog.show()
    
    def update(self):
        cmd = self.status().strip()
        per = int(round(self.percent()))
        self.test.set_tooltip("Battery status: %s | Current charge: %d%%" % (cmd, per))
        
        if cmd == "Full":
            self.set_icon("full")
            self.set_icon("power")
        elif cmd == "Discharging":
            if per > 87:
                self.set_icon("full")
                self.test.set_blinking(False)
            elif per > 75:
                self.set_icon("7")
            elif round(per) > 62:
                self.set_icon("6")
            elif per > 50:
                self.set_icon("5")
            elif per > 37:
                self.set_icon("4")
            elif per > 25:
                self.set_icon("3")
            elif per > 12:
                self.set_icon("2")
            elif per > 8:
                self.set_icon("1")
            elif per > 5:
                self.set_icon("empty!")
            else:
                self.set_icon("empty")
                self.test.set_blinking(True)
                self.alert(self)
        else:
            pass
            # should this cause an error?
    
    
if __name__ == "__main__":
    
    tray=systray()
