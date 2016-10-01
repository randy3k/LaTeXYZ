import sublime
import sublime_plugin
from .constants import math_commands, general_commands


def is_duplicated(x, r):
    for item in r:
        if item[0].startswith(x):
            return True
    return False


class LatexBoxAutoCompletions(sublime_plugin.EventListener):

    def on_query_completions(self, view, prefix, locations):
        if not view.match_selector(locations[0], "text.tex.latex"):
            return None

        # use default completion for non latex command
        ploc = locations[0]-len(prefix)
        if prefix and view.substr(sublime.Region(ploc-1, ploc)) != "\\":
            return None

        r = general_commands
        if view.match_selector(locations[0], "meta.environment.math"):
            r = r + math_commands

        extract_completions = list(set(
            [view.substr(s) for s in view.find_all(r"\\%s[a-zA-Z@]+\*?" % prefix) if s.size() > 3]
        ))
        r = r + [(item, ) for item in extract_completions if not is_duplicated(item, r)]
        return list(set(r))
