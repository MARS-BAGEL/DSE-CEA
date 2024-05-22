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
oxid O2(L)   N 2 O 4   wt%=99.9
h,j/mol=0    
oxid CO2    C 1.0 O 2.0      wt%=0.1
h,j/mol=-393520     
"""
add_new_oxidizer( 'LOX_1pCO2', card_str )

card_str = """
oxid O2(L)   N 2 O 4   wt%=99
h,j/mol=0    
oxid CO2    C 1.0 O 2.0      wt%=1
h,j/mol=-393520     
"""
add_new_oxidizer( 'LOX_10pCO2', card_str )

card_str = """
oxid O2(L)   N 2 O 4   wt%=98
h,j/mol=0    
oxid CO2    C 1.0 O 2.0      wt%=2
h,j/mol=-393520     
"""
add_new_oxidizer( 'LOX_20pCO2', card_str )

pcL = [ 435.11321319] # 30 bar
ispObj0 = CEA_Obj(oxName='LOX', fuelName="LCO")
ispObj1 = CEA_Obj(oxName='LOX_1pCO2', fuelName="LCO")
ispObj10 = CEA_Obj(oxName='LOX_10pCO2', fuelName="LCO")
ispObj20 = CEA_Obj(oxName='LOX_20pCO2', fuelName="LCO")


# for Pc in pcL:
#     cstarArr100 = []
#     MR = 0.1
#     mrArr = []
#     while MR < 2.0:
#         cstarArr100.append( ispObj0.get_Cstar( Pc=Pc, MR=MR ) * 0.3048)
#         mrArr.append(MR)
#         MR += 0.01
#     plot(mrArr, cstarArr100, label='100% O2')

for Pc in pcL:
    cstarArr100 = []
    MR = 0.1
    mrArr = []
    while MR < 2.0:
        cstarArr100.append( ispObj1.get_Cstar( Pc=Pc, MR=MR ) * 0.3048)
        mrArr.append(MR)
        MR += 0.01
    plot(mrArr, cstarArr100, label='99.9% O2')

for Pc in pcL:
    cstarArr100 = []
    MR = 0.1
    mrArr = []
    while MR < 2.0:
        cstarArr100.append( ispObj10.get_Cstar( Pc=Pc, MR=MR ) * 0.3048)
        mrArr.append(MR)
        MR += 0.01
    plot(mrArr, cstarArr100, label='99% O2')

for Pc in pcL:
    cstarArr100 = []
    MR = 0.1
    mrArr = []
    while MR < 2.0:
        cstarArr100.append( ispObj20.get_Cstar( Pc=Pc, MR=MR ) * 0.3048)
        mrArr.append(MR)
        MR += 0.01
    plot(mrArr, cstarArr100, label='98% O2')

legend(loc='best')
grid(True)
#title( ispObj0.desc )
xlabel( 'O/F Ratio' )
ylabel( 'Cstar (m/sec)' )
savefig('cea_cstar_plot.png', dpi=120)

show()