from functions.additional_functions import *
import decimal

def clear_comments(input_file:str, output_file:str):
    char1:str = ""
    char2:str = ""
    i:int = 0
    tmp_str:str = ""
    tmp_str2:str = ""
    num_comment:int = 0
    iscomment:bool = False
    hascomment:bool = False
    isstring1:bool = False
    isstring2:bool = False
    single_comment:bool = False
    comment_start:int = 0
    comment_end:int = 0
    start_substring:int = 1


    db_session = local_storage.db_session

    def generate_output():
        nonlocal char1, char2, i, tmp_str, tmp_str2, num_comment, iscomment, hascomment, isstring1, isstring2, single_comment, comment_start, comment_end, start_substring
        nonlocal input_file, output_file

        return {}


    for i in range(1,len(char1)  + 1) :
        tmp_str = substring(char1, i - 1, 2)

        if single_comment:
            single_comment = False

        elif re.match('".*',tmp_str, re.IGNORECASE) and num_comment == 0 and not isstring2:
            isstring1 = not isstring1

        elif re.match(r"'.*",tmp_str, re.IGNORECASE) and num_comment == 0 and not isstring1:
            isstring2 = not isstring2

        elif tmp_str == "" and not single_comment and not isstring1 and not isstring2:
            single_comment = True
            num_comment = num_comment - 1
            comment_end = i

        if iscomment and num_comment == 0 and not single_comment:
            iscomment = False
            char2 = char2 + substring(char1, start_substring - 1, comment_start - start_substring)
            start_substring = i + 1

    if hascomment:
        char2 = char2 + substring(char1, comment_end + 2 - 1, len(char1) - comment_end)
    else:
        char2 = char1


    return generate_output()