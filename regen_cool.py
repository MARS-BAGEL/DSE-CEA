import numpy as np
from rocketcea.cea_obj import CEA_Obj, add_new_fuel
from combustion import get_combustion_properties
import CoolProp.CoolProp as CP

CO = 'CarbonMonoxide'

#############################
#______input parameters_____#
#############################
stage = 2 #enter 1 for first stage engine, 2 for second stage engine

#geometry 
D_c = 0.1 #diameter of chamber [m] #MAKE MORE ACCURATE LATER 
D_f = 0.008 #diameter of fuel cooland channels [m]
t = 0.01 #thickness of engine between combustion and cooling channel [m] 

#thermal/fluid
T_c = 3300 #combustion temperature [K] #IMPORT FROM PREV FILE?
T_wall0 = 293 #initial wall temperature [K]
T_f0 = 100 #initial fuel temperature [K]
gamma_c, mach_c, Cp_c, mu_c, k_c, Pr_c = get_combustion_properties()
r = Pr_c**(1/3) #EDIT LATER TO DIFFERENCIATE COMBUSTION CHAMBER AND THROAT 
mdot_c = 0.529 #total mass flow [kg/s] (from SSOT)
OF = 0.5714 #O/F ratio [-] taken from SSOT
mdot_f = mdot_c/(OF + 1) #mass flow of fuel [kg/s]  #CHECK IF CORRECT 
eta_c = 0.92 #combustion efficiency [-] #from sparrow paper, perform sensitivity analysis later 

#############################
#############################





def get_CO_dynamic_visc(temp, stage): 
    #linearly interpolating data from https://webbook.nist.gov/cgi/fluid.cgi?P=15&TLow=100&THigh=200&TInc=1&Digits=5&ID=C630080&Action=Load&Type=IsoBar&TUnit=K&PUnit=bar&DUnit=kg%2Fm3&HUnit=kJ%2Fmol&WUnit=m%2Fs&VisUnit=Pa*s&STUnit=N%2Fm&RefState=DEF
    #coolprop unfortunately does not have viscocity model for CO

    if stage == 2: #calculations done at 15 bar for upper stage
        if temp>115:
            print('BOMBOCLART this bitch finna vapourise')
            exit()
        viscosity_values = np.array([
        9.4763e-05, 9.2101e-05, 8.9522e-05, 8.7028e-05, 8.4589e-05, 8.2232e-05, 7.9917e-05,
        7.7666e-05, 7.5465e-05, 7.3308e-05, 7.1191e-05, 6.9107e-05, 6.7052e-05, 6.5026e-05,
        6.3003e-05, 6.0995e-05
        ])
        temps = np.arange(100,116,1)    
    elif stage == 1:  #calculations done at 25 bar for lower stage
        print('havent coded this yet innit')       
    else:
        print('Please enter a valid stage number (1 or 2)')    
        exit() 

    temp = round(temp) #round to nearest int to match with data 
    index = np.where(temps == temp)[0]
    mu = viscosity_values[index][0] #[Pa*s]
    return mu

def get_CO_conductivity(temp, stage): 
    #linearly interpolating data from https://webbook.nist.gov/cgi/fluid.cgi?P=15&TLow=100&THigh=200&TInc=1&Digits=5&ID=C630080&Action=Load&Type=IsoBar&TUnit=K&PUnit=bar&DUnit=kg%2Fm3&HUnit=kJ%2Fmol&WUnit=m%2Fs&VisUnit=Pa*s&STUnit=N%2Fm&RefState=DEF
    #coolprop unfortunately does not have viscocity model for CO

    if stage == 2: #calculations done at 15 bar for upper stage
        if temp>115:
            print('BOMBOCLART this bitch finna vapourise')
            exit()
        conductivity_values = np.array([
        0.10841, 0.10658, 0.10474, 0.10290, 0.10106, 0.099202, 0.097340, 
        0.095469, 0.093588, 0.091696, 0.089791, 0.087871, 0.085943, 0.083979,
        0.082001, 0.079997
        ])
        temps = np.arange(100,116,1)    
    elif stage == 1:  #calculations done at 25 bar for lower stage
        print('havent coded this yet innit')       
    else:
        print('Please enter a valid stage number (1 or 2)')    
        exit() 
        
    temp = round(temp) #round to nearest int to match with data 
    index = np.where(temps == temp)[0]
    k = conductivity_values[index][0] #[W/m*k]
    return k



def get_fuel_properties(temp, pressure, substance, stage):
    cp = CP.PropsSI('C', 'T', temp, 'P', pressure, substance) #get the Cp in [J/kg/K]  #DOUBLE CHECK UNITS
    rho = CP.PropsSI('D', 'T', temp, 'P', pressure, substance) #get density in [kg/m^3]
    mu = get_CO_dynamic_visc(temp, stage) #get dynamic viscocity in [Pa-s] 
    k = get_CO_conductivity(temp, stage) #get thermal conductivity in [kW/m/K]
    return cp

print(get_CO_conductivity(113,2))
    






