# written by elitali94 and yechezker
# this program gets asm files (files that written in assembly language),
# and translate them to binary code (hack language).
#  for every input file_name.asm, the program output file_name.hack .
############################################################
# Imports
############################################################
import sys
import os
############################################################
# Constants
############################################################
START_BRACKET = '('
END_BRACKET = ')'
A_INSTRUCTION = "@"
COMMENT = "//"
ENTER = "\n"
SPACE= " "
FIRST_PLACE = 0
SEC_PLACE = 1
HACK_SUFFIX = ".hack"
ASM_SUFFIX= ".asm"

############################################################
# Global variables
############################################################
ok = "ok"
list_of_asm_lines = []
dictionary_new_symbol_label = {}
dictionary_known_symbol = {"R0": "0000000000000000",     "R1": "0000000000000001",  "R2": "0000000000000010",
                           "R3": "0000000000000011",     "R4": "0000000000000100",  "R5": "0000000000000101",
                           "R6": "0000000000000110",     "R7": "0000000000000111",  "R8": "0000000000001000",
                           "R9": "0000000000001001",    "R10": "0000000000001010", "R11": "0000000000001011",
                          "R12": "0000000000001100",    "R13": "0000000000001101", "R14": "0000000000001110",
                          "R15": "0000000000001111", "SCREEN": "0100000000000000", "KBD": "0110000000000000",
                           "SP": "0000000000000000",    "LCL": "0000000000000001", "ARG": "0000000000000010",
                         "THIS": "0000000000000011",   "THAT": "0000000000000100"}

dictionary_compare = {"0": "1110101010",   "1": "1110111111", "-1":  "1110111010",   "D": "1110001100",
                      "A": "1110110000",  "!D": "1110001101", "!A":  "1110110001",  "-D": "1110001111",
                     "-A": "1110110011", "D+1": "1110011111", "A+1": "1110110111", "D-1": "1110001110",
                    "A-1": "1110110010", "D+A": "1110000010", "D-A": "1110010011", "A-D": "1110000111",
                    "D&A": "1110000000", "D|A": "1110010101",   "M": "1111110000",  "!M": "1111110001",
                     "-M": "1111110011", "M+1": "1111110111", "M-1": "1111110010", "D+M": "1111000010",
                    "M+D": "1111000010", "D-M": "1111010011", "M-D": "1111000111", "D&M": "1111000000",
                    "D|M": "1111010101", "A>>": "1010000000", "M>>": "1011000000", "D<<": "1010110000",
                    "D>>": "1010010000", "M<<": "1011100000", "A<<": "1010100000"}

dictionary_destination = {"0": "000", "M": "001", "D": "010", "MD": "011", "A": "100", "AM": "101", "AD": "110",
                          "AMD": "111"}

dictionary_jump = {"JGT":"001","JEQ":"010","JGE":"011","JLT":"100","JNE":"101","JLE":"110","JMP":"111"}


############################################################
# Functions
############################################################

def list_without_symbol():
    '''
    The function runs on the array list_of_asm_lines and for A INSTRUCTION
    if @symbol then replaces values stored in dictionaries -
    dictionary_known_symbol, dictionary_new_symbol_label.
    else adds the new symbol to the dictionary
    '''
    current_address = 16
    for line in list_of_asm_lines:
        if line.startswith(A_INSTRUCTION):
            split_line = line.split(A_INSTRUCTION)[SEC_PLACE]
            if split_line in dictionary_new_symbol_label:
                index = list_of_asm_lines.index(line)
                list_of_asm_lines[index] = A_INSTRUCTION + str(dictionary_new_symbol_label.get(split_line))
            elif split_line in dictionary_known_symbol:
                index = list_of_asm_lines.index(line)
                list_of_asm_lines[index] = dictionary_known_symbol.get(split_line)
            else:
                if split_line.isdigit():
                    continue
                else:
                    dictionary_new_symbol_label[split_line] = str(current_address)
                    current_address += 1
                    index = list_of_asm_lines.index(line)
                    list_of_asm_lines[index] = A_INSTRUCTION + str(dictionary_new_symbol_label.get(split_line))


def list_without_labels():
    '''
    The function runs on the array list_of_asm_lines and for A INSTRUCTION
    if @label then replaces values stored in dictionary_new_symbol_label.
    '''
    for line in list_of_asm_lines:
        if line.startswith(A_INSTRUCTION):
            split_line = line.split(A_INSTRUCTION)[SEC_PLACE]
            if split_line in dictionary_new_symbol_label:
                index = list_of_asm_lines.index(line)
                list_of_asm_lines[index] = A_INSTRUCTION + str(dictionary_new_symbol_label.get(split_line))


def list_without_comments():
    '''
    The function runs on the array list_of_asm_lines and deletes all comments
    That appear after a standard A INSTRUCTION/ C INSTRUCTION
    '''
    for line in list_of_asm_lines:
        if COMMENT in line:
            comment_index = line.index(COMMENT)
            fix_line = line[:comment_index]
            index = list_of_asm_lines.index(line)
            list_of_asm_lines[index] = str(fix_line)


def decimal_to_binary():
    '''
    The function runs on the array list_of_asm_lines and for A INSTRUCTION
    if @number then replaces with binary number
    '''
    for line in list_of_asm_lines:
        if line.startswith(A_INSTRUCTION):
            binary = bin(int(line[1:]))[2:]
            fix_line = dictionary_known_symbol["R0"][:16 - len(binary)] + binary
            index = list_of_asm_lines.index(line)
            list_of_asm_lines[index] = str(fix_line)


def c_instruction_to_binary():
    '''
    The function runs on the array list_of_asm_lines and for C INSTRUCTION
    replaces values stored in dictionary_compare, dictionary_destination and
     dictionary_jump
    '''
    for line in list_of_asm_lines:
        if not line.isdigit():
            if "=" in line:
                equal_index = line.index("=")
                if ";" in line:
                    index = line.index(";")
                    fix_line = dictionary_compare[line[equal_index + 1:index]] + dictionary_destination[
                        line[:equal_index]] + dictionary_jump[line[index + 1:]]
                else:
                    fix_line = dictionary_compare[line[equal_index + 1:]] + dictionary_destination[line[:equal_index]] + "000"
            else:
                if ";" in line:
                    index = line.index(";")
                    fix_line = dictionary_compare[line[:index]] + "000" +dictionary_jump[line[index + 1:]]
                else:
                    fix_line = dictionary_compare[line] + "000000"
            index = list_of_asm_lines.index(line)
            list_of_asm_lines[index] = str(fix_line)


def writing_to_a_file(input_file):
    '''
    The function runs on the array list_of_asm_lines and write to file all
    the values in array
    :param input_file: the given path with the ending .hack
    '''
    with open(input_file, "w") as file_lines:
        for i in range(0, len(list_of_asm_lines)):
            end = ENTER
            if i == len(list_of_asm_lines) - 1:
                end = ""
            file_lines.write(list_of_asm_lines[i] + end)
    if len(list_of_asm_lines) != 0:
        del list_of_asm_lines[:]


def from_asm_to_list(input_file):
    '''
    The function runs on the lines of the input file, and add to
    dictionary_new_symbol_label ant @(label). also save all valuable lines to
     list_of_asm_lines
    :param input_file: the given path
    '''
    with open(input_file, "r") as file_lines:
        for line in file_lines:
            line = line.replace(SPACE, "")
            if line.startswith(COMMENT):
                continue
            elif not line or line == ENTER or line == SPACE or line=="\r":
                continue
            elif line.startswith(START_BRACKET):
                label = line[line.find(START_BRACKET) + 1:line.find(END_BRACKET)]
                label_value = len(list_of_asm_lines)
                dictionary_new_symbol_label[label] = str(label_value)
                continue
            else:
                line_with_no_enter = line.split(ENTER)[FIRST_PLACE]
                split_line = line_with_no_enter.replace("\r","")
                if not (split_line == ""):
                    list_of_asm_lines.append(split_line)


def from_asm_to_hack(input_file):
    '''
    The function runs on the functions that transfer the file from asm to hack
    if file end with .asm
    :param input_file: the given path
    '''
    if input_file.endswith(ASM_SUFFIX):
        from_asm_to_list(input_file)
        list_without_labels()
        list_without_symbol()
        list_without_comments()
        decimal_to_binary()
        #print(list_of_asm_lines)
        c_instruction_to_binary()
        writing_to_a_file(os.path.splitext(input_file)[FIRST_PLACE] + HACK_SUFFIX)


def __main__():
    input_file = sys.argv[SEC_PLACE]
    if os.path.isfile(input_file):
        from_asm_to_hack(input_file)
    elif os.path.isdir(input_file):
        list_of_files = os.listdir(input_file)
        for file in list_of_files:
            from_asm_to_hack(input_file+file)
    else:
        return


if __name__ == "__main__":
    __main__()