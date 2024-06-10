import numpy as np
from rocketcea.cea_obj import CEA_Obj, add_new_fuel
import gas_fluid_properties
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
gamma_c, mach_c, Cp_c, mu_c, k_c, Pr_c = gas_fluid_properties.get_combustion_properties() #fetch properties of gas in combustion chamber 
r = Pr_c**(1/3) #EDIT LATER TO DIFFERENCIATE COMBUSTION CHAMBER AND THROAT 
mdot_c = 0.529 #total mass flow [kg/s] (from SSOT)
OF = 0.5714 #O/F ratio [-] taken from SSOT
mdot_f = mdot_c/(OF + 1) #mass flow of fuel [kg/s]  #CHECK IF CORRECT 
eta_c = 0.92 #combustion efficiency [-] #from sparrow paper, perform sensitivity analysis later 

#############################
#############################


def get_fuel_convectivity(temp, pressure, substance, stage): #this requires additional geometric input hence is calculated in this file
    cp, rho, mu, k = gas_fluid_properties.get_fuel_properties(temp, pressure, substance, stage)
    velocity = mdot_c/(rho*np.pi*((0.5*D_f)**2)) #get velocity from mass flow, density and area 
    Re = (rho*velocity*D_f/mu) #calculate reynolds number 
    Pr = (mu*cp)/k #calculate stationary prandtl number 
    Pr = 0.75 + 1.63/(np.log10(1 + Pr/0.0015)) #correct prandtl number for turbulence
    Nu = 0.023*(Re**0.8)*(Pr**0.4) #Nusselt number
    h_alpha = (k*Nu)/D_f #convective heat transfer coefficient 
    return h_alpha 

def get_gas_convectivity(T_left):
    T_hg = T_c + 0.8*(T_c*(eta_c**2) - T_c) #calculate 'hot gas temperature' as specified in method #DOUBLE CHECK 
    h_alpha = 0.01975*(((k_c**0.18)*((mdot_c*Cp_c)**0.82))/(D_c**1.82))*((T_hg/T_c)**0.35) #fuck you I like using brackets 
    return h_alpha
    






