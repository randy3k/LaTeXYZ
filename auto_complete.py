import sublime
import sublime_plugin
import re
from .latex_commands import math_commands, general_commands


def is_duplicated(x, r):
    for item in r:
        if item[0].startswith(x):
            return True
    return False


ARROW = re.compile(r"(<?)([-=]{1,2})(>?)$")

arrow_map = {
    "<-": "\\leftarrow",
    "<--": "\\longleftarrow",
    "->": "\\rightarrow",
    "-->": "\\longrightarrow",
    "<->": "\\leftrightarrow",
    "<-->": "\\longleftrightarrow",
    "<=": "\\Leftarrow",
    "<==": "\\Longleftarrow",
    "=>": "\\Rightarrow",
    "==>": "\\Longrightarrow",
    "<=>": "\\Leftrightarrow",
    "<==>": "\\Longleftrightarrow"
}


class LatexyzAutoCompletions(sublime_plugin.EventListener):

    def on_query_completions(self, view, prefix, locations):
        if not view.match_selector(locations[0], "text.tex.latex"):
            return None

        if not prefix:
            # arrow completion
            pt = locations[0]
            arrow = view.substr(sublime.Region(pt - 4, pt))
            m = ARROW.search(arrow)
            if m and (m.group(1) or m.group(3)) and m.group(0) in arrow_map:
                arr = arrow_map[m.group(0)]
                return [(m.group(0), arr)]

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
