#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import H_artikel, Htparam, Waehrung, Hoteldpt, H_compli, H_bill, H_journal, Queasy, H_bill_line, Exrate

def over_crlimit_listbl(from_date:date, to_date:date, from_dept:int, to_dept:int, from_art:int, to_art:int):

    prepare_cache ([H_artikel, Htparam, Waehrung, Hoteldpt, H_compli, H_bill, H_journal, Queasy, H_bill_line, Exrate])

    out_list_data = []
    foreign_nr:int = 0
    h_artikel = htparam = waehrung = hoteldpt = h_compli = h_bill = h_journal = queasy = h_bill_line = exrate = None

    c_list = output_list = out_list = None

    c_list_data, C_list = create_model("C_list", {"name":string, "rechnr":int, "p_artnr":int, "datum":date, "dept":int, "betrag":Decimal, "f_betrag":Decimal})
    output_list_data, Output_list = create_model("Output_list", {"guest_name":string, "artnr":int, "art_desc":string, "card_no":string, "credit_limit":Decimal, "amount":Decimal, "balanced":Decimal})
    out_list_data, Out_list = create_model("Out_list", {"guest_name":string, "artnr":int, "art_desc":string, "card_no":string, "credit_limit":Decimal, "amount":Decimal, "balanced":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal out_list_data, foreign_nr, h_artikel, htparam, waehrung, hoteldpt, h_compli, h_bill, h_journal, queasy, h_bill_line, exrate
        nonlocal from_date, to_date, from_dept, to_dept, from_art, to_art


        nonlocal c_list, output_list, out_list
        nonlocal c_list_data, output_list_data, out_list_data

        return {"out-list": out_list_data}

    def handle_null_char(inp_char:string):

        nonlocal out_list_data, foreign_nr, h_artikel, htparam, waehrung, hoteldpt, h_compli, h_bill, h_journal, queasy, h_bill_line, exrate
        nonlocal from_date, to_date, from_dept, to_dept, from_art, to_art


        nonlocal c_list, output_list, out_list
        nonlocal c_list_data, output_list_data, out_list_data

        if inp_char == None:
            return ""
        else:
            return inp_char


    def create_list():

        nonlocal out_list_data, foreign_nr, h_artikel, htparam, waehrung, hoteldpt, h_compli, h_bill, h_journal, queasy, h_bill_line, exrate
        nonlocal from_date, to_date, from_dept, to_dept, from_art, to_art


        nonlocal c_list, output_list, out_list
        nonlocal c_list_data, output_list_data, out_list_data

        f_endkum:int = 0
        b_endkum:int = 0
        rate:Decimal = 1
        exchg_rate:Decimal = 1
        curr_datum:date = None
        double_currency:bool = False
        bezeich:string = ""
        h_art = None
        H_art =  create_buffer("H_art",H_artikel)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 240)]})

        if htparam.flogical:
            double_currency = True

        htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})

        if htparam.fchar != "":

            waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

            if waehrung:
                exchg_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
                foreign_nr = waehrung.waehrungsnr
            else:
                exchg_rate =  to_decimal("1")

        for hoteldpt in db_session.query(Hoteldpt).filter(
                 (Hoteldpt.num >= from_dept) & (Hoteldpt.num <= to_dept)).order_by(Hoteldpt._recid).all():

            h_compli_obj_list = {}
            h_compli = H_compli()
            h_art = H_artikel()
            for h_compli.datum, h_compli.departement, h_compli.rechnr, h_compli.p_artnr, h_compli.anzahl, h_compli.epreis, h_compli._recid, h_art.bezeich, h_art._recid in db_session.query(H_compli.datum, H_compli.departement, H_compli.rechnr, H_compli.p_artnr, H_compli.anzahl, H_compli.epreis, H_compli._recid, H_art.bezeich, H_art._recid).join(H_art,(H_art.departement == H_compli.departement) & (H_art.artnr == H_compli.p_artnr) & (H_art.artart == 11)).filter(
                     (H_compli.datum >= from_date) & (H_compli.datum <= to_date) & (H_compli.departement == hoteldpt.num) & (H_compli.betriebsnr == 0)).order_by(H_compli.rechnr).all():
                if h_compli_obj_list.get(h_compli._recid):
                    continue
                else:
                    h_compli_obj_list[h_compli._recid] = True

                if double_currency and curr_datum != h_compli.datum:
                    curr_datum = h_compli.datum
                    find_exrate(curr_datum)

                    if exrate:
                        rate =  to_decimal(exrate.betrag)
                    else:
                        rate =  to_decimal(exchg_rate)

                c_list = query(c_list_data, filters=(lambda c_list: c_list.datum == h_compli.datum and c_list.dept == h_compli.departement and c_list.rechnr == h_compli.rechnr and c_list.p_artnr == h_compli.p_artnr), first=True)

                if not c_list:
                    c_list = C_list()
                    c_list_data.append(c_list)

                    c_list.datum = h_compli.datum
                    c_list.dept = h_compli.departement
                    c_list.rechnr = h_compli.rechnr
                    c_list.p_artnr = h_compli.p_artnr

                    h_bill = get_cache (H_bill, {"rechnr": [(eq, h_compli.rechnr)],"departement": [(eq, h_compli.departement)]})

                    if h_bill:
                        c_list.name = handle_null_char (h_bill.bilname)
                    else:

                        h_journal = get_cache (H_journal, {"bill_datum": [(eq, h_compli.datum)],"departement": [(eq, h_compli.departement)],"segmentcode": [(eq, h_compli.p_artnr)],"zeit": [(ge, 0)]})

                        if h_journal and h_journal.aendertext != "":
                            c_list.name = handle_null_char (h_journal.aendertext)
                c_list.betrag =  to_decimal(c_list.betrag) + to_decimal(h_compli.anzahl) * to_decimal(h_compli.epreis) * to_decimal(rate)

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 105)).order_by(Queasy._recid).all():
            bezeich = queasy.char1 + " - " + to_string(get_month(to_date) , "99") + "/" + to_string(get_year(to_date) , "9999")

            output_list = query(output_list_data, filters=(lambda output_list: output_list.guest_name.lower()  == (bezeich).lower()), first=True)

            if not output_list:
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.guest_name = bezeich
                output_list.credit_limit =  to_decimal(queasy.deci3)
                output_list.artnr = queasy.number3
                output_list.card_no = queasy.char2

                h_artikel = get_cache (H_artikel, {"departement": [(eq, 1)],"artnr": [(eq, queasy.number3)]})

                if h_artikel:
                    output_list.art_desc = h_artikel.bezeich


            output_list.amount =  to_decimal("0")
            output_list.balanced =  to_decimal(queasy.deci3) - to_decimal(output_list.amount)

        for c_list in query(c_list_data):

            h_bill_line = get_cache (H_bill_line, {"rechnr": [(eq, c_list.rechnr)],"artnr": [(eq, c_list.p_artnr)]})

            if h_bill_line:

                queasy = get_cache (Queasy, {"key": [(eq, 105)],"char1": [(eq, h_bill_line.bezeich)],"number3": [(eq, h_bill_line.artnr)]})

                if queasy:
                    bezeich = queasy.char1 + " - " + to_string(get_month(c_list.datum) , "99") + "/" + to_string(get_year(c_list.datum) , "9999")

                    output_list = query(output_list_data, filters=(lambda output_list: output_list.guest_name.lower()  == (bezeich).lower()), first=True)

                    if not output_list:
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        output_list.guest_name = bezeich
                        output_list.credit_limit =  to_decimal(queasy.deci3)
                        output_list.artnr = queasy.number3
                        output_list.card_no = queasy.char2

                        h_artikel = get_cache (H_artikel, {"departement": [(eq, 1)],"artnr": [(eq, queasy.number3)]})

                        if h_artikel:
                            output_list.art_desc = h_artikel.bezeich


                    output_list.amount =  to_decimal(output_list.amount) + to_decimal(c_list.betrag)
                    output_list.balanced =  to_decimal(queasy.deci3) - to_decimal(output_list.amount)

        for output_list in query(output_list_data, filters=(lambda output_list: output_list.artnr >= from_art and output_list.artnr <= to_art), sort_by=[("guest_name",False)]):
            out_list = Out_list()
            out_list_data.append(out_list)

            out_list.guest_name = output_list.guest_name
            out_list.artnr = output_list.artnr
            out_list.art_desc = output_list.art_desc
            out_list.card_no = output_list.card_no
            out_list.credit_limit =  to_decimal(output_list.credit_limit)
            out_list.amount =  to_decimal(output_list.amount)
            out_list.balanced =  to_decimal(output_list.balanced)


    def find_exrate(curr_date:date):

        nonlocal out_list_data, foreign_nr, h_artikel, htparam, waehrung, hoteldpt, h_compli, h_bill, h_journal, queasy, h_bill_line, exrate
        nonlocal from_date, to_date, from_dept, to_dept, from_art, to_art


        nonlocal c_list, output_list, out_list
        nonlocal c_list_data, output_list_data, out_list_data

        if foreign_nr != 0:

            exrate = get_cache (Exrate, {"artnr": [(eq, foreign_nr)],"datum": [(eq, curr_date)]})
        else:

            exrate = get_cache (Exrate, {"datum": [(eq, curr_date)]})

    create_list()

    return generate_output()