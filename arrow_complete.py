import sublime
import sublime_plugin
import re


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


class LatexyzArrowCompletions(sublime_plugin.EventListener):

    general_commands = None
    math_commands = None

    def on_query_completions(self, view, prefix, locations):
        if view.settings().get('is_widget'):
            return

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
