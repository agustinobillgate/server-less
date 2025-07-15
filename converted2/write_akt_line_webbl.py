#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from functions.upload_imagesetupbl import upload_imagesetupbl
from functions.delete_imagesetupbl import delete_imagesetupbl
from models import Akt_line

akt_line1_data, Akt_line1 = create_model_like(Akt_line)

def write_akt_line_webbl(case_type:int, file_mode:int, base64file:string, user_init:string, akt_line1_data:[Akt_line1]):
    success_flag = False
    result_message = ""
    curr_counter:int = 0
    akt_line = None

    akt_line1 = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, result_message, curr_counter, akt_line
        nonlocal case_type, file_mode, base64file, user_init, akt_line1_data


        nonlocal akt_line1

        return {"success_flag": success_flag, "result_message": result_message}

    akt_line1 = query(akt_line1_data, first=True)

    if not akt_line1:

        return generate_output()
    curr_counter = akt_line1.linenr

    if base64file == None:
        base64file = ""

    if case_type == 1:
        akt_line = Akt_line()
        db_session.add(akt_line)

        buffer_copy(akt_line1, akt_line)
        success_flag = True
        pass

        if success_flag:

            if base64file != "" and user_init != "":
                result_message = get_output(upload_imagesetupbl(file_mode, base64file, user_init, curr_counter))
    elif case_type == 2:

        akt_line = get_cache (Akt_line, {"linenr": [(eq, akt_line1.linenr)]})

        if akt_line:
            buffer_copy(akt_line1, akt_line)
            success_flag = True
        pass

        if success_flag:

            if akt_line1.flag == 2:
                result_message, base64file = get_output(delete_imagesetupbl(file_mode, curr_counter))
            else:

                if base64file != "" and user_init != "":
                    result_message = get_output(upload_imagesetupbl(file_mode, base64file, user_init, curr_counter))

    return generate_output()