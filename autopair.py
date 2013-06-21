import sublime, sublime_plugin

class AutoLeftRightPairListener(sublime_plugin.EventListener):
    def on_query_context(self, view, key, operator, operand, match_all):
        if view.is_scratch() or view.settings().get('is_widget'): return
        print(key)
        if key == 'in_brackets':
            out = all([view.substr(sel.begin()-1)=='(' and view.substr(sel.end())==')' for sel in view.sel()])
            return (out == operand) if operator==0 else not (out == operand)
        elif key == 'in_square_brackets':
            out = all([view.substr(sel.begin()-1)=='[' and view.substr(sel.end())==']' for sel in view.sel()])
            return (out == operand) if operator==0 else not (out == operand)
        elif key == 'in_curly_brackets':
            out = all([view.substr(sel.begin()-1)=='{' and view.substr(sel.end())=='}' for sel in view.sel()])
            return (out == operand) if operator==0 else not (out == operand)

class AutoLeftRightPairCommand(sublime_plugin.TextCommand):
    def run(self, edit, arg):
        view = self.view
        sel = [(s.begin(), s.end()) for s in view.sel()]
        view.sel().clear()
        for a,b in reversed(sel):
            left = "\\left"+arg[0]
            right = "\\right"+arg[1]
            view.replace(edit, sublime.Region(a-1,b+1),
                  left + view.substr(sublime.Region(a,b)) + right)
            view.sel().add(sublime.Region(a+4+len(arg[0]),b+4+len(arg[1])))
