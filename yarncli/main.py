from __future__ import print_function, unicode_literals 

from prompt_toolkit.application import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.key_binding.bindings.focus import focus_next, focus_previous
from prompt_toolkit.layout.containers import HSplit, VSplit, Window, FloatContainer, VerticalAlign, HorizontalAlign
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.widgets import Box, Frame, TextArea, Button
from prompt_toolkit.widgets.base import Border
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.layout.dimension import D
from prompt_toolkit.styles import Style
from prompt_toolkit.layout.screen import Point
from prompt_toolkit.formatted_text import HTML


DEFAULT_ROW_WIDTH = 70


#import pydevd; pydevd.settrace(port=3000)

class YarnApplication(object):
    """A Yarn application."""

    def __init__(self, app_id, name, progress, status):
        self.app_id = app_id
        self.name = name
        self.progress = progress
        self.status = status

    @property
    def fields(self):
        return [self.app_id, self.name, self.progress, self.status]

    def as_text(self, width=DEFAULT_ROW_WIDTH):
        col_width = int(width / 4)

        def _as_text(val):
            txt = ' ' + val
            txt = txt.ljust(col_width)
            return txt[:col_width]
        return ''.join([_as_text(f) for f in self.fields])


class YarnWatcher(object):
    """Data class to keep state and display applications."""

    def __init__(self):
        self.apps = [
            YarnApplication('xxx', 'job-1, 2017-01-01 to 2017-01-01', '100', 'FINISHED'),
            YarnApplication('yyy', 'job-2, 2017-01-01 to 2017-01-01', '10', 'RUNNING'),
            YarnApplication('zzz', 'job-3, 2017-01-01 to 2017-01-01', '70', 'FAILED')
        ]
        self.selected_index = 0

    @property
    def current_application(self):
        return self.apps[self.selected_index]

    def select_previous(self):
        self.selected_index = (self.selected_index - 1) % len(self.apps)

    def select_next(self):
        self.selected_index = (self.selected_index + 1) % len(self.apps)


def create_application_table(yarn_watcher):
    """Create table with the list of applications."""

    def get_text():
        result = []
        result.append(('', Border.TOP_LEFT))
        result.append(('', Border.HORIZONTAL * (DEFAULT_ROW_WIDTH - 2)))
        result.append(('', Border.TOP_RIGHT))
        result.append(('', '\n'))
        for a in yarn_watcher.apps:
            result.append(('', Border.VERTICAL))
            if a == yarn_watcher.current_application:
                result.append(('[SetCursorPosition]', ''))
                result.append(('class:table.current', a.as_text()))
            else:
                result.append(('', a.as_text()))
            result.append(('', Border.VERTICAL))
            result.append(('', '\n'))
        result.append(('', Border.BOTTOM_LEFT))
        result.append(('', Border.HORIZONTAL * (DEFAULT_ROW_WIDTH - 2)))
        result.append(('', Border.BOTTOM_RIGHT))
        result.append(('', '\n'))
        return result

    kb = KeyBindings()

    @kb.add('up')
    def _(event):
        yarn_watcher.select_previous()

    @kb.add('down')
    def _(event):
        yarn_watcher.select_next()

    control = FormattedTextControl(
        get_text,
        focusable=True,
        key_bindings=kb)

    return Window(control,
                  width=DEFAULT_ROW_WIDTH,
                  always_hide_cursor=True,
                  style='class:table')


def create_application_details(yarn_watcher):
    """Create application details window."""
    def get_text(width=DEFAULT_ROW_WIDTH):
        def _row(val, st=''):
            return [(st, Border.VERTICAL),
                    (st, val.ljust(width-2)[:width-2]),
                    (st, Border.VERTICAL),
                    (st, '\n')]

        curr = yarn_watcher.current_application
        result = []
        result.append(('', Border.TOP_LEFT))
        result.append(('', Border.HORIZONTAL * (width - 2)))
        result.append(('', Border.TOP_RIGHT))
        result.append(('', '\n'))
        result.extend(_row('Application ID: {}'.format(curr.app_id)))
        result.extend(_row('Name: {}'.format(curr.name)))
        result.extend(_row('Progress: {}%'.format(curr.progress)))
        result.extend(_row('Status: {}'.format(curr.status),
                           'class:status.{}'.format(curr.status).lower()))
        result.append(('', Border.BOTTOM_LEFT))
        result.append(('', Border.HORIZONTAL * (width - 2)))
        result.append(('', Border.BOTTOM_RIGHT))
        result.append(('', '\n'))
        return result

    control = FormattedTextControl(get_text, focusable=False)

    return Window(control, width=DEFAULT_ROW_WIDTH, style='class:details')


# def app_selected(app_ix):
#     global selected_index
#     text_area.text = 'Selected: {}'.format(apps[app_ix].id)
#     selected_index = app_ix
#
#
# def get_formatted_text():
#     result = []
#     result.append(('class:table', Border.TOP_LEFT))
#     result.append(('class:table', Border.HORIZONTAL * (80 + 4)))
#     result.append(('class:table', Border.TOP_RIGHT))
#     result.append(('', '\n'))
#     for i, a in enumerate(apps):
#         row_text = '    '.join(a)
#         row_handler = lambda: app_selected(i)
#         if i == selected_index:
#             result.append(('[SetCursorPosition]', ''))
#         else:
#             result.append(('class:table', row_text, row_handler))
#         result.append(('', '\n'))
#     return result


# table = Window(
#     FormattedTextControl(get_formatted_text, focussable=True, show_cursor=False),
#     style='class:menu',
#     transparent=False)


# Styling.
style = Style([
    ('table', 'bg:#268bd2 #ffffff'),
    ('table.current', 'bg:#cccccc #000000'),
    ('table.border shadow', '#444444'),
    ('details', 'bg:#cccccc #000000'),
    ('status.finished', '#228b22'),
    ('status.running', '#0066cc'),
    ('status.failed', '#cc0000'),
    ('header', 'bg:#eee8d5 #002b36'),
    ('footer', 'bg:#2aa198 #002b36'),
    ('shortcut', 'bold underline'),
])


def create_layout(yarn_watcher):
    """
    Create the layout.
    """

    app_table = create_application_table(yarn_watcher)
    app_details = create_application_details(yarn_watcher)

    # Toolbars.
    titlebar_text = HTML(
        '<strong>YARN Application Watcher</strong> Press <shortcut>[Ctrl-C]</shortcut> to quit.')

    bottom_toolbar_text = HTML(
        '<shortcut>[Ctrl-C]</shortcut>: quit  '
        '<shortcut>[Up]</shortcut>/<shortcut>[Down]</shortcut> select previous/next.'
    )

    root_container = FloatContainer(
        content=HSplit([

            # The titlebar.
            Window(height=1,
                   content=FormattedTextControl(titlebar_text),
                   align=VerticalAlign.CENTER,
                   style='class:header'),

            # The table.
            VSplit([
                app_table,
                app_details
            ]),

            # bottom buttons

            VSplit([Button('Resource Manager', width=30),
                    Button('Node Manager', width=30)],
                   align=VerticalAlign.CENTER),

            # bottom toolbar.
            Window(height=1,
                   content=FormattedTextControl(bottom_toolbar_text),
                   style='class:footer'),

        ]),
        floats=[])

    return Layout(root_container, focused_element=app_table)


kb = KeyBindings()


@kb.add('c-c', eager=True)
@kb.add('c-q', eager=True)
def _(event):
    """Pressing Ctrl-Q or Ctrl-C will exit the user interface."""
    event.app.exit()


def cli():
    watcher = YarnWatcher()

    application = Application(
        layout=create_layout(watcher),
        key_bindings=kb,
        full_screen=True,
        style=style
    )
    application.run()

