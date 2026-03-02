class DimensionsError(Exception):
    pass


class EntryExitError(Exception):
    pass


def read_config():
    file = open('config.txt', "r")
    f = file.read()
    lst = f.split("\n")
    print(lst)
    values = []

    for element in lst:
        if '#' in element:
            continue
        values.append(element.split("=")[1])
    try:
        width, height = check_dimensions(values[0], values[1])
        check_entry(values[2], width, height)
        check_exit(values[3], width, height)
    except (DimensionsError, EntryExitError) as error:
        print(error)
    print(values)


def check_entry(entry, width, height):
    entry_splited = entry.split(",")
    if len(entry_splited) != 2:
        raise EntryExitError("Entry cordinates must be (x,y)")
    x_width = entry_splited[0]
    y_height = entry_splited[1]
    try:
        x = int(x_width)
    except ValueError:
        raise EntryExitError(f"The entry x must be a number: not {x_width}")

    try:
        y = int(y_height)
    except ValueError:
        raise EntryExitError(f"The entry y must be a number: not {y_height}")

    if x > width or x < 0:
        raise EntryExitError(f"The entery x can`t be : {x}"
              f"  => (max : {width}) and (min : 1)")
    if y > height or y < 0:
        raise EntryExitError(f"The entery y can`t be : {y}"
              f"  => (max : {height}) and (min : 1)")


def check_exit(exit, width, height):
    exit_splited = exit.split(",")
    if len(exit_splited) != 2:
        raise EntryExitError("Exit cordinates must be (x,y)")
    x_width = exit_splited[0]
    y_height = exit_splited[1]
    try:
        x = int(x_width)
    except ValueError:
        raise EntryExitError(f"The exit x must be a number: not {x_width}")

    try:
        y = int(y_height)
    except ValueError:
        raise EntryExitError(f"The exit y must be a number: not {y_height}")

    if x > width or x < 0:
        raise EntryExitError(f"The exit x can`t be : {x}"
              f"  => (max : {width}) and (min : 1)")
    if y > height or y < 0:
        raise EntryExitError(f"The exit y can`t be : {y}"
              f"  => (max : {height}) and (min : 1)")


def check_dimensions(w, h):
    try:
        width = int(w)
    except ValueError:
        raise DimensionsError(f"The width must be a number not: {w}")
    try:
        height = int(h)
    except ValueError:
        raise DimensionsError(f"The height must be a number not: {h})")

    if width > 200 or width < 1:
        raise DimensionsError(f"The width can`t be : {width}"
                              "  => (max : 200) and (min : 1)")
    elif height > 200 or height < 1:
        raise DimensionsError(f"The height can`t be : {height}"
                              " => (max : 200) and (min : 1)")
    return width, height

read_config()