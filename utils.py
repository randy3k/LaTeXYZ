import sublime
import sublime_plugin
import os
import re
import sys
import subprocess
from .constants import latex_unicode_map


# sublime wrapper for insert
class LatexBoxInsertCommand(sublime_plugin.TextCommand):
    def run(self, edit, content, before=0, after=0):
        sel = [(s.begin(), s.end()) for s in self.view.sel()]
        for (a, b) in reversed(sel):
            region = sublime.Region(a-before, b+after)
            self.view.replace(edit, region, content)


# sublime wrapper for replacement
class LatexBoxReplaceCommand(sublime_plugin.TextCommand):
    def run(self, edit, a, b, replacement):
        region = sublime.Region(a, b)
        self.view.replace(edit, region, replacement)
        self.view.sel().clear()
        self.view.sel().add(a+len(replacement))


class LatexBoxOutputCommand(sublime_plugin.TextCommand):
    def run(self, edit, characters):
        self.view.set_read_only(False)
        self.view.insert(edit, self.view.size(), characters)
        self.view.set_read_only(True)


def check_program(args, env):
    try:
        if sys.platform == "win32":
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            subprocess.check_output(args, startupinfo=startupinfo, env=env)
        else:
            subprocess.check_output(args, env=env)
    except:
        return False
    return True


def get_tex_root(view):
    # 1) First, try to test if the currect file is a self contained tex file
    # 2) Second, check for TEX root
    # 3) Third, check for project setting
    # 4) search of local .synctex.gz and .pdf
    # 5) If all above fail, use current file

    file_name = view.file_name()
    file_dir = os.path.dirname(file_name)
    last_row = view.rowcol(view.size())[0]
    # check frist 5 rows only
    for i in range(0, min(5, last_row)):
        line = view.substr(view.line(view.text_point(i, 0)))
        if re.match(r"\s*\\documentclass", line):
            print("!TEX root = ", file_name)
            return file_name
        mroot = re.match(r"%\s*!tex\s*root *= *(.*tex)\s*$", line, re.IGNORECASE)
        if mroot:
            tex_root = os.path.join(file_dir, mroot.group(1))
            tex_root = os.path.abspath(os.path.normpath(tex_root))
            if os.path.isfile(tex_root):
                print("!TEX root = ", tex_root)
                return tex_root

    folders = view.window().folders()
    if folders:
        old_dir = os.getcwd()
        os.chdir(folders[0])
        try:
            tex_root = os.path.abspath(view.settings().get('TEXroot'))
            if os.path.isfile(tex_root):
                print("!TEX root = ", tex_root)
                os.chdir(old_dir)
                return tex_root
        except:
            pass
        os.chdir(old_dir)

    sync = [f for f in os.listdir(file_dir) if f.endswith(".synctex.gz")]
    if len(sync) == 1:
        tex_root = os.path.join(file_dir, sync[0].replace(".synctex.gz", ".tex"))
        if os.path.isfile(tex_root):
            print("!TEX root = ", tex_root)
            return tex_root

    pdf = [f for f in os.listdir(file_dir) if f.endswith(".pdf")]
    if len(pdf) == 1:
        tex_root = os.path.join(file_dir, pdf[0].replace(".pdf", ".tex"))
        if os.path.isfile(tex_root):
            print("!TEX root = ", tex_root)
            return tex_root

    print("!TEX root = ", file_name)
    return file_name


# List a directory using quick panel
def listdir(dir, base, ext):
    ret = []
    for (d, _, files) in os.walk(dir):
        for f in files:
            if not ext or os.path.splitext(f)[1].lower() in ext:
                if not base or base.lower() in f.lower():
                    ret.append(os.path.normpath(os.path.join(d, f)))
    return ret


# search for pattern in the tex files
def search_in_tex(rexp, src, tex_dir=None, recursive=True):
    print("Scanning file: " + repr(src))
    results = []
    if not tex_dir:
        tex_dir = os.path.dirname(src)
    try:
        src_file = open(src, "r", encoding="utf-8")
        src_content = src_file.readlines()

        for line, c in enumerate(src_content):
            this_result = re.findall(rexp, re.sub(r"(?<![\\])(\\\\)*%.*", "", c))
            if not this_result:
                continue
            results += [{"file": src, "line": line+1, "result": t} for t in this_result]

        # recursive search
        if recursive:
            for f in re.findall(r'\\(?:input|include)\{([^\{\}]+)\}', "\n".join(src_content)):
                if f[-4:].lower() != ".tex":
                    f = f + ".tex"
                f = os.path.normpath(os.path.join(tex_dir, f))
                results += search_in_tex(rexp, f, tex_dir)

    except IOError:
        print("Cannot open file: %s" % src)

    return results


def decode_latex(name):
    for u, latex in latex_unicode_map:
        name = name.replace(latex, u)
    name = name.replace("{", "").replace("}", "")
    return name


# find bibtex records
def find_bib_records(tex_root, by=None):
    tex_dir = os.path.dirname(tex_root)
    bib_files = search_in_tex(r'\\(?:bibliography|addbibresource)\{([^\}]+)\}', tex_root, tex_dir)

    bib_files = [subitem.strip() for item in bib_files for subitem in item['result'].split(",")]
    bib_files = [f+".bib" if f[-4:].lower() != ".bib" else f for f in bib_files]
    bib_files = [os.path.normpath(os.path.join(tex_dir, f)) for f in bib_files]
    bib_files = list(set(bib_files))
    # print(bib_files)

    if not bib_files:
        sublime.status_message("No bib files found!")
        return

    bibtextype = ["article", "book", "mvbook", "inbook", "bookinbook", "suppbook",
                  "booklet", "collection", "mvcollection", "incollection",
                  "suppcollection", "manual", "misc", "online", "patent",
                  "periodical", "suppperiodical", "proceedings", "mvproceedings",
                  "inproceedings", "reference", "mvreference", "inreference",
                  "report", "set", "thesis", "unpublished", "conference",
                  "electronic", "mastersthesis", "phdthesis", "techreport", "www"]
    keywordp = re.compile(r'^@(' + '|'.join(bibtextype) + r')\{(.*?)[\} ,"]*$', re.IGNORECASE)
    titlep = re.compile(r'\btitle\s*=\s*(?:\{+|")\s*(.*?)[\} ,"]*$', re.IGNORECASE)
    authorp = re.compile(r'\bauthor\s*=\s*(?:\{+|")\s*(.*?)[\} ,"]*$', re.IGNORECASE)
    yearp = re.compile(r'\byear\s*=\s*(?:\{+|")\s*(.*?)[\} ,"]*$', re.IGNORECASE)
    publisherp = re.compile(r'\bpublisher\s*=\s*(?:\{+|")\s*(.*?)[\} ,"]*$', re.IGNORECASE)

    results = []
    for bibfname in bib_files:
        try:
            bibf = open(bibfname, encoding="utf-8")
        except IOError:
            print("Cannot open file: %s" % (bibfname,))
            continue
        else:
            bib = bibf.readlines()
            bibf.close()

        lines = [i+1 for i, item in enumerate(bib) if keywordp.search(item)]
        print("Found %d bib records in %s" % (len(lines), bibfname))

        nextline = lines[1:]+[len(bib)+1]
        for i, line in enumerate(lines):
            j = line
            keyword = keywordp.search(bib[j-1]).group(2)
            title = author = year = publisher = ""
            while j < nextline[i]:
                content = bib[j-1]
                if not title:
                    t = titlep.search(content)
                    if t:
                        title = decode_latex(t.group(1))
                if not author:
                    a = authorp.search(content)
                    if a:
                        author = decode_latex(a.group(1))
                if not year:
                    y = yearp.search(content)
                    if y:
                        year = y.group(1)
                if not publisher:
                    p = publisherp.search(content)
                    if p:
                        publisher = p.group(1)
                if title and author and year:
                    break
                j += 1
            if not author:
                author = publisher
            results.append({'keyword': keyword, 'title': title, 'author': author,
                            'year': year, 'file': bibfname, 'line': line})

    if by:
        results = sorted(results, key=lambda x: x[by].lower())
    return results
