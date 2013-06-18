import sublime, sublime_plugin
import sys, os, threading, time
import subprocess
import re
from . import getroot
from . import parser

class LaTeXThread(threading.Thread):
    killed = False

    def __init__(self, caller):
        self.caller = caller
        threading.Thread.__init__(self)

    def run(self):
        print("Welcome to thread " + self.getName())
        t = time.time()
        caller = self.caller
        caller.output("[Compling " + caller.file_name + "]\n")
        if caller.path:
            old_path = os.environ["PATH"]
            os.environ["PATH"] = os.path.expandvars(caller.path)

        plat = sublime.platform()
        old_dir = os.getcwd()
        os.chdir(os.path.dirname(caller.file_name))
        try:
            if plat == "windows":
                # make sure console does not come up
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                proc = subprocess.Popen(caller.cmd, startupinfo=startupinfo)
            else:
                proc = subprocess.Popen(caller.cmd)
        except:
            caller.output("[Cannot compile!]\n")
            os.environ["PATH"] = old_path
            os.path.dirname(old_dir)
            return

        # reset PATH and working dir
        os.environ["PATH"] = old_path
        os.chdir(old_dir)

        # wait until proc finishes
        self.proc = proc
        proc.wait()

        # # print(proc.returncode)
        if self.killed:
            caller.output("[Process killed!]\n")
            return

        caller.finish(proc.returncode)
        elapsed = (time.time() - t)
        caller.output("[Process killed!]\n")
        caller.output("\n\n[Done in %ss!]\n"% round(elapsed,2) )


class MakePdfCommand(sublime_plugin.WindowCommand):
    thread = None

    def run(self, cmd="", file_regex="", path=""):
        view = self.window.active_view()
        if view.is_dirty():
            print("saving...")
            view.run_command('save')

        # Get parameters for Thread:
        self.file_name = getroot.get_tex_root(view)
        self.cmd = cmd + [self.file_name]
        self.path = path

        self.output_view = self.window.get_output_panel("exec")
        self.output_view.set_read_only(True)
        self.output_view.settings().set("result_file_regex", file_regex)

        if view.settings().get("show_panel_on_build", False):
            self.window.run_command("show_panel", {"panel": "output.exec"})

        print(self.cmd)

        if self.thread and self.thread.isAlive():
            self.output("[Killing running process!]\n")
            self.thread.proc.kill()
            self.thread.killed = True
            time.sleep(0.5)

        self.thread = LaTeXThread(self)
        self.thread.start()

    def output(self, data):
        view = self.output_view
        self.output_view.set_read_only(False)
        # view.run_command("insert", {"characters": data})
        view.run_command("do_output", {"characters": data})
        self.output_view.set_read_only(True)

    def finish(self, returncode):
        base = os.path.splitext(self.file_name)[0]
        tex_dir = os.path.dirname(self.file_name)
        logfile = base + ".log"
        os.chdir(tex_dir)

        check = parser.LogCheck()
        check.read(logfile)

        D = check.parse(errors=1, boxes=1, refs=1, warnings=1)

        errors = []
        badboxes = []
        warnings = []

        for d in D:
            out = (os.path.abspath(d['file']), int(d['line']) if 'line' in d else 0, d['text'])
            # print(d)
            if 'kind' in d:
                if d['kind'] == "error":
                    errors.append("E: %s:%d   %s"% out)
                elif d['kind'] == "warning" and ('Underfull' in d['text'] or 'Overfull' in d['text']):
                    badboxes.append("B: %s:%d   %s"% out)
                elif d['kind'] == "warning":
                    warnings.append("W: %s:%d   %s"% out)

        if errors:
            self.output("\n[Errors]\n" + "\n".join(errors) + "\n")
        if warnings:
            self.output("\n[Warnings]\n" + "\n".join(warnings)+ "\n")
        if badboxes:
            self.output("\n[Badboxes]\n" + "\n".join(badboxes))

        if returncode==0 and not errors:
            self.window.active_view().run_command("jump_to_pdf", {"keep_focus": True, "forward_sync": False})

class DoOutputCommand(sublime_plugin.TextCommand):
    def run(self, edit, characters):
        self.view.insert(edit, self.view.size(), characters)