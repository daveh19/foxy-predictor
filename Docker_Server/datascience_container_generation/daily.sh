#!/bin/bash
# This script is to be run every morning at 2:00am after the database has loaded new data.
# Daily results of any new data will be displayed on the webserver as a new tab.

# After echo specify the arguments to be entered
# Output piped to a log file with timestamp
# Currently only specifying one option till the interface command is fixed
echo d | python ./Commandline_Interface/interface.py > $(date +%Y-%m-%d_%H:%M).log
