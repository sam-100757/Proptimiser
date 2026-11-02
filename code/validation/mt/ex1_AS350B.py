import math
print("Please use meters and kilograms wherever unspecified.")

class Rotor:
    def __init__(self):
        #self.c = None
        self.Rad = None
        self.Area = None
        self.w = None
        self.Fom = None
        self.c_T = None
        self.c_P = None
        self.sect_c_d0 = None
        self.rho = None
        self.v_i = None
        self.v_h = None
        self.P_i = None
        self.P_h = None
        self.lamb_h = None
        self.lamb = None
        self.lamb_i = None
        self.v_c = None
        self.Thrust = None
        self.pwrLoad = None
        self.diskLoad = None 
        self.omega = None
        self.dia = None
        self.rpm = None
        self.v_tip = None
        self.Power = None
        self.condition = None
        self.P_act = None

    def applyArea(self):
        if (
            self.Area is None
            and self.Rad is not None
        ):
            self.Area = math.pi * (self.Rad**2)

        elif (
            self.Rad is None 
            and self.Area is not None
        ):
            self.Rad = math.sqrt((self.Area / math.pi)) 

    def applyDia(self):
        if (
            self.dia is None
            and self.Rad is not None
        ):
            self.dia = 2 * self.Rad

        elif (
            self.Rad is None 
            and self.dia is not None
        ):
            self.Rad = self.dia / 2

    def applyRPM(self):
        if (
            self.rpm is None
            and self.omega is not None
        ):
           self.rpm = (self.omega * 60) / (2 * math.pi)

        elif (
            self.omega is None
            and self.rpm is not None
        ):
            self.omega = 2 * math.pi * self.rpm / 60

    def applyVtip(self):
        if (
            self.omega is None
            and self.v_tip is not None
            and self.Rad is not None
        ):
            self.omega = self.v_tip / self.Rad

        elif (
            self.v_tip is None
            and self.Rad is not None
            and self.omega is not None
        ):
            self.v_tip = self.omega * self.Rad

        elif (
            self.Rad is None
            and self.v_tip is not None
            and self.omega is not None
        ):
            self.Rad = self.v_tip / self.omega


    def applyCT(self):
        if (
            self.c_T is None
            and self.Thrust is not None
            and self.rho is not None
            and self.Area is not None
            and self.v_tip is not None
        ):
            self.c_T = self.Thrust / (self.rho * self.Area * (self.v_tip**2))

        elif (
            self.Thrust is None
            and self.c_T is not None
            and self.rho is not None
            and self.Area is not None
            and self.v_tip is not None
        ):
            self.Thrust = self.c_T * self.rho * self.Area * (self.v_tip**2)

        elif (
            self.rho is None
            and self.Thrust is not None
            and self.c_T is not None
            and self.Area is not None
            and self.v_tip is not None
        ):
            self.rho = self.Thrust / ( self.c_T * self.Area * (self.v_tip**2) )

        elif (
            self.Area is None
            and self.Thrust is not None
            and self.c_T is not None
            and self.rho is not None
            and self.v_tip is not None
        ):
            self.Area = self.Thrust / ( self.c_T * self.rho * (self.v_tip**2) )

        elif (
            self.v_tip is None
            and self.Thrust is not None
            and self.c_T is not None
            and self.Area is not None
            and self.rho is not None
        ):
            self.v_tip = math.sqrt(self.Thrust / ( self.c_T * self.Area * self.rho ))

    def applyCP(self):
            if (
                self.c_P is None
                and self.Power is not None
                and self.rho is not None
                and self.Area is not None
                and self.v_tip is not None
            ):
                self.c_P = self.Power / (self.rho * self.Area * (self.v_tip**3))
    
            elif (
                self.Power is None
                and self.c_P is not None
                and self.rho is not None
                and self.Area is not None
                and self.v_tip is not None
            ):
                self.Power = self.c_P * self.rho * self.Area * (self.v_tip**3)
    
            elif (
                self.rho is None
                and self.Power is not None
                and self.c_P is not None
                and self.Area is not None
                and self.v_tip is not None
            ):
                self.rho = self.Power / ( self.c_P * self.Area * (self.v_tip**3) )
    
            elif (
                self.Area is None
                and self.Power is not None
                and self.c_P is not None
                and self.rho is not None
                and self.v_tip is not None
            ):
                self.Area = self.Power / ( self.c_P * self.rho * (self.v_tip**3) )
    
            elif (
                self.v_tip is None
                and self.Power is not None
                and self.c_P is not None
                and self.Area is not None
                and self.rho is not None
            ):
                self.v_tip = (self.Power / ( self.c_P * self.Area * self.rho ))**(1/3)

    def applyPwrLoad(self):
        if (
            self.pwrLoad is None 
            and self.P_act is not None
            and self.Thrust is not None
        ):
            self.pwrLoad = self.Thrust / ( self.P_act )

        elif ( 
            self.Thrust is None
            and self.P_act is not None
            and self.pwrLoad is not None
        ):
            self.Thrust = ( self.pwrLoad * self.P_act ) 

        elif (
            self.P_act is None
            and self.Thrust is not None
            and self.pwrLoad is not None
        ):
            self.P_act = (self.Thrust ) / self.pwrLoad

    def ifClimb_vi(self):
        if (
            self.v_i is None
            and self.v_c is not None
            and self.v_h is not None
        ):
            self.v_i = (-self.v_c / 2) + math.sqrt( ((self.v_c / 2)**2) + ((self.v_h)**2))

        elif (
            self.v_c is None 
            and self.v_h is not None
            and self.v_i is not None #supposing we've got it from power/powerloading
            and self.v_i!=0
        ):
            self.v_c = ( (self.v_h**2) / self.v_i ) - self.v_i


    def ifDescent_vi(self):
            if (
                self.v_i is None
                and self.v_c is not None
                and self.v_h is not None
            ):
                if ( ( (self.v_c / 2)**2) >= (self.v_h**2) ):
                    self.v_i = (-self.v_c / 2) - math.sqrt( ((self.v_c / 2)**2) - ((self.v_h)**2))
                else:
                    if (self.x == 0):
                        print("A higher descent rate is required to apply Momentum Theory. At this descent rate, the propeller is likely to be in Vortex Ring state, which cannot be solved by Momentum Theory.")
                        self.x = 1
    
            elif (
                self.v_c is None 
                and self.v_h is not None
                and self.v_i is not None 
                and self.v_i!=0
            ):
                self.v_c = ( -(self.v_h**2) / self.v_i ) - self.v_i
            

                        
    def applyDLCondition(self):
        if (
            self.diskLoad is None
            and self.Thrust is not None
            and self.Area is not None
        ):
            self.diskLoad = self.Thrust / self.Area

        elif (
            self.Thrust is None
            and self.diskLoad is not None
            and self.Area is not None
        ):
            self.Thrust = self.diskLoad * self.Area

        elif (
            self.Area is None
            and self.diskLoad is not None
            and self.Thrust is not None
        ):
            self.Area = self.Thrust / self.diskLoad

    def applyWake(self):
        if(
            self.w is None
            and self.v_i is not None
        ):
            self.w = 2*self.v_i

        elif (
            self.v_i is None
            and self.w is not None
        ):
            self.v_i = self.w / 2


    def applyFOM(self):
        if (
            self.P_act is None
            and self.P_i is not None
            and self.Fom is not None
        ):
            self.P_act = self.P_i / self.Fom

        elif (
            self.P_i is None
            and self.P_act is not None
            and self.Fom is not None
        ):
            self.P_i = (self.P_act * self.Fom)

        elif (
            self.Fom is None
            and self.P_act is not None
            and self.P_i is not None
        ):
            self.Fom = self.P_i / self.P_act

        
    def applyP_i(self):
        if (
            self.P_i is None
            and self.Thrust is not None
            and self.v_i is not None
        ):
            self.P_i = self.Thrust * self.v_i

        elif (
            self.Thrust is None
            and self.v_i is not None
            and self.P_i is not None
        ):
            self.Thrust = self.P_i / (self.v_i)

        elif (
            self.v_i is None
            and self.Thrust is not None
            and self.P_i is not None
        ):
            self.v_i = self.P_i / (self.Thrust)

    def applylamb_i(self):
        if (
            self.lamb_i is None
            and self.v_tip is not None
            and self.v_i is not None
        ):
            self.lamb_i = self.v_i / self.v_tip

        elif (
            self.v_tip is None
            and self.v_i is not None
            and self.lamb_i is not None
        ):
            self.v_tip = self.v_i / self.lamb_i

        elif (
            self.v_i is None
            and self.v_tip is not None
            and self.lamb_i is not None
        ):
            self.v_i = self.lamb_i * self.v_tip

    def applyFlightStateDependent_vi(self):
        if (self.condition=="hover"):
            self.v_c = 0
            self.v_i = self.v_h
            self.P_i = self.P_h
            self.lamb_i = self.lamb_h
                    
        elif (self.condition=="climb"):
            self.ifClimb_vi()
            self.applyP_i()
            self.applylamb_i()
                    
        elif (self.condition=="descent"):
            self.ifDescent_vi()
            self.applyP_i()
            self.applylamb_i()

    def applyIndVelHover(self):
        if (self.v_h is None
            and self.Thrust is not None
            and self.Area is not None
            and self.rho is not None
        ):
            self.v_h = math.sqrt((self.Thrust / (2*self.rho*self.Area)))

        elif (self.Thrust is None
            and self.v_h is not None
            and self.Area is not None
            and self.rho is not None
        ):
            self.Thrust = ((self.v_h**2) * 2 * self.rho * self.Area)

        elif (self.Area is None
              and self.Thrust is not None
              and self.v_h is not None
              and self.rho is not None
        ):
            self.Area = self.Thrust / ((self.v_h**2) * 2 * self.rho)

        if ( 
            self.Thrust is not None
            and self.v_h is not None
            and self.rho is not None
        ):
            self.P_h = self.Thrust * self.v_h




    def updateGeom(self):

        iteration = 0
        self.x = 0

        self.condition=input("Please enter flight state: Climb/Hover/Descent ").strip().lower()

        changed = True

        while changed and iteration<150:

            iteration+=1

            changed = False

            oldState = self.__dict__.copy()

            self.applyDia()
            self.applyArea()
            self.applyDLCondition()
            self.applyVtip()
            self.applyWake()
            self.applyRPM()
            self.applyCP()
            self.applyCT()
            self.applyFlightStateDependent_vi()
            self.applyIndVelHover()
            self.applyFOM()
            self.applyPwrLoad()

            if iteration == 150:
                print("The solver could not converge. Try changing the values.")

            changed = oldState != self.__dict__

        for key, value, in self.__dict__.items():
            if value != 0 and value is not None:
                print(f"{key:15} : {value}")



rotor = Rotor()
rotor.Rad = 5.345
rotor.Thrust = (9.80665*1950)     #=mg
rotor.rho = 0.4772                #calculated for 8.85km according to ISA
rotor.v_sound = 304.462           #calculated for 8.85km according to ISA
rotor.v_tip = 213
rotor.Fom = 0.7

#Ideal power required is given by P_i; for actual Power calculation we require FOM.


    #please enter what your input is, here:
    #INPUTBEGIN



    #INPUTEND

rotor.updateGeom()