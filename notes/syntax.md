### Escape Character (`\`)
- if `\` appears before a markdown symbol, do not parse the symbol


### Number sign (`#`)
- marks the **entire line** as a heading
- must appear at the beginning of a line _(left trailing spaces are exempted)_
- must has space(s) between the symbol and the following character
- formatting is not multi-line
- have 6 varieties:
    - heading 1 (`#`) -> `<h1></h1>`
    - heading 2 (`##`) -> `<h2></h2>`
    - heading 3 (`###`) -> `<h3></h3>`
    - heading 4 (`####`) -> `<h4></h4>`
    - heading 5 (`#####`) -> `<h5></h5>`
    - heading 6 (`######`) -> `<h6></h6>`