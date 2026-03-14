class DimensionsError(Exception):
    pass


class FileNameError(Exception):
    pass


class PerfectWayError(Exception):
    pass


class EntryExitError(Exception):
    pass


def read_config():
    file = open("config.txt", "r")
    f = file.read()
    lst = f.split("\n")
    print(lst)
    values = []

    file_elements = ["WIDTH",
                     "OUTPUT_FILE",
                     "HEIGHT",
                     "ENTRY",
                     "EXIT",
                     "PERFECT"]

    for element in lst:
        if "#" in element:
            continue
        if element.split("=")[0] in file_elements:
            values.append(element.split("=")[1])

    try:
        height, width = check_dimensions(values[0], values[1])
        x_entry, y_entry = check_entry(values[2], width, height)
        x_exit, y_exit = check_exit(values[3], width, height)
        file_name = check_file(values[4])
        check_perfect(values[5])

        return width, height, (x_entry, y_entry), (x_exit, y_exit), file_name
    except (DimensionsError,
            EntryExitError,
            FileNameError,
            PerfectWayError) as error:
        print(error)


def check_perfect(answer):
    if answer == "True":
        pass  ############## put the perfect way
    elif answer == "False":
        pass  ##############    put the unperfect way
    else:
        raise PerfectWayError("PERFECT = (the answer should be "
                              "'True' or 'False') ")


def check_file(file_name):
    if len(file_name) > 0:
        return file_name
    else:
        raise FileNameError("File name cant be empty")


def check_entry(entry, width, height):
    entr = entry.replace("(", "").replace(")", "")
    entry_splited = entr.split(",")
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
        raise EntryExitError(
            f"The entery x can't be : {x}" f"  => (max : {width})"
            "and (min : 1)")
    if y > height or y < 0:
        raise EntryExitError(
            f"The entery y can't be : {y}" f"  => (max : {height})"
            " and (min : 1)")
    return x, y


def check_exit(exit, width, height):
    exit = exit.replace("(", "").replace(")", "")
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
        raise EntryExitError(
            f"The exit x can't be : {x}" f"  => (max : {width}) and (min : 1)"
        )
    if y > height or y < 0:
        raise EntryExitError(
            f"The exit y can't be : {y}" f"  => (max : {height}) and (min : 1)"
            )
    return x, y


def check_dimensions(w, h):
    try:
        width = int(w)
    except ValueError:
        raise DimensionsError(f"The width must be a number not: {w}")
    try:
        height = int(h)
    except ValueError:
        raise DimensionsError(f"The height must be a number not: {h})")

    if width > 1200 or width < 1:
        raise DimensionsError(
            f"The width can`t be : {width}" "  => (max : 200) and (min : 1)"
        )
    elif height > 1200 or height < 1:
        raise DimensionsError(
            f"The height can`t be : {height}" " => (max : 200) and (min : 1)"
        )
    return width, height
