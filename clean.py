import sublime, sublime_plugin
import os
import re
from . misc import *

def cleantex(texfile):
    prefix = os.path.splitext(texfile)[0]
    ext = ["aux", "dvi", "lis", "log", "blg", "bbl", "toc", "idx", "ind",
            "ilg", "thm", "out", "fdb_latexmk", "fls", "synctex.gz", "nav", "snm"]
    # ls = os.listdir(dir)
    # rexp = '|'.join(['\\.'+e for e in ext])
    # fnames = [os.path.join(dir, f) for f in ls if re.search(rexp, f)]
    for e in ext:
        if os.path.isfile(prefix+'.'+e):
            os.remove(prefix+'.'+e)

class LatexsqCleanCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        tex_root = get_tex_root(view)
        tex_dir = os.path.dirname(tex_root)

        rexp = r'\\(?:input|include)\{([^\}]*)\}'
        results = search_in_tex(rexp, tex_root)
        texfiles = [r['result'] for r in results]
        texfiles = [f+".tex" if f[-4:].lower() != ".tex" else f for f in texfiles]
        texfiles = [tex_root] + [os.path.join(tex_dir,f) for f in texfiles]
        for f in texfiles:
            if os.path.isfile(f): cleantex(f)

        print("Clean Build!")
        sublime.status_message("Clean Build!")

