#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 10/10/2025
# fchar -> htparam.
#
#------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Gl_jouhdr, Gl_acct, Gl_journal

def closemonth1bl(pvilanguage:int):

    prepare_cache ([Htparam, Gl_acct, Gl_journal])

    curr_date = None
    msg_str = ""
    curr_closeyr:int = 0
    balance:Decimal = to_decimal("0.0")
    pnl_acct:string = ""
    first_date:date = None
    bom_597:date = None
    end_of_month:date = None
    param269:date = None
    param1003:date = None
    param1014:date = None
    param1035:date = None
    param1118:date = None
    param1123:date = None
    param221:date = None
    param224:date = None
    param988:bool = False
    param996:bool = False
    param1016:bool = False
    param997:bool = False
    lvcarea:string = "closemonth"
    htparam = gl_jouhdr = gl_acct = gl_journal = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal curr_date, msg_str, curr_closeyr, balance, pnl_acct, first_date, bom_597, end_of_month, param269, param1003, param1014, param1035, param1118, param1123, param221, param224, param988, param996, param1016, param997, lvcarea, htparam, gl_jouhdr, gl_acct, gl_journal
        nonlocal pvilanguage

        return {"curr_date": curr_date, "msg_str": msg_str}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 597)]})
    curr_date = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 269)]})
    param269 = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1003)]})
    param1003 = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1014)]})
    param1014 = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1035)]})
    param1035 = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1118)]})
    param1118 = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1123)]})
    param1123 = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 221)]})
    param221 = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 224)]})
    param224 = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 988)]})
    param988 = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 996)]})
    param996 = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1016)]})
    param1016 = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 997)]})
    param997 = htparam.flogical

    if param996:

        if param1003 < curr_date:
            msg_str = msg_str +translateExtended ("Closing month not possible, please check Parameter 1003.", lvcarea, "")

            return generate_output()

    if param1016:

        if param1118 < curr_date:
            msg_str = msg_str +translateExtended ("Closing month not possible, please check Parameter 1118.", lvcarea, "")

            return generate_output()

    if param997:

        if param1014 < curr_date:
            msg_str = msg_str +translateExtended ("Closing month not possible, please check Parameter 1014.", lvcarea, "")

            return generate_output()

    if param988:

        if param269 < curr_date:
            msg_str = msg_str +translateExtended ("Closing month not possible, please check Parameter 269.", lvcarea, "")

            return generate_output()

        elif param1035 < curr_date:
            msg_str = msg_str +translateExtended ("Closing month not possible, please check Parameter 1035.", lvcarea, "")

            return generate_output()

        elif param1123 < curr_date:
            msg_str = msg_str +translateExtended ("Closing month not possible, please check Parameter 1123.", lvcarea, "")

            return generate_output()

        if param221 <= curr_date:
            msg_str = msg_str +translateExtended ("Closing month not possible, inventory has not yet closed.", lvcarea, "") + chr_unicode(10) + translateExtended ("Please check Parameter 221.", lvcarea, "")

            return generate_output()

        elif param224 <= curr_date:
            msg_str = msg_str +translateExtended ("Closing month not possible, inventory has not yet closed.", lvcarea, "") + chr_unicode(10) + translateExtended ("Please check Parameter 224.", lvcarea, "")

            return generate_output()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 558)]})
    first_date = htparam.fdate + timedelta(days=1)

    if htparam.fdate >= curr_date:
        msg_str = msg_str +translateExtended ("Closing date incorrect (Parameter 558).", lvcarea, "")

        return generate_output()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 795)]})
    curr_closeyr = get_year(htparam.fdate) + 1

    if get_year(curr_date) > curr_closeyr:
        msg_str = msg_str +translateExtended ("Closing Year has not been done yet.", lvcarea, "")

        return generate_output()

    gl_jouhdr = db_session.query(Gl_jouhdr).filter(
             (Gl_jouhdr.activeflag == 0) & (Gl_jouhdr.batch) & (Gl_jouhdr.datum <= curr_date)).first()

    if gl_jouhdr:
        msg_str = msg_str +translateExtended ("Batch journal(s) still exists, closing not possible.", lvcarea, "") + chr_unicode(10) + to_string(gl_jouhdr.datum) + " - " + gl_jouhdr.refno

        return generate_output()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 979)]})

    gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, htparam.fchar)]})

    if not gl_acct:
        msg_str = msg_str +translateExtended ("P&L Account not defined (Parameter 979).", lvcarea, "")

        return generate_output()
    pnl_acct = gl_acct.fibukonto

    gl_jouhdr = get_cache (Gl_jouhdr, {"activeflag": [(eq, 1)],"datum": [(ge, first_date),(le, curr_date)]})

    if gl_jouhdr:
        msg_str = msg_str +translateExtended ("Closed Journal found! Re-check it.", lvcarea, "")

        return generate_output()

    gl_jouhdr = get_cache (Gl_jouhdr, {"activeflag": [(eq, 0)],"datum": [(ge, first_date),(le, curr_date)]})
    while None != gl_jouhdr:
        balance =  to_decimal("0")

        for gl_journal in db_session.query(Gl_journal).filter(
                 (Gl_journal.jnr == gl_jouhdr.jnr)).order_by(Gl_journal._recid).all():
            balance =  to_decimal(balance) + to_decimal(gl_journal.debit) - to_decimal(gl_journal.credit)

        if balance > 0 and balance > 0.01 or balance < 0 and balance < (- 0.01):
            msg_str = msg_str + translateExtended ("Not balanced Journals found (closing not possible).", lvcarea, "") + chr_unicode(10) + translateExtended ("Date : ", lvcarea, "") + to_string(gl_jouhdr.datum) + " - " + translateExtended ("RefNo : ", lvcarea, "") + gl_jouhdr.refno

            return generate_output()

        curr_recid = gl_jouhdr._recid
        gl_jouhdr = db_session.query(Gl_jouhdr).filter(
                 (Gl_jouhdr.activeflag == 0) & (Gl_jouhdr.datum >= first_date) & (Gl_jouhdr.datum <= curr_date) & (Gl_jouhdr._recid > curr_recid)).first()

    return generate_output()