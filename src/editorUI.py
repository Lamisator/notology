import uuid
from time import sleep

import urwid

import mainUI
from lineWalker import LineWalker

class EditorUI(object):

    def __init__(self, filename):

        assert open(filename, "a")

        self.filename = filename

        # Default footer, showing possible key sequences
        self.default_footer = urwid.AttrWrap(urwid.Text("<Alt + y> Save as |  <Alt + q> Close"), "standard")
        
        # Text field for new filemes. Defining it here and seperately, so we may access it later
        self.filename_field = urwid.Edit("Enter new filename: ")

        # Footer shown during filename selection
        self.filename_footer = urwid.AttrWrap(self.filename_field, "filename")

        # Defining view components
        self.walker = LineWalker(filename)
        self.content = urwid.ListBox(self.walker)

        self.central_frame = urwid.Frame(self.content)
        self.central_frame.set_footer(self.default_footer)
        
        


    def open(self, loop = None, callback = None, quicknote = False):
        



        # If we are edting a (new) quicknote, show this header
        if quicknote:
            self.central_frame.set_header(urwid.AttrWrap(urwid.Text("Notology Quicknote\n" + self.filename, align = "center"), "header"))

        # Remember the callback function (if any) we got, so we may return to the last view, once we have finished our editing
        self.callback = callback


        self.palette = [("standard", "light blue", "black"),
                        ("warning", "yellow", "black"),
                        ("header", "black", "dark blue")]
        
        # Check if the UI is fresh by checking if a loop has been passed. If not, create a new one, otherwise use the existing one
        fresh = False
        if loop == None:
            self.loop = urwid.MainLoop(self.central_frame, self.palette, unhandled_input = self.keypress_handler)
            fresh = True
        else:
            # Update the existing loop with the attributes we would otherwise have set in the above constructor
            loop.widget = self.central_frame
            
            loop.unhandled_input = self.keypress_handler
            # We can't just do loop.palette = [...]! We have to 'register' our local palette. 
            loop.screen.register_palette(self.palette)

            # This is our new loop! Remember it 
            self.loop = loop

            # Use our new loop to redraw the screen, as it is running already
            self.loop.draw_screen()

        if fresh:
            # If this loop is new, we have to start it first. Duh!
            self.loop.run()
        return 0

    def keypress_handler(self, key):
        # What we're gonna do, if we encounter any keystrokes

        if key == "meta q":    
            # Quit the editor. If we have no callback function, exit the main loop and thus quit the program. Else, call the callback function and "go back"
            if not self.callback:
                self.exit_program()
            else:
                self.callback(self.loop)
        
        elif key == "meta y":
            # Save the file
            self.save(self.filename, verbose = True)
    
        
        elif key == "delete":
            # delete at end of line
            self.walker.combine_focus_with_next()

        elif key == "backspace":
            # backspace at beginning of line
            self.walker.combine_focus_with_prev()

        elif key == "enter":
            # start new line
            self.walker.split_focus()
            # move the cursor to the new line and reset pref_col
            self.loop.process_input(["down", "home"])
        elif key == "right":
            # Check if there is a char right to the cursor, if yes, move there
            w, pos = self.walker.get_focus()
            w, pos = self.walker.get_next(pos)
            if w:
                self.listbox.set_focus(pos, 'above')
                self.loop.process_input(["home"])

        elif key == "left":
            # Check if there is a char left to the cursor, if yes, move there
            w, pos = self.walker.get_focus()
            w, pos = self.walker.get_prev(pos)
            if w:
                self.listbox.set_focus(pos, 'below')
                self.loop.process_input(["end"])

        else:
            # Everything else is fine as well
            return

        return True
    


    def keypress_handler_filename(self, key):
        # A dedicated keypress handler for the filename text field

        if key == "enter":
            # If return is hit, we are finished here
            self.filename = self.filename_field.get_edit_text()

    def save(self, save_filename, verbose = False):
        walker = self.walker
        lines = []

        for edit in walker.lines:
            if edit.original_text.expandtabs() == edit.edit_text:
                lines.append(edit.original_text)
            else:
                lines.append(re_tab(edit.edit_text))

        while walker.file is not None:
            lines.append(walker.read_next_line())
        #pdb.set_trace()
        file_handle = open(save_filename, "w")


        prefix = ""
        for line in lines:
            file_handle.write(prefix + line)
            prefix = "\n"

        if verbose:
            self.central_frame.footer = urwid.AttrWrap(urwid.Text(save_filename + " saved."), "warning")
            self.loop.draw_screen()
            sleep(2)
            self.central_frame.footer = self.default_footer


    def exit_program(self):

        # Exit this program
        raise urwid.ExitMainLoop()

def re_tab(s):
    """Return a tabbed string from an expanded one."""
    l = []
    p = 0
    for i in range(8, len(s), 8):
        if s[i-2:i] == "  ":
            # collapse two or more spaces into a tab
            l.append( s[p:i].rstrip() + "\t" )
            p = i

    if p == 0:
        return s
    else:
        l.append(s[p:])
        return "".join(l)

