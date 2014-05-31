all:

push:
		git push

subtree-push:
		git subtree push --prefix=LaTeX-Extended syntax master

subtree-pull:
		git subtree pull --prefix=LaTeX-Extended syntax master --squash
