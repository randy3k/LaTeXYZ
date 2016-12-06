import sublime
import sublime_plugin


class LatexZetaPreviewMath(sublime_plugin.EventListener):

    def on_activated_async(self, view):
        self.set_template_preamble(view)

    def on_post_save_async(self, view):
        self.set_template_preamble(view)

    def set_template_preamble(self, view):
        if not view.match_selector(view.sel()[0].end() if len(view.sel()) > 0 else 0,
                                   "text.tex.latex"):
            return
        lz_settings = sublime.load_settings("LaTeXZeta.sublime-settings")
        if not lz_settings.get("auto_set_preview_math_template_preamble"):
            return
        newcommand_regions = view.find_by_selector("meta.function.newcommand.latex")
        newcommands = []
        for s in newcommand_regions:
            newcommands.append(view.substr(s))
        view.settings().set("preview_math_template_preamble", "\n".join(newcommands))
