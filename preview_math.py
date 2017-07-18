import sublime
import sublime_plugin


lz_settings_file = "LaTeXYZ.sublime-settings"


class LatexyzPreviewMath(sublime_plugin.EventListener):

    def on_activated_async(self, view):
        self.set_template_preamble(view)

    def on_post_save_async(self, view):
        self.set_template_preamble(view)

    def set_template_preamble(self, view):
        try:
            pt = view.sel()[0].end()
        except:
            pt = 0

        if not view.match_selector(pt, "text.tex.latex"):
            return
        lz_settings = sublime.load_settings(lz_settings_file)
        if not lz_settings.get("auto_set_preview_math_template_preamble"):
            return
        newcommand_regions = view.find_by_selector(
            "meta.function.newcommand.latex, meta.function.declare-math-operator.latex")
        newcommands = []
        for s in newcommand_regions:
            newcommands.append(view.substr(s))
        view.settings().set("preview_math_template_preamble", "\n".join(newcommands))


class LatexyzTooglePreviewMath(sublime_plugin.TextCommand):
    def run(self, view):
        lz_settings = sublime.load_settings(lz_settings_file)
        flag = not lz_settings.get("auto_set_preview_math_template_preamble")
        lz_settings.set("auto_set_preview_math_template_preamble", flag)
        sublime.status_message("Set auto_set_preview_math_template_preamble as {}".format(flag))
        lz_settings = sublime.load_settings(lz_settings_file)
