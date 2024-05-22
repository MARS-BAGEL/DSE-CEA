from rocketcea.cea_obj import CEA_Obj, add_new_fuel, add_new_oxidizer, add_new_propellant
import CoolProp.CoolProp as CP
from pylab import *
matplotlib.use('TkAgg')

# Add LCO as a prop
card_str = """
fuel CO(L)  C 1.0   O 1.0     wt%=100.00
h,j/mol=-110530
"""
add_new_fuel( 'LCO', card_str )

card_str = """
fuel CO(L)  C 1.0   O 1.0     wt%=99.90
h,j/mol=-110530
fuel CO2    C 1.0 O 2.0      wt%=0.10
h,j/mol=-393520
"""
add_new_fuel( 'LCO_1pCO2', card_str )

card_str = """
fuel CO(L)  C 1.0   O 1.0     wt%=99.00
h,j/mol=-110530
fuel CO2    C 1.0 O 2.0      wt%=1.00
h,j/mol=-393520
"""
add_new_fuel( 'LCO_10pCO2', card_str )

card_str = """
fuel CO(L)  C 1.0   O 1.0     wt%=95.00
h,j/mol=-110530
fuel CO2    C 1.0 O 2.0      wt%=5.00
h,j/mol=-393520
"""
add_new_fuel( 'LCO_50pCO2', card_str )

card_str = """
fuel CO(L)  C 1.0   O 1.0     wt%=90.00
h,j/mol=-110530
fuel CO2    C 1.0 O 2.0      wt%=10.00
h,j/mol=-393520
"""
add_new_fuel( 'LCO_100pCO2', card_str )

pcL = [ 435.11321319] # 30 bar
ispObj0 = CEA_Obj(oxName='LOX', fuelName="LCO")
ispObj1 = CEA_Obj(oxName='LOX', fuelName="LCO_1pCO2")
ispObj10 = CEA_Obj(oxName='LOX', fuelName="LCO_10pCO2")
ispObj50 = CEA_Obj(oxName='LOX', fuelName="LCO_50pCO2")
ispObj100 = CEA_Obj(oxName='LOX', fuelName="LCO_100pCO2")
# # ispObj = CEA_Obj(propName='', oxName='LOX', fuelName="LH2")
#
for Pc in pcL:
    cstarArr = []
    MR = 0.1
    mrArr = []
    while MR < 2.0:
        cstarArr.append( ispObj0.get_Cstar( Pc=Pc, MR=MR ) * 0.3048 )
        mrArr.append(MR)
        MR += 0.01
    plot(mrArr, cstarArr, label='100% CO')

for Pc in pcL:
    cstarArr1 = []
    MR = 0.1
    mrArr = []
    while MR < 2.0:
        cstarArr1.append( ispObj1.get_Cstar( Pc=Pc, MR=MR ) * 0.3048 )
        mrArr.append(MR)
        MR += 0.01
    plot(mrArr, cstarArr1, label='99.9% CO')

for Pc in pcL:
    cstarArr10 = []
    MR = 0.1
    mrArr = []
    while MR < 2.0:
        cstarArr10.append( ispObj10.get_Cstar( Pc=Pc, MR=MR ) * 0.3048)
        mrArr.append(MR)
        MR += 0.01
    plot(mrArr, cstarArr10, label='99% CO')

for Pc in pcL:
    cstarArr50 = []
    MR = 0.1
    mrArr = []
    while MR < 2.0:
        cstarArr50.append( ispObj50.get_Cstar( Pc=Pc, MR=MR ) * 0.3048)
        mrArr.append(MR)
        MR += 0.01
    plot(mrArr, cstarArr50, label='95% CO')

for Pc in pcL:
    cstarArr100 = []
    MR = 0.1
    mrArr = []
    while MR < 2.0:
        cstarArr100.append( ispObj100.get_Cstar( Pc=Pc, MR=MR ) * 0.3048)
        mrArr.append(MR)
        MR += 0.01
    plot(mrArr, cstarArr100, label='90% CO')

legend(loc='best')
grid(True)
#title( ispObj0.desc )
xlabel( 'O/F Ratio' )
ylabel( 'Cstar (m/sec)' )
savefig('cea_cstar_plot.png', dpi=120)

show()