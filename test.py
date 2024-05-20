from rocketcea.cea_obj import CEA_Obj, add_new_fuel, add_new_oxidizer, add_new_propellant
import CoolProp.CoolProp as CP
from pylab import *

# # O/F ratio
# C = CEA_Obj( oxName='LOX', fuelName='LH2')
# for mr in range(2,9):
#     print(mr, C.get_Isp(Pc=100.0, MR=mr, eps=40.0) )


# # General information
# ispObj = CEA_Obj( oxName='LOX', fuelName='LH2')
# s = ispObj.get_full_cea_output( Pc=1000.0, MR=6.0, eps=40.0, short_output=1)
# print( s )




# Add LCO as a prop
card_str = """
fuel CO(L)  C 1.0   O 1.0     wt%=100.00
h,cal=12900.0     t(k)=80   rho=CP.PropsSI('D', 'T', 80, 'P', 1500000, 'CarbonMonoxide')
"""
add_new_fuel( 'LCO', card_str )
# C = CEA_Obj(oxName="LOX", fuelName="LCO")
# s = C.get_full_cea_output( Pc=1850.0, MR=0.7, eps=40.0, short_output=1)
# print( s )




# pcL = [ 2000., 500., 70.]
#
# ispObj = CEA_Obj(propName='', oxName='LOX', fuelName="LCO")
# # ispObj = CEA_Obj(propName='', oxName='LOX', fuelName="LH2")
#
# for Pc in pcL:
#     cstarArr = []
#     MR = 0.25
#     mrArr = []
#     while MR < 8.0:
#         cstarArr.append( ispObj.get_Cstar( Pc=Pc, MR=MR ) )
#         mrArr.append(MR)
#         MR += 0.05
#     plot(mrArr, cstarArr, label='Pc=%g psia'%Pc)
#
# legend(loc='best')
# grid(True)
# title( ispObj.desc )
# xlabel( 'O/F Ratio' )
# ylabel( 'Cstar (ft/sec)' )
# savefig('cea_cstar_plot.png', dpi=120)
#
# show()