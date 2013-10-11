import sublime, sublime_plugin
import os
import re
from . misc import *
# from collections import OrderedDict

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
        if not view.score_selector(point, "text.tex.latex"):
            return
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

        sublime.status_message("Nothing to be auto completed.")

    def dispatch_ref(self, m, point):
        print("dispatching ref")
        view = self.view
        texroot = get_tex_root(view)
        tex_dir = os.path.dirname(texroot)
        braces, prefix = m.groups()

        completions = []
        search_in_tex(r'\\label\{([^\{\}]+)\}', texroot, tex_dir, completions)
        # to clear duplicate labels
        # completions = list(OrderedDict([(c['result'],c) for c in completions]).values())

        if prefix:
            completions = [c for c in completions if prefix in c['result']]
        else:
            prefix = ""
        open_brace = "" if braces else "{"
        close_brace = "" if braces else "}"

        if not completions:
            sublime.status_message("No label matches %s!" % (prefix,))
            return

        def on_done(i):
            if i<0: return
            ref = open_brace + completions[i]['result'] + close_brace
            view.run_command("latexsq_replace", {"a": point - len(prefix), "b": point, "replacement": ref})

        item = [[c['result'], os.path.relpath(c['file'], tex_dir)+":"+str(c['line'])] for c in completions]
        view.window().show_quick_panel(item, on_done)

    def dispatch_cite(self, m, point):
        print("dispatching cite")
        view = self.view
        texroot = get_tex_root(view)
        braces, prefix = m.groups()

        completions = []
        find_bib_records(texroot, completions)

        if prefix:
            completions = [c for c in completions \
                            if prefix.lower() in ("%s %s %s" % (c['keyword'],c['title'], c['author'])).lower()]
        else:
            prefix = ""
        open_brace = "" if braces else "{"
        close_brace = "" if braces else "}"

        if not completions:
            sublime.status_message("No bib record matches %s!" % (prefix,))
            return
        # sort by author
        completions = sorted(completions, key=lambda x: x['author'].lower())

        def on_done(i):
            if i<0: return
            cite = open_brace + completions[i]['keyword'] + close_brace
            view.run_command("latexsq_replace", {"a": point-len(prefix), "b": point, "replacement": cite})

        items = [[ "[" + c['author'] + "] " + c['title'], " (" + c['keyword'] + ") " + c['title'] ] for c in completions]
        view.window().show_quick_panel(items, on_done)

    def dispatch_label(self, m, point):
        print("dispatching label")
        view = self.view
        texroot = get_tex_root(view)
        tex_dir = os.path.dirname(texroot)
        braces, prefix = m.groups()
        print(prefix)

        if not prefix:
            return

        completions = []
        search_in_tex(r'\\label\{('+ prefix +'[^\{\}]+)\}', texroot, tex_dir, completions)
        print(completions)



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
