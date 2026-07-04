from pathlib import Path
import shutil

file_path = Path(__file__)  # current file
project_path = file_path.parent.parent

convert_path = project_path / "convert"
infilter_path = convert_path / "input-filtered"
inraw_path = convert_path / "input-raw"

#---

def copy_paste(): #copy file/folder path from input and paste to /convert/
    pass

#get files from convert folder

def filter_md():
    convert_num = 0
    ignore_num = 0

    def _filter(dir:Path):
        for entry in dir.iterdir():
            if entry.is_file():
                if entry.suffix == ".md":

                    # Copy file into folder
                    shutil.copy(entry, infilter_path)
                    convert_num += 1
                    
                else: #not a markdown file
                    ignore_num += 1

            elif entry.is_dir():
                _filter(entry) #recursion

    _filter(inraw_path)

    return (convert_num, ignore_num)


#read file and store contents in a dictionary tree (may use a lot of memory i think?)

def store_md():
    md_dict = {}

    for entry in infilter_path.iterdir():
        md_dict[entry.stem] = []

        with open(entry, "r") as f:
            for line in f:
                md_dict[entry.stem].append(line)

    return md_dict