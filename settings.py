import ConfigParser
import os


class config:
    def __init__(self):
	self.configure = ConfigParser.ConfigParser()
	self.filename= self.settings_exist ()
	self.configure.read(self.filename)
	
    def settings_exist(self):
	 if os.path.exists('~/.config/batterymon/batterymon.rc'):
	     return "~/.config/batterymon/batterymon.rc"
	 elif os.path.exists('/usr/share/batterymon/batterymon.rc'):
	     return "/usr/share/batterymon/batterymon.rc"
	 else:
	     return ('./batterymon.rc')
    
    def read_settings(self):
	self.configure.read (self.filename)
	return ("done")
    
    def read_settings_int(self):
	x = self.configure.get ("default",key)
        return int(x)    
	
	def write_settings_string(self,key,value):
		self.configure.set("tray",key,str(value) )
        	with open (self.filename, 'wb') as configfile:
	           self.configure.write(configfile)
		return
		
    def write_settings_int(self,key,value):	
	self.configure.set("tray",key,str(value) )
        with open (self.filename, 'wb') as configfile:
           self.configure.write(configfile)
        return    
	
