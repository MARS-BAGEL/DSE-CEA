import numpy as np
import CoolProp.CoolProp as CP

CO = 'CARBONMONOXIDE'

# #############################
# #______input parameters_____#
# #############################
# T_c = 3300 #combustion temperature [K] #IMPORT FROM PREV FILE?
# T_wall0 = 293 #initial wall temperature [K]
# T_f0 = 100 #initial fuel temperature [K]
# gamma_c = #import from other file 
# mach_c = #import from other file 
# Pr_c = #import from other file
# mdot_c = #import from other file '
# mdot_f = #import from other file
# k_c = #import from other file 
# Cp_c = #import from other file
# D_c = 
# eta_c = 
# Pr_f = 

def get_fuel_properties(temp, pressure, substance):
    Cp = CP.PropsSI('C', 'T', temp, 'P', pressure, substance) #fetch the Cp in J/kgK
    #rho = CP.PropSI()
    return Cp

print(get_fuel_properties(293, 100000, CO))






