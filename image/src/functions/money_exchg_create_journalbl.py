from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam, Billjournal, Umsatz

def money_exchg_create_journalbl(s_list:[S_list], room:str, user_init:str, print_flag:bool):
    fl_code = 0
    char_455 = ""
    i:int = 0
    bill_date:date = None
    htparam = billjournal = umsatz = None

    s_list = None

    s_list_list, S_list = create_model("S_list", {"wahrnr":int, "dept":int, "artnr":int, "bezeich":str, "zinr":str, "anzahl":int, "preis":decimal, "we_buy":decimal, "we_sell":decimal, "betrag":decimal})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal fl_code, char_455, i, bill_date, htparam, billjournal, umsatz


        nonlocal s_list
        nonlocal s_list_list
        return {"fl_code": fl_code, "char_455": char_455}

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 110)).first()
    bill_date = htparam.fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 253)).first()

    if htparam.flogical:
        bill_date = bill_date + 1

    for s_list in query(s_list_list):
        billjournal = Billjournal()
        db_session.add(billjournal)

        billjournal.rechnr = 0
        billjournal.artnr = s_list.artnr
        billjournal.anzahl = 1
        billjournal.fremdwaehrng = s_list.preis
        billjournal.betrag = s_list.betrag
        billjournal.bezeich = s_list.bezeich
        billjournal.zinr = room
        billjournal.departement = 0
        billjournal.zeit = get_current_time_in_seconds() + i
        billjournal.userinit = user_init
        billjournal.bill_datum = bill_date
        billjournal.waehrungsnr = s_list.wahrnr

        billjournal = db_session.query(Billjournal).first()
        i = i + 1

        umsatz = db_session.query(Umsatz).filter(
                (Umsatz.artnr == s_list.artnr) &  (Umsatz.departement == 0) &  (Umsatz.datum == bill_date)).first()

        if not umsatz:
            umsatz = Umsatz()
            db_session.add(umsatz)

            umsatz.artnr = s_list.artnr
            umsatz.datum = bill_date
            umsatz.departement = 0


        umsatz.betrag = umsatz.betrag + s_list.betrag
        umsatz.anzahl = umsatz.anzahl + 1

        umsatz = db_session.query(Umsatz).first()

    if print_flag:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 455)).first()

        if htparam and htparam.fchar != "":
            fl_code = 1
            char_455 = htparam.fchar


        else:
            fl_code = 2

    return generate_output()