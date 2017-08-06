import urwid
from lineWalker import LineWalker
import uuid
from time import sleep
import mainUI
import pdb

class EditorUI(object):

    def __init__(self, filename):

        assert open(filename, "a")

        self.filename = filename

        self.default_footer = urwid.AttrWrap(urwid.Text("<Alt + y> Save as |  <Alt + q> Close"), "standard")

        self.walker = LineWalker(filename)
        self.content = urwid.ListBox(self.walker)

        self.central_frame = urwid.Frame(self.content)
        self.central_frame.set_footer(self.default_footer)
        
        


    def open(self, loop = None, callback = None, quicknote = False):
        
        if quicknote:
            self.central_frame.set_header(urwid.AttrWrap(urwid.Text("Notology Quicknote\n" + self.filename, align = "center"), "header"))

        self.callback = callback
        self.palette = [("standard", "light blue", "black"),
                        ("warning", "yellow", "black"),
                        ("header", "black", "dark blue")]
        fresh = False
        if loop == None:
            self.loop = urwid.MainLoop(self.central_frame, self.palette, unhandled_input = self.keypress_handler)
            fresh = True
        else:
            loop.widget = self.central_frame
            loop.unhandled_input = self.keypress_handler
            loop.screen.register_palette(self.palette)
            loop.draw_screen()
            self.loop = loop

        if fresh:
            self.loop.run()
        return 0

    def keypress_handler(self, key):
        
        if key == "meta q":
            if not self.callback:
                raise urwid.ExitMainLoop()
            else:
                #mainUI.MainUI().open(self.loop)
                self.callback(self.loop)
                
        elif key == "meta y":
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
            w, pos = self.walker.get_focus()
            w, pos = self.walker.get_next(pos)
            if w:
                self.listbox.set_focus(pos, 'above')
                self.loop.process_input(["home"])
        elif key == "left":
            w, pos = self.walker.get_focus()
            w, pos = self.walker.get_prev(pos)
            if w:
                self.listbox.set_focus(pos, 'below')
                self.loop.process_input(["end"])
        else:
            return

        return True
    
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

