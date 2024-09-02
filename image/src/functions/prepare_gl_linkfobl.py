from functions.additional_functions import *
import decimal
from datetime import date
from models import Artikel, Htparam, Guest, Gl_acct, Hoteldpt

def prepare_gl_linkfobl(pvilanguage:int, combo_pf_file1:str, combo_pf_file2:str, combo_gastnr:int, combo_ledger:int, combo_gl_link:bool):
    f_int = 0
    last_acctdate = None
    acct_date = None
    close_year = None
    price_decimal = 0
    cash_fibu = ""
    msg_str = ""
    lvcarea:str = "gl_linkfo"
    artikel = htparam = guest = gl_acct = hoteldpt = None

    trans_dept = art2 = None

    trans_dept_list, Trans_dept = create_model("Trans_dept", {"nr":int})

    Art2 = Artikel

    db_session = local_storage.db_session

    def generate_output():
        nonlocal f_int, last_acctdate, acct_date, close_year, price_decimal, cash_fibu, msg_str, lvcarea, artikel, htparam, guest, gl_acct, hoteldpt
        nonlocal art2


        nonlocal trans_dept, art2
        nonlocal trans_dept_list
        return {"f_int": f_int, "last_acctdate": last_acctdate, "acct_date": acct_date, "close_year": close_year, "price_decimal": price_decimal, "cash_fibu": cash_fibu, "msg_str": msg_str}

    def check_dept():

        nonlocal f_int, last_acctdate, acct_date, close_year, price_decimal, cash_fibu, msg_str, lvcarea, artikel, htparam, guest, gl_acct, hoteldpt
        nonlocal art2


        nonlocal trans_dept, art2
        nonlocal trans_dept_list

        i:int = 0
        trans_dept_list.clear()

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 793)).first()

        if htparam.fchar != "":
            for i in range(1,num_entries(htparam.fchar, ",")  + 1) :

                trans_dept = query(trans_dept_list, filters=(lambda trans_dept :trans_dept.nr == to_int(entry(i - 1, htparam.fchar, ","))), first=True)

                if not trans_dept:
                    trans_dept = Trans_dept()
                    trans_dept_list.append(trans_dept)

                    nr = to_int(entry(i - 1, htparam.fchar, ","))


        else:

            for hoteldpt in db_session.query(Hoteldpt).all():
                trans_dept = Trans_dept()
                trans_dept_list.append(trans_dept)

                nr = hoteldpt.num

    if combo_gastnr == None:

        htparam = db_session.query(Htparam).filter(
                (htpara.paramnr == 155)).first()
        combo_gastnr = htparam.finteger

        if combo_gastnr > 0:

            guest = db_session.query(Guest).filter(
                    (Guest.gastnr == combo_gastnr)).first()

            if not guest:
                combo_gastnr = 0
            else:
                combo_ledger = guest.zahlungsart

            if combo_ledger > 0:

                artikel = db_session.query(Artikel).filter(
                        (Artikel.artnr == combo_ledger) &  (Artikel.departement == 0) &  (Artikel.artart == 2)).first()

                if not artikel:
                    combo_gastnr = 0
                    combo_ledger = 0


            else:
                combo_gastnr = 0
        else:
            combo_gastnr = 0

    if combo_gastnr > 0:

        htparam = db_session.query(Htparam).filter(
                (htpara.paramnr == 339)).first()
        combo_pf_file1 = htparam.fchar

        htparam = db_session.query(Htparam).filter(
                (htpara.paramnr == 340)).first()
        combo_pf_file2 = htparam.fchar

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 343)).first()
        combo_gl_link = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1012)).first()

    if htparam.paramgruppe == 38 and htparam.feldtyp == 1 and htparam.finteger > 0:
        f_int = htparam.finteger
    check_dept()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1003)).first()
    last_acctdate = htparam.fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 597)).first()
    acct_date = htparam.fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 795)).first()
    close_year = htparam.fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 491)).first()
    price_decimal = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 112)).first()

    art2 = db_session.query(Art2).filter(
            (Art2.artnr == htparam.finteger) &  (Art2.departement == 0) &  (Art2.artart == 6) &  (not Art2.pricetab)).first()

    if not art2:
        msg_str = msg_str + chr(2) + translateExtended ("Local Cash Article not defined! (Param 112 / Grp 5).", lvcarea, "")

        return generate_output()

    gl_acct = db_session.query(Gl_acct).filter(
            (Gl_acct.fibukonto == art2.fibukonto)).first()

    if not gl_acct:
        msg_str = msg_str + chr(2) + translateExtended ("AcctNo of Cash Article", lvcarea, "") + " " + to_string(art2.artnr) + " " + translateExtended ("not defined.", lvcarea, "")

        return generate_output()
    cash_fibu = gl_acct.fibukonto

    return generate_output()