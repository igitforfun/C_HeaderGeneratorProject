"""
    This is the main script to generate C and C++ header code
"""

import json
import re
import argparse
import os
from FileCreator.CFileHandler import NewHeaderFileCreator

STRUCTNAME = 'name'
STRUCTDATA = 'data'
ARG = 'param'
DESC= 'description'

tab = "    "

script_dir_path = os.path.dirname(os.path.abspath(__file__))

def createStruct(struct, matrix, pk, al) -> str:

    noVar = len(matrix)
    noColumn = len(matrix[0])
    VarStr = ""

    for i in range(noVar):
        for j in range (noColumn):
            if j == 0:
                VarStr = VarStr + tab + matrix[i][j] + " "
            elif matrix[i][j] == matrix[i][-1]:
                #Add in comments for struct variables
                if DESC in struct[STRUCTDATA][i] and struct[STRUCTDATA][i][DESC] != "":
                    VarStr += matrix[i][j] + f";{tab}//!< {struct[STRUCTDATA][i][DESC]}\n"
                else:
                    VarStr = VarStr + matrix[i][j] + ";\n"
            else:
                VarStr = VarStr + " " + matrix[i][j] + " "

    #Add in comments for overall struct description
    code = f"/**\n * @brief"
    if DESC in struct and DESC != "":
        code += f" {struct[DESC]}\n */\n"
    else:
        code += "\n */\n"

    if pk != "" and al != "":
        code += f"typedef struct __attribute__(({pk}, {al})) _{struct[STRUCTNAME]}_ " + "{\n" + f"{VarStr}" + "} " + f"{struct[STRUCTNAME]};\n\n"
    elif pk != "" and al == "":
        code += f"typedef struct __attribute__(({pk})) _{struct[STRUCTNAME]}_ " + "{\n" + f"{VarStr}" + "} " + f"{struct[STRUCTNAME]};\n\n"
    elif pk == "" and al != "":
        code += f"typedef struct __attribute__(({al})) _{struct[STRUCTNAME]}_ " + "{\n" + f"{VarStr}" + "} " + f"{struct[STRUCTNAME]};\n\n"
    else:
        code += f"typedef struct _{struct[STRUCTNAME]}_ " + "{\n" + f"{VarStr}" + "} " + f"{struct[STRUCTNAME]};\n\n"
    return code

def createEnum(enum, matrix) -> str:
    noVar = len(matrix)
    noColumn = len(matrix[0])

    VarStr = ""
    for i in range(noVar):
        for j in range (noColumn):
            if matrix[i][j] == matrix[i][-1]:
                if matrix[i][j] == matrix[-1][j]:
                    VarStr = VarStr + matrix[i][j]
                else:
                    VarStr = VarStr + matrix[i][j] + ","

                # Add in comments in the enum elements
                if DESC in enum[STRUCTDATA][i] and enum[STRUCTDATA][i][DESC] != "":
                    VarStr += f"{tab}//!< {enum[STRUCTDATA][i][DESC]}\n"
                else:
                    VarStr+="\n"
            else:
                VarStr += tab + matrix[i][j] + " = "

    #Add in comments for overall enum description
    code = f"/**\n * @brief"
    if DESC in enum and DESC != "":
        code += f" {enum[DESC]}\n */\n"
    else:
        code += "\n */\n"

    code += f"typedef enum _{enum[STRUCTNAME]}_ " + "{\n" + f"{VarStr}" + "} " + f"{enum[STRUCTNAME]};\n\n"
    return code

def createMatrix(structtype, operand1, operand2) -> list:
        rows = len(structtype[STRUCTDATA]) # the number of rows of matrix
        matrix = [[None for c in range(2)]for r in range(rows)]

        # writing the data into a 2D matrix
        for row in range(rows):
                matrix[row][0] = structtype[STRUCTDATA][row][operand1]
                matrix[row][1] = structtype[STRUCTDATA][row][operand2]

        return matrix

def parser_init():
    parser = argparse.ArgumentParser(description = 'Generates C/C++ files based on input \
                                    configuration json files')
    parser.add_argument('-c', '--config', nargs = '*', default = ['Config/' + s for s in os.listdir(os.path.join(script_dir_path, 'Config\\'))], dest = 'config_input_file', help='List of input message struct config files to generate')
    parser.add_argument('-o', '--output-dir', default= 'Generated', dest = 'output_dir', help='Name of output directory to generate output source files')
    return parser

def main():
    parser = parser_init()
    args = parser.parse_args()
    print("Header Code generation started...\n")
    print(f"Detected {len(args.config_input_file)} config files:")

    #Remove output directory if it exists
    if os.path.isdir(args.output_dir):
        for f in os.listdir(args.output_dir):
            os.remove(args.output_dir + '\\'+ f)

    #Print out detected config json files
    for f in args.config_input_file:
        print(f.split('/')[-1])

    #Parsing each config json files
    for x in range(len(args.config_input_file)):
        allstructcode = [] #Has to be a list for writing lines to file
        header_file_name = args.config_input_file[x].split("/")[-1].split(".")[0]
        with open(args.config_input_file[x], 'r') as f:
            data = json.load(f)
            datatype = str(data.keys())
            # Check if Preprocessor macros exists and handle code creation
            if (re.search(".*[PREMACROSpremacros]{9}.*", datatype)):
                predefinecode = ""
                predefine = re.search(".*([PREMACROSpremacros]{9}).*", datatype).group(1)
                for item in data[predefine]:
                    if item ['param'] != "":
                        predefinecode += "#define " + item['param'] + " " + item['value']
                        # Add in comments for doxygen intepretation
                        if DESC in item and item[DESC] != "":
                            predefinecode += f" //!< {item[DESC]}\n"
                        else:
                            predefinecode += "\n"

                allstructcode.append(predefinecode + '\n')

            # Check if Structs exists and handle code creation
            if (re.search(".*[structsSTRUCTS]{7}.*", datatype)):
                struct = re.search(".*([structsSTRUCTS]{7}).*", datatype).group(1)

                for i in data[struct]:
                    packed = ""
                    aligned = ""
                    if i['aligned'] == "" or i['aligned'] == "0":
                        if i['packed'].upper() != "FALSE" and i['packed'].upper() != "":
                            packed = "__packed__"
                    else:
                        aligned = f"aligned({i['aligned']})"
                        if i['packed'].upper() != "FALSE" and i['packed'].upper() != "":
                            packed = "packed"

                    structmatrix = createMatrix(i, 'type', ARG)
                    structcode = createStruct(i, structmatrix, packed, aligned)
                    allstructcode.append(structcode)

            #Check if Enums exists and handle code creation
            if (re.search(".*[enumsENUMS]{5}.*", datatype)):
                enum = re.search(".*([enumsENUMS]{5}).*",datatype).group(1)

                for i in data[enum]:
                    enummatrix = createMatrix(i, ARG, 'value')

                    enumcode = createEnum(i, enummatrix)
                    allstructcode.append(enumcode)

            outdir = os.path.join(script_dir_path, args.output_dir)
            filecreator = NewHeaderFileCreator(header_file_name, outdir)


            filecreator.createHfile(allstructcode)
            filecreator.createHPPfile(allstructcode)

    print(f"\nHeader Code generation succeeded. Output files are created in {args.output_dir}/")

if __name__ == "__main__":
    main()
