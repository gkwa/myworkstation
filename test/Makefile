prep: FORCE
	rm -f Brewfile*
	python main.py
	perl -i -ne 'print if(!m{cask.*virtualbox.*} and !m{^mas })' Brewfile*

FORCE: