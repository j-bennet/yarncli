from __future__ import print_function, unicode_literals 

from prompt_toolkit.application import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.key_binding.bindings.focus import focus_next, focus_previous
from prompt_toolkit.layout.containers import HSplit
from prompt_toolkit.layout.widgets import Button, Box, Frame, TextArea
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.layout.dimension import D
from prompt_toolkit.styles import Style

from collections import namedtuple

YarnApp = namedtuple('YarnApp', ['id', 'name', 'progress', 'state'])

apps = [
    YarnApp('xxx', 'job-1, 2017-01-01 to 2017-01-01', '100', 'FINISHED'),
    YarnApp('yyy', 'job-2, 2017-01-01 to 2017-01-01', '10', 'RUNNING'),
    YarnApp('zzz', 'job-3, 2017-01-01 to 2017-01-01', '70', 'FAILED')
]


def app_selected(app_id):
    text_area.text = 'Selected: {}'.format(app_id)


buttons = [Button('    '.join(ya),
                  width=80,
                  handler=lambda: app_selected(ya.id))
           for ya in apps]


text_area = TextArea(focussable=True, multiline=False)


body = Box(
    HSplit([
        Box(body=HSplit(buttons, padding=1),
            style='class:table',
            width=D(preferred=80),
            padding=1),
        Box(body=Frame(text_area),
            width=D(preferred=80),
            style='class:command-bar',
            padding=1)
    ])
)


# 2. Key bindings
kb = KeyBindings()
kb.add('tab')(focus_next)
kb.add('s-tab')(focus_previous)


@kb.add('q')
def _(event):
    """Quit application."""
    event.app.set_result(None)


# Styling.
style = Style([
    ('table', 'bg:#0000ff #000000'),
    ('command-bar', 'bg:#666666 #000000'),
    ('button',          '#000000'),
    ('button-arrow',    '#000000'),
    ('button focussed', 'bg:#cccccc'),
])


layout = Layout(container=body, focussed_window=buttons[0])


def cli():
    application = Application(
        layout=layout,
        key_bindings=kb,
        style=style,
        full_screen=True
    )
    application.run()
