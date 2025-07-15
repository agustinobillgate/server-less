#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Gl_jouhdr, Htparam, Gl_acct, Gl_journal, Queasy

def hm_cashflowbl(pvilanguage:int, to_date:date):

    prepare_cache ([Gl_jouhdr, Htparam, Gl_acct, Gl_journal, Queasy])

    output_list_data = []
    from_date:date = None
    currency:string = ""
    gl_jouhdr = htparam = gl_acct = gl_journal = queasy = None

    output_list = b_jouhdr = None

    output_list_data, Output_list = create_model("Output_list", {"coa":string, "post_date":date, "liq_item":string, "trans_curr":string, "amt_trans":Decimal, "trd_partner":string, "debit":Decimal, "credit":Decimal, "bezeich":string, "cf_bezeich":string, "cashflow_code":string})

    B_jouhdr = create_buffer("B_jouhdr",Gl_jouhdr)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_data, from_date, currency, gl_jouhdr, htparam, gl_acct, gl_journal, queasy
        nonlocal pvilanguage, to_date
        nonlocal b_jouhdr


        nonlocal output_list, b_jouhdr
        nonlocal output_list_data

        return {"output-list": output_list_data}

    def create_list():

        nonlocal output_list_data, from_date, currency, gl_jouhdr, htparam, gl_acct, gl_journal, queasy
        nonlocal pvilanguage, to_date
        nonlocal b_jouhdr


        nonlocal output_list, b_jouhdr
        nonlocal output_list_data

        c:string = ""
        cashflow_code:string = ""
        amount:Decimal = to_decimal("0.0")
        post_date:date = None
        coa:string = ""
        liq_item:string = ""
        trd_partner:string = ""

        gl_journal_obj_list = {}
        gl_journal = Gl_journal()
        gl_acct = Gl_acct()
        gl_jouhdr = Gl_jouhdr()
        for gl_journal.fibukonto, gl_journal.bemerk, gl_journal.debit, gl_journal.credit, gl_journal._recid, gl_acct.fibukonto, gl_acct._recid, gl_jouhdr.datum, gl_jouhdr._recid in db_session.query(Gl_journal.fibukonto, Gl_journal.bemerk, Gl_journal.debit, Gl_journal.credit, Gl_journal._recid, Gl_acct.fibukonto, Gl_acct._recid, Gl_jouhdr.datum, Gl_jouhdr._recid).join(Gl_acct,(Gl_acct.fibukonto == Gl_journal.fibukonto)).join(Gl_jouhdr,(Gl_jouhdr.jnr == Gl_journal.jnr) & (Gl_jouhdr.datum >= from_date) & (Gl_jouhdr.datum <= to_date)).order_by(Gl_jouhdr.datum, Gl_journal.fibukonto).all():
            if gl_journal_obj_list.get(gl_journal._recid):
                continue
            else:
                gl_journal_obj_list[gl_journal._recid] = True

            if num_entries(gl_journal.bemerk, chr_unicode(2)) >= 2:

                if entry(1, gl_journal.bemerk, chr_unicode(2)) != "":

                    output_list = query(output_list_data, filters=(lambda output_list: output_list.coa == gl_journal.fibukonto and output_list.post_date == gl_jouhdr.datum and output_list.cashflow_code == entry(1, gl_journal.bemerk, chr_unicode(2))), first=True)

                    if not output_list:
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        cashflow_code = entry(1, gl_journal.bemerk, chr_unicode(2))
                        output_list.cashflow_code = entry(1, gl_journal.bemerk, chr_unicode(2))
                        output_list.coa = gl_acct.fibukonto
                        output_list.post_date = gl_jouhdr.datum
                        output_list.trans_curr = currency
                        output_list.liq_item = substring(cashflow_code, 0, 6)
                        output_list.bezeich = to_string(entry(0, gl_journal.bemerk, chr_unicode(2)) , "x(50)")
                        output_list.amt_trans = to_decimal(round(gl_journal.debit - gl_journal.credit , 0))


                        if substring(cashflow_code, 6, 4) == ("0000").lower() :
                            trd_partner = " "
                        else:
                            trd_partner = substring(cashflow_code, 6, 4)
                        output_list.trd_partner = trd_partner

                        queasy = get_cache (Queasy, {"key": [(eq, 177)],"deci1": [(eq, to_decimal(cashflow_code))]})

                        if queasy:
                            output_list.cf_bezeich = queasy.char1
                    else:
                        output_list.amt_trans = to_decimal(output_list.amt_trans + round(gl_journal.debit - gl_journal.credit , 0))


    def convert_fibu(konto:string):

        nonlocal output_list_data, from_date, currency, gl_jouhdr, htparam, gl_acct, gl_journal, queasy
        nonlocal pvilanguage, to_date
        nonlocal b_jouhdr


        nonlocal output_list, b_jouhdr
        nonlocal output_list_data

        s = ""
        ch:string = ""
        i:int = 0
        j:int = 0

        def generate_inner_output():
            return (s)


        htparam = get_cache (Htparam, {"paramnr": [(eq, 977)]})
        ch = htparam.fchar
        j = 0
        for i in range(1,length(ch)  + 1) :

            if substring(ch, i - 1, 1) >= ("0").lower()  and substring(ch, i - 1, 1) <= ("9").lower() :
                j = j + 1
                s = s + substring(konto, j - 1, 1)
            else:
                s = s + substring(ch, i - 1, 1)

        return generate_inner_output()


    htparam = get_cache (Htparam, {"paramnr": [(eq, 152)]})

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