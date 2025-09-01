#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 1/9/2025
# beda sorting
#------------------------------------------

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Artikel, Hoteldpt, Billjournal

def fo_cjourn_listbl(from_art:int, to_art:int, from_dept:int, to_dept:int, from_date:date, to_date:date, foreign_flag:bool, long_digit:bool):

    prepare_cache ([Htparam, Hoteldpt, Billjournal])

    cjourn_list_data = []
    htparam = artikel = hoteldpt = billjournal = None

    output_list = cjourn_list = htl_list = art_list = None

    output_list_data, Output_list = create_model("Output_list", {"str":string})
    cjourn_list_data, Cjourn_list = create_model("Cjourn_list", {"artnr":int, "bezeich":string, "dept":string, "datum":date, "zinr":string, "rechnr":int, "canc_reason":string, "qty":int, "amount":Decimal, "zeit":string, "id":string})
    htl_list_data, Htl_list = create_model("Htl_list", {"num":int, "depart":string})
    art_list_data, Art_list = create_model("Art_list", {"artnr":int, "departement":int, "endkum":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal cjourn_list_data, htparam, artikel, hoteldpt, billjournal
        nonlocal from_art, to_art, from_dept, to_dept, from_date, to_date, foreign_flag, long_digit


        nonlocal output_list, cjourn_list, htl_list, art_list
        nonlocal output_list_data, cjourn_list_data, htl_list_data, art_list_data

        return {"cjourn-list": cjourn_list_data}

    def journal_list():

        nonlocal cjourn_list_data, htparam, artikel, hoteldpt, billjournal
        nonlocal from_art, to_art, from_dept, to_dept, from_date, to_date, foreign_flag, long_digit


        nonlocal output_list, cjourn_list, htl_list, art_list
        nonlocal output_list_data, cjourn_list_data, htl_list_data, art_list_data

        qty:int = 0
        sub_tot:Decimal = to_decimal("0.0")
        tot:Decimal = to_decimal("0.0")
        curr_date:date = None
        last_dept:int = -1
        it_exist:bool = False
        ekumnr:int = 0
        amount:Decimal = to_decimal("0.0")
        hoteldpt_num:int = 0
        hoteldpt_depart:string = ""
        curr_art:int = 0
        curr_dept:int = 0
        i:int = 0

        htparam = get_cache (Htparam, {"paramnr": [(eq, 555)]})

        if htparam:
            ekumnr = htparam.finteger
        cjourn_list_data.clear()

        for artikel in db_session.query(Artikel).filter(
                 (Artikel.artnr >= from_art) & (Artikel.artnr <= to_art) & (Artikel.departement >= from_dept) & 
                 (Artikel.departement <= to_dept) & (Artikel.endkum != ekumnr)).order_by((Artikel.departement * 10000 + Artikel.artnr)).all():

            htl_list = query(htl_list_data, filters=(lambda htl_list: htl_list.num == artikel.departement), first=True)

            if not htl_list:

                hoteldpt = get_cache (Hoteldpt, {"num": [(eq, artikel.departement)]})

                if hoteldpt:
                    htl_list = Htl_list()
                    htl_list_data.append(htl_list)

                    htl_list.num = hoteldpt.num
                    htl_list.depart = hoteldpt.depart


            art_list = Art_list()
            art_list_data.append(art_list)

            buffer_copy(artikel, art_list)

        for billjournal in db_session.query(Billjournal).filter(
                 (Billjournal.stornogrund != "") & (Billjournal.bill_datum >= from_date) & 
                 (Billjournal.bill_datum <= to_date) & (Billjournal.artnr >= from_art) & 
                 (Billjournal.artnr <= to_art)).order_by(((Billjournal.departement * 10000) + Billjournal.artnr), Billjournal.sysdate, Billjournal.zeit).all():

            art_list = query(art_list_data, filters=(lambda art_list: art_list.artnr == billjournal.artnr and art_list.departement == billjournal.departement), first=True)

            if art_list:
                i = i + 1

                # if curr_art != billjournal.artnr and curr_dept != billjournal.departement and i != 1:
                if curr_art != billjournal.artnr  and i != 1:
                    cjourn_list = Cjourn_list()
                    cjourn_list_data.append(cjourn_list)

                    cjourn_list.canc_reason = "T O T A L   "
                    cjourn_list.qty = qty
                    cjourn_list.amount =  to_decimal(sub_tot)
                    qty = 0
                    sub_tot =  to_decimal("0")
                    curr_art = billjournal.artnr
                    curr_dept = billjournal.departement

                if i == 1:
                    curr_art = billjournal.artnr
                    curr_dept = billjournal.departement

                if foreign_flag:
                    amount =  to_decimal(billjournal.fremdwaehrng)
                else:
                    amount =  to_decimal(billjournal.betrag)
                cjourn_list = Cjourn_list()
                cjourn_list_data.append(cjourn_list)

                cjourn_list.artnr = billjournal.artnr
                cjourn_list.bezeich = billjournal.bezeich
                cjourn_list.datum = billjournal.bill_datum
                cjourn_list.zinr = billjournal.zinr
                cjourn_list.rechnr = billjournal.rechnr
                cjourn_list.canc_reason = billjournal.stornogrund
                cjourn_list.qty = billjournal.anzahl
                cjourn_list.amount =  to_decimal(amount)
                cjourn_list.zeit = to_string(billjournal.zeit, "HH:MM")
                cjourn_list.id = billjournal.userinit
                qty = qty + billjournal.anzahl


                sub_tot =  to_decimal(sub_tot) + to_decimal(amount)
                tot =  to_decimal(tot) + to_decimal(amount)

                htl_list = query(htl_list_data, filters=(lambda htl_list: htl_list.num == billjournal.departement), first=True)

                if htl_list:
                    cjourn_list.dept = htl_list.depart
        cjourn_list = Cjourn_list()
        cjourn_list_data.append(cjourn_list)

        cjourn_list.canc_reason = "T O T A L   "
        cjourn_list.qty = qty
        cjourn_list.amount =  to_decimal(sub_tot)


        cjourn_list = Cjourn_list()
        cjourn_list_data.append(cjourn_list)

        cjourn_list.canc_reason = "Grand TOTAL"
        cjourn_list.qty = 0
        cjourn_list.amount =  to_decimal(tot)


    journal_list()

    return generate_output()