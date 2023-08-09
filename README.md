# Header Generator
## Introduction
This header generation scripts provides the capabilities to generate a .h and .hpp files automatically from a key-value text based file(json)

## Directory structure

├── **C_HeaderGeneratorProject/**   
│   │   ├── Config/  
│   │   │   └── Example.json  
│   │   ├── FileCreator/  
│   │   │   └── CFileHandler.py  
│   │   ├── JsontoC_HeaderGenerator.py   
│   │   └── template.json  

**Config/:** Contains input json files
**Example.json:** input example config file that contains C structs and data to be generated in the header file  
**template.json:** Reference file/guide to be followed when adding new elements into input json file  
**JsontoC_HeaderGenerator.py:** The main Python script to be run for header file generation. Check [Usage](#Usage) for more details  
**CFileHandler.py:** A class to be used for creation of C header files. Will be called by JsontoC_HeaderGenerator.py    

## Usage
To generate the desired header files,
1. Clone the repository into a local workspace
2. Fill up structure/data definition in json file format. Follow the template.json for valid data structure. Save the name of the json file appropriately. **The name of json input file will be the name of the generated header file!**

3. Execute the main python script:  `JsontoC_HeaderGenerator.py`
	```shell
 	$ cd <PATH_TO_WORKSPACE>/ProjectsForFun/C_HeaderGeneratorProject/
	$ python JsontoC_HeaderGenerator.py -c ./Config/Example.json

	Optional Argument:
		-c/--config    [Path to config json file]
		-o/--output-dir [Name of output dir where generated files will be placed]
		
	By default the script will parse all json files in Config/
	```
4.  An output folder will be created in the same level.

5.  Check the files generated under name of output directory OR "Generated/" by default
