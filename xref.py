import sublime, sublime_plugin
import os, os.path
import re
from . import getroot

def match(rex, str):
    m = rex.match(str)
    if m:
        return m.group(0)
    else:
        return None

class LatexQReplaceCommand(sublime_plugin.TextCommand):
    def run(self, edit, a, b, replacement):
        region = sublime.Region(a, b)
        self.view.replace(edit, region, replacement)
        self.view.sel().clear()
        self.view.sel().add(a+len(replacement))

class LatexRefCiteCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        point = view.sel()[0].end()
        if not view.score_selector(point, "text.tex.latex"):
            return

        line = view.substr(sublime.Region(view.line(point).begin(), point))
        line = line[::-1]

        rex_ref = re.compile(r"([^{]*?)(\{)?fer(?:qe|egap)?\\")
        rex_cite = re.compile(r"([^,{ ]*?)[^{]*?(\{)?[a-zA-Z_*]*etic\\")

        root = getroot.get_tex_root(view)

        # dispatching ref
        if re.match(rex_ref, line):
            expr = match(rex_ref, line)
            prefix, paren = rex_ref.match(expr).groups()
            prefix = prefix[::-1]

            completions = []
            find_labels_in_files(os.path.dirname(root), root, completions)
            completions = list(set(completions))

            if prefix:
                completions = [c for c in completions if prefix in c]
            open_brace = "" if paren else "{"
            close_brace = "" if paren else "}"

            if not completions:
                sublime.error_message("No label matches %s !" % (prefix,))
                return

            # Note we now generate refs on the fly. Less copying of vectors! Win!
            def on_done(i):
                # Allow user to cancel
                if i<0: return
                ref = open_brace + completions[i] + close_brace
                view.run_command("latex_q_replace", {"a": point - len(prefix), "b": point, "replacement": ref})

            view.window().show_quick_panel(completions, on_done)

        # dispatching cite
        elif re.match(rex_cite, line):
            expr = match(rex_cite, line)
            prefix, paren= rex_cite.match(expr).groups()
            prefix = prefix[::-1]

            completions = []
            find_bib_records(root, completions)

            # filter against keyword, title, or author
            if prefix:
                completions = [comp for comp in completions if prefix.lower() in "%s %s %s" \
                                                        % (comp[0].lower(),comp[1].lower(), comp[2].lower())]
            open_brace = "" if paren else "{"
            close_brace = "" if paren else "}"

            # Note we now generate citation on the fly. Less copying of vectors! Win!
            def on_done(i):
                # Allow user to cancel
                if i<0: return
                cite = open_brace + completions[i][0] + close_brace
                view.run_command("latex_q_replace", {"a": point-len(prefix), "b": point, "replacement": cite})

            items = [[ "[" + author + "] " + title, title + " (" + keyword + ")"] for (keyword,title, author) in completions]
            view.window().show_quick_panel(items, on_done)

        else:
            sublime.error_message("Ref/cite: unrecognized format.")
            return


def find_bib_files(rootdir, src, bibfiles):
    if src[-4:].lower() != ".tex":
        src = src + ".tex"

    file_path = os.path.normpath(os.path.join(rootdir,src))
    print("Searching file: " + repr(file_path))

    try:
        src_file = open(file_path, "r")
    except IOError:
        sublime.status_message("Rubber WARNING: cannot open included file " + file_path)
        print("WARNING! I can't find it! Check your \\include's and \\input's.")
        return

    src_content = re.sub(r"(?<![\\])(\\\\)*%.*","",src_file.read())
    bibtags =  re.findall(r'\\bibliography\{[^\}]+\}', src_content)

    # extract absolute filepath for each bib file
    for tag in bibtags:
        bfiles = re.search(r'\{([^\}]+)', tag).group(1).split(',')
        for bf in bfiles:
            if bf[-4:].lower() != '.bib':
                bf = bf + '.bib'
            # We join with rootdir - everything is off the dir of the master file
            bf = os.path.normpath(os.path.join(rootdir,bf))
            bibfiles.append(bf)

    # search through input tex files recursively
    for f in re.findall(r'\\(?:input|include)\{[^\}]+\}',src_content):
        input_f = re.search(r'\{([^\}]+)', f).group(1)
        find_bib_files(rootdir, input_f, bibfiles)

def find_bib_records(root, completions):

    bib_files = []
    find_bib_files(os.path.dirname(root), root, bib_files)
    # remove duplicate bib files
    bib_files = ([x.strip() for x in bib_files])
    bib_files = list(set(bib_files))

    if not bib_files:
        sublime.error_message("No bib files found!") # here we can!
        return []

    kp = re.compile(r'@[^\{]+\{(.+),')
    tp = re.compile(r'\btitle\s*=\s*(?:\{+|")\s*(.+)', re.IGNORECASE)  # note no comma!
    ap = re.compile(r'\bauthor\s*=\s*(?:\{+|")\s*(.+)', re.IGNORECASE)

    for bibfname in bib_files:
        try:
            bibf = open(bibfname)
        except IOError:
            print("Cannot open bibliography file %s !" % (bibfname,))
            sublime.status_message("Cannot open bibliography file %s !" % (bibfname,))
            continue
        else:
            bib = bibf.readlines()
            bibf.close()

        # note Unicode trickery
        keywords = [kp.search(line).group(1) for line in bib if line[0] == '@']
        titles = [tp.search(line).group(1) for line in bib if tp.search(line)]
        authors = [ap.search(line).group(1) for line in bib if ap.search(line)]


        if len(keywords) != len(titles):
            print("Bibliography " + repr(bibfname) + " is broken!")
            return

        print("Found %d total bib entries" % (len(keywords),))

        # Filter out }'s and ,'s at the end. Ugly!
        nobraces = re.compile(r'\s*,*\}*(.+)')
        titles = [nobraces.search(t[::-1]).group(1)[::-1] for t in titles]
        authors = [nobraces.search(a[::-1]).group(1)[::-1] for a in authors]
        completions += list(zip(keywords, titles, authors))


def find_labels_in_files(rootdir, src, labels):
    if src[-4:].lower() != ".tex":
        src = src + ".tex"

    file_path = os.path.normpath(os.path.join(rootdir, src))
    print("Searching file: " + repr(file_path))

    try:
        with open(file_path, "r") as src_file:
            src_content = re.sub(r"(?<![\\])(\\\\)*%.*", "", src_file.read())
            labels += re.findall(r'\\label\{([^\{\}]+)\}', src_content)
    except IOError:
        sublime.status_message("Rubber WARNING: cannot find included file " + file_path)
        print("WARNING! I can't find it! Check your \\include's and \\input's.")
        return

    # search through input tex files recursively
    for f in re.findall(r'\\(?:input|include)\{([^\{\}]+)\}', src_content):
        find_labels_in_files(rootdir, f, labels)


