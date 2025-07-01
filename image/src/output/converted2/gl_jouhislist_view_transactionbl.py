#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Gl_jourhis, Gl_acct

def gl_jouhislist_view_transactionbl(jnr:int):

    prepare_cache ([Gl_jourhis, Gl_acct])

    detail_trans_list = []
    gl_jourhis = gl_acct = None

    detail_trans = gl_jou = gl_acct1 = None

    detail_trans_list, Detail_trans = create_model("Detail_trans", {"fibukonto":string, "debit":Decimal, "credit":Decimal, "bemerk":string, "userinit":string, "sysdate":date, "chginit":string, "chgdate":date, "bezeich":string})

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

    def get_bemerk(bemerk:string):

        nonlocal detail_trans_list, gl_jourhis, gl_acct
        nonlocal jnr
        nonlocal gl_jou, gl_acct1


        nonlocal detail_trans, gl_jou, gl_acct1
        nonlocal detail_trans_list

        n:int = 0
        s1:string = ""
        bemerk = replace_str(bemerk, chr_unicode(10) , " ")
        n = get_index(bemerk, ";&&")

        if n > 0:
            s1 = substring(bemerk, 0, n - 1)
        else:
            s1 = bemerk
        return s1


    gl_jou_obj_list = {}
    gl_jou = Gl_jourhis()
    gl_acct1 = Gl_acct()
    for gl_jou.debit, gl_jou.credit, gl_jou.bemerk, gl_jou.userinit, gl_jou.sysdate, gl_jou.chginit, gl_jou.chgdate, gl_jou._recid, gl_acct1.fibukonto, gl_acct1.bezeich, gl_acct1._recid in db_session.query(Gl_jou.debit, Gl_jou.credit, Gl_jou.bemerk, Gl_jou.userinit, Gl_jou.sysdate, Gl_jou.chginit, Gl_jou.chgdate, Gl_jou._recid, Gl_acct1.fibukonto, Gl_acct1.bezeich, Gl_acct1._recid).join(Gl_acct1,(Gl_acct1.fibukonto == Gl_jou.fibukonto)).filter(
             (Gl_jou.jnr == jnr)).order_by(Gl_acct1.fibukonto).all():
        if gl_jou_obj_list.get(gl_jou._recid):
            continue
        else:
            gl_jou_obj_list[gl_jou._recid] = True


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