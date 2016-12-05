import sublime
import sublime_plugin


# sublime wrapper for insert
class LatexZetaInsertCommand(sublime_plugin.TextCommand):
    def run(self, edit, content, before=0, after=0):
        sel = [(s.begin(), s.end()) for s in self.view.sel()]
        for (a, b) in reversed(sel):
            region = sublime.Region(a-before, b+after)
            self.view.replace(edit, region, content)


class LatexZetaJumpToPdfCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        pt = self.view.sel()[0].end() if len(self.view.sel()) > 0 else 0
        if not self.view.score_selector(pt, "text.tex.latex"):
            print("LaTeXZeta: current file is not a latex file.")
            return
        self.view.window().run_command("view_pdf")
        # add a bit delay so that "view_pdf" is executed first
        sublime.set_timeout(
            lambda: self.view.run_command("jump_to_pdf", {"from_keybinding": True}), 100)
