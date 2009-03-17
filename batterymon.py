#!/usr/bin/env python
#
#       batterymon.py
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
import sys, os, string
from optparse import OptionParser
#import subprocess 
VERSION="0.5.6"

#basepath="/home/matthew/Projects/batman/"

basepath = os.path.abspath(os.path.dirname(__file__))
theme=""
batpath="/sys/class/power_supply/"
interval=0
BATnumber=""
#batpath="/home/matthew/Projects/systray/"
iconpath = "/usr/share/batterymon"    

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
        self.test.set_from_file("%s/icons/%s/battery_%s.png" % (iconpath,theme, name))
    
    def __init__(self):
        self.check_theme()
        self.test= gtk.StatusIcon()
        self.set_icon("full")
        self.test.set_blinking(False)
        self.test.connect("activate", self.activate)
        self.test.connect("popup_menu", self.popup)
        self.test.set_visible(True)
        gobject.timeout_add(interval, self.update)
        self.update()
        gtk.main()

    def status(self):
        FILE=open(batpath+BATnumber + "/status","r")
        print batpath+BATnumber+"/status"
        CMD=FILE.read()
        FILE.close
        print CMD
        return CMD

    def percent(self):
        
        FILE=open(batpath+BATnumber+"/charge_full","r")
        MAX=FILE.read()
        FILE.close
        FILE=open(batpath+BATnumber+"/charge_now","r")
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

    def check_theme(self):
        
        x = os.path.exists("/%s/icons/%s/" % (iconpath,theme)) # check if the battery exists
        if x:
            ## Theme directory found
            return ()
        else:
            print "Theme not found please check the name and try again!"
            sys.exit (0)
        return

class commandline:
    def passargs(self,arg):
        print arg
        parser = OptionParser(usage='usage: %prog [options] ', version=VERSION, description="Simple Battery Monitor")
        parser.add_option("-i", '--interval',action="store",help="set interval to check battery in miliseconds", dest="interval", default="30000")
        parser.add_option("-t",'--theme',action="store",help="set battery icon theme",dest="theme",default="default")
        parser.add_option("-b",'--battery',action="store", help="which battery to monitor e.g BAT0",dest="battery",default="default")
        #parser.add_option("-l",'--list',action="store_true",help="list avaliable batterys",dest="listbatts")
        (options, args) = parser.parse_args()
        if arg=="none":
            parser.print_help()
        return options

    def checkbatterys(self):
        command='ls ' + batpath +' | grep BAT'
        
        
        test = os.popen(command).readlines()     # search for batteries
        
        if len(test) >1:
            print "More than one battery was found please pass -b BAT[number]"
            print "using battery "+str(test[0]) +" as default"
            return str(test[0])
        else:                               
            print "One battery found"   
            return str(test[0])
    
    def check_battery_exists(self):
        bat = str.upper(cmdline.battery) # make sure the bat is upper
        x = os.path.exists(batpath+bat ) # check if the battery exists
        
        if x:
            BATnumber==bat
        else:
            print "Battery doesn't exist please double check your Battery number \n e.g ./batterymon.py -b BAT1"
            sys.exit(0)
    

if __name__ == "__main__":
    
    options=commandline() 
    cmdline = options.passargs("") ## pass command line options
    
    
    if cmdline.theme == "default":  ## set theme
        theme="default"
    else:
        theme=cmdline.theme        ### currently no error checking for themes
    
    interval=int(cmdline.interval) ## set interval
    
    if cmdline.battery == "default":
        tempBATnumber = options.checkbatterys()  ## set default battery number
        BATnumber=tempBATnumber.strip('\n')
    else:
        Batnumber = options.check_battery_exists() ## set battery number set on command line 
    
    
    tray=systray()
