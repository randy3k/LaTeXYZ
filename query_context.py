import sublime
import sublime_plugin


lz_settings_file = "LaTeXYZ.sublime-settings"


class LatexyzQuotes(sublime_plugin.EventListener):

    def on_query_context(self, view, key, operator, operand, match_all):
        if view.settings().get('is_widget'):
            return
        if not view.match_selector(view.sel()[0].end() if len(view.sel()) > 0 else 0,
                                   "text.tex.latex"):
            return

        lz_settings = sublime.load_settings(lz_settings_file)

        if key == 'latexyz_quotes':
            return lz_settings.get("use_latex_quotes", True)
