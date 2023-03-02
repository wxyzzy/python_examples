import sys, os
from pathlib import Path
from subprocess import Popen


python_path = Path(sys.executable)
script_path = Path(__file__).parent


def run_script(filename, args):
    command = [str(python_path), str(script_path / filename)] + list(args)
    print('running command:', command, file=sys.stderr)
    process = Popen(command, close_fds=False)
    return process


def main():
    r, w = os.pipe()
    os.set_inheritable(r, True)
    os.set_inheritable(w, True)
    print('created read/write file descriptors:', r, w, file=sys.stderr)

    sender = run_script('pipe_sender.py', [str(w)])
    receiver = run_script('pipe_receiver.py', [str(r)])

    sender.wait()
    receiver.wait()
    print('pipe finished.', file=sys.stderr)


if __name__ == '__main__':
    main()
