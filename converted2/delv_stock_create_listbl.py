#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from sqlalchemy import func
from models import L_lieferant, L_artikel, L_op, L_ophis

def delv_stock_create_listbl(sname:string, fdate:date, tdate:date, show_price:bool, long_digit:bool):

    prepare_cache ([L_lieferant, L_artikel, L_op, L_ophis])

    ttstock_data = []
    tot_anz:Decimal = to_decimal("0.0")
    tot_amount:Decimal = to_decimal("0.0")
    note_str:List[string] = [" ", "Transfer"]
    l_lieferant = l_artikel = l_op = l_ophis = None

    ttstock = None

    ttstock_data, Ttstock = create_model("Ttstock", {"ddate":date, "ist":int, "sdocument":string, "delivnote":string, "iarticle":int, "sdesc":string, "dquantity":int, "samount":string, "price":Decimal, "itime":string, "ssupplier":string, "snote":string, "imark":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal ttstock_data, tot_anz, tot_amount, note_str, l_lieferant, l_artikel, l_op, l_ophis
        nonlocal sname, fdate, tdate, show_price, long_digit


        nonlocal ttstock
        nonlocal ttstock_data

        return {"ttStock": ttstock_data}

    def create_list():

        nonlocal ttstock_data, tot_anz, tot_amount, note_str, l_lieferant, l_artikel, l_op, l_ophis
        nonlocal sname, fdate, tdate, show_price, long_digit


        nonlocal ttstock
        nonlocal ttstock_data

        del_note2:string = ""
        curr_note:string = ""
        sub_anz:int = 0
        sub_amount:Decimal = to_decimal("0.0")
        ttstock_data.clear()
        tot_anz =  to_decimal("0")
        tot_amount =  to_decimal("0")
        sub_anz = 0
        sub_amount =  to_decimal("0")

        l_lieferant = get_cache (L_lieferant, {"firma": [(eq, sname)]})

        if l_lieferant:

            l_op_obj_list = {}
            l_op = L_op()
            l_artikel = L_artikel()
            for l_op.lscheinnr, l_op.anzahl, l_op.warenwert, l_op.datum, l_op.lager_nr, l_op.docu_nr, l_op.einzelpreis, l_op.zeit, l_op._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel._recid in db_session.query(L_op.lscheinnr, L_op.anzahl, L_op.warenwert, L_op.datum, L_op.lager_nr, L_op.docu_nr, L_op.einzelpreis, L_op.zeit, L_op._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel._recid).join(L_artikel,(L_artikel.artnr == L_op.artnr)).filter(
                     (L_op.loeschflag < 2) & (L_op.op_art == 1) & (L_op.lief_nr == l_lieferant.lief_nr) & (L_op.datum >= fdate) & (L_op.datum <= tdate)).order_by(L_op.lscheinnr, L_op.artnr).all():
                if l_op_obj_list.get(l_op._recid):
                    continue
                else:
                    l_op_obj_list[l_op._recid] = True

                if curr_note != "" and curr_note != l_op.lscheinnr:
                    ttstock = Ttstock()
                    ttstock_data.append(ttstock)

                    ttstock.sdesc = "SubTotal"
                    ttstock.dquantity = sub_anz
                    ttstock.imark = 1

                    if show_price:

                        if long_digit:
                            ttstock.samount = to_string(sub_amount, " ->>>,>>>,>>>,>>9")
                        else:
                            ttstock.samount = to_string(sub_amount, "->>>,>>>,>>>,>>9.99")
                    sub_anz = 0
                    sub_amount =  to_decimal("0")


                curr_note = l_op.lscheinnr
                ttstock = Ttstock()
                ttstock_data.append(ttstock)

                sub_anz = sub_anz + l_op.anzahl
                sub_amount =  to_decimal(sub_amount) + to_decimal(l_op.warenwert)
                tot_anz =  to_decimal(tot_anz) + to_decimal(l_op.anzahl)
                tot_amount =  to_decimal(tot_amount) + to_decimal(l_op.warenwert)
                ttstock.ddate = l_op.datum
                ttstock.ist = l_op.lager_nr
                ttstock.iarticle = l_artikel.artnr
                ttstock.sdocument = l_op.docu_nr
                ttstock.sdesc = l_artikel.bezeich
                ttstock.dquantity = l_op.anzahl
                ttstock.price =  to_decimal(l_op.einzelpreis)
                ttstock.itime = to_string(l_op.zeit, "HH:MM:SS")
                ttstock.snote = note_str[l_op.op_art - 1]
                ttstock.imark = 0
                ttstock.ssupplier = l_lieferant.firma
                ttstock.delivnote = l_op.lscheinnr

                if show_price:

                    if long_digit:
                        ttstock.samount = to_string(l_op.warenwert, " ->>>,>>>,>>>,>>9")
                    else:
                        ttstock.samount = to_string(l_op.warenwert, "->>>,>>>,>>>,>>9.99")

            l_ophis_obj_list = {}
            l_ophis = L_ophis()
            l_artikel = L_artikel()
            for l_ophis.lscheinnr, l_ophis.anzahl, l_ophis.warenwert, l_ophis.datum, l_ophis.lager_nr, l_ophis.docu_nr, l_ophis.einzelpreis, l_ophis._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel._recid in db_session.query(L_ophis.lscheinnr, L_ophis.anzahl, L_ophis.warenwert, L_ophis.datum, L_ophis.lager_nr, L_ophis.docu_nr, L_ophis.einzelpreis, L_ophis._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel._recid).join(L_artikel,(L_artikel.artnr == L_ophis.artnr)).filter(
                     (L_ophis.lief_nr == l_lieferant.lief_nr) & (L_ophis.datum >= fdate) & (L_ophis.datum <= tdate) & (L_ophis.op_art == 1) & (not_(matches(L_ophis.fibukonto,"*;CANCELLED*")))).order_by(L_ophis.lscheinnr, L_ophis.artnr).all():
                if l_ophis_obj_list.get(l_ophis._recid):
                    continue
                else:
                    l_ophis_obj_list[l_ophis._recid] = True

                if curr_note != "" and curr_note != l_ophis.lscheinnr:
                    ttstock = Ttstock()
                    ttstock_data.append(ttstock)

                    ttstock.sdesc = "SubTotal"
                    ttstock.dquantity = sub_anz
                    ttstock.imark = 1

                    if show_price:

                        if long_digit:
                            ttstock.samount = to_string(sub_amount, " ->>>,>>>,>>>,>>9")
                        else:
                            ttstock.samount = to_string(sub_amount, "->>>,>>>,>>>,>>9.99")
                    sub_anz = 0
                    sub_amount =  to_decimal("0")


                curr_note = l_ophis.lscheinnr
                ttstock = Ttstock()
                ttstock_data.append(ttstock)

                sub_anz = sub_anz + l_ophis.anzahl
                sub_amount =  to_decimal(sub_amount) + to_decimal(l_ophis.warenwert)
                tot_anz =  to_decimal(tot_anz) + to_decimal(l_ophis.anzahl)
                tot_amount =  to_decimal(tot_amount) + to_decimal(l_ophis.warenwert)
                ttstock.ddate = l_ophis.datum
                ttstock.ist = l_ophis.lager_nr
                ttstock.iarticle = l_artikel.artnr
                ttstock.sdocument = l_ophis.docu_nr
                ttstock.sdesc = l_artikel.bezeich
                ttstock.dquantity = l_ophis.anzahl
                ttstock.price =  to_decimal(l_ophis.einzelpreis)
                ttstock.snote = note_str[l_ophis.op_art - 1]
                ttstock.imark = 0
                ttstock.ssupplier = l_lieferant.firma
                ttstock.delivnote = l_ophis.lscheinnr

                if show_price:

                    if long_digit:
                        ttstock.samount = to_string(l_op.warenwert, " ->>>,>>>,>>>,>>9")
                    else:
                        ttstock.samount = to_string(l_op.warenwert, "->>>,>>>,>>>,>>9.99")
            ttstock = Ttstock()
            ttstock_data.append(ttstock)

            ttstock.sdesc = "SubTotal"
            ttstock.dquantity = sub_anz
            ttstock.imark = 1

            if show_price:

                if long_digit:
                    ttstock.samount = to_string(sub_amount, " ->>>,>>>,>>>,>>9")
                else:
                    ttstock.samount = to_string(sub_amount, "->>>,>>>,>>>,>>9.99")
            ttstock = Ttstock()
            ttstock_data.append(ttstock)

            ttstock.sdesc = "T O T A L"
            ttstock.dquantity = tot_anz
            ttstock.imark = 2

            if show_price:

                if long_digit:
                    ttstock.samount = to_string(tot_amount, " ->>>,>>>,>>>,>>9")
                else:
                    ttstock.samount = to_string(tot_amount, "->>>,>>>,>>>,>>9.99")

    create_list()

    return generate_output()