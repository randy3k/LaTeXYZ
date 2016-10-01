import sublime
import sublime_plugin
import os
import re
from .utils import get_tex_root, search_in_tex, find_bib_records, listdir


class LatexBoxCompletionCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        sublime.set_timeout_async(self.run_async)

    def run_async(self):
        view = self.view
        point = view.sel()[0].end() if view.sel() else 0
        if not view.score_selector(point, "text.tex.latex"):
            return
        contentb = view.substr(sublime.Region(view.line(point).begin(), point))
        content = view.substr(view.line(point))

        m = re.match(r".*\\\w*[Rr]ef\*?(\{([a-zA-Z0-9_:-]*))?$", contentb)
        if m:
            self.dispatch_ref(m, point)
            return

        m = re.match(
            r"""
            .*\\(?:(?:[pP]aren|foot|[tT]ext|[sS]mart|super|[aA]|no|full|footfull)cite
            |[Cc]ite\w*|footcitetext)\*?
            (?:\[[^\]]*\])*
            (\{(?:[a-zA-Z0-9_:-]*\s*,\s*)*([a-zA-Z0-9_:-]*))?
            $
            """,
            contentb, re.VERBOSE
        )
        if m:
            self.dispatch_cite(m, point)
            return

        m = re.match(r".*\\label(\{([a-zA-Z0-9_:-]*))?$", contentb)
        if m:
            self.dispatch_label(m, point)
            return

        m = re.match(r".*\\includegraphics((?:\[[^\]]*\])?\{([^\}]*))?$", contentb)
        ext = ['.jpg', '.jpeg', '.bmp', '.pdf', '.ps', '.eps', '.png']
        if m:
            self.dispatch_listdir(m, point, ext)
            return

        m = re.match(r".*\\(?:input|include)(\{([^\}]*))?$", contentb)
        ext = ['.tex']
        if m:
            self.dispatch_listdir(m, point, ext)
            return

        m = re.match(r".*\\(?:bibliography|addbibresource(?:\[[^\]]*\])?)(\{([^\}]*))?$", contentb)
        ext = ['.bib']
        if m:
            self.dispatch_listdir(m, point, ext)
            return

        if re.match(r"^\s*$", content):
            self.dispatch_closeenv(point)
            return

        sublime.status_message("Nothing to be auto completed.")

    def replace(self, content, braces, a, b):
        open_brace = "" if braces else "{"
        close_brace = "" if braces else "}"
        rept = open_brace + content + close_brace
        self.view.run_command("latex_box_replace", {"a": a, "b": b, "replacement": rept})

    def dispatch_ref(self, m, point):
        print("dispatching ref")
        view = self.view
        tex_root = get_tex_root(view)
        tex_dir = os.path.dirname(tex_root)
        braces, prefix = m.groups()

        results = search_in_tex(r'\\label\{([^\{\}]+)\}', tex_root)

        if prefix:
            results = [r for r in results if prefix in r['result']]
        else:
            prefix = ""

        if not results:
            sublime.status_message("No label matches %s!" % (prefix,))
            return

        display = [[r['result'],
                    os.path.relpath(r['file'], tex_dir)+":"+str(r['line'])] for r in results]

        def on_done(action):
            if action < 0:
                return
            self.replace(display[action][0], braces, point - len(prefix), point)

        view.window().show_quick_panel(display, on_done)

    def dispatch_cite(self, m, point):
        print("dispatching cite")
        view = self.view
        tex_root = get_tex_root(view)
        braces, prefix = m.groups()

        results = find_bib_records(tex_root, by='author')

        if prefix:
            results = [r for r in results
                       if prefix.lower() in
                       ("%s %s %s" % (r['keyword'], r['title'], r['author'])).lower()]
        else:
            prefix = ""

        if not results:
            sublime.status_message("No bib record matches %s!" % (prefix,))
            return

        display = [[r['author'] +
                    (" (" + r['year'] + "): " if r['year'] else ": ") +
                    r['title'], " (" + r['keyword'] + ") " + r['title']]
                   for r in results]

        def on_done(action):
            if action < 0:
                return
            self.replace([r['keyword'] for r in results][action],
                         braces, point - len(prefix), point)

        view.window().show_quick_panel(display, on_done)

    def dispatch_label(self, m, point):
        print("dispatching label")

    def dispatch_listdir(self, m, point, ext):
        print("dispatching listdir")
        view = self.view
        tex_root = get_tex_root(view)
        tex_dir = os.path.dirname(tex_root)
        braces, prefix = m.groups()

        if not prefix:
            prefix = ""
        dir = os.path.join(tex_dir, os.path.dirname(prefix))
        base = os.path.basename(prefix)
        results = listdir(dir, base, ext)

        def on_done(action):
            if action < 0:
                return
            target = os.path.relpath(results[action], tex_dir)
            dirname = os.path.dirname(target)
            fname, ext = os.path.splitext(os.path.basename(target))
            if "." in fname:
                out = os.path.join(dirname, "{" + fname + "}" + ext).replace(os.sep, '/')
            else:
                out = os.path.join(dirname, fname).replace(os.sep, '/')
            self.replace(out, braces, point - len(prefix), point)

        if results:
            view.window().show_quick_panel([os.path.relpath(d, dir) for d in results], on_done)
        else:
            sublime.status_message("No matching files found.")

    def dispatch_closeenv(self, point):
        print("dispatching close env")
        view = self.view
        pt = 0
        env = []
        while 1:
            r = view.find(r'\\(begin|end)\{[^\}]+\}', pt)
            pt = r.end()
            if pt == -1 or pt >= point:
                break
            if view.scope_name(pt-1).find("comment") >= 0:
                continue
            thisenv = re.match(r'\\(begin|end)\{([^\}]+)\}', view.substr(r)).groups()
            if thisenv[0] == 'begin':
                env.append(thisenv)
            elif thisenv[1] == env[-1][1]:
                env.pop()
            else:
                sublime.error_message(
                    'Line %d: {%s} closed with {%s}.' %
                    (view.rowcol(pt)[0]+1, env[-1][1], thisenv[1])
                )

        view.run_command("insert_snippet", {'contents': "\\\\end{" + env[-1][1] + "}"})
        if view.settings().get('auto_indent'):
            view.run_command('reindent', {'force_indent': False})
        view.run_command("insert_snippet", {'contents': "\n"})
