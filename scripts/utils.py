def get_model_size_cat(params):
    if params == 0.0:
        return 'other'
    elif params <= 2.0:
        return "1B"
    elif params <= 4.0:
        return "3B"
    elif params <= 6.5:
        return "6B"
    elif params <= 8.0:
        return "7B"
    elif params <= 14.5:
        return "13B"
    elif params <= 17.0:
        return "16B"
    elif params <= 25.0:
        return "20B"
    elif params <= 35.0:
        return "30B"
    elif params <= 45.0:
        return "40B"
    elif params <= 66.0:
        return "65B"
    elif params <= 75.0:
        return "70B"
    elif params <= 190.0:
        return "180B"
    else:
        raise Exception("Param too big")