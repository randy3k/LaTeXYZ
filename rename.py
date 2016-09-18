import sublime
import os


def plugin_loaded():

    ofile = os.path.join(sublime.packages_path(), "User", "LaTeX-Plus.sublime-settings")
    nfile = os.path.join(sublime.packages_path(), "User", "LaTeXPlus.sublime-settings")
    if os.path.exists(ofile) and not os.path.exists(nfile):
        os.rename(ofile, nfile)
        os.unlink(ofile)

    ofile = os.path.join(sublime.packages_path(), "User", "LaTeXPlus.sublime-settings")
    nfile = os.path.join(sublime.packages_path(), "User", "LaTeXBox.sublime-settings")
    if os.path.exists(ofile) and not os.path.exists(nfile):
        os.rename(ofile, nfile)
        os.unlink(ofile)

    latexplus = os.path.join(sublime.packages_path(), "User", "LaTeX+.sublime-settings")
    latex = os.path.join(sublime.packages_path(), "User", "LaTeX.sublime-settings")
    if os.path.exists(latexplus) and not os.path.exists(latex):
        os.rename(latexplus, latex)
        os.unlink(latexplus)
