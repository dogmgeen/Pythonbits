PYTHON=python2
NOSE=/usr/local/bin/nosetests-2.7

all: clean dist install

dist:
		$(PYTHON) setup.py sdist

install:
		pip2 uninstall pythonbits
		pip2 install dist/Pythonbits-2.0.0.tar.gz

clean:
		rm -r dist/

test:
		$(NOSE) --with-progressive --logging-clear-handlers
