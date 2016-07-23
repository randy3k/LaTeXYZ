import sublime
import os


def plugin_loaded():

    ofile = os.path.join(sublime.packages_path(), "User", "LaTeX-Plus.sublime-settings")
    nfile = os.path.join(sublime.packages_path(), "User", "LaTeXPlus.sublime-settings")
    if os.path.exists(ofile):
        os.rename(ofile, nfile)
