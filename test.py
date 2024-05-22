from rocketcea.cea_obj import CEA_Obj, add_new_fuel, add_new_oxidizer, add_new_propellant
import CoolProp.CoolProp as CP
from pylab import *
import numpy as np

# isp_units            = 'sec',         # N-s/kg, m/s, km/s
# cstar_units          = 'ft/sec',      # m/s
# pressure_units       = 'psia',        # MPa, KPa, Pa, Bar, Atm, Torr
# temperature_units    = 'degR',        # K, C, F
# sonic_velocity_units = 'ft/sec',      # m/s
# enthalpy_units       = 'BTU/lbm',     # J/g, kJ/kg, J/kg, kcal/kg, cal/g
# density_units        = 'lbm/cuft',    # g/cc, sg, kg/m^3
# specific_heat_units  = 'BTU/lbm degR' # kJ/kg-K, cal/g-C, J/kg-K
# viscosity_units      = 'millipoise'   # lbf-sec/sqin, lbf-sec/sqft, lbm/ft-sec, poise, centipoise
# thermal_cond_units   = 'mcal/cm-K-s'  # millical/cm-degK-sec, BTU/hr-ft-degF, BTU/s-in-degF, cal/s-cm-degC, W/cm-degC



# Add LCO as a prop
card_str = """
fuel CO(L)  C 1.0   O 1.0     wt%=100.00
h,j/mol=-110530
"""
add_new_fuel( 'LCO', card_str )


# # General information
ispObj = CEA_Obj(propName='', oxName='LOX', fuelName='LCO')
s = ispObj.get_full_cea_output( Pc=30, MR=0.45, eps=22.8, short_output=1, pc_units='bar', output='siunits')
print( s )


# C* vs O/F
pcL = np.array([5.3, 10.7, 30]) #bar
pcL = pcL * 14.5037738        #psi
for Pc in pcL:
    cstarArr = []
    mrArr = []
    MR = 0.25
    while MR < 2:
        cstarArr.append( ispObj.get_Cstar( Pc=Pc, MR=MR ) * 0.3048 )
        mrArr.append(MR)
        MR += 0.01
    Pc = Pc / 14.5037738
    plot(mrArr, cstarArr, label='Pc=%g bar' %Pc)

    # plot max point
    bbox_props = dict(boxstyle="square,pad=0.0001", fc="w", ec="k", lw=0.72)
    arrowprops = dict(arrowstyle="->")
    kw = dict(arrowprops=arrowprops, bbox=bbox_props)
    xmax = mrArr[np.argmax(cstarArr)]
    ymax = np.max(cstarArr)
    annotate(f'{round(xmax, 2), int(ymax)}', xy=(xmax, ymax), xytext=(xmax + 0.8 , ymax - 5), **kw)
ylim(1100, 1400)
xlim(0, 2.2)
legend(loc='lower left')
grid(True)
title( ispObj.desc )
xlabel( 'O/F Ratio' )
ylabel( 'Cstar (m/s)' )
# savefig('cea_cstar_plot.png', dpi=120)
show()


# Isp vs eps
ispArr = []
isp_theo_Arr = []
epsL = range(1,271,1)
for eps in epsL:
    ispArr.append( ispObj.get_IvacCstrTc_ThtMwGam(Pc=435.113213, MR=0.45, eps=eps)[0] )
    isp_theo_Arr.append(ispObj.get_IvacCstrTc_ThtMwGam(Pc=435.113213, MR=0.571, eps=eps)[0])

plot(epsL, ispArr, label='Pc=30 bar; O/F=0.45')
plot(epsL, isp_theo_Arr, label='Pc=30 bar; O/F=0.571')
plt.plot([22.7981, 22.7981], [150, 270], 'r--',label='Isp=270s, Ae/At=22.8')
plt.plot([0, 22.7981],[270,270],'r--')
plt.plot([262, 262], [150, 308], 'g--',label='Isp=308s, Ae/At=262')
plt.plot([0, 262],[308.07, 308.07],'g--')
ylim(150, 400)
xlim(0, 270)
legend(loc='best')
grid(True)
title( ispObj.desc )
xlabel( 'Nozzle Expansion Area Ratio' )
ylabel( 'Isp' )
show()


# # O/F ratio
# for mr in range(2,9):
#     print(mr, ispObj.get_Isp(Pc=435.113213, MR=mr, eps=40) )

# print( ispObj.get_eps_at_PcOvPe(Pc=435.113213, MR=0.5, PcOvPe=435.113213/0.1015, frozen=1, frozenAtThroat=1) )