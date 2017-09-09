import sublime
import sublime_plugin

lz_settings_file = "LaTeXYZ.sublime-settings"


class LatexyzInsertPairCommand(sublime_plugin.TextCommand):
    def run(self, edit, arg):
        left = "\\\\left" + arg[0].replace('\\', '\\\\')
        right = "\\\\right" + arg[1].replace('\\', '\\\\')

        lz_settings = sublime.load_settings(lz_settings_file)
        d = 1 if lz_settings.get("auto_create_fields", False) else 0
        self.view.run_command("latexyz_insert_snippet", {
            "contents": left + "${%d:$SELECTION}" % d + right,
            "before": len(arg[0]),
            "after": len(arg[1])})


class LatexyzRemovePairCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        sel = [(s.begin(), s.end()) for s in view.sel()]
        for a, b in reversed(sel):
            if view.substr(sublime.Region(a - 6, a)) == '\\left(' and \
                    view.substr(sublime.Region(a, a + 7)) == '\\right)':
                view.replace(edit, sublime.Region(a - 6, a + 7), "")
            elif view.substr(sublime.Region(a - 6, a)) == '\\left[' and \
                    view.substr(sublime.Region(a, a + 7)) == '\\right]':
                view.replace(edit, sublime.Region(a - 6, a + 7), "")
            elif view.substr(sublime.Region(a - 7, a)) == '\\left\\{' and \
                    view.substr(sublime.Region(a, a + 8)) == '\\right\\}':
                view.replace(edit, sublime.Region(a - 7, a + 8), "")
            elif view.substr(sublime.Region(a - 7, a)) == '\\left\\|' and \
                    view.substr(sublime.Region(a, a + 8)) == '\\right\\|':
                view.replace(edit, sublime.Region(a - 7, a + 8), "")
            elif view.substr(sublime.Region(a - 12, a)) == '\\left\\langle' and \
                    view.substr(sublime.Region(a, a + 13)) == '\\right\\rangle':
                view.replace(edit, sublime.Region(a - 12, a + 13), "")
