import numpy as np
from rocketcea.cea_obj import CEA_Obj, add_new_fuel
import gas_fluid_properties
import CoolProp.CoolProp as CP
import prop_dimension

CO = 'CarbonMonoxide'
O2 = 'OXYGEN'
#start of array is at nozzle exit, end of array is at injector, this way it follows the flow of fuel

#############################
#______input parameters_____#
#############################

#general 
stage = 2 #enter 1 for first stage engine, 2 for second stage engine
burn_time = 200 #[s]

#geometry/wall
D_f = 0.008 #diameter of fuel coolant channels [m]
t = 0.003 #thickness of engine between combustion and cooling channel [m] 
l_engine = 0.40369 #total length of engine [m]
channel_gap = 0.02  #[m] - gap between cooling channel loops
l_tot = prop_dimension.get_cooling_channel_length(stage, channel_gap) #total length of cooling channel [m]
n_nodes = 100 #number of different nodes the channel is split into for simulation [-]
k_wall = 6.5 #thermal conductivity of wall [W/m*K] https://www.azom.com/article.aspx?ArticleID=4459
rho_wall = 8220 #[kg/m^3] - density of material used for chamber wall
c_wall = 435 #[J/kg*K] - specific heat of wall material https://www.matweb.com/search/datasheet_print.aspx?matguid=94950a2d209040a09b89952d45086134
unit_length = l_tot/n_nodes #[m] #CHANGE THIS LATER 
unit_width = D_f #used for getting the area of a node for heat transfer [m]
unit_area = unit_length*unit_width #[m^2] #this is area for heat transfer, not cross sectional area of cooling channel
unit_mass_wall = unit_area*t*rho_wall/2 #mass per node of wall used to calculate temp increase, /2 because there are 2 nodes: left and right

#set up array of diameter values
D_c = np.linspace(0, 1, n_nodes)
D_c = prop_dimension.get_diameter_from_distance_along_channel(D_c, l_engine, stage)

#thermal/fluid
T_c = 3300 #combustion temperature [K] #IMPORT FROM PREV FILE?
T_wall0 = 293 #initial wall temperature [K]
T_f0 = 100 #initial fuel temperature [K]
gamma_c, mach_c, Cp_c, mu_c, k_c, Pr_c = gas_fluid_properties.get_combustion_properties() #fetch properties of gas in combustion chamber 
r = Pr_c**(1/3) #EDIT LATER TO DIFFERENCIATE COMBUSTION CHAMBER AND THROAT 
T_aw = T_c*(1 + r*0.5*(gamma_c-1)*(mach_c**2)) #ablative wall temperature [K] (accounts for fluid slowing down near wall)
mdot_c = 0.529 #total mass flow [kg/s] (from SSOT)
OF = 0.5714 #O/F ratio [-] taken from SSOT
mdot_f = mdot_c/(OF + 1) #mass flow of fuel [kg/s]  #CHECK IF CORRECT 
eta_c = 0.92 #combustion efficiency [-] #from sparrow paper, perform sensitivity analysis later 
unit_mass_fluid = unit_length*np.pi*((0.5*D_f)**2)*gas_fluid_properties.get_fuel_properties(T_f0, 1500000, O2, 2)[1] #[kg], we'll just assume constant density throughout the process for the unit mass

dt = unit_mass_fluid/mdot_f #maybe I'm stupid but I do this so that in one time step 1 unit mass shifts from 1 node to the next so that all the properties can like shift down the array 

#############################
#Define other functions
#############################

def get_fuel_convectivity(temp, pressure, substance, stage): #returns convective heat transfer coefficient for fuel 
    cp, rho, mu, k = gas_fluid_properties.get_fuel_properties(temp, pressure, substance, stage)
    velocity = mdot_c/(rho*np.pi*((0.5*D_f)**2)) #get velocity from mass flow, density and area 
    Re = (rho*velocity*D_f/mu) #calculate reynolds number 
    Pr = (mu*cp)/k #calculate stationary prandtl number 
    Pr = 0.75 + 1.63/(np.log10(1 + Pr/0.0015)) #correct prandtl number for turbulence
    Nu = 0.023*(Re**0.8)*(Pr**0.4) #Nusselt number
    h_alpha = (k*Nu)/D_f #convective heat transfer coefficient [W/m^2*K]
    return h_alpha 

def get_gas_convectivity(T_left):  #returns convective heat transfer coefficient for combustion gas
    T_hg = T_c + 0.8*(T_c*(eta_c**2) - T_c) #calculate 'hot gas temperature' as specified in method #DOUBLE CHECK 
    h_alpha = 0.01975*(((k_c**0.18)*((mdot_c*Cp_c)**0.82))/(D_c**1.82))*((T_hg/T_c)**0.35) #convective heat transfer coefficient [W/m^2*K]
    return h_alpha

def get_convective_heat_transfer(T_hot, T_cold, coefficient): #returns heat transfer [W] due to convection process
    return coefficient*(T_hot-T_cold)*unit_area

def get_conductive_heat_transfer(T_hot, T_cold): #returns heat transfer [W] due to conductive process
    return (k_wall*(T_hot - T_cold)*unit_area)/t 

def get_delta_T(Q, m, c):
    delta_T = (Q*dt)/(m*c)
    return delta_T


def get_temp_changes(T_left, T_right, T_fuel):
    #calculate all the heat transfers  
    h_alpha_hot = get_gas_convectivity(T_left) #convectivity between combustion chamber and wall 
    h_alpha_cold = get_fuel_convectivity(T_fuel, 1500000, O2, 2) #convectivity between fuel and wall 
    Q_convection_hot = get_convective_heat_transfer(T_aw, T_left, h_alpha_hot) #heat transfered [W] between wall and comubstion gas
    Q_convection_cold = get_convective_heat_transfer(T_right, T_fuel, h_alpha_cold) #heat transfered [W] between wall and fuel
    Q_conduction = get_conductive_heat_transfer(T_left, T_right)

    #work out net heat added/lost for each node 
    dQ_left = Q_convection_hot - Q_conduction  #left wall of chamber gains heat via convection from combustio and loses it via conduction to other side of wall 
    dQ_right = Q_conduction - Q_convection_cold #right wall gains heat via conduction from left wall and loses it via convection with fuel 
    dQ_fuel = Q_convection_cold #fuel gains heat via convection with wall

    #then work out the temperature changes 
    delta_T_left = get_delta_T(dQ_left, unit_mass_wall, c_wall)
    delta_T_right = get_delta_T(dQ_right, unit_mass_wall, c_wall)

    c_fuel = gas_fluid_properties.get_fuel_properties(T_fuel, 1500000, O2, 2)[0] #need specific heat of fuel to work out temp rise
    delta_T_fuel = get_delta_T(dQ_fuel, unit_mass_fluid, c_fuel)

    return delta_T_left, delta_T_right, delta_T_fuel

def shift_array(arr): #use to shift the array of fluid temperatures to show how the mass flows 
    shifted_arr = np.empty_like(arr)
    shifted_arr[0] = T_f0 #assume new fluid at the initial fluid temperature flows into the cooling channel
    shifted_arr[1:] = arr[:-1]
    return shifted_arr

def simulate():

    #setup initial arrays
    T_L = T_wall0*np.ones(n_nodes) #temperature of nodes representing left side of wall (next to combustion chamber)
    T_R = T_wall0*np.ones(n_nodes) #temperature of nodes representing right side of wall (next to cooling channel)
    T_f = T_f0*np.ones(n_nodes) #temperature of nodes representing fluid in cooling channel 
    time = 0
    counter = 0

    #simulation loop
    while time < burn_time:
        dT_L, dT_R, dT_f = get_temp_changes(T_L, T_R, T_f) #calculate all the stuff and change the temperatures accordingly
        T_L += dT_L
        T_R += dT_R 
        T_f += dT_f
        T_f = shift_array(T_f) #shift the fluid temperature array since the fluid flows innit
        time += dt
        counter += 1 
        if counter%300 == 0:
            print(f"time = {time}")
            print(f"average fluid temp = {np.mean(T_f)}")
            print(f"average hot wall temp = {np.mean(T_L)}")
    
    return T_L, T_R, T_f 

def main():
    T_L_final, T_R_final, T_f_final = simulate()
    print(T_L_final)


#############################
#run it
#############################

if __name__ == "__main__":
    main()
















