#using conversion tools version: 1.0.0.117
#-----------------------------------------
# Rd 25/7/2025
# gitlab:817
# payload:
# {
#     "request": {
#         "pvILanguage": 1,
#         "mainGrp": 0,
#         "sorttype": 0,
#         "mattype": 0,
#         "fromLager": 1,
#         "toLager": 2,
#         "fromArt": 1100001,
#         "toArt": 3990079,
#         "fromDate": "07/28/2025",
#         "toDate": "07/28/2025",
#         "inputUserkey": "95EE44CBF839764A7690C157AC66C9C902905E01",
#         "inputUsername": "it",
#         "hotel_schema": "qcserverless3"
#     }
# }
#-----------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_lager, L_artikel, L_op, L_untergrup

def stock_translist_btn_gobl(main_grp:int, sorttype:int, mattype:int, from_lager:int, to_lager:int, from_art:int, to_art:int, from_date:date, to_date:date):

    prepare_cache ([L_lager, L_artikel, L_op, L_untergrup])

    t_list_data = []
    curr_nr:int = 0
    l_lager = l_artikel = l_op = l_untergrup = None

    t_list = None

    t_list_data, T_list = create_model("T_list", {"nr":int, "f_lager":int, "t_lager":int, "f_bezeich":string, "t_bezeich":string, "artnr":string, "subgr":int, "sub_bezeich":string, "bezeich":string, "qty":Decimal, "val":Decimal, "t_qty":Decimal, "t_val":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_list_data, curr_nr, l_lager, l_artikel, l_op, l_untergrup
        nonlocal main_grp, sorttype, mattype, from_lager, to_lager, from_art, to_art, from_date, to_date


        nonlocal t_list
        nonlocal t_list_data

        return {"t-list": t_list_data}

    def create_list():

        nonlocal t_list_data, curr_nr, l_lager, l_artikel, l_op, l_untergrup
        nonlocal main_grp, sorttype, mattype, from_lager, to_lager, from_art, to_art, from_date, to_date


        nonlocal t_list
        nonlocal t_list_data

        f_lager:int = 0
        t_lager:int = 0
        qty:Decimal = to_decimal("0.0")
        val:Decimal = to_decimal("0.0")
        t_qty:Decimal = to_decimal("0.0")
        t_val:Decimal = to_decimal("0.0")
        d_qty:Decimal = to_decimal("0.0")
        d_val:Decimal = to_decimal("0.0")
        m_qty:Decimal = to_decimal("0.0")
        m_val:Decimal = to_decimal("0.0")
        l_store = None
        L_store =  create_buffer("L_store",L_lager)

        if from_lager == to_lager:
            create_lista()

            return
        t_list_data.clear()
        f_lager = 0

        for l_lager in db_session.query(L_lager).filter(
                 (L_lager.lager_nr >= from_lager) & (L_lager.lager_nr <= to_lager)).order_by(L_lager._recid).all():
            t_lager = 0
            qty =  to_decimal("0")
            val =  to_decimal("0")
            t_qty =  to_decimal("0")
            t_val =  to_decimal("0")

            l_op_obj_list = {}
            l_op = L_op()
            l_artikel = L_artikel()
            for l_op.pos, l_op.artnr, l_op.anzahl, l_op.warenwert, l_op.datum, l_op._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel.zwkum, l_artikel._recid in db_session.query(L_op.pos, L_op.artnr, L_op.anzahl, L_op.warenwert, L_op.datum, L_op._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel.zwkum, L_artikel._recid).join(L_artikel,(L_artikel.artnr == L_op.artnr)).filter(
                     (L_op.lager_nr == l_lager.lager_nr) & (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.artnr >= from_art) & (L_op.artnr <= to_art) & (L_op.op_art == 4) & (L_op.herkunftflag == 1)).order_by(L_op.pos, L_artikel.bezeich).all():
                if l_op_obj_list.get(l_op._recid):
                    continue
                else:
                    l_op_obj_list[l_op._recid] = True

                if (f_lager != l_lager.lager_nr or t_lager != l_op.pos) and t_qty != 0:
                    t_list = T_list()
                    t_list_data.append(t_list)

                    curr_nr = curr_nr + 1
                    t_list.nr = curr_nr
                    t_list.bezeich = "Total"
                    t_list.qty =  to_decimal(qty)
                    t_list.val =  to_decimal(val)
                    t_list.t_qty =  to_decimal(t_qty)
                    t_list.t_val =  to_decimal(t_val)
                    qty =  to_decimal("0")
                    val =  to_decimal("0")
                    t_qty =  to_decimal("0")
                    t_val =  to_decimal("0")

                t_list = query(t_list_data, filters=(lambda t_list: t_list.f_lager == l_lager.lager_nr and t_list.t_lager == l_op.pos and to_int(t_list.artnr) == l_artikel.artnr), first=True)

                if not t_list:

                    l_store = get_cache (L_lager, {"lager_nr": [(eq, l_op.pos)]})
                    t_list = T_list()
                    t_list_data.append(t_list)

                    curr_nr = curr_nr + 1
                    t_list.nr = curr_nr
                    t_list.f_lager = l_lager.lager_nr
                    t_list.t_lager = l_op.pos

                    if f_lager != l_lager.lager_nr or t_lager != l_op.pos:
                        t_list.f_bezeich = l_lager.bezeich

                        if l_store:
                            t_list.t_bezeich = l_store.bezeich
                        f_lager = l_lager.lager_nr
                        t_lager = l_op.pos
                    t_list.artnr = to_string(l_op.artnr, "9999999")
                    t_list.bezeich = l_artikel.bezeich

                if l_op.datum == to_date:
                    t_list.qty =  to_decimal(t_list.qty) + to_decimal(l_op.anzahl)
                    t_list.val =  to_decimal(t_list.val) + to_decimal(l_op.warenwert)
                    qty =  to_decimal(qty) + to_decimal(l_op.anzahl)
                    val =  to_decimal(val) + to_decimal(l_op.warenwert)
                    d_qty =  to_decimal(d_qty) + to_decimal(l_op.anzahl)
                    d_val =  to_decimal(d_val) + to_decimal(l_op.warenwert)
                t_list.t_qty =  to_decimal(t_list.t_qty) + to_decimal(l_op.anzahl)
                t_list.t_val =  to_decimal(t_list.t_val) + to_decimal(l_op.warenwert)
                t_qty =  to_decimal(t_qty) + to_decimal(l_op.anzahl)
                t_val =  to_decimal(t_val) + to_decimal(l_op.warenwert)
                m_qty =  to_decimal(m_qty) + to_decimal(l_op.anzahl)
                m_val =  to_decimal(m_val) + to_decimal(l_op.warenwert)

            if t_qty != 0:
                t_list = T_list()
                t_list_data.append(t_list)

                curr_nr = curr_nr + 1
                t_list.nr = curr_nr
                t_list.bezeich = "Total"
                t_list.qty =  to_decimal(qty)
                t_list.val =  to_decimal(val)
                t_list.t_qty =  to_decimal(t_qty)
                t_list.t_val =  to_decimal(t_val)

        if m_qty != 0:
            t_list = T_list()
            t_list_data.append(t_list)

            curr_nr = curr_nr + 1
            t_list.nr = curr_nr
            t_list.bezeich = "GRAND TOTAL"
            t_list.qty =  to_decimal(d_qty)
            t_list.val =  to_decimal(d_val)
            t_list.t_qty =  to_decimal(m_qty)
            t_list.t_val =  to_decimal(m_val)


    def create_lista():

        nonlocal t_list_data, curr_nr, l_lager, l_artikel, l_op, l_untergrup
        nonlocal main_grp, sorttype, mattype, from_lager, to_lager, from_art, to_art, from_date, to_date


        nonlocal t_list
        nonlocal t_list_data

        f_lager:int = 0
        t_lager:int = 0
        qty:Decimal = to_decimal("0.0")
        val:Decimal = to_decimal("0.0")
        t_qty:Decimal = to_decimal("0.0")
        t_val:Decimal = to_decimal("0.0")
        d_qty:Decimal = to_decimal("0.0")
        d_val:Decimal = to_decimal("0.0")
        m_qty:Decimal = to_decimal("0.0")
        m_val:Decimal = to_decimal("0.0")
        l_store = None
        L_store =  create_buffer("L_store",L_lager)
        t_list_data.clear()

        l_lager = get_cache (L_lager, {"lager_nr": [(eq, from_lager)]})
        if l_lager is None:
            return
            

        t_lager = 0
        qty =  to_decimal("0")
        val =  to_decimal("0")
        t_qty =  to_decimal("0")
        t_val =  to_decimal("0")
        d_qty =  to_decimal("0")
        d_val =  to_decimal("0")
        m_qty =  to_decimal("0")
        m_val =  to_decimal("0")

        l_op_obj_list = {}
        l_op = L_op()
        l_artikel = L_artikel()
        # Rd 28/7/2025
        # for l_op.pos, l_op.artnr, l_op.anzahl, l_op.warenwert, l_op.datum, l_op._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel.zwkum, l_artikel._recid in db_session.query(L_op.pos, L_op.artnr, L_op.anzahl, L_op.warenwert, L_op.datum, L_op._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel.zwkum, L_artikel._recid).join(L_artikel,(L_artikel.artnr == L_op.artnr)).filter(
        #          (L_op.lager_nr == l_lager.lager_nr) & (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.artnr >= from_art) & (L_op.artnr <= to_art) & (L_op.op_art == 4) & (L_op.herkunftflag == 1) & (L_op.loeschflag <= 1)).order_by(L_op.pos, L_artikel.bezeich).all():
        
        l_op_list = db_session.query(L_op).filter(
            (L_op.lager_nr == l_lager.lager_nr) &
            (L_op.datum >= from_date) &
            (L_op.datum <= to_date) &
            (L_op.artnr >= from_art) &
            (L_op.artnr <= to_art) &
            (L_op.op_art == 4) &
            (L_op.herkunftflag == 1) &
            (L_op.loeschflag <= 1)
        ).order_by(L_op.pos).all()

        for l_op in l_op_list:
            l_artikel = db_session.query(L_artikel).filter(
                L_artikel.artnr == l_op.artnr
            ).order_by(L_artikel.bezeich).first()

            if l_artikel:
                    
                if l_op_obj_list.get(l_op._recid):
                    continue
                else:
                    l_op_obj_list[l_op._recid] = True

                if t_lager == 0:
                    t_lager = l_op.pos

                if t_lager != l_op.pos and t_qty != 0:
                    t_list = T_list()
                    t_list_data.append(t_list)

                    curr_nr = curr_nr + 1
                    t_list.nr = curr_nr
                    t_list.bezeich = "Total"
                    t_list.qty =  to_decimal(qty)
                    t_list.val =  to_decimal(val)
                    t_list.t_qty =  to_decimal(t_qty)
                    t_list.t_val =  to_decimal(t_val)
                    qty =  to_decimal("0")
                    val =  to_decimal("0")
                    t_qty =  to_decimal("0")
                    t_val =  to_decimal("0")
                    t_lager = l_op.pos

                t_list = query(t_list_data, filters=(lambda t_list: t_list.f_lager == l_lager.lager_nr and t_list.t_lager == l_op.pos and to_int(t_list.artnr) == l_artikel.artnr), first=True)

                if not t_list:

                    l_store = get_cache (L_lager, {"lager_nr": [(eq, l_op.pos)]})
                    t_list = T_list()
                    t_list_data.append(t_list)

                    curr_nr = curr_nr + 1
                    t_list.nr = curr_nr
                    t_list.f_lager = l_lager.lager_nr
                    t_list.t_lager = l_op.pos
                    t_list.artnr = to_string(l_op.artnr, "9999999")


                    t_list.bezeich = l_artikel.bezeich

                    if t_qty == 0:
                        t_list.f_bezeich = l_lager.bezeich
                        t_list.t_bezeich = l_store.bezeich

                if l_op.datum == to_date:
                    t_list.qty =  to_decimal(t_list.qty) + to_decimal(l_op.anzahl)
                    t_list.val =  to_decimal(t_list.val) + to_decimal(l_op.warenwert)
                    qty =  to_decimal(qty) + to_decimal(l_op.anzahl)
                    val =  to_decimal(val) + to_decimal(l_op.warenwert)
                    d_qty =  to_decimal(d_qty) + to_decimal(l_op.anzahl)
                    d_val =  to_decimal(d_val) + to_decimal(l_op.warenwert)


                t_list.t_qty =  to_decimal(t_list.t_qty) + to_decimal(l_op.anzahl)
                t_list.t_val =  to_decimal(t_list.t_val) + to_decimal(l_op.warenwert)
                t_qty =  to_decimal(t_qty) + to_decimal(l_op.anzahl)
                t_val =  to_decimal(t_val) + to_decimal(l_op.warenwert)
                m_qty =  to_decimal(m_qty) + to_decimal(l_op.anzahl)
                m_val =  to_decimal(m_val) + to_decimal(l_op.warenwert)

        if t_qty != 0:
            t_list = T_list()
            t_list_data.append(t_list)

            curr_nr = curr_nr + 1
            t_list.nr = curr_nr
            t_list.bezeich = "Total"
            t_list.qty =  to_decimal(qty)
            t_list.val =  to_decimal(val)
            t_list.t_qty =  to_decimal(t_qty)
            t_list.t_val =  to_decimal(t_val)

        if m_qty != 0:
            t_list = T_list()
            t_list_data.append(t_list)

            curr_nr = curr_nr + 1
            t_list.nr = curr_nr
            t_list.bezeich = "GRAND TOTAL"
            t_list.qty =  to_decimal(d_qty)
            t_list.val =  to_decimal(d_val)
            t_list.t_qty =  to_decimal(m_qty)
            t_list.t_val =  to_decimal(m_val)


        t_lager = 0
        qty =  to_decimal("0")
        val =  to_decimal("0")
        t_qty =  to_decimal("0")
        t_val =  to_decimal("0")
        d_qty =  to_decimal("0")
        d_val =  to_decimal("0")
        m_qty =  to_decimal("0")
        m_val =  to_decimal("0")

        l_op_obj_list = {}
        l_op = L_op()
        l_artikel = L_artikel()
        for l_op.pos, l_op.artnr, l_op.anzahl, l_op.warenwert, l_op.datum, l_op._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel.zwkum, l_artikel._recid in db_session.query(L_op.pos, L_op.artnr, L_op.anzahl, L_op.warenwert, L_op.datum, L_op._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel.zwkum, L_artikel._recid).join(L_artikel,(L_artikel.artnr == L_op.artnr)).filter(
                 (L_op.lager_nr == l_lager.lager_nr) & (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.artnr >= from_art) & (L_op.artnr <= to_art) & (L_op.op_art == 2) & (L_op.herkunftflag == 1) & (L_op.loeschflag <= 1)).order_by(L_op.pos, L_artikel.bezeich).all():
            if l_op_obj_list.get(l_op._recid):
                continue
            else:
                l_op_obj_list[l_op._recid] = True

            if t_lager == 0:
                t_lager = l_op.pos

            if t_lager != l_op.pos and t_qty != 0:
                t_list = T_list()
                t_list_data.append(t_list)

                curr_nr = curr_nr + 1
                t_list.nr = curr_nr
                t_list.bezeich = "Total"
                t_list.qty =  to_decimal(qty)
                t_list.val =  to_decimal(val)
                t_list.t_qty =  to_decimal(t_qty)
                t_list.t_val =  to_decimal(t_val)
                qty =  to_decimal("0")
                val =  to_decimal("0")
                t_qty =  to_decimal("0")
                t_val =  to_decimal("0")
                t_lager = l_op.pos

            t_list = query(t_list_data, filters=(lambda t_list: t_list.t_lager == l_lager.lager_nr and t_list.f_lager == l_op.pos and to_int(t_list.artnr) == l_artikel.artnr), first=True)

            if not t_list:

                l_store = get_cache (L_lager, {"lager_nr": [(eq, l_op.pos)]})
                t_list = T_list()
                t_list_data.append(t_list)

                curr_nr = curr_nr + 1
                t_list.nr = curr_nr
                t_list.t_lager = l_lager.lager_nr
                t_list.f_lager = l_op.pos
                t_list.artnr = to_string(l_op.artnr, "9999999")


                t_list.bezeich = l_artikel.bezeich

                if t_qty == 0:
                    t_list.t_bezeich = l_lager.bezeich
                    t_list.f_bezeich = l_store.bezeich

            if l_op.datum == to_date:
                t_list.qty =  to_decimal(t_list.qty) + to_decimal(l_op.anzahl)
                t_list.val =  to_decimal(t_list.val) + to_decimal(l_op.warenwert)
                qty =  to_decimal(qty) + to_decimal(l_op.anzahl)
                val =  to_decimal(val) + to_decimal(l_op.warenwert)
                d_qty =  to_decimal(d_qty) + to_decimal(l_op.anzahl)
                d_val =  to_decimal(d_val) + to_decimal(l_op.warenwert)


            t_list.t_qty =  to_decimal(t_list.t_qty) + to_decimal(l_op.anzahl)
            t_list.t_val =  to_decimal(t_list.t_val) + to_decimal(l_op.warenwert)
            t_qty =  to_decimal(t_qty) + to_decimal(l_op.anzahl)
            t_val =  to_decimal(t_val) + to_decimal(l_op.warenwert)
            m_qty =  to_decimal(m_qty) + to_decimal(l_op.anzahl)
            m_val =  to_decimal(m_val) + to_decimal(l_op.warenwert)

        if t_qty != 0:
            t_list = T_list()
            t_list_data.append(t_list)

            curr_nr = curr_nr + 1
            t_list.nr = curr_nr
            t_list.bezeich = "Total"
            t_list.qty =  to_decimal(qty)
            t_list.val =  to_decimal(val)
            t_list.t_qty =  to_decimal(t_qty)
            t_list.t_val =  to_decimal(t_val)

        if m_qty != 0:
            t_list = T_list()
            t_list_data.append(t_list)

            curr_nr = curr_nr + 1
            t_list.nr = curr_nr
            t_list.bezeich = "GRAND TOTAL"
            t_list.qty =  to_decimal(d_qty)
            t_list.val =  to_decimal(d_val)
            t_list.t_qty =  to_decimal(m_qty)
            t_list.t_val =  to_decimal(m_val)


    def list_subgroup():

        nonlocal t_list_data, curr_nr, l_lager, l_artikel, l_op, l_untergrup
        nonlocal main_grp, sorttype, mattype, from_lager, to_lager, from_art, to_art, from_date, to_date


        nonlocal t_list
        nonlocal t_list_data

        last_sub:string = ""
        to_store:int = 0
        f_lager:int = 0
        t_lager:int = 0
        t_subgr:int = 0
        qty:Decimal = to_decimal("0.0")
        val:Decimal = to_decimal("0.0")
        t_qty:Decimal = to_decimal("0.0")
        t_val:Decimal = to_decimal("0.0")
        d_qty:Decimal = to_decimal("0.0")
        d_val:Decimal = to_decimal("0.0")
        m_qty:Decimal = to_decimal("0.0")
        m_val:Decimal = to_decimal("0.0")
        subd_qty:Decimal = to_decimal("0.0")
        subd_val:Decimal = to_decimal("0.0")
        subm_qty:Decimal = to_decimal("0.0")
        subm_val:Decimal = to_decimal("0.0")
        l_store = None
        L_store =  create_buffer("L_store",L_lager)
        t_list_data.clear()
        f_lager = 0

        for l_lager in db_session.query(L_lager).filter(
                 (L_lager.lager_nr >= from_lager) & (L_lager.lager_nr <= to_lager)).order_by(L_lager._recid).all():
            t_lager = 0
            qty =  to_decimal("0")
            val =  to_decimal("0")
            t_qty =  to_decimal("0")
            t_val =  to_decimal("0")

            l_op_obj_list = {}
            l_op = L_op()
            l_artikel = L_artikel()
            l_untergrup = L_untergrup()
            for l_op.pos, l_op.artnr, l_op.anzahl, l_op.warenwert, l_op.datum, l_op._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel.zwkum, l_artikel._recid, l_untergrup.bezeich, l_untergrup.betriebsnr, l_untergrup._recid in db_session.query(L_op.pos, L_op.artnr, L_op.anzahl, L_op.warenwert, L_op.datum, L_op._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel.zwkum, L_artikel._recid, L_untergrup.bezeich, L_untergrup.betriebsnr, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_op.artnr)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                     (L_op.lager_nr == l_lager.lager_nr) & (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.artnr >= from_art) & (L_op.artnr <= to_art) & (L_op.op_art == 4) & (L_op.herkunftflag == 1)).order_by(L_artikel.zwkum, L_op.pos, L_artikel.bezeich).all():
                if l_op_obj_list.get(l_op._recid):
                    continue
                else:
                    l_op_obj_list[l_op._recid] = True

                if to_store != l_op.pos and subm_qty != 0 or (t_subgr != 0 and t_subgr != l_artikel.zwkum):
                    t_list = T_list()
                    t_list_data.append(t_list)

                    curr_nr = curr_nr + 1
                    t_list.nr = curr_nr
                    t_list.bezeich = "SubTotal"
                    t_list.qty =  to_decimal(subd_qty)
                    t_list.val =  to_decimal(subd_val)
                    t_list.t_qty =  to_decimal(subm_qty)
                    t_list.t_val =  to_decimal(subm_val)
                    subd_qty =  to_decimal("0")
                    subd_val =  to_decimal("0")
                    subm_qty =  to_decimal("0")
                    subm_val =  to_decimal("0")


                to_store = l_op.pos

                if t_subgr != l_artikel.zwkum and t_qty != 0:
                    t_list = T_list()
                    t_list_data.append(t_list)

                    curr_nr = curr_nr + 1
                    t_list.nr = curr_nr
                    t_list.bezeich = "Total " + last_sub
                    t_list.qty =  to_decimal(qty)
                    t_list.val =  to_decimal(val)
                    t_list.t_qty =  to_decimal(t_qty)
                    t_list.t_val =  to_decimal(t_val)
                    qty =  to_decimal("0")
                    val =  to_decimal("0")
                    t_qty =  to_decimal("0")
                    t_val =  to_decimal("0")

                t_list = query(t_list_data, filters=(lambda t_list: t_list.subgr == l_artikel.zwkum and t_list.f_lager == l_lager.lager_nr and t_list.t_lager == l_op.pos and to_int(t_list.artnr) == l_artikel.artnr), first=True)

                if not t_list:

                    l_store = get_cache (L_lager, {"lager_nr": [(eq, l_op.pos)]})
                    t_list = T_list()
                    t_list_data.append(t_list)

                    curr_nr = curr_nr + 1
                    t_list.nr = curr_nr
                    t_list.f_lager = l_lager.lager_nr
                    t_list.t_lager = l_op.pos

                    if f_lager != l_lager.lager_nr or t_lager != l_op.pos or t_subgr != l_artikel.zwkum:
                        t_list.f_bezeich = l_lager.bezeich

                        if l_store:
                            t_list.t_bezeich = l_store.bezeich
                        f_lager = l_lager.lager_nr
                        t_lager = l_op.pos

                        if t_subgr != l_artikel.zwkum:
                            t_list.sub_bezeich = l_untergrup.bezeich
                    t_list.artnr = to_string(l_op.artnr, "9999999")
                    t_list.bezeich = l_artikel.bezeich
                    t_list.subgr = l_artikel.zwkum
                    t_subgr = l_artikel.zwkum
                    last_sub = l_untergrup.bezeich

                if l_op.datum == to_date:
                    t_list.qty =  to_decimal(t_list.qty) + to_decimal(l_op.anzahl)
                    t_list.val =  to_decimal(t_list.val) + to_decimal(l_op.warenwert)
                    qty =  to_decimal(qty) + to_decimal(l_op.anzahl)
                    val =  to_decimal(val) + to_decimal(l_op.warenwert)
                    d_qty =  to_decimal(d_qty) + to_decimal(l_op.anzahl)
                    d_val =  to_decimal(d_val) + to_decimal(l_op.warenwert)
                    subd_qty =  to_decimal(subd_qty) + to_decimal(l_op.anzahl)
                    subd_val =  to_decimal(subd_val) + to_decimal(l_op.warenwert)
                t_list.t_qty =  to_decimal(t_list.t_qty) + to_decimal(l_op.anzahl)
                t_list.t_val =  to_decimal(t_list.t_val) + to_decimal(l_op.warenwert)
                t_qty =  to_decimal(t_qty) + to_decimal(l_op.anzahl)
                t_val =  to_decimal(t_val) + to_decimal(l_op.warenwert)
                m_qty =  to_decimal(m_qty) + to_decimal(l_op.anzahl)
                m_val =  to_decimal(m_val) + to_decimal(l_op.warenwert)
                subm_qty =  to_decimal(subm_qty) + to_decimal(l_op.anzahl)
                subm_val =  to_decimal(subm_val) + to_decimal(l_op.warenwert)

            if subm_qty != 0:
                t_list = T_list()
                t_list_data.append(t_list)

                curr_nr = curr_nr + 1
                t_list.nr = curr_nr
                t_list.bezeich = "SubTotal"
                t_list.qty =  to_decimal(subd_qty)
                t_list.val =  to_decimal(subd_val)
                t_list.t_qty =  to_decimal(subm_qty)
                t_list.t_val =  to_decimal(subm_val)
                subd_qty =  to_decimal("0")
                subd_val =  to_decimal("0")
                subm_qty =  to_decimal("0")
                subm_val =  to_decimal("0")

            if t_qty != 0:
                t_list = T_list()
                t_list_data.append(t_list)

                curr_nr = curr_nr + 1
                t_list.nr = curr_nr
                t_list.bezeich = "Total " + last_sub
                t_list.qty =  to_decimal(qty)
                t_list.val =  to_decimal(val)
                t_list.t_qty =  to_decimal(t_qty)
                t_list.t_val =  to_decimal(t_val)

        if m_qty != 0:
            t_list = T_list()
            t_list_data.append(t_list)

            curr_nr = curr_nr + 1
            t_list.nr = curr_nr
            t_list.bezeich = "GRAND TOTAL"
            t_list.qty =  to_decimal(d_qty)
            t_list.val =  to_decimal(d_val)
            t_list.t_qty =  to_decimal(m_qty)
            t_list.t_val =  to_decimal(m_val)


    def create_list1():

        nonlocal t_list_data, curr_nr, l_lager, l_artikel, l_op, l_untergrup
        nonlocal main_grp, sorttype, mattype, from_lager, to_lager, from_art, to_art, from_date, to_date


        nonlocal t_list
        nonlocal t_list_data

        f_lager:int = 0
        t_lager:int = 0
        qty:Decimal = to_decimal("0.0")
        val:Decimal = to_decimal("0.0")
        t_qty:Decimal = to_decimal("0.0")
        t_val:Decimal = to_decimal("0.0")
        d_qty:Decimal = to_decimal("0.0")
        d_val:Decimal = to_decimal("0.0")
        m_qty:Decimal = to_decimal("0.0")
        m_val:Decimal = to_decimal("0.0")
        l_store = None
        do_it:bool = False
        L_store =  create_buffer("L_store",L_lager)
        t_list_data.clear()
        f_lager = 0

        for l_lager in db_session.query(L_lager).filter(
                 (L_lager.lager_nr >= from_lager) & (L_lager.lager_nr <= to_lager)).order_by(L_lager._recid).all():
            t_lager = 0
            qty =  to_decimal("0")
            val =  to_decimal("0")
            t_qty =  to_decimal("0")
            t_val =  to_decimal("0")

            l_op_obj_list = {}
            l_op = L_op()
            l_artikel = L_artikel()
            l_untergrup = L_untergrup()
            for l_op.pos, l_op.artnr, l_op.anzahl, l_op.warenwert, l_op.datum, l_op._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel.zwkum, l_artikel._recid, l_untergrup.bezeich, l_untergrup.betriebsnr, l_untergrup._recid in db_session.query(L_op.pos, L_op.artnr, L_op.anzahl, L_op.warenwert, L_op.datum, L_op._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel.zwkum, L_artikel._recid, L_untergrup.bezeich, L_untergrup.betriebsnr, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_op.artnr) & (L_artikel.endkum == main_grp)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                     (L_op.lager_nr == l_lager.lager_nr) & (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.artnr >= from_art) & (L_op.artnr <= to_art) & (L_op.op_art == 4) & (L_op.herkunftflag == 1)).order_by(L_op.pos, L_artikel.bezeich).all():
                if l_op_obj_list.get(l_op._recid):
                    continue
                else:
                    l_op_obj_list[l_op._recid] = True


                do_it = True

                if (mattype == 1 and l_untergrup.betriebsnr == 1) or (mattype == 2 and l_untergrup.betriebsnr == 0):
                    do_it = False

                if (f_lager != l_lager.lager_nr or t_lager != l_op.pos) and t_qty != 0:
                    t_list = T_list()
                    t_list_data.append(t_list)

                    curr_nr = curr_nr + 1
                    t_list.nr = curr_nr
                    t_list.bezeich = "Total"
                    t_list.qty =  to_decimal(qty)
                    t_list.val =  to_decimal(val)
                    t_list.t_qty =  to_decimal(t_qty)
                    t_list.t_val =  to_decimal(t_val)
                    qty =  to_decimal("0")
                    val =  to_decimal("0")
                    t_qty =  to_decimal("0")
                    t_val =  to_decimal("0")

                if do_it:

                    t_list = query(t_list_data, filters=(lambda t_list: t_list.f_lager == l_lager.lager_nr and t_list.t_lager == l_op.pos and to_int(t_list.artnr) == l_artikel.artnr), first=True)

                    if not t_list:

                        l_store = get_cache (L_lager, {"lager_nr": [(eq, l_op.pos)]})
                        t_list = T_list()
                        t_list_data.append(t_list)

                        curr_nr = curr_nr + 1
                        t_list.nr = curr_nr
                        t_list.f_lager = l_lager.lager_nr
                        t_list.t_lager = l_op.pos

                        if f_lager != l_lager.lager_nr or t_lager != l_op.pos:
                            t_list.f_bezeich = l_lager.bezeich

                            if l_store:
                                t_list.t_bezeich = l_store.bezeich
                            f_lager = l_lager.lager_nr
                            t_lager = l_op.pos
                        t_list.artnr = to_string(l_op.artnr, "9999999")
                        t_list.bezeich = l_artikel.bezeich

                    if l_op.datum == to_date:
                        t_list.qty =  to_decimal(t_list.qty) + to_decimal(l_op.anzahl)
                        t_list.val =  to_decimal(t_list.val) + to_decimal(l_op.warenwert)
                        qty =  to_decimal(qty) + to_decimal(l_op.anzahl)
                        val =  to_decimal(val) + to_decimal(l_op.warenwert)
                        d_qty =  to_decimal(d_qty) + to_decimal(l_op.anzahl)
                        d_val =  to_decimal(d_val) + to_decimal(l_op.warenwert)
                    t_list.t_qty =  to_decimal(t_list.t_qty) + to_decimal(l_op.anzahl)
                    t_list.t_val =  to_decimal(t_list.t_val) + to_decimal(l_op.warenwert)
                    t_qty =  to_decimal(t_qty) + to_decimal(l_op.anzahl)
                    t_val =  to_decimal(t_val) + to_decimal(l_op.warenwert)
                    m_qty =  to_decimal(m_qty) + to_decimal(l_op.anzahl)
                    m_val =  to_decimal(m_val) + to_decimal(l_op.warenwert)

            if t_qty != 0:
                t_list = T_list()
                t_list_data.append(t_list)

                curr_nr = curr_nr + 1
                t_list.nr = curr_nr
                t_list.bezeich = "Total"
                t_list.qty =  to_decimal(qty)
                t_list.val =  to_decimal(val)
                t_list.t_qty =  to_decimal(t_qty)
                t_list.t_val =  to_decimal(t_val)

        if m_qty != 0:
            t_list = T_list()
            t_list_data.append(t_list)

            curr_nr = curr_nr + 1
            t_list.nr = curr_nr
            t_list.bezeich = "GRAND TOTAL"
            t_list.qty =  to_decimal(d_qty)
            t_list.val =  to_decimal(d_val)
            t_list.t_qty =  to_decimal(m_qty)
            t_list.t_val =  to_decimal(m_val)


    def list_subgroup1():

        nonlocal t_list_data, curr_nr, l_lager, l_artikel, l_op, l_untergrup
        nonlocal main_grp, sorttype, mattype, from_lager, to_lager, from_art, to_art, from_date, to_date


        nonlocal t_list
        nonlocal t_list_data

        t_subgr:int = 0
        f_lager:int = 0
        t_lager:int = 0
        qty:Decimal = to_decimal("0.0")
        val:Decimal = to_decimal("0.0")
        t_qty:Decimal = to_decimal("0.0")
        t_val:Decimal = to_decimal("0.0")
        d_qty:Decimal = to_decimal("0.0")
        d_val:Decimal = to_decimal("0.0")
        m_qty:Decimal = to_decimal("0.0")
        m_val:Decimal = to_decimal("0.0")
        l_store = None
        do_it:bool = False
        to_store:int = 0
        subd_qty:Decimal = to_decimal("0.0")
        subd_val:Decimal = to_decimal("0.0")
        subm_qty:Decimal = to_decimal("0.0")
        subm_val:Decimal = to_decimal("0.0")
        last_sub:string = ""
        L_store =  create_buffer("L_store",L_lager)
        t_list_data.clear()
        f_lager = 0

        for l_lager in db_session.query(L_lager).filter(
                 (L_lager.lager_nr >= from_lager) & (L_lager.lager_nr <= to_lager)).order_by(L_lager._recid).all():
            t_lager = 0
            qty =  to_decimal("0")
            val =  to_decimal("0")
            t_qty =  to_decimal("0")
            t_val =  to_decimal("0")

            l_op_obj_list = {}
            l_op = L_op()
            l_artikel = L_artikel()
            l_untergrup = L_untergrup()
            for l_op.pos, l_op.artnr, l_op.anzahl, l_op.warenwert, l_op.datum, l_op._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel.zwkum, l_artikel._recid, l_untergrup.bezeich, l_untergrup.betriebsnr, l_untergrup._recid in db_session.query(L_op.pos, L_op.artnr, L_op.anzahl, L_op.warenwert, L_op.datum, L_op._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel.zwkum, L_artikel._recid, L_untergrup.bezeich, L_untergrup.betriebsnr, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_op.artnr) & (L_artikel.endkum == main_grp)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                     (L_op.lager_nr == l_lager.lager_nr) & (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.artnr >= from_art) & (L_op.artnr <= to_art) & (L_op.op_art == 4) & (L_op.herkunftflag == 1)).order_by(L_artikel.zwkum, L_op.pos, L_artikel.bezeich).all():
                if l_op_obj_list.get(l_op._recid):
                    continue
                else:
                    l_op_obj_list[l_op._recid] = True


                do_it = True

                if (mattype == 1 and l_untergrup.betriebsnr == 1) or (mattype == 2 and l_untergrup.betriebsnr == 0):
                    do_it = False

                if do_it:

                    if to_store != l_op.pos and subm_qty != 0 or (t_subgr != 0 and t_subgr != l_artikel.zwkum):
                        t_list = T_list()
                        t_list_data.append(t_list)

                        curr_nr = curr_nr + 1
                        t_list.nr = curr_nr
                        t_list.bezeich = "SubTotal"
                        t_list.qty =  to_decimal(subd_qty)
                        t_list.val =  to_decimal(subd_val)
                        t_list.t_qty =  to_decimal(subm_qty)
                        t_list.t_val =  to_decimal(subm_val)
                        subd_qty =  to_decimal("0")
                        subd_val =  to_decimal("0")
                        subm_qty =  to_decimal("0")
                        subm_val =  to_decimal("0")


                    to_store = l_op.pos

                    if (t_subgr != l_artikel.zwkum) and t_qty != 0:
                        t_list = T_list()
                        t_list_data.append(t_list)

                        curr_nr = curr_nr + 1
                        t_list.nr = curr_nr
                        t_list.bezeich = "Total " + last_sub
                        t_list.qty =  to_decimal(qty)
                        t_list.val =  to_decimal(val)
                        t_list.t_qty =  to_decimal(t_qty)
                        t_list.t_val =  to_decimal(t_val)
                        qty =  to_decimal("0")
                        val =  to_decimal("0")
                        t_qty =  to_decimal("0")
                        t_val =  to_decimal("0")

                    t_list = query(t_list_data, filters=(lambda t_list: t_list.subgr == l_artikel.zwkum and t_list.f_lager == l_lager.lager_nr and t_list.t_lager == l_op.pos and to_int(t_list.artnr) == l_artikel.artnr), first=True)

                    if not t_list:

                        l_store = get_cache (L_lager, {"lager_nr": [(eq, l_op.pos)]})
                        t_list = T_list()
                        t_list_data.append(t_list)

                        curr_nr = curr_nr + 1
                        t_list.nr = curr_nr
                        t_list.f_lager = l_lager.lager_nr
                        t_list.t_lager = l_op.pos

                        if f_lager != l_lager.lager_nr or t_lager != l_op.pos or t_subgr != l_artikel.zwkum:
                            t_list.f_bezeich = l_lager.bezeich

                            if l_store:
                                t_list.t_bezeich = l_store.bezeich
                            f_lager = l_lager.lager_nr
                            t_lager = l_op.pos

                            if t_subgr != l_artikel.zwkum:
                                t_list.sub_bezeich = l_untergrup.bezeich
                        t_list.artnr = to_string(l_op.artnr, "9999999")
                        t_list.subgr = l_artikel.zwkum
                        t_list.bezeich = l_artikel.bezeich
                        last_sub = l_untergrup.bezeich
                        t_subgr = l_artikel.zwkum

                    if l_op.datum == to_date:
                        t_list.qty =  to_decimal(t_list.qty) + to_decimal(l_op.anzahl)
                        t_list.val =  to_decimal(t_list.val) + to_decimal(l_op.warenwert)
                        qty =  to_decimal(qty) + to_decimal(l_op.anzahl)
                        val =  to_decimal(val) + to_decimal(l_op.warenwert)
                        d_qty =  to_decimal(d_qty) + to_decimal(l_op.anzahl)
                        d_val =  to_decimal(d_val) + to_decimal(l_op.warenwert)
                        subd_qty =  to_decimal(subd_qty) + to_decimal(l_op.anzahl)
                        subd_val =  to_decimal(subd_val) + to_decimal(l_op.warenwert)
                    t_list.t_qty =  to_decimal(t_list.t_qty) + to_decimal(l_op.anzahl)
                    t_list.t_val =  to_decimal(t_list.t_val) + to_decimal(l_op.warenwert)
                    t_qty =  to_decimal(t_qty) + to_decimal(l_op.anzahl)
                    t_val =  to_decimal(t_val) + to_decimal(l_op.warenwert)
                    m_qty =  to_decimal(m_qty) + to_decimal(l_op.anzahl)
                    m_val =  to_decimal(m_val) + to_decimal(l_op.warenwert)
                    subm_qty =  to_decimal(subm_qty) + to_decimal(l_op.anzahl)
                    subm_val =  to_decimal(subm_val) + to_decimal(l_op.warenwert)

            if subm_qty != 0:
                t_list = T_list()
                t_list_data.append(t_list)

                curr_nr = curr_nr + 1
                t_list.nr = curr_nr
                t_list.bezeich = "SubTotal"
                t_list.qty =  to_decimal(subd_qty)
                t_list.val =  to_decimal(subd_val)
                t_list.t_qty =  to_decimal(subm_qty)
                t_list.t_val =  to_decimal(subm_val)
                subd_qty =  to_decimal("0")
                subd_val =  to_decimal("0")
                subm_qty =  to_decimal("0")
                subm_val =  to_decimal("0")

            if t_qty != 0:
                t_list = T_list()
                t_list_data.append(t_list)

                curr_nr = curr_nr + 1
                t_list.nr = curr_nr
                t_list.bezeich = "Total " + last_sub
                t_list.qty =  to_decimal(qty)
                t_list.val =  to_decimal(val)
                t_list.t_qty =  to_decimal(t_qty)
                t_list.t_val =  to_decimal(t_val)

        if m_qty != 0:
            t_list = T_list()
            t_list_data.append(t_list)

            curr_nr = curr_nr + 1
            t_list.nr = curr_nr
            t_list.bezeich = "GRAND TOTAL"
            t_list.qty =  to_decimal(d_qty)
            t_list.val =  to_decimal(d_val)
            t_list.t_qty =  to_decimal(m_qty)
            t_list.t_val =  to_decimal(m_val)


    if main_grp == 0:

        if sorttype == 0:
            create_list()
        else:
            list_subgroup()
    else:

        if sorttype == 0:
            create_list1()
        else:
            list_subgroup1()

    return generate_output()