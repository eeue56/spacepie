text_mapping = {
    ' ' : '[Space]',
    '\n' : '[LF]',
    '\t' : '[Tab]'
}


class Stack(object):
    def __init__(self):
        self.stack = []
        self.heap = {}

    def push(self, number):
        self.stack.append(number)

    def duplicate(self):
        self.stack.append(self.stack[-1])

    def copy(self, n):
        self.stack.append(self.stack[n])

    def swap(self):
        self.stack[-1], self.stack[-2] = self.stack[-2], self.stack[-1]

    def discard(self):
        self.stack.pop()

    def slide(self, n):
        return


    def add(self):
        a = self.stack.pop()
        b = self.stack.pop()

        self.stack.append(a + b)

    def subtract(self):
        a = self.stack.pop()
        b = self.stack.pop()

        self.stack.append(a - b)

    def multiply(self):
        a = self.stack.pop()
        b = self.stack.pop()

        self.stack.append(a * b)

    def divide(self):
        a = self.stack.pop()
        b = self.stack.pop()

        self.stack.append(a // b)

    def modulo(self):
        a = self.stack.pop()
        b = self.stack.pop()

        self.stack.append(a % b)


    def store(self):
        address = self.stack[-2]
        value = self.stack[-1]

        self.heap[address] = value

    def retrieve(self):
        address = self.stack[-1]

        self.stack.append(self.heap[address])


    def output_char(self):
        print(chr(self.stack[-1]))

    def output_number(self):
        print(self.stack[-1])

    def read_char(self):
        address = self.stack[-1]
        self.heap[address] = input("Enter: ").strip()[0]

    def read_number(self):
        address = self.stack[-1]
        self.heap[address] = ord(input("Enter: ").strip())


# TODO: give a sensible name
def process(text):
    stack = Stack()
    index = 0
    before = -1

    while True:

        # catch infinite loops, for debugging
        if index == before:
            break
        else: 
            before = index

        next_char = text[index]

        # space for stack
        if next_char == ' ':
            next_char = text[index + 1]

            # space for push
            if next_char == ' ':
                last_index = text[index + 2:].index('\n') 
                bits = text[index + 2:last_index + 2]
                number = whitespace_to_number(bits)

                stack.push(number)

                index = last_index + 3

            elif next_char == '\n':
                next_char = text[index + 2]

                if next_char == ' ':
                    stack.duplicate()
                elif next_char == '\t':
                    stack.swap()
                elif next_char == '\n':
                    stack.discard()

                index += 3

            elif next_char == '\t':
                next_char = text[index + 2]

                if next_char == ' ':
                    last_index = text[index + 2:].index('\n')
                    bits = text[index + 2:last_index + 2]
                    number = whitespace_to_number(bits)

                    stack.copy(number)

                    index = last_index + 3
                elif next_char == '\n':
                    #TODO: slide
                    
                    index += 2



        elif next_char == '\t':
            next_char += text[index + 1]

            # tab space for arithmetic
            if next_char == '\t ':
                op_code = text[index + 2:index + 4]

                if op_code == '  ':
                    stack.add()
                elif op_code == ' \t':
                    stack.subtract()
                elif op_code == ' \n':
                    stack.multiply()
                elif op_code == '\t ':
                    stack.divide()
                elif op_code == '\t\t':
                    stack.modulo()

                index += 4


            # tab tab heap access
            elif next_char == '\t\t':
                next_char = text[index + 2]

                if next_char == ' ':
                    stack.store()
                elif next_char == '\t':
                    stack.retrieve()

                index += 2

            # tab lf IO
            elif next_char == '\t\n':
                op_code = text[index + 2:index+ 4]

                if op_code == '  ':
                    stack.output_char()
                elif op_code == ' \t':
                    stack.output_number()
                elif op_code == '\t ':
                    stack.read_char()
                elif op_code == '\t\t':
                    stack.read_number()

                index += 4

        # lf flow control
        elif next_char == '\n':

            op_code = text[index + 1: index +3]

            if op_code == '  ':
                #stack.mark()
                pass
            elif op_code == ' \t':
                #stack.call
                pass
            elif op_code == ' \n':
                #stack.jump_unconditionally
                pass
            elif op_code == '\t ':
                #stack_jump_if_zero
                pass
            elif op_code == '\t\t':
                #stack_jump_if_negative
                pass
            elif op_code == '\t\n':
                #stack_end_mark
                pass
            elif op_code == '\n\n':
                return




def whitespace_to_number(whitespace):
    return int(whitespace.replace(" ", "0").replace("\t", "1"), 2)

def number_to_whitespace(number):
    as_string = "{0:b}".format(number)
    return as_string.replace("0", " ").replace("1", "\t")


def convert_to_readable(text):
    for v, k in text_mapping.items():
        text = text.replace(v, k)
    return text



def test():
    def test_conversion():
        program = "  \t\t\n\n"
        compiled = '[Space][Space][Tab][Tab][LF][LF]'
        nonsense = 'asdfghjkl;qwertyuiopzxcvbnm,..,mnbvcx'

        assert convert_to_readable(program) == compiled

        program += nonsense

        assert convert_to_readable(program) == compiled + nonsense

        six = "\t\t "

        assert whitespace_to_number(six) == 6

        assert number_to_whitespace(6) == six
    

    def test_validity():

        with open('count.ws', 'rb') as f:
            data = f.read()

        converted = convert_to_readable(data)
            
        for char, code in zip(data, converted.split('[')):
            print('"{}" : "{}"'.format(ord(char), code)) 

        #assert is_valid_program(convert_to_readable(data))


    test_conversion()
    #test_validity()


if __name__ == '__main__':
    test()

    # push 6 to stack
    # 0
    text = '  \t\t \n'

    # duplicate
    # 6
    text += ' \n '

    # output number
    # 9
    text += '\t\n \t'

    # add them
    # 13
    text += '\t   '

    # output number
    # 17
    text += '\t\n \t'

    # end
    text += '\n\n\n'

    process(text)
