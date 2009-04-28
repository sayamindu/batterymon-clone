import logging
class logger_init:
    def __init__(self):
	self.mylogger = logging.getLogger("batterymon")
        self.mylogger.setLevel(logging.INFO)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        self.mylogger.addHandler(ch)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        ch.setFormatter(formatter)
    
    
    def debug(self,message):
        self.mylogger.debug(message)
    
    def error(self,message):
        self.mylogger.error(message)
    
    def critical(self,message):
        self.mylogger.critical(message)
    
    def set_level(self,level):        
        if level == "debug":
            self.mylogger.setLevel(logging.DEBUG)
#}}}
