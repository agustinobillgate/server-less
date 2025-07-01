#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_artikel, L_lieferant, L_op, L_untergrup, L_ophis

payload_list_list, Payload_list = create_model("Payload_list", {"frm_grp":int, "to_grp":int, "storage_no":int, "frm_date":date, "to_date":date, "case_type":int})

def incoming_print_summary_by_date_webbl(payload_list_list:[Payload_list]):

    prepare_cache ([L_op, L_ophis])

    print_list_list = []
    frm_grp:int = 0
    to_grp:int = 0
    storage_no:int = 0
    frm_date:date = None
    to_date:date = None
    tot_amount:Decimal = to_decimal("0.0")
    temp_date:date = None
    l_artikel = l_lieferant = l_op = l_untergrup = l_ophis = None

    payload_list = print_list = None

    print_list_list, Print_list = create_model("Print_list", {"datum":date, "t_amount":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal print_list_list, frm_grp, to_grp, storage_no, frm_date, to_date, tot_amount, temp_date, l_artikel, l_lieferant, l_op, l_untergrup, l_ophis


        nonlocal payload_list, print_list
        nonlocal print_list_list

        return {"print-list": print_list_list}


    payload_list = query(payload_list_list, first=True)

    if payload_list:
        frm_grp = payload_list.frm_grp
        to_grp = payload_list.to_grp
        storage_no = payload_list.storage_no
        frm_date = payload_list.frm_date
        to_date = payload_list.to_date

        if case_type == 1:

            if storage_no == 0:

                l_op_obj_list = {}
                for l_op, l_artikel, l_lieferant in db_session.query(L_op, L_artikel, L_lieferant).join(L_artikel,(L_artikel.artnr == L_op.artnr) & (L_artikel.endkum >= frm_grp) & (L_artikel.endkum <= to_grp)).join(L_lieferant,(L_lieferant.lief_nr == L_op.lief_nr)).filter(
                         (L_op.datum >= frm_date) & (L_op.datum <= to_date) & (L_op.lief_nr > 0) & (L_op.loeschflag <= 1) & (L_op.op_art == 1)).order_by(L_op.datum).all():
                    if l_op_obj_list.get(l_op._recid):
                        continue
                    else:
                        l_op_obj_list[l_op._recid] = True

                    if temp_date != l_op.datum:
                        print_list = Print_list()
                        print_list_list.append(print_list)

                        print_list.datum = l_op.datum
                        temp_date = l_op.datum
                    tot_amount =  to_decimal(tot_amount) + to_decimal(l_op.warenwert)
                    print_list.t_amount =  to_decimal(print_list.t_amount) + to_decimal(l_op.warenwert)
            else:

                l_op_obj_list = {}
                for l_op, l_artikel, l_lieferant in db_session.query(L_op, L_artikel, L_lieferant).join(L_artikel,(L_artikel.artnr == L_op.artnr) & (L_artikel.endkum >= frm_grp) & (L_artikel.endkum <= to_grp)).join(L_lieferant,(L_lieferant.lief_nr == L_op.lief_nr)).filter(
                         (L_op.datum >= frm_date) & (L_op.datum <= to_date) & (L_op.lief_nr > 0) & (L_op.loeschflag <= 1) & (L_op.op_art == 1) & (L_op.lager_nr == storage_no)).order_by(L_op.datum).all():
                    if l_op_obj_list.get(l_op._recid):
                        continue
                    else:
                        l_op_obj_list[l_op._recid] = True

                    if temp_date != l_op.datum:
                        print_list = Print_list()
                        print_list_list.append(print_list)

                        print_list.datum = l_op.datum
                        temp_date = l_op.datum
                    tot_amount =  to_decimal(tot_amount) + to_decimal(l_op.warenwert)
                    print_list.t_amount =  to_decimal(print_list.t_amount) + to_decimal(l_op.warenwert)
            print_list = Print_list()
            print_list_list.append(print_list)

            print_list.datum = None
            print_list.t_amount =  to_decimal(tot_amount)

        elif case_type == 2:

            if storage_no == 0:

                l_ophis_obj_list = {}
                for l_ophis, l_artikel, l_untergrup in db_session.query(L_ophis, L_artikel, L_untergrup).join(L_artikel,(L_artikel.artnr == L_ophis.artnr) & (L_artikel.endkum >= frm_grp) & (L_artikel.endkum <= to_grp)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                         (L_ophis.datum >= frm_date) & (L_ophis.datum <= to_date) & (L_ophis.lief_nr > 0) & (L_ophis.op_art == 1) & (L_ophis.anzahl != 0) & (not_ (length(L_ophis.fibukonto) > 8) & (substring(L_ophis.fibukonto, length(L_ophis.fibukonto) - length(("CANCELLED").lower() ) + 1 - 1, length(L_ophis.fibukonto)) == ("CANCELLED").lower()))).order_by(L_ophis.datum).all():
                    if l_ophis_obj_list.get(l_ophis._recid):
                        continue
                    else:
                        l_ophis_obj_list[l_ophis._recid] = True

                    if temp_date != l_ophis.datum:
                        print_list = Print_list()
                        print_list_list.append(print_list)

                        print_list.datum = l_ophis.datum
                        temp_date = l_ophis.datum
                    tot_amount =  to_decimal(tot_amount) + to_decimal(l_ophis.warenwert)
                    print_list.t_amount =  to_decimal(print_list.t_amount) + to_decimal(l_ophis.warenwert)
            else:

                l_ophis_obj_list = {}
                for l_ophis, l_artikel, l_untergrup in db_session.query(L_ophis, L_artikel, L_untergrup).join(L_artikel,(L_artikel.artnr == L_ophis.artnr) & (L_artikel.endkum >= frm_grp) & (L_artikel.endkum <= to_grp)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                         (L_ophis.datum >= frm_date) & (L_ophis.datum <= to_date) & (L_ophis.lief_nr > 0) & (L_ophis.op_art == 1) & (L_ophis.anzahl != 0) & (L_ophis.lager_nr == storage_no) & (not_ (length(L_ophis.fibukonto) > 8) & (substring(L_ophis.fibukonto, length(L_ophis.fibukonto) - length(("CANCELLED").lower() ) + 1 - 1, length(L_ophis.fibukonto)) == ("CANCELLED").lower()))).order_by(L_ophis.datum).all():
                    if l_ophis_obj_list.get(l_ophis._recid):
                        continue
                    else:
                        l_ophis_obj_list[l_ophis._recid] = True

                    if temp_date != l_ophis.datum:
                        print_list = Print_list()
                        print_list_list.append(print_list)

                        print_list.datum = l_ophis.datum
                        temp_date = l_ophis.datum
                    tot_amount =  to_decimal(tot_amount) + to_decimal(l_ophis.warenwert)
                    print_list.t_amount =  to_decimal(print_list.t_amount) + to_decimal(l_ophis.warenwert)
            print_list = Print_list()
            print_list_list.append(print_list)

            print_list.datum = None
            print_list.t_amount =  to_decimal(tot_amount)

    return generate_output()