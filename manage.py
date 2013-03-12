#!/usr/bin/env python
import os
import sys
import readline
import rlcompleter
readline.parse_and_bind("tab:complete")

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "xpertSummary.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
