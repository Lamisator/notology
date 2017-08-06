import urwid
import sys

class SelectionDialog(object):

    def menu(self, title, choices):
        body = [ urwid.Text(title, align = "center"), urwid.Divider()]
        '''headline = urwid.BigText("Notology", None)
        headline = urwid.Padding(headline)
        headline = urwid.Filler(headline, "bottom", None, 7)
        headline = urwid.BoxAdapter(headline, 7)
        body.append(headline)'''
        for c in choices:
            button = urwid.Button(c)
            urwid.connect_signal(button, 'click', self.item_chosen, c)
            body.append(urwid.AttrMap(button, None, focus_map='reversed'))
            body.append(urwid.Text("------"))
        return urwid.ListBox(urwid.SimpleFocusListWalker(body))

    def item_chosen(self, button, choice):
        self.choice = choice
        self.exit_program()

    def exit_program(self):
        raise urwid.ExitMainLoop()

    def __init__ (self, title, choices, width = 60, height = 60):
        self.choices = choices
        self.mainpd = urwid.Padding(self.menu(title, choices), left=1, right=1)
        self.top = urwid.Overlay(self.mainpd, urwid.SolidFill(u'\N{MEDIUM SHADE}'),
            align='center', width=('relative', 60),
            valign='middle', height=('relative', 60),
            min_width=20, min_height=9)

        bt = urwid.BigText("Notology.", urwid.font.HalfBlock5x4Font())
        bt = urwid.Padding(bt, "center", width = "clip")
        bt = urwid.Filler(bt, "bottom")
        bt = urwid.BoxAdapter(bt, height = 5)
        self.main_frame = urwid.Frame(self.top, header = bt)

    def start(self):
        urwid.MainLoop(self.main_frame, palette=[('reversed', 'standout', '')]).run()
        return self.choices.index(self.choice)
    
