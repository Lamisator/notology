from selectionDialog import SelectionDialog
import os


def openFileChoserDialog(title, path, preview = True):
    choices = list()
    file_list = list()

    for filename in os.listdir(path):
        fullpath = path + "/" + filename
        file_list.append(fullpath)
        with open(fullpath, "r") as fhandle:
            appendstring = ""
            if preview:
                line = fhandle.readline()
                line = line.rstrip()
                if len(line) > 20:
                    line = line[:17]
                    line += "..."
                appendstring += line + "\n("

            appendstring += filename

            if preview:
                appendstring += ")"

            choices.append(appendstring)

    choice = SelectionDialog(title, choices, 20).start()
    print(file_list[choice])
