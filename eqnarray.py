import sublime, sublime_plugin
import re

# for auto pair \left \right pairs

class AutoLeftRightPairListener(sublime_plugin.EventListener):
    def on_query_context(self, view, key, operator, operand, match_all):
        if view.is_scratch() or view.settings().get('is_widget'): return
        if not view.score_selector(view.sel()[0].end() if len(view.sel())>0 else 0, "text.tex.latex"): return
        if key == 'in_multiline_eqnarray':
            return True
            

class AutoLeftRightPairCommand(sublime_plugin.TextCommand):
    def run(self, edit, arg):
        view = self.view
        sel = [(s.begin(),s.end()) for s in view.sel()]
        view.sel().clear()
        for a,b in reversed(sel):
            print(len(arg[0]))
            view.replace(edit, sublime.Region(a-len(arg[0]),b+len(arg[1])), view.substr(sublime.Region(a,b)))
            view.sel().add(sublime.Region(a-len(arg[0]),b-len(arg[0])))

        left = "\\left"+ arg[0].replace('\\', '\\\\')
        right = "\\right"+ arg[1].replace('\\', '\\\\')

        view.run_command("insert_snippet", {"contents": left+"${1:$SELECTION}"+right})

