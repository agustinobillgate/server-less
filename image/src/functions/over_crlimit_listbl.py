from functions.additional_functions import *
import decimal
from datetime import date
from models import H_artikel, Htparam, Waehrung, Hoteldpt, H_compli, H_bill, H_journal, Queasy, Exrate

def over_crlimit_listbl(from_date:date, to_date:date, from_dept:int, to_dept:int, from_art:int, to_art:int):
    out_list_list = []
    foreign_nr:int = 0
    h_artikel = htparam = waehrung = hoteldpt = h_compli = h_bill = h_journal = queasy = exrate = None

    c_list = output_list = out_list = h_art = None

    c_list_list, C_list = create_model("C_list", {"name":str, "rechnr":int, "p_artnr":int, "datum":date, "dept":int, "betrag":decimal, "f_betrag":decimal})
    output_list_list, Output_list = create_model("Output_list", {"guest_name":str, "artnr":int, "art_desc":str, "card_no":str, "credit_limit":decimal, "amount":decimal, "balanced":decimal})
    out_list_list, Out_list = create_model_like(Output_list)

    H_art = H_artikel

    db_session = local_storage.db_session

    def generate_output():
        nonlocal out_list_list, foreign_nr, h_artikel, htparam, waehrung, hoteldpt, h_compli, h_bill, h_journal, queasy, exrate
        nonlocal h_art


        nonlocal c_list, output_list, out_list, h_art
        nonlocal c_list_list, output_list_list, out_list_list
        return {"out-list": out_list_list}

    def create_list():

        nonlocal out_list_list, foreign_nr, h_artikel, htparam, waehrung, hoteldpt, h_compli, h_bill, h_journal, queasy, exrate
        nonlocal h_art


        nonlocal c_list, output_list, out_list, h_art
        nonlocal c_list_list, output_list_list, out_list_list

        f_endkum:int = 0
        b_endkum:int = 0
        rate:decimal = 1
        exchg_rate:decimal = 1
        curr_datum:date = None
        double_currency:bool = False
        H_art = H_artikel

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 240)).first()

        if htparam.flogical:
            double_currency = True

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 144)).first()

        if htparam.fchar != "":

            waehrung = db_session.query(Waehrung).filter(
                    (Waehrung.wabkurz == htparam.fchar)).first()

            if waehrung:
                exchg_rate = waehrung.ankauf / waehrung.einheit
                foreign_nr = waehrungsnr
            else:
                exchg_rate = 1

        for hoteldpt in db_session.query(Hoteldpt).filter(
                (Hoteldpt.num >= from_dept) &  (Hoteldpt.num <= to_dept)).all():

            h_compli_obj_list = []
            for h_compli, h_art in db_session.query(H_compli, H_art).join(H_art,(H_art.departement == H_compli.departement) &  (H_art.artnr == H_compli.p_artnr) &  (H_art.artart == 11)).filter(
                    (H_compli.datum >= from_date) &  (H_compli.datum <= to_date) &  (H_compli.departement == hoteldpt.num) &  (H_compli.betriebsnr == 0)).all():
                if h_compli._recid in h_compli_obj_list:
                    continue
                else:
                    h_compli_obj_list.append(h_compli._recid)

                if double_currency and curr_datum != h_compli.datum:
                    curr_datum = h_compli.datum
                    find_exrate(curr_datum)

                    if exrate:
                        rate = exrate.betrag
                    else:
                        rate = exchg_rate

                c_list = query(c_list_list, filters=(lambda c_list :c_list.datum == h_compli.datum and c_list.dept == h_compli.departement and c_list.rechnr == h_compli.rechnr and c_list.p_artnr == h_compli.p_artnr), first=True)

                if not c_list:
                    c_list = C_list()
                    c_list_list.append(c_list)

                    c_list.datum = h_compli.datum
                    c_list.dept = h_compli.departement
                    c_list.rechnr = h_compli.rechnr
                    c_list.p_artnr = h_compli.p_artnr

                    h_bill = db_session.query(H_bill).filter(
                            (H_bill.rechnr == h_compli.rechnr) &  (H_bill.departement == h_compli.departement)).first()

                    if h_bill:
                        c_list.name = h_bill.bilname
                    else:

                        h_journal = db_session.query(H_journal).filter(
                                (H_journal.bill_datum == h_compli.datum) &  (H_journal.departement == h_compli.departement) &  (H_journal.segmentcode == h_compli.p_artnr) &  (H_journal.zeit >= 0)).first()

                        if h_journal and h_journal.aendertext != "":
                            c_list.name = h_journal.aendertext
                c_list.betrag = c_list.betrag + h_compli.anzahl * h_compli.epreis * rate

        for c_list in query(c_list_list):

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 105) &  (Queasy.char1 == c_list.name)).first()

            if queasy:

                output_list = query(output_list_list, filters=(lambda output_list :output_list.guest_name == c_list.name), first=True)

                if not output_list:
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.guest_name = c_list.name
                    output_list.credit_limit = queasy.deci3
                    output_list.artnr = queasy.number3
                    output_list.card_no = queasy.char2

                    h_artikel = db_session.query(H_artikel).filter(
                            (H_artikel.departement == c_list.dept) &  (H_artikel.artnr == queasy.number3)).first()

                    if h_artikel:
                        output_list.art_desc = h_artikel.bezeich


                output_list.amount = output_list.amount + c_list.betrag
                output_list.balanced = output_list.amount - queasy.deci3

        for output_list in query(output_list_list, filters=(lambda output_list :output_list.artnr >= from_art and output_list.artnr <= to_art and output_list.balanced >= 0)):
            out_list = Out_list()
            out_list_list.append(out_list)

            buffer_copy(output_list, out_list)

    def find_exrate(curr_date:date):

        nonlocal out_list_list, foreign_nr, h_artikel, htparam, waehrung, hoteldpt, h_compli, h_bill, h_journal, queasy, exrate
        nonlocal h_art


        nonlocal c_list, output_list, out_list, h_art
        nonlocal c_list_list, output_list_list, out_list_list

        if foreign_nr != 0:

            exrate = db_session.query(Exrate).filter(
                    (Exrate.artnr == foreign_nr) &  (Exrate.datum == curr_date)).first()
        else:

            exrate = db_session.query(Exrate).filter(
                    (Exrate.datum == curr_date)).first()


    create_list()

    return generate_output()