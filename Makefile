test: FORCE
	rm -f test/Brewfile*
	cd test && python main.py

FORCE: