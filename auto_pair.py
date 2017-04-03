import sublime
import sublime_plugin


# for auto pairing \left \right pairs
class LatexyzSurroundListener(sublime_plugin.EventListener):
    def on_query_context(self, view, key, operator, operand, match_all):
        if view.settings().get('is_widget'):
            return
        if not view.score_selector(view.sel()[0].end() if len(view.sel()) > 0 else 0,
                                   "text.tex.latex meta.environment.math"):
            return
        if key == 'latexyz_surround':
            left = operand[0]
            right = operand[1]
            out = True
            for sel in view.sel():
                if view.substr(sublime.Region(sel.begin()-len(left), sel.begin())) != left:
                    out = False
                    break
                if view.substr(sublime.Region(sel.end(), sel.end()+len(right))) != right:
                    out = False
                    break
            return out if operator == 0 else not out


class LatexyzInsertPairCommand(sublime_plugin.TextCommand):
    def run(self, edit, arg):
        left = "\\\\left" + arg[0].replace('\\', '\\\\')
        right = "\\\\right" + arg[1].replace('\\', '\\\\')
        self.view.run_command("latexyz_insert_snippet", {
            "contents": left+"${1:$SELECTION}"+right,
            "before": len(arg[0]),
            "after": len(arg[1])})


class LatexyzRemovePairCommand(sublime_plugin.TextCommand):
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
