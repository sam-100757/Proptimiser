import math
g = 9.8
gas_const = 287
gamma = 1.4
e = 2.7182818
Re = 6356.766

class Environment:
    def __init__(self):
        self.alti = 0
        self.pressure = 0
        self.density = 0
        self.vis_kin = 0
        self.vis_dyn = 0
        self.temp = 0
        self.v_sound = 0

    def findP(self):
        p_0 = 101325.0

        p_11 = p_0 * ((216.65/288)**( g / (0.0065 * gas_const)))
        p_20 = p_11 * (e ** ((g * 9.1 * 1000 * (-1)) / (gas_const * 216.65)) )
        p_32 = p_20 * ((228.65/216.65)**(g / (-0.000991736 * gas_const)))
        p_47 = p_32 * ((270.65/228.65)**(g / (-0.002781457 * gas_const)))
        p_52 = p_47 * (e ** ((g * 5.1 * 1000 * (-1)) / (gas_const * 270.65)) )
        p_61 = p_52 * ((252.65/270.65)**(g / (0.001956522 * gas_const)))
        p_80 = p_61 * ((180.65/252.65)**(g / (0.003913043 * gas_const)))

        return p_0,p_11,p_20,p_32,p_47,p_52,p_61,p_80
    
    def findTP(self):
        p_0,p_11,p_20,p_32,p_47,p_52,p_61,p_80 = self.findP()

        self.alti = self.takeHeight()

        if(self.alti<0):
            print("Please enter an altitude above Sea level")
            self.findTP()
        elif(self.alti<=11):
            self.temp = ((165 - (71.5*self.alti)) / 11) + 273.15
            self.pressure = p_0 * ((self.temp/288)**(g / (0.0065 * gas_const)))

        elif(self.alti>11 and self.alti<=20.1):
            self.temp = -56.5 + 273.15           
            self.pressure = p_11 * (e ** ((g * (self.alti - 11) * 1000 * (-1)) / (gas_const * 216.65)) )
        elif(self.alti>20.1 and self.alti<=32.2):
            self.temp = (((12*self.alti) - 924.85) / 12.1) + 273.15
            self.pressure = p_20 * ((self.temp/216.65)**(g / (-0.000991736 * gas_const)))
 
        elif(self.alti>32.2 and self.alti<=47.3):
            self.temp = (((42*self.alti) - 2024.35) / 15.1) + 273.15
            self.pressure = p_32 * ((self.temp/228.65)**(g / (-0.002781457 * gas_const)))
        elif(self.alti>47.3 and self.alti<=52.4):
            self.temp = -2.5 + 273.15
            self.pressure = p_47 * (e ** ((g * (self.alti - 47.3) * 1000 * (-1)) / (gas_const * 270.65)) )
        elif(self.alti>52.4 and self.alti<=61.6):
            self.temp = ((920.2 - (18*self.alti) ) / 9.2) + 273.15
            self.pressure = p_52 * ((self.temp/270.65)**(g / (0.001956522 * gas_const)))
        elif(self.alti>61.6 and self.alti<=80):
            self.temp = ((4058 - (72*self.alti) ) / 18.4) + 273.15
            self.pressure = p_61 * ((self.temp/252.65)**(g / (0.003913043 * gas_const)))
        elif(self.alti>80):
            print("Please enter an altitude less than 80 km.")
            self.findTP()
        
        print("Temperature is ", round(self.temp, 3), "K.")
        print("Pressure is ", round((self.pressure / 1000), 5), "kPa.")
        return self.temp,self.pressure


    def takeHeight(self):
        geo_alti=float(input("Please enter altitude in km: "))
        alti = (Re * geo_alti) / (Re + geo_alti)
        return alti
    
    def convertToC(self):
        t_c = self.temp - 273.15
        print("Temperature in Celsius is", round(t_c, 2), "°C.")

        return t_c
    
    def findDensity(self):
        t = self.temp
        p = self.pressure

        self.density = p / (gas_const * t)

        print("Density at the given altitude is ", round(self.density, 5), "kg/m³.")
        return self.density
    
    def findSound(self):
        t = self.temp

        self.v_sound = math.sqrt((t * gas_const * gamma))
        print("Speed of sound is ", round(self.v_sound,3), "m/s².")

        return self.v_sound
    
    def findVisc(self):
        t = self.temp
        self.vis_dyn = ((1.458 * (10**-6) * math.sqrt(t)) / (1+(110.4/t)))
        self.vis_kin = self.vis_dyn / self.density

        print(f"Dynamic viscosity is: {self.vis_dyn:.3e} Pa·s")
        print(f"Kinematic viscosity is: {self.vis_kin:.3e} m²/s")

        return self.vis_dyn, self.vis_kin


env = Environment()
env.findTP()
env.convertToC()
env.findDensity()
env.findSound()
env.findVisc()