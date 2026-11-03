import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
g = 9.81

print("Please use meters and kilograms wherever unspecified. \nSmall angle approximation is inherent in the current programme (phi<10 degrees). \n Please neglect the sign for Washout and enter the positive value. We have implicitly assumed that the blade is washed-out and not washed-in.\nUniform mass distribution has been assumed throughout the blade.\nThis model is valid only for NACA 0012 propellers.")

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
        self.rho = None
        self.v_i = None
        self.Thrust = None
        self.Lift = None #add t/w ratio
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
        self.vdp = None
        self.condition = None
        self.twistType = None
        self.taperType = None
        self.solidity = None
        self.n = None
        self.designMode = None
        self.centrePitch = None
        self.tipPitch = None
        self.Washout = None
        #self.c_l_avg = None
        #self.alpha_avg = None
        self.thrustToWeight = None
        self.mtow = None
        self.tipLoss = None
        self.v_sound = None
        self.aoa0 = None
        self.collectivePitch = None
        self.vis_dyn = None
        self.c_TdivSol = None
        self.airfoil = None


    def gainData(self):


        print("PLEASE SELECT MODE:\n\n" \
        "Enter 1 for COMPUTE FOR GIVEN CONFIGURATION\n" \
        "(Press enter to leave a value blank.)")
        #after computation for given configuration is completed, design for different optimisations will be added as well.
                
        self.designMode=int(input("Enter Selection: "))
        #add mode 2 to achieve target

        #self.condition=input("Please enter flight state: Climb/Hover/Descent ").strip().lower()
        self.condition = 'hover'
        self.twistType=input("Please enter type of twist: Linear/Ideal: ").strip().lower()

        if(self.twistType != 'linear' and self.twistType != 'ideal'):
            print("ERROR: Twist type not supported.")

        self.calculate()

    def calculate(self):
        self.N_b = 4
        self.Rad = 9.144
        self.cutoutRatio = 0.15
        self.mtow = 8900
        self.v_tip = 198.12
        self.Washout = (10 * math.pi ) / 180
        self.collectivePitch = (17.5 * math.pi) / 180
        self.ch_root = 0.6096
        self.taperRatio = 1
        self.rho = 1.225
        self.v_sound = 340.263
        self.aoa0 = 0
        #self.tipPitch = (8.06 * math.pi) / 180
        self.vis_dyn = 1.789e-05
        self.airfoil = 'naca0012'
        self.I_b = 3891

        q = 10
        while q>0:
            self.applyArea()
            self.applyDia()
            self.applyRPM()
            self.applyVtip()

            q = (q - 1)

                    ### PITCH ###

                #how to make programme capable of reading imported values?

        if self.twistType == 'linear':
            if self.airfoil == 'naca0012' and self.Washout is not None:
                self.centrePitch = self.collectivePitch
                self.tipPitch = self.collectivePitch - self.Washout      

            elif self.collectivePitch is None and self.centrePitch is None and self.tipPitch is None:
                print("Please enter more data.")
                exit()

                #can i forego this?? add a functionality here

                    ### PITCH ###

        if self.designMode==1:
            self.Mode1()


        #elif self.designMode==2:
        #    self.Mode2()

    def Mode1(self):

        ### GEOMETRY ###
        self.taperType = input("Please enter taper category: Linear/Power/Constant ").strip().lower()
        if self.ch_root is None:
            self.applyTaperRatio()

        if (self.taperType == 'power'):
            self.n=float(input("Please enter index of the Power law for taper variation: "))

        elif (self.taperType =='constant'):
            if self.ch_root is not None:
                self.chord = self.ch_root
            elif self.ch_tip is not None:
                self.chord = self.ch_tip
            elif (
                    self.solidity is not None
                    and self.Rad is not None
                    and self.N_b is not None
                ):
                    self.chord = (self.solidity * self.Rad * math.pi) / self.N_b

            if self.chord is None:
                ifChordKnown=input("Do you have a value for constant chord? Yes/No : ").strip().lower()
                if (ifChordKnown == 'yes'):
                    self.chord = float(input("Please enter the constant chord value: "))
                    self.ch_root = self.chord
                    self.ch_tip = self.chord
                    self.taperRatio = 1
                else:
                    print("Data insufficient.")

        self.applySolidity()
        print("Collectivepitch=", self.collectivePitch)

        #print("Please enter slope at 0 mach and 0 lift AOA in degrees.")

        r = np.linspace(self.cutoutRatio, 1, 100)
        tempC_T = 0
        cQ_prof = 0

        temp_cQ_prof = []

        elements = {
            "RadRatio": [],
            "chordAtStn": [],
            "chordRatio": [],
            "localMach": [],
            "localSlope": [],
            "localPitch": [],
            "localv_i": [],
            "localAOA": [],
            "localV_rel": [],
            "localRe": [],
            "localcl": [],
            "localc_T": [],
            "localc_D": []
        }

        cTValues = []

        ### GEOMETRY ###

        ### COEFFICIENT OF THRUST ###

        for num in r:
            RadRatio, chordAtStn, chordRatio, localMach, localSlope, localPitch, localv_i, localAOA, localV_rel, localRe, localcl = self.applyElements(num)

            localC_T = (RadRatio**2 * self.N_b * chordRatio * localcl) / (2 * math.pi)

            localcd = self.applylocalcd(localMach, localAOA)
            
            dcQ_prof = (self.N_b * (RadRatio**3) * chordRatio * localcd) / (2 * math.pi) 

            temp_cQ_prof.append(dcQ_prof)

            cTValues.append(localC_T)
            localcd = self.applylocalcd(localMach, localAOA)


            elements["RadRatio"].append(RadRatio)
            elements["chordAtStn"].append(chordAtStn)
            elements["chordRatio"].append(chordRatio)
            elements["localMach"].append(localMach)
            elements["localSlope"].append(localSlope)
            elements["localPitch"].append(((localPitch * 180) / math.pi))
            elements["localv_i"].append(localv_i)
            elements["localAOA"].append(((localAOA * 180) / math.pi))
            elements["localV_rel"].append(localV_rel)
            elements["localRe"].append(localRe)
            elements["localcl"].append(localcl)
            elements["localc_T"].append(localC_T)
            elements["localc_D"].append(localcd)

            tempC_T = np.trapezoid(cTValues, elements["RadRatio"])

        df = pd.DataFrame(elements)

        print(df.to_string(
            index=False
        ))


        ifToPrint = (input("Would you like to export the above data to a CSV file? Yes/No: ")).strip().lower()
        if ifToPrint=='yes':
            df.to_csv("Blade Results.csv", index = False)
            print("Data exported.")

        '''the tip loss calculations are based upon the data set of carpenters experiments- true only for the configuration used in those experiments
        REFERENCE: Carpenter, "Lift and Profile-Drag Characteristics of an NACA 0012 Airfoil 
        Section as Derived from Measured Helicopter-Rotor Hovering Performance," 
        NACA TN 4357, 1958.
         -prouty, page 71 '''

        cQ_prof = np.trapezoid(temp_cQ_prof, r)

        c_T_iter1 = tempC_T

        if c_T_iter1<=0.006:
            self.tipLoss = 1 - (0.06 / self.N_b)
        else:
            self.tipLoss = 1 - (((math.sqrt((2.27 * c_T_iter1) - 0.01))) / self.N_b)

        tempRemoved = 0
        removedCT = 0

        r = np.linspace(self.tipLoss, 1, 100)
        tempRemoved = 0

        removedCT_Values = []

        for num in r:
            RadRatio, chordAtStn, chordRatio, localMach, localSlope, localPitch, localv_i, localAOA, localV_rel, localRe, localcl = self.applyElements(num)


            removedCT = (RadRatio**2 * self.N_b * chordRatio * localcl) / (2 * math.pi)

            removedCT_Values.append(removedCT)

        tempRemoved = np.trapezoid(removedCT_Values, r)

        self.c_T = c_T_iter1 - tempRemoved
        self.c_T = 0.00719

        ### COEFFICIENT OF THRUST ###

        ### COEFFICIENT OF TORQUE ###

        temp_cQ_ind = []
        cQ_ind = 0

        r = np.linspace(self.cutoutRatio, self.tipLoss, 100)
        for num in r:
            RadRatio, chordAtStn, chordRatio, localMach, localSlope, localPitch, localv_i, localAOA, localV_rel, localRe, localcl = self.applyElements(num)

            localInflow = ((((localSlope * 180) / math.pi) * self.N_b * chordRatio) / (16 * math.pi * RadRatio)) * ((-1)+(math.sqrt(1+((32 * math.pi * localPitch * RadRatio) / (((localSlope * 180) / math.pi) * self.N_b * chordRatio)))))

            dcQ_ind = (self.N_b * (RadRatio**3) * chordRatio * localcl * localInflow) / (2 * math.pi)

            temp_cQ_ind.append(dcQ_ind)

        cQ_ind = np.trapezoid(temp_cQ_ind, r)

        plotArray = np.linspace(0.0001, 1, 100)
        elementsGraphing = {var: [] for var in ["RadRatio", "chordAtStn", "localPitch", "localAOA", "localcl", "localcd", "localMach", "localSlope", "localInflow", "localcT", "localc_Q0", "localc_Qi"]}
        for num in plotArray:
            RadRatio, chordAtStn, chordRatio, localMach, localSlope, localPitch, localv_i, localAOA, localV_rel, localRe, localcl = self.applyElements(num)
            localcd = self.applylocalcd(localMach, localAOA)

            localInflow = math.atan(localv_i / (self.omega * self.Rad * RadRatio))
            #gotta compute this separately because other values are being updated at each turn and returned. inflow only calculated for the list purpose otherwise, not for computation.

            elementsGraphing["RadRatio"].append(RadRatio)
            elementsGraphing["chordAtStn"].append(chordAtStn)
            elementsGraphing["localPitch"].append(((localPitch * 180)/ math.pi))
            elementsGraphing["localAOA"].append(((localAOA * 180) / math.pi))
            elementsGraphing["localcl"].append((10 * localcl))
            elementsGraphing["localcd"].append((100 * localcd))
            elementsGraphing["localMach"].append((10 * localMach))
            elementsGraphing["localSlope"].append(((localSlope * 180) / math.pi))
            elementsGraphing["localInflow"].append(((180 * math.atan((localv_i / (self.omega * RadRatio * self.Rad))) / math.pi)))
            elementsGraphing["localcT"].append(1000 * (((RadRatio**2 * self.N_b * chordRatio * localcl) / (2 * math.pi))))
            elementsGraphing["localc_Q0"].append(10000 * (((self.N_b * (RadRatio**3) * chordRatio * localcd) / (2 * math.pi))))
            if num<=self.tipLoss:
                elementsGraphing["localc_Qi"].append((10000 * ((self.N_b * (RadRatio**3) * chordRatio * localcl * localInflow) / (2 * math.pi))))
            else:
                elementsGraphing["localc_Qi"].append(np.nan)

        for key, lbl in [("chordAtStn", "c"), ("localPitch", "θ"), ("localAOA", "α"),( "localcl", "10 * cl"), ("localcd", "100 * cd"), ("localMach", "10*M"), ("localSlope", "a"), ("localInflow", "tan^-1(vi/omega*r)"), ("localcT", "1000 * dcT/(dr/R)"), ("localc_Q0", "10000 * dcQ0/d(r/R)"), ("localc_Qi", "10000 * dcQi/d(r/R)")]:
            plt.plot(elementsGraphing["RadRatio"], elementsGraphing[key], label = lbl)

        plt.axvspan(0, self.cutoutRatio, color = "gray", alpha = 0.15)
        plt.xlim(0,1)
        plt.xlabel("Radial Postition (r/R)")
        plt.title("Parameter Distribution")
        plt.grid(True)
        plt.legend()
        plt.show()

        #########################################################################################s

        localSwirlbyThrust = 0
        swirlPowdivThrustPow = []

        r =  np.linspace((math.sqrt(2*self.c_T)), 1, 600)

        for num in r:
            RadRatio, chordAtStn, chordRatio, localMach, localSlope, localPitch, localv_i, localAOA, localV_rel, localRe, localcl = self.applyElements(num)

            localC_T = (RadRatio**2 * self.N_b * chordRatio * localcl) / (2 * math.pi)

            localSwirlbyThrust = (RadRatio**3) * ((1 - (math.sqrt (1 - ((2*self.c_T) / (RadRatio**2)))))**2)

            swirlPowdivThrustPow.append(localSwirlbyThrust)

        swirlPowdivThrustPow = (np.trapezoid(swirlPowdivThrustPow, r)) / self.c_T

        cQ_rot = swirlPowdivThrustPow * cQ_ind

        self.diskLoad = self.c_T * self.rho * (self.v_tip**2)

        self.c_TdivSol = self.c_T / ((self.N_b * self.chord) / (math.pi * self.Rad))

        DlxCtbySol = 0
        DlxCtbySol = (self.diskLoad * self.c_TdivSol) / 47.88

        if (DlxCtbySol<0.4788 or DlxCtbySol>63.2016):  #from 0.01 lb/ft2 to 1.32lb/ft2 (approximated range from fig 1.34; page 58, prouty)
            print("Range invalid for empirical correction for tip vortex interference.")
            exit()
        else:
            if ((142.01098**2) - (4 * 74.6807 * (67.54978 - (DlxCtbySol)))) >= 0:
                correction_TipInterfere = (142.01098 + math.sqrt((142.01098**2) - (4 * 74.6807 * (67.54978 - (DlxCtbySol))))) / (2 * 74.6807)
            else: 
                print("ERROR. Values unacceptable. Discriminant negative. Recompute.")
                exit()

        self.c_Q = 0
        self.Thrust = 0
        self.Power = 0
        self.Fom = 0


        self.c_Q = (cQ_prof + cQ_ind + cQ_rot) * (correction_TipInterfere)
        self.Thrust = self.rho * self.Area * (self.v_tip**2) * self.c_T
        self.Power = (self.rho * self.Area * (self.v_tip**3) * self.c_Q)
        self.Fom = (self.c_T**1.5) / ((math.sqrt(2) * self.c_Q)) 

        print("Solidity: ", self.solidity)
        print("Pitch at tip (degrees): ", (self.tipPitch * 180) / math.pi)
        print("Tip velocity (ft/s): ", self.v_tip / 0.3048)
        print("Cutout Ratio: ",self.cutoutRatio)
        print("The coefficient of Thrust without tip loss is: ", c_T_iter1)
        print("Tip Loss factor is (B): ", self.tipLoss)
        print("Coefficient of thrust after accounting for tip loss: ", self.c_T)
        print("Profile Torque Coefficient is : ", cQ_prof)
        print("Induced Torque Coefficient is : ", cQ_ind)
        print("CQ_rot (additional power required due to rotation of wake) / CQ_induced: ", cQ_rot / cQ_ind)
        print("Disk Loading: (lbf/ft^2) ", self.diskLoad / 47.8803)
        print("CT/sol: ", self.c_TdivSol)
        print("CT/solidity * DL", DlxCtbySol)
        print("Correction due to Tip Interference (Measured Pwr/Calculated Pwr): ", correction_TipInterfere)
        print("CQ/solidity ", self.c_Q / self.solidity)
        print("Thrust (at Sea Level): ", self.Thrust * 0.224809)
        print("Power (hp): ", self.Power / 745.7)
        print("FOM: ", self.Fom)


        self.applyWeightArm()

        self.applyConing()
        print("Weight arm: ", self.M_w)
        print("coning angle: ", self.a0)


#basic elementary functions
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

    def applyConing(self):

        if (
            self.a0 is None
            and self.rho is not None
            and self.M_w is not None
            and self.omega is not None
            and self.Rad is not None
            and self.I_b is not None
        ):
            r = np.linspace(self.cutoutRatio, 1, 100)
            M_liftInt = 0

            for num in r:

                RadRatio, chordAtStn, chordRatio, localMach, localSlope, localPitch, localv_i, localAOA, localV_rel, localRe, localcl = self.applyElements(num)

                integral = (chordAtStn * localcl * RadRatio**3)
                M_liftInt += integral
            
            self.a0 = ((self.rho * M_liftInt * (self.Rad**4)) / (2 * self.I_b)) + (self.M_w / (self.I_b * self.omega**2))

            print("Coning angle is ", self.a0)

    def applyWeightArm(self):
        if (
            self.I_b is None
            and self.moi is not None
            and self.N_b is not None
        ):
            self.I_b = self.moi / self.N_b
    
        if (
            self.M_w is None
            and self.Rad is not None
            and self.I_b is not None
        ):
            self.M_w = (3 * g * self.I_b) / (2 * self.Rad)

    def applyTaperRatio(self):
        if (
            self.ch_root is None
            and self.taperRatio is not None
            and self.ch_tip is not None
        ):
            self.ch_root = self.ch_tip / self.taperRatio

        elif (
            self.taperRatio is None
            and self.ch_tip is not None
            and self.ch_root is not None
        ):
            self.taperRatio = self.ch_tip / self.ch_root

        elif (
            self.ch_tip is None
            and self.taperRatio is not None
            and self.ch_root is not None
        ):
            self.ch_tip = self.taperRatio * self.ch_root

    def applySolidity(self, N=100):
        if (self.taperType == 'constant'):
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
            chordSum = 0
            r_ = np.linspace(self.cutoutRatio, 1, 100)
            r2 = r_[1] - r_[0]
            for num in r_:

                tempTaper = self.applyTaper(num)

                dchord = (tempTaper * (num**2) * r2)

                chordSum += dchord

            self.chord = (3 * chordSum) 

            if (
                self.solidity is None
                and self.N_b is not None
                and self.chord is not None
                and self.Rad is not None
            ):
                self.solidity = (self.N_b * self.chord) / (self.Rad * math.pi)


#complex#

    def applyTaper(self, x):

        if (self.taperType == 'linear'):
            return self.ch_root * (1+((self.taperRatio-1)*x))
        elif (self.taperType == 'power'):
            return self.ch_root * (1+((self.taperRatio-1)*(x**self.n)))
        elif (self.taperType =='constant'):
            return self.ch_root
        #elif (self.taperType =='custom'):

    def applyTwistIdeal(self, x):
        if (self.tipPitch is None):
            self.tipPitch=float(input("Please enter tip pitch: "))

        if (self.Rad is None):
            self.Rad=float(input("Please enter rotor radius: "))

        return self.tipPitch / x

    def applyTwistLinear(self, x):

        if (self.centrePitch is None):
            self.centrePitch=float(input("Please enter the pitch at the centre of rotation: "))

        if (self.Washout is None):
            self.Washout=float(input("Please enter the magnitude of washout: "))

        return (x * self.Washout )

    def applyElements(self, num):
            RadRatio = num
            chordAtStn = self.applyTaper(RadRatio) 
            chordRatio = chordAtStn / self.Rad
            localMach = (RadRatio * self.v_tip) / self.v_sound

            ### MACH & SLOPE ###

            if (localMach >= 1):
                print("SUPERSONIC FLOW. OUT OF BOUNDS.")
                exit()
            if localMach < 0.725:
                localSlope = (((0.1) / math.sqrt(1 - (localMach**2))) - (0.01 * localMach))
            else:
                localSlope = (0.677 - (0.744 * localMach))

            if localMach < 0.725:
                localstallAOA = 15 - (16 * localMach)
                localK1 = 0.0233 + (0.342 * (localMach**7.15))
                localK2 = 2.05 - (0.95 * localMach) 

            else:
                localstallAOA = 3.4
                localK1 = 0.575 - (0.144 * ((localMach - 0.725)**0.44)) 
                localK2 = 2.05 - (0.95 * localMach) 

            ### MACH AND SLOPE ###

            ### PITCH ###

            if self.twistType=='linear':
                localTwist = self.applyTwistLinear(RadRatio)
                localPitch = self.collectivePitch - localTwist - self.aoa0
            elif self.twistType=='ideal':
                localPitch = self.applyTwistIdeal(RadRatio)

            ### PITCH ###

            ### GENERAL ###
    
            localv_i = ((self.omega*self.Rad*RadRatio) * ((((localSlope*180)/math.pi) * self.N_b * chordRatio) / (16 * math.pi * RadRatio)) * ((-1)+(math.sqrt(1+((32 * math.pi * localPitch * RadRatio) / (((localSlope*180) / math.pi) * self.N_b * chordRatio))))))
            localAOA = localPitch - (math.atan((localv_i) / (self.omega * self.Rad * RadRatio)))
            localV_rel = math.sqrt(((self.omega * RadRatio * self.Rad)**2) + (localv_i**2))
            localRe = self.rho * localV_rel * chordAtStn / self.vis_dyn

            ### GENERAL ###

            ### LOCAL CL ###

            if ((localAOA * 180) / math.pi)<localstallAOA:
                localcl = localSlope * ((localAOA * 180) / math.pi)
            elif ((localAOA * 180) / math.pi)>=localstallAOA:
                localcl = (localSlope * ((localAOA * 180) / math.pi)) - (localK1 * ((((localAOA * 180) / math.pi) - localstallAOA)**localK2))

            ### LOCAL CL ###

            list1 = [RadRatio, chordAtStn, chordRatio, localMach, localSlope, localPitch, localv_i, localAOA, localV_rel, localRe, localcl]

            return list1
        
    def applylocalcd(self, localMach, localAOA):
        localAOA_incomp = 17 - (23.4 * localMach)

        if ((localAOA * 180) / math.pi) < localAOA_incomp:
            localcd_incomp = 0.0081 + (((-350 * ((localAOA * 180) / math.pi)) + (396 * (((localAOA * 180) / math.pi)**2)) - (63.3 * (((localAOA * 180) / math.pi)**3)) + (3.66 * (((localAOA * 180) / math.pi)**4))) * (10**(-6)))
            localcd = localcd_incomp
        elif ((localAOA * 180) / math.pi) >= localAOA_incomp:
            localcd_incomp = 0.0081 + (((-350 * ((localAOA * 180) / math.pi)) + (396 * (((localAOA * 180) / math.pi)**2)) - (63.3 * (((localAOA * 180) / math.pi)**3)) + (3.66 * (((localAOA * 180) / math.pi)**4))) * (10**(-6)))
            localK3 = 0.00066
            localK4 = 2.54
            localcd = localcd_incomp + (localK3 * ((((localAOA * 180) / math.pi) - localAOA_incomp)**localK4))

        return localcd


rotor = Rotor()
rotor.gainData()