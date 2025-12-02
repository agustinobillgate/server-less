#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Billjournal, Umsatz

s_list_data, S_list = create_model("S_list", {"wahrnr":int, "dept":int, "artnr":int, "bezeich":string, "zinr":string, "anzahl":int, "preis":Decimal, "we_buy":Decimal, "we_sell":Decimal, "betrag":Decimal})

def money_exchg_create_journalbl(s_list_data:[S_list], room:string, user_init:string, print_flag:bool):

    prepare_cache ([Htparam, Billjournal, Umsatz])

    fl_code = 0
    char_455 = ""
    i:int = 0
    bill_date:date = None
    htparam = billjournal = umsatz = None

    s_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal fl_code, char_455, i, bill_date, htparam, billjournal, umsatz
        nonlocal room, user_init, print_flag


        nonlocal s_list

        return {"fl_code": fl_code, "char_455": char_455}

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    bill_date = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 253)]})

    if htparam.flogical:
        bill_date = bill_date + timedelta(days=1)

    for s_list in query(s_list_data):
        billjournal = Billjournal()
        db_session.add(billjournal)

        billjournal.rechnr = 0
        billjournal.artnr = s_list.artnr
        billjournal.anzahl = 1
        billjournal.fremdwaehrng = to_decimal(s_list.preis)
        billjournal.betrag = to_decimal(s_list.betrag)
        billjournal.bezeich = s_list.bezeich
        billjournal.zinr = room
        billjournal.departement = 0
        billjournal.zeit = get_current_time_in_seconds() + i
        billjournal.userinit = user_init
        billjournal.bill_datum = bill_date
        billjournal.waehrungsnr = s_list.wahrnr

        i = i + 1

        umsatz = db_session.query(Umsatz).filter(
            Umsatz.artnr == s_list.artnr,
            Umsatz.departement == 0,
            Umsatz.datum == bill_date
        ).with_for_update().first()

        if not umsatz:
            umsatz = Umsatz()
            db_session.add(umsatz)

            umsatz.artnr = s_list.artnr
            umsatz.datum = bill_date
            umsatz.departement = 0

        umsatz.betrag = to_decimal(umsatz.betrag) + to_decimal(s_list.betrag)
        umsatz.anzahl = umsatz.anzahl + 1

    if print_flag:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 455)]})

        if htparam and htparam.fchar != "":
            fl_code = 1
            char_455 = htparam.fchar
        else:
            fl_code = 2

    return generate_output()