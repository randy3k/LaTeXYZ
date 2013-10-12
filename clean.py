import sublime, sublime_plugin
import os
import re
from . misc import *

def cleantex(dir):
    ext = ["aux", "dvi", "lis", "log", "blg", "bbl", "toc", "idx", "ind",
            "ilg", "thm", "out", "fdb_latexmk", "fls", "synctex.gz", "nav", "snm"]
    ls = os.listdir(dir)
    rexp = '|'.join(['\\.'+e for e in ext])
    fnames = [os.path.join(dir, f) for f in ls if re.search(rexp, f)]
    for f in fnames: os.remove(f)

class LatexsqCleanCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        texroot = get_tex_root(view)
        tex_dir = os.path.dirname(texroot)

        results = []
        rexp = r'\\(?:input|include)\{([^\}]*)\}'
        search_in_tex(rexp, texroot, tex_dir, results)
        dirs = [os.path.dirname(r['result']) for r in results]
        dirs = [tex_dir] + [os.path.join(tex_dir,d) for d in dirs if d]
        for d in dirs:
            if os.path.isdir(d): cleantex(d)

        print("Clean Build!")
        sublime.status_message("Clean Build!")

