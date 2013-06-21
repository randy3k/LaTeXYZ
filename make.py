import sublime, sublime_plugin
import sys, os, threading, time
import subprocess
import re
from . import getroot
from . import parser

class RubberThread(threading.Thread):

    # pass caller to make output and killing possible
    def __init__(self, caller):
        self.caller = caller
        threading.Thread.__init__(self)

    def run(self):
        print("Thread " + self.getName())
        t = time.time()
        caller = self.caller
        caller.output("[Compling " + caller.file_name + "]\n")
        sublime.set_timeout(caller.status_updater, 100)
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
            # reset PATH and working dir
            os.environ["PATH"] = old_path
            os.path.dirname(old_dir)
            return

        # reset PATH and working dir
        os.environ["PATH"] = old_path
        os.chdir(old_dir)

        # export proc in case it needs to be killed
        self.proc = proc
        # wait until proc finishes
        proc.wait()

        if hasattr(self, 'killed') and self.killed:
            caller.output("\n[Process killed!]\n")
            return

        caller.output_log(proc.returncode)
        elapsed = (time.time() - t)
        caller.output("\n\n[Done in %ss!]\n"% round(elapsed,2) )


class RubberCompileCommand(sublime_plugin.WindowCommand):
    def run(self, cmd="", file_regex="", path=""):
        view = self.window.active_view()
        if view.is_dirty():
            print("saving...")
            view.run_command('save')

        # Get parameters for Thread:
        self.file_name = getroot.get_tex_root(view)
        tex_dir = os.path.dirname(self.file_name)
        self.cmd = cmd + [self.file_name]
        self.path = path

        self.output_view = self.window.get_output_panel("exec")
        self.output_view.set_read_only(True)
        self.output_view.settings().set("result_file_regex", file_regex)
        self.output_view.settings().set("result_base_dir", tex_dir)

        if view.settings().get("show_panel_on_build", False):
            self.window.run_command("show_panel", {"panel": "output.exec"})

        print(self.cmd)

        # kill process if process exists
        if hasattr(self, 'thread') and self.thread.isAlive():
            self.output("[Process is running!]\n")
            self.output("\n[Killing running process!]\n")
            self.thread.proc.kill()
            self.thread.killed = True
            return

        self.thread = RubberThread(self)
        self.thread.start()

    def status_updater(self, status=0):
        status = status % 14
        before = min(status, 14-status)
        after = 7 - before
        self.window.active_view().set_status("rubber", "Compling [%s=%s]" % (" " * before, " " * after))
        if self.thread and self.thread.isAlive():
            sublime.set_timeout(lambda: self.status_updater(status+1), 100)
        else:
            self.window.active_view().erase_status("rubber")

    def output(self, data):
        self.output_view.run_command("rubber_output", {"characters": data})

    def output_log(self, returncode):
        logfile = os.path.splitext(self.file_name)[0] + ".log"

        check = parser.LogCheck()
        check.read(logfile)
        try:
            D  = check.parse()
            errors = []
            badboxes = []
            warnings = []
            fspecifiers = []

            for d in D:
                print(d)
                out = (d['file'], int(d['line']) if 'line' in d and d['line'] else 0, d['text'])
                if 'kind' in d:
                    if d['kind'] == "error":
                        errors.append("E: %s:%-4d  %s"% out)
                    elif d['kind'] == "warning" and ('Underfull' in d['text'] or 'Overfull' in d['text']):
                        badboxes.append("B: %s:%-4d  %s"% out)
                    elif d['kind'] == "warning" and 'float specifier changed' in d['text']:
                        fspecifiers.append("F: %s:%-4d  %s"% out)
                    elif d['kind'] == "warning":
                        warnings.append("W: %s:%-4d  %s"% out)
        except:
            self.output("\nCannot parse LaTeX log file: %s\n" % logfile)
            self.output("Report to Github.")
            return

        self.output("\n"+ str(len(errors)) + " Erorr(s), " + str(len(warnings)) +
                     " Warning(s), " + str(len(fspecifiers)) + " Float specifier(s) changed, and " +
                         str(len(badboxes)) + " Bad box(es)" + ".\n")

        if errors:
            self.output("\n[Error(s)]\n" + "\n".join(errors) + "\n")
        if warnings:
            self.output("\n[Warning(s)]\n" + "\n".join(warnings)+ "\n")
        if fspecifiers:
            self.output("\n[Float specifier(s) changed]\n" + "\n".join(fspecifiers)+ "\n")
        if badboxes:
            self.output("\n[Bad box(es)]\n" + "\n".join(badboxes)+ "\n")

        if returncode==0 and not errors:
            self.window.active_view().run_command("jump_to_pdf", {"keep_focus": True, "forward_sync": False})

class RubberOutputCommand(sublime_plugin.TextCommand):
    def run(self, edit, characters):
        self.view.set_read_only(False)
        self.view.insert(edit, self.view.size(), characters)
        self.view.set_read_only(True)