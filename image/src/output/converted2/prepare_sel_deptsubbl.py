#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Htparam, Queasy, Eg_subtask

def prepare_sel_deptsubbl():

    prepare_cache ([Htparam, Queasy, Eg_subtask])

    engid = 0
    msg_flag = False
    deptsub_list = []
    htparam = queasy = eg_subtask = None

    deptsub = None

    deptsub_list, Deptsub = create_model("Deptsub", {"deptsub_nr":int, "deptsub_nm":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal engid, msg_flag, deptsub_list, htparam, queasy, eg_subtask


        nonlocal deptsub
        nonlocal deptsub_list

        return {"engid": engid, "msg_flag": msg_flag, "DeptSub": deptsub_list}

    def define_engineering():

        nonlocal engid, msg_flag, deptsub_list, htparam, queasy, eg_subtask


        nonlocal deptsub
        nonlocal deptsub_list

        htparam = get_cache (Htparam, {"paramnr": [(eq, 1200)],"feldtyp": [(eq, 1)]})

        if htparam:
            engid = htparam.finteger


        else:
            engid = 0
            msg_flag = True


    def create_related_dept():

        nonlocal engid, msg_flag, deptsub_list, htparam, queasy, eg_subtask


        nonlocal deptsub
        nonlocal deptsub_list

        i:int = 0
        c:int = 0
        qbuff = None
        Qbuff =  create_buffer("Qbuff",Queasy)
        deptsub_list.clear()

        queasy = get_cache (Queasy, {"key": [(eq, 19)],"number1": [(eq, engid)]})

        if queasy:
            deptsub = Deptsub()
            deptsub_list.append(deptsub)

            deptsub.deptsub_nr = engid
            deptsub.deptsub_nm = queasy.char3


            for i in range(1,num_entries(queasy.char2, ";")  + 1) :
                c = to_int(entry(i - 1, queasy.char2, ";"))

                qbuff = get_cache (Queasy, {"key": [(eq, 19)],"number1": [(eq, to_int(entry(i - 1, queasy.char2, ";")))]})

                if qbuff:
                    deptsub = Deptsub()
                    deptsub_list.append(deptsub)

                    deptsub.deptsub_nr = c
                    deptsub.deptsub_nm = qbuff.char3


    def create_deptsub():

        nonlocal engid, msg_flag, deptsub_list, htparam, queasy, eg_subtask


        nonlocal deptsub
        nonlocal deptsub_list

        qbuff = None
        qbuff1 = None
        Qbuff =  create_buffer("Qbuff",Eg_subtask)
        Qbuff1 =  create_buffer("Qbuff1",Queasy)
        deptsub_list.clear()

        for qbuff in db_session.query(Qbuff).order_by(Qbuff._recid).all():

            deptsub = query(deptsub_list, filters=(lambda deptsub: deptsub.deptsub_nr == qbuff.dept_nr), first=True)

            if deptsub:
                pass
            else:

                qbuff1 = get_cache (Queasy, {"key": [(eq, 19)],"number1": [(eq, qbuff.dept_nr)]})

                if qbuff1:
                    deptsub = Deptsub()
                    deptsub_list.append(deptsub)

                    deptsub.deptsub_nr = qbuff.dept_nr
                    deptsub.deptsub_nm = qbuff1.char3


                else:
                    pass

    define_engineering()
    create_related_dept()

    return generate_output()