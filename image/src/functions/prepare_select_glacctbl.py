from functions.additional_functions import *
import decimal
from models import Queasy, Gl_department, Htparam, Gl_acct

def prepare_select_glacctbl(curr_dept:int):
    from_fibu = ""
    glacct_list_list = []
    gl_depart_list_list = []
    t_queasy_list = []
    queasy = gl_department = htparam = gl_acct = None

    t_queasy = glacct_list = gl_depart_list = None

    t_queasy_list, T_queasy = create_model_like(Queasy)
    glacct_list_list, Glacct_list = create_model("Glacct_list", {"fibukonto":str, "bezeich":str, "acc_type":int, "deptnr":int, "subdept_nr":int, "subdept_bez":str, "main_nr":int, "activeflag":bool})
    gl_depart_list_list, Gl_depart_list = create_model_like(Gl_department)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal from_fibu, glacct_list_list, gl_depart_list_list, t_queasy_list, queasy, gl_department, htparam, gl_acct


        nonlocal t_queasy, glacct_list, gl_depart_list
        nonlocal t_queasy_list, glacct_list_list, gl_depart_list_list
        return {"from_fibu": from_fibu, "glacct-list": glacct_list_list, "gl-depart-list": gl_depart_list_list, "t-queasy": t_queasy_list}

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 551)).first()

    if htparam.paramgruppe == 38 and htparam.fchar != "":
        from_fibu = htparam.fchar

    if curr_dept == 0:

        for gl_acct in db_session.query(Gl_acct).filter(
                (Gl_acct.fibukonto >= from_fibu) &  (Gl_acct.activeflag)).all():
            glacct_list = Glacct_list()
            glacct_list_list.append(glacct_list)

            glacct_list.fibukonto = gl_acct.fibukonto
            glacct_list.bezeich = gl_acct.bezeich
            glacct_list.acc_type = gl_acct.acc_type
            glacct_list.deptnr = gl_acct.deptnr
            glacct_list.main_nr = gl_acct.main_nr
            glacct_list.activeflag = gl_acct.activeflag

    else:

        for gl_acct in db_session.query(Gl_acct).filter(
                (Gl_acct.deptnr == curr_dept) &  (Gl_acct.fibukonto >= from_fibu) &  (Gl_acct.activeflag)).all():
            glacct_list = Glacct_list()
            glacct_list_list.append(glacct_list)

            glacct_list.fibukonto = gl_acct.fibukonto
            glacct_list.bezeich = gl_acct.bezeich
            glacct_list.acc_type = gl_acct.acc_type
            glacct_list.deptnr = gl_acct.deptnr
            glacct_list.main_nr = gl_acct.main_nr
            glacct_list.activeflag = gl_acct.activeflag


    for gl_depart_list in query(gl_depart_list_list):
        gl_depart_list = Gl_depart_list()
        gl_depart_list_list.append(gl_depart_list)

        buffer_copy(gl_department, gl_depart_list)

    for queasy in db_session.query(Queasy).filter(
            (Queasy.key == 155)).all():
        t_queasy = T_queasy()
        t_queasy_list.append(t_queasy)

        buffer_copy(queasy, t_queasy)

    return generate_output()