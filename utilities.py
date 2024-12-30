def read_file(path, mode='r'):
    with open(path, mode) as file:
        return file.read()

def write_file(path, contents, mode='w'):
    with open(path, mode) as file:
        return file.write(contents)


def safe_filename(name):
    underscore_replace = [
        " ",
    "&",
        "|",
        "/",
    "\\",        
]
    remove = [
    "<",
    ">",
    ":",
    '"',


    "?",
    "*",
    "^",

    "'",
    ";",
    "{",
    "}",
    "[",
    "]",
    "=",
    "+",
    "$",
    ",",
    "`",
    "~"
    ]
    new_filename = ""
    for character in name:
        if character in underscore_replace:
            character = '_'
        if character not in remove:
            new_filename += character
    new_filename = new_filename.replace('\n','').replace('\t', '_').lower().strip()
    return new_filename
    
