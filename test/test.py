def is_between(target, start, end, including_start=False, including_end=False):
    if including_start == False and including_end == False:
        print("Not including anything")
    elif including_start == True and including_end == True:
        print("Included start and end")
    elif including_start == True and including_end == False:
        print("Included start but NOT end")
    elif not including_start and including_end:
        print("Included end but NOT start")

if __name__ == '__main__':
    is_between(5, 1, 7, including_start=False, including_end=False)
    is_between(5, 1, 7, including_start=True, including_end=True)
    is_between(5, 1, 7, including_start=True, including_end=False)
    is_between(5, 1, 7, including_start=False, including_end=True)