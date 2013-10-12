import sublime, sublime_plugin
import os
import re
from . misc import *

# sublime wrapper for replacement
class LatexsqReplaceCommand(sublime_plugin.TextCommand):
    def run(self, edit, a, b, replacement):
        region = sublime.Region(a, b)
        self.view.replace(edit, region, replacement)
        self.view.sel().clear()
        self.view.sel().add(a+len(replacement))

class LatexsqAcCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        point = view.sel()[0].end()
        if not view.score_selector(point, "text.tex.latex"): return
        linecontent = view.substr(sublime.Region(view.line(point).begin(), point))

        rexp = re.compile(r".*\\(?:eq|page)*ref(\{([a-zA-Z0-9_:-]*))?$")
        m = rexp.match(linecontent)
        if m: self.dispatch_ref(m, point); return

        rexp = re.compile(r".*\\cite(?:[a-zA-Z_*]*)(\{(?:[a-zA-Z0-9_:-]*\s*,\s*)*([a-zA-Z0-9_:-]*))?$")
        m = rexp.match(linecontent)
        if m: self.dispatch_cite(m, point); return

        rexp = re.compile(r".*\\label(\{([a-zA-Z0-9_:-]*))?$")
        m = rexp.match(linecontent)
        if m: self.dispatch_label(m, point); return

        rexp = re.compile(r".*\\includegraphics((?:\[[\]]*\])?\{([^\}]*))?$")
        m = rexp.match(linecontent)
        ext = ['jpg', 'jpeg', 'bmp', 'pdf', 'ps', 'eps']
        if m: self.dispatch_listdir(m, point, ext); return

        rexp = re.compile(r".*\\(?:input|include)(\{([^\}]*))?$")
        m = rexp.match(linecontent)
        ext = ['tex']
        if m: self.dispatch_listdir(m, point, ext); return

        rexp = re.compile(r".*\\bibliography(\{([^\}]*))?$")
        m = rexp.match(linecontent)
        ext = ['bib']
        if m: self.dispatch_listdir(m, point, ext); return

        sublime.status_message("Nothing to be auto completed.")

    def on_completion(self, i, completions, add_braces, a, b):
        if i<0: return
        open_brace = "" if add_braces else "{"
        close_brace = "" if add_braces else "}"
        rept = open_brace + completions[i] + close_brace
        self.view.run_command("latexsq_replace", {"a": a, "b": b, "replacement": rept})

    def dispatch_ref(self, m, point):
        print("dispatching ref")
        view = self.view
        texroot = get_tex_root(view)
        tex_dir = os.path.dirname(texroot)
        option, prefix = m.groups()

        results = []
        search_in_tex(r'\\label\{([^\{\}]+)\}', texroot, tex_dir, results)

        if prefix:
            results = [c for c in results if prefix in c['result']]
        else:
            prefix = ""

        if not results:
            sublime.status_message("No label matches %s!" % (prefix,))
            return

        display = [[c['result'], os.path.relpath(c['file'], tex_dir)+":"+str(c['line'])] for c in results]
        on_done = lambda i: self.on_completion(i, [c['result'] for c in results], option, point - len(prefix), point)
        view.window().show_quick_panel(display, on_done)

    def dispatch_cite(self, m, point):
        print("dispatching cite")
        view = self.view
        texroot = get_tex_root(view)
        option, prefix = m.groups()

        results = []
        find_bib_records(texroot, results)

        if prefix:
            results = [c for c in results \
                            if prefix.lower() in ("%s %s %s" % (c['keyword'],c['title'], c['author'])).lower()]
        else:
            prefix = ""

        if results:
            # sort by author
            results = sorted(results, key=lambda x: x['author'].lower())
        else:
            sublime.status_message("No bib record matches %s!" % (prefix,))
            return

        display = [[ "[" + c['author'] + "] " + c['title'], " (" + c['keyword'] + ") " + c['title'] ] for c in results]
        on_done = lambda i: self.on_completion(i, [c['keyword'] for c in results], option, point - len(prefix), point)
        view.window().show_quick_panel(display, on_done)

    def dispatch_label(self, m, point):
        print("dispatching label")
        view = self.view
        texroot = get_tex_root(view)
        tex_dir = os.path.dirname(texroot)
        option, prefix = m.groups()
        print(prefix)

    def dispatch_listdir(self, m, point, ext):
        print("dispatching listdir")
        view = self.view
        texroot = get_tex_root(view)
        tex_dir = os.path.dirname(texroot)
        option, prefix = m.groups()

        if not prefix: prefix = ""
        dir = os.path.join(tex_dir, os.path.dirname(prefix))
        base = os.path.basename(prefix)
        def on_done(target):
            target_dir = os.path.splitext(os.path.relpath(target, tex_dir))[0]
            self.on_completion(0, [target_dir], option, point - len(prefix), point)
        listdir(view, dir, base, ext, on_done)


class LaTeXSqEnvCloserCommand(sublime_plugin.TextCommand):
    def run(self, edit, **args):
        view = self.view
        pattern = r'\\(begin|end)\{[^\}]+\}'
        b = []
        currpoint = view.sel()[0].b
        point = 0
        r = view.find(pattern, point)
        while r and r.end() <= currpoint:
            be = view.substr(r)
            point = r.end()
            if "\\begin" == be[0:6]:
                b.append(be[6:])
            else:
                if be[4:] == b[-1]:
                    b.pop()
                else:
                    sublime.error_message("\\begin%s closed with %s on line %d"
                    % (b[-1], be, view.rowcol(point)[0]))
                    return
            r = view.find(pattern, point)
        # now either b = [] or b[-1] is unmatched
        if b == []:
            sublime.error_message("Every environment is closed")
        else:
            # note the double escaping of \end
            #view.run_command("insertCharacters \"\\\\end" + b[-1] + "\\n\"")
            print("now we insert")
            # for some reason insert does not work
            view.run_command("insert_snippet",
                                {'contents': "\\\\end" + b[-1] + "\n"})
