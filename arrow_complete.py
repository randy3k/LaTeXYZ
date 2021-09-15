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


class LatexyzArrowCompleteCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        sel = view.sel()
        for s in reversed(sel):
            if not s.empty():
                return
            pt = s.end()
            arrow = view.substr(sublime.Region(pt - 4, pt))
            m = ARROW.search(arrow)
            if m and (m.group(1) or m.group(3)) and m.group(0) in arrow_map:
                arr = arrow_map[m.group(0)]
                view.replace(edit, sublime.Region(pt - len(m.group(0)), pt), arr)
