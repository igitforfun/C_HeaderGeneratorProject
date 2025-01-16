/******************************************************************************
* Copyright (C) [Message to be written in this segment]
 ******************************************************************************/
/**
 * @file Example.h
 * @brief [Insert your brief description about this file].
*/

#ifndef EXAMPLE_H
#define EXAMPLE_H

/******************************************************************************/
/* Constants and types */
/*============================================================================*/

#define PREMACRO1 0 //!< Description of Premacro 1
#define PREMACRO2 1 //!< Description of Premacro 2

/**
 * @brief Description of struct one
 */
typedef struct __attribute__((packed, aligned(1))) _struct_one_ {
    int var1;    //!< Description of var1
    char var2;    //!< Description of var2
    int var3;    //!< Description of var3
} struct_one;

/**
 * @brief Description of struct two
 */
typedef struct _struct_two_ {
    int param1;    //!< Description of param1
    bool param2;    //!< Description of param2
} struct_two;

/**
 * @brief Description of enumExample
 */
typedef enum _enumExample_ {
    enum1 = 0,    //!< Description of enum1
    enum2 = 1,    //!< Description of enum2
    enum3 = 2    //!< Description of enum3
} enumExample;

/**
 * @brief Description of enumExample two
 */
typedef enum _enumExampleTwo_ {
    enum1 = 0,    //!< Description of enum1
    enum2 = 10,    //!< Description of enum2
    enum3 = 99    //!< Description of enum3
} enumExampleTwo;

#endif /* EXAMPLE_H */
