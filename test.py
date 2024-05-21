from rocketcea.cea_obj import CEA_Obj, add_new_fuel, add_new_oxidizer, add_new_propellant
import CoolProp.CoolProp as CP
from pylab import *

# isp_units            = 'sec',         # N-s/kg, m/s, km/s
# cstar_units          = 'ft/sec',      # m/s
# pressure_units       = 'psia',        # MPa, KPa, Pa, Bar, Atm, Torr
# temperature_units    = 'degR',        # K, C, F
# sonic_velocity_units = 'ft/sec',      # m/s
# enthalpy_units       = 'BTU/lbm',     # J/g, kJ/kg, J/kg, kcal/kg, cal/g
# density_units        = 'lbm/cuft',    # g/cc, sg, kg/m^3
# specific_heat_units  = 'BTU/lbm degR' # kJ/kg-K, cal/g-C, J/kg-K
# viscosity_units      = 'millipoise'   # lbf-sec/sqin, lbf-sec/sqft, lbm/ft-sec, poise, centipoise
# thermal_cond_units   = 'mcal/cm-K-s'  # millical/cm-degK-sec, BTU/hr-ft-degF, BTU/s-in-degF,
#                                       #  cal/s-cm-degC, W/cm-degC

# # O/F ratio
# C = CEA_Obj( oxName='LOX', fuelName='LH2')
# for mr in range(2,9):
#     print(mr, C.get_Isp(Pc=100.0, MR=mr, eps=40.0) )



# Add LCO as a prop
card_str = """
fuel CO(L)  C 1.0   O 1.0     wt%=100.00
h,j/mol=-110530
"""
add_new_fuel( 'LCO', card_str )


# # General information
ispObj = CEA_Obj(oxName='LOX', fuelName='LCO')
# s = ispObj.get_full_cea_output( Pc=30, MR=0.571, eps=40.0, short_output=1, pc_units='bar', output='siunits')
# print( s )



# # C* vs O/F
# pcL = [ 435.113213 ]
# # ispObj = CEA_Obj(propName='', oxName='LOX', fuelName='LCO')
#
# for Pc in pcL:
#     cstarArr = []
#     MR = 0.25
#     mrArr = []
#     while MR < 2:
#         cstarArr.append( ispObj.get_Cstar( Pc=Pc, MR=MR ) * 0.3048 )
#         mrArr.append(MR)
#         MR += 0.01
#     Pc = 30
#     plot(mrArr, cstarArr, label='Pc=%g bar' %Pc)
# ylim(1100, 1400)
# xlim(0, 2.2)
# legend(loc='best')
# grid(True)
# title( ispObj.desc )
# xlabel( 'O/F Ratio' )
# ylabel( 'Cstar (m/s)' )
# # savefig('cea_cstar_plot.png', dpi=120)
# show()





# Isp vs eps
ispArr = []
epsL = range(1,41,1)
for eps in epsL:
    ispArr.append( ispObj.get_IvacCstrTc_ThtMwGam(Pc=435.113213, MR=0.571, eps=eps)[0] )

plot(epsL, ispArr, label='Pc=30 bar; O/F=0.571')
legend(loc='best')
grid(True)
title( ispObj.desc )
xlabel( 'Nozzle Expansion Area Ratio' )
ylabel( 'Isp' )
show()
