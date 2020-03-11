#!c:\users\administrator\desktop\cotan\venv\scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'pandas-profiling==2.5.0','console_scripts','pandas_profiling'
__requires__ = 'pandas-profiling==2.5.0'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('pandas-profiling==2.5.0', 'console_scripts', 'pandas_profiling')()
    )
