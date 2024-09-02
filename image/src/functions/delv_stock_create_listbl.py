from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import L_lieferant, L_artikel, L_op, L_ophis

def delv_stock_create_listbl(sname:str, fdate:date, tdate:date, show_price:bool, long_digit:bool):
    ttstock_list = []
    tot_anz:decimal = 0
    tot_amount:decimal = 0
    note_str:[str] = ["", "", ""]
    l_lieferant = l_artikel = l_op = l_ophis = None

    ttstock = None

    ttstock_list, Ttstock = create_model("Ttstock", {"ddate":date, "ist":int, "sdocument":str, "delivnote":str, "iarticle":int, "sdesc":str, "dquantity":int, "samount":str, "price":decimal, "itime":str, "ssupplier":str, "snote":str, "imark":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal ttstock_list, tot_anz, tot_amount, note_str, l_lieferant, l_artikel, l_op, l_ophis


        nonlocal ttstock
        nonlocal ttstock_list
        return {"ttStock": ttstock_list}

    def create_list():

        nonlocal ttstock_list, tot_anz, tot_amount, note_str, l_lieferant, l_artikel, l_op, l_ophis


        nonlocal ttstock
        nonlocal ttstock_list

        del_note2:str = ""
        curr_note:str = ""
        sub_anz:int = 0
        sub_amount:decimal = 0
        ttStock_list.clear()
        tot_anz = 0
        tot_amount = 0
        sub_anz = 0
        sub_amount = 0

        l_lieferant = db_session.query(L_lieferant).filter(
                (func.lower(L_lieferant.firma) == (sname).lower())).first()

        if l_lieferant:

            l_op_obj_list = []
            for l_op, l_artikel in db_session.query(L_op, L_artikel).join(L_artikel,(L_artikel.artnr == L_op.artnr)).filter(
                    (L_op.loeschflag < 2) &  (L_op.op_art == 1) &  (L_op.lief_nr == l_lieferant.lief_nr) &  (L_op.datum >= fdate) &  (L_op.datum <= tdate)).all():
                if l_op._recid in l_op_obj_list:
                    continue
                else:
                    l_op_obj_list.append(l_op._recid)

                if curr_note != "" and curr_note != l_op.lscheinnr:
                    ttstock = Ttstock()
                    ttstock_list.append(ttstock)

                    ttStock.sDesc = "SubTotal"
                    ttStock.dQuantity = sub_anz
                    ttStock.iMark = 1

                    if show_price:
                        ttStock.sAmount = IF long_digit THEN
                        to_string(sub_amount, "   ->>>,>>>,>>>,>>9") ELSE
                        to_string(sub_amount, "->>>,>>>,>>>,>>9.99")


                    sub_anz = 0
                    sub_amount = 0


                curr_note = l_op.lscheinnr
                ttstock = Ttstock()
                ttstock_list.append(ttstock)

                sub_anz = sub_anz + l_op.anzahl
                sub_amount = sub_amount + l_op.warenwert
                tot_anz = tot_anz + l_op.anzahl
                tot_amount = tot_amount + l_op.warenwert
                ttStock.dDate = l_op.datum
                ttStock.iSt = l_op.lager_nr
                ttStock.iArticle = l_artikel.artnr
                ttStock.sDocument = l_op.docu_nr
                ttStock.sDesc = l_artikel.bezeich
                ttStock.dQuantity = l_op.anzahl
                ttstock.price = l_op.einzelpreis
                ttstock.itime = to_string(l_op.zeit, "HH:MM:SS")
                ttStock.sNote = note_str[l_op.op_art - 1]
                ttStock.iMark = 0
                ttStock.sSupplier = l_lieferant.firma
                ttStock.delivnote = l_op.lscheinnr

                if show_price:
                    ttStock.sAmount = IF long_digit THEN
                    to_string(l_op.warenwert, "   ->>>,>>>,>>>,>>9") ELSE
                    to_string(l_op.warenwert, "->>>,>>>,>>>,>>9.99")

            l_ophis_obj_list = []
            for l_ophis, l_artikel in db_session.query(L_ophis, L_artikel).join(L_artikel,(L_artikel.artnr == L_ophis.artnr)).filter(
                    (L_ophis.lief_nr == l_lieferant.lief_nr) &  (L_ophis.datum >= fdate) &  (L_ophis.datum <= tdate) &  (L_ophis.op_art == 1) &  (not L_ophis.fibukonto.op("~")(".*;CANCELLED.*"))).all():
                if l_ophis._recid in l_ophis_obj_list:
                    continue
                else:
                    l_ophis_obj_list.append(l_ophis._recid)

                if curr_note != "" and curr_note != l_ophis.lscheinnr:
                    ttstock = Ttstock()
                    ttstock_list.append(ttstock)

                    ttStock.sDesc = "SubTotal"
                    ttStock.dQuantity = sub_anz
                    ttStock.iMark = 1

                    if show_price:
                        ttStock.sAmount = IF long_digit THEN
                        to_string(sub_amount, "   ->>>,>>>,>>>,>>9") ELSE
                        to_string(sub_amount, "->>>,>>>,>>>,>>9.99")


                    sub_anz = 0
                    sub_amount = 0


                curr_note = l_ophis.lscheinnr
                ttstock = Ttstock()
                ttstock_list.append(ttstock)

                sub_anz = sub_anz + l_ophis.anzahl
                sub_amount = sub_amount + l_ophis.warenwert
                tot_anz = tot_anz + l_ophis.anzahl
                tot_amount = tot_amount + l_ophis.warenwert
                ttStock.dDate = l_ophis.datum
                ttStock.iSt = l_ophis.lager_nr
                ttStock.iArticle = l_artikel.artnr
                ttStock.sDocument = l_ophis.docu_nr
                ttStock.sDesc = l_artikel.bezeich
                ttStock.dQuantity = l_ophis.anzahl
                ttstock.price = l_ophis.einzelpreis
                ttStock.sNote = note_str[l_ophis.op_art - 1]
                ttStock.iMark = 0
                ttStock.sSupplier = l_lieferant.firma
                ttStock.delivnote = l_ophis.lscheinnr

                if show_price:
                    ttStock.sAmount = IF long_digit THEN
                    to_string(l_ophis.warenwert, "   ->>>,>>>,>>>,>>9") ELSE
                    to_string(l_ophis.warenwert, "->>>,>>>,>>>,>>9.99")


            ttstock = Ttstock()
            ttstock_list.append(ttstock)

            ttStock.sDesc = "SubTotal"
            ttStock.dQuantity = sub_anz
            ttStock.iMark = 1

            if show_price:
                ttStock.sAmount = IF long_digit THEN
                to_string(sub_amount, "   ->>>,>>>,>>>,>>9") ELSE
                to_string(sub_amount, "->>>,>>>,>>>,>>9.99")


            ttstock = Ttstock()
            ttstock_list.append(ttstock)

            ttStock.sDesc = "T O T A L"
            ttStock.dQuantity = tot_anz
            ttStock.iMark = 2

            if show_price:
                ttStock.sAmount = IF long_digit THEN
                to_string(tot_amount, "   ->>>,>>>,>>>,>>9") ELSE
                to_string(tot_amount, "->>>,>>>,>>>,>>9.99")


    create_list()

    return generate_output()