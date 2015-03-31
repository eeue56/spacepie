from __future__ import print_function

from functools import partial

from util import *

text_mapping = {
    ' ' : '[Space]',
    '\n' : '[LF]',
    '\t' : '[Tab]'
}


class Stack(object):
    def __init__(self):
        self.stack = []
        self.heap = {}
        self.labels = {}

    def push(self, number):
        #print("Pushing", number)
        self.stack.append(number)

    def duplicate(self):
        #print("Duplicating")
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
        print(chr(self.stack[-1]), end="")

    def output_number(self):
        print(self.stack[-1], end="")

    def read_char(self):
        address = self.stack[-1]
        self.heap[address] = input("Enter: ").strip()[0]

    def read_number(self):
        address = self.stack[-1]
        self.heap[address] = ord(input("Enter: ").strip())


    def mark(self, label, index):
        #print("Marking", label, "at", index)
        self.labels[label] = index

    def call(self, label):
        return self.labels[label]

    def jump_to_unconditionally(self, label):
        return self.labels[label]

    def jump_if_zero(self, label):
        if self.stack[-1] == 0:
            return self.labels[label]
        return None

    def jump_if_negative(self, label):
        if self.stack[-1] < 0:
            return self.labels[label]
        return None


def stack_operations(stack, text, index):
    next_char = text[index + 1]

    # space for push
    if next_char == ' ':
        number, last_index = collect_number(text, index + 2)

        stack.push(number)

        index = last_index 

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
            number, last_index = collect_number(text, index + 2)

            stack.copy(number)

            index = last_index + 3
        elif next_char == '\n':
            #TODO: slide
            
            index += 2
    else:
        index += 1

    return index

def heap_and_arithmetic_operations(stack, text, index):

    next_char = text[index: index + 2]

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

    else:
        index += 1

    return index


# TODO: give a sensible name
def process(text):
    stack = Stack()

    index = 0
    before = -1

    i = 0

    _stack_operations = partial(stack_operations, stack, text)
    _heap_and_arithmetic_operations = partial(heap_and_arithmetic_operations, stack, text)

    while True:
        i+=1
        #print("index is ", index, repr(text[index:]))
        #print(stack.stack)
        #print(stack.labels)

        # catch infinite loops, for debugging
        if index == before or i > 100:
            break
        else: 
            before = index

        next_char = text[index]

        if next_char not in text_mapping:
            index += 1
            continue

        # space for stack
        if next_char == ' ':
            index = _stack_operations(index)

        elif next_char == '\t':
            index = _heap_and_arithmetic_operations(index)

        # lf flow control
        elif next_char == '\n':

            op_code = text[index + 1: index +3]

            if op_code == '  ':
                number, last_index = collect_number(text, index + 2)

                stack.mark(number, last_index)

                index = last_index 
            elif op_code == ' \t':
                call_index = index + 2

                number, last_index = collect_number(text, index + 2)

                index = stack.call(number)
            elif op_code == ' \n':
                number, last_index = collect_number(text, index + 2)

                index = stack.jump_to_unconditionally(number)

            elif op_code == '\t ':
                number, last_index = collect_number(text, index + 2)

                _index = stack.jump_if_zero(number)


                if _index is None:
                    index = last_index
                else:
                    index = _index

            elif op_code == '\t\t':
                number, last_index = collect_number(text, index + 2)

                _index = stack.jump_if_negative(number)

                if _index is None:
                    index = last_index
                else:
                    index = _index
            elif op_code == '\t\n':
                index = call_index
            elif op_code == '\n\n':
                return


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

    # push 4 to stack
    # 0
    text = '  \t  \n'

    assert collect_number(text, 2) == (4, 6)

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

    # push 2
    # 21
    text += '   \t \n'

    # mark with label 1
    # 27
    text += '\n  \t \n'

    # push 2
    # 33
    text += '   \t \n'

    # subtract
    # 39
    text += '\t  \t'

    # output number
    # 43
    text += '\t\n \t'

    # jump if zero
    # 47
    text += '\n\t \t \n'

    # end
    # 53
    text += '\n\n\n'

    # expected output:
    # 4820

    process(text)
