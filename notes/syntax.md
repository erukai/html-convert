### Escape Character (`\`)
- if `\` appears before a markdown symbol, do not parse the symbol


### Number sign (`#`)
- marks the **entire line** as a header
- must appear at the beginning of a line _(left trailing spaces are exempted)_
- must has space(s) between the symbol and the following character
- formatting is not multi-line
- have 6 varieties:
    - header 1 (`#`) -> `<h1></h1>`
    - header 2 (`##`) -> `<h2></h2>`
    - header 3 (`###`) -> `<h3></h3>`
    - header 4 (`####`) -> `<h4></h4>`
    - header 5 (`#####`) -> `<h5></h5>`
    - header 6 (`######`) -> `<h6></h6>`