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

#basepath="/sys/class/power_supply/"
basepath="/home/matthew/Projects/batman/"
batpath="/sys/class/power_supply/"
interval=30000
#batpath="/home/matthew/Projects/systray/"
class systray:
	def alert( self, widget, data=None):
		stat 		   = self.status()
		perc 		   = self.percent()
		perc1=int(perc)
		dialog = gtk.MessageDialog(
		parent         = None,
		flags          = gtk.DIALOG_DESTROY_WITH_PARENT,
		type           = gtk.MESSAGE_INFO,
		buttons        = gtk.BUTTONS_OK,
		message_format = "Battery Status "+stat +"\n" +"Current Charge " +str(perc1) +"%" +"\n"+"Battery level is low please plug in your mains adaptor")
		dialog.set_title('Batman')
		dialog.connect('response', self.show_hide)
		dialog.show()
		
	def __init__(self):
		self.test= gtk.StatusIcon()
		self.test.set_from_file(basepath+"icons/battery_full.png")
		self.test.set_blinking(False)
		self.test.connect("activate", self.activate)
		self.test.connect("popup_menu", self.popup)
		self.test.set_visible(True)
		gobject.timeout_add(interval,self.update)
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
		
		per=(float(NOW) / float(MAX) * 100)
		return (per)
	def activate( self, widget, data=None):
		stat 		   = self.status()
		perc 		   = self.percent()
		perc1=int(perc)
		dialog = gtk.MessageDialog(
		parent         = None,
		flags          = gtk.DIALOG_DESTROY_WITH_PARENT,
		type           = gtk.MESSAGE_INFO,
		buttons        = gtk.BUTTONS_OK,
		message_format = "Battery Status "+stat +"\n" +"Current Charge " +str(perc1) +"%")
		dialog.set_title('Batman')
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
		dialog.set_title('Batman')
		dialog.connect('response', self.destroyer)
		dialog.show()
	
	def update(self):
		CMD=self.status()
		per=self.percent()
		per1=int(per)
		self.test.set_tooltip("Battery status "+ CMD + "Current charge " + str(per1) + "%")

		if CMD.strip() =="Full":
			self.test.set_from_file(basepath+"icons/battery_full.png")
			gobject.timeout_add(interval,self.update)
			return()

		if CMD.strip()=="Charging":
			self.test.set_from_file(basepath+"icons/battery_power.png")
			gobject.timeout_add(interval,self.update)
			return()

		if CMD.strip()=="Discharging":
				if round(per) <= 100.0:
					self.test.set_from_file(basepath+"icons/battery_full.png")
					self.test.set_blinking(False)	

				if round(per) <= 87.0:
					self.test.set_from_file(basepath+"icons/battery_7.png")
					
				if round(per) <= 75.0:
					self.test.set_from_file(basepath+"icons/battery_6.png")
					
				if round(per) <= 62.0:
					self.test.set_from_file(basepath+"icons/battery_5.png")
					
				if round(per) <= 50.0:
					self.test.set_from_file(basepath+"icons/battery_4.png")
					
				if round(per) <= 37.0:
					self.test.set_from_file(basepath+"icons/battery_3.png")
					
				if round(per) <= 25.0:
					self.test.set_from_file(basepath+"icons/battery_2.png")
				
				if round(per) <= 12.0:
					self.test.set_from_file(basepath+"icons/battery_1.png")

				if round(per) <= 8.0:
					self.test.set_from_file(basepath+"icons/battery_empty!.png")

				if round(per) <= 5.0:
					self.test.set_from_file(basepath+"icons/battery_empty.png")
					self.test.set_blinking(True)
					self.alert(self)
				gobject.timeout_add(interval,self.update)
	
	
if __name__ == "__main__":
	tray=systray()


	
	
