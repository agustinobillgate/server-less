from functions.additional_functions import *
import decimal
from models import Gl_journal, Gl_acct, Gl_jourhis

def gl_view_transactionbl(srecid:int, jnr:int, refno:str):
    b3_list_list = []
    gl_journal = gl_acct = gl_jourhis = None

    joulist = b3_list = gl_acct1 = None

    joulist_list, Joulist = create_model_like(Gl_journal, {"selflag":bool})
    b3_list_list, B3_list = create_model("B3_list", {"fibukonto":str, "debit":decimal, "credit":decimal, "bemerk":str, "userinit":str, "sysdate":date, "chginit":str, "chgdate":date, "selflag":bool, "bezeich":str})

    Gl_acct1 = create_buffer("Gl_acct1",Gl_acct)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal b3_list_list, gl_journal, gl_acct, gl_jourhis
        nonlocal srecid, jnr, refno
        nonlocal gl_acct1


        nonlocal joulist, b3_list, gl_acct1
        nonlocal joulist_list, b3_list_list

        return {"b3-list": b3_list_list}

    def get_bemerk(bemerk:str):

        nonlocal b3_list_list, gl_journal, gl_acct, gl_jourhis
        nonlocal srecid, jnr, refno
        nonlocal gl_acct1


        nonlocal joulist, b3_list, gl_acct1
        nonlocal joulist_list, b3_list_list

        n:int = 0
        s1:str = ""
        bemerk = replace_str(bemerk, chr(10) , " ")
        n = 1 + get_index(bemerk, ";&&")

        if n > 0:
            s1 = substring(bemerk, 0, n - 1)
        else:
            s1 = bemerk
        return s1

    gl_journal = db_session.query(Gl_journal).filter(
             (Gl_journal.jnr == jnr) & (to_int(Gl_journal._recid) == srecid)).first()

    if gl_journal:

        for gl_journal in db_session.query(Gl_journal).filter(
                 (Gl_journal.jnr == jnr)).order_by(Gl_journal._recid).all():
            joulist = Joulist()
            joulist_list.append(joulist)

            buffer_copy(gl_journal, joulist)
            joulist.bemerk = to_string(get_bemerk (joulist.bemerk) , "x(50)")

            if to_int(gl_journal._recid) == srecid:
                joulist.selflag = True


    else:

        for gl_jourhis in db_session.query(Gl_jourhis).filter(
                 (Gl_jourhis.jnr == jnr)).order_by(Gl_jourhis._recid).all():
            joulist = Joulist()
            joulist_list.append(joulist)

            buffer_copy(gl_jourhis, joulist)
            joulist.bemerk = to_string(get_bemerk (joulist.bemerk) , "x(50)")

            if to_int(gl_jourhis._recid) == srecid:
                joulist.selflag = True

    gl_acct1_obj_list = []
    for gl_acct1 in db_session.query(Gl_acct1).filter(
             ((Gl_acct1.fibukonto.in_(list(set([joulist.fibukonto for joulist in joulist_list if joulist.jnr == jnr)]))))).order_by(joulist.selflag.desc(), Gl_acct1.fibukonto).all():
        if gl_acct1._recid in gl_acct1_obj_list:
            continue
        else:
            gl_acct1_obj_list.append(gl_acct1._recid)

        joulist = query(joulist_list, (lambda joulist: (gl_acct1.fibukonto == joulist.fibukonto)), first=True)
        b3_list = B3_list()
        b3_list_list.append(b3_list)

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