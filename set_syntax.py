import sublime, sublime_plugin

class RubberSetSyntax(sublime_plugin.EventListener):

    def set_syntax(self, view):
        point = view.sel()[0].end()
        s  = sublime.load_settings("Rubber.sublime-settings")
        if view.score_selector(point, "text.tex.latex") and s.get('force_set_syntax', True):
            print("force_set_syntax")
            view.set_syntax_file("Packages/Rubber/support/LaTeX.tmLanguage")

    def on_load(self, view):
        self.set_syntax(view)

    def on_post_save(self, view):
        self.set_syntax(view)

    def on_activated(self, view):
        self.set_syntax(view)