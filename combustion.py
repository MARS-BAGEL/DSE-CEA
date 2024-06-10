
import numpy as np
from rocketcea.cea_obj import CEA_Obj, add_new_fuel
import CoolProp.CoolProp as CP

def get_combustion_properties():
    # Add LCO as a prop
    card_str = """
    fuel CO(L)  C 1.0   O 1.0     wt%=100.00
    h,j/mol=-110530
    """
    add_new_fuel( 'LCO', card_str )

    # General information
    Pc = 25     # chamber pressure [bar]
    MR = 0.55   # O/F ratio
    eps = 262   # Exit area / Throat area
    ispObj = CEA_Obj(propName='', oxName='LOX', fuelName='LCO')
    s = ispObj.get_full_cea_output( Pc=Pc, MR=MR, eps=eps, short_output=1, pc_units='bar', output='siunits')

    fac_CR = 55.16**2 / 18.52**2  # Chamber area / Throat area
    gamma = ispObj.get_Chamber_MolWt_gamma(Pc=Pc, MR=MR, eps=eps)[1] # specific heat ratio
    Mach = ispObj.get_Chamber_MachNumber(Pc=Pc, MR=MR, fac_CR=fac_CR) # Mach No. 
    cp, miu, k, Pr = ispObj.get_Chamber_Transport(Pc=Pc, MR=MR, eps=eps, frozen=0) # heat capacity, viscosity, thermal conductivity, Prandtl number

    return gamma, Mach, cp, miu, k, Pr 