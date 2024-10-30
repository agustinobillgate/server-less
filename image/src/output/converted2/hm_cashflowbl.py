from functions.additional_functions import *
import decimal
from datetime import date
from models import Gl_jouhdr, Htparam, Gl_acct, Gl_journal, Queasy

def hm_cashflowbl(pvilanguage:int, to_date:date):
    output_list_list = []
    from_date:date = None
    currency:str = ""
    gl_jouhdr = htparam = gl_acct = gl_journal = queasy = None

    output_list = b_jouhdr = None

    output_list_list, Output_list = create_model("Output_list", {"coa":str, "post_date":date, "liq_item":str, "trans_curr":str, "amt_trans":decimal, "trd_partner":str, "debit":decimal, "credit":decimal, "bezeich":str, "cf_bezeich":str, "cashflow_code":str})

    B_jouhdr = create_buffer("B_jouhdr",Gl_jouhdr)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_list, from_date, currency, gl_jouhdr, htparam, gl_acct, gl_journal, queasy
        nonlocal pvilanguage, to_date
        nonlocal b_jouhdr


        nonlocal output_list, b_jouhdr
        nonlocal output_list_list

        return {"output-list": output_list_list}

    def create_list():

        nonlocal output_list_list, from_date, currency, gl_jouhdr, htparam, gl_acct, gl_journal, queasy
        nonlocal pvilanguage, to_date
        nonlocal b_jouhdr


        nonlocal output_list, b_jouhdr
        nonlocal output_list_list

        c:str = ""
        cashflow_code:str = ""
        amount:decimal = to_decimal("0.0")
        post_date:date = None
        coa:str = ""
        liq_item:str = ""
        trd_partner:str = ""

        gl_journal_obj_list = []
        for gl_journal, gl_acct, gl_jouhdr in db_session.query(Gl_journal, Gl_acct, Gl_jouhdr).join(Gl_acct,(Gl_acct.fibukonto == Gl_journal.fibukonto)).join(Gl_jouhdr,(Gl_jouhdr.jnr == Gl_journal.jnr) & (Gl_jouhdr.datum >= from_date) & (Gl_jouhdr.datum <= to_date)).order_by(Gl_jouhdr.datum, Gl_journal.fibukonto).all():
            if gl_journal._recid in gl_journal_obj_list:
                continue
            else:
                gl_journal_obj_list.append(gl_journal._recid)

            if num_entries(gl_journal.bemerk, chr(2)) >= 2:

                if entry(1, gl_journal.bemerk, chr(2)) != "":

                    output_list = query(output_list_list, filters=(lambda output_list: output_list.coa == gl_journal.fibukonto and output_list.post_date == gl_jouhdr.datum and output_list.cashflow_code == entry(1, gl_journal.bemerk, chr(2))), first=True)

                    if not output_list:
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        cashflow_code = entry(1, gl_journal.bemerk, chr(2))
                        output_list.cashflow_code = entry(1, gl_journal.bemerk, chr(2))
                        output_list.coa = gl_acct.fibukonto
                        output_list.post_date = gl_jouhdr.datum
                        output_list.trans_curr = currency
                        output_list.liq_item = substring(cashflow_code, 0, 6)
                        output_list.bezeich = to_string(entry(0, gl_journal.bemerk, chr(2)) , "x(50)")
                        output_list.amt_trans = to_decimal(round(gl_journal.debit - gl_journal.credit , 0))


                        pass

                        if substring(cashflow_code, 6, 4) == ("0000").lower() :
                            trd_partner = " "
                        else:
                            trd_partner = substring(cashflow_code, 6, 4)
                        output_list.trd_partner = trd_partner

                        queasy = db_session.query(Queasy).filter(
                                 (Queasy.key == 177) & (Queasy.deci1 == to_decimal(cashflow_code))).first()

                        if queasy:
                            output_list.cf_bezeich = queasy.char1
                    else:
                        output_list.amt_trans = to_decimal(output_list.amt_trans + round(gl_journal.debit - gl_journal.credit , 0))


    def convert_fibu(konto:str):

        nonlocal output_list_list, from_date, currency, gl_jouhdr, htparam, gl_acct, gl_journal, queasy
        nonlocal pvilanguage, to_date
        nonlocal b_jouhdr


        nonlocal output_list, b_jouhdr
        nonlocal output_list_list

        s = ""
        ch:str = ""
        i:int = 0
        j:int = 0

        def generate_inner_output():
            return (s)


        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 977)).first()
        ch = htparam.fchar
        j = 0
        for i in range(1,len(ch)  + 1) :

            if substring(ch, i - 1, 1) >= ("0").lower()  and substring(ch, i - 1, 1) <= ("9").lower() :
                j = j + 1
                s = s + substring(konto, j - 1, 1)
            else:
                s = s + substring(ch, i - 1, 1)

        return generate_inner_output()


    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 152)).first()

    if htparam:

        if htparam.fchar.lower()  == ("RP").lower() :
            currency = "IDR"

        elif htparam.fchar.lower()  == ("US$").lower() :
            currency = "USD"


        else:
            currency = htparam.fchar


    from_date = date_mdy(get_month(to_date) , 1, get_year(to_date))


    create_list()

    return generate_output()