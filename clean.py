import sublime
import sublime_plugin
import os
import re
from . utils import get_tex_root, search_in_tex


def cleantex(texfile):
    settings = sublime.load_settings('LaTeXBox.sublime-settings')
    ext = settings.get("clean_ext")
    prefix = os.path.splitext(texfile)[0]
    for e in ext:
        if os.path.isfile(prefix+e):
            os.remove(prefix+e)


def cleantexdir(texdir):
    settings = sublime.load_settings('LaTeXBox.sublime-settings')
    ext = settings.get("clean_ext") + settings.get("clean_ext_force")
    ls = os.listdir(texdir)
    rexp = "(" + '|'.join(['\\'+e for e in ext]) + ")$"
    fnames = [os.path.join(texdir, f) for f in ls if re.search(rexp, f)]
    for f in fnames:
        os.remove(f)


class LatexBoxCleanCommand(sublime_plugin.WindowCommand):
    def run(self, **kwargs):
        if "force" in kwargs:
            force = kwargs["force"]
        else:
            force = False
        view = self.window.active_view()
        tex_root = get_tex_root(view)
        tex_dir = os.path.dirname(tex_root)

        rexp = r'\\(?:input|include)\{([^\}]*)\}'
        results = search_in_tex(rexp, tex_root, recursive=True if force is True else False)
        texfiles = [r['result'] for r in results]
        texfiles = [f+".tex" if f[-4:].lower() != ".tex" else f for f in texfiles]
        texfiles = [tex_root] + [os.path.join(tex_dir, f) for f in texfiles]

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
