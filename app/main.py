#! python3

# this example focuses on creating an environment env
#     https://docs.python.org/3/tutorial/venv.html
# First change directory to the app folder then:
#     python -m venv env
#     C:\Python34\python -m venv env
# Activate this environment on Windows:
#     env\Scripts\activate.bat
# You get an env prompt.
#     Type python and you get a python shell
#     Type pip to use the installer
#     Run any python program: it will use the virtual environment
# Deactivate the virtual environment with:
#     deactivate
# Run main.py from the env version of Python:
#     env\scripts\python.exe main.py


import sys


def main(arg):
    print('This is a main program.')
    return


if __name__ == "__main__":
    print(sys.argv[1:])
    print(sys.version)
    print(sys.exec_prefix)
    main(sys.argv)
    a = input('hit return')
