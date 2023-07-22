import numpy as np
from sympy import *


class Convolution_Signal():
    def __init__(self,input1,input2,limit_left,limit_right,sampling_time):
        self.sampling_time = sampling_time
        self.limit_left = limit_left
        self.limit_right = limit_right

        if input1 == 'Triangle' or input1 == 'triangle':
            self.input1 = ['t',0,1,'2-t',1,2]
        
        elif input1 == 'Square' or input1 == 'square':
            self.input1 = ['1',0,1]

        elif input1 == 'Ramp' or input1 == 'ramp':
            self.input1 = ['t',0,1]

        elif input1 == 'Exp' or input1 == 'exp':
            self.input1 = ['3*exp(-3*t)',0,self.limit_right]
        
        elif input1 == 'Damped Sine' or input1 == 'damped sine':
            self.input1 = ['exp(-0.3*t)*sin(t)',0,self.limit_right]

        elif input1 == 'Unit Step' or input1 == 'unit step':
            self.input1 = ['1',0,self.limit_right]

        elif input1 == 'Pulse Train' or input1 == 'pulse train':
            self.input1 = ['1',0,1,'-1',1,2]
            
        else:
            self.input1 = input1

        if input2 == 'Triangle' or input2 == 'triangle':
            self.input2 = ['t',0,1,'2-t',1,2]
        
        elif input2 == 'Square' or input2 == 'square':
            self.input2 = ['1',0,1]
        
        elif input2 == 'Ramp' or input2 == 'ramp':
            self.input2 = ['t',0,1]

        elif input2 == 'Exp' or input2 == 'exp':
            self.input2 = ['3*exp(-3*t)',0,self.limit_right]

        elif input2 == 'Unit Step' or input2 == 'unit step':
            self.input2 = ['1',0,self.limit_right]

        elif input2 == 'Impulse' or input2 == 'impulse':
            self.input2 = 'impulse'
        
        elif input2 == 'Pulse Train' or input2 == 'pulse train':
            self.input2 = ['1',0,1,'-1',1,2]

        else:
            self.input2 = input2

        if self.input2 !='impulse':
        
            if len(self.input1) == 3:
                self.fvector = self.function_vector1(self.input1)
            else:
                self.fvector = self.function_vector2(self.input1)
            
            if len(self.input2) == 3:
                self.gvector = self.function_vector1(self.input2)

            else:
                self.gvector = self.function_vector2(self.input2)
            
            self.tvector = self.time_vector()
            self.convolution_signal = self.convolution_vector()
        
        else:
            if len(self.input1) == 3:
                self.fvector = self.function_vector1(self.input1)
            else:
                self.fvector = self.function_vector2(self.input1)

            self.tvector = self.time_vector()
            self.gvector = self.impulse()
            self.convolution_signal = self.fvector
        
    def impulse(self):
        vector = []
        tau = self.limit_left
        while tau<self.limit_right:
            if tau == 0:
                result = 1
            else:
                result = 0
            vector.append(result)
            tau = tau+self.sampling_time
        return vector
        
    def function_vector1(self,input):
        vector = []
        expr = input[0]
        left = float(input[1])
        right = float(input[2])
        t = symbols("t")
        function = sympify(expr)
        tau = self.limit_left
        while tau<self.limit_right:
            if left<=tau<=right:
                result = function.subs(t,tau)
            else:
                result = 0
            vector.append(result)
            tau = tau+self.sampling_time
        return vector
    
    def function_vector2(self,input):
        vector = []
        expr1 = input[0]
        left1 = float(input[1])
        right1 = float(input[2])
        expr2 = input[3]
        left2 = float(input[4])
        right2 = float(input[5])
        t = symbols("t")
        function1 = sympify(expr1)
        function2 = sympify(expr2)
        tau = self.limit_left
        while tau<self.limit_right:
            if left1<=tau<=right1:
                result = function1.subs(t,tau)
            elif left2<=tau<=right2:
                result = function2.subs(t,tau)
            else:
                result = 0
            vector.append(result)
            tau = tau+self.sampling_time
        return vector
    
    def time_vector(self):
        vector = []
        t = self.limit_left
        while t<self.limit_right:
            vector.append(t)
            t = t+self.sampling_time
        return vector
    
    def convolution_vector(self):
        convolution_signal = self.sampling_time*np.convolve(self.fvector,self.gvector,'same')
        return convolution_signal
    
   
