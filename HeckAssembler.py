## written by Guy Soudri and Hezki Raff.
import sys
import os
from os.path import isfile, join

ASMSUFIX = ".asm"
NUM_OF_BINARY_LINE = 16
HACKSUFIX = ".hack"

ZERO = "0" * 16
EQUAL = "="
COLON = ";"
DEST_START = 9
DEST_END = 11
JUMP_START = 12
## dest forms dictionary
destTable = {"0": "000", "M": "001", "D": "010", "MD": "011", "A": "100", "AM": "101", "AD": "110", "AMD": "111"}
## jump forms dictionary
jumpTable = {"JLE": "110", "JGT": "001", "JEQ": "010", "GLT": "100", "JNE": "101", "JMP": "111", "JGE": "011"}
## comp forms dictoinary
compTable = {"0": "1110101010", "1": "1110111111", "-1": "1110111010", "D": "1110001100", "A": "1110110000",
             "!D": "1110001101",
             "!A": "1110110001", "-D": "1110001111", "-A": "1110110011", "D+1": "1110011111", "A+1": "1110110111",
             "D-1": "1110001110",
             "A-1": "1110110010", "D+A": "1110000010", "D-A": "1110010011", "A-D": "1110000111", "D&A": "1110000000",
             "D|A": "1110010101",
             "M": "1111110000", "!M": "111110001", "-M": "1111110011", "M+1": "1111110111", "M-1": "1111110010",
             "D+M": "1111000010",
             "D-M": "1111010011", "M-D": "1111000111", "D&M": "1111000000", "D|M": "1111010101", "A>>": "1010000000",
             "M>>": "1011000000",
             "D<<": "1010110000", "D>>": "1010010000", "M<<": "1011100000", "A<<": "1010100000"}
## symbols dictionary
symbolTable = {"R0": "0000000000000000", "R1": "0000000000000001", "R2": "0000000000000010", "R3": "0000000000000011",
               "R4": "0000000000000100", "R5": "0000000000000101", "R6": "0000000000000110", "R7": "0000000000000111",
               "R8": "0000000000001000", "R9": "0000000000001001", "R10": "0000000000001010", "R11": "0000000000001011",
               "R12": "0000000000001100", "R13": "0000000000001101", "R14": "0000000000001110",
               "R15": "0000000000001111"
    , "SCREEN": "0100000000000000", "KBD": "110000000000000", "SP": "0000000000000000", "LCL": "0000000000000001",
               "ARG": "0000000000000010", "THIS": "0000000000000011", "THAT": "0000000000000100"
               }

LEFT_BARACADE = '('
RIGHT_BARACADE = ')'
SHTROODEL = '@'
SPACE = ' '
SLASH = '/'



## goes through the file, removes un-necessery lines and white spaces.
def parser(fileName):
    k = open(fileName, "r")
    lines = []
    for line in k:
        theline = "".join(line.split())
        if line != "\n" and line[0] != '/':
            if SLASH + SLASH in theline:
                for i in range(0, len(theline)):
                    if theline[i] == SLASH and i < len(theline) - 1 and theline[i + 1] == SLASH:
                        theline = theline[:i]
                        break

            lines.append(theline.replace("\n", ''))

    return lines


## find labels and adds them to the labels dictionary
def findLabels(array):
    counter = 0
    for line in array:

        if (len(line) > 0 and line[0] == LEFT_BARACADE):
            end = line.index(RIGHT_BARACADE)
            lable = line[1:end]
            if lable not in symbolTable:
                symbolTable[lable] = decToBin(counter)
                counter += 1
        else:
            counter += 1


## finds symbols and adds them to the symbols dictionary
def findSymbol(array):
    counter = 16
    for line in array:
        if (len(line) > 0 and line[0] == SHTROODEL and not line[1].isdigit()):
            lable = line[1:len(line)]
            if lable not in symbolTable:
                symbolTable[lable] = decToBin(counter)
                counter += 1


##translates decimal number to it's binary form
def decToBin(num):
    binary = bin(int(num))
    return ZERO[:16 - len(binary) + 2] + binary[2:]


## the last loop in the program. goes through the parsed file and translates it to binary code.
def finalLoop(lines, fileName):
    with open(fileName, "w") as text_file:
        for line in lines:
            if len(line) > 0 and line[0] == LEFT_BARACADE:
                continue
            if len(line) > 0 and line[0] == SHTROODEL:
                if line[1].isdigit():
                    num = line[1:]
                    num = decToBin(num)
                    text_file.write(num + "\n")
                else:
                    text_file.write(symbolTable[line[1:]] + "\n")
            elif EQUAL in line or COLON in line:
                finalLine = ["0"] * NUM_OF_BINARY_LINE
                finalLine[:2] = [1, 1, 1]
                if EQUAL in line and COLON not in line:

                    finalLine[DEST_START:DEST_END] = destTable[line[:line.index(EQUAL)]]
                    if line[line.index(EQUAL) + 1:] in compTable.keys():
                        finalLine[:DEST_START] = compTable.get(line[line.index(EQUAL) + 1:])

                elif COLON in line and EQUAL not in line:
                    finalLine[:JUMP_START] = compTable[line[:line.index(COLON)]]

                    finalLine[JUMP_START + 1:] = jumpTable[line[line.index(COLON) + 1:]]
                elif COLON in line and EQUAL in line:
                    finalLine[:DEST_START] = compTable[line[line.index(EQUAL) + 1:line.index(COLON)]]

                    finalLine[DEST_START:DEST_END] = destTable[line[:line.index(EQUAL)]]

                    finalLine[JUMP_START + 1:] = jumpTable[line[1 + line.index(COLON):]]

                finalLine = list(map(str, finalLine))
                guy = ''.join(finalLine[:NUM_OF_BINARY_LINE])
                text_file.write(guy + "\n")


## checks if the input is a file or a directory and makes the rest of the program run by it.
def firstRun(input):
    if os.path.isfile(input):
        lines = parser(input)
        findLabels(lines)
        findSymbol(lines)
        finalLoop(lines, os.path.splitext(input)[0] + HACKSUFIX)
    else:
        files = [f for f in os.listdir(input) if isfile(join(input, f))]
        for file in files:
            if os.path.splitext(file)[1] == ASMSUFIX:
                lines = parser(join(input, file))
                findLabels(lines)
                findSymbol(lines)
                finalLoop(lines, os.path.splitext(join(input, file))[0] + HACKSUFIX)


## the min function
def __main__():
    firstRun(sys.argv[1])


if __name__ == "__main__":
    __main__()
