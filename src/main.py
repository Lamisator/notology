#!/usr/bin/env python3

import mainUI
import getopt
from uuid import uuid4
import editorUI
import urwid
import sys
import os

def new_quicknote():
    path = os.path.expanduser("~") + "/.notology/quicknotes/" 
    filename = path + str(uuid4()) + ".txt" 
    if not os.path.exists(path):
        os.makedirs(path)

    editorUI.EditorUI(filename).open(quicknote = True)

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "q", ["quicknote"])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err)
        sys.exit(2)
    if not opts:
        mainUI.MainUI().open()
    
    for o, a in opts:
        if o in ("-q", "--quicknote"):
            print("New quicknote")
            new_quicknote()
        else:
            assert False, "unhandled option"
    #print(mainUI.MainUI().open())
if __name__ == "__main__":
    main()
