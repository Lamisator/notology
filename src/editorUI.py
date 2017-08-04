import urwid
from lineWalker import LineWalker
import uuid


class EditorUI(object):

    def __init__(self, filename):

        assert open(filename, "a")

        self.filename = filename

        self.footer = urwid.AttrWrap(urwid.Text("<Alt + s> Save as |  <Alt + q> Close"), "standard")

        self.walker = LineWalker(filename)
        self.content = urwid.ListBox(self.walker)

        self.central_frame = urwid.Frame(self.content)
        self.central_frame.set_footer(self.footer)
        
        


    def main(self): 
        self.palette = [("standard", "light blue", "black"),
                        ("warning", "yellow", "black")]
        self.loop = urwid.MainLoop(self.central_frame, self.palette, unhandled_input = self.keypress_handler)
        self.loop.run()

    def keypress_handler(self, key):
        
        if key == "meta q":
            raise urwid.ExitMainLoop()

        elif key == "meta s":
            self.save(self.filename)


    def save(self, save_filename):
        walker = self.walker

        lines = []

        while walker.file is not None:
            lines.append(walker.read_next_line())

        file_handle = open(save_filename, "w")


        prefix = ""
        for line in lines:
            file_handle.write(line)
            prefix = "\n"
