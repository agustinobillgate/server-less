# using conversion tools version: 1.0.0.119
"""_yusufwijasena_12/11/2025

    Ticket ID: F6D79E
        _remark_:   - update DZIKRI: 1A82C7
                    - fix python indentation
"""
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, H_journal, H_artikel, Hoteldpt, H_bill, Res_line, Guest


def rest_billjourn_journal_listbl(from_art: int, from_dept: int, to_dept: int, from_date: date, to_date: date, price_decimal: int):

    prepare_cache([Htparam, H_journal, H_artikel, Hoteldpt, H_bill, Res_line, Guest])

    output_list_data = []
    disc_art1: int = 0
    disc_art2: int = 0
    disc_art3: int = 0
    htparam = h_journal = h_artikel = hoteldpt = h_bill = res_line = guest = None

    output_list = None

    output_list_data, Output_list = create_model(
        "Output_list",
        {
            "str": str,
            "gname": str,
            "st_optable": str,
            "ct_optable": str
        })

    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_data, disc_art1, disc_art2, disc_art3, htparam, h_journal, h_artikel, hoteldpt, h_bill, res_line, guest
        nonlocal from_art, from_dept, to_dept, from_date, to_date, price_decimal
        nonlocal output_list
        nonlocal output_list_data

        return {
            "output-list": output_list_data
        }

    def journal_list():
        nonlocal output_list_data, disc_art1, disc_art2, disc_art3, htparam, h_journal, h_artikel, hoteldpt, h_bill, res_line, guest
        nonlocal from_art, from_dept, to_dept, from_date, to_date, price_decimal
        nonlocal output_list
        nonlocal output_list_data

        qty: int = 0
        sub_tot = to_decimal("0.0")
        tot = to_decimal("0.0")
        sub_tot1 = to_decimal("0.0")
        tot1 = to_decimal("0.0")
        curr_date: date = None
        last_dept: int = -1
        it_exist: bool = False
        curr_guest = ""
        curr_room = ""
        bill_datum: date = None
        # start - DZIKRI: 1A82C7
        dqty: int = 0
        dsub_tot = to_decimal("0.0")
        dsub_tot1 = to_decimal("0.0")
        # end - DZIKRI: 1A82C7
        gqty: int = 0
        gsub_tot = to_decimal("0.0")
        gsub_tot1 = to_decimal("0.0")
        bill_no: int = 0
        dept_no: int = 0
        curr_time = ""
        curr_time_pay = ""
        count_i: int = 0
        pay_exist: bool = False
        buf_hjournal = None
        buf_hart = None
        Buf_hjournal = create_buffer("Buf_hjournal", H_journal)
        Buf_hart = create_buffer("Buf_hart", H_artikel)
        output_list_data.clear()

        if from_art == 0:
            # start - DZIKRI: 1A82C7
            for hoteldpt in db_session.query(Hoteldpt).filter(
                    (Hoteldpt.num >= from_dept) & (Hoteldpt.num <= to_dept)).order_by(Hoteldpt.num).all():
                sub_tot = to_decimal("0")
                sub_tot1 = to_decimal("0")
                it_exist = False
                qty = 0
                bill_no = 0
                dept_no = hoteldpt.num
                curr_time = ""
                curr_time_pay = ""
                count_i = 0
                dqty = 0
                dsub_tot = to_decimal("0")
                dsub_tot1 = to_decimal("0")
                for curr_date in date_range(from_date, to_date):
                    for h_journal in db_session.query(H_journal).filter(
                            (H_journal.bill_datum == curr_date) & (H_journal.departement == hoteldpt.num)).order_by(H_journal.rechnr, H_journal.sysdate, H_journal.zeit).all():
                        h_artikel = get_cache(
                            H_artikel, {"artnr": [(eq, h_journal.artnr)], "departement": [(eq, h_journal.departement)]})
                        it_exist = True
                        curr_guest = ""
                        curr_room = ""
                        pay_exist = False

                        h_bill = get_cache(
                            H_bill, {"rechnr": [(eq, h_journal.rechnr)], "departement": [(eq, h_journal.departement)]})

                        if h_bill:
                            if h_bill.resnr > 0 and h_bill.reslinnr > 0:
                                res_line = get_cache(
                                    Res_line, {"resnr": [(eq, h_bill.resnr)], "reslinnr": [(eq, h_bill.reslinnr)]})

                                if res_line:
                                    curr_guest = res_line.name
                                    curr_room = res_line.zinr

                            elif h_bill.resnr > 0:
                                guest = get_cache(
                                    Guest, {"gastnr": [(eq, h_bill.resnr)]})

                                if guest:
                                    curr_guest = guest.name + "," + guest.vorname1
                                    curr_room = ""

                            elif h_bill.resnr == 0:
                                curr_guest = h_bill.bilname
                                curr_room = ""

                        if (h_journal.artnr == disc_art1 or h_journal.artnr == disc_art2 or h_journal.artnr == disc_art2) and h_journal.betrag == 0:
                            pass
                        else:
                            if bill_datum == None or bill_datum >= h_journal.bill_datum:
                                bill_datum = h_journal.bill_datum

                            if bill_datum == h_journal.bill_datum:
                                output_list = Output_list()
                                output_list_data.append(output_list)

                                output_list.gname = curr_guest
                                str = to_string(h_journal.bill_datum) + \
                                    to_string(h_journal.tischnr, ">>>>>9") + \
                                    to_string(h_journal.rechnr, "9,999,999") + \
                                    to_string(h_journal.artnr, ">>>>>>>>>>") + \
                                    to_string(h_journal.bezeich, "x(24)") + \
                                    to_string(hoteldpt.depart, "x(12)") + \
                                    to_string(h_journal.anzahl, "->>>>>9")

                                if h_artikel and h_artikel.artart == 0:
                                    if price_decimal == 2:
                                        str = str + \
                                            to_string(h_journal.betrag, "->>,>>>,>>>,>>9.99") + \
                                            to_string(0, "->>,>>>,>>>,>>9.99")
                                    else:
                                        str = str + \
                                            to_string(h_journal.betrag, "->,>>>,>>>,>>>,>>9") + \
                                            to_string(0, "->,>>>,>>>,>>>,>>9")

                                    if bill_no != h_journal.rechnr and dept_no == h_journal.departement and h_journal.anzahl > 0:
                                        count_i = 0
                                        curr_time = to_string(
                                            h_journal.zeit, "HH:MM:SS")
                                    else:
                                        count_i = 0

                                        for buf_hjournal in db_session.query(Buf_hjournal).filter(
                                                (Buf_hjournal.rechnr == h_journal.rechnr) & (Buf_hjournal.departement == h_journal.departement) & (Buf_hjournal.bill_datum == h_journal.bill_datum) & (Buf_hjournal.anzahl > 0) & (Buf_hjournal.betrag < 0)).order_by(Buf_hjournal.zeit.desc()).all():
                                            pay_exist = True
                                            break

                                        if not pay_exist:
                                            output_list.ct_optable = to_string(
                                                h_journal.zeit, "HH:MM:SS")

                                    if (h_journal.anzahl > 0) or (h_journal.anzahl < 0 and pay_exist):
                                        output_list.st_optable = curr_time
                                    sub_tot = to_decimal(
                                        sub_tot) + to_decimal(h_journal.betrag)
                                    tot = to_decimal(
                                        tot) + to_decimal(h_journal.betrag)
                                    gsub_tot = to_decimal(
                                        gsub_tot) + to_decimal(h_journal.betrag)
                                    dsub_tot = to_decimal(
                                        dsub_tot) + to_decimal(h_journal.betrag)

                                elif h_journal.artnr == 0 and substring(h_journal.bezeich, 0, 9) == "To Table ":
                                    if price_decimal == 2:
                                        str = str + \
                                            to_string(h_journal.betrag, "->>,>>>,>>>,>>9.99") + \
                                            to_string(0, "->>,>>>,>>>,>>9.99")
                                    else:
                                        str = str + \
                                            to_string(h_journal.betrag, "->,>>>,>>>,>>>,>>9") + \
                                            to_string(0, "->,>>>,>>>,>>>,>>9")
                                    sub_tot = to_decimal(
                                        sub_tot) + to_decimal(h_journal.betrag)
                                    tot = to_decimal(
                                        tot) + to_decimal(h_journal.betrag)
                                    gsub_tot = to_decimal(
                                        gsub_tot) + to_decimal(h_journal.betrag)
                                    dsub_tot = to_decimal(
                                        dsub_tot) + to_decimal(h_journal.betrag)

                                elif h_journal.artnr == 0 and substring(h_journal.bezeich, 0, 11) == "From Table ":
                                    if price_decimal == 2:
                                        str = str + \
                                            to_string(h_journal.betrag, "->>,>>>,>>>,>>9.99") + \
                                            to_string(0, "->>,>>>,>>>,>>9.99")
                                    else:
                                        str = str + \
                                            to_string(h_journal.betrag, "->,>>>,>>>,>>>,>>9") + \
                                            to_string(0, "->,>>>,>>>,>>>,>>9")
                                    sub_tot = to_decimal(
                                        sub_tot) + to_decimal(h_journal.betrag)
                                    tot = to_decimal(
                                        tot) + to_decimal(h_journal.betrag)
                                    gsub_tot = to_decimal(
                                        gsub_tot) + to_decimal(h_journal.betrag)
                                    dsub_tot = to_decimal(
                                        dsub_tot) + to_decimal(h_journal.betrag)
                                else:
                                    if price_decimal == 2:
                                        str = str + \
                                            to_string(0, "->>,>>>,>>>,>>9.99") + \
                                            to_string(h_journal.betrag, "->>,>>>,>>>,>>9.99")
                                    else:
                                        str = str + \
                                            to_string(0, "->,>>>,>>>,>>>,>>9") + \
                                            to_string(h_journal.betrag, "->,>>>,>>>,>>>,>>9")
                                    sub_tot1 = to_decimal(
                                        sub_tot1) + to_decimal(h_journal.betrag)
                                    tot1 = to_decimal(
                                        tot1) + to_decimal(h_journal.betrag)
                                    gsub_tot1 = to_decimal(
                                        gsub_tot1) + to_decimal(h_journal.betrag)
                                    dsub_tot1 = to_decimal(
                                        dsub_tot1) + to_decimal(h_journal.betrag)
                                    
                                    count_i = count_i + 1
                                    if count_i == 1:
                                        for buf_hjournal in db_session.query(Buf_hjournal).filter(
                                                (Buf_hjournal.rechnr == h_journal.rechnr) & 
                                                (Buf_hjournal.departement == h_journal.departement) & 
                                                (Buf_hjournal.bill_datum == h_journal.bill_datum) & 
                                                (Buf_hjournal.anzahl > 0) & 
                                                (Buf_hjournal.betrag < 0)).order_by(Buf_hjournal.zeit.desc()).all():
                                            curr_time_pay = to_string(
                                                buf_hjournal.zeit, "HH:MM:SS")
                                            break
                                    output_list.ct_optable = curr_time_pay
                                str = str + \
                                    to_string(h_journal.kellner_nr, "999") + \
                                    to_string(h_journal.zeit, "HH:MM:SS") + curr_room
                                qty = qty + h_journal.anzahl
                                gqty = gqty + h_journal.anzahl
                                dqty = dqty + h_journal.anzahl
                                bill_no = h_journal.rechnr
                            else:
                                output_list = Output_list()
                                output_list_data.append(output_list)

                                if price_decimal == 2:
                                    str = to_string("", "x(33)") + \
                                        to_string("T O T A L ", "x(24)") + \
                                        to_string(" ", "x(12)") + \
                                        to_string(qty, "->>>>>9")

                                    if sub_tot < -99999999 or sub_tot > 999999999:
                                        str = str + to_string(sub_tot, "->>,>>>,>>>,>>9.99")
                                    else:
                                        str = str + to_string(sub_tot, "->>,>>>,>>>,>>9.99")

                                    if sub_tot1 < -99999999 or sub_tot1 > 999999999:
                                        str = str + to_string(sub_tot1, "->>,>>>,>>>,>>9.99")
                                    else:
                                        str = str + to_string(sub_tot1, "->>,>>>,>>>,>>9.99")
                                else:
                                    str = to_string("", "x(33)") + \
                                        to_string("T O T A L ", "x(24)") + \
                                        to_string(" ", "x(12)") + \
                                        to_string(qty, "->>>>>9") + \
                                        to_string(sub_tot, "->,>>>,>>>,>>>,>>9") + \
                                        to_string(sub_tot1, "->,>>>,>>>,>>>,>>9")
                                qty = 0
                                sub_tot = to_decimal("0")
                                sub_tot1 = to_decimal("0")
                                bill_datum = h_journal.bill_datum
                # end - DZIKRI: 1A82C7
                
                if qty > 0 and it_exist and from_date != to_date:
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    if price_decimal == 2:
                        str = to_string("", "x(33)") + \
                            to_string("T O T A L ", "x(24)") + \
                            to_string(" ", "x(12)") + \
                            to_string(qty, "->>>>>9")

                        if sub_tot < -99999999 or sub_tot > 999999999:
                            str = str + \
                                to_string(sub_tot, "->>,>>>,>>>,>>9.99")
                        else:
                            str = str + \
                                to_string(sub_tot, "->>,>>>,>>>,>>9.99")

                        if sub_tot1 < -99999999 or sub_tot1 > 999999999:
                            str = str + \
                                to_string(sub_tot1, "->>,>>>,>>>,>>9.99")
                        else:
                            str = str + \
                                to_string(sub_tot1, "->>,>>>,>>>,>>9.99")
                    else:
                        str = to_string("", "x(33)") + \
                            to_string("T O T A L ", "x(24)") + \
                            to_string(" ", "x(12)") + \
                            to_string(qty, "->>>>>9") + \
                            to_string(sub_tot, "->,>>>,>>>,>>>,>>9") + \
                            to_string(sub_tot1, "->,>>>,>>>,>>>,>>9")

                # start - DZIKRI: 1A82C7
                if dqty > 0 and it_exist and from_dept != to_dept:
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    if price_decimal == 2:
                        str = to_string("", "x(33)") + \
                            to_string(trim(to_string(hoteldpt.depart, "x(12)")) + " T O T A L ", "x(24)") + \
                            to_string(" ", "x(12)") + \
                            to_string(dqty, "->>>>>9")

                        if dsub_tot < -99999999 or dsub_tot > 999999999:
                            str = str + \
                                to_string(dsub_tot, "->>,>>>,>>>,>>9.99")
                        else:
                            str = str + \
                                to_string(dsub_tot, "->>,>>>,>>>,>>9.99")

                        if dsub_tot1 < -99999999 or dsub_tot1 > 999999999:
                            str = str + \
                                to_string(dsub_tot1, "->>,>>>,>>>,>>9.99")
                        else:
                            str = str + \
                                to_string(dsub_tot1, "->>,>>>,>>>,>>9.99")
                    else:
                        str = to_string("", "x(33)") + \
                            to_string(trim(to_string(hoteldpt.depart, "x(12)")) + " T O T A L ", "x(24)") + \
                            to_string(" ", "x(12)") + \
                            to_string(dqty, "->>>>>9") + \
                            to_string(dsub_tot, "->,>>>,>>>,>>>,>>9") + \
                            to_string(dsub_tot1, "->,>>>,>>>,>>>,>>9")
                    # end - DZIKRI: 1A82C7
            output_list = Output_list()
            output_list_data.append(output_list)

            if price_decimal == 2:
                str = to_string("", "x(33)") + \
                    to_string("GRAND TOTAL ", "x(24)") + \
                    to_string(" ", "x(12)") + to_string(gqty, "->>>>>9")

                if gsub_tot < -99999999 or gsub_tot > 999999999:
                    str = str + to_string(gsub_tot, "->>,>>>,>>>,>>9.99")
                else:
                    str = str + to_string(gsub_tot, "->>,>>>,>>>,>>9.99")

                if gsub_tot1 < -99999999 or gsub_tot1 > 999999999:
                    str = str + to_string(gsub_tot1, "->>,>>>,>>>,>>9.99")
                else:
                    str = str + to_string(gsub_tot1, "->>,>>>,>>>,>>9.99")
            else:
                str = to_string("", "x(33)") + \
                    to_string("GRAND TOTAL ", "x(24)") + \
                    to_string(" ", "x(12)") + \
                    to_string(gqty, "->>>>>9") + \
                    to_string(gsub_tot, "->,>>>,>>>,>>>,>>9") + \
                    to_string(gsub_tot1, "->,>>>,>>>,>>>,>>9")

    htparam = get_cache(Htparam, {"paramnr": [(eq, 557)]})
    disc_art1 = htparam.finteger

    htparam = get_cache(Htparam, {"paramnr": [(eq, 596)]})
    disc_art2 = htparam.finteger

    htparam = get_cache(Htparam, {"paramnr": [(eq, 556)]})
    disc_art3 = htparam.finteger
    journal_list()

    return generate_output()
