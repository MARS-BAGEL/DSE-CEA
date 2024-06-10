import numpy as np
import CoolProp.CoolProp as CP

fluid = 'CARBONMONOXIDE'
pressure_at_critical_point = CP.PropsSI(fluid,'pcrit')
print(pressure_at_critical_point)

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





