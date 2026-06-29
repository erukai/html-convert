import filtering
import parser

#filtering
convert_num, ignore_num = filtering.filter_md()
md_dict = filtering.store_md()

#parsing
html_dict = parser.parse_md(md_dict)


#injecting