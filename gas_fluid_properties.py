
#this file is used to retrieve properties of both the combustion chamber gas and the regeneratively cooling fluid 
#based on temperature and pressure

import numpy as np
from rocketcea.cea_obj import CEA_Obj, add_new_fuel
import CoolProp.CoolProp as CP

def get_combustion_properties():  #EDIT TO ACCOUNT FOR CHANGES WITH EACH STAGE
    # Add LCO as a prop
    card_str = """
    fuel CO(L)  C 1.0   O 1.0     wt%=100.00
    h,j/mol=-110530
    """
    add_new_fuel( 'LCO', card_str )

    # General information
    Pc = 15     # chamber pressure [bar]
    MR = 0.55   # O/F ratio
    eps = 262   # Exit area / Throat area
    ispObj = CEA_Obj(propName='', oxName='LOX', fuelName='LCO')
    s = ispObj.get_full_cea_output( Pc=Pc, MR=MR, eps=eps, short_output=1, pc_units='bar', output='siunits')

    fac_CR = 55.16**2 / 18.52**2  # Chamber area / Throat area
    gamma = ispObj.get_Chamber_MolWt_gamma(Pc=Pc, MR=MR, eps=eps)[1] # specific heat ratio
    Mach = ispObj.get_Chamber_MachNumber(Pc=Pc, MR=MR, fac_CR=fac_CR) # Mach No. 
    cp, miu, k, Pr = ispObj.get_Chamber_Transport(Pc=Pc, MR=MR, eps=eps, frozen=0) # heat capacity, dynamics viscosity, thermal conductivity, Prandtl number

    # unit conversion
    cp = cp * 4186.8        # J/(KG)(K)
    miu  =  miu * 0.0001    # Pa·s
    k = k * 0.0000024       # W/(m)(K)
    
    return gamma, Mach, cp, miu, k, Pr


def get_CO_dynamic_visc(temp, stage): 
    #linearly interpolating data from https://webbook.nist.gov/cgi/fluid.cgi?P=15&TLow=100&THigh=200&TInc=1&Digits=5&ID=C630080&Action=Load&Type=IsoBar&TUnit=K&PUnit=bar&DUnit=kg%2Fm3&HUnit=kJ%2Fmol&WUnit=m%2Fs&VisUnit=Pa*s&STUnit=N%2Fm&RefState=DEF
    #coolprop unfortunately does not have viscocity model for CO

    if stage == 2: #calculations done at 15 bar for upper stage
        if isinstance(temp, (int, float)): #need this so that it accepts both ints/floats and arrays
            if temp>115:
                print('BOMBOCLART this bitch finna vapourise')
                exit()
        elif isinstance(temp, np.ndarray):
            if temp.any()>115:
                print('BOMBOCLART this bitch finna vapourise')
                exit()

        viscosity_values = np.array([
        9.4763e-05, 9.2101e-05, 8.9522e-05, 8.7028e-05, 8.4589e-05, 8.2232e-05, 7.9917e-05,
        7.7666e-05, 7.5465e-05, 7.3308e-05, 7.1191e-05, 6.9107e-05, 6.7052e-05, 6.5026e-05,
        6.3003e-05, 6.0995e-05
        ])
        temps = np.arange(100,116,1)    
    elif stage == 1:  #calculations done at 25 bar for lower stage
        print('havent coded this yet innit')      
        exit()
    else:
        print('Please enter a valid stage number (1 or 2)')    
        exit() 

    temp = np.round(temp) #round to nearest int to match with data 
    index = np.where(temps == temp)[0]
    mu = viscosity_values[index][0] #[Pa*s]
    return mu



def get_CO_conductivity(temp, stage): 
    #linearly interpolating data from https://webbook.nist.gov/cgi/fluid.cgi?P=15&TLow=100&THigh=200&TInc=1&Digits=5&ID=C630080&Action=Load&Type=IsoBar&TUnit=K&PUnit=bar&DUnit=kg%2Fm3&HUnit=kJ%2Fmol&WUnit=m%2Fs&VisUnit=Pa*s&STUnit=N%2Fm&RefState=DEF
    #coolprop unfortunately does not have viscocity model for CO

    if stage == 2: #calculations done at 15 bar for upper stage
        if isinstance(temp, (int, float)): #need this so that it accepts both ints/floats and arrays
            if temp>115:
                print('BOMBOCLART this bitch finna vapourise')
                exit()
        elif isinstance(temp, np.ndarray):
            if temp.any()>115:
                print('BOMBOCLART this bitch finna vapourise')
                exit()
        conductivity_values = np.array([
        0.10841, 0.10658, 0.10474, 0.10290, 0.10106, 0.099202, 0.097340, 
        0.095469, 0.093588, 0.091696, 0.089791, 0.087871, 0.085943, 0.083979,
        0.082001, 0.079997
        ])
        temps = np.arange(100,116,1)    
    elif stage == 1:  #calculations done at 25 bar for lower stage
        print('havent coded this yet innit')
        exit()      
    else:
        print('Please enter a valid stage number (1 or 2)')    
        exit() 
        
    temp = np.round(temp) #round to nearest int to match with data 
    index = np.where(temps == temp)[0]
    k = conductivity_values[index][0] #[W/m*k]
    return k

def get_fuel_properties(temp, pressure, substance, stage):
    cp = CP.PropsSI('C', 'T', temp, 'P', pressure, substance) #get the Cp in [J/kg/K]  #DOUBLE CHECK UNITS
    rho = CP.PropsSI('D', 'T', temp, 'P', pressure, substance) #get density in [kg/m^3]
    mu = CP.PropsSI('V', 'T', temp, 'P', pressure, substance) #get dynamic viscocity in [Pa-s] 
    k = CP.PropsSI('L', 'T', temp, 'P', pressure, substance) #get thermal conductivity in [W/m/K]
    # mu = get_CO_dynamic_visc(temp, stage) #get dynamic viscocity in [Pa-s] 
    # k = get_CO_conductivity(temp, stage) #get thermal conductivity in [kW/m/K]
    return cp, rho, mu, k
