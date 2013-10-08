import sublime, sublime_plugin, os.path, subprocess, time
from . import getroot
import os
import shutil

class JumpToPdfCommand(sublime_plugin.TextCommand):
    def run(self, edit, **args):
        view = self.view
        point = view.sel()[0].end()
        if not view.score_selector(point, "text.tex.latex"):
            return

        s = sublime.load_settings("Rubber.sublime-settings")
        osx_settings = s.get("osx")
        linux_settings = s.get("linux")

        keep_focus = args["keep_focus"] if "keep_focus" in args else True
        forward_sync = args["forward_sync"] if "forward_sync" in args else False

        srcfile = self.view.file_name()
        root = getroot.get_tex_root(self.view)

        rootName, rootExt = os.path.splitext(root)
        pdffile = rootName + '.pdf'

        (line, col) = self.view.rowcol(self.view.sel()[0].end())
        print("Jump to: ", line,col)

        line += 1

        plat = sublime.platform()
        if plat == 'osx':
            args = ['osascript']
            apple_script = ('tell application "Skim"\n'
                                'if '+ str(not keep_focus)+' then activate\n'
                                'open POSIX file "' + pdffile + '"\n'
                                'revert front document\n'
                                'if '+ str(forward_sync)+' then\n'
                                    'tell front document to go to TeX line ' + str(line) + ' from POSIX file "' + srcfile + '"\n'
                                'end if\n'
                            'end tell\n')
            args.extend(['-e', apple_script])
            # print(apple_script)
            subprocess.Popen(args)


        elif plat == 'windows':
            # hide console
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            tasks = subprocess.Popen(["tasklist"], stdout=subprocess.PIPE,
                    startupinfo=startupinfo).communicate()[0]

            if "SumatraPDF.exe" not in str(tasks, encoding='utf8' ):
                print("Sumatra not running, launch it")
                try:
                    subprocess.Popen(["SumatraPDF", "-reuse-instance", pdffile])
                except:
                    sublime.error_message("Cannot launch SumatraPDF.")

                # wait 1/2 seconds so Sumatra comes up
                time.sleep(0.5)

            if forward_sync:
                subprocess.Popen(["SumatraPDF.exe","-reuse-instance","-forward-search", srcfile, str(line), pdffile])
            elif not keep_focus:
                subprocess.Popen(["SumatraPDF.exe","-reuse-instance","-forward-search", srcfile, str(0), pdffile])

        elif plat == 'linux':

            # the required scripts are in the 'evince' subdir
            ev_path = os.path.join(sublime.packages_path(), 'Rubber', 'evince')
            ev_fwd_exec = os.path.join(ev_path, 'evince_forward_search')
            ev_sync_exec = os.path.join(ev_path, 'evince_sync') # for inverse search!
            #print ev_fwd_exec, ev_sync_exec

            # Run evince if either it's not running, or if focus PDF was toggled
            # Sadly ST2 has Python <2.7, so no check_output:
            running_apps = subprocess.Popen(['ps', 'xw'], stdout=subprocess.PIPE).communicate()[0]
            # If there are non-ascii chars in the output just captured, we will fail.
            # Thus, decode using the 'ignore' option to simply drop them---we don't need them
            running_apps = running_apps.decode(sublime_plugin.sys.getdefaultencoding(), 'ignore')

            # Run scripts through sh because the script files will lose their exec bit on github

            # Get python binary if set:
            py_binary = linux_settings["python2"] or 'python'
            sb_binary = linux_settings["sublime"] or 'sublime-text'
            # How long we should wait after launching sh before syncing
            sync_wait = linux_settings["sync_wait"] or 1.0

            evince_running = ("evince " + pdffile in running_apps)
            if (not keep_focus) or (not evince_running):
                print("(Re)launching evince")
                subprocess.Popen(['sh', ev_sync_exec, py_binary, sb_binary, pdffile], cwd=ev_path)
                print("launched evince_sync")
                if not evince_running: # Don't wait if we have already shown the PDF
                    time.sleep(sync_wait)
            if forward_sync:
                subprocess.Popen([py_binary, ev_fwd_exec, pdffile, str(line), srcfile])
        else:
            sublime.error_message("Platform not supported!")

    def is_enabled(self):
        view = self.view
        point = view.sel()[0].end()
        return view.score_selector(point, "text.tex.latex")>0

    def is_visible(self):
        view = self.view
        point = view.sel()[0].end()
        return view.score_selector(point, "text.tex.latex")>0

