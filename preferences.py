#!/usr/bin/env python
import gtk
from logger import logger_init
from settings import config
logger = logger_init()
settings = config()
class prefs:
	
	def destroy(self,widget):        
		self.pref_win.hide()

	def Radio_Call_Back(self,widget,data=None):		
		
		test = (("OFF","ON")[widget.get_active()])
		Toggled = data +" " + test
		if Toggled == "Always_show ON":
			logger.debug("DEBUG Always show an icon")
			settings.write_settings_int("show_icon","1")	
			return
		elif Toggled == "show_charging_discharging ON":
			logger.debug("DEBUG only show when battery is charging or discharing")
			settings.write_settings_int("show_icon","3")
			return
		elif Toggled == "Show_discharging_only ON":
			logger.debug("DEBUG Show an icon when discharging")
			settings.write_settings_int("show_icon","2")
			return
            
	def okay_button_clicked(self,widget,data=None):
		self.pref_win.hide()
		print "OKAY"
	
	def __init__(self):
		
		self.pref_win = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.pref_win.set_border_width(0)
		self.pref_win.set_title("Preferences")
		self.pref_win.connect("destroy",self.destroy)
		## Windows  Stuff
		box1 = gtk.VBox(False,0)  ## Virtical Layout Box
		self.pref_win.add(box1)
		box1.show()
        
		box2 = gtk.VBox(False,10)
		box2.set_border_width(10)
		box1.pack_start(box2,True,True,0)
		box2.show()
        
		## Setup Radio Buttons
		radio_button = gtk.RadioButton(group=None, label="Only display an icon when battery is charging or discharging")
		radio_button.connect("toggled",self.Radio_Call_Back,"show_charging_discharging")
		box2.pack_start(radio_button,True,True,0)
		radio_button.show()
	        ##Button 2
        	radio_button = gtk.RadioButton(radio_button, label="Only show an icon when battery is discharging")
	        radio_button.connect("toggled",self.Radio_Call_Back,"Show_discharging_only")
        	box2.pack_start(radio_button,True,True,0)
	        radio_button.show()
	        ##Button 3
	        radio_button = gtk.RadioButton(radio_button, label="Always display an icon")
	        radio_button.connect("toggled",self.Radio_Call_Back,"Always_show")
	        box2.pack_start(radio_button,True,True,0)
	        radio_button.show()
	        ##Separtor
	        separator = gtk.HSeparator()
	        box1.pack_start(separator,False,True,0)
	        separator.show()
        
	        box2 = gtk.VBox(False,10)
	        box2.set_border_width(10)
	        box1.pack_start(box2,False,True,0)
	        box2.show()
	        #Okay Button
        	okay_button = gtk.Button("Okay")
	        okay_button.connect_object("clicked",self.okay_button_clicked,self.__init__,None)
        	box2.pack_start(okay_button,True,True,0)
	        okay_button.show()                    
                
        	self.pref_win.show()

	
	
		
    
	

