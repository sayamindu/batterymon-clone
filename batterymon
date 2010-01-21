#!/usr/bin/env python

import dbus
import dbus.glib

import pygtk
import gtk
from optparse import OptionParser
import os,sys

## code modules
#from preferences import prefs
from logger import logger_init
#from settings import config

#{{{ Desktop notifications init
try:
    import pynotify
    if not pynotify.init("Battery Monitor"):
        print("There was an error initializing the notification system. Notifications won't work.")
except:
    print("You do not seem to have python-notify installed. Notifications won't work.")
    pynotify = None
#}}}


#{{{ Program defaults
VERSION="1.1.2"
theme="default"
logger = logger_init()
#}}}



# {{{ DBUSObject
class DBusObject:
    def __init__(self):
        self.bus = dbus.SystemBus()
        hal_obj = self.bus.get_object('org.freedesktop.Hal', '/org/freedesktop/Hal/Manager')
        self.hal = dbus.Interface(hal_obj, 'org.freedesktop.Hal.Manager')
#}}}

# {{{ AcAdapter
class AcAdapter(DBusObject):
    def __init__(self):
        DBusObject.__init__(self)
        self.property_modified_handler = None

        udis = self.hal.FindDeviceByCapability('ac_adapter')

        if len(udis) == 0:
            raise Exception("No AC adapter found")

        # take the first adapter
        adapter_obj = self.bus.get_object('org.freedesktop.Hal', udis[0])
        self.__adapter = dbus.Interface(adapter_obj, 'org.freedesktop.Hal.Device')
        self.__adapter.connect_to_signal('PropertyModified', self.__on_property_modified)

    def update(self):
        present = self.__adapter.GetProperty('ac_adapter.present')
        logger.debug("Adapter is present: %s" % present)

        if self.property_modified_handler:
            self.property_modified_handler(present)
        else:
            logger.warn("No AC adapter property modified handler, ignoring status update")


    def __on_property_modified(self, num_changes, property):
        property_name, added, removed = property[0]

        if property_name != "ac_adapter.present":
            logger.debug("HAL AC adapter property modified")
            return

        logger.debug("HAL AC adapter present modified")

        self.update()
#}}}

# {{{ BatteryDetector
class BatteryDetector(DBusObject):
    def __init__(self):
        DBusObject.__init__(self)

    def get_all(self):
        udis = self.hal.FindDeviceByCapability('battery')

        logger.debug("Found %s battery(ies)" % str(len(udis)))
   
        batteries = []

        for udi in udis:
            battery_obj = self.bus.get_object('org.freedesktop.Hal', udi)
            battery = dbus.Interface(battery_obj, 'org.freedesktop.Hal.Device')

            batteries.append(Battery(battery))

        return batteries
#}}}

# {{{ Battery
class Battery:
    def __init__(self, battery):
        self.property_modified_handler = None
        self.__battery = battery
        self.__battery.connect_to_signal('PropertyModified', self.__on_property_modified)
        self.remaining_time = "unknown"  ## added this or the program crashes on a full battery
       
    def __on_property_modified(self, num_changes, property):
        property_name, added, removed = property[0]

        logger.debug("Battery property %s modified" % property_name)
       
        self.update()

    def update(self):
        present = self.__battery.GetProperty('battery.present')
        logger.debug("battery.present: %s" % str(present))

        #XXX: check if the battery is rechargable first
        is_charging = self.__battery.GetProperty('battery.rechargeable.is_charging')
        logger.debug("battery.is_charging: %s" % str(is_charging))
                   
        is_discharging = self.__battery.GetProperty('battery.rechargeable.is_discharging')
        logger.debug("battery.is_discharging: %s" % str(is_discharging))

        charge_level = self.__battery.GetProperty('battery.charge_level.percentage')
        logger.debug("battery.percentage: %s" % str(charge_level))

        try:
            remaining_time = self.__battery.GetProperty('battery.remaining_time')
            logger.debug("battery.remaining_time: %s" % str(remaining_time))

        except dbus.DBusException, e:
            logger.error(e)
            remaining_time = -1

        remaining_time = self.__str_time(remaining_time)

        if self.property_modified_handler:
            self.property_modified_handler(BatteryInfo(charge_level, remaining_time, is_charging, is_discharging, present))
        else:
            logger.warn("No property modified handler, ignoring battery status update")

    def __str_time(self, seconds):
        if seconds < 0:
            return 'Unknown'
       
        minutes = seconds / 60
       
        hours = minutes / 60
        minutes = minutes % 60                    
       
        logger.debug("Minutes: %s" % str(minutes))
        logger.debug("Hours: %s" % str(hours))


        return self.__format_time(hours, "Hour", "Hours") + " " + self.__format_time(minutes, "Minute", "Minutes")

    def __format_time(self, time, singular, plural):
        if time == 0:
            return ""
        elif time == 1:
            return "1 %s" % singular
        else:
            return "%s %s" % (time, plural)


#}}}

#{{{ Theme
class Theme:
    def __init__(self, theme):
        self.theme = theme
        self.iconpath = self.__resolve_iconpath()

        if not self.validate(theme):
            logger.error("Theme %s does not exists, falling back to default" % theme)
            self.theme = "default"

            if not self.validate("default"):
                logger.critical("Default theme does not exists, fatal")
                exit()

        logger.debug("Theme %s validated" % self.theme)
    	
    def __resolve_iconpath(self):
        if os.path.isdir('./icons/' + theme):
            logger.debug('Using local icons')
            return './'
        else:
            logger.debug('Using /usr/share')
            return  '/usr/share/batterymon'

    def get_icon(self, name):
        return "%s/icons/%s/battery_%s.png" % (self.iconpath, self.theme, name)

    def file_exists(self, f):
        try:
            open(f)
        except IOError:
            return False
        else:
            return True
   
    def validate(self, theme):
        all_icons = ["1", "2", "3", "4", "5", "empty", "full", 
        "charging_1","charging_2","charging_3","charging_4","charging_5",
        "charging_full","charging_empty"]

        for icon in all_icons:
            if not self.file_exists(self.get_icon(icon)):
                logger.debug("Could not find icon %s" % self.get_icon(icon))
                return False

        return True
#}}}

# {{{ PowerEventListener
class PowerEventListener:
    def ac_property_modified(self, present):
        pass

    def battery_property_modified(self, battery_info):
        pass
#}}}

# {{{ BatteryInfo
class BatteryInfo:
    def __init__(self, charge_level, remaining_time, is_charging, is_discharging, present):
        self.charge_level = charge_level
        self.remaining_time = remaining_time
        self.is_charging = is_charging
        self.is_discharging = is_discharging
        self.present = present
# }}}

# {{{ Systray
class Systray(PowerEventListener):
    def __init__(self, theme):
        self.theme = theme
        self.tray_object= gtk.StatusIcon()
        self.tray_object.set_visible(False)
        #self.set_icon("full")
        self.tray_object.set_blinking(False)
        self.tray_object.connect("popup_menu", self.rightclick_menu)
        
        self.show_trayicon(1) ## fixed to one for now
        
    
    def show_trayicon(self,value):
       setting = value
       ### only changing on startup
       
       if setting == 3 : ## only show if charing or discharging
            self.tray_object.set_visible(False)
            return
            
       if setting == 1: ### always show an icon
                self.tray_object.set_visible(True)
                return
       
       if setting == 2: ## only show when discharging
            self.tray_object.set_visible(True)    
              
            return
    
    def read_settings(self):
       settings=config()
       result = settings.read_settings_int("show_icon")
       
       return result
       
    def battery_property_modified(self, battery):
        
        if battery.is_charging:       
            self.tray_object.set_tooltip("On AC (Charging) \nBattery Level: %s%%" % battery.charge_level)
            logger.debug("Charging\n Battery Percentage %s" % battery.charge_level)

        elif battery.is_discharging:
            
            self.tray_object.set_tooltip("Battery Level: %s%% \nTime remaining %s" % (battery.charge_level, battery.remaining_time))
            logger.debug("Battery Percentage %s \nTime remainging: %s" % (battery.charge_level, battery.remaining_time))

        else:
            self.tray_object.set_tooltip("On AC \nBattery Level: %s%%" % battery.charge_level)
            logger.debug("On AC")
        
        if battery.is_charging == 0 and battery.is_discharging == 0 :
            
            self.set_icon("charging_full")
            return
        
                  
        if battery.charge_level > 96:
            if battery.is_charging ==0:
                self.set_icon("full")                
            else:
                self.set_icon("charging_full")
                self.tray_object.set_blinking(False)                                      

        elif battery.charge_level > 80:
            if battery.is_charging ==0:
                self.set_icon("5")
            else:
                self.set_icon("charging_5")

        elif battery.charge_level > 64:
            if battery.is_charging ==0:
                self.set_icon("4")
            else:
                self.set_icon("charging_4")

        elif battery.charge_level > 48:
            if battery.is_charging ==0:
                self.set_icon("3")
            else:    
                self.set_icon("charging_3")

        elif battery.charge_level > 32:
            if battery.is_charging ==0:
                self.set_icon("2")
            else:
                self.set_icon("charging_2")

        elif battery.charge_level >16:
            if battery.is_charging ==0:                
                self.set_icon("1")
            else:
                self.set_icon("charging_1")
        else:
            if battery.is_charging ==0:
                self.set_icon("empty")
                self.tray_object.set_blinking(True)
            else:
                self.tray_object.set_blinking(False)
		self.set_icon("charging_empty")
        return
        
        
            
    def rightclick_menu(self, button, widget, event):
        menu = gtk.Menu()
        about_menu = gtk.ImageMenuItem(gtk.STOCK_ABOUT)
        about_menu.connect('activate', self.about)
        exit_menu = gtk.ImageMenuItem(gtk.STOCK_CLOSE)
        exit_menu.connect('activate', self.close)        
        pref_menu = gtk.ImageMenuItem(gtk.STOCK_PREFERENCES
)
        pref_menu.connect('activate',self.preferences)
        menu.append(about_menu)
        #menu.append(pref_menu)
        menu.append(exit_menu)
        menu.show_all()           
        menu.popup(None, None, None, 2, event)
    
        
    def preferences(self,button):
        show_prefs = prefs()
        
    
    def close(self,button):
        sys.exit(0)
    
        
        
    def about(self, button):
        about_dg = gtk.AboutDialog()
        about_dg.set_name("Battery Monitor")
        about_dg.set_version(VERSION)
        about_dg.set_authors(["Matthew Horsell", "Tomas Kramar"])
        about_dg.connect("response", lambda d, r: d.destroy())
        about_dg.show()
       
    def set_icon(self,name):
        self.tray_object.set_from_file(self.theme.get_icon(name))                     
        self.Icon_name = name
        logger.debug("Icon updated")
        logger.debug("Icon Name: %s" % name)
   
#}}}

#{{{ Notification
class NotificationHelper:
    def notify(self, title, message, icon):
        if pynotify:
            n = pynotify.Notification(title, message)                                                            
            iconf = theme.get_icon(icon)            
            print "TEST " + systray.Icon_name            
            logger.debug("DEBUG Notification icon " +iconf)
            icon = gtk.gdk.pixbuf_new_from_file_at_size(iconf, 46, 46)                
            n.set_icon_from_pixbuf(icon)                                            
            n.show()
            logger.debug("Notification shown")
#}}}

#{{{ commandline
class commandline:
    def passargs(self,arg):
       
        parser = OptionParser(usage='usage: %prog [options] ', version=VERSION, description="Simple Battery Monitor")  
        parser.add_option("-t","--theme",action="store",help="set icon theme",dest="theme",default="default")                
        parser.add_option("-n", "--notify-at", action="store", help="notify me when battery level is lower than the provided value", dest="notification_level", default="10")
        parser.add_option("-c", "--critical", action="store", help="set critical level", dest="critical_level", default="5")
        parser.add_option("-e", "--on-critical", action="store", help="run this command on critical power level", dest="critical_command", default=None)
        parser.add_option("-l", "--list-themes", action="store_true", help="list all avalable themes", dest="list_themes", default=False)
        parser.add_option("-d", "--debug"      , action="store_true",help="run in debug mode" , dest="debug", default=False)
        (options, args) = parser.parse_args()
       
        if arg=="none":
            parser.print_help()
        return options
    
#}}}

# {{{ PowerManager
class PowerManager:
    def __init__(self):
        self.listeners = []
        self.adapter = AcAdapter()
        self.batteries = BatteryDetector().get_all()

        self.adapter.property_modified_handler = self.__ac_property_modified_handler

        for battery in self.batteries:
            battery.property_modified_handler = self.__battery_property_modified_handler

    def __ac_property_modified_handler(self, present):
        for listener in self.listeners:
            listener.ac_property_modified(present)

    def __battery_property_modified_handler(self, battery):
        for listener in self.listeners:
            listener.battery_property_modified(battery)

    def update(self):
        for battery in self.batteries:
            battery.update()

# }}}

# {{{ Notificator
class Notificator(PowerEventListener):
    def __init__(self, low_level=-1, critical_level=-1):
        self.n = NotificationHelper()
        self.low_level = low_level
        self.notified = False
        self.critical_level = critical_level
        self.critically_notified = False
        logger.debug("self.low_level " + str(self.low_level))           
    
    def ac_property_modified(self, present):
        if present:            
            self.n.notify("On AC", "You are currently running on AC","charging_empty")
        else:            
            self.n.notify("On Battery", "AC adapter unplugged, running on battery","full")

    def battery_property_modified(self, battery):
        if battery.charge_level <= self.low_level and not self.notified:
            self.n.notify("Low Battery", "You have approximatelly <b>%s</b> remaining" % battery.remaining_time,"empty")
            self.notified = True

        if battery.charge_level <= self.critical_level and not self.critically_notified:
            self.n.notify("Critical Battery", "You have approximatelly <b>%s</b> remaining" % battery.remaining_time,"empty")
            self.critically_notified = True


        if battery.is_charging and battery.charge_level > self.critical_level:
            self.critically_notified = False

        if battery.is_charging and battery.charge_level > self.low_level:
            self.notify = False

#}}}

#{{{ CommandRunner
class CommandRunner(PowerEventListener):
    def __init__(self, power_level, command):
        self.power_level = power_level
        self.command = command

    def battery_property_modified(self, battery):
                
        if int(battery.charge_level) <= int(self.power_level) and self.command:
            logger.debug("Running command '%s'" % self.command)
            os.system(self.command)
#}}}

#{{{ List all Themes
class list_themes:
    def list_all_themes(self):
	print "Themes:"
        temp = os.listdir("/usr/share/batterymon/icons")
	print str(temp)
	return

	
        
#}}}
 
if __name__ == "__main__":
    
    options = commandline()
    
    cmdline = options.passargs("") ## pass command line options
    
    ## not sure on this yet? might be handy if the theme base grows
    
    if cmdline.list_themes:
            test = list_themes()
            test.list_all_themes()
            
            sys.exit(1)
    if cmdline.debug:        
        logger.set_level("debug")    
        
    theme = Theme(cmdline.theme)
    
    systray = Systray(theme)
    notificator = Notificator(int(cmdline.notification_level), int(cmdline.critical_level))    
    executor = CommandRunner(int(cmdline.critical_level), cmdline.critical_command)
    
    pm = PowerManager()
    pm.listeners.append(notificator)
    pm.listeners.append(systray)
    pm.listeners.append(executor)
    
    pm.update()

    gtk.main()

