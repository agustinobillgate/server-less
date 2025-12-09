#using conversion tools version: 1.0.0.119
#------------------------------------------
# Rd, 05/11/2025
# 
#------------------------------------------

from functions.additional_functions import *
from decimal import Decimal
from functions.calc_servtaxesbl import calc_servtaxesbl
from sqlalchemy import func
from models import Bill_line, Bill, Artikel, Queasy, Res_line, Billjournal

def fo_invoice_disp_bill_line_cldbl(bil_recid:int, double_currency:bool):

    prepare_cache ([Bill, Artikel, Queasy, Billjournal])

    t_bill_line_data = []
    t_spbill_list_data = []
    serv:Decimal = to_decimal("0.0")
    vat:Decimal = to_decimal("0.0")
    netto:Decimal = to_decimal("0.0")
    vat2:Decimal = to_decimal("0.0")
    fact:Decimal = to_decimal("0.0")
    art_type:int = 0
    ar_ledger:int = 0
    bill_line = bill = artikel = queasy = res_line = billjournal = None

    t_spbill_list = t_bill_line = None

    t_spbill_list_data, T_spbill_list = create_model("T_spbill_list", {"selected":bool, "bl_recid":int}, {"selected": True})
    t_bill_line_data, T_bill_line = create_model_like(Bill_line, {"rec_id":int, "serv":Decimal, "vat":Decimal, "netto":Decimal, "art_type":int, "counter":int, "addserv":bool, "addvat":bool, "bjournal":bool})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_bill_line_data, t_spbill_list_data, serv, vat, netto, vat2, fact, art_type, ar_ledger, bill_line, bill, artikel, queasy, res_line, billjournal
        nonlocal bil_recid, double_currency


        nonlocal t_spbill_list, t_bill_line
        nonlocal t_spbill_list_data, t_bill_line_data

        return {"t-bill-line": t_bill_line_data, "t-spbill-list": t_spbill_list_data}


    # bill = get_cache (Bill, {"_recid": [(eq, bil_recid)]})
    bill = db_session.query(Bill).filter((Bill._recid == bil_recid)).first()

    if bill:

        for bill_line in db_session.query(Bill_line).filter(
                 (Bill_line.rechnr == bill.rechnr)).order_by(Bill_line._recid).all():

            t_spbill_list = query(t_spbill_list_data, filters=(lambda t_spbill_list: t_spbill_list.bl_recid == to_int(bill_line._recid)), first=True)

            if not t_spbill_list:
                t_spbill_list = T_spbill_list()
                t_spbill_list_data.append(t_spbill_list)

                t_spbill_list.selected = False
                t_spbill_list.bl_recid = bill_line._recid

        if double_currency:

            for bill_line in db_session.query(Bill_line).filter(
                     (Bill_line.rechnr == bill.rechnr)).order_by(Bill_line._recid).all():
                serv =  to_decimal("0")
                vat =  to_decimal("0")
                netto =  to_decimal("0")
                vat2 =  to_decimal("0")
                fact =  to_decimal("0")

                artikel = get_cache (Artikel, {"artnr": [(eq, bill_line.artnr)]})

                if artikel:
                    art_type = artikel.artart
                    serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, bill_line.bill_datum))
                    
                t_bill_line = T_bill_line()
                t_bill_line_data.append(t_bill_line)

                buffer_copy(bill_line, t_bill_line)
                t_bill_line.rec_id = bill_line._recid
                netto =  to_decimal(bill_line.betrag) / to_decimal(fact)
                t_bill_line.serv =  to_decimal(netto) * to_decimal(serv)
                t_bill_line.vat =  to_decimal(netto) * to_decimal(vat)
                t_bill_line.netto =  to_decimal(t_bill_line.betrag) - to_decimal(t_bill_line.serv) - to_decimal(t_bill_line.vat)
                t_bill_line.art_type = art_type

        else:

            for bill_line in db_session.query(Bill_line).filter(
                     (Bill_line.rechnr == bill.rechnr)).order_by(Bill_line._recid).all():
                serv =  to_decimal("0")
                vat =  to_decimal("0")
                netto =  to_decimal("0")
                vat2 =  to_decimal("0")
                fact =  to_decimal("0")

                artikel = get_cache (Artikel, {"artnr": [(eq, bill_line.artnr)]})

                if artikel:
                    art_type = artikel.artart
                    serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, bill_line.bill_datum))

                t_bill_line = T_bill_line()
                t_bill_line_data.append(t_bill_line)

                buffer_copy(bill_line, t_bill_line)
                t_bill_line.rec_id = bill_line._recid
                netto =  to_decimal(bill_line.betrag) / to_decimal(fact)
                t_bill_line.serv =  to_decimal(netto) * to_decimal(serv)
                t_bill_line.vat =  to_decimal(netto) * to_decimal(vat)
                t_bill_line.netto =  to_decimal(t_bill_line.betrag) - to_decimal(t_bill_line.serv) - to_decimal(t_bill_line.vat)
                t_bill_line.art_type = art_type


        queasy = get_cache (Queasy, {"key": [(eq, 329)],"number1": [(eq, bill.resnr)]})

        if queasy and bill.billnr == 1:

            res_line = get_cache (Res_line, {"resnr": [(eq, queasy.number1)],"reslinnr": [(eq, queasy.number2)]})

            if res_line:

                billjournal_obj_list = {}
                billjournal = Billjournal()
                artikel = Artikel()
                for billjournal.bill_datum, billjournal.bezeich, billjournal.betrag, billjournal._recid, artikel.artart, artikel.artnr, artikel.departement, artikel._recid in db_session.query(Billjournal.bill_datum, Billjournal.bezeich, Billjournal.betrag, Billjournal._recid, Artikel.artart, Artikel.artnr, Artikel.departement, Artikel._recid).join(Artikel,(Artikel.artnr == Billjournal.artnr) & (Artikel.departement == Billjournal.departement)).filter(
                         (matches(Billjournal.bezeich,"*Payment Leasing #*")) & (Billjournal.artnr != ar_ledger) & (Billjournal.betrag < 0) & (num_entries(Billjournal.bezeich, "#") > 0) & (entry(1, Billjournal.bezeich, "#") == to_string(bill.resnr) + "]")).order_by(Billjournal._recid).all():
                    if billjournal_obj_list.get(billjournal._recid):
                        continue
                    else:
                        billjournal_obj_list[billjournal._recid] = True


                    t_bill_line = T_bill_line()
                    t_bill_line_data.append(t_bill_line)

                    t_bill_line.bill_datum = billjournal.bill_datum
                    t_bill_line.rechnr = 0
                    t_bill_line.bezeich = billjournal.bezeich
                    t_bill_line.anzahl = 1
                    t_bill_line.zinr = bill.zinr
                    t_bill_line.betrag =  to_decimal(t_bill_line.betrag) + to_decimal(billjournal.betrag)
                    t_bill_line.nettobetrag =  to_decimal(t_bill_line.nettobetrag) + to_decimal(billjournal.betrag)
                    t_bill_line.bjournal = True

                billjournal_obj_list = {}
                billjournal = Billjournal()
                artikel = Artikel()
                for billjournal.bill_datum, billjournal.bezeich, billjournal.betrag, billjournal._recid, artikel.artart, artikel.artnr, artikel.departement, artikel._recid in db_session.query(Billjournal.bill_datum, Billjournal.bezeich, Billjournal.betrag, Billjournal._recid, Artikel.artart, Artikel.artnr, Artikel.departement, Artikel._recid).join(Artikel,(Artikel.artnr == Billjournal.artnr) & (Artikel.departement == Billjournal.departement)).filter(
                         (matches(Billjournal.bezeich,"*Payment Change Rate #*")) & (Billjournal.artnr != ar_ledger) & (num_entries(Billjournal.bezeich, "#") > 0) & (entry(1, Billjournal.bezeich, "#") == to_string(bill.resnr) + "]")).order_by(Billjournal._recid).all():
                    if billjournal_obj_list.get(billjournal._recid):
                        continue
                    else:
                        billjournal_obj_list[billjournal._recid] = True


                    t_bill_line = T_bill_line()
                    t_bill_line_data.append(t_bill_line)

                    t_bill_line.bill_datum = billjournal.bill_datum
                    t_bill_line.rechnr = 0
                    t_bill_line.bezeich = billjournal.bezeich
                    t_bill_line.anzahl = 1
                    t_bill_line.zinr = bill.zinr
                    t_bill_line.betrag =  to_decimal(t_bill_line.betrag) + to_decimal(billjournal.betrag)
                    t_bill_line.nettobetrag =  to_decimal(t_bill_line.nettobetrag) + to_decimal(billjournal.betrag)
                    t_bill_line.bjournal = True

                billjournal_obj_list = {}
                billjournal = Billjournal()
                artikel = Artikel()
                for billjournal.bill_datum, billjournal.bezeich, billjournal.betrag, billjournal._recid, artikel.artart, artikel.artnr, artikel.departement, artikel._recid in db_session.query(Billjournal.bill_datum, Billjournal.bezeich, Billjournal.betrag, Billjournal._recid, Artikel.artart, Artikel.artnr, Artikel.departement, Artikel._recid).join(Artikel,(Artikel.artnr == Billjournal.artnr) & (Artikel.departement == Billjournal.departement)).filter(
                         (matches(Billjournal.bezeich,"*Refund Change Rate #*")) & (Billjournal.artnr != ar_ledger) & (num_entries(Billjournal.bezeich, "#") > 0) & (entry(1, Billjournal.bezeich, "#") == to_string(bill.resnr) + "]")).order_by(Billjournal._recid).all():
                    if billjournal_obj_list.get(billjournal._recid):
                        continue
                    else:
                        billjournal_obj_list[billjournal._recid] = True


                    t_bill_line = T_bill_line()
                    t_bill_line_data.append(t_bill_line)

                    t_bill_line.bill_datum = billjournal.bill_datum
                    t_bill_line.rechnr = 0
                    t_bill_line.bezeich = billjournal.bezeich
                    t_bill_line.anzahl = 1
                    t_bill_line.zinr = bill.zinr
                    t_bill_line.betrag =  to_decimal(t_bill_line.betrag) + to_decimal(billjournal.betrag)
                    t_bill_line.nettobetrag =  to_decimal(t_bill_line.nettobetrag) + to_decimal(billjournal.betrag)
                    t_bill_line.bjournal = True

    return generate_output()