import optparse # because of 2.6 support
import sys
import threading
import time

from sarge import capture_stdout

def progress(capture, options):
    lines_seen = 0
    messages = {
        'line 25\n': 'Getting going ...\n',
        'line 50\n': 'Well on the way ...\n',
        'line 75\n': 'Almost there ...\n',
    }
    while True:
        s = capture.readline()
        if not s and lines_seen:
            break
        if options.dots:
            sys.stdout.write('.')
        else:
            msg = messages.get(s)
            if msg:
                sys.stdout.write(msg)
        lines_seen += 1
    if options.dots:
        sys.stdout.write('\n')
    sys.stdout.write('Done - %d lines seen.\n' % lines_seen)

def main():
    parser = optparse.OptionParser()
    parser.add_option('-n', '--no-dots', dest='dots', default=True,
                      action='store_false', help='Show dots for progress')
    options, args = parser.parse_args()
    p = capture_stdout('python /home/abhishek/Downloads/sarge/lister.py -d 0.1 -c 100', async=True)
    t = threading.Thread(target=progress, args=(p.stdout, options))
    t.start()
    while(p.returncodes[0] is None):
        # We could do other useful work here. If we have no useful
        # work to do here, we can call readline() and process it
        # directly in this loop, instead of creating a thread to do it in.
        p.commands[0].poll()
        time.sleep(0.05)
    t.join()

if __name__ == '__main__':
    sys.exit(main())
