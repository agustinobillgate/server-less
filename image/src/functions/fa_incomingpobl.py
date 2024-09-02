from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Fa_ordheader, L_lieferant, Mathis, Fa_op, Bediener, Fa_order

def fa_incomingpobl(fromdate:date, todate:date, searchby:int, devnote_no:str, po_no:str, supp_no:int):
    fa_ordheader = l_lieferant = mathis = fa_op = bediener = fa_order = None

    op_list = fa_ordheaderlist = None

    op_list_list, Op_list = create_model("Op_list", {"lscheinnr":str, "name":str, "location":str, "einzelpreis":decimal, "anzahl":int, "warenwert":decimal, "firma":str, "datum":date, "docu_nr":str, "lief_nr":int, "rec_id":int})
    fa_ordheaderlist_list, Fa_ordheaderlist = create_model_like(Fa_ordheader, {"create_name":str, "modify_name":str, "total_amount1":decimal})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal fa_ordheader, l_lieferant, mathis, fa_op, bediener, fa_order


        nonlocal op_list, fa_ordheaderlist
        nonlocal op_list_list, fa_ordheaderlist_list
        return {}

    def distinct_op():

        nonlocal fa_ordheader, l_lieferant, mathis, fa_op, bediener, fa_order


        nonlocal op_list, fa_ordheaderlist
        nonlocal op_list_list, fa_ordheaderlist_list

        temp_number:str = ""
        op_list_list.clear()

        if (devnote_no == "" and po_no == "" and supp_no == 0) or searchby == 0 or (searchby == 1 and devnote_no == "") or (searchby == 2 and po_no == "") or (searchby == 3 and supp_no == 0):

            fa_op_obj_list = []
            for fa_op, fa_ordheaderlist, l_lieferant, mathis in db_session.query(Fa_op, Fa_ordheaderlist, L_lieferant, Mathis).join(Fa_ordheaderlist,(Fa_ordheaderlist.order_nr == Fa_op.docu_nr)).join(L_lieferant,(L_lieferant.lief_nr == Fa_op.lief_nr)).join(Mathis,(Mathis.nr == Fa_op.nr)).filter(
                    (Fa_op.loeschflag <= 1) &  (Fa_op.warenwert > 0) &  (Fa_op.datum >= fromdate) &  (Fa_op.datum <= todate)).all():
                if fa_op._recid in fa_op_obj_list:
                    continue
                else:
                    fa_op_obj_list.append(fa_op._recid)

                if temp_number == "":
                    temp_number = fa_op.lscheinnr
                    create_op_list()
                else:

                    if temp_number != fa_op.lscheinnr:
                        temp_number = fa_op.lscheinnr
                        create_op_list()

        elif searchby == 1 and devnote_no != "":

            fa_op_obj_list = []
            for fa_op, fa_ordheaderlist, l_lieferant, mathis in db_session.query(Fa_op, Fa_ordheaderlist, L_lieferant, Mathis).join(Fa_ordheaderlist,(Fa_ordheaderlist.order_nr == Fa_op.docu_nr)).join(L_lieferant,(L_lieferant.lief_nr == Fa_op.lief_nr)).join(Mathis,(Mathis.nr == Fa_op.nr)).filter(
                    (Fa_op.loeschflag <= 1) &  (Fa_op.warenwert > 0) &  (Fa_op.datum >= fromdate) &  (Fa_op.datum <= todate) &  (func.lower(Fa_op.lscheinnr) == (devnote_no).lower())).all():
                if fa_op._recid in fa_op_obj_list:
                    continue
                else:
                    fa_op_obj_list.append(fa_op._recid)

                if temp_number == "":
                    temp_number = fa_op.lscheinnr
                    create_op_list()
                else:

                    if temp_number != fa_op.lscheinnr:
                        temp_number = fa_op.lscheinnr
                        create_op_list()


        elif searchby == 2 and po_no != "":

            fa_op_obj_list = []
            for fa_op, fa_ordheaderlist, l_lieferant, mathis in db_session.query(Fa_op, Fa_ordheaderlist, L_lieferant, Mathis).join(Fa_ordheaderlist,(func.lower(Fa_ordheaderlist.order_nr) == Fa_op.docu_nr) &  (func.lower(Fa_ordheaderlist.order_nr) == (po_no).lower())).join(L_lieferant,(L_lieferant.lief_nr == Fa_op.lief_nr)).join(Mathis,(Mathis.nr == Fa_op.nr)).filter(
                    (Fa_op.loeschflag <= 1) &  (Fa_op.warenwert > 0) &  (Fa_op.datum >= fromdate) &  (Fa_op.datum <= todate) &  (Fa_op.lscheinnr != "")).all():
                if fa_op._recid in fa_op_obj_list:
                    continue
                else:
                    fa_op_obj_list.append(fa_op._recid)

                if temp_number == "":
                    temp_number = fa_op.lscheinnr
                    create_op_list()
                else:

                    if temp_number != fa_op.lscheinnr:
                        temp_number = fa_op.lscheinnr
                        create_op_list()


        elif searchby == 3 and supp_no != 0:

            fa_op_obj_list = []
            for fa_op, fa_ordheaderlist, l_lieferant, mathis in db_session.query(Fa_op, Fa_ordheaderlist, L_lieferant, Mathis).join(Fa_ordheaderlist,(Fa_ordheaderlist.order_nr == Fa_op.docu_nr) &  (Fa_ordheaderlist.supplier_nr == supp_no)).join(L_lieferant,(L_lieferant.lief_nr == Fa_op.lief_nr)).join(Mathis,(Mathis.nr == Fa_op.nr)).filter(
                    (Fa_op.loeschflag <= 1) &  (Fa_op.warenwert > 0) &  (Fa_op.datum >= fromdate) &  (Fa_op.datum <= todate) &  (Fa_op.lscheinnr != "")).all():
                if fa_op._recid in fa_op_obj_list:
                    continue
                else:
                    fa_op_obj_list.append(fa_op._recid)

                if temp_number == "":
                    temp_number = fa_op.lscheinnr
                    create_op_list()
                    buffer_copy(fa_op, op_list)
                else:

                    if temp_number != fa_op.lscheinnr:
                        temp_number = fa_op.lscheinnr
                        create_op_list()


    def create_op_list():

        nonlocal fa_ordheader, l_lieferant, mathis, fa_op, bediener, fa_order


        nonlocal op_list, fa_ordheaderlist
        nonlocal op_list_list, fa_ordheaderlist_list


        op_list = Op_list()
        op_list_list.append(op_list)

        op_list.lscheinnr = fa_op.lscheinnr
        op_list.name = mathis.name
        op_list.location = mathis.location
        op_list.einzelpreis = fa_op.einzelpreis
        op_list.anzahl = fa_op.anzahl
        op_list.warenwert = fa_op.warenwert
        op_list.firma = l_lieferant.firma
        op_list.datum = fa_op.datum
        op_list.docu_nr = fa_op.docu_nr
        op_list.lief_nr = fa_op.lief_nr
        op_list.rec_id = fa_op._recid

    def create_faordheaderlist():

        nonlocal fa_ordheader, l_lieferant, mathis, fa_op, bediener, fa_order


        nonlocal op_list, fa_ordheaderlist
        nonlocal op_list_list, fa_ordheaderlist_list

        temp_create:str = ""
        temp_modify:str = ""
        total_amount:decimal = 0
        fa_ordheaderlist_list.clear()

        for fa_ordheader in db_session.query(Fa_ordheader).all():

            if fa_ordheader.created_by != "":

                bediener = db_session.query(Bediener).filter(
                        (Bediener.userinit == fa_ordheader.created_by)).first()

                if bediener:
                    temp_create = bediener.username
                else:
                    temp_create = ""
            else:
                temp_create = ""

            if fa_ordheader.modified_by != "":

                bediener = db_session.query(Bediener).filter(
                        (Bediener.userinit == fa_ordheader.modified_by)).first()

                if bediener:
                    temp_modify = bediener.username
                else:
                    temp_modify = ""
            else:
                temp_modify = ""

            for fa_order in db_session.query(Fa_order).filter(
                    (Fa_order.order_nr == fa_ordheader.order_nr)).all():
                total_amount = total_amount + fa_order.order_amount
            fa_ordheaderlist = Fa_ordheaderlist()
            fa_ordheaderlist_list.append(fa_ordheaderlist)

            buffer_copy(fa_ordheader, fa_ordheaderlist)
            fa_ordheaderlist.create_name = temp_create
            fa_ordheaderlist.modify_name = temp_modify
            fa_ordheaderlist.total_amount1 = total_amount


            temp_create = ""
            temp_modify = ""
            total_amount = 0

    create_faordheaderlist()
    distinct_op()

    return generate_output()