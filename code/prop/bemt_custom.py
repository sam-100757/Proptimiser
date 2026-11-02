
import math
import numpy as np
import pandas as pd
import sympy as sp
g = 9.81

print("Please use meters and kilograms wherever unspecified. \nSmall angle approximation is inherent in the current programme (phi<10 degrees). \n Please neglect the sign for Washout and enter the positive value. We have implicitly assumed that the blade is washed-out and not washed-in.\n Uniform mass distribution has been assumed throughout the blade\n")

class Rotor:
    def __init__(self):
        self.chord = None
        self.cutoutRatio = None #B=
        self.N_b = None
        self.Rad = None
        self.Area = None
        self.Fom = None
        self.c_T = None
        self.c_P = None
        self.c_Q = None
        self.sect_c_d0 = None
        self.a = None #a=slope of airfoil lift curve
        self.rho = None
        self.v_i = None
        self.Thrust = None
        self.Lift = None #add t/w ratio
        #self.Lift_eff = None
        self.pwrLoad = None
        self.diskLoad = None 
        self.omega = None
        self.dia = None
        self.rpm = None
        self.taperRatio = None
        self.ch_root = None
        self.ch_tip = None
        self.v_tip = None
        self.Power = None
        self.Torque = None
        self.vdp = None #vdp=vertical drag penalty
        self.condition = None
        self.twistType = None
        self.taperType = None
        self.chordType = None
        #here, effective area is only considered wrt taper. effects of root cutout and tip loss shall be added later on.
        self.solidity = None
        self.n = None
        self.designMode = None
        self.centrePitch = None
        self.tipPitch = None
        self.Washout = None
        self.c_l_avg = None
        self.alpha_avg = None
        self.k = None #airfoil dependent induced drag coefficient
        self.thrustToWeight = None
        self.mtow = None
        self.a0 = None #Coning angle
        self.I_b = None # blade MOI
        self.moi = None #rotor MOI
        self.M_w = None # moment due to weight
        self.LockNo = None
        self.tipLoss = None

    def applyConingIdeal(self):
        if (
            self.LockNo is None
            and self.rho is not None
            and self.a is not None
            and self.chord is not None
            and self.Rad is not None
            and self.I_b is not None
        ):
            self.LockNo = (self.rho * self.a * self.chord * (self.Rad**4)) / self.I_b

        if(
            self.a0 is None 
            and self.LockNo is not None
            and self.c_T is not None
            and self.solidity is not None
            and self.M_w is not None
        ):
            self.a0 = ((2 * self.LockNo * self.c_T) / (3 * self.a)) - (self.M_w / (self.I_b * (self.omega**2)))

    def applyWeightArm(self):
        if (
            self.M_w is None
            and self.Rad is not None
            and self.I_b is not None
        ):
            self.M_w = (3 * g * self.I_b) / (2 * self.Rad)

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

    def avgCalc(self):
        if (
            self.c_l_avg is None
            and self.c_T is not None
            and self.solidity is not None
        ):
            self.c_l_avg = (6*self.c_T) / self.solidity

    def avgAlpha(self):
        self.alpha_avg = (57.3 * 6 * self.c_T) / (self.solidity * self.a)

    def applyFOM(self):
        if (
            self.Fom is None
            and self.solidity is not None
            and self.c_T is not None
            and self.c_Q is not None
        ):
            self.Fom = (math.sqrt(self.solidity/2))*(((self.c_T/self.solidity)**1.5)/(self.c_Q/self.solidity))

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

    def applySolidity(self, N=100):
        if (self.chordType is 'constant'):
            if (
                self.solidity is None
                and self.N_b is not None
                and self.chord is not None
                and self.Rad is not None
            ):
                self.solidity = (self.N_b * self.chord) / (self.Rad * math.pi)

            elif (
                self.N_b is None
                and self.solidity is not None
                and self.chord is not None
                and self.Rad is not None
            ):
                self.N_b = (self.solidity * math.pi * self.Rad) / self.chord

            elif (
                self.Rad is None
                and self.solidity is not None
                and self.chord is not None
                and self.N_b is not None
            ):
                self.Rad = (self.N_b * self.chord) / (self.solidity * math.pi)

        else:

            for i in range(N):
                x = (i + 0.5) / N 

                tempTaper = self.applyTaper(x)

                dchord = 3*(tempTaper*x*1/N)

                self.chord += dchord

                if (
                    self.solidity is None
                    and self.N_b is not None
                    and self.chord is not None
                    and self.Rad is not None
                ):
                    self.solidity = (self.N_b * self.chord) / (self.Rad * math.pi)


    def applyVariedPhi(self, x): #x=r/R
        return self.v_i / (self.omega * x * self.Rad)

    def applyWhichTaper(self): #x=r/R
        if (self.taperType == 'linear'):
            self.applyPowerChord()
        elif (self.taperType == 'power'):
            self.n=float(input("Please enter index of the Power law for taper variation: "))
            self.applyPowerChord()
        elif (self.taperType == 'constant'):
            ifChordKnown=input("Do you have a value for constant chord? Yes/No : ").strip().lower()
            if (ifChordKnown == 'yes'):
                self.chord = float(input("Please enter the constant chord value: "))
                self.ch_root = self.chord
                self.ch_tip = self.chord
                self.taperRatio = 1
            elif (ifChordKnown == 'no'):
                if (
                    self.solidity is not None
                    and self.Rad is not None
                    and self.N_b is not None
                ):
                    self.chord = (self.solidity * self.Rad * math.pi) / self.N_b

            self.applyPowerChord()

        #elif (self.taperType == 'custom'):


    def applyTaper(self, x):
        if (self.taperType == 'linear'):
            return self.ch_root * (1+((self.taperRatio-1)*x))
        elif (self.taperType == 'power'):
            return self.ch_root * (1+((self.taperRatio-1)*(x**self.n)))
        elif (self.taperType =='constant'):
            return self.ch_root
        #elif (self.taperType =='custom'):


    def applyPowerChord(self, N=100, maxIter = 100):

        for name, value in {
            "density": self.rho,
            "Number of blades": self.N_b,
            "Angular Velocity": self.omega,
            "Slope of Lift Curve": self.a,
            "Cutout Ratio": self.cutoutRatio
        }.items():
            if value is None:
                print (name, ": Value required.")
                
        else:
            self.applySolidity()

            for p in range(maxIter):
                x0 = self.cutoutRatio
                TipLoss = 1
                dx = TipLoss- x0 / N
                dC_T_total = 0
                dT_total = 0

                for i in range(N):

                    x = x0 + (i + 0.5) / N

                    if (self.twistType=='linear'):
                        twist_temp = self.applyTwistLinear(x)

                    elif (self.twistType == 'ideal'):
                        twist_temp = self.applyTwistIdeal(x)

                    theta_t = twist_temp
                    phi_t = self.applyVariedPhi(x)
                    chord = self.applyTaper(x)
                    dT = (( 0.5 * self.rho * self.N_b * (self.omega**2) * ((self.Rad**3) * self.a * (theta_t - phi_t) * (x**2) * chord )) * dx)

                    dT_total += dT

                    dC_T = dT / (self.rho * math.pi * (self.Rad**2) * (self.v_tip**2))

                    dC_T_total += dC_T

                TipLoss_new = 1 - (math.sqrt(2*self.dC_T_total) / self.N_b)
                TipLoss = TipLoss_new

                if (abs(TipLoss_new - TipLoss)<1e-4):

                    self.tipLoss = TipLoss_new
                    break

            self.Thrust = dT_total
            self.c_T = dC_T_total                
            return self.Thrust, self.c_T
                    

    def applyPwrTor(self):
        if (
            self.Power is None
            and self.omega is not None
            and self.Torque is not None
        ):
            self.Power = self.omega * self.Torque

        elif (
            self.omega is None
            and self.Power is not None
            and self.Torque is not None
        ):
            self.omega = self.Power / self.Torque

        elif (
            self.Torque is None
            and self.omega is not None
            and self.Power is not None
        ):
            self.Torque = self.Power / self.omega

    ####### do we keep this?
    def applyc_P(self):
        if (
            self.c_P is None
            and self.Power is not None
            and self.rho is not None
            and self.Area is not None
            and self.v_tip is not None
        ):
            self.c_P = self.Power / ( self.rho * self.Area * (self.v_tip**3))

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
            self.rho = self.Power / ( self.c_P * self.Area * (self.v_tip**3))

        elif (
            self.Area is None
            and self.Power is not None
            and self.c_P is not None
            and self.Area is not None
            and self.v_tip is not None
        ):
            self.Area = self.Power / ( self.c_P * self.rho * (self.v_tip**3))

        elif (
            self.v_tip is None
            and self.Power is not None
            and self.c_P is not None
            and self.Area is not None
            and self.rho is not None
        ):    
            self.v_tip = math.cbrt(self.Power / ( self.c_P * self.Area * self.rho))

    
    def applyc_QIdeal(self):
            if (
                self.c_Q is None
                and self.c_T is not None
                and self.sect_c_d0 is not None
            ):
                self.c_Q = self.c_T * math.sqrt(self.c_T/2) + ((self.sect_c_d0*self.solidity) / 8)

    def applyc_QGeneral(self, N=100):
        
        dQ_induced = 0
        dQ_profile = 0
        dT = 0
        dQ_total = 0

        for name, value in {
            "density": self.rho,
            "Number of blades": self.N_b,
            "Angular Velocity": self.omega,
            "Slope of Lift Curve": self.a,
            "Radius": self.Rad
        }.items():
            if value is None:
                print (name, ": Value required.")
                
            else:

                for i in range(N):

                    x = (i + 0.5) / N

                    if (self.twistType=='linear'):
                        twist_temp = self.applyTwistLinear(x)

                    elif (self.twistType == 'ideal'):
                        twist_temp = self.applyTwistIdeal(x)

                    theta_t = twist_temp
                    phi_t = self.applyVariedPhi(x)

                    chord = self.applyTaper(x)
                    cd_x = self.applyCdLocal(x)

                    print("DEBUG:")
                    print("rho =", self.rho)
                    print("N_b =", self.N_b)
                    print("omega =", self.omega)
                    print("Rad =", self.Rad)
                    print("a =", self.a)
                    print("theta_t =", theta_t)
                    print("phi_t =", phi_t)
                    print("chord =", chord)
                    dT = (0.5 * self.rho * self.N_b * (self.omega**2) * (self.Rad**3) * self.a * (theta_t - phi_t) * (x**2) * chord) * (1/N)

                    dQ_induced = self.Rad * x * phi_t * dT
                    dQ_profile += (0.5 * self.rho * self.N_b * (self.omega**2) * (self.Rad**4) * chord * cd_x * (x**3)) / N
                    dQ_total +=dQ_induced + dQ_profile

        self.Torque = dQ_total

        self.c_Q = self.Torque / (self.rho * self.Area * self.Rad * (self.v_tip**2))

    def applyCdLocal(self, x):
        for name, value in {
            "Airfoil profile drag at zero lift" : self.sect_c_d0,
            "slope of C_l vs AOA" : self.a,
            "Drag polar coefficient" : self.k
        }.items():
            if value is None:
                print("ERROR: ", name, "NOT FOUND.")
            else:
                if (self.twistType=='linear'):
                    if self.applyTwistLinear(x) is not None:
                        twist_temp = self.applyTwistLinear(x)
                    else: twist_temp is None

                elif (self.twistType == 'ideal'):
                    if self.applyTwistIdeal(x) is not None:
                        twist_temp = self.applyTwistIdeal(x)
                    else: twist_temp is None

                theta_t = twist_temp
                phi_t = self.applyVariedPhi(x)
                if (
                    self.k is not None
                    and self.sect_c_d0 is not None
                    and self.a is not None
                ):
                    return self.sect_c_d0 + (self.k*((self.a*(theta_t-phi_t))**2))
                else: print("ERROR")

    def applyVDP(self):
        if (
            self.Lift_eff is None
            and self.Lift is not None
            and self.vdp is not None
        ):
            self.Lift_eff = self.Lift * (1-(self.vdp / 100))
            self.Lift = self.Lift_eff
        

    def gainData(self):


        print("PLEASE SELECT MODE:\n\n" \
        "Enter 1 for COMPUTE FOR GIVEN CONFIGURATION\n" \
        "(Press enter to leave a value blank.)")
        #after computation for given configuration is completed, design for different optimisations will be added as well.

        self.N_b=int(input("Please enter number of blades: "))
        if self.N_b=="":
            self.N_b = None
        self.Rad = float(input("Please enter Radius: "))
        if self.Rad=="":
            self.Rad = None
        self.cutoutRatio = float(input("Please enter cutout ratio: "))
        if self.cutoutRatio=="":
            self.cutoutRatio = None
        self.mtow = float(input("Please enter MTOW: "))
        if self.mtow=="":
            self.mtow = None
        self.v_tip = float(input("Please enter Tip velocity: "))
        if self.v_tip=="":
            self.v_tip = None
        self.Washout = float(input("Please enter Washout: "))
        if self.Washout=="":
            self.Washout = None 
        self.a = float(input("Please enter slope of airfoil lift curve: "))
        if self.a=="":
            self.a = None
        self.k = float(input("Please enter aifoil induced drag coefficient: "))
        if self.k=="":
            self.k = None
        self.sect_c_d0 = float(input("Please enter airfoil coefficient of induced drag: "))
        if self.sect_c_d0=="":
            self.sect_c_d0 = None
        self.ch_root = float(input("Please enter chord at root: "))
        if self.ch_root=="":
            self.ch_root = None
        self.ch_tip = float(input("Please enter chord at tip: "))
        if self.ch_tip=="":
            self.ch_tip = None
        self.taperRatio = float(input("Please enter taper ratio: "))
        if self.taperRatio=="":
            self.taperRatio = None
        self.rho = float(input("Please enter density: "))
        if self.rho=="":
            self.rho = None
        self.moi = float(input("Please enter Rotor Moment of inertia: "))
        if self.moi=="":
            self.moi = None

        
        self.designMode=int(input("Enter Selection: "))
        

        self.condition=input("Please enter flight state: Climb/Hover/Descent ").strip().lower()
        self.twistType=input("Please enter type of twist: Linear/Ideal ").strip().lower()
        self.chordType=input("Please enter the chord type: Constant/Variable").strip().lower()

        if (self.twistType=='linear'):
            self.calcForLinear()

        elif (self.twistType=='ideal'):
            self.calcForIdeal()

        else:
            print("ERROR: Twist type not supported.")

    def applyTwistIdeal(self, x):
        if (self.tipPitch is None):
            self.tipPitch=float(input("Please enter tip pitch: "))

        if (self.Rad is None):
            self.Rad=float(input("Please enter rotor radius: "))

        return self.tipPitch / x

    def applyTwistLinear(self, x):
        if (self.centrePitch is None):
            self.centrePitch=float(input("Please enter the pitch at the centre of rotation: "))

        if (self.Rad is None):
            self.Rad=float(input("Please enter rotor radius: "))

        if (self.Washout is None):
            self.Washout=float(input("Please enter the magnitude of difference between the pitch at Centre of rotation and tip of the rotor: "))

        return (self.centrePitch - (x*self.Washout))
    


    def calcForIdeal(self):

        if self.designMode==1:
            self.IdealMode1()

        elif self.designMode==2:
            self.IdealMode2()

    def IdealMode1(self):
        iteration = 0
        self.x = 0

        changed = True

        while changed and iteration<50:

            iteration+=1

            changed = False

            oldState = self.__dict__.copy()

            self.applyDia()
            self.applyArea()
            self.applyVtip()
            self.applyRPM()
            self.applyc_P()
            self.applySolidity()

            if iteration == 50:
                print("The solver could not converge. Try changing the values.")

            changed = oldState != self.__dict__


        self.applyWhichTaper()

        self.thrustToWeight = self.Thrust/self.mtow

        if self.condition=='hover':
            self.Lift=self.Thrust
        elif self.condition=='climb':
            pass
        elif self.condition=='descent':
            pass

        self.vdpCondition=input("Would you like to apply Vertical Drag Penalty (%)? : Yes/No").strip().lower()
        if (self.vdpCondition == 'no'):
            self.Lift_eff = self.Lift
        
        elif (self.vdpCondition =='yes'):
            self.vdp=float(input("Please enter Penalty for Vertical Drag (in %): ")) #add method for computing this
            self.applyVDP()

        if self.chordType=='constant':
                self.applyc_QIdeal()
        else:
                self.applyc_QGeneral()

        self.applyPwrTor()

        self.applyFOM()

        self.applyWeightArm()

        self.applyConingIdeal()

        if (self.twistType=='ideal'):
            linToIdeal=int(input("Do you wish to convert ideal distribution into linear?\n*Produced linear distribution preserves C_T as is given by ideal twist*\n Enter 1 for yes; 2 for no: "))
            if (linToIdeal==1):
                #if ideal twist is decided, tip pitch is already given and held constant
                if self.Washout is not None:
                    self.centrePitch = (1.5*self.tipPitch) + ((3*self.Washout)/4)
                    self.calcForLinear()
                elif self.centrePitch is not None:
                    self.tipPitch = (self.centrePitch - ((3*self.Washout)/4)) / 1.5
                    self.calcForLinear()
                elif (self.centrePitch is None and self.Washout is None):
                    print("Please enter either Centre Pitch or Washout to run.")

                print("Pitch distribution for equivalent linear pitch:\n")

                x = np.linspace(0,1,11)
                pitch = self.centrePitch + (x * self.Washout)

                table = pd.DataFrame({
                    "r/R":x,
                    "Pitch": pitch
                })

                print(table.to_string(index=False))

                #self.applyFOM()

        for key, value, in self.__dict__.items():
            if value != 0 and value is not None:
                print(f"{key:15} : {value}")


    def IdealMode2(self):

        self.Lift=float(input("Please enter targeted Lift: "))
        self.vdpCondition=input("Would you like to apply Vertical Drag Penalty (%)? : Yes/No").strip().lower()

        if (self.vdpCondition == 'no'):
            self.Lift_eff = self.Lift

        elif (self.vdpCondition =='yes'):
            self.vdp=float(input("Please enter Penalty for Vertical Drag (in %): "))
            self.applyVDP()

        changed = True

        while changed and iteration<150:

            iteration+=1

            changed = False

            oldState = self.__dict__.copy()

            self.applyDia()
            self.applyArea()
            self.applyVtip()
            self.applyRPM()
            self.applyc_P()
            if self.chordType=='constant':
                self.applyc_QIdeal()
            else:
                self.applyc_QGeneral()

            self.applyPwrTor()

            if iteration == 150:
                print("The solver could not converge. Try changing the values.")

            changed = oldState != self.__dict__

        self.applyWhichTaper()

        self.applyWeightArm()

        self.applyConingIdeal()

        if (self.twistType=='ideal'):
            linToIdeal=int(input("Do you wish to convert ideal distribution into linear?\n*Produced linear distribution preserves C_T as is given by ideal twist*\n Enter 1 for yes; 2 for no: "))
            if (linToIdeal==1):
                #if ideal twist is decided, tip pitch is already given and held constant
                if self.Washout is not None:
                    self.centrePitch = (1.5*self.tipPitch) + ((3*self.Washout)/4)
                    self.calcForLinear()
                elif self.centrePitch is not None:
                    self.tipPitch = (self.centrePitch - ((3*self.Washout)/4)) / 1.5
                    self.calcForLinear()
                elif (self.centrePitch is None and self.Washout is None):
                    print("Please enter either Centre Pitch or Washout to run.")
                #other var

        #for imperial units (hp), apply:
        #if (self.Power is not None):
        #    self.Power = self.Power / 550

        for key, value, in self.__dict__.items():
            if value != 0 and value is not None:
                print(f"{key:15} : {value}")

    def calcForLinear(self):
        if self.designMode==1:
            self.LinearMode1()

        elif self.designMode==2:
            self.LinearMode2()


    def LinearMode1(self):
        iteration = 0
        self.x = 0

        changed = True

        while changed and iteration<50:

            iteration+=1

            changed = False

            oldState = self.__dict__.copy()

            self.applyDia()
            self.applyArea()
            self.applyVtip()
            self.applyRPM()
            self.applyc_P()
            self.applySolidity()

            if iteration == 50:
                print("The solver could not converge. Try changing the values.")

            changed = oldState != self.__dict__

        self.applyWhichTaper()

        if (
            self.Thrust is not None
            and self.mtow is not None
        ):
            self.thrustToWeight = self.Thrust/self.mtow

        if self.condition=='hover':
            self.Lift=self.Thrust
        elif self.condition=='climb':
            pass
        elif self.condition=='descent':
            pass


        self.vdpCondition=input("Would you like to apply Vertical Drag Penalty (%)? : Yes/No").strip().lower()
        if (self.vdpCondition == 'no'):
            self.Lift_eff = self.Lift

        elif (self.vdpCondition =='yes'):
            self.vdp=float(input("Please enter Penalty for Vertical Drag (in %): "))
            self.applyVDP()

        self.applyc_QGeneral()

        self.applyPwrTor()

        self.applyFOM()

        for key, value, in self.__dict__.items():
            if value != 0 and value is not None:
                print(f"{key:15} : {value}")

   
    def LinearMode2(self):


        self.Lift=float(input("Please enter targeted Lift: "))
        self.vdpCondition=input("Would you like to apply Vertical Drag Penalty (%)? : Yes/No").strip().lower()

        if (self.vdpCondition == 'no'):
            self.Lift_eff = self.Lift

        elif (self.vdpCondition =='yes'):
            self.vdp=float(input("Please enter Penalty for Vertical Drag (in %): "))
            self.applyVDP()

        changed = True

        while changed and iteration<150:

            iteration+=1

            changed = False

            oldState = self.__dict__.copy()

            self.applyDia()
            self.applyArea()
            self.applyVtip()
            self.applyRPM()
            self.applyc_P()
            self.applyc_QGeneral()
            self.applyPwrTor()

            if iteration == 150:
                print("The solver could not converge. Try changing the values.")

            changed = oldState != self.__dict__

        self.applyWhichTaper()

        #for imperial units (hp), apply:
        #if (self.Power is not None):
        #    self.Power = self.Power / 550

        for key, value, in self.__dict__.items():
            if value != 0 and value is not None:
                print(f"{key:15} : {value}")


rotor = Rotor()

    #please enter what your input is, here:
    #INPUTBEGIN

rotor.mtow = 1950
rotor.Rad = 5.345
rotor.N_b = 3
rotor.v_tip = 213
rotor.Washout = 12.275 #- sign has already been taken into consideration
rotor.rho = 1.22858
rotor.a = 0.09948
rotor.k = 0.015
rotor.sect_c_d0 = 0.008
rotor.ch_root = 0.3



    #INPUTEND

rotor.gainData()
