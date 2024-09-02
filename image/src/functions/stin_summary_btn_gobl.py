from functions.additional_functions import *
import decimal
from datetime import date
from models import L_lager, L_artikel, L_op, L_untergrup

def stin_summary_btn_gobl(sorttype:int, from_lager:int, to_lager:int, from_date:date, to_date:date, from_art:int, to_art:int, from_grp:int, to_grp:int):
    t_list_list = []
    l_lager = l_artikel = l_op = l_untergrup = None

    t_list = l_store = None

    t_list_list, T_list = create_model("T_list", {"flag":int, "subgroup":int, "subbez":str, "f_lager":int, "f_bezeich":str, "artnr":str, "bezeich":str, "einheit":str, "qty":decimal, "val":decimal, "t_qty":decimal, "t_val":decimal})

    L_store = L_lager

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_list_list, l_lager, l_artikel, l_op, l_untergrup
        nonlocal l_store


        nonlocal t_list, l_store
        nonlocal t_list_list
        return {"t-list": t_list_list}

    def create_list1():

        nonlocal t_list_list, l_lager, l_artikel, l_op, l_untergrup
        nonlocal l_store


        nonlocal t_list, l_store
        nonlocal t_list_list

        f_lager:int = 0
        qty:decimal = 0
        val:decimal = 0
        t_qty:decimal = 0
        t_val:decimal = 0
        m_qty:decimal = 0
        m_val:decimal = 0
        d_qty:decimal = 0
        d_val:decimal = 0
        L_store = L_lager
        t_list_list.clear()
        f_lager = 0

        for l_lager in db_session.query(L_lager).filter(
                (L_lager.lager_nr >= from_lager) &  (L_lager.lager_nr <= to_lager)).all():
            qty = 0
            val = 0
            t_qty = 0
            t_val = 0

            l_op_obj_list = []
            for l_op, l_artikel in db_session.query(L_op, L_artikel).join(L_artikel,(L_artikel.artnr == L_op.artnr) &  (L_artikel.zwkum >= from_grp) &  (L_artikel.zwkum <= to_grp)).filter(
                    (L_op.lager_nr == l_lager.lager_nr) &  (L_op.datum >= from_date) &  (L_op.datum <= to_date) &  (L_op.artnr >= from_art) &  (L_op.artnr <= to_art) &  (L_op.loeschflag <= 1) &  (L_op.anzahl != 0) &  (L_op.op_art == 1)).all():
                if l_op._recid in l_op_obj_list:
                    continue
                else:
                    l_op_obj_list.append(l_op._recid)

                if f_lager != l_lager.lager_nr and t_qty != 0:
                    t_list = T_list()
                    t_list_list.append(t_list)

                    t_list.flag = 1
                    t_list.f_lager = f_lager
                    t_list.bezeich = "TOTAL"
                    t_list.qty = qty
                    t_list.val = val
                    t_list.t_qty = t_qty
                    t_list.t_val = t_val
                    qty = 0
                    val = 0
                    t_qty = 0
                    t_val = 0
                    f_lager = l_lager.lager_nr

                t_list = query(t_list_list, filters=(lambda t_list :t_list.f_lager == l_lager.lager_nr and to_int(t_list.artnr) == l_artikel.artnr), first=True)

                if not t_list:
                    t_list = T_list()
                    t_list_list.append(t_list)

                    t_list.f_lager = l_lager.lager_nr

                    if f_lager != l_lager.lager_nr:
                        t_list.f_bezeich = l_lager.bezeich
                        f_lager = l_lager.lager_nr
                    t_list.artnr = to_string(l_op.artnr, "9999999")
                    t_list.bezeich = l_artikel.bezeich
                    t_list.einheit = l_artikel.masseinheit

                if l_op.datum == to_date:
                    t_list.qty = t_list.qty + l_op.anzahl
                    t_list.val = t_list.val + l_op.warenwert
                    qty = qty + l_op.anzahl
                    val = val + l_op.warenwert
                    d_qty = d_qty + l_op.anzahl
                    d_val = d_val + l_op.warenwert
                t_list.t_qty = t_list.t_qty + l_op.anzahl
                t_list.t_val = t_list.t_val + l_op.warenwert
                t_qty = t_qty + l_op.anzahl
                t_val = t_val + l_op.warenwert
                m_qty = m_qty + l_op.anzahl
                m_val = m_val + l_op.warenwert

            if t_qty != 0:
                t_list = T_list()
                t_list_list.append(t_list)

                t_list.flag = 1
                t_list.f_lager = f_lager
                t_list.bezeich = "TOTAL"
                t_list.qty = qty
                t_list.val = val
                t_list.t_qty = t_qty
                t_list.t_val = t_val
        t_list = T_list()
        t_list_list.append(t_list)

        t_list.flag = 1
        t_list.f_lager = 9999
        t_list.bezeich = "GRAND TOTAL"
        t_list.qty = d_qty
        t_list.val = d_val
        t_list.t_qty = m_qty
        t_list.t_val = m_val

    def create_list3():

        nonlocal t_list_list, l_lager, l_artikel, l_op, l_untergrup
        nonlocal l_store


        nonlocal t_list, l_store
        nonlocal t_list_list

        f_lager:int = 0
        qty:decimal = 0
        val:decimal = 0
        t_qty:decimal = 0
        t_val:decimal = 0
        m_qty:decimal = 0
        m_val:decimal = 0
        d_qty:decimal = 0
        d_val:decimal = 0
        st_qty:decimal = 0
        st_val:decimal = 0
        sm_qty:decimal = 0
        sm_val:decimal = 0
        subgr:str = ""
        L_store = L_lager
        t_list_list.clear()
        f_lager = 0

        for l_lager in db_session.query(L_lager).filter(
                (L_lager.lager_nr >= from_lager) &  (L_lager.lager_nr <= to_lager)).all():
            qty = 0
            val = 0
            t_qty = 0
            t_val = 0

            l_op_obj_list = []
            for l_op, l_artikel, l_untergrup in db_session.query(L_op, L_artikel, L_untergrup).join(L_artikel,(L_artikel.artnr == L_op.artnr) &  (L_artikel.zwkum >= from_grp) &  (L_artikel.zwkum <= to_grp)).join(L_untergrup,(L_untergrup.zwkum == l_artikel.zwkum)).filter(
                    (L_op.lager_nr == l_lager.lager_nr) &  (L_op.datum >= from_date) &  (L_op.datum <= to_date) &  (L_op.artnr >= from_art) &  (L_op.artnr <= to_art) &  (L_op.loeschflag <= 1) &  (L_op.anzahl != 0) &  (L_op.op_art == 1)).all():
                if l_op._recid in l_op_obj_list:
                    continue
                else:
                    l_op_obj_list.append(l_op._recid)

                if subgr != l_untergrup.bezeich and subgr != "" and sm_qty != 0:
                    t_list = T_list()
                    t_list_list.append(t_list)

                    t_list.flag = 1
                    t_list.bezeich = subgr
                    t_list.qty = st_qty
                    t_list.val = st_val
                    t_list.t_qty = sm_qty
                    t_list.t_val = sm_val
                    st_qty = 0
                    st_val = 0
                    sm_qty = 0
                    sm_val = 0

                if f_lager != l_lager.lager_nr and t_qty != 0:
                    t_list = T_list()
                    t_list_list.append(t_list)

                    t_list.flag = 1
                    t_list.f_lager = f_lager
                    t_list.bezeich = "TOTAL"
                    t_list.qty = qty
                    t_list.val = val
                    t_list.t_qty = t_qty
                    t_list.t_val = t_val
                    qty = 0
                    val = 0
                    t_qty = 0
                    t_val = 0
                    f_lager = l_lager.lager_nr

                t_list = query(t_list_list, filters=(lambda t_list :t_list.f_lager == l_lager.lager_nr and to_int(t_list.artnr) == l_artikel.artnr), first=True)

                if not t_list:
                    t_list = T_list()
                    t_list_list.append(t_list)

                    t_list.f_lager = l_lager.lager_nr

                    if f_lager != l_lager.lager_nr:
                        t_list.f_bezeich = l_lager.bezeich
                        f_lager = l_lager.lager_nr
                    t_list.artnr = to_string(l_op.artnr, "9999999")
                    t_list.bezeich = l_artikel.bezeich
                    t_list.einheit = l_artikel.masseinheit
                    t_list.subgroup = l_artikel.zwkum
                    t_list.subbez = l_untergrup.bezeich

                if l_op.datum == to_date:
                    t_list.qty = t_list.qty + l_op.anzahl
                    t_list.val = t_list.val + l_op.warenwert
                    qty = qty + l_op.anzahl
                    val = val + l_op.warenwert
                    st_qty = st_qty + l_op.anzahl
                    st_val = st_val + l_op.warenwert
                    d_qty = d_qty + l_op.anzahl
                    d_val = d_val + l_op.warenwert
                t_list.t_qty = t_list.t_qty + l_op.anzahl
                t_list.t_val = t_list.t_val + l_op.warenwert
                t_qty = t_qty + l_op.anzahl
                t_val = t_val + l_op.warenwert
                m_qty = m_qty + l_op.anzahl
                m_val = m_val + l_op.warenwert
                sm_qty = sm_qty + l_op.anzahl
                sm_val = sm_val + l_op.warenwert
                subgr = l_untergrup.bezeich

            if sm_qty != 0:
                t_list = T_list()
                t_list_list.append(t_list)

                t_list.flag = 1
                t_list.bezeich = subgr
                t_list.qty = st_qty
                t_list.val = st_val
                t_list.t_qty = sm_qty
                t_list.t_val = sm_val
                st_qty = 0
                st_val = 0
                sm_qty = 0
                sm_val = 0

            if t_qty != 0:
                t_list = T_list()
                t_list_list.append(t_list)

                t_list.flag = 1
                t_list.f_lager = f_lager
                t_list.bezeich = "TOTAL"
                t_list.qty = qty
                t_list.val = val
                t_list.t_qty = t_qty
                t_list.t_val = t_val
        t_list = T_list()
        t_list_list.append(t_list)

        t_list.flag = 1
        t_list.f_lager = 9999
        t_list.bezeich = "GRAND TOTAL"
        t_list.qty = d_qty
        t_list.val = d_val
        t_list.t_qty = m_qty
        t_list.t_val = m_val

    def create_list2():

        nonlocal t_list_list, l_lager, l_artikel, l_op, l_untergrup
        nonlocal l_store


        nonlocal t_list, l_store
        nonlocal t_list_list

        f_lager:int = 0
        qty:decimal = 0
        val:decimal = 0
        t_qty:decimal = 0
        t_val:decimal = 0
        m_qty:decimal = 0
        m_val:decimal = 0
        d_qty:decimal = 0
        d_val:decimal = 0
        L_store = L_lager
        t_list_list.clear()
        f_lager = 0

        for l_lager in db_session.query(L_lager).filter(
                (L_lager.lager_nr >= from_lager) &  (L_lager.lager_nr <= to_lager)).all():
            qty = 0
            val = 0
            t_qty = 0
            t_val = 0

            l_op_obj_list = []
            for l_op, l_artikel in db_session.query(L_op, L_artikel).join(L_artikel,(L_artikel.artnr == L_op.artnr) &  (L_artikel.zwkum >= from_grp) &  (L_artikel.zwkum <= to_grp)).filter(
                    (L_op.lager_nr == l_lager.lager_nr) &  (L_op.datum >= from_date) &  (L_op.datum <= to_date) &  (L_op.artnr >= from_art) &  (L_op.artnr <= to_art) &  (L_op.loeschflag <= 1) &  (L_op.anzahl != 0) &  (L_op.op_art == 1)).all():
                if l_op._recid in l_op_obj_list:
                    continue
                else:
                    l_op_obj_list.append(l_op._recid)

                if f_lager != l_lager.lager_nr and t_qty != 0:
                    t_list = T_list()
                    t_list_list.append(t_list)

                    t_list.flag = 1
                    t_list.f_lager = f_lager
                    t_list.bezeich = "TOTAL"
                    t_list.qty = qty
                    t_list.val = val
                    t_list.t_qty = t_qty
                    t_list.t_val = t_val
                    qty = 0
                    val = 0
                    t_qty = 0
                    t_val = 0
                    f_lager = l_lager.lager_nr

                t_list = query(t_list_list, filters=(lambda t_list :t_list.f_lager == l_lager.lager_nr and to_int(t_list.artnr) == l_artikel.artnr), first=True)

                if not t_list:
                    t_list = T_list()
                    t_list_list.append(t_list)

                    t_list.f_lager = l_lager.lager_nr

                    if f_lager != l_lager.lager_nr:
                        t_list.f_bezeich = l_lager.bezeich
                        f_lager = l_lager.lager_nr
                    t_list.artnr = to_string(l_op.artnr, "9999999")
                    t_list.bezeich = l_artikel.bezeich
                    t_list.einheit = l_artikel.masseinheit

                if l_op.datum == to_date:
                    t_list.qty = t_list.qty + l_op.anzahl
                    t_list.val = t_list.val + l_op.warenwert
                    qty = qty + l_op.anzahl
                    val = val + l_op.warenwert
                    d_qty = d_qty + l_op.anzahl
                    d_val = d_val + l_op.warenwert
                t_list.t_qty = t_list.t_qty + l_op.anzahl
                t_list.t_val = t_list.t_val + l_op.warenwert
                t_qty = t_qty + l_op.anzahl
                t_val = t_val + l_op.warenwert
                m_qty = m_qty + l_op.anzahl
                m_val = m_val + l_op.warenwert

            if t_qty != 0:
                t_list = T_list()
                t_list_list.append(t_list)

                t_list.flag = 1
                t_list.f_lager = f_lager
                t_list.bezeich = "TOTAL"
                t_list.qty = qty
                t_list.val = val
                t_list.t_qty = t_qty
                t_list.t_val = t_val
        t_list = T_list()
        t_list_list.append(t_list)

        t_list.flag = 1
        t_list.f_lager = 9999
        t_list.bezeich = "GRAND TOTAL"
        t_list.qty = d_qty
        t_list.val = d_val
        t_list.t_qty = m_qty
        t_list.t_val = m_val

    if sorttype == 1:
        create_list1()

    elif sorttype == 2:
        create_list2()
    else:
        create_list3()

    return generate_output()