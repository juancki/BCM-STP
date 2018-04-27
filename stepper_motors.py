#/etc/bin python

# Decription of motor specs.
#
# Used to store grbl the microstepping configuration,
#  maximum  velocity and acceleration.


class Nema17StepperMotor():
    def __init__(self,
            stepsperrevolution = 200,
            microsteps = 16,
            gear_box=100,# one to one hundret,
            lead_screw_pitch =1, # milimiters per revolution
            max_rmp = 120, # maximum rpm
            torque = 58, # in Newtons per centimer [Ncm]
            inertia = 57, # measured in grams times squared centimeter [g*cm2]
            max_amp = 2,
            phases = 2):
        # default from http://www.pbclinear.com/Download/DataSheet/Stepper-Motor-Support-Document.pdf
        self.stepsperrevolution = stepsperrevolution
        self.microsteps = microsteps
        self.gear_box = gear_box
        self.torque = torque
        self.inertia = inertia
        self.max_amp = max_amp
        self.phases = phases
        self.lead_screw_pitch= lead_screw_pitch 
        self.max_rmp = max_rmp


    def getconfig(self):
        config = {}
        config['step_mm'] = self.stepsperrevolution*self.microsteps/self.lead_screw_pitch 
        config['max_rate'] =self.microsteps*self.max_rmp*self.lead_screw_pitch
        config['accel'] = 1*self.microsteps #not real, made it up
        return config 



class Mitsumi55StepperMotor():
    def __init__(self,
            stepsperrevolution = 48,
            microsteps = 8,
            gear_box=100,# one to one hundret,
            lead_screw_pitch =2, # milimiters per revolution
            max_rmp = 100, # maximum rpm
            torque = 58, # in Newtons per centimer [Ncm]
            inertia = 57, # measured in grams times squared centimeter [g*cm2]
            max_amp = 2,
            phases = 2):
        # default from http://www.pbclinear.com/Download/DataSheet/Stepper-Motor-Support-Document.pdf
        self.stepsperrevolution = stepsperrevolution
        self.microsteps = microsteps
        self.gear_box = gear_box
        self.torque = torque
        self.inertia = inertia
        self.max_amp = max_amp
        self.phases = phases
        self.lead_screw_pitch= lead_screw_pitch 
        self.max_rmp = max_rmp


    def getconfig(self):
        config = {}
        config['step_mm'] = self.stepsperrevolution*self.microsteps/self.lead_screw_pitch 
        config['max_rate'] =self.max_rmp*self.lead_screw_pitch 
        #not real, made up
        config['accel'] =1 #not real, made it up
        return config 




