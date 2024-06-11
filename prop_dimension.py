def get_diameter(x, stage): #returns the diameter for the engine section
    # x is the distance start from injector toward nozzle in [m]
    # total length of first stage is 0.55955 m
    # total length of second stage is 0.40369 m
    if stage == 1:
        if 0.10036 >= x >= 0:           # chamber
            diameter = 0.05516                                                  # m
        elif 0.13965 >= x > 0.10036:    # chamber to throat
            diameter = 0.05516 - (0.05516 - 0.01852) * (x - 0.10036) / 0.03929  # m
        elif 0.55955 >= x > 0.13965:    # throat to exit
            diameter = 0.01852 + (0.2998 - 0.01852) * (x - 0.13965) / 0.4199    # m
        else:
            print('Out of the scope of the 1st stage engine')
            exit()
    elif stage == 2:
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