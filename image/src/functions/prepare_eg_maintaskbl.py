from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Queasy, Htparam, Bediener

def prepare_eg_maintaskbl(user_init:str):
    engid = 0
    groupid = 0
    t_queasy_list = []
    t_queasy132_list = []
    tcategory_list = []
    queasy = htparam = bediener = None

    tcategory = t_queasy = t_queasy132 = qbuff = None

    tcategory_list, Tcategory = create_model("Tcategory", {"categ_nr":int, "categ_nm":str, "str":str})
    t_queasy_list, T_queasy = create_model_like(Queasy, {"rec_id":int})
    t_queasy132_list, T_queasy132 = create_model_like(Queasy, {"rec_id":int})

    Qbuff = Queasy

    db_session = local_storage.db_session

    def generate_output():
        nonlocal engid, groupid, t_queasy_list, t_queasy132_list, tcategory_list, queasy, htparam, bediener
        nonlocal qbuff


        nonlocal tcategory, t_queasy, t_queasy132, qbuff
        nonlocal tcategory_list, t_queasy_list, t_queasy132_list
        return {"engid": engid, "groupid": groupid, "t-queasy": t_queasy_list, "t-queasy132": t_queasy132_list, "tCategory": tcategory_list}

    def create_categ():

        nonlocal engid, groupid, t_queasy_list, t_queasy132_list, tcategory_list, queasy, htparam, bediener
        nonlocal qbuff


        nonlocal tcategory, t_queasy, t_queasy132, qbuff
        nonlocal tcategory_list, t_queasy_list, t_queasy132_list


        Qbuff = Queasy
        tcategory_list.clear()
        tcategory = Tcategory()
        tcategory_list.append(tcategory)

        tcategory.categ_nr = 0
        tcategory.categ_nm = ""

        for qbuff in db_session.query(Qbuff).filter(
                (Qbuff.key == 132)).all():
            tcategory = Tcategory()
            tcategory_list.append(tcategory)

            tcategory.categ_nr = qbuff.number1
            tcategory.categ_nm = qbuff.CHAR1

    def define_engineering():

        nonlocal engid, groupid, t_queasy_list, t_queasy132_list, tcategory_list, queasy, htparam, bediener
        nonlocal qbuff


        nonlocal tcategory, t_queasy, t_queasy132, qbuff
        nonlocal tcategory_list, t_queasy_list, t_queasy132_list

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1200) &  (Htparam.feldtyp == 1)).first()

        if htparam:
            engid = htparam.finteger


        else:
            engid = 0

    def define_group():

        nonlocal engid, groupid, t_queasy_list, t_queasy132_list, tcategory_list, queasy, htparam, bediener
        nonlocal qbuff


        nonlocal tcategory, t_queasy, t_queasy132, qbuff
        nonlocal tcategory_list, t_queasy_list, t_queasy132_list

        bediener = db_session.query(Bediener).filter(
                (func.lower(Bediener.userinit) == (user_init).lower())).first()

        if bediener:
            groupid = bediener.user_group


    define_group()
    define_engineering()
    create_categ()

    for queasy in db_session.query(Queasy).filter(
            (Queasy.key == 133)).all():
        t_queasy = T_queasy()
        t_queasy_list.append(t_queasy)

        buffer_copy(queasy, t_queasy)
        t_queasy.rec_id = queasy._recid

    for queasy in db_session.query(Queasy).filter(
            (Queasy.key == 132)).all():
        t_queasy132 = T_queasy132()
        t_queasy132_list.append(t_queasy132)

        buffer_copy(queasy, t_queasy132)
        t_queasy132.rec_id = queasy._recid

    return generate_output()