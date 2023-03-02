# Localization


import locale as loc
import time
import gettext


loc.setlocale(loc.LC_ALL, '')
print(loc.getlocale())
print(loc.currency(350))
print(time.strftime("%x %X", time.localtime()))


# This uses files of the form, localedir/sw/LC_MESSAGES/base.mo
ldir = 'localedir\\'
lang = gettext.translation('base', localedir=ldir, languages=['sw'])
lang.install()
_ = lang.gettext
_ = lambda s: s

def foo():
	print(_("This is some text"))
	print(_("This is a warning"))
	print(_("This is an error"))

foo()
