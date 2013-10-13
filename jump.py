import sublime, sublime_plugin, os, subprocess, time, threading
from . misc import *

class EvinceThread(threading.Thread):
    def __init__(self, args):
        self.args = args
        threading.Thread.__init__(self)

    def run(self):
        ev_sync = subprocess.Popen(self.args)
        ev = subprocess.Popen(['evince', self.args[3]])
        ev.wait()
        ev_sync.kill()

class JumpToPdfCommand(sublime_plugin.TextCommand):
    def run(self, edit, **args):
        view = self.view
        point = view.sel()[0].end()
        if not view.score_selector(point, "text.tex.latex"):
            return

        s = sublime.load_settings("LaTeXSq.sublime-settings")

        bring_front = args["bring_front"] if "bring_front" in args else False
        forward_sync = args["forward_sync"] if "forward_sync" in args else False

        srcfile = self.view.file_name()
        root = get_tex_root(self.view)

        rootName, rootExt = os.path.splitext(root)
        pdffile = rootName + '.pdf'

        (line, col) = self.view.rowcol(self.view.sel()[0].end())
        line += 1

        plat = sublime.platform()
        if plat == 'osx':
            osx_settings = s.get("osx")

            args = ['osascript']
            apple_script = ('tell application "Skim"\n'
                                'if '+ str(bring_front)+' then activate\n'
                                'open POSIX file "' + pdffile + '"\n'
                                'revert front document\n'
                                'if '+ str(forward_sync)+' then\n'
                                    'tell front document to go to TeX line ' + str(line) + ' from POSIX file "' + srcfile + '"\n'
                                'end if\n'
                            'end tell\n')
            args.extend(['-e', apple_script])
            subprocess.Popen(args)


        elif plat == 'windows':
            # hide console
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            tasks = subprocess.check_output(["tasklist"], startupinfo=startupinfo)

            sumatra_is_running = "SumatraPDF.exe" in str(tasks, encoding='utf8' )
            if bring_front or not sumatra_is_running:
                print("Sumatra not running, launch it")
                try:
                    subprocess.Popen(["SumatraPDF", "-reuse-instance", pdffile], startupinfo=startupinfo)
                except:
                    print("Cannot launch SumatraPDF.")
                    return
                if not sumatra_is_running: time.sleep(1)

            if forward_sync:
                subprocess.Popen(["SumatraPDF.exe","-reuse-instance","-forward-search", srcfile, str(line), pdffile], startupinfo=startupinfo)

        elif plat == 'linux':

            linux_settings = s.get("linux")
            evince_sync = os.path.join(sublime.packages_path(), 'LaTeXSq', 'evince_sync')

            tasks = subprocess.check_output(['ps', 'xw'])

            python = linux_settings["python"]
            subl = linux_settings["sublime"]

            evince_is_running = "evince " + pdffile in str(tasks, encoding='utf8')
            if bring_front or not evince_is_running:
                args = [python, evince_sync, "backward", pdffile, subl + " %f:%l"]
                EvinceThread(args).start()
                if not evince_is_running: time.sleep(1)

            if forward_sync:
                subprocess.Popen([python, evince_sync, "forward", pdffile, str(line), srcfile])


    def is_enabled(self):
        view = self.view
        point = view.sel()[0].end()
        return view.score_selector(point, "text.tex.latex")>0

    def is_visible(self):
        view = self.view
        point = view.sel()[0].end()
        return view.score_selector(point, "text.tex.latex")>0

