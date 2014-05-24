import sublime, sublime_plugin
import os
import re
from . misc import *

def cleantex(texfile):

    ext = [".aux", ".dvi", ".lis", ".log", ".blg", ".bbl", ".toc", ".idx", ".ind",
            ".ilg", ".thm", ".out", ".fdb_latexmk", ".fls", ".nav", ".snm"]
    prefix = os.path.splitext(texfile)[0]
    for e in ext:
        if os.path.isfile(prefix+e):
            os.remove(prefix+e)

def cleantexdir(texdir):
    ext = [".aux", ".dvi", ".lis", ".log", ".blg", ".bbl", ".toc", ".idx", ".ind",
            ".ilg", ".thm", ".out", ".fdb_latexmk", ".fls", ".nav", ".snm", ".synctex.gz"]
    ls = os.listdir(texdir)
    rexp = "(" + '|'.join(['\\'+e for e in ext]) + ")$"
    fnames = [os.path.join(texdir, f) for f in ls if re.search(rexp, f)]
    for f in fnames: os.remove(f)


class LatexPlusCleanCommand(sublime_plugin.TextCommand):
    def run(self, edit, force=False):
        view = self.view
        tex_root = get_tex_root(view)
        tex_dir = os.path.dirname(tex_root)

        rexp = r'\\(?:input|include)\{([^\}]*)\}'
        results = search_in_tex(rexp, tex_root, recursive=True if force==True else False)
        texfiles = [r['result'] for r in results]
        texfiles = [f+".tex" if f[-4:].lower() != ".tex" else f for f in texfiles]
        texfiles = [tex_root] + [os.path.join(tex_dir,f) for f in texfiles]

        if force:
            texdirs = list(set([os.path.dirname(f) for f in texfiles]))
            for d in texdirs:
                if os.path.isdir(d):
                    cleantexdir(d)
            print("Force Clean Build!")
            sublime.status_message("Force Clean Build!")
        else:
            for f in texfiles:
                if os.path.isfile(f):
                    cleantex(f)
            print("Clean Build!")
            sublime.status_message("Clean Build!")
