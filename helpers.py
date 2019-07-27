def get_prompt(string=None):
    if string is not None:
        cmd = input("\nDALEK ({}) >>> ".format(string))
    else:
        cmd = input("\nDALEK >>> ")
    return cmd

def print_options(list, api_key):
    for item in list:
        print(item)
    return
