import sublime
import sublime_plugin


# for auto pair \left \right pairs
class LatexBoxPairListener(sublime_plugin.EventListener):
    def on_query_context(self, view, key, operator, operand, match_all):
        if view.is_scratch() or view.settings().get('is_widget'):
            return
        if not view.score_selector(view.sel()[0].end() if len(view.sel()) > 0 else 0,
                                   "text.tex.latex meta.environment.math"):
            return
        if key == 'selection_in_brackets':
            out = all([view.substr(sel.begin()-1) == '(' and
                      view.substr(sel.end()) == ')' for sel in view.sel()])
            return (out == operand) if operator == 0 else not (out == operand)
        elif key == 'selection_in_square_brackets':
            out = all([view.substr(sel.begin()-1) == '[' and
                       view.substr(sel.end()) == ']' for sel in view.sel()])
            return (out == operand) if operator == 0 else not (out == operand)
        elif key == 'selection_in_curly_brackets':
            out = all([view.substr(sublime.Region(sel.begin()-2, sel.begin())) == '\\{' and
                       view.substr(sublime.Region(sel.end(), sel.end()+2)) == '\\}'
                       for sel in view.sel()])
            return (out == operand) if operator == 0 else not (out == operand)
        elif key == 'selection_in_bars':
            out = all([view.substr(sublime.Region(sel.begin()-2, sel.begin())) == '\\|' and
                       view.substr(sublime.Region(sel.end(), sel.end()+2)) == '\\|'
                       for sel in view.sel()])
            return (out == operand) if operator == 0 else not (out == operand)
        elif key == 'selection_in_angles':
            out = all([view.substr(sublime.Region(sel.begin()-7, sel.begin())) == '\\langle' and
                       view.substr(sublime.Region(sel.end(), sel.end()+7)) == '\\rangle'
                       for sel in view.sel()])
            return (out == operand) if operator == 0 else not (out == operand)


class LatexBoxPairCommand(sublime_plugin.TextCommand):
    def run(self, edit, arg):
        view = self.view
        sel = [(s.begin(), s.end()) for s in view.sel()]
        view.sel().clear()
        for a, b in reversed(sel):
            view.replace(edit, sublime.Region(a-len(arg[0]), b+len(arg[1])),
                         view.substr(sublime.Region(a, b)))
            view.sel().add(sublime.Region(a-len(arg[0]), b-len(arg[0])))

        left = "\\left" + arg[0].replace('\\', '\\\\')
        right = "\\right" + arg[1].replace('\\', '\\\\')

        view.run_command("insert_snippet", {"contents": left+"${1:$SELECTION}"+right})


class LatexBoxRemovePairCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        sel = [(s.begin(), s.end()) for s in view.sel()]
        for a, b in reversed(sel):
            if view.substr(sublime.Region(a-6, a)) == '\\left(' and \
                    view.substr(sublime.Region(a, a+7)) == '\\right)':
                view.replace(edit, sublime.Region(a-6, a+7), "")
            elif view.substr(sublime.Region(a-6, a)) == '\\left[' and \
                    view.substr(sublime.Region(a, a+7)) == '\\right]':
                view.replace(edit, sublime.Region(a-6, a+7), "")
            elif view.substr(sublime.Region(a-7, a)) == '\\left\\{' and \
                    view.substr(sublime.Region(a, a+8)) == '\\right\\}':
                view.replace(edit, sublime.Region(a-7, a+8), "")
            elif view.substr(sublime.Region(a-7, a)) == '\\left\\|' and \
                    view.substr(sublime.Region(a, a+8)) == '\\right\\|':
                view.replace(edit, sublime.Region(a-7, a+8), "")
            elif view.substr(sublime.Region(a-12, a)) == '\\left\\langle' and \
                    view.substr(sublime.Region(a, a+13)) == '\\right\\rangle':
                view.replace(edit, sublime.Region(a-12, a+13), "")
