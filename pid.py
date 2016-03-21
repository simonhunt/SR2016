import time
from limits import mapToLimits

class PidController():
    
    def __init__(self, name, kp = 0, ki = 0, kd = 0, max_output = 0, min_output = 0, setpoint = 0, i_limit = 0, starting_i = 0, time_period = 0.01): # default 100Hz
        self.name = name
        self.kp = kp
        self.ki = ki    
        self.kd = kd
        self.max_output = max_output
        self.min_output = min_output    
        self.setpoint = setpoint
        self.time_period = time_period
        self.last_time = 0
        self.last_error = 0
        self.p = 0
        self.starting_i = starting_i
        self.i = self.starting_i
        self.i_limit = i_limit
        self.d = 0
        self.output = 0
        self.first_run = True
        self.stopped = False
    
    def setCoefficients(self, new_kp, new_ki, new_kd):
        self.kp = new_kp
        self.ki = new_ki
        self.kd = new_kd
        
    def setOutputLimits(self, new_max_output, new_min_output):
        self.max_output = new_max_output
        self.min_output = new_min_output
    
    def setTimeperiod(self, time_period):
        self.time_period = time_period
        
    def setSetpoint(self, new_setpoint):
        self.setpoint = new_setpoint
        
    def restart(self):
        self.first_run = True
        self.stopped = False
    
    def stop(self):
        self.stopped = True
        
    def run(self, value):
        
        if (self.stopped == True):
            self.output = 0
            output_calculated = True
            
        else: #self.stopped == False
            current_time = time.time()
            dt = current_time - self.last_time
            output_calculated = False
            
            if (self.first_run == False):
                
                if (dt >= self.time_period): 
                    error = self.setpoint - value
                    
                    self.p = self.kp * error
                    self.i += self.ki * error * dt
                    self.d = (error - self.last_error) / dt
                    
                    if (self.i_limit != 0):
                        self.i = mapToLimits(self.i, self.i_limit, - self.i_limit)
                        
                    if ((self.max_output != 0) or (self.min_output != 0)):
                        self.output = mapToLimits((self.p + self.i + self.d), self.max_output, self.min_output)
                    
                    else:
                        self.output = self.p + self.i + self.d
                    
                    output_calculated = True
            
                    self.last_time = current_time
                    self.last_error = error
                    
            else: #self.first_run == True
                error = value - self.setpoint
                
                self.p = self.kp * error
                self.i = self.starting_i
                self.d = 0
                
                if ((self.max_output != 0) or (self.min_output != 0)):
                    self.output = mapToLimits((self.p + self.i + self.d), self.max_output, self.min_output)
                    
                else:
                    self.output = self.p + self.i + self.d
                        
                output_calculated = True
            
                self.last_time = current_time
                self.last_error = error
                self.first_run = False
            
        return output_calculated
    
    def debug(self):
        print self.name + ": stopped = " + str(self.stopped) + ", (p, i, d) = (" + str(self.p) + ", " + str(self.i) + ", " + str(self.d) + "), output = " + str(self.output)
        
        
        