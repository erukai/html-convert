### Running the Script

1. The script or program is meant to be run through the batch file `activate.bat`
2. Clicking `activate.bat` will open a terminal using your computer's default shell program _(e.g. Command Prompt, PowerShell, Bash, etc.)_.
3. The terminal will prompt you to either:
    - enter the absolute path of the Markdown file you want to convert
    - drag-and-drop the file
4. If you want to convert multiple Markdown files, put the files in a folder, then in the terminal, enter the path to the folder or drag-and-drop it.
5. You can only enter the path of a single file/folder. Likewise, you can only drag-and-drop a single file/folder. Therefore, if you intend to input multiple files, make sure you place all those files in a single folder before you send it to the terminal.

### File Conversion
1. If you enter a file that is not a Markdown file _(extension is not `.md`)_, the terminal will cancel the conversion, and you must send the file again.
2. If you enter a folder that includes a non-Markdown file, the program will still run but only converts Markdown files in the folder. After all conversion is finished, the terminal will print the result of the conversion like this:
```
x Markdown files successfully converted to HTML; y files ignored.
```
- _(`x` and `y` represent the amount of files involved.)_
3. Once the conversion process is finished, your terminal will prompt you to pick a location to save the file. If you input a single Markdown file, the terminal will return a single HTML file. If you input a folder, the terminal will return a `.zip` file.