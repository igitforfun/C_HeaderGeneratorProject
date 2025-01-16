"""
    This is the file handler class to create a .h file following a template
"""
import os

COPYRIGHT = "/******************************************************************************\n\
* Copyright (C) [Message to be written in this segment]\n\
 ******************************************************************************/\n"

FILE_START_HEADER = "/**\n\
 * @file filename.h\n\
 * @brief [Insert your brief description about this file].\n\
*/\n\n\
#ifndef FILE_NAME_H\n\
#define FILE_NAME_H\n\n\
/******************************************************************************/\n\
/* Constants and types */\n\
/*============================================================================*/\n\n"

FILE_END_HEADER= "#endif /* FILE_NAME_H */\n"

class NewHeaderFileCreator():

    def __init__(self, filename, output_dir):
        self.filename = filename + ".h"
        self.file_start_header = FILE_START_HEADER.replace("filename", f"{filename}")
        self.file_start_header = self.file_start_header.replace("FILE_NAME", f"{filename.upper()}")
        self.file_end_header = FILE_END_HEADER.replace("FILE_NAME", f"{filename.upper()}")
        self.output_dir = output_dir

    def createFile(self, name, start_header, code, end_header):
        if not (os.path.isdir(self.output_dir)):
            os.makedirs(self.output_dir)

        with open(self.output_dir + '/'+ name, 'w+') as f:
            f.writelines(COPYRIGHT)
            f.writelines(start_header)
            f.writelines(code)
            f.writelines(end_header)

    def createHfile(self, structcode):
        self.createFile(self.filename, self.file_start_header, structcode, self.file_end_header)

    def createHPPfile(self, structcode):
        cppfile_start_header = self.file_start_header.replace(".h", ".hpp")
        self.createFile(self.filename.replace(".h", ".hpp"),
                        cppfile_start_header.replace("_H", "_HPP"),
                        structcode,
                        self.file_end_header.replace("_H", "_HPP"))
