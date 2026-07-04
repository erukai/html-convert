import re

def parse_md(md_dict:dict, convert_num):
    html_dict = {}

    #iterate through the dictionary file by file
    for i, file_name, file_content in enumerate(md_dict.items(), 1):
        print(f"Converting file... ({i}/{convert_num})")

        #create MarkdownParse object per file
        file = MarkdownParser(file_content)
        parsed_file = file.parse() # list

        #execute line parser
        '''html_dict[file_name] = parsed_file'''
        





    return html_dict
        
#---

class MarkdownParser:
    def __init__(self, lines: list):
        self.lines = lines #list
        self.cursor = 0 #position of cursor in a line, starts at 0

        self.state = ParserState()
        self.text = None

    #---

    #helper methods, not to be accessed outside, but to be used by other methods in this class
    def current(self): #check char on cursor
        return self.text[self.cursor]
    
    def peek(self): #check char ahead cursor
        return self.text[self.cursor+1]

    def turn(self): #check char behind cursor
        return self.text[self.cursor-1]

    def advance(self, n=1): #move the cursor to the next column
        self.cursor += n

    #---

    def parse(self) -> list:
        for line in self.lines: #move line by line
            self.text = line

            while self.cursor < len(self.text):
                char = self.text[self.cursor]

                self.parse_check(char)
                self.advance() #move to parse_check() later

            #end of line:
            self.cursor = 0
            




    def parse_check(self, char):
        #some formatting only works if the symbol is at the start of the line.
        #if current cursor is NOT at the start, ignore those formattings

        match self.current():
            case "*":
                if self.peek() == "*":
                    pass

            case "_":
                fork_underscore(self)

            case "~":
                fork_tilde(self)

            case "`":
                fork_backtick(self)

            case "-":
                fork_hyphen(self)

            case "#" if self.cursor == 0:
                parse_header(self)

            case ">" if self.cursor == 0:
                parse_quote(self)

            case "^":
                parse_sup(self)

            case "()": #special case, change later
                parse_link(self)


class ParserState():
    def __init__(self):
        self.delimiter_stack = []

        #entire line
        self.is_line_header = False
        self.is_line_quote = False
        self.is_line_hr = False

        #single line
        self.is_code = False
        self.is_link_text = False
        self.is_link_url = False

        #multi-line
        self.is_bold = False
        self.is_italic = False
        self.is_strikethrough = False
        self.is_code_block = False

        self.text = False

#----------

#`?:` non-capturing group
#`?<=` look behind (+)
#`|` OR
#`^` start of string
#`.` matches any single character (except newline)
#`?=` look ahead (+)
#`\S` matches any non-whitespace character


def opening(delimiter):
    return rf'(?:(?<=\s)|(?<=^))({re.escape(delimiter)})(?=.)'

def closing(delimiter):
    return rf'(?<=.)({re.escape(delimiter)})(?:(?=\s)|(?=$))'

#---

'''def fork_asterisk(text, char): #bold, italic
    

def fork_underscore(line, i):
    pass

def fork_tilde(line, i): #strikethrough, subscript
    pass

def fork_backtick(line, i): #code, code block
    pass

def fork_hyphen(line, i): #unordered list, horizontal rulek
    pass'''

#---

def parse_hr(line):
    pattern =  r'(?:(?<=\s)|(?<=^))(-{3,})(?:(?<=\s)|(?<=$))'

    match = re.match(pattern, line)

#---

def parse_italic(line, i):
    

    #if found closing tag
    pass

def parse_header(line, i):
    pass

def parse_quote(line, i):
    pass

def parse_sup(line, i):
    pass

def parse_link(line, i):
    pass

def parse_ol(line, i):
    pass













#---



