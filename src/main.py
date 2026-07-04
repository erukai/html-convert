import sys
from pathlib import Path

import filtering
import parser
import injection

#wait for file/folder input
def file_input():
    # sys.argv[0] is the script name itself
    # sys.argv[1:] are the dropped files/folders
    if len(sys.argv) < 2:
        print("Please drag and drop a file or folder...")
        return

    for arg in sys.argv[1:]:
        path = Path(arg)
        if path.is_file():
            print(f"File dropped: {path}")
        elif path.is_dir():
            print(f"Folder dropped: {path}")
        else:
            print(f"Unknown type: {path}")

file_input()

#filtering
convert_num, ignore_num = filtering.filter_md()
md_dict = filtering.store_md()

#parsing
html_dict = parser.parse_md(md_dict, convert_num)


#injecting