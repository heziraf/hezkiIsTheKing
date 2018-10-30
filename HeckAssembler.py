## written by elitali94 and yechezker

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
lableTable={}



# get name of file, open him and return list with his lines - except empty lines and lines that start whit /
def parser(fileName):pass#TODO ELITAL
    assemblerFile = open(fileName, "r")
    lines = []
    #
    #
    #
    return lines


#gets list of line without empty line and lines that start whit /, and return list of line
#without labels (without @i, @loop, (LOOP). but with @R5, @KBD...instead of @i, put @16,@17,...and delete "(LABLE)".
#instructions for elital:
# put all "(LABLE)" in lableTable (dictionary) as key and the value is the num of line. also put in this dictionary
# @i as a key and value is 16...
def deleteLabels(lines):pass #TODO ELITAL
    linesWhithOutLabels=[0]
    #
    #
    #
    return linesWhithOutLabels

#gets lins with assembly code - without empty lines, / lines, labels, and make replacing simbols as @R5 by @5
def deleteSimbols(lines)pass:#TODO ELITAL
    finish = []
    #
    #
    #
    return finish

def finishTranslate(lines)pass:#TODO hezki


def __main__():
    input = sys.argv[1]
    if os.path.isfile(input):
        lines = parser(input)
        lines = deleteLabels(lines)
        lines = deleteSimbols(lines)
        finishTranslate(lines, os.path.splitext(input)[0] + ".hack")
    else:
        for file in [f for f in os.listdir(input) if isfile(join(input, f))]:
            if os.path.splitext(file)[1] == ".asm":
                lines = parser(join(input, file))
                lines = deleteLabels(lines)
                lines = deleteSimbols(lines)
                finishTranslate(lines, os.path.splitext(join(input, file))[0] + ".hack")



if __name__ == "__main__":
    __main__()
