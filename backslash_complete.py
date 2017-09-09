import sublime
import sublime_plugin
from .completions.latex_commands import math_commands, general_commands


def is_duplicated(x, r):
    for item in r:
        if item[0].startswith(x):
            return True
    return False


lz_settings_file = "LaTeXYZ.sublime-settings"


def tidy(x):
    if len(x) == 2:
        contents = x[1]
        if "$1" not in contents:
            contents = contents.replace("$0", "$1")
        elif "$2" not in contents:
            contents = contents.replace("$0", "$2")
        return (x[0], contents)
    else:
        return x


class LatexyzBlackSlashCompletions(sublime_plugin.EventListener):

    general_commands = None
    math_commands = None

    def on_query_completions(self, view, prefix, locations):
        if view.settings().get('is_widget'):
            return

        if not view.match_selector(locations[0], "text.tex.latex"):
            return None

        lz_settings = sublime.load_settings(lz_settings_file)

        if not lz_settings.get("backslash_complete"):
            return

        if not self.general_commands:
            if lz_settings.get("auto_create_fields", False):
                self.general_commands = [tidy(x) for x in general_commands]
            else:
                self.general_commands = general_commands

        if not self.math_commands:
            if lz_settings.get("auto_create_fields", False):
                self.math_commands = [tidy(x) for x in math_commands]
            else:
                self.math_commands = math_commands

        # use default completion for non latex command
        ploc = locations[0] - len(prefix)
        if prefix and view.substr(sublime.Region(ploc - 1, ploc)) != "\\":
            return None

        r = self.general_commands
        if view.match_selector(locations[0], "meta.environment.math"):
            r = r + self.math_commands

        extract_completions = list(set(
            [view.substr(s) for s in view.find_all(r"\\%s[a-zA-Z@]+\*?" % prefix) if s.size() > 3]
        ))
        r = r + [(item, ) for item in extract_completions if not is_duplicated(item, r)]
        return list(set(r))
