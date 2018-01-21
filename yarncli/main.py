from __future__ import print_function, unicode_literals 

from prompt_toolkit.application import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.key_binding.bindings.focus import focus_next, focus_previous
from prompt_toolkit.layout.containers import HSplit, VSplit, Window, FloatContainer, Align
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.widgets import Box, Frame, TextArea
from prompt_toolkit.layout.widgets.base import Border
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.layout.dimension import D
from prompt_toolkit.styles import Style
from prompt_toolkit.layout.screen import Point
from prompt_toolkit.formatted_text import HTML


DEFAULT_ROW_WIDTH = 70


class YarnApplication(object):
    """A Yarn application."""

    def __init__(self, app_id, name, progress, status):
        self.app_id = app_id
        self.name = name
        self.progress = progress
        self.status = status

    def as_text(self, width=DEFAULT_ROW_WIDTH):
        col_width = width / 4
        return '{}{}{}{}'.format(self.app_id.ljust(col_width),
                                 self.name.ljust(col_width),
                                 self.progress.ljust(col_width),
                                 self.status.ljust(col_width))


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
        return '\n'.join(a.as_text() for a in yarn_watcher.apps)

    kb = KeyBindings()

    @kb.add('up')
    def _(event):
        yarn_watcher.select_previous()

    @kb.add('down')
    def _(event):
        yarn_watcher.select_next()

    def cursor_position():
        return Point(x=0, y=yarn_watcher.selected_index)

    control = FormattedTextControl(
        get_text,
        focussable=True,
        get_cursor_position=cursor_position,
        key_bindings=kb)

    return Window(control, width=DEFAULT_ROW_WIDTH, cursorline=True, style='class:table')


def create_application_details(yarn_watcher):
    """Create application details window."""

    def get_text():
        return 'Selected: {}'.format(yarn_watcher.current_application.app_id)

    control = FormattedTextControl(get_text,
                                   focussable=False)

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
    ('table.border', '#eee8d5'),
    ('table.border shadow', '#444444'),
    ('details', 'bg:#666666 #000000'),
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
        '<strong>YARN Application Watcher</strong> Press <shortcut>[Ctrl-Q]</shortcut> to quit.')

    bottom_toolbar_text = HTML(
        '<shortcut>[Ctrl-C]</shortcut>: quit  '
        '<shortcut>[Up]</shortcut>/<shortcut>[Down]</shortcut> select previous/next.'
    )

    root_container = FloatContainer(
        content=HSplit([

            # The titlebar.
            Window(height=1,
                   content=FormattedTextControl(titlebar_text),
                   align=Align.CENTER,
                   style='class:header'),

            # The table.
            VSplit([
                app_table,
                app_details
            ]),

            # bottom toolbar.
            Window(height=1,
                   content=FormattedTextControl(bottom_toolbar_text),
                   style='class:footer'),

        ]),
        floats=[])

    return Layout(root_container, focussed_window=app_table)


kb = KeyBindings()


@kb.add('c-c', eager=True)
@kb.add('c-q', eager=True)
def _(event):
    """Pressing Ctrl-Q or Ctrl-C will exit the user interface."""
    event.app.set_result(None)


def cli():
    watcher = YarnWatcher()

    application = Application(
        layout=create_layout(watcher),
        key_bindings=kb,
        full_screen=True,
        style=style
    )
    application.run()
