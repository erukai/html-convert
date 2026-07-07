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
    #- del the state in delimiter_stack
    #- pop the state coord list
    def _remove(self, attr_name: str):

        #delimiter_stack does not count because the argument `state` is only for bool states
        not_is_states = ["text, parsing"]

        #custom Exception handler
        if (
            attr_name not in self.dir_getattr(self.state) 
            or (not attr_name.startswith("is_") and attr_name not in not_is_states)
        ):
            raise AttributeError("state ptovided is not a valid ParserState attribute")

        else:
            #return state to False
            if getattr(self.state, attr_name) != False: #in case the value is not only True but also None
                setattr(self.state, attr_name, False)

            #remove state in delimiter stack (hard coded but safe since there is only 1 delimiter_stack attr)
            state = attr_name[3:].upper()
            if state in self.state.delimiter_stack:
                self.state.delimiter_stack.reverse()
                self.state.delimiter_stack.remove(state)
                self.state.delimiter_stack.reverse()

            #pop state coord list (hard coded, kind of unsafe since attr is not known)
            coord_name = f"{attr_name[3:]}_coord"
            coord_attr = getattr(self.state, coord_name)
            coord_attr.pop()

    #---

    def _is_char(self, i: int) -> re.Match | None: #i = relative cursor index
        pos = self.text[self.cursor+i]

        #the position is a character and NOT a whitespace / end of line / start of line
        return re.fullmatch(r"\S", pos)
    
    def dir_getattr(self, obj) -> list: #`obj` also works with class, not necessarily an instance
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

        ...

    def _parse_check(self, char):
        #some formatting only works if the symbol is at the start of the line.
        #if current cursor is NOT at the start, ignore those formattings

        match self._current():
            case "*":
                self._fork_asterisk()                 

            case "_":
                self._fork_underscore()

            case "~":
                self._fork_tilde()

            case "`":
                self._fork_backtick()

            case "-":
                self._fork_hyphen()

            case "#" if self.cursor == 0:
                self._parse_heading()

            case ">" if self.cursor == 0:
                self._parse_quote()

            case "^":
                self._parse_sup()

            case "(": #special case
                self._parse_link()

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

    #---

    def _fork_underscore(self):
        pass

    def _fork_tilde(self):
        pass

    def _fork_backtick(self):
        pass

    def _fork_hyphen(self):
        pass

    def _parse_heading(self):
        pass

    def _parse_quote(self):
        pass

    def _parse_sup(self):
        pass


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
        self.is_heading = False
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

        self.heading_coord = [] #(list[tuple]) --> (line, heading_num)
        self.link_coord = [] #(list[tuple]) --> (line_start, column_start, line_end, column_end)

#----------