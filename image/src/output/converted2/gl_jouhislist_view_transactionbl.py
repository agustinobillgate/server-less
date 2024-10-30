from functions.additional_functions import *
import decimal
from datetime import date
from models import Gl_jourhis, Gl_acct

def gl_jouhislist_view_transactionbl(jnr:int):
    detail_trans_list = []
    gl_jourhis = gl_acct = None

    detail_trans = gl_jou = gl_acct1 = None

    detail_trans_list, Detail_trans = create_model("Detail_trans", {"fibukonto":str, "debit":decimal, "credit":decimal, "bemerk":str, "userinit":str, "sysdate":date, "chginit":str, "chgdate":date, "bezeich":str})

    Gl_jou = create_buffer("Gl_jou",Gl_jourhis)
    Gl_acct1 = create_buffer("Gl_acct1",Gl_acct)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal detail_trans_list, gl_jourhis, gl_acct
        nonlocal jnr
        nonlocal gl_jou, gl_acct1


        nonlocal detail_trans, gl_jou, gl_acct1
        nonlocal detail_trans_list

        return {"detail-trans": detail_trans_list}

    def get_bemerk(bemerk:str):

        nonlocal detail_trans_list, gl_jourhis, gl_acct
        nonlocal jnr
        nonlocal gl_jou, gl_acct1


        nonlocal detail_trans, gl_jou, gl_acct1
        nonlocal detail_trans_list

        n:int = 0
        s1:str = ""
        bemerk = replace_str(bemerk, chr(10) , " ")
        n = 1 + get_index(bemerk, ";&&")

        if n > 0:
            s1 = substring(bemerk, 0, n - 1)
        else:
            s1 = bemerk
        return s1


    gl_jou_obj_list = []
    for gl_jou, gl_acct1 in db_session.query(Gl_jou, Gl_acct1).join(Gl_acct1,(Gl_acct1.fibukonto == Gl_jou.fibukonto)).filter(
             (Gl_jou.jnr == jnr)).order_by(Gl_acct1.fibukonto).all():
        if gl_jou._recid in gl_jou_obj_list:
            continue
        else:
            gl_jou_obj_list.append(gl_jou._recid)


        detail_trans = Detail_trans()
        detail_trans_list.append(detail_trans)

        detail_trans.fibukonto = gl_acct1.fibukonto
        detail_trans.debit =  to_decimal(gl_jou.debit)
        detail_trans.credit =  to_decimal(gl_jou.credit)
        detail_trans.bemerk = to_string(get_bemerk (gl_jou.bemerk) , "x(50)")
        detail_trans.userinit = gl_jou.userinit
        detail_trans.sysdate = gl_jou.sysdate
        detail_trans.chginit = gl_jou.chginit
        detail_trans.chgdate = gl_jou.chgdate
        detail_trans.bezeich = gl_acct1.bezeich

    return generate_output()