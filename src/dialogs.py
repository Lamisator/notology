import sys

import urwid


class DialogExit(Exception):
    pass


class DialogDisplay:
    palette = [
        ('body','black','light gray', 'standout'),
        ('border','black','dark blue'),
        ('shadow','white','black'),
        ('selectable','black', 'dark cyan'),
        ('focus','white','dark blue','bold'),
        ('focustext','light gray','dark blue'),
        ]

    def __init__(self, text, height, width, body=None):
        width = int(width)
        if width <= 0:
            width = ('relative', 80)
        height = int(height)
        if height <= 0:
            height = ('relative', 80)

        self.body = body
        if body is None:
            # fill space with nothing
            body = urwid.Filler(urwid.Divider(),'top')

        self.frame = urwid.Frame( body, focus_part='footer')
        if text is not None:
            self.frame.header = urwid.Pile( [urwid.Text(text),
                urwid.Divider()] )
        w = self.frame

        # pad area around listbox
        w = urwid.Padding(w, ('fixed left',2), ('fixed right',2))
        w = urwid.Filler(w, ('fixed top',1), ('fixed bottom',1))
        w = urwid.AttrWrap(w, 'body')

        # "shadow" effect
        w = urwid.Columns( [w,('fixed', 2, urwid.AttrWrap(
            urwid.Filler(urwid.Text(('border','  ')), "top")
            ,'shadow'))])
        w = urwid.Frame( w, footer =
            urwid.AttrWrap(urwid.Text(('border','  ')),'shadow'))

        # outermost border area
        w = urwid.Padding(w, 'center', width )
        w = urwid.Filler(w, 'middle', height )
        w = urwid.AttrWrap( w, 'border' )

        self.view = w


    def add_buttons(self, buttons):
        l = []
        for name, exitcode in buttons:
            b = urwid.Button( name, self.button_press )
            b.exitcode = exitcode
            b = urwid.AttrWrap( b, 'selectable','focus' )
            l.append( b )
        self.buttons = urwid.GridFlow(l, 10, 3, 1, 'center')
        self.frame.footer = urwid.Pile( [ urwid.Divider(),
            self.buttons ], focus_item = 1)

    def button_press(self, button):
        raise DialogExit(button.exitcode)

    def main(self):
        self.loop = urwid.MainLoop(self.view, self.palette)
        try:
            self.loop.run()
        except DialogExit:
            return self.on_exit( e.args[0] )

    def on_exit(self, exitcode):
        return exitcode, ""




class InputDialogDisplay(DialogDisplay):
    def __init__(self, text, height, width):
        self.edit = urwid.Edit()
        body = urwid.ListBox([self.edit])
        body = urwid.AttrWrap(body, 'selectable','focustext')

        DialogDisplay.__init__(self, text, height, width, body)

        self.frame.set_focus('body')

    def unhandled_key(self, size, k):
        if k in ('up','page up'):
            self.frame.set_focus('body')
        if k in ('down','page down'):
            self.frame.set_focus('footer')
        if k == 'enter':
            # pass enter to the "ok" button
            self.frame.set_focus('footer')
            self.view.keypress( size, k )

    def on_exit(self, exitcode):
        return exitcode, self.edit.get_edit_text()

def do_inputbox(text, height, width):
    d = InputDialogDisplay( text, height, width )
    d.add_buttons([    ("Exit", 0) ])
    return d
