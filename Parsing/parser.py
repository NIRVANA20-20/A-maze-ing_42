import sys
import os


class DimensionsError(Exception):
    pass


class FileNameError(Exception):
    pass


class PerfectWayError(Exception):
    pass


class EntryExitError(Exception):
    pass


class Parser:
    def __init__(self):
        self.file_elements = [
            "WIDTH",
            "OUTPUT_FILE",
            "HEIGHT",
            "SEED",
            "ENTRY",
            "EXIT",
            "PERFECT",
        ]
        self.args_checker()
        self.read_config()

    def args_checker(self):
        args = sys.argv
        if len(args) != 2 or args[1] != "config.txt":
            print(
                "Error = You must run the program: python3 amazing.py config.txt",
                "\n PRESS [Control] key to exit",
            )
            exit(0)

    def read_config(self):
        file = open("config.txt", "r")
        f = file.read()
        lst = f.split("\n")
        values = []

        for element in lst:
            if "#" in element:
                continue
            if element.split("=")[0] in self.file_elements:
                values.append(element.split("=")[1])
        if len(values) != 7:
            print("One of the arguments in (config.txt) is missing")
            sys.exit(0)
        try:
            self.check_dimensions(values[0], values[1])
            self.check_entry(values[2])
            self.check_exit(values[3])
            self.check_file(values[4])
            self.check_seed(values[6])
            self.check_perfect(values[5])

        except Exception as error:
            print(error)
            sys.exit(0)

    def check_seed(self, seed):
        if not seed:
            self.seed = None
            return
        elif int(seed) < 0:
            raise ValueError("The seed must be number (positive)", file=sys.stderr)
        self.seed = int(seed)

    def check_perfect(self, answer):
        if answer == "True":
            self.perfect = True
        elif answer == "False":
            self.perfect = False
        else:
            raise PerfectWayError(
                "PERFECT = (the answer should be " "'True' or 'False') "
            )

    def check_file(self, file_name):
        file_checker = file_name.split(".")
        if len(file_checker) != 2 or file_checker[1] != "txt":
            raise FileNameError("only '.txt' files are permitted as maze output file")
        if os.path.exists(file_name) and not os.access(file_name, os.W_OK):
            raise FileNameError(f"OUTPUT_FILE '{file_name}' is not writable")
        parent = os.path.dirname(file_name) or "."
        if not os.access(parent, os.W_OK):
            raise ValueError(f"OUTPUT_FILE '{file_name}' directory is not writable")
        else:
            self.file_name = file_name

    def check_entry(self, entry):
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

        if x > self.width or x < 0:
            raise EntryExitError(
                f"The entery x can't be : {x}"
                f"  => (max : {self.width})"
                "and (min : 1)"
            )
        if y > self.height or y < 0:
            raise EntryExitError(
                f"The entery y can't be : {y}"
                f"  => (max : {self.height})"
                " and (min : 1)"
            )
        self.entry = (x, y)

    def check_exit(self, exit):
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

        if x > self.width or x < 0:
            raise EntryExitError(
                f"The exit x can't be : {x}" f" => (max : {self.width}) and (min : 1)"
            )
        if y > self.height or y < 0:
            raise EntryExitError(
                f"The exit y can't be : {y}"
                f"  => "
                f"(max : {self.height}) and (min : 1)"
            )
        self.exit = (x, y)

    def check_dimensions(self, w, h):
        try:
            self.width = int(w)
        except ValueError:
            raise DimensionsError(f"The width must be a number not: {w}")
        try:
            self.height = int(h)
        except ValueError:
            raise DimensionsError(f"The height must be a number not: {h})")

        if self.width > 1200 or self.width < 1:
            raise DimensionsError(
                f"The width can`t be : {self.width}" "  => (max : 200) and (min : 1)"
            )
        elif self.height > 1200 or self.height < 1:
            raise DimensionsError(
                f"The height can`t be : {self.height}" " => (max : 200) and (min : 1)"
            )

    # TODO: just for test remember to parse if from config file
    def set_perfect(self):
        self.perfect = True
