import sublime, sublime_plugin, os, subprocess, time, threading
from . misc import *
import sys
if sys.platform == "win32":
    if sys.version_info >= (3, 0, 0):
        from winreg import *
    else:
        from _winreg import *

def SumatraPDF():
    try:
        akey=OpenKey(HKEY_LOCAL_MACHINE, "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\App Paths\\SumatraPDF.exe", 0, KEY_WOW64_64KEY|KEY_READ)
        path=QueryValueEx(akey, "")[0]
    except:
        print("Cannot find SumatraPDF from registry. Check if SumatraPDF has been installed!")
        return
    return path

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

        s = view.settings()

        bring_forward = args["bring_forward"] if "bring_forward" in args else False
        forward_sync = args["forward_sync"] if "forward_sync" in args else False

        srcfile = self.view.file_name()
        tex_root = get_tex_root(self.view)

        pdffile = os.path.splitext(tex_root)[0] + '.pdf'

        (line, col) = self.view.rowcol(self.view.sel()[0].end())
        line += 1

        plat = sublime.platform()
        if plat == 'osx':
            osx_settings = s.get("osx")

            args = ['osascript']
            apple_script = ('tell application "Skim"\n'
                                'if '+ str(bring_forward)+' then activate\n'
                                'open POSIX file "' + pdffile + '"\n'
                                'revert front document\n'
                                'if '+ str(forward_sync)+' then\n'
                                    'tell front document to go to TeX line ' + str(line) + ' from POSIX file "' + srcfile + '"\n'
                                'end if\n'
                            'end tell\n')
            # print(apple_script)
            args.extend(['-e', apple_script])
            subprocess.Popen(args)


        elif plat == 'windows':
            # hide console
            windows_settings = s.get("windows")

            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            tasks = subprocess.check_output(["tasklist"], startupinfo=startupinfo)
            sumatra_is_running = "SumatraPDF.exe" in str(tasks, encoding='utf8' )
            try:
                sumatrapdf = windows_settings["sumatrapdf"] if "sumatrapdf" in windows_settings else SumatraPDF()
                if not sumatra_is_running:
                    print("SumatraPDF not running, launch it")
                    subprocess.Popen([sumatrapdf, pdffile])
                    if not sumatra_is_running: time.sleep(1)
                elif bring_forward:
                    subprocess.Popen([sumatrapdf, "-reuse-instance", pdffile])
            except:
                print("Cannot launch SumatraPDF!")
                return

            if forward_sync:
                subprocess.Popen([sumatrapdf,"-reuse-instance","-forward-search", srcfile, str(line), pdffile])

        elif plat == 'linux':

            linux_settings = s.get("linux")
            evince_sync = os.path.join(sublime.packages_path(), 'LaTeXSq', 'evince_sync')

            tasks = subprocess.check_output(['ps', 'xw'])

            subl = linux_settings["sublime"] if "sublime" in linux_settings else "subl"

            evince_is_running = "evince " + pdffile in str(tasks, encoding='utf8')
            if bring_forward or not evince_is_running:
                args = ["python", evince_sync, "backward", pdffile, subl + " %f:%l"]
                EvinceThread(args).start()
                if not evince_is_running: time.sleep(1)

            if forward_sync:
                subprocess.Popen(["python", evince_sync, "forward", pdffile, str(line), srcfile])


    def is_enabled(self):
        view = self.view
        point = view.sel()[0].end()
        return view.score_selector(point, "text.tex.latex")>0

    def is_visible(self):
        view = self.view
        point = view.sel()[0].end()
        return view.score_selector(point, "text.tex.latex")>0

