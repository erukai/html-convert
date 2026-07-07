### Opening Delimiter ✅
- pattern: delimiter
- before pattern: any character OR whitespace(s) OR start of string
- after pattern: any character EXCEPT whitespace(s) or end of string

### Closing Delimiter ✅
- pattern: delimiter
- before pattern: any character EXCEPT whitespace(s) or start of string
- after pattern: any character OR whitespace(s) OR end of string

---

### Opening Delimiter (subscript & superscript)
- pattern: delimiter
- before pattern: any character OR whitespace(s) OR start of string
- after pattern: any character(s) EXCEPT whitespace(s) or end of string UNTIL closing delimiter

### Closing Delimiter (subscript & superscript)
- pattern: delimiter
- before pattern: any character(s) EXCEPT whitespace(s) or end of string FROM opening delimiter
- after pattern: any character OR whitespace(s) OR end of string

---

### horizontal rule
- pattern: `---`
- before pattern: whitespace(s) OR start of string
- after pattern: whitespace(s) OR end of string

### block quote
- pattern: `>` / `>>` / `>>>` ...
- before pattern: whitespace(s) OR start of string
- after pattern: any character OR whitespace(s) OR end of string

### heading
- pattern: `#`, `##`, `###`, `####`, `#####`, `######`
- before pattern: whitespace(s) OR start of string
- after pattern: whitespace(s), any character

### paragraph
- pattern: any character(s)
- before pattern: whitespace(s) OR start of string
- after pattern: whitespace(s) OR end of string

### link
- pattern 1: `[...]`
- pattern 2: `(...)`

- before pattern 1 op: whitespace(s) OR start of string
- after pattern 1 op / before pattern 1 cl: any character(s) OR whitespace(s) 
- after pattern 1 cl: `(`

- before pattern 2 op: `]` 
- after pattern 2 op / before pattern 2 cl: any character(s) OR whitespace(s) _<- (whitespace(s) will be stripped)_
- after pattern 2 cl: whitespace(s) OR end of string

### code block
- pattern: ` ``` `
- before pattern op: start of string
- after pattern op: whitespace(s) AND/OR code language AND/OR end of string, newline, any character(s) OR whitespace(s)
- before pattern cl: any character(s) OR whitespace(s), newline
_(all markdown formatting in a code block is ignored)_

---

### empty line
- pattern: `\n`
- before pattern: start of string
- after pattern: end of string

---

### unordered list
- pattern: `-`
- before pattern: start of string OR whitespace(s)
- after pattern: whitespace(s), any character
_(indentation determines level. 1 level = 2 whitespaces. but parent and siblings also affect the indentation)_

### ordered list
- pattern: `n.` _(`n` is any positive integer)_
- before pattern: start of string OR whitespace(s)
- after pattern: whitespace(s), any character
_(indentation determines level. 1 level = 2 whitespaces. but parent and siblings also affect the indentation)_


---

NOTE: a formatting is invalid _(ignored)_ if not all rules are fulfilled, or if either the opening / closing delimiter is not found.