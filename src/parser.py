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

    def _ignore_open(self): #ignore parse if already open
        pass

    #---

    def _op_match(self, delimiter): #works for: * (1–3) _ (1–3) ~ (2) ` (1)
        window = self.text[self.cursor: self.cursor+4]  #the char, 3 after
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

    def _turn(self, n=1) -> str | None: #check char behind cursor
        if self.cursor-n < 0: #"hello", cursor=1 ("e"), n=2
            return

        char = ""

        for i in range(n, 0, -1):
            char += self.text[self.cursor-i]

        return char
    
    #---

    def _advance(self, n=1): #move the cursor to the next column
        self.cursor += n


    #when used on a ParserState variable (is_...):
    #- return the state to False
    #- del the state in delimiter_stack (must use roundabout method to get the name of the variable)
    #- pop the state coord list (must use roundabout method)
    def _remove(self, **state: dict[str, bool]): #roundabout method 1: pack in a dictionary to get key-value pair
        '''example:\n
        state = `{"is_bold": self.state.is_bold}`\n
        state_key = `is_bold` (type: str)\n
        state_value = `self.state.is_bold` (type: MarkdownParser -> ParserState -> bool)'''

        if len(state) != 1:
            raise ValueError("state provided must be 1")

        #convert the single-item dictionary into a list, then unpack the single-item list into a string (key only)
        state_key = list(state.keys())[0] #using list() turns it into a string
        state_value = next(iter(state.values())) #this one doesn't use list(), so it still references the original value of `state`
        
        #---

        not_is_states = ["text, parsing"] #delimiter_stack does not count because the argument `state` is only expected to be a bool
        if state_key not in self.dir_data_attr(ParserState) or (not state_key.startswith("is_") and state_key not in not_is_states):
            raise NameError("state ptovided is not a valid ParserState data attribute")
        
        else:
            value_name = f'self.state.{state_key}' #inject
            state_value = False
            self.state.delimiter_stack.remove()

    #---

    def _is_char(self, i: int) -> re.Match | None: #i = relative cursor index
        pos = self.text[self.cursor+i]

        #the position is a character and NOT a whitespace / end of line / start of line
        return re.fullmatch(r"\S", pos)
    
    def dir_data_attr(self, obj) -> list: #`obj` also works with class, not necessarily an instance
        return [name for name in dir(obj) if not callable(getattr(obj, name)) and not name.startswith("__")]

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
            if self.state.is_bold is False and self.state.is_italic is False:
                self.state.delimiter_stack.append("BOLD_ITALIC")
                self.state.is_bold = True
                self.state.is_italic = True

            '''else:
                self._remove(is_bold=self.state.is_bold)'''

        elif self._peek(1) == "*" and self._is_char(2): #**\S
            if self.state.is_bold is False:
                self.state.delimiter_stack.append("BOLD")
                self.state.is_bold = True

        elif self._is_char(1): #*\S
            if self.state.is_italic is False:
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