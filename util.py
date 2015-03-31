
def collect_number(text, start_index):
    last_index = text[start_index:].index('\n')
    bits = text[start_index:start_index + last_index + 1]
    number = whitespace_to_number(bits)
    return (number, start_index + last_index + 1)


def whitespace_to_number(whitespace):
    return int(whitespace.replace(" ", "0").replace("\t", "1"), 2)

def number_to_whitespace(number):
    as_string = "{0:b}".format(number)
    return as_string.replace("0", " ").replace("1", "\t")


