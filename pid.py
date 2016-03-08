import time
from limits import mapToLimits

class PidController():
    
    def __init__(self, name, kp = 0, ki = 0, kd = 0, setpoint = 0, i_limit = 0, starting_i = 0, time_period = 0.01): # default 100Hz
        self.name = name
        self.kp = kp
        self.ki = ki    
        self.kd = kd
        self.setpoint = setpoint
        self.time_period = time_period
        self.last_time = 0
        self.last_error = 0
        self.i = starting_i
        self.i_limit = i_limit
        self.output = 0
        self.first_run = True
    
    def setCoefficients(self, new_kp, new_ki, new_kd):
        self.kp = new_kp
        self.ki = new_ki
        self.kd = new_kd
    
    def setTimeperiod(self, time_period):
        self.time_period = time_period
        
    def setSetpoint(self, new_setpoint):
        self.setpoint = new_setpoint
        
    def restart(self):
        self.first_run = True
        
    def run(self, value):
        current_time = time.time()
        dt = current_time - self.last_time
        output_calculated = False
        
        if (self.first_run == False):
            
            if (dt >= self.time_period): 
                error = value - self.setpoint
                
                p = self.kp * error
                self.i += self.ki * error * dt
                d = (error - self.last_error) / dt
                
                if (self.i_limit != 0):
                    self.i = mapToLimits(self.i, self.i_limit, - self.i_limit)
                
                self.output = p + self.i + d
                output_calculated = True
        
                self.last_time = current_time
                self.last_error = error
                
        else: #self.first_run == True
            error = value - self.setpoint
            
            p = self.kp * error
            self.i += 0
            d = 0
            
            if (self.i_limit != 0):
                self.i = mapToLimits(self.i, self.i_limit, - self.i_limit)
            
            self.output = p + self.i + d
            output_calculated = True
        
            self.last_time = current_time
            self.last_error = error
            self.first_run = False
        
        return output_calculated
        
        
