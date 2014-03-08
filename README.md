# Purpose

If you are a heavy Dropbox user like me, you probably already dealt with the annoying conflicted files that sometimes get generated. This script provides a quick interactive way for handling those files. In particular, it allows you to:
-   quickly pick one of the conflicted file versions, removing the others;
-   run a command (like diff) before picking, to better understand what to keep.

# Usage

1.  Backup your important files! (Script still experimental)

2.  Optionally, change the `extrakeys` variable at the top of the script to support further actions to handle conflicted files

3.  In your favourite shell, launch the script with something like

        python dropbox_cleaner.py /path/to/root/dir/for/cleaning

4.  Follow the instructions during interaction (type `h` for help)

# DISCLAIMER

THIS SOFTWARE IS PRIVIDED "AS IS" AND COMES WITH NO WARRANTY. USE AT YOUR OWN RISK. IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING BUT NOT LIMITED TO LOSS OR CORRUPTION OF DATA). USE AT YOUR OWN RISK.