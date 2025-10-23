# using conversion tools version: 1.0.0.117

"""_yusufwijasena_ 10/10/2025

    TICKET ID: 79EBDE
    ISSUE:  - Fix variabel = None
            - Fix python indentation
            - add type:ignore to model Op_list & Fa_ordheader, avoid warning cannot assign attribute
            - Change condition if == "" to if = None
            - Change confition if != "" to if {condition}
"""

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Fa_ordheader, L_lieferant, Mathis, Fa_op, Bediener, Fa_order


def fa_incomingpobl(fromdate: date, todate: date, searchby: int, devnote_no: string, po_no: string, supp_no: int):

    prepare_cache([L_lieferant, Mathis, Fa_op, Bediener, Fa_order])

    op_list_data = []
    fa_ordheader = l_lieferant = mathis = fa_op = bediener = fa_order = None

    op_list = fa_ordheaderlist = None

    op_list_data, Op_list = create_model("Op_list", {"lscheinnr": string, "name": string, "location": string, "einzelpreis": Decimal, "anzahl": int, "warenwert": Decimal,
                                         "firma": string, "datum": date, "docu_nr": string, "lief_nr": int, "order_date": date, "createdby": string, "release_date": date, "order_amount": Decimal, "rec_id": int})
    fa_ordheaderlist_data, Fa_ordheaderlist = create_model_like(
        Fa_ordheader, {"create_name": string, "modify_name": string, "total_amount1": Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal op_list_data, fa_ordheader, l_lieferant, mathis, fa_op, bediener, fa_order
        nonlocal fromdate, todate, searchby, devnote_no, po_no, supp_no

        nonlocal op_list, fa_ordheaderlist
        nonlocal op_list_data, fa_ordheaderlist_data

        return {"op-list": op_list_data}

    def distinct_op():

        nonlocal op_list_data, fa_ordheader, l_lieferant, mathis, fa_op, bediener, fa_order
        nonlocal fromdate, todate, searchby, devnote_no, po_no, supp_no

        nonlocal op_list, fa_ordheaderlist
        nonlocal op_list_data, fa_ordheaderlist_data

        temp_number: string
        op_list_data.clear()

        if (devnote_no == None and po_no == None and supp_no == 0) or searchby == 0 or (searchby == 1 and devnote_no == None) or (searchby == 2 and po_no == None) or (searchby == 3 and supp_no == 0):

            fa_op_obj_list = {}
            for fa_op, l_lieferant, mathis in db_session.query(Fa_op, L_lieferant, Mathis).join(L_lieferant, (L_lieferant.lief_nr == Fa_op.lief_nr)).join(Mathis, (Mathis.nr == Fa_op.nr)).filter(
                    (Fa_op.loeschflag <= 1) & (Fa_op.warenwert > 0) & (Fa_op.datum >= fromdate) & (Fa_op.datum <= todate)).order_by(Fa_op.docu_nr, Fa_op.lscheinnr, Fa_op.zeit).all():
                fa_ordheaderlist = query(fa_ordheaderlist_data, (
                    lambda fa_ordheaderlist: fa_ordheaderlist.order_nr == fa_op.docu_nr), first=True)  # type: ignore
                if not fa_ordheaderlist:
                    continue

                if fa_op_obj_list.get(fa_op._recid):
                    continue
                else:
                    fa_op_obj_list[fa_op._recid] = True

                create_op_list()

        elif searchby == 1 and devnote_no:

            fa_op_obj_list = {}
            for fa_op, l_lieferant, mathis in db_session.query(Fa_op, L_lieferant, Mathis).join(L_lieferant, (L_lieferant.lief_nr == Fa_op.lief_nr)).join(Mathis, (Mathis.nr == Fa_op.nr)).filter(
                    (Fa_op.loeschflag <= 1) & (Fa_op.warenwert > 0) & (Fa_op.datum >= fromdate) & (Fa_op.datum <= todate) & (Fa_op.lscheinnr == (devnote_no).lower())).order_by(Fa_op.docu_nr, Fa_op.lscheinnr, Fa_op.zeit).all():
                fa_ordheaderlist = query(fa_ordheaderlist_data, (
                    lambda fa_ordheaderlist: fa_ordheaderlist.order_nr == fa_op.docu_nr), first=True)  # type: ignore
                if not fa_ordheaderlist:
                    continue

                if fa_op_obj_list.get(fa_op._recid):
                    continue
                else:
                    fa_op_obj_list[fa_op._recid] = True

                create_op_list()

        elif searchby == 2 and po_no:

            fa_op_obj_list = {}
            for fa_op, l_lieferant, mathis in db_session.query(Fa_op, L_lieferant, Mathis).join(L_lieferant, (L_lieferant.lief_nr == Fa_op.lief_nr)).join(Mathis, (Mathis.nr == Fa_op.nr)).filter(
                    (Fa_op.loeschflag <= 1) & (Fa_op.warenwert > 0) & (Fa_op.datum >= fromdate) & (Fa_op.datum <= todate) & (Fa_op.lscheinnr != "")).order_by(Fa_op.docu_nr, Fa_op.lscheinnr, Fa_op.zeit).all():
                fa_ordheaderlist = query(fa_ordheaderlist_data, (lambda fa_ordheaderlist: fa_ordheaderlist.order_nr.lower(
                    # type: ignore
                ) == fa_op.docu_nr and fa_ordheaderlist.order_nr.lower() == (po_no).lower()), first=True)  # type: ignore
                if not fa_ordheaderlist:
                    continue

                if fa_op_obj_list.get(fa_op._recid):
                    continue
                else:
                    fa_op_obj_list[fa_op._recid] = True

                create_op_list()

        elif searchby == 3 and supp_no != 0:

            fa_op_obj_list = {}
            for fa_op, l_lieferant, mathis in db_session.query(Fa_op, L_lieferant, Mathis).join(L_lieferant, (L_lieferant.lief_nr == Fa_op.lief_nr)).join(Mathis, (Mathis.nr == Fa_op.nr)).filter(
                    (Fa_op.loeschflag <= 1) & (Fa_op.warenwert > 0) & (Fa_op.datum >= fromdate) & (Fa_op.datum <= todate) & (Fa_op.lscheinnr != "")).order_by(Fa_op.docu_nr, Fa_op.lscheinnr, Fa_op.zeit).all():
                fa_ordheaderlist = query(fa_ordheaderlist_data, (lambda fa_ordheaderlist: fa_ordheaderlist.order_nr ==
                                         fa_op.docu_nr and fa_ordheaderlist.supplier_nr == supp_no), first=True)  # type: ignore
                if not fa_ordheaderlist:
                    continue

                if fa_op_obj_list.get(fa_op._recid):
                    continue
                else:
                    fa_op_obj_list[fa_op._recid] = True

                create_op_list()

    def create_op_list():

        nonlocal op_list_data, fa_ordheader, l_lieferant, mathis, fa_op, bediener, fa_order
        nonlocal fromdate, todate, searchby, devnote_no, po_no, supp_no

        nonlocal op_list, fa_ordheaderlist
        nonlocal op_list_data, fa_ordheaderlist_data

        op_list = Op_list()
        op_list_data.append(op_list)

        op_list.lscheinnr = fa_op.lscheinnr  # type: ignore
        op_list.name = mathis.name  # type: ignore
        op_list.location = mathis.location  # type: ignore
        op_list.einzelpreis = to_decimal(fa_op.einzelpreis)  # type: ignore
        op_list.anzahl = fa_op.anzahl  # type: ignore
        op_list.warenwert = to_decimal(fa_op.warenwert)  # type: ignore
        op_list.firma = l_lieferant.firma  # type: ignore
        op_list.datum = fa_op.datum  # type: ignore
        op_list.docu_nr = fa_op.docu_nr  # type: ignore
        op_list.lief_nr = fa_op.lief_nr  # type: ignore
        op_list.rec_id = fa_op._recid  # type: ignore
        op_list.order_date = fa_ordheaderlist.order_date  # type: ignore
        op_list.createdby = fa_ordheaderlist.create_name  # type: ignore
        op_list.release_date = fa_ordheaderlist.released_date  # type: ignore
        op_list.order_amount = to_decimal( # type: ignore
            fa_ordheaderlist.total_amount1)  # type: ignore

    def create_faordheaderlist():

        nonlocal op_list_data, fa_ordheader, l_lieferant, mathis, fa_op, bediener, fa_order
        nonlocal fromdate, todate, searchby, devnote_no, po_no, supp_no

        nonlocal op_list, fa_ordheaderlist
        nonlocal op_list_data, fa_ordheaderlist_data

        temp_create: string
        temp_modify: string
        total_amount = to_decimal("0.0")
        fa_ordheaderlist_data.clear()

        for fa_ordheader in db_session.query(Fa_ordheader).order_by(Fa_ordheader._recid).all():

            if fa_ordheader.created_by:

                bediener = get_cache(
                    Bediener, {"userinit": [(eq, fa_ordheader.created_by)]})

                if bediener:
                    temp_create = bediener.username
                else:
                    temp_create = ""
            else:
                temp_create = ""

            if fa_ordheader.modified_by:

                bediener = get_cache(
                    Bediener, {"userinit": [(eq, fa_ordheader.modified_by)]})

                if bediener:
                    temp_modify = bediener.username
                else:
                    temp_modify = ""
            else:
                temp_modify = ""

            for fa_order in db_session.query(Fa_order).filter(
                    (Fa_order.order_nr == fa_ordheader.order_nr)).order_by(Fa_order._recid).all():
                total_amount = to_decimal(
                    # type: ignore
                    total_amount) + to_decimal(fa_order.order_amount)
            fa_ordheaderlist = Fa_ordheaderlist()
            fa_ordheaderlist_data.append(fa_ordheaderlist)

            buffer_copy(fa_ordheader, fa_ordheaderlist)
            fa_ordheaderlist.create_name = temp_create
            fa_ordheaderlist.modify_name = temp_modify
            fa_ordheaderlist.total_amount1 = to_decimal(total_amount)

            temp_create = ""
            temp_modify = ""
            total_amount = to_decimal("0")

    create_faordheaderlist()
    distinct_op()

    return generate_output()
