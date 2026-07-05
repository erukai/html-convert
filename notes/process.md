### Running the Program
1. run `activate.bat`
2. the batch script opens a terminal window and waits for input
3. if a markdown file or a folder is not received, cancel progress and wait for input again _(until timeout after 120 seconds.)_
4. if a markdown file or a folder is not received, start parsing by running `parser.py`

---

### Filter Files / Folders
1. open `convert/input-raw/`
2. iterate through contents
    -  if content is a file:
        - if `.md` extension: add to `convert/input-filtered/`. +1 to `convert_num`
        - if not `.md` extension: +1 to `ignore_num`
    - if content is a folder, repeat step 2


### Store Files Contents
1. create an empty dictionary `md_files = {}`
2. open `convert/input-filtered`
3. iterate through contents _(`.md` files)_
    - store the name of the file as a key in the `md_files` dictionary
    - read the file and store each line as an item in a list
    - store the list as the value to the key in the `md_files` dictionary




### Parsing Emphasis (bold and italic)
- current char: * ✅
- check next char:
    - if *: might be bold ✅
        check next char:
            - if *: it is both bold and italic
            - if not * and not space / end of line: it is bold
    - if not * and not space / end of line: it is italic


[~aijas~](https://google.com)