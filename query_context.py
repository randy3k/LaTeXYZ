import sublime
import sublime_plugin


lz_settings_file = "LaTeXYZ.sublime-settings"


class LatexyzQueryContext(sublime_plugin.EventListener):

    def on_query_context(self, view, key, operator, operand, match_all):
        if view.settings().get('is_widget'):
            return

        try:
            pt = view.sel()[0].end()
        except Exception:
            pt = 0

        if not view.match_selector(pt, "text.tex.latex"):
            return

        lz_settings = sublime.load_settings(lz_settings_file)

        if key == 'latexyz.use_latex_quotes':
            out = lz_settings.get("use_latex_quotes", True)
            return out if operator == 0 else not out

        elif key == 'latexyz.space_arrow_complete':
            out = lz_settings.get("space_arrow_complete", True)
            return out if operator == 0 else not out

        elif key == 'latexyz.surrounded_by':
            left = operand[0]
            right = operand[1]
            out = True
            for sel in view.sel():
                if view.substr(sublime.Region(sel.begin() - len(left), sel.begin())) != left:
                    out = False
                    break
                if view.substr(sublime.Region(sel.end(), sel.end() + len(right))) != right:
                    out = False
                    break
            return out if operator == 0 else not out
