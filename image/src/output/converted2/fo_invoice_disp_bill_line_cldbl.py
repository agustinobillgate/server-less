#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from functions.calc_servvat import calc_servvat
from models import Bill_line, Bill, Artikel

def fo_invoice_disp_bill_line_cldbl(bil_recid:int, double_currency:bool):

    prepare_cache ([Bill, Artikel])

    t_bill_line_list = []
    t_spbill_list_list = []
    serv:Decimal = to_decimal("0.0")
    vat:Decimal = to_decimal("0.0")
    netto:Decimal = to_decimal("0.0")
    art_type:int = 0
    bill_line = bill = artikel = None

    t_spbill_list = t_bill_line = None

    t_spbill_list_list, T_spbill_list = create_model("T_spbill_list", {"selected":bool, "bl_recid":int}, {"selected": True})
    t_bill_line_list, T_bill_line = create_model_like(Bill_line, {"rec_id":int, "serv":Decimal, "vat":Decimal, "netto":Decimal, "art_type":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_bill_line_list, t_spbill_list_list, serv, vat, netto, art_type, bill_line, bill, artikel
        nonlocal bil_recid, double_currency


        nonlocal t_spbill_list, t_bill_line
        nonlocal t_spbill_list_list, t_bill_line_list

        return {"t-bill-line": t_bill_line_list, "t-spbill-list": t_spbill_list_list}


    bill = get_cache (Bill, {"_recid": [(eq, bil_recid)]})

    if bill:

        for bill_line in db_session.query(Bill_line).filter(
                 (Bill_line.rechnr == bill.rechnr)).order_by(Bill_line._recid).all():

            t_spbill_list = query(t_spbill_list_list, filters=(lambda t_spbill_list: t_spbill_list.bl_recid == to_int(bill_line._recid)), first=True)

            if not t_spbill_list:
                t_spbill_list = T_spbill_list()
                t_spbill_list_list.append(t_spbill_list)

                t_spbill_list.selected = False
                t_spbill_list.bl_recid = bill_line._recid

        if double_currency:

            for bill_line in db_session.query(Bill_line).filter(
                     (Bill_line.rechnr == bill.rechnr)).order_by(Bill_line._recid).all():
                serv =  to_decimal("0")
                vat =  to_decimal("0")
                netto =  to_decimal("0")

                artikel = get_cache (Artikel, {"artnr": [(eq, bill_line.artnr)]})

                if artikel:
                    art_type = artikel.artart


                    serv, vat = get_output(calc_servvat(artikel.departement, artikel.artnr, bill_line.bill_datum, artikel.service_code, artikel.mwst_code))
                t_bill_line = T_bill_line()
                t_bill_line_list.append(t_bill_line)

                buffer_copy(bill_line, t_bill_line)
                t_bill_line.rec_id = bill_line._recid
                t_bill_line.serv =  to_decimal(t_bill_line.betrag) * to_decimal(serv)
                t_bill_line.vat =  to_decimal(t_bill_line.betrag) * to_decimal(vat)
                t_bill_line.netto =  to_decimal(t_bill_line.betrag) - to_decimal(t_bill_line.serv) - to_decimal(t_bill_line.vat)
                t_bill_line.art_type = art_type

        else:

            for bill_line in db_session.query(Bill_line).filter(
                     (Bill_line.rechnr == bill.rechnr)).order_by(Bill_line._recid).all():
                serv =  to_decimal("0")
                vat =  to_decimal("0")
                netto =  to_decimal("0")

                artikel = get_cache (Artikel, {"artnr": [(eq, bill_line.artnr)]})

                if artikel:
                    art_type = artikel.artart


                    serv, vat = get_output(calc_servvat(artikel.departement, artikel.artnr, bill_line.bill_datum, artikel.service_code, artikel.mwst_code))
                t_bill_line = T_bill_line()
                t_bill_line_list.append(t_bill_line)

                buffer_copy(bill_line, t_bill_line)
                t_bill_line.rec_id = bill_line._recid
                t_bill_line.serv =  to_decimal(t_bill_line.betrag) * to_decimal(serv)
                t_bill_line.vat =  to_decimal(t_bill_line.betrag) * to_decimal(vat)
                t_bill_line.netto =  to_decimal(t_bill_line.betrag) - to_decimal(t_bill_line.serv) - to_decimal(t_bill_line.vat)
                t_bill_line.art_type = art_type


    return generate_output()