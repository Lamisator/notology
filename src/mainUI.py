from __future__ import print_function
import urwid
import popup
import editorUI
import os
from uuid import uuid4
import sys
import time
import datetime

# See https://stackoverflow.com/questions/5574702/how-to-print-to-stderr-in-python
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)



class MainUI(object):

    
    def main_menu(self):
        choices = ("Open Note", "Quick Note", "About", "Exit")
        mainpd = urwid.Padding(self.menu("Main Menu", choices, self.main_menu_item_chosen), left=1, right=1)
        top = urwid.Overlay(mainpd, urwid.SolidFill(u'\N{MEDIUM SHADE}'),
        align='center', width=('relative', 60),
        valign='middle', height=('relative', 60),
        min_width=20, min_height=9)

        main_frame = urwid.Frame(top, header = self.header)
        self.mainloop.widget = main_frame


    def menu(self, title, choices, callback):
        body = [ urwid.Text(title, align = "center"), urwid.Divider()]
        for c in choices:
            button = urwid.Button(c)
            urwid.connect_signal(button, 'click', callback, c)
            body.append(urwid.AttrMap(button, None, focus_map='reversed'))
            body.append(urwid.Text("------"))
        return urwid.ListBox(urwid.SimpleFocusListWalker(body))

    def file_menu(self, path, preview = True):
        choices = list()
        file_list = list()
        file_path_lookup = dict()

        # How long each entry should be at most, before we cut its tail off
        max_len = 50

        for filename in os.listdir(path):
            fullpath = path + "/" + filename
            file_list.append(filename)
            file_path_lookup[filename] = fullpath
            with open(fullpath, "r") as fhandle:

                # Get creation timei
                timestamp = time.localtime(os.path.getctime(fullpath))
                appendstring = time.strftime("%a %b %d %H:%M:%S %Y", timestamp) + "\n"
                if preview:
                    line = fhandle.readline()
                    line = line.rstrip()
                    if len(line) > max_len:
                        line = line[:(max_len - 3)]
                        line += "..."
                    appendstring += line + "\n("

                appendstring += filename

                if preview:
                    appendstring += ")"

                choices.append(appendstring)
        self.file_list = file_list
        self.file_path_lookup = file_path_lookup

        mainpd = urwid.Padding(self.menu("Select a file\n" + path, choices, self.file_menu_item_chosen), left=1, right=1)
        top = urwid.Overlay(mainpd, urwid.SolidFill(u'\N{MEDIUM SHADE}'),
        align='center', width=('relative', 60),
        valign='middle', height=('relative', 60),
        min_width=20, min_height=100)

        main_frame = urwid.Frame(top, header = self.header)
        self.mainloop.widget = main_frame

    def file_menu_item_chosen(self, button, choice):
        for filename in self.file_list:
            if filename in choice:
                eprint("TRUE")
                editorUI.EditorUI(self.file_path_lookup[filename]).open(self.mainloop, callback = self.open)

    def main_menu_item_chosen(self, button, choice):
        self.choice = choice

        if choice == "Open Note":
            self.file_menu(self.default_dir + "quicknotes")

        if choice == "Quick Note":
            editorUI.EditorUI(self.default_dir + "quicknotes/" + str(uuid4()) + ".txt").open(self.mainloop, callback = self.open)

        if choice == "Exit":
            self.exit_program()


    def exit_program(self):
        raise urwid.ExitMainLoop()


    def keypress_handler(self, key):

        if key == "esc":
            self.main_menu()

    def __init__ (self):
        eprint("Initialized.")
        bt = urwid.AttrWrap(urwid.BigText("Notology.", urwid.font.HalfBlock5x4Font()), "standard")
        bt = urwid.Padding(bt, "center", width = "clip")
        bt = urwid.AttrWrap(urwid.Filler(bt, "bottom"), "standard")
        bt = urwid.BoxAdapter(bt, height = 5)
        self.header = bt

        self.default_dir = os.path.expanduser("~") + "/.notology/"
    def open(self, loop = None):
        fresh = False
        if loop == None:
            fresh = True
            self.mainloop = urwid.MainLoop(None)
        else:
            self.mainloop = loop

        #self.mainloop = urwid.MainLoop(self.main_frame, palette=[('reversed', 'standout', '')])
        self.mainloop.screen.register_palette([("reversed", "standout", ""),
                                        ("standard", "black", "dark blue")])
        self.mainloop.unhandled_input = self.keypress_handler
        self.main_menu()
        if fresh:
            self.mainloop.run()
