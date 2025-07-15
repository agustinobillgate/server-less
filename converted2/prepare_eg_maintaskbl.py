#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy, Htparam, Bediener

def prepare_eg_maintaskbl(user_init:string):

    prepare_cache ([Htparam, Bediener])

    engid = 0
    groupid = 0
    t_queasy_data = []
    t_queasy132_data = []
    tcategory_data = []
    queasy = htparam = bediener = None

    tcategory = t_queasy = t_queasy132 = None

    tcategory_data, Tcategory = create_model("Tcategory", {"categ_nr":int, "categ_nm":string, "str":string})
    t_queasy_data, T_queasy = create_model_like(Queasy, {"rec_id":int})
    t_queasy132_data, T_queasy132 = create_model_like(Queasy, {"rec_id":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal engid, groupid, t_queasy_data, t_queasy132_data, tcategory_data, queasy, htparam, bediener
        nonlocal user_init


        nonlocal tcategory, t_queasy, t_queasy132
        nonlocal tcategory_data, t_queasy_data, t_queasy132_data

        return {"engid": engid, "groupid": groupid, "t-queasy": t_queasy_data, "t-queasy132": t_queasy132_data, "tCategory": tcategory_data}

    def create_categ():

        nonlocal engid, groupid, t_queasy_data, t_queasy132_data, tcategory_data, queasy, htparam, bediener
        nonlocal user_init


        nonlocal tcategory, t_queasy, t_queasy132
        nonlocal tcategory_data, t_queasy_data, t_queasy132_data

        qbuff = None
        Qbuff =  create_buffer("Qbuff",Queasy)
        tcategory_data.clear()
        tcategory = Tcategory()
        tcategory_data.append(tcategory)

        tcategory.categ_nr = 0
        tcategory.categ_nm = ""

        for qbuff in db_session.query(Qbuff).filter(
                 (Qbuff.key == 132)).order_by(Qbuff._recid).all():
            tcategory = Tcategory()
            tcategory_data.append(tcategory)

            tcategory.categ_nr = qbuff.number1
            tcategory.categ_nm = qbuff.char1


    def define_engineering():

        nonlocal engid, groupid, t_queasy_data, t_queasy132_data, tcategory_data, queasy, htparam, bediener
        nonlocal user_init


        nonlocal tcategory, t_queasy, t_queasy132
        nonlocal tcategory_data, t_queasy_data, t_queasy132_data

        htparam = get_cache (Htparam, {"paramnr": [(eq, 1200)],"feldtyp": [(eq, 1)]})

        if htparam:
            engid = htparam.finteger


        else:
            engid = 0


    def define_group():

        nonlocal engid, groupid, t_queasy_data, t_queasy132_data, tcategory_data, queasy, htparam, bediener
        nonlocal user_init


        nonlocal tcategory, t_queasy, t_queasy132
        nonlocal tcategory_data, t_queasy_data, t_queasy132_data

        bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

        if bediener:
            groupid = bediener.user_group

    define_group()
    define_engineering()
    create_categ()

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 133)).order_by(Queasy._recid).all():
        t_queasy = T_queasy()
        t_queasy_data.append(t_queasy)

        buffer_copy(queasy, t_queasy)
        t_queasy.rec_id = queasy._recid

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 132)).order_by(Queasy._recid).all():
        t_queasy132 = T_queasy132()
        t_queasy132_data.append(t_queasy132)

        buffer_copy(queasy, t_queasy132)
        t_queasy132.rec_id = queasy._recid

    return generate_output()