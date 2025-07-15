#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Gl_journal, Gl_acct, Gl_jourhis

def gl_view_transactionbl(srecid:int, jnr:int, refno:string):

    prepare_cache ([Gl_acct])

    b3_list_data = []
    gl_journal = gl_acct = gl_jourhis = None

    joulist = b3_list = gl_acct1 = None

    joulist_data, Joulist = create_model_like(Gl_journal, {"selflag":bool})
    b3_list_data, B3_list = create_model("B3_list", {"fibukonto":string, "debit":Decimal, "credit":Decimal, "bemerk":string, "userinit":string, "sysdate":date, "chginit":string, "chgdate":date, "selflag":bool, "bezeich":string})

    Gl_acct1 = create_buffer("Gl_acct1",Gl_acct)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal b3_list_data, gl_journal, gl_acct, gl_jourhis
        nonlocal srecid, jnr, refno
        nonlocal gl_acct1


        nonlocal joulist, b3_list, gl_acct1
        nonlocal joulist_data, b3_list_data

        return {"b3-list": b3_list_data}

    def get_bemerk(bemerk:string):

        nonlocal b3_list_data, gl_journal, gl_acct, gl_jourhis
        nonlocal srecid, jnr, refno
        nonlocal gl_acct1


        nonlocal joulist, b3_list, gl_acct1
        nonlocal joulist_data, b3_list_data

        n:int = 0
        s1:string = ""
        bemerk = replace_str(bemerk, chr_unicode(10) , " ")
        n = get_index(bemerk, ";&&")

        if n > 0:
            s1 = substring(bemerk, 0, n - 1)
        else:
            s1 = bemerk
        return s1

    gl_journal = get_cache (Gl_journal, {"jnr": [(eq, jnr)],"_recid": [(eq, srecid)]})

    if gl_journal:

        for gl_journal in db_session.query(Gl_journal).filter(
                 (Gl_journal.jnr == jnr)).order_by(Gl_journal._recid).all():
            joulist = Joulist()
            joulist_data.append(joulist)

            buffer_copy(gl_journal, joulist)
            joulist.bemerk = to_string(get_bemerk (joulist.bemerk) , "x(50)")

            if to_int(gl_journal._recid) == srecid:
                joulist.selflag = True


    else:

        for gl_jourhis in db_session.query(Gl_jourhis).filter(
                 (Gl_jourhis.jnr == jnr)).order_by(Gl_jourhis._recid).all():
            joulist = Joulist()
            joulist_data.append(joulist)

            buffer_copy(gl_jourhis, joulist)
            joulist.bemerk = to_string(get_bemerk (joulist.bemerk) , "x(50)")

            if to_int(gl_jourhis._recid) == srecid:
                joulist.selflag = True

    for joulist in query(joulist_data, filters=(lambda joulist: joulist.jnr == jnr), sort_by=[("selflag",True),("fibukonto",False)]):

        gl_acct1 = get_cache (Gl_acct, {"fibukonto": [(eq, joulist.fibukonto)]})

        if gl_acct1:
            b3_list = B3_list()
            b3_list_data.append(b3_list)

            b3_list.fibukonto = gl_acct1.fibukonto
            b3_list.debit =  to_decimal(joulist.debit)
            b3_list.credit =  to_decimal(joulist.credit)
            b3_list.bemerk = joulist.bemerk
            b3_list.userinit = joulist.userinit
            b3_list.sysdate = joulist.sysdate
            b3_list.chginit = joulist.chginit
            b3_list.chgdate = joulist.chgdate
            b3_list.selflag = joulist.selFlag
            b3_list.bezeich = gl_acct1.bezeich

    return generate_output()