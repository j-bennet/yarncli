from __future__ import print_function, unicode_literals 

from prompt_toolkit.application import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.key_binding.bindings.focus import focus_next, focus_previous
from prompt_toolkit.layout.containers import VSplit, HSplit, Window
from prompt_toolkit.layout.widgets import Button, Box, Label, Frame, TextArea
from prompt_toolkit.layout.layout import Layout

from collections import namedtuple

YarnApp = namedtuple('YarnApp', ['id', 'name', 'progress', 'state'])

apps = [
    YarnApp('xxx', 'job-1', '100', 'FINISHED'),
    YarnApp('yyy', 'job-2', '10', 'RUNNING'),
    YarnApp('zzz', 'job-3', '70', 'FAILED')
]

text_area = TextArea(focussable=True)

def button_clicked():
    text_area.text = 'XXXXXXX'

buttons = [
    Button('FFFFFFFFFFFFFFFFF', handler=button_clicked) 
    for ya in apps
]

body = Box(
    HSplit(
        Box(body=HSplit(buttons, padding=1),
            #style='class:table',
            padding=1),
        Box(body=Frame(text_area),
            #style='class:status-bar',
            padding=1)
    )
)

# 2. Key bindings
kb = KeyBindings()
kb.add('tab')(focus_next)
kb.add('s-tab')(focus_previous)

@kb.add('q')
def _(event):
    " Quit application. "
    event.app.set_result(None)

layout=Layout(container=body,
              focussed_window=buttons[0]),

def cli():
    application = Application(
        layout=layout,
        key_bindings=kb,
        full_screen=True
    )
    application.run()

