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


# General information
ispObj = CEA_Obj(propName='', oxName='LOX', fuelName='LCO')
s = ispObj.get_full_cea_output( Pc=15, MR=0.55, eps=262, short_output=1, pc_units='bar', output='siunits')
print( s )


# # PLOT: C* vs O/F
# pcL = np.array([5.3, 10.7, 30]) #bar
# pcL = pcL * 14.5037738        #psi
# for Pc in pcL:
#     cstarArr = []
#     mrArr = []
#     MR = 0.25
#     while MR < 2:
#         cstarArr.append( ispObj.get_Cstar( Pc=Pc, MR=MR ) * 0.3048 )
#         mrArr.append(MR)
#         MR += 0.01
#     Pc = Pc / 14.5037738
#     plot(mrArr, cstarArr, label='Pc=%g bar' %Pc)
#
#     # plot max point
#     bbox_props = dict(boxstyle="square,pad=0.0001", fc="w", ec="k", lw=0.72)
#     arrowprops = dict(arrowstyle="->")
#     kw = dict(arrowprops=arrowprops, bbox=bbox_props)
#     xmax = mrArr[np.argmax(cstarArr)]
#     ymax = np.max(cstarArr)
#     annotate(f'{round(xmax, 2), int(ymax)}', xy=(xmax, ymax), xytext=(xmax + 0.8 , ymax - 5), **kw)
# ylim(1100, 1400)
# xlim(0, 2.2)
# legend(loc='lower left')
# grid(True)
# title( ispObj.desc )
# xlabel( 'O/F Ratio' )
# ylabel( 'Cstar (m/s)' )
# # savefig('cea_cstar_plot.png', dpi=120)
# # show()


# # PLOT: Isp vs eps
# ispArr = []
# isp_theo_Arr = []
# epsL = range(1,271,1)
# for eps in epsL:
#     ispArr.append( ispObj.get_IvacCstrTc_ThtMwGam(Pc=1160, MR=0.45, eps=eps)[0] )
#     isp_theo_Arr.append(ispObj.get_IvacCstrTc_ThtMwGam(Pc=1160, MR=0.571, eps=eps)[0])
# plot(epsL, ispArr, label='Pc=30 bar; O/F=0.45')
# plot(epsL, isp_theo_Arr, label='Pc=30 bar; O/F=0.571')
# plt.plot([22.7981, 22.7981], [150, 270], 'r--',label='Isp=270s, Ae/At=22.8')
# plt.plot([0, 22.7981],[270,270],'r--')
# plt.plot([262, 262], [150, 308], 'g--',label='Isp=308s, Ae/At=262')
# plt.plot([0, 262],[308.07, 308.07],'g--')
# ylim(150, 400)
# xlim(0, 270)
# legend(loc='best')
# grid(True)
# title( ispObj.desc )
# xlabel( 'Nozzle Expansion Area Ratio' )
# ylabel( 'Isp' )
# show()


# # CALCULATION: O/F ratio
# for mr in range(2,9):
#     print(mr, ispObj.get_Isp(Pc=435.113213, MR=mr, eps=262) )


# # CALCULATION: Throat Area (this is wrong!)
# print( ispObj.get_eps_at_PcOvPe(Pc=435.113213, MR=0.5, PcOvPe=435.113213/0.1015, frozen=1, frozenAtThroat=1) )


# # PLOT: C* vs chamber pressure at 0.5 O/F
# pcL = np.array( range(1,200,1) )  # bar
# pcL = pcL * 14.5037738  # psi
# cstarArr = []
# for Pc in pcL:
#     cstarArr.append( ispObj.get_Cstar(Pc=Pc, MR=0.5) * 0.3048 )
# pcL = pcL / 14.5037738  # bar
# plot(pcL, cstarArr, label='O/F=0.5')
# legend(loc='best')
# grid(True)
# title( ispObj.desc )
# xlabel( 'Chamber pressure (bar)' )
# ylabel( 'Cstar (m/s)' )
# show()



# New throat calculation
Thrust = 1400
Tt = 3209.04    # throat temperature
gamma = 1.1179    # specific heat ratio
Isp = 270       # specific impulse
g0 = 9.81       # standard gravity
Ve = Isp * g0    # exhaust velocity
R = (8.314462) / (44.01) * 1000
Pe = 650   # ambient pressure

m_dot = Thrust / Ve
Te = Tt - (gamma-1)/2 * (Ve**2)/(gamma*R)
Ma_e = Ve / np.sqrt(gamma * R * Te)
Pt = Pe * ( 1 + (gamma-1)/2 * Ma_e**2 )**(gamma/(gamma-1))
At = m_dot / ( Pt / np.sqrt(Tt) * np.sqrt(gamma/R) * ((gamma+1)/2)**(-(gamma+1)/(2*(gamma-1))) )

dt = np.sqrt(At/np.pi) * 2 * 1000
# print(m_dot, Te, Ma_e, Pt, At, dt)
# print( ispObj.getFrozen_PambCf(Pamb=0.000000000000000001, Pc=435.113, MR=0.55, eps=200, frozenAtThroat=0) )

# # DELETE
# PLOT: C* vs chamber pressure at 0.5 O/F
# MrL = range(0.01,0.99,0.01)
# MrL = np.array( range(1,100,1) ) / 100
# CfArr = []
# for Mr in MrL:
#     CfArr.append( ispObj.getFrozen_PambCf(Pamb=0.000001, Pc=500, MR=Mr, eps=700, frozenAtThroat=1)[0] )
# plot(MrL, CfArr, label='...')
# legend(loc='best')
# grid(True)
# title( ispObj.desc )
# xlabel( 'O/F ratio' )
# ylabel( 'Cf' )
# show()

# test!