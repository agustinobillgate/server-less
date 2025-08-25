#using conversion tools version: 1.0.0.118
#------------------------------------------
# Rd, 25/8/2025
#
#------------------------------------------

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_lager, L_artikel, L_untergrup, L_ophis

def stin_summaryhis_btn_gobl(sorttype:int, from_lager:int, to_lager:int, from_date:date, to_date:date, from_art:int, to_art:int, from_grp:int, to_grp:int):

    prepare_cache ([L_lager, L_artikel, L_untergrup, L_ophis])

    t_list_data = []
    l_lager = l_artikel = l_untergrup = l_ophis = None

    tt_list = t_list = big_total = temp_list = None

    tt_list_data, Tt_list = create_model("Tt_list", {"flag":int, "subgroup":int, "subbez":string, "f_lager":int, "f_bezeich":string, "artnr":string, "bezeich":string, "einheit":string, "qty":Decimal, "val":Decimal, "t_qty":Decimal, "t_val":Decimal, "grand_flag":bool})
    t_list_data, T_list = create_model("T_list", {"flag":int, "subgroup":int, "subbez":string, "f_lager":int, "f_bezeich":string, "artnr":string, "bezeich":string, "einheit":string, "qty":Decimal, "val":Decimal, "t_qty":Decimal, "t_val":Decimal, "grand_flag":bool})
    big_total_data, Big_total = create_model("Big_total", {"total":Decimal, "lager_nr":int, "f_bezeich":string})
    temp_list_data, Temp_list = create_model_like(Tt_list)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_list_data, l_lager, l_artikel, l_untergrup, l_ophis
        nonlocal sorttype, from_lager, to_lager, from_date, to_date, from_art, to_art, from_grp, to_grp


        nonlocal tt_list, t_list, big_total, temp_list
        nonlocal tt_list_data, t_list_data, big_total_data, temp_list_data

        return {"t-list": t_list_data}

    def create_list1():

        nonlocal t_list_data, l_lager, l_artikel, l_untergrup, l_ophis
        nonlocal sorttype, from_lager, to_lager, from_date, to_date, from_art, to_art, from_grp, to_grp


        nonlocal tt_list, t_list, big_total, temp_list
        nonlocal tt_list_data, t_list_data, big_total_data, temp_list_data

        f_lager:int = 0
        qty:Decimal = to_decimal("0.0")
        val:Decimal = to_decimal("0.0")
        t_qty:Decimal = to_decimal("0.0")
        t_val:Decimal = to_decimal("0.0")
        m_qty:Decimal = to_decimal("0.0")
        m_val:Decimal = to_decimal("0.0")
        d_qty:Decimal = to_decimal("0.0")
        d_val:Decimal = to_decimal("0.0")
        l_store = None
        L_store =  create_buffer("L_store",L_lager)
        t_list_data.clear()
        f_lager = 0

        for l_lager in db_session.query(L_lager).filter(
                 (L_lager.lager_nr >= from_lager) & (L_lager.lager_nr <= to_lager)).order_by(L_lager.lager_nr).all():
            qty =  to_decimal("0")
            val =  to_decimal("0")
            t_qty =  to_decimal("0")
            t_val =  to_decimal("0")

            l_artikel_obj_list = {}
            # for l_artikel in db_session.query(L_artikel).filter(
            #          ((L_artikel.artnr.in_(list(set([l_ophis.artnr for l_ophis in l_ophis_data if l_ophis.lager_nr == l_lager.lager_nr] & (l_ophis.datum >= from_date) & 
            #                                         (l_ophis.datum <= to_date) & 
            #                                         (l_ophis.artnr >= from_art) & 
            #                                         (l_ophis.artnr <= to_art) & 
            #                                         (l_ophis.anzahl != 0) & 
            #                                         (l_ophis.op_art == 1))))) & 
            #                                         (L_artikel.zwkum >= from_grp) & 
            #                                         (L_artikel.zwkum <= to_grp))).order_by(L_artikel.artnr).all():
             # Inner: FOR EACH l-ophis WHERE ... (for this lager)
            for l_ophis in (
                db_session.query(L_ophis)
                .filter(
                    L_ophis.lager_nr == l_lager.lager_nr,   # join to current l-lager
                    L_ophis.datum    >= from_date,
                    L_ophis.datum    <= to_date,
                    L_ophis.artnr    >= from_art,
                    L_ophis.artnr    <= to_art,
                    L_ophis.anzahl   != 0,
                    L_ophis.op_art   == 1,
                )
                .order_by(L_ophis.artnr.asc())
                .all()
            ):
                # FIRST l-artikel WHERE artnr = l-ophis.artnr
                #   AND zwkum BETWEEN from-grp AND to-grp BY l-artikel.artnr
                l_artikel = (
                    db_session.query(L_artikel)
                    .filter(
                        L_artikel.artnr == l_ophis.artnr,
                        L_artikel.zwkum >= from_grp,
                        L_artikel.zwkum <= to_grp,
                    )
                    .first()   # "FIRST"; returns None if not found
                )

                if l_artikel is None:
                    # IF l-artikel NOT AVAILABLE THEN: CONTINUE (skip this l-ophis)
                    continue
                if l_artikel_obj_list.get(l_artikel._recid):
                    continue
                else:
                    l_artikel_obj_list[l_artikel._recid] = True

                if f_lager != l_lager.lager_nr and t_qty != 0:
                    t_list = T_list()
                    t_list_data.append(t_list)

                    t_list.flag = 1
                    t_list.f_lager = f_lager
                    t_list.bezeich = "TOTAL"
                    t_list.qty =  to_decimal(qty)
                    t_list.val =  to_decimal(val)
                    t_list.t_qty =  to_decimal(t_qty)
                    t_list.t_val =  to_decimal(t_val)
                    qty =  to_decimal("0")
                    val =  to_decimal("0")
                    t_qty =  to_decimal("0")
                    t_val =  to_decimal("0")
                    f_lager = l_lager.lager_nr

                t_list = query(t_list_data, filters=(lambda t_list: t_list.f_lager == l_lager.lager_nr and to_int(t_list.artnr) == l_artikel.artnr), first=True)

                if not t_list:
                    t_list = T_list()
                    t_list_data.append(t_list)

                    t_list.f_lager = l_lager.lager_nr

                    if f_lager != l_lager.lager_nr:
                        t_list.f_bezeich = l_lager.bezeich
                        f_lager = l_lager.lager_nr
                    t_list.artnr = to_string(l_ophis.artnr, "9999999")
                    t_list.bezeich = l_artikel.bezeich
                    t_list.einheit = l_artikel.masseinheit

                if l_ophis.datum == to_date:
                    t_list.qty =  to_decimal(t_list.qty) + to_decimal(l_ophis.anzahl)
                    t_list.val =  to_decimal(t_list.val) + to_decimal(l_ophis.warenwert)
                    qty =  to_decimal(qty) + to_decimal(l_ophis.anzahl)
                    val =  to_decimal(val) + to_decimal(l_ophis.warenwert)
                    d_qty =  to_decimal(d_qty) + to_decimal(l_ophis.anzahl)
                    d_val =  to_decimal(d_val) + to_decimal(l_ophis.warenwert)
                t_list.t_qty =  to_decimal(t_list.t_qty) + to_decimal(l_ophis.anzahl)
                t_list.t_val =  to_decimal(t_list.t_val) + to_decimal(l_ophis.warenwert)
                t_qty =  to_decimal(t_qty) + to_decimal(l_ophis.anzahl)
                t_val =  to_decimal(t_val) + to_decimal(l_ophis.warenwert)
                m_qty =  to_decimal(m_qty) + to_decimal(l_ophis.anzahl)
                m_val =  to_decimal(m_val) + to_decimal(l_ophis.warenwert)

            if t_qty != 0:
                t_list = T_list()
                t_list_data.append(t_list)

                t_list.flag = 1
                t_list.f_lager = f_lager
                t_list.bezeich = "TOTAL"
                t_list.qty =  to_decimal(qty)
                t_list.val =  to_decimal(val)
                t_list.t_qty =  to_decimal(t_qty)
                t_list.t_val =  to_decimal(t_val)
        t_list = T_list()
        t_list_data.append(t_list)

        t_list.flag = 1
        t_list.f_lager = 9999
        t_list.bezeich = "GRAND TOTAL"
        t_list.qty =  to_decimal(d_qty)
        t_list.val =  to_decimal(d_val)
        t_list.t_qty =  to_decimal(m_qty)
        t_list.t_val =  to_decimal(m_val)
        t_list.grand_flag = True


    def create_list3():

        nonlocal t_list_data, l_lager, l_artikel, l_untergrup, l_ophis
        nonlocal sorttype, from_lager, to_lager, from_date, to_date, from_art, to_art, from_grp, to_grp


        nonlocal tt_list, t_list, big_total, temp_list
        nonlocal tt_list_data, t_list_data, big_total_data, temp_list_data

        f_lager:int = 0
        qty:Decimal = to_decimal("0.0")
        val:Decimal = to_decimal("0.0")
        t_qty:Decimal = to_decimal("0.0")
        t_val:Decimal = to_decimal("0.0")
        m_qty:Decimal = to_decimal("0.0")
        m_val:Decimal = to_decimal("0.0")
        d_qty:Decimal = to_decimal("0.0")
        d_val:Decimal = to_decimal("0.0")
        st_qty:Decimal = to_decimal("0.0")
        st_val:Decimal = to_decimal("0.0")
        sm_qty:Decimal = to_decimal("0.0")
        sm_val:Decimal = to_decimal("0.0")
        subgr:string = ""
        l_store = None
        L_store =  create_buffer("L_store",L_lager)
        t_list_data.clear()
        f_lager = 0

        for l_lager in db_session.query(L_lager).filter(
                 (L_lager.lager_nr >= from_lager) & (L_lager.lager_nr <= to_lager)).order_by(L_lager.lager_nr).all():
            qty =  to_decimal("0")
            val =  to_decimal("0")
            t_qty =  to_decimal("0")
            t_val =  to_decimal("0")

            l_ophis_obj_list = {}
            l_ophis = L_ophis()
            l_artikel = L_artikel()
            l_untergrup = L_untergrup()
            for l_ophis.datum, l_ophis.artnr, l_ophis.anzahl, l_ophis.op_art, l_ophis.warenwert, l_ophis._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel.masseinheit, l_artikel.zwkum, l_artikel._recid, l_untergrup.bezeich, l_untergrup._recid in db_session.query(L_ophis.datum, L_ophis.artnr, L_ophis.anzahl, L_ophis.op_art, L_ophis.warenwert, L_ophis._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel.masseinheit, L_artikel.zwkum, L_artikel._recid, L_untergrup.bezeich, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_ophis.artnr) & (L_artikel.zwkum >= from_grp) & (L_artikel.zwkum <= to_grp)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                     (L_ophis.lager_nr == l_lager.lager_nr) & (L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & (L_ophis.artnr >= from_art) & (L_ophis.artnr <= to_art) & (L_ophis.anzahl != 0) & (L_ophis.op_art == 1)).order_by(L_artikel.zwkum, L_artikel.artnr).all():
                if l_ophis_obj_list.get(l_ophis._recid):
                    continue
                else:
                    l_ophis_obj_list[l_ophis._recid] = True

                if subgr != l_untergrup.bezeich and subgr != "" and sm_qty != 0:
                    t_list = T_list()
                    t_list_data.append(t_list)

                    t_list.flag = 1
                    t_list.bezeich = subgr
                    t_list.qty =  to_decimal(st_qty)
                    t_list.val =  to_decimal(st_val)
                    t_list.t_qty =  to_decimal(sm_qty)
                    t_list.t_val =  to_decimal(sm_val)
                    st_qty =  to_decimal("0")
                    st_val =  to_decimal("0")
                    sm_qty =  to_decimal("0")
                    sm_val =  to_decimal("0")

                if f_lager != l_lager.lager_nr and t_qty != 0:
                    t_list = T_list()
                    t_list_data.append(t_list)

                    t_list.flag = 1
                    t_list.f_lager = f_lager
                    t_list.bezeich = "TOTAL"
                    t_list.qty =  to_decimal(qty)
                    t_list.val =  to_decimal(val)
                    t_list.t_qty =  to_decimal(t_qty)
                    t_list.t_val =  to_decimal(t_val)
                    qty =  to_decimal("0")
                    val =  to_decimal("0")
                    t_qty =  to_decimal("0")
                    t_val =  to_decimal("0")
                    f_lager = l_lager.lager_nr

                t_list = query(t_list_data, filters=(lambda t_list: t_list.f_lager == l_lager.lager_nr and to_int(t_list.artnr) == l_artikel.artnr), first=True)

                if not t_list:
                    t_list = T_list()
                    t_list_data.append(t_list)

                    t_list.f_lager = l_lager.lager_nr

                    if f_lager != l_lager.lager_nr:
                        t_list.f_bezeich = l_lager.bezeich
                        f_lager = l_lager.lager_nr
                    t_list.artnr = to_string(l_ophis.artnr, "9999999")
                    t_list.bezeich = l_artikel.bezeich
                    t_list.einheit = l_artikel.masseinheit
                    t_list.subgroup = l_artikel.zwkum
                    t_list.subbez = l_untergrup.bezeich

                if l_ophis.datum == to_date:
                    t_list.qty =  to_decimal(t_list.qty) + to_decimal(l_ophis.anzahl)
                    t_list.val =  to_decimal(t_list.val) + to_decimal(l_ophis.warenwert)
                    qty =  to_decimal(qty) + to_decimal(l_ophis.anzahl)
                    val =  to_decimal(val) + to_decimal(l_ophis.warenwert)
                    st_qty =  to_decimal(st_qty) + to_decimal(l_ophis.anzahl)
                    st_val =  to_decimal(st_val) + to_decimal(l_ophis.warenwert)
                    d_qty =  to_decimal(d_qty) + to_decimal(l_ophis.anzahl)
                    d_val =  to_decimal(d_val) + to_decimal(l_ophis.warenwert)
                t_list.t_qty =  to_decimal(t_list.t_qty) + to_decimal(l_ophis.anzahl)
                t_list.t_val =  to_decimal(t_list.t_val) + to_decimal(l_ophis.warenwert)
                t_qty =  to_decimal(t_qty) + to_decimal(l_ophis.anzahl)
                t_val =  to_decimal(t_val) + to_decimal(l_ophis.warenwert)
                m_qty =  to_decimal(m_qty) + to_decimal(l_ophis.anzahl)
                m_val =  to_decimal(m_val) + to_decimal(l_ophis.warenwert)
                sm_qty =  to_decimal(sm_qty) + to_decimal(l_ophis.anzahl)
                sm_val =  to_decimal(sm_val) + to_decimal(l_ophis.warenwert)
                subgr = l_untergrup.bezeich

            if sm_qty != 0:
                t_list = T_list()
                t_list_data.append(t_list)

                t_list.flag = 1
                t_list.bezeich = subgr
                t_list.qty =  to_decimal(st_qty)
                t_list.val =  to_decimal(st_val)
                t_list.t_qty =  to_decimal(sm_qty)
                t_list.t_val =  to_decimal(sm_val)
                st_qty =  to_decimal("0")
                st_val =  to_decimal("0")
                sm_qty =  to_decimal("0")
                sm_val =  to_decimal("0")

            if t_qty != 0:
                t_list = T_list()
                t_list_data.append(t_list)

                t_list.flag = 1
                t_list.f_lager = f_lager
                t_list.bezeich = "TOTAL"
                t_list.qty =  to_decimal(qty)
                t_list.val =  to_decimal(val)
                t_list.t_qty =  to_decimal(t_qty)
                t_list.t_val =  to_decimal(t_val)
        t_list = T_list()
        t_list_data.append(t_list)

        t_list.flag = 1
        t_list.f_lager = 9999
        t_list.bezeich = "GRAND TOTAL"
        t_list.qty =  to_decimal(d_qty)
        t_list.val =  to_decimal(d_val)
        t_list.t_qty =  to_decimal(m_qty)
        t_list.t_val =  to_decimal(m_val)


    def create_list2():

        nonlocal t_list_data, l_lager, l_artikel, l_untergrup, l_ophis
        nonlocal sorttype, from_lager, to_lager, from_date, to_date, from_art, to_art, from_grp, to_grp


        nonlocal tt_list, t_list, big_total, temp_list
        nonlocal tt_list_data, t_list_data, big_total_data, temp_list_data

        f_lager:int = 0
        qty:Decimal = to_decimal("0.0")
        val:Decimal = to_decimal("0.0")
        t_qty:Decimal = to_decimal("0.0")
        t_val:Decimal = to_decimal("0.0")
        m_qty:Decimal = to_decimal("0.0")
        m_val:Decimal = to_decimal("0.0")
        d_qty:Decimal = to_decimal("0.0")
        d_val:Decimal = to_decimal("0.0")
        l_store = None
        L_store =  create_buffer("L_store",L_lager)
        t_list_data.clear()
        f_lager = 0

        for l_lager in db_session.query(L_lager).filter(
                 (L_lager.lager_nr >= from_lager) & (L_lager.lager_nr <= to_lager)).order_by(L_lager.lager_nr).all():
            qty =  to_decimal("0")
            val =  to_decimal("0")
            t_qty =  to_decimal("0")
            t_val =  to_decimal("0")

            l_ophis_obj_list = {}
            l_ophis = L_ophis()
            l_artikel = L_artikel()
            for l_ophis.datum, l_ophis.artnr, l_ophis.anzahl, l_ophis.op_art, l_ophis.warenwert, l_ophis._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel.masseinheit, l_artikel.zwkum, l_artikel._recid in db_session.query(L_ophis.datum, L_ophis.artnr, L_ophis.anzahl, L_ophis.op_art, L_ophis.warenwert, L_ophis._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel.masseinheit, L_artikel.zwkum, L_artikel._recid).join(L_artikel,(L_artikel.artnr == L_ophis.artnr) & (L_artikel.zwkum >= from_grp) & (L_artikel.zwkum <= to_grp)).filter(
                     (L_ophis.lager_nr == l_lager.lager_nr) & (L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & (L_ophis.artnr >= from_art) & (L_ophis.artnr <= to_art) & (L_ophis.anzahl != 0) & (L_ophis.op_art == 1)).order_by(L_artikel.bezeich).all():
                if l_ophis_obj_list.get(l_ophis._recid):
                    continue
                else:
                    l_ophis_obj_list[l_ophis._recid] = True

                if f_lager != l_lager.lager_nr and t_qty != 0:
                    t_list = T_list()
                    t_list_data.append(t_list)

                    t_list.flag = 1
                    t_list.f_lager = f_lager
                    t_list.bezeich = "TOTAL"
                    t_list.qty =  to_decimal(qty)
                    t_list.val =  to_decimal(val)
                    t_list.t_qty =  to_decimal(t_qty)
                    t_list.t_val =  to_decimal(t_val)
                    qty =  to_decimal("0")
                    val =  to_decimal("0")
                    t_qty =  to_decimal("0")
                    t_val =  to_decimal("0")
                    f_lager = l_lager.lager_nr

                t_list = query(t_list_data, filters=(lambda t_list: t_list.f_lager == l_lager.lager_nr and to_int(t_list.artnr) == l_artikel.artnr), first=True)

                if not t_list:
                    t_list = T_list()
                    t_list_data.append(t_list)

                    t_list.f_lager = l_lager.lager_nr

                    if f_lager != l_lager.lager_nr:
                        t_list.f_bezeich = l_lager.bezeich
                        f_lager = l_lager.lager_nr
                    t_list.artnr = to_string(l_ophis.artnr, "9999999")
                    t_list.bezeich = l_artikel.bezeich
                    t_list.einheit = l_artikel.masseinheit

                if l_ophis.datum == to_date:
                    t_list.qty =  to_decimal(t_list.qty) + to_decimal(l_ophis.anzahl)
                    t_list.val =  to_decimal(t_list.val) + to_decimal(l_ophis.warenwert)
                    qty =  to_decimal(qty) + to_decimal(l_ophis.anzahl)
                    val =  to_decimal(val) + to_decimal(l_ophis.warenwert)
                    d_qty =  to_decimal(d_qty) + to_decimal(l_ophis.anzahl)
                    d_val =  to_decimal(d_val) + to_decimal(l_ophis.warenwert)
                t_list.t_qty =  to_decimal(t_list.t_qty) + to_decimal(l_ophis.anzahl)
                t_list.t_val =  to_decimal(t_list.t_val) + to_decimal(l_ophis.warenwert)
                t_qty =  to_decimal(t_qty) + to_decimal(l_ophis.anzahl)
                t_val =  to_decimal(t_val) + to_decimal(l_ophis.warenwert)
                m_qty =  to_decimal(m_qty) + to_decimal(l_ophis.anzahl)
                m_val =  to_decimal(m_val) + to_decimal(l_ophis.warenwert)

            if t_qty != 0:
                t_list = T_list()
                t_list_data.append(t_list)

                t_list.flag = 1
                t_list.f_lager = f_lager
                t_list.bezeich = "TOTAL"
                t_list.qty =  to_decimal(qty)
                t_list.val =  to_decimal(val)
                t_list.t_qty =  to_decimal(t_qty)
                t_list.t_val =  to_decimal(t_val)
        t_list = T_list()
        t_list_data.append(t_list)

        t_list.flag = 1
        t_list.f_lager = 9999
        t_list.bezeich = "GRAND TOTAL"
        t_list.qty =  to_decimal(d_qty)
        t_list.val =  to_decimal(d_val)
        t_list.t_qty =  to_decimal(m_qty)
        t_list.t_val =  to_decimal(m_val)


    def create_list4():

        nonlocal t_list_data, l_lager, l_artikel, l_untergrup, l_ophis
        nonlocal sorttype, from_lager, to_lager, from_date, to_date, from_art, to_art, from_grp, to_grp


        nonlocal tt_list, t_list, big_total, temp_list
        nonlocal tt_list_data, t_list_data, big_total_data, temp_list_data

        f_lager:int = 0
        qty:Decimal = to_decimal("0.0")
        val:Decimal = to_decimal("0.0")
        t_qty:Decimal = to_decimal("0.0")
        t_val:Decimal = to_decimal("0.0")
        m_qty:Decimal = to_decimal("0.0")
        m_val:Decimal = to_decimal("0.0")
        d_qty:Decimal = to_decimal("0.0")
        d_val:Decimal = to_decimal("0.0")
        l_store = None
        L_store =  create_buffer("L_store",L_lager)
        t_list_data.clear()
        f_lager = 0

        for l_lager in db_session.query(L_lager).filter(
                 (L_lager.lager_nr >= from_lager) & (L_lager.lager_nr <= to_lager)).order_by(L_lager.lager_nr).all():
            qty =  to_decimal("0")
            val =  to_decimal("0")
            t_qty =  to_decimal("0")
            t_val =  to_decimal("0")

            l_ophis_obj_list = {}
            l_ophis = L_ophis()
            l_artikel = L_artikel()
            for l_ophis.datum, l_ophis.artnr, l_ophis.anzahl, l_ophis.op_art, l_ophis.warenwert, l_ophis._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel.masseinheit, l_artikel.zwkum, l_artikel._recid in db_session.query(L_ophis.datum, L_ophis.artnr, L_ophis.anzahl, L_ophis.op_art, L_ophis.warenwert, L_ophis._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel.masseinheit, L_artikel.zwkum, L_artikel._recid).join(L_artikel,(L_artikel.artnr == L_ophis.artnr) & (L_artikel.zwkum >= from_grp) & (L_artikel.zwkum <= to_grp)).filter(
                     (L_ophis.lager_nr == l_lager.lager_nr) & (L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & (L_ophis.artnr >= from_art) & (L_ophis.artnr <= to_art) & (L_ophis.anzahl != 0) & (L_ophis.op_art == 1)).order_by(L_artikel.bezeich).all():
                if l_ophis_obj_list.get(l_ophis._recid):
                    continue
                else:
                    l_ophis_obj_list[l_ophis._recid] = True

                if f_lager != l_lager.lager_nr and t_qty != 0:
                    tt_list = Tt_list()
                    tt_list_data.append(tt_list)

                    tt_list.flag = 1
                    tt_list.f_lager = f_lager
                    tt_list.bezeich = "TOTAL"
                    tt_list.qty =  to_decimal(qty)
                    tt_list.val =  to_decimal(val)
                    tt_list.t_qty =  to_decimal(t_qty)
                    tt_list.t_val =  to_decimal(t_val)
                    qty =  to_decimal("0")
                    val =  to_decimal("0")
                    t_qty =  to_decimal("0")
                    t_val =  to_decimal("0")
                    f_lager = l_lager.lager_nr

                tt_list = query(tt_list_data, filters=(lambda tt_list: tt_list.f_lager == l_lager.lager_nr and to_int(tt_list.artnr) == l_artikel.artnr), first=True)

                if not tt_list:
                    tt_list = Tt_list()
                    tt_list_data.append(tt_list)

                    tt_list.f_lager = l_lager.lager_nr

                    if f_lager != l_lager.lager_nr:
                        tt_list.f_bezeich = l_lager.bezeich
                        f_lager = l_lager.lager_nr
                    tt_list.artnr = to_string(l_ophis.artnr, "9999999")
                    tt_list.bezeich = l_artikel.bezeich
                    tt_list.einheit = l_artikel.masseinheit

                if tt_list.f_bezeich != "":
                    tt_list = Tt_list()
                    tt_list_data.append(tt_list)

                    tt_list.f_lager = l_lager.lager_nr

                    if f_lager != l_lager.lager_nr:
                        tt_list.f_bezeich = l_lager.bezeich
                        f_lager = l_lager.lager_nr
                    tt_list.artnr = to_string(l_ophis.artnr, "9999999")
                    tt_list.bezeich = l_artikel.bezeich
                    tt_list.einheit = l_artikel.masseinheit

                if l_ophis.datum == to_date:
                    tt_list.qty =  to_decimal(tt_list.qty) + to_decimal(l_ophis.anzahl)
                    tt_list.val =  to_decimal(tt_list.val) + to_decimal(l_ophis.warenwert)
                    qty =  to_decimal(qty) + to_decimal(l_ophis.anzahl)
                    val =  to_decimal(val) + to_decimal(l_ophis.warenwert)
                    d_qty =  to_decimal(d_qty) + to_decimal(l_ophis.anzahl)
                    d_val =  to_decimal(d_val) + to_decimal(l_ophis.warenwert)
                tt_list.t_qty =  to_decimal(tt_list.t_qty) + to_decimal(l_ophis.anzahl)
                tt_list.t_val =  to_decimal(tt_list.t_val) + to_decimal(l_ophis.warenwert)
                t_qty =  to_decimal(t_qty) + to_decimal(l_ophis.anzahl)
                t_val =  to_decimal(t_val) + to_decimal(l_ophis.warenwert)
                m_qty =  to_decimal(m_qty) + to_decimal(l_ophis.anzahl)
                m_val =  to_decimal(m_val) + to_decimal(l_ophis.warenwert)

            if t_qty != 0:
                tt_list = Tt_list()
                tt_list_data.append(tt_list)

                tt_list.flag = 1
                tt_list.f_lager = f_lager
                tt_list.bezeich = "TOTAL"
                tt_list.qty =  to_decimal(qty)
                tt_list.val =  to_decimal(val)
                tt_list.t_qty =  to_decimal(t_qty)
                tt_list.t_val =  to_decimal(t_val)
        tt_list = Tt_list()
        tt_list_data.append(tt_list)

        tt_list.flag = 1
        tt_list.f_lager = 9999
        tt_list.bezeich = "GRAND TOTAL"
        tt_list.qty =  to_decimal(d_qty)
        tt_list.val =  to_decimal(d_val)
        tt_list.t_qty =  to_decimal(m_qty)
        tt_list.t_val =  to_decimal(m_val)


    def create_output():

        nonlocal t_list_data, l_lager, l_artikel, l_untergrup, l_ophis
        nonlocal sorttype, from_lager, to_lager, from_date, to_date, from_art, to_art, from_grp, to_grp


        nonlocal tt_list, t_list, big_total, temp_list
        nonlocal tt_list_data, t_list_data, big_total_data, temp_list_data

        for tt_list in query(tt_list_data):
            temp_list = Temp_list()
            temp_list_data.append(temp_list)

            buffer_copy(tt_list, temp_list)

        for tt_list in query(tt_list_data, filters=(lambda tt_list: tt_list.bezeich.lower()  == ("TOTAL").lower()  and tt_list.f_lager != 9999), sort_by=[("t_val",True)]):

            temp_list = query(temp_list_data, filters=(lambda temp_list: temp_list.f_lager == tt_list.f_lager and temp_list.f_bezeich != ""), first=True)

            if temp_list:
                t_list = T_list()
                t_list_data.append(t_list)

                t_list.artnr = temp_list.artnr
                t_list.bezeich = temp_list.bezeich
                t_list.einheit = temp_list.einheit
                t_list.f_bezeich = temp_list.f_bezeich
                t_list.f_lager = temp_list.f_lager
                t_list.flag = temp_list.flag
                t_list.qty =  to_decimal(temp_list.qty)
                t_list.subbez = temp_list.subbez
                t_list.subgroup = temp_list.subgroup
                t_list.t_qty =  to_decimal(temp_list.t_qty)
                t_list.t_val =  to_decimal(temp_list.t_val)
                t_list.val =  to_decimal(temp_list.val)

            for temp_list in query(temp_list_data, filters=(lambda temp_list: temp_list.f_lager == tt_list.f_lager and temp_list.bezeich.lower()  != ("TOTAL").lower()), sort_by=[("t_val",True)]):
                t_list = T_list()
                t_list_data.append(t_list)

                t_list.artnr = temp_list.artnr
                t_list.bezeich = temp_list.bezeich
                t_list.einheit = temp_list.einheit
                t_list.f_bezeich = temp_list.f_bezeich
                t_list.f_lager = temp_list.f_lager
                t_list.flag = temp_list.flag
                t_list.qty =  to_decimal(temp_list.qty)
                t_list.subbez = temp_list.subbez
                t_list.subgroup = temp_list.subgroup
                t_list.t_qty =  to_decimal(temp_list.t_qty)
                t_list.t_val =  to_decimal(temp_list.t_val)
                t_list.val =  to_decimal(temp_list.val)

            temp_list = query(temp_list_data, filters=(lambda temp_list: temp_list.f_lager == t_list.f_lager and temp_list.bezeich.lower()  == ("TOTAL").lower()), first=True)

            if temp_list:
                t_list = T_list()
                t_list_data.append(t_list)

                t_list.artnr = temp_list.artnr
                t_list.bezeich = temp_list.bezeich
                t_list.einheit = temp_list.einheit
                t_list.f_bezeich = temp_list.f_bezeich
                t_list.f_lager = temp_list.f_lager
                t_list.flag = temp_list.flag
                t_list.qty =  to_decimal(temp_list.qty)
                t_list.subbez = temp_list.subbez
                t_list.subgroup = temp_list.subgroup
                t_list.t_qty =  to_decimal(temp_list.t_qty)
                t_list.t_val =  to_decimal(temp_list.t_val)
                t_list.val =  to_decimal(temp_list.val)

        temp_list = query(temp_list_data, filters=(lambda temp_list: temp_list.f_lager == 9999), first=True)

        if temp_list:
            t_list = T_list()
            t_list_data.append(t_list)

            t_list.flag = temp_list.flag
            t_list.f_lager = temp_list.f_lager
            t_list.bezeich = temp_list.bezeich
            t_list.qty =  to_decimal(temp_list.qty)
            t_list.t_qty =  to_decimal(temp_list.t_qty)
            t_list.t_val =  to_decimal(temp_list.t_val)
            t_list.val =  to_decimal(temp_list.val)

    if sorttype == 1:
        create_list1()

    elif sorttype == 2:
        create_list2()

    elif sorttype == 3:
        create_list3()

    elif sorttype == 4:
        create_list4()
        create_output()

    return generate_output()

"""
"error": "Traceback (most recent call last):\n  File \"/usr1/serverless/src/main.py\", line 1722, in handle_dynamic_data\n    
output_data =  obj(**input_data)\n  File \"/usr1/serverless/src/functions/stin_summaryhis_btn_gobl.py\", 
line 616, in stin_summaryhis_btn_gobl\n    
create_list1()\n    ~~~~~~~~~~~~^^\n  File \"/usr1/serverless/src/functions/stin_summaryhis_btn_gobl.py\", line 70, 
in create_list1\n    ((L_artikel.artnr.in_(list(set([l_ophis.artnr for l_ophis in l_ophis_data if l_ophishis.lager_nr == l_lager.lager_nr] 
& (l_ophis.datum >= from_date) & (l_ophis.datum <= to_date) & (l_ophis.artnr >= from_art) 
& (l_ophis.artnr <= to_art) & (l_ophis.anzahl != 0) & (l_ophis.op_art == 1))))) & (L_artikel.zwkum >= from_grp) & (L_artikel.zwkum <= to_grp))).order_by(L_artikel.artnr).all():\n                                                                 ^^^^^^^^^^^^\nNameError: name 'l_ophis_data' is not defined\n",
        
        """