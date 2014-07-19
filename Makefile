all:

push:
		git push

subtree-push:
		git subtree push --prefix=LaTeX-Extended git@github.com:randy3k/LaTeX-Extended.git master

subtree-pull:
		git subtree pull --prefix=LaTeX-Extended git@github.com:randy3k/LaTeX-Extended.git master --squash
