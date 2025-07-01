#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Artikel, Htparam, Guest, Gl_acct, Hoteldpt

def prepare_gl_linkfobl(pvilanguage:int, combo_pf_file1:string, combo_pf_file2:string, combo_gastnr:int, combo_ledger:int, combo_gl_link:bool):

    prepare_cache ([Artikel, Htparam, Guest, Gl_acct, Hoteldpt])

    f_int = 0
    last_acctdate = None
    acct_date = None
    close_year = None
    price_decimal = 0
    cash_fibu = ""
    msg_str = ""
    lvcarea:string = "gl-linkfo"
    last_acct_period:date = None
    tmpdate:date = None
    artikel = htparam = guest = gl_acct = hoteldpt = None

    trans_dept = art2 = None

    trans_dept_list, Trans_dept = create_model("Trans_dept", {"nr":int})

    Art2 = create_buffer("Art2",Artikel)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal f_int, last_acctdate, acct_date, close_year, price_decimal, cash_fibu, msg_str, lvcarea, last_acct_period, tmpdate, artikel, htparam, guest, gl_acct, hoteldpt
        nonlocal pvilanguage, combo_pf_file1, combo_pf_file2, combo_gastnr, combo_ledger, combo_gl_link
        nonlocal art2


        nonlocal trans_dept, art2
        nonlocal trans_dept_list

        return {"f_int": f_int, "last_acctdate": last_acctdate, "acct_date": acct_date, "close_year": close_year, "price_decimal": price_decimal, "cash_fibu": cash_fibu, "msg_str": msg_str, "combo_pf_file1": combo_pf_file1, "combo_pf_file2": combo_pf_file2, "combo_gastnr": combo_gastnr, "combo_ledger": combo_ledger, "combo_gl_link": combo_gl_link}

    def check_dept():

        nonlocal f_int, last_acctdate, acct_date, close_year, price_decimal, cash_fibu, msg_str, lvcarea, last_acct_period, tmpdate, artikel, htparam, guest, gl_acct, hoteldpt
        nonlocal pvilanguage, combo_pf_file1, combo_pf_file2, combo_gastnr, combo_ledger, combo_gl_link
        nonlocal art2


        nonlocal trans_dept, art2
        nonlocal trans_dept_list

        i:int = 0
        trans_dept_list.clear()

        htparam = get_cache (Htparam, {"paramnr": [(eq, 793)]})

        if htparam.fchar != "":
            for i in range(1,num_entries(htparam.fchar, ",")  + 1) :

                trans_dept = query(trans_dept_list, filters=(lambda trans_dept: trans_dept.nr == to_int(entry(i - 1, htparam.fchar, ","))), first=True)

                if not trans_dept:
                    trans_dept = Trans_dept()
                    trans_dept_list.append(trans_dept)

                    nr = to_int(entry(i - 1, htparam.fchar, ","))


        else:

            for hoteldpt in db_session.query(Hoteldpt).order_by(Hoteldpt._recid).all():
                trans_dept = Trans_dept()
                trans_dept_list.append(trans_dept)

                nr = hoteldpt.num


    if combo_gastnr == None:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 155)]})
        combo_gastnr = htparam.finteger

        if combo_gastnr > 0:

            guest = get_cache (Guest, {"gastnr": [(eq, combo_gastnr)]})

            if not guest:
                combo_gastnr = 0
            else:
                combo_ledger = guest.zahlungsart

            if combo_ledger > 0:

                artikel = get_cache (Artikel, {"artnr": [(eq, combo_ledger)],"departement": [(eq, 0)],"artart": [(eq, 2)]})

                if not artikel:
                    combo_gastnr = 0
                    combo_ledger = 0


            else:
                combo_gastnr = 0
        else:
            combo_gastnr = 0

    if combo_gastnr > 0:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 339)]})
        combo_pf_file1 = htparam.fchar

        htparam = get_cache (Htparam, {"paramnr": [(eq, 340)]})
        combo_pf_file2 = htparam.fchar

        htparam = get_cache (Htparam, {"paramnr": [(eq, 343)]})
        combo_gl_link = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1012)]})

    if htparam.paramgruppe == 38 and htparam.feldtyp == 1 and htparam.finteger > 0:
        f_int = htparam.finteger
    check_dept()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1003)]})
    last_acctdate = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 597)]})
    acct_date = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 558)]})
    last_acct_period = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 795)]})
    close_year = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
    price_decimal = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 112)]})

    art2 = db_session.query(Art2).filter(
             (Art2.artnr == htparam.finteger) & (Art2.departement == 0) & (Art2.artart == 6) & not_ (Art2.pricetab)).first()

    if not art2:
        msg_str = msg_str + chr_unicode(2) + translateExtended ("Local Cash Article not defined! (Param 112 / Grp 5).", lvcarea, "")

        return generate_output()

    gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, art2.fibukonto)]})

    if not gl_acct:
        msg_str = msg_str + chr_unicode(2) + translateExtended ("AcctNo of Cash Article", lvcarea, "") + " " + to_string(art2.artnr) + " " + translateExtended ("not defined.", lvcarea, "")

        return generate_output()
    cash_fibu = gl_acct.fibukonto
    tmpdate = last_acctdate + timedelta(days=1)

    if tmpdate <= last_acct_period:
        msg_str = msg_str + chr_unicode(2) + translateExtended ("Last FO transfer to GL (Param 1003) lower THEN last accounting closing period (Param 558).", lvcarea, "") + chr_unicode(10) + translateExtended ("Transfer to GL not possible.", lvcarea, "")

        return generate_output()

    return generate_output()