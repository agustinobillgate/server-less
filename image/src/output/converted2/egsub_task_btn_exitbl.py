#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Eg_subtask

subtask_list, Subtask = create_model_like(Eg_subtask)

def egsub_task_btn_exitbl(subtask_list:[Subtask], case_type:int, user_init:string, rec_id:int):

    prepare_cache ([Eg_subtask])

    fl_code = 0
    eg_subtask = None

    subtask = subbuff = None

    Subbuff = create_buffer("Subbuff",Eg_subtask)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal fl_code, eg_subtask
        nonlocal case_type, user_init, rec_id
        nonlocal subbuff


        nonlocal subtask, subbuff

        return {"fl_code": fl_code}

    subtask = query(subtask_list, first=True)

    if case_type == 1:
        eg_subtask = Eg_subtask()
        db_session.add(eg_subtask)

        subtask.create_date = get_current_date()
        subtask.create_time = get_current_time_in_seconds()
        subtask.create_by = user_init
        subtask.sourceform = "0"


        buffer_copy(subtask, eg_subtask)

    elif case_type == 2:

        subbuff = get_cache (Eg_subtask, {"main_nr": [(eq, subtask.main_nr)],"bezeich": [(eq, subtask.bezeich)],"sub_code": [(ne, subtask.sub_code)]})

        if subBuff:
            fl_code = 1
        else:

            eg_subtask = get_cache (Eg_subtask, {"dept_nr": [(eq, subtask.dept_nr)],"main_nr": [(eq, subtask.main_nr)],"sub_code": [(eq, subtask.sub_code)]})

            if eg_subtask:

                if eg_subtask.othersflag != subtask.othersflag:

                    if subtask.othersflag :

                        eg_subtask = get_cache (Eg_subtask, {"dept_nr": [(eq, subtask.dept_nr)],"main_nr": [(eq, subtask.main_nr)],"sub_code": [(ne, subtask.sub_code)],"othersflag": [(eq, True)]})

                        if eg_subtask:
                            fl_code = 2
                        else:

                            eg_subtask = get_cache (Eg_subtask, {"_recid": [(eq, rec_id)]})
                            pass
                            buffer_copy(subtask, eg_subtask)
                            pass
                            pass
                            fl_code = 3
                    else:

                        eg_subtask = get_cache (Eg_subtask, {"_recid": [(eq, rec_id)]})
                        pass
                        buffer_copy(subtask, eg_subtask)
                        pass
                        pass
                        fl_code = 3
                else:

                    eg_subtask = get_cache (Eg_subtask, {"_recid": [(eq, rec_id)]})
                    pass
                    buffer_copy(subtask, eg_subtask)
                    pass
                    pass
                    fl_code = 3

    return generate_output()