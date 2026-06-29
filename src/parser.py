def parse_md(md_dict:dict):
    html_dict = {}

    #iterate through the dictionary file by file
    for file_name, file_content in md_dict.items():

        #execute line parser
        html_dict[file_name] = parse_line(file_content)
        
    return html_dict
        
#---
        
def parse_line(lines):
    pass