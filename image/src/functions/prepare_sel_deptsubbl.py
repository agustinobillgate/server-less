from functions.additional_functions import *
import decimal
from models import Htparam, Queasy, Eg_subtask

def prepare_sel_deptsubbl():
    engid = 0
    msg_flag = False
    deptsub_list = []
    htparam = queasy = eg_subtask = None

    deptsub = qbuff = qbuff1 = None

    deptsub_list, Deptsub = create_model("Deptsub", {"deptsub_nr":int, "deptsub_nm":str})

    Qbuff = Eg_subtask
    Qbuff1 = Queasy

    db_session = local_storage.db_session

    def generate_output():
        nonlocal engid, msg_flag, deptsub_list, htparam, queasy, eg_subtask
        nonlocal qbuff, qbuff1


        nonlocal deptsub, qbuff, qbuff1
        nonlocal deptsub_list
        return {"engid": engid, "msg_flag": msg_flag, "DeptSub": deptsub_list}

    def define_engineering():

        nonlocal engid, msg_flag, deptsub_list, htparam, queasy, eg_subtask
        nonlocal qbuff, qbuff1


        nonlocal deptsub, qbuff, qbuff1
        nonlocal deptsub_list

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1200) &  (Htparam.feldtyp == 1)).first()

        if htparam:
            engid = htparam.finteger


        else:
            engid = 0
            msg_flag = True

    def create_related_dept():

        nonlocal engid, msg_flag, deptsub_list, htparam, queasy, eg_subtask
        nonlocal qbuff, qbuff1


        nonlocal deptsub, qbuff, qbuff1
        nonlocal deptsub_list

        i:int = 0
        c:int = 0
        Qbuff = Queasy
        deptsub_list.clear()

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 19) &  (Queasy.number1 == engid)).first()

        if queasy:
            deptsub = Deptsub()
            deptsub_list.append(deptsub)

            deptsub.deptsub_nr = engid
            deptsub.deptsub_nm = queasy.char3


            for i in range(1,num_entries(queasy.char2, ";")  + 1) :
                c = to_int(entry(i - 1, queasy.char2, ";"))

                qbuff = db_session.query(Qbuff).filter(
                        (Qbuff.key == 19) &  (Qbuff.number1 == to_int(entry(i - 1, queasy.char2, ";")))).first()

                if qbuff:
                    deptsub = Deptsub()
                    deptsub_list.append(deptsub)

                    deptsub.deptsub_nr = c
                    deptsub.deptsub_nm = qbuff.char3

    def create_deptsub():

        nonlocal engid, msg_flag, deptsub_list, htparam, queasy, eg_subtask
        nonlocal qbuff, qbuff1


        nonlocal deptsub, qbuff, qbuff1
        nonlocal deptsub_list


        Qbuff = Eg_subtask
        Qbuff1 = Queasy
        deptsub_list.clear()

        for qbuff in db_session.query(Qbuff).all():

            deptsub = query(deptsub_list, filters=(lambda deptsub :deptsub.deptsub_nr == qbuff.dept_nr), first=True)

            if deptsub:
                pass
            else:

                qbuff1 = db_session.query(Qbuff1).filter(
                        (Qbuff1.key == 19) &  (Qbuff1.number1 == qbuff.dept_nr)).first()

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