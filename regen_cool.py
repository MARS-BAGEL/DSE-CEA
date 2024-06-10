import numpy as np
from rocketcea.cea_obj import CEA_Obj, add_new_fuel
from combustion import get_combustion_properties
import CoolProp.CoolProp as CP

CO = 'CARBONMONOXIDE'

#############################
#______input parameters_____#
#############################
T_c = 3300 #combustion temperature [K] #IMPORT FROM PREV FILE?
T_wall0 = 293 #initial wall temperature [K]
T_f0 = 100 #initial fuel temperature [K]
gamma_c, mach_c, Cp_c, mu_c, k_c, Pr_c = get_combustion_properties()
mdot_c = 0.529 #total mass flow [kg/s] (from SSOT)
OF = 0.5714 #O/F ratio [-] taken from SSOT
mdot_f = mdot_c/(OF + 1) #mass flow of fuel [kg/s]  #CHECK IF CORRECT 
D_c = 0.1 #diameter of chamber [m] #MAKE MORE ACCURATE LATER 
D_f = 0.008 #diameter of fuel cooland channels [m]
eta_c = 0.92 #combustion efficiency [-] #from sparrow paper, perform sensitivity analysis later 


def get_fuel_properties(temp, pressure, substance):
    cp = CP.PropsSI('C', 'T', temp, 'P', pressure, substance) #get the Cp in [kJ/kgK]
    rho = CP.PropsSI('D', 'T', temp, 'P', pressure, substance) #get density in [kg/m^3]
    mu = CP.PropsSI('V', 'T', temp, 'P', pressure, substance) #get dynamic viscocity in [Pa-s]
    k = CP.PropsSI('L', 'T', temp, 'P', pressure, substance) #get density in [kg/m^3]
    






