import numpy as np 

def get_diameter(x, stage): #returns the diameter for the engine section
    # x is the distance start from nozzle toward injector in [m]
    # total length of first stage is 0.55955 m
    # total length of second stage is 0.40369 m
    if stage == 1:
        if isinstance(x, (int, float)):
            x = 0.55955 - x #I added this since the code originally went injector to nozzle but I want other way round
            if 0.10036 >= x >= 0:           # chamber
                diameter = 0.05516                                                  # m
            elif 0.13965 >= x > 0.10036:    # chamber to throat
                diameter = 0.05516 - (0.05516 - 0.01852) * (x - 0.10036) / 0.03929  # m
            elif 0.55955 >= x > 0.13965:    # throat to exit
                diameter = 0.01852 + (0.2998 - 0.01852) * (x - 0.13965) / 0.4199    # m
            else:
                print('Out of the scope of the 1st stage engine')
                exit()
            return diameter
        elif isinstance(x, np.ndarray):
            diameters = []
            for element in x:
                element = 0.55955 - element #I added this since the code originally went injector to nozzle but I want other way round
                if 0.10036 >= element >= 0:           # chamber
                    diameter = 0.05516                                                  # m
                elif 0.13965 >= element > 0.10036:    # chamber to throat
                    diameter = 0.05516 - (0.05516 - 0.01852) * (element - 0.10036) / 0.03929  # m
                elif 0.55955 >= element > 0.13965:    # throat to exit
                    diameter = 0.01852 + (0.2998 - 0.01852) * (element - 0.13965) / 0.4199    # m
                else:
                    print('Out of the scope of the 1st stage engine')
                    exit()
                diameters.append(diameter)
            diameters = np.array(diameters)
            return diameters
    elif stage == 2:
        if isinstance(x, (int, float)):
            x = 0.40369 - x
            if 0.08349 >= x >= 0:           # chamber
                diameter = 0.04125                                                  # m
            elif 0.11739 >= x > 0.08349:    # chamber to throat
                diameter = 0.04125 - (0.04125 - 0.01263) * (x - 0.08349) / 0.0339  # m
            elif 0.40369 >= x > 0.11739:    # throat to exit
                diameter = 0.01263 + (0.2045 - 0.01263) * (x - 0.11739) / 0.2863    # m
            else:
                print('Out of the scope of the 2nd stage engine')
                exit()
            return diameter
        elif isinstance(x, np.ndarray):
            diameters = []
            for element in x:
                element = 0.40369 - element
                if 0.08349 >= element >= 0:           # chamber
                    diameter = 0.04125                                                  # m
                elif 0.11739 >= element > 0.08349:    # chamber to throat
                    diameter = 0.04125 - (0.04125 - 0.01263) * (element - 0.08349) / 0.0339  # m
                elif 0.40369 >= element > 0.11739:    # throat to exit
                    diameter = 0.01263 + (0.2045 - 0.01263) * (element - 0.11739) / 0.2863    # m
                else:
                    print('Out of the scope of the 2nd stage engine')
                    exit()
                diameters.append(diameter)
            diameters = np.array(diameters)
            return diameters

def get_cooling_channel_length(stage, channel_gap): #this is rough asf broski deal with it 
    distance = 0 #distance traveled length wise along engine 
    tot_length = 0 #total length of cooling channel 
    if stage == 1: 
        while distance <= 0.55955:
            tot_length += get_diameter(distance, stage)
            distance += channel_gap
    elif stage == 2:
        while distance <= 0.40369:
            tot_length += get_diameter(distance, stage)
            distance += channel_gap 
    #tot_length *= 0.5 #I'm pretty sure I gotta do this cuz of the way the channel spirals and isn't just a series of circles 

    return tot_length

def get_diameter_from_distance_along_channel(length_fraction, total_engine_length, stage): #seems stupid but basically from the nodes we have the distance along the cooling channel and that needs to be converted to a local diameter
    #this function is skuffed as fuck 
    #I literally don't CARE 
    #it is technically better than nothing (I think)
    #if you have feedback redirect it to NO ONE 
    # <3 
    correction_factor = 0.9 #pls ask me (dominic) why this is here, don't want to write an ugly explanation paragraph here
    reference_length = length_fraction*correction_factor*total_engine_length
    diameter = get_diameter(reference_length, stage)
    return diameter
