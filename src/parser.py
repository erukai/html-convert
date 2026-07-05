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

        self.ln = 1
        self.cursor = 0 #position of cursor in a line, starts at 0

        self.state = ParserState()
        self.text = None

    #---
    
    def _ignore_parse(self):
        if self.state.is_code or self.state.is_code_fence or self.state.is_link_url:
            self.state.parsing = False

    #---

    def _op_match(self, delimiter): #works for: * (1–3) _ (1–3) ~ (2) ` (1)
        window = self.text[max(0, self.cursor-1): self.cursor+4]  # 1 char before, the char, 3 after
        match = re.search(rf'({re.escape(delimiter)})(?=\S)', window)

        return match

    def _cl_match(self, delimiter):
        window = self.text[max(0, self.cursor-1): self.cursor+4]  # 1 char before, the char, 3 after
        match = re.search(rf'(?<=\S)({re.escape(delimiter)})', window)
    
        return match

    def _spaceless_op(self, delimiter): #works for: subscript (~) and superscript (^)
        pass

    def _spaceless_cl(self, delimiter): #works for: subscript (~) and superscript (^)
        pass

    def _link_match(self): #special regex matching for link formatting
       ''' window = self.text[max(0, self.cursor-1):]  # 1 char before, the char, end of line
        match = re.search(rf'\[(.*?)\]\((.*?)\)', window)

        #ONLY MATCH ON FIRST OCCURENCE. After finish, advance the cursor to the next unparsed char
        return match'''



    #---
    
    #helper methods, not to be accessed outside, but to be used by other methods in this class
    def _current(self): #check char on cursor
        return self.text[self.cursor]
    
    def _peek(self, n=1): #check char ahead cursor

        #make sure there's enough remaining characters in the line to peek through
        #else, cancel peek and cancel parsing
        if not self.text[self.cursor+n] < len(self.text): #"hello"
            return

        char = ""

        for i in range(1, n+1): #range is exclusive
            char += self.text[self.cursor+i]

        return char

    def _turn(self, n=1): #check char behind cursor
        if self.cursor-n < 0: #"hello", cursor=1 ("e"), n=2
            return

        char = ""

        for i in range(n, 0, -1):
            char += self.text[self.cursor-i]

        return char
    




    def _advance(self, n=1): #move the cursor to the next column
        self.cursor += n

    def _is_char(self, i: int): #i = relative cursor index
        pos = self.text[self.cursor+i]

        #the position is a character and NOT a whitespace / end of line / start of line
        return re.fullmatch(r"\S", pos)

    #---

    #the only method that should be used outside of the class
    def parse(self) -> list:
        for line in self.lines: #move line by line
            self.text = line

            while self.cursor < len(self.text):
                char = self.text[self.cursor]

                self._parse_check(char)
                self._advance()

            #end of line:
            self.cursor = 0
            self.ln += 1
            




    def _parse_check(self, char):
        #some formatting only works if the symbol is at the start of the line.
        #if current cursor is NOT at the start, ignore those formattings

        match self._current():
            case "*":
                self._fork_asterisk()                 

            case "_":
                _fork_underscore(self)

            case "~":
                _fork_tilde(self)

            case "`":
                _fork_backtick(self)

            case "-":
                _fork_hyphen(self)

            case "#" if self.cursor == 0:
                _parse_header(self)

            case ">" if self.cursor == 0:
                _parse_quote(self)

            case "^":
                _parse_sup(self)

            case "()": #special case, change later
                _parse_link(self)

            case _: #not a formatting character
                return

    #---

    def _fork_asterisk(self):
        if self._peek(2) == "**" and self._is_char(3): #***\S
            self.state.delimiter_stack.append("BOLD_ITALIC")
            self.state.is_bold = True
            self.state.is_italic = True

        elif self._peek(1) == "*" and self._is_char(2): #**\S
            self.state.delimiter_stack.append("BOLD")
            self.state.is_bold = True

        elif self._is_char(1): #*\S
            self.state.delimiter_stack.append("ITALIC")
            self.state.is_italic = True









    #unlike other parsers, link parser checks the entire line in advance (using regex) for link formatting,
    #because link formatting only works when written in a single line
    def _parse_link(self):
        match = self._link_match(self.text) #if match

        #len() counts the first item as "1", whereas cursor counts the first column as "0".
        #So to take the value of len() into cursor, cursor must subtract by 1
        cursor += len(match.group(0)) - 1 #advances until the final matching character

        #update the link coordinate (line range, column range)
        self.state.link_coord.append((self.ln, match.span()[0], self.ln, match.span()[1]))



class ParserState():
    def __init__(self):
        self.delimiter_stack = []

        #entire line
        self.is_header = False
        self.is_quote = False
        self.is_hr = False

        #single line
        self.is_code = False
        self.is_link_text = False
        self.is_link_url = False

        #multi-line
        self.is_bold = False
        self.is_italic = False
        self.is_strikethrough = False
        self.is_code_fence= False

        self.text = False
        self.parsing = True

        #---

        self.link_coord = [] #(list[tuple]) --> (line_start, column_start, line_end, column_end)

#----------

def fork_underscore(line, i):
    pass

def fork_tilde(line, i): #strikethrough, subscript
    pass

def fork_backtick(line, i): #code, code block
    pass

def fork_hyphen(line, i): #unordered list, horizontal rulek
    pass

'''

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
'''