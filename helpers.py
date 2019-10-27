import math

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

def calculate_pages(total):
    pages = math.floor(total / 100) + 1

    print(pages)
    return pages

def prompt_for_pages(pages):
    print("Each page = 1 Query Credit")
    page_number = get_prompt("Enter Maximum Page Number: ")

    return page_number



if __name__ == '__main__':
    prompt_for_pages(calculate_pages(3836))
