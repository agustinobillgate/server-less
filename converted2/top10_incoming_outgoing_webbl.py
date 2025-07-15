#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_artikel, L_lieferant, L_ophis, L_op, L_ophhis, L_lager, Gl_acct, Gl_department, L_ophdr

def top10_incoming_outgoing_webbl(from_date:date, to_date:date, from_grp:int, to_grp:int, store:int, sorttype:int):

    prepare_cache ([L_artikel, L_ophis, L_op])

    str_list_output_data = []
    tot_qty:int = 0
    qty:int = 0
    counter:int = 0
    unit_price:Decimal = to_decimal("0.0")
    tot_price:Decimal = to_decimal("0.0")
    tot_incoming:int = 0
    tot_outgoing:int = 0
    l_artikel = l_lieferant = l_ophis = l_op = l_ophhis = l_lager = gl_acct = gl_department = l_ophdr = None

    str_list = str_list_output = None

    str_list_data, Str_list = create_model("Str_list", {"artnr_no":int, "artikel_name":string, "qty":Decimal, "unit_price":Decimal, "tot_price":Decimal, "tot_incoming":Decimal, "tot_outgoing":Decimal})
    str_list_output_data, Str_list_output = create_model("Str_list_output", {"artnr_no":int, "artikel_name":string, "qty":Decimal, "unit_price":Decimal, "tot_price":Decimal, "turnover":Decimal, "tot_outgoing":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal str_list_output_data, tot_qty, qty, counter, unit_price, tot_price, tot_incoming, tot_outgoing, l_artikel, l_lieferant, l_ophis, l_op, l_ophhis, l_lager, gl_acct, gl_department, l_ophdr
        nonlocal from_date, to_date, from_grp, to_grp, store, sorttype


        nonlocal str_list, str_list_output
        nonlocal str_list_data, str_list_output_data

        return {"str-list-output": str_list_output_data}

    def incoming_procedure():

        nonlocal str_list_output_data, tot_qty, qty, counter, unit_price, tot_price, tot_incoming, tot_outgoing, l_artikel, l_lieferant, l_ophis, l_op, l_ophhis, l_lager, gl_acct, gl_department, l_ophdr
        nonlocal from_date, to_date, from_grp, to_grp, store, sorttype


        nonlocal str_list, str_list_output
        nonlocal str_list_data, str_list_output_data

        if store == 0:
            tot_qty = 0
            qty = 0
            tot_outgoing = 0
            tot_price =  to_decimal("0")
            tot_incoming = 0
            str_list_data.clear()

            l_ophis_obj_list = {}
            for l_ophis, l_artikel, l_lieferant in db_session.query(L_ophis, L_artikel, L_lieferant).join(L_artikel,(L_artikel.artnr == L_ophis.artnr) & (L_artikel.endkum >= from_grp) & (L_artikel.endkum <= to_grp)).join(L_lieferant,(L_lieferant.lief_nr == L_ophis.lief_nr)).filter(
                     (L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & (L_ophis.lief_nr > 0) & (L_ophis.op_art == 1) & (L_ophis.anzahl != 0) & (not_ (length(L_ophis.fibukonto) > 8) & (substring(L_ophis.fibukonto, length(L_ophis.fibukonto) - length(("CANCELLED").lower() ) + 1 - 1, length(L_ophis.fibukonto)) == ("CANCELLED").lower()))).order_by(L_lieferant.firma, L_ophis.datum, L_artikel.bezeich).all():
                if l_ophis_obj_list.get(l_ophis._recid):
                    continue
                else:
                    l_ophis_obj_list[l_ophis._recid] = True

                str_list = query(str_list_data, filters=(lambda str_list: str_list.artnr_no == l_ophis.artnr), first=True)

                if not str_list:
                    str_list = Str_list()
                    str_list_data.append(str_list)

                    str_list.artnr_no = l_ophis.artnr
                    str_list.artikel_name = l_artikel.bezeich
                    str_list.qty =  to_decimal(l_ophis.anzahl)
                    str_list.unit_price =  to_decimal(l_ophis.einzelpreis)
                    str_list.tot_price =  to_decimal(l_ophis.einzelpreis) * to_decimal(l_ophis.anzahl)
                    str_list.tot_incoming =  to_decimal("1")


                else:
                    str_list.qty =  to_decimal(str_list.qty) + to_decimal(l_ophis.anzahl)
                    str_list.tot_price =  to_decimal(str_list.tot_price) + to_decimal((l_ophis.einzelpreis) * to_decimal(l_ophis.anzahl))
                    str_list.tot_incoming =  to_decimal(str_list.tot_incoming) + to_decimal("1")

            l_op_obj_list = {}
            for l_op, l_artikel, l_lieferant in db_session.query(L_op, L_artikel, L_lieferant).join(L_artikel,(L_artikel.artnr == L_op.artnr) & (L_artikel.endkum >= from_grp) & (L_artikel.endkum <= to_grp)).join(L_lieferant,(L_lieferant.lief_nr == L_op.lief_nr)).filter(
                     (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.lief_nr > 0) & (L_op.loeschflag <= 1) & (L_op.op_art == 1)).order_by(L_op.artnr, L_lieferant.firma, L_op.datum, L_artikel.bezeich).all():
                if l_op_obj_list.get(l_op._recid):
                    continue
                else:
                    l_op_obj_list[l_op._recid] = True

                str_list = query(str_list_data, filters=(lambda str_list: str_list.artnr_no == l_op.artnr), first=True)

                if not str_list:
                    str_list = Str_list()
                    str_list_data.append(str_list)

                    str_list.artnr_no = l_op.artnr
                    str_list.artikel_name = l_artikel.bezeich
                    str_list.qty =  to_decimal(l_op.anzahl)
                    str_list.unit_price =  to_decimal(l_op.einzelpreis)
                    str_list.tot_price =  to_decimal(l_op.einzelpreis) * to_decimal(l_op.anzahl)
                    str_list.tot_incoming =  to_decimal("1")


                else:
                    str_list.qty =  to_decimal(str_list.qty) + to_decimal(l_op.anzahl)
                    str_list.tot_price =  to_decimal(str_list.tot_price) + to_decimal((l_op.einzelpreis) * to_decimal(l_op.anzahl))
                    str_list.tot_incoming =  to_decimal(str_list.tot_incoming) + to_decimal("1")
            str_list_output_data.clear()

            for str_list in query(str_list_data, sort_by=[("tot_incoming",True)]):
                counter = counter + 1
                str_list_output = Str_list_output()
                str_list_output_data.append(str_list_output)

                str_list_output.artnr_no = str_list.artnr_no
                str_list_output.artikel_name = str_list.artikel_name
                str_list_output.qty =  to_decimal(str_list.qty)
                str_list_output.unit_price =  to_decimal(str_list.tot_price) / to_decimal(str_list.tot_incoming)
                str_list_output.tot_price =  to_decimal(str_list.tot_price)
                str_list_output.turnover =  to_decimal(str_list.tot_incoming)
                tot_qty = tot_qty + str_list.qty


                tot_incoming = tot_incoming + str_list.tot_incoming

                if counter == 100:
                    break
            str_list_output = Str_list_output()
            str_list_output_data.append(str_list_output)

            str_list_output.artnr_no = 0
            str_list_output.artikel_name = "TOTAL : "
            str_list_output.qty =  to_decimal(tot_qty)
            str_list_output.unit_price =  to_decimal("0")
            str_list_output.tot_price =  to_decimal("0")
            str_list_output.turnover =  to_decimal(tot_incoming)


        else:
            tot_qty = 0
            qty = 0
            tot_outgoing = 0
            tot_price =  to_decimal("0")
            tot_incoming = 0
            str_list_data.clear()

            l_ophis_obj_list = {}
            for l_ophis, l_artikel, l_lieferant in db_session.query(L_ophis, L_artikel, L_lieferant).join(L_artikel,(L_artikel.artnr == L_ophis.artnr) & (L_artikel.endkum >= from_grp) & (L_artikel.endkum <= to_grp)).join(L_lieferant,(L_lieferant.lief_nr == L_ophis.lief_nr)).filter(
                     (L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & (L_ophis.lief_nr > 0) & (L_ophis.op_art == 1) & (L_ophis.anzahl != 0) & (L_ophis.lager_nr == store) & (not_ (length(L_ophis.fibukonto) > 8) & (substring(L_ophis.fibukonto, length(L_ophis.fibukonto) - length(("CANCELLED").lower() ) + 1 - 1, length(L_ophis.fibukonto)) == ("CANCELLED").lower()))).order_by(L_lieferant.firma, L_ophis.datum, L_artikel.bezeich).all():
                if l_ophis_obj_list.get(l_ophis._recid):
                    continue
                else:
                    l_ophis_obj_list[l_ophis._recid] = True

                str_list = query(str_list_data, filters=(lambda str_list: str_list.artnr_no == l_ophis.artnr), first=True)

                if not str_list:
                    str_list = Str_list()
                    str_list_data.append(str_list)

                    str_list.artnr_no = l_ophis.artnr
                    str_list.artikel_name = l_artikel.bezeich
                    str_list.qty =  to_decimal(l_ophis.anzahl)
                    str_list.unit_price =  to_decimal(l_ophis.einzelpreis)
                    str_list.tot_price =  to_decimal(l_ophis.einzelpreis) * to_decimal(l_ophis.anzahl)
                    str_list.tot_incoming =  to_decimal("1")


                else:
                    str_list.qty =  to_decimal(str_list.qty) + to_decimal(l_ophis.anzahl)
                    str_list.tot_price =  to_decimal(str_list.tot_price) + to_decimal((l_ophis.einzelpreis) * to_decimal(l_ophis.anzahl))
                    str_list.tot_incoming =  to_decimal(str_list.tot_incoming) + to_decimal("1")

            l_op_obj_list = {}
            for l_op, l_artikel, l_lieferant in db_session.query(L_op, L_artikel, L_lieferant).join(L_artikel,(L_artikel.artnr == L_op.artnr) & (L_artikel.endkum >= from_grp) & (L_artikel.endkum <= to_grp)).join(L_lieferant,(L_lieferant.lief_nr == L_op.lief_nr)).filter(
                     (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.lief_nr > 0) & (L_op.loeschflag <= 1) & (L_op.op_art == 1) & (L_op.lager_nr == store)).order_by(L_op.artnr, L_lieferant.firma, L_op.datum, L_artikel.bezeich).all():
                if l_op_obj_list.get(l_op._recid):
                    continue
                else:
                    l_op_obj_list[l_op._recid] = True

                str_list = query(str_list_data, filters=(lambda str_list: str_list.artnr_no == l_op.artnr), first=True)

                if not str_list:
                    str_list = Str_list()
                    str_list_data.append(str_list)

                    str_list.artnr_no = l_op.artnr
                    str_list.artikel_name = l_artikel.bezeich
                    str_list.qty =  to_decimal(l_op.anzahl)
                    str_list.unit_price =  to_decimal(l_op.einzelpreis)
                    str_list.tot_price =  to_decimal(l_op.einzelpreis) * to_decimal(l_op.anzahl)
                    str_list.tot_incoming =  to_decimal("1")


                else:
                    str_list.qty =  to_decimal(str_list.qty) + to_decimal(l_op.anzahl)
                    str_list.tot_price =  to_decimal(str_list.tot_price) + to_decimal((l_op.einzelpreis) * to_decimal(l_op.anzahl))
                    str_list.tot_incoming =  to_decimal(str_list.tot_incoming) + to_decimal("1")
            str_list_output_data.clear()

            for str_list in query(str_list_data, sort_by=[("tot_incoming",True)]):
                counter = counter + 1
                str_list_output = Str_list_output()
                str_list_output_data.append(str_list_output)

                str_list_output.artnr_no = str_list.artnr_no
                str_list_output.artikel_name = str_list.artikel_name
                str_list_output.qty =  to_decimal(str_list.qty)
                str_list_output.unit_price =  to_decimal(str_list.tot_price) / to_decimal(str_list.tot_incoming)
                str_list_output.tot_price =  to_decimal(str_list.tot_price)
                str_list_output.turnover =  to_decimal(str_list.tot_incoming)
                tot_qty = tot_qty + str_list.qty


                tot_incoming = tot_incoming + str_list.tot_incoming

                if counter == 100:
                    break
            str_list_output = Str_list_output()
            str_list_output_data.append(str_list_output)

            str_list_output.artnr_no = 0
            str_list_output.artikel_name = "TOTAL : "
            str_list_output.qty =  to_decimal(tot_qty)
            str_list_output.unit_price =  to_decimal("0")
            str_list_output.tot_price =  to_decimal("0")
            str_list_output.turnover =  to_decimal(tot_incoming)


    def outgoing_procedure():

        nonlocal str_list_output_data, tot_qty, qty, counter, unit_price, tot_price, tot_incoming, tot_outgoing, l_artikel, l_lieferant, l_ophis, l_op, l_ophhis, l_lager, gl_acct, gl_department, l_ophdr
        nonlocal from_date, to_date, from_grp, to_grp, store, sorttype


        nonlocal str_list, str_list_output
        nonlocal str_list_data, str_list_output_data

        if store == 0:
            tot_qty = 0
            qty = 0
            tot_outgoing = 0
            tot_price =  to_decimal("0")
            tot_incoming = 0
            str_list_data.clear()

            l_ophis_obj_list = {}
            for l_ophis, l_ophhis, l_lager, gl_acct, gl_department, l_artikel in db_session.query(L_ophis, L_ophhis, L_lager, Gl_acct, Gl_department, L_artikel).join(L_ophhis,(L_ophhis.op_typ == ("STT").lower()) & (L_ophhis.lscheinnr == L_ophis.lscheinnr) & (L_ophhis.fibukonto != "")).join(L_lager,(L_lager.lager_nr == L_ophis.lager_nr)).join(Gl_acct,(Gl_acct.fibukonto == L_ophhis.fibukonto)).join(Gl_department,(Gl_department.nr == Gl_acct.deptnr)).join(L_artikel,(L_artikel.artnr == L_ophis.artnr) & (L_artikel.endkum >= from_grp) & (L_artikel.endkum <= to_grp)).filter(
                     (L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & (L_ophis.anzahl != 0) & (L_ophis.op_art == 3)).order_by(L_ophis.lscheinnr, L_ophis.artnr).all():
                if l_ophis_obj_list.get(l_ophis._recid):
                    continue
                else:
                    l_ophis_obj_list[l_ophis._recid] = True

                str_list = query(str_list_data, filters=(lambda str_list: str_list.artnr_no == l_ophis.artnr), first=True)

                if not str_list:
                    str_list = Str_list()
                    str_list_data.append(str_list)

                    str_list.artnr_no = l_ophis.artnr
                    str_list.artikel_name = l_artikel.bezeich
                    str_list.qty =  to_decimal(l_ophis.anzahl)
                    str_list.unit_price =  to_decimal(l_ophis.einzelpreis)
                    str_list.tot_price =  to_decimal(l_ophis.einzelpreis) * to_decimal(l_ophis.anzahl)
                    str_list.tot_outgoing =  to_decimal("1")


                else:
                    str_list.qty =  to_decimal(str_list.qty) + to_decimal(l_ophis.anzahl)
                    str_list.tot_price =  to_decimal(str_list.tot_price) + to_decimal((l_ophis.einzelpreis) * to_decimal(l_ophis.anzahl))
                    str_list.tot_outgoing =  to_decimal(str_list.tot_outgoing) + to_decimal("1")

            l_op_obj_list = {}
            for l_op, l_ophdr, gl_acct, l_artikel in db_session.query(L_op, L_ophdr, Gl_acct, L_artikel).join(L_ophdr,(L_ophdr.op_typ == ("STT").lower()) & (L_ophdr.lscheinnr == L_op.lscheinnr) & (L_ophdr.fibukonto != "")).join(Gl_acct,(Gl_acct.fibukonto == L_op.stornogrund)).join(L_artikel,(L_artikel.artnr == L_op.artnr) & (L_artikel.endkum >= from_grp) & (L_artikel.endkum <= to_grp)).filter(
                     (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.anzahl != 0) & (L_op.op_art == 3) & (L_op.loeschflag <= 1)).order_by(L_op.lscheinnr, L_op.artnr).all():
                if l_op_obj_list.get(l_op._recid):
                    continue
                else:
                    l_op_obj_list[l_op._recid] = True

                str_list = query(str_list_data, filters=(lambda str_list: str_list.artnr_no == l_op.artnr), first=True)

                if not str_list:
                    str_list = Str_list()
                    str_list_data.append(str_list)

                    str_list.artnr_no = l_op.artnr
                    str_list.artikel_name = l_artikel.bezeich
                    str_list.qty =  to_decimal(l_op.anzahl)
                    str_list.unit_price =  to_decimal(l_op.einzelpreis)
                    str_list.tot_price =  to_decimal(l_op.einzelpreis) * to_decimal(l_op.anzahl)
                    str_list.tot_outgoing =  to_decimal("1")


                else:
                    str_list.qty =  to_decimal(str_list.qty) + to_decimal(l_op.anzahl)
                    str_list.tot_price =  to_decimal(str_list.tot_price) + to_decimal((l_op.einzelpreis) * to_decimal(l_op.anzahl))
                    str_list.tot_outgoing =  to_decimal(str_list.tot_outgoing) + to_decimal("1")
            str_list_output_data.clear()

            for str_list in query(str_list_data, sort_by=[("tot_outgoing",True)]):
                counter = counter + 1
                str_list_output = Str_list_output()
                str_list_output_data.append(str_list_output)

                str_list_output.artnr_no = str_list.artnr_no
                str_list_output.artikel_name = str_list.artikel_name
                str_list_output.qty =  to_decimal(str_list.qty)
                str_list_output.unit_price =  to_decimal(str_list.tot_price) / to_decimal(str_list.tot_outgoing)
                str_list_output.tot_price =  to_decimal(str_list.tot_price)
                str_list_output.turnover =  to_decimal(str_list.tot_outgoing)
                tot_qty = tot_qty + str_list.qty
                tot_outgoing = tot_outgoing + str_list.tot_outgoing

                if counter == 100:
                    break
            str_list_output = Str_list_output()
            str_list_output_data.append(str_list_output)

            str_list_output.artnr_no = 0
            str_list_output.artikel_name = "TOTAL"
            str_list_output.qty =  to_decimal(tot_qty)
            str_list_output.unit_price =  to_decimal("0")
            str_list_output.tot_price =  to_decimal("0")
            str_list_output.turnover =  to_decimal(tot_outgoing)


        else:
            tot_qty = 0
            qty = 0
            tot_outgoing = 0
            tot_price =  to_decimal("0")
            tot_incoming = 0
            str_list_data.clear()

            l_ophis_obj_list = {}
            for l_ophis, l_ophhis, gl_acct, gl_department, l_artikel in db_session.query(L_ophis, L_ophhis, Gl_acct, Gl_department, L_artikel).join(L_ophhis,(L_ophhis.op_typ == ("STT").lower()) & (L_ophhis.lscheinnr == L_ophis.lscheinnr) & (L_ophhis.fibukonto != "") & (L_ophis.lager_nr == store)).join(Gl_acct,(Gl_acct.fibukonto == L_ophhis.fibukonto)).join(Gl_department,(Gl_department.nr == Gl_acct.deptnr)).join(L_artikel,(L_artikel.artnr == L_ophis.artnr) & (L_artikel.endkum >= from_grp) & (L_artikel.endkum <= to_grp)).filter(
                     (L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & (L_ophis.anzahl != 0) & (L_ophis.op_art == 3)).order_by(L_ophis.lscheinnr, L_ophis.artnr).all():
                if l_ophis_obj_list.get(l_ophis._recid):
                    continue
                else:
                    l_ophis_obj_list[l_ophis._recid] = True

                str_list = query(str_list_data, filters=(lambda str_list: str_list.artnr_no == l_ophis.artnr), first=True)

                if not str_list:
                    str_list = Str_list()
                    str_list_data.append(str_list)

                    str_list.artnr_no = l_ophis.artnr
                    str_list.artikel_name = l_artikel.bezeich
                    str_list.qty =  to_decimal(l_ophis.anzahl)
                    str_list.unit_price =  to_decimal(l_ophis.einzelpreis)
                    str_list.tot_price =  to_decimal(l_ophis.einzelpreis) * to_decimal(l_ophis.anzahl)
                    str_list.tot_outgoing =  to_decimal("1")


                else:
                    str_list.qty =  to_decimal(str_list.qty) + to_decimal(l_ophis.anzahl)
                    str_list.tot_price =  to_decimal(str_list.tot_price) + to_decimal((l_ophis.einzelpreis) * to_decimal(l_ophis.anzahl))
                    str_list.tot_outgoing =  to_decimal(str_list.tot_outgoing) + to_decimal("1")

            l_op_obj_list = {}
            for l_op, l_ophdr, gl_acct, l_artikel in db_session.query(L_op, L_ophdr, Gl_acct, L_artikel).join(L_ophdr,(L_ophdr.op_typ == ("STT").lower()) & (L_ophdr.lscheinnr == L_op.lscheinnr) & (L_ophdr.fibukonto != "")).join(Gl_acct,(Gl_acct.fibukonto == L_op.stornogrund)).join(L_artikel,(L_artikel.artnr == L_op.artnr) & (L_artikel.endkum >= from_grp) & (L_artikel.endkum <= to_grp)).filter(
                     (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.anzahl != 0) & (L_op.op_art == 3) & (L_op.loeschflag <= 1) & (L_op.lager_nr == store)).order_by(L_op.lscheinnr, L_op.artnr).all():
                if l_op_obj_list.get(l_op._recid):
                    continue
                else:
                    l_op_obj_list[l_op._recid] = True

                str_list = query(str_list_data, filters=(lambda str_list: str_list.artnr_no == l_op.artnr), first=True)

                if not str_list:
                    str_list = Str_list()
                    str_list_data.append(str_list)

                    str_list.artnr_no = l_op.artnr
                    str_list.artikel_name = l_artikel.bezeich
                    str_list.qty =  to_decimal(l_op.anzahl)
                    str_list.unit_price =  to_decimal(l_op.einzelpreis)
                    str_list.tot_price =  to_decimal(l_op.einzelpreis) * to_decimal(l_op.anzahl)
                    str_list.tot_outgoing =  to_decimal("1")


                else:
                    str_list.qty =  to_decimal(str_list.qty) + to_decimal(l_op.anzahl)
                    str_list.tot_price =  to_decimal(str_list.tot_price) + to_decimal((l_op.einzelpreis) * to_decimal(l_op.anzahl))
                    str_list.tot_outgoing =  to_decimal(str_list.tot_outgoing) + to_decimal("1")
            str_list_output_data.clear()

            for str_list in query(str_list_data, sort_by=[("tot_outgoing",True)]):
                counter = counter + 1
                str_list_output = Str_list_output()
                str_list_output_data.append(str_list_output)

                str_list_output.artnr_no = str_list.artnr_no
                str_list_output.artikel_name = str_list.artikel_name
                str_list_output.qty =  to_decimal(str_list.qty)
                str_list_output.unit_price =  to_decimal(str_list.tot_price) / to_decimal(str_list.tot_outgoing)
                str_list_output.tot_price =  to_decimal(str_list.tot_price)
                str_list_output.turnover =  to_decimal(str_list.tot_outgoing)
                tot_qty = tot_qty + str_list.qty
                tot_outgoing = tot_outgoing + str_list.tot_outgoing

                if counter == 100:
                    break
            str_list_output = Str_list_output()
            str_list_output_data.append(str_list_output)

            str_list_output.artnr_no = 0
            str_list_output.artikel_name = "TOTAL"
            str_list_output.qty =  to_decimal(tot_qty)
            str_list_output.unit_price =  to_decimal("0")
            str_list_output.tot_price =  to_decimal("0")
            str_list_output.turnover =  to_decimal(tot_outgoing)

    if sorttype == 0:
        incoming_procedure()
    else:
        outgoing_procedure()

    return generate_output()