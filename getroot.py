import os.path, re

# 1) First, try to test if the currect file is a self contained tex file
# 2) Second, check for TEX root
# 3) Third, check for project
# 4) If all above fail, use current file

def get_tex_root(view):

	texFile = view.file_name()
	last_row = view.rowcol(view.size())[0]
	# check frist 5 rows only
	for i in range(0,min(5,last_row)):
		line = view.substr(view.line(view.text_point(i,0)))
		if re.match(r"\s*\\documentclass",line):
			print("!TEX root = ", texFile)
			return texFile
		mroot = re.match(r"%\s*!TEX\s*root *= *(.*(tex|TEX))\s*$",line)
		if mroot:
			(texPath, texName) = os.path.split(texFile)
			(rootPath, rootName) = os.path.split(mroot.group(1))
			root = os.path.join(texPath,rootPath,rootName)
			root = os.path.abspath(os.path.normpath(root))
			if os.path.isfile(root):
				print("!TEX root = ", root)
				return root

	folders = view.window().folders()
	if folders:
		os.chdir(folders[0])
		try:
			root = os.path.abspath(view.settings().get('TEXroot'))
			if os.path.isfile(root):
				print("!TEX root = ", root)
				return root
		except:
			pass

	print("!TEX root = ", texFile)
	return texFile
