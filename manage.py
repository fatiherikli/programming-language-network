#!/usr/bin/env python
import os
import sys
#windows: set DJANGO_SETTINGS_MODULE

if __name__ == "__main__":

    this_dir=os.path.join(os.path.dirname(__file__),'')
    sys.path.append(this_dir)
    print "Append this: "+this_dir
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

    from django.core.management import execute_from_command_line
    print "execute_from_command_line: "+str(sys.argv)

    execute_from_command_line(sys.argv)
