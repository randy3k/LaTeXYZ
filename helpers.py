import sublime
import sublime_plugin
import os
import json


# sublime wrapper for insert_snippet
class LatexyzInsertSnippetCommand(sublime_plugin.TextCommand):
    def run(self, edit, contents, before=0, after=0):
        sel = [(s.begin(), s.end()) for s in self.view.sel()]
        for (a, b) in reversed(sel):
            self.view.replace(edit, sublime.Region(b, b+after), "")
            self.view.replace(edit, sublime.Region(a-before, a), "")
        self.view.run_command("insert_snippet", {"contents": contents})


class LatexyzJumpToPdfCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        pt = self.view.sel()[0].end() if len(self.view.sel()) > 0 else 0
        if not self.view.score_selector(pt, "text.tex.latex"):
            print("LaTeXYZ: current file is not a latex file.")
            return
        self.view.run_command("jump_to_pdf", {
            "from_keybinding": True,
            "keep_focus": False})

mousebind = [
    {
        "button": "button1", "modifiers": ["shift", "ctrl"],
        "press_command": "latexyz_jump_to_pdf"
    }
]


class LatexyzInstallPdfMousebindingCommand(sublime_plugin.TextCommand):
    def run(self, edit, remove=False):
        if sublime.platform() == "windows":
            plat = "Windows"
        elif sublime.platform() == "osx":
            plat = "OSX"
            mousebind[0]["modifiers"][1] = "super"
        elif sublime.platform() == "linux":
            plat = "Linux"

        mousebind_file = os.path.join(
            sublime.packages_path(),
            "User",
            "LaTeXYZ",
            "Default ({}).sublime-mousemap".format(plat))

        if remove:
            try:
                os.unlink(mousebind_file)
                os.unlink(mousebind_file.replace("LaTeXYZ", "LaTeXZeta"))
            except:
                pass
        else:
            os.makedirs(os.path.dirname(mousebind_file), exist_ok=True)

            with open(mousebind_file, "w") as f:
                json.dump(mousebind, f)
