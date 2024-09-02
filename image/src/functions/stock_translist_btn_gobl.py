from functions.additional_functions import *
import decimal
from datetime import date
from models import L_lager, L_artikel, L_op, L_untergrup

def stock_translist_btn_gobl(main_grp:int, sorttype:int, mattype:int, from_lager:int, to_lager:int, from_art:int, to_art:int, from_date:date, to_date:date):
    t_list_list = []
    curr_nr:int = 0
    l_lager = l_artikel = l_op = l_untergrup = None

    t_list = l_store = None

    t_list_list, T_list = create_model("T_list", {"nr":int, "f_lager":int, "t_lager":int, "f_bezeich":str, "t_bezeich":str, "artnr":str, "subgr":int, "sub_bezeich":str, "bezeich":str, "qty":decimal, "val":decimal, "t_qty":decimal, "t_val":decimal})

    L_store = L_lager

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_list_list, curr_nr, l_lager, l_artikel, l_op, l_untergrup
        nonlocal l_store


        nonlocal t_list, l_store
        nonlocal t_list_list
        return {"t-list": t_list_list}

    def create_list():

        nonlocal t_list_list, curr_nr, l_lager, l_artikel, l_op, l_untergrup
        nonlocal l_store


        nonlocal t_list, l_store
        nonlocal t_list_list

        f_lager:int = 0
        t_lager:int = 0
        qty:decimal = 0
        val:decimal = 0
        t_qty:decimal = 0
        t_val:decimal = 0
        d_qty:decimal = 0
        d_val:decimal = 0
        m_qty:decimal = 0
        m_val:decimal = 0
        L_store = L_lager

        if from_lager == to_lager:
            create_lista()

            return
        t_list_list.clear()
        f_lager = 0

        for l_lager in db_session.query(L_lager).filter(
                (L_lager.lager_nr >= from_lager) &  (L_lager.lager_nr <= to_lager)).all():
            t_lager = 0
            qty = 0
            val = 0
            t_qty = 0
            t_val = 0

            l_op_obj_list = []
            for l_op, l_artikel in db_session.query(L_op, L_artikel).join(L_artikel,(L_artikel.artnr == L_op.artnr)).filter(
                    (L_op.lager_nr == l_lager.lager_nr) &  (L_op.datum >= from_date) &  (L_op.datum <= to_date) &  (L_op.artnr >= from_art) &  (L_op.artnr <= to_art) &  (L_op.op_art == 4) &  (L_op.herkunftflag == 1)).all():
                if l_op._recid in l_op_obj_list:
                    continue
                else:
                    l_op_obj_list.append(l_op._recid)

                if (f_lager != l_lager.lager_nr or t_lager != l_op.pos) and t_qty != 0:
                    t_list = T_list()
                    t_list_list.append(t_list)

                    curr_nr = curr_nr + 1
                    t_list.nr = curr_nr
                    t_list.bezeich = "Total"
                    t_list.qty = qty
                    t_list.val = val
                    t_list.t_qty = t_qty
                    t_list.t_val = t_val
                    qty = 0
                    val = 0
                    t_qty = 0
                    t_val = 0

                t_list = query(t_list_list, filters=(lambda t_list :t_list.f_lager == l_lager.lager_nr and t_list.t_lager == l_op.pos and to_int(t_list.artnr) == l_artikel.artnr), first=True)

                if not t_list:

                    l_store = db_session.query(L_store).filter(
                            (L_store.lager_nr == l_op.pos)).first()
                    t_list = T_list()
                    t_list_list.append(t_list)

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

                curr_nr = curr_nr + 1
                t_list.nr = curr_nr
                t_list.bezeich = "Total"
                t_list.qty = qty
                t_list.val = val
                t_list.t_qty = t_qty
                t_list.t_val = t_val

        if m_qty != 0:
            t_list = T_list()
            t_list_list.append(t_list)

            curr_nr = curr_nr + 1
            t_list.nr = curr_nr
            t_list.bezeich = "GRAND TOTAL"
            t_list.qty = d_qty
            t_list.val = d_val
            t_list.t_qty = m_qty
            t_list.t_val = m_val

    def create_lista():

        nonlocal t_list_list, curr_nr, l_lager, l_artikel, l_op, l_untergrup
        nonlocal l_store


        nonlocal t_list, l_store
        nonlocal t_list_list

        f_lager:int = 0
        t_lager:int = 0
        qty:decimal = 0
        val:decimal = 0
        t_qty:decimal = 0
        t_val:decimal = 0
        d_qty:decimal = 0
        d_val:decimal = 0
        m_qty:decimal = 0
        m_val:decimal = 0
        L_store = L_lager
        t_list_list.clear()

        l_lager = db_session.query(L_lager).filter(
                (L_lager.lager_nr == from_lager)).first()
        t_lager = 0
        qty = 0
        val = 0
        t_qty = 0
        t_val = 0
        d_qty = 0
        d_val = 0
        m_qty = 0
        m_val = 0

        l_op_obj_list = []
        for l_op, l_artikel in db_session.query(L_op, L_artikel).join(L_artikel,(L_artikel.artnr == L_op.artnr)).filter(
                (L_op.lager_nr == l_lager.lager_nr) &  (L_op.datum >= from_date) &  (L_op.datum <= to_date) &  (L_op.artnr >= from_art) &  (L_op.artnr <= to_art) &  (L_op.op_art == 4) &  (L_op.herkunftflag == 1) &  (L_op.loeschflag <= 1)).all():
            if l_op._recid in l_op_obj_list:
                continue
            else:
                l_op_obj_list.append(l_op._recid)

            if t_lager == 0:
                t_lager = l_op.pos

            if t_lager != l_op.pos and t_qty != 0:
                t_list = T_list()
                t_list_list.append(t_list)

                curr_nr = curr_nr + 1
                t_list.nr = curr_nr
                t_list.bezeich = "Total"
                t_list.qty = qty
                t_list.val = val
                t_list.t_qty = t_qty
                t_list.t_val = t_val
                qty = 0
                val = 0
                t_qty = 0
                t_val = 0
                t_lager = l_op.pos

            t_list = query(t_list_list, filters=(lambda t_list :t_list.f_lager == l_lager.lager_nr and t_list.t_lager == l_op.pos and to_int(t_list.artnr) == l_artikel.artnr), first=True)

            if not t_list:

                l_store = db_session.query(L_store).filter(
                        (L_store.lager_nr == l_op.pos)).first()
                t_list = T_list()
                t_list_list.append(t_list)

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

            curr_nr = curr_nr + 1
            t_list.nr = curr_nr
            t_list.bezeich = "Total"
            t_list.qty = qty
            t_list.val = val
            t_list.t_qty = t_qty
            t_list.t_val = t_val

        if m_qty != 0:
            t_list = T_list()
            t_list_list.append(t_list)

            curr_nr = curr_nr + 1
            t_list.nr = curr_nr
            t_list.bezeich = "GRAND TOTAL"
            t_list.qty = d_qty
            t_list.val = d_val
            t_list.t_qty = m_qty
            t_list.t_val = m_val


        t_lager = 0
        qty = 0
        val = 0
        t_qty = 0
        t_val = 0
        d_qty = 0
        d_val = 0
        m_qty = 0
        m_val = 0

        l_op_obj_list = []
        for l_op, l_artikel in db_session.query(L_op, L_artikel).join(L_artikel,(L_artikel.artnr == L_op.artnr)).filter(
                (L_op.lager_nr == l_lager.lager_nr) &  (L_op.datum >= from_date) &  (L_op.datum <= to_date) &  (L_op.artnr >= from_art) &  (L_op.artnr <= to_art) &  (L_op.op_art == 2) &  (L_op.herkunftflag == 1) &  (L_op.loeschflag <= 1)).all():
            if l_op._recid in l_op_obj_list:
                continue
            else:
                l_op_obj_list.append(l_op._recid)

            if t_lager == 0:
                t_lager = l_op.pos

            if t_lager != l_op.pos and t_qty != 0:
                t_list = T_list()
                t_list_list.append(t_list)

                curr_nr = curr_nr + 1
                t_list.nr = curr_nr
                t_list.bezeich = "Total"
                t_list.qty = qty
                t_list.val = val
                t_list.t_qty = t_qty
                t_list.t_val = t_val
                qty = 0
                val = 0
                t_qty = 0
                t_val = 0
                t_lager = l_op.pos

            t_list = query(t_list_list, filters=(lambda t_list :t_list.t_lager == l_lager.lager_nr and t_list.f_lager == l_op.pos and to_int(t_list.artnr) == l_artikel.artnr), first=True)

            if not t_list:

                l_store = db_session.query(L_store).filter(
                        (L_store.lager_nr == l_op.pos)).first()
                t_list = T_list()
                t_list_list.append(t_list)

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

            curr_nr = curr_nr + 1
            t_list.nr = curr_nr
            t_list.bezeich = "Total"
            t_list.qty = qty
            t_list.val = val
            t_list.t_qty = t_qty
            t_list.t_val = t_val

        if m_qty != 0:
            t_list = T_list()
            t_list_list.append(t_list)

            curr_nr = curr_nr + 1
            t_list.nr = curr_nr
            t_list.bezeich = "GRAND TOTAL"
            t_list.qty = d_qty
            t_list.val = d_val
            t_list.t_qty = m_qty
            t_list.t_val = m_val

    def list_subgroup():

        nonlocal t_list_list, curr_nr, l_lager, l_artikel, l_op, l_untergrup
        nonlocal l_store


        nonlocal t_list, l_store
        nonlocal t_list_list

        last_sub:str = ""
        to_store:int = 0
        f_lager:int = 0
        t_lager:int = 0
        t_subgr:int = 0
        qty:decimal = 0
        val:decimal = 0
        t_qty:decimal = 0
        t_val:decimal = 0
        d_qty:decimal = 0
        d_val:decimal = 0
        m_qty:decimal = 0
        m_val:decimal = 0
        subd_qty:decimal = 0
        subd_val:decimal = 0
        subm_qty:decimal = 0
        subm_val:decimal = 0
        L_store = L_lager
        t_list_list.clear()
        f_lager = 0

        for l_lager in db_session.query(L_lager).filter(
                (L_lager.lager_nr >= from_lager) &  (L_lager.lager_nr <= to_lager)).all():
            t_lager = 0
            qty = 0
            val = 0
            t_qty = 0
            t_val = 0

            l_op_obj_list = []
            for l_op, l_artikel, l_untergrup in db_session.query(L_op, L_artikel, L_untergrup).join(L_artikel,(L_artikel.artnr == L_op.artnr)).join(L_untergrup,(L_untergrup.zwkum == l_artikel.zwkum)).filter(
                    (L_op.lager_nr == l_lager.lager_nr) &  (L_op.datum >= from_date) &  (L_op.datum <= to_date) &  (L_op.artnr >= from_art) &  (L_op.artnr <= to_art) &  (L_op.op_art == 4) &  (L_op.herkunftflag == 1)).all():
                if l_op._recid in l_op_obj_list:
                    continue
                else:
                    l_op_obj_list.append(l_op._recid)

                if to_store != l_op.pos and subm_qty != 0 or (t_subgr != 0 and t_subgr != l_artikel.zwkum):
                    t_list = T_list()
                    t_list_list.append(t_list)

                    curr_nr = curr_nr + 1
                    t_list.nr = curr_nr
                    t_list.bezeich = "SubTotal"
                    t_list.qty = subd_qty
                    t_list.val = subd_val
                    t_list.t_qty = subm_qty
                    t_list.t_val = subm_val
                    subd_qty = 0
                    subd_val = 0
                    subm_qty = 0
                    subm_val = 0


                to_store = l_op.pos

                if t_subgr != l_artikel.zwkum and t_qty != 0:
                    t_list = T_list()
                    t_list_list.append(t_list)

                    curr_nr = curr_nr + 1
                    t_list.nr = curr_nr
                    t_list.bezeich = "Total " + last_sub
                    t_list.qty = qty
                    t_list.val = val
                    t_list.t_qty = t_qty
                    t_list.t_val = t_val
                    qty = 0
                    val = 0
                    t_qty = 0
                    t_val = 0

                t_list = query(t_list_list, filters=(lambda t_list :t_list.subgr == l_artikel.zwkum and t_list.f_lager == l_lager.lager_nr and t_list.t_lager == l_op.pos and to_int(t_list.artnr) == l_artikel.artnr), first=True)

                if not t_list:

                    l_store = db_session.query(L_store).filter(
                            (L_store.lager_nr == l_op.pos)).first()
                    t_list = T_list()
                    t_list_list.append(t_list)

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
                    t_list.qty = t_list.qty + l_op.anzahl
                    t_list.val = t_list.val + l_op.warenwert
                    qty = qty + l_op.anzahl
                    val = val + l_op.warenwert
                    d_qty = d_qty + l_op.anzahl
                    d_val = d_val + l_op.warenwert
                    subd_qty = subd_qty + l_op.anzahl
                    subd_val = subd_val + l_op.warenwert
                t_list.t_qty = t_list.t_qty + l_op.anzahl
                t_list.t_val = t_list.t_val + l_op.warenwert
                t_qty = t_qty + l_op.anzahl
                t_val = t_val + l_op.warenwert
                m_qty = m_qty + l_op.anzahl
                m_val = m_val + l_op.warenwert
                subm_qty = subm_qty + l_op.anzahl
                subm_val = subm_val + l_op.warenwert

            if subm_qty != 0:
                t_list = T_list()
                t_list_list.append(t_list)

                curr_nr = curr_nr + 1
                t_list.nr = curr_nr
                t_list.bezeich = "SubTotal"
                t_list.qty = subd_qty
                t_list.val = subd_val
                t_list.t_qty = subm_qty
                t_list.t_val = subm_val
                subd_qty = 0
                subd_val = 0
                subm_qty = 0
                subm_val = 0

            if t_qty != 0:
                t_list = T_list()
                t_list_list.append(t_list)

                curr_nr = curr_nr + 1
                t_list.nr = curr_nr
                t_list.bezeich = "Total " + last_sub
                t_list.qty = qty
                t_list.val = val
                t_list.t_qty = t_qty
                t_list.t_val = t_val

        if m_qty != 0:
            t_list = T_list()
            t_list_list.append(t_list)

            curr_nr = curr_nr + 1
            t_list.nr = curr_nr
            t_list.bezeich = "GRAND TOTAL"
            t_list.qty = d_qty
            t_list.val = d_val
            t_list.t_qty = m_qty
            t_list.t_val = m_val

    def create_list1():

        nonlocal t_list_list, curr_nr, l_lager, l_artikel, l_op, l_untergrup
        nonlocal l_store


        nonlocal t_list, l_store
        nonlocal t_list_list

        f_lager:int = 0
        t_lager:int = 0
        qty:decimal = 0
        val:decimal = 0
        t_qty:decimal = 0
        t_val:decimal = 0
        d_qty:decimal = 0
        d_val:decimal = 0
        m_qty:decimal = 0
        m_val:decimal = 0
        do_it:bool = False
        L_store = L_lager
        t_list_list.clear()
        f_lager = 0

        for l_lager in db_session.query(L_lager).filter(
                (L_lager.lager_nr >= from_lager) &  (L_lager.lager_nr <= to_lager)).all():
            t_lager = 0
            qty = 0
            val = 0
            t_qty = 0
            t_val = 0

            l_op_obj_list = []
            for l_op, l_artikel, l_untergrup in db_session.query(L_op, L_artikel, L_untergrup).join(L_artikel,(L_artikel.artnr == L_op.artnr) &  (L_artikel.endkum == main_grp)).join(L_untergrup,(L_untergrup.zwkum == l_artikel.zwkum)).filter(
                    (L_op.lager_nr == l_lager.lager_nr) &  (L_op.datum >= from_date) &  (L_op.datum <= to_date) &  (L_op.artnr >= from_art) &  (L_op.artnr <= to_art) &  (L_op.op_art == 4) &  (L_op.herkunftflag == 1)).all():
                if l_op._recid in l_op_obj_list:
                    continue
                else:
                    l_op_obj_list.append(l_op._recid)


                do_it = True

                if (mattype == 1 and l_untergrup.betriebsnr == 1) or (mattype == 2 and l_untergrup.betriebsnr == 0):
                    do_it = False

                if (f_lager != l_lager.lager_nr or t_lager != l_op.pos) and t_qty != 0:
                    t_list = T_list()
                    t_list_list.append(t_list)

                    curr_nr = curr_nr + 1
                    t_list.nr = curr_nr
                    t_list.bezeich = "Total"
                    t_list.qty = qty
                    t_list.val = val
                    t_list.t_qty = t_qty
                    t_list.t_val = t_val
                    qty = 0
                    val = 0
                    t_qty = 0
                    t_val = 0

                if do_it:

                    t_list = query(t_list_list, filters=(lambda t_list :t_list.f_lager == l_lager.lager_nr and t_list.t_lager == l_op.pos and to_int(t_list.artnr) == l_artikel.artnr), first=True)

                    if not t_list:

                        l_store = db_session.query(L_store).filter(
                                (L_store.lager_nr == l_op.pos)).first()
                        t_list = T_list()
                        t_list_list.append(t_list)

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

                curr_nr = curr_nr + 1
                t_list.nr = curr_nr
                t_list.bezeich = "Total"
                t_list.qty = qty
                t_list.val = val
                t_list.t_qty = t_qty
                t_list.t_val = t_val

        if m_qty != 0:
            t_list = T_list()
            t_list_list.append(t_list)

            curr_nr = curr_nr + 1
            t_list.nr = curr_nr
            t_list.bezeich = "GRAND TOTAL"
            t_list.qty = d_qty
            t_list.val = d_val
            t_list.t_qty = m_qty
            t_list.t_val = m_val

    def list_subgroup1():

        nonlocal t_list_list, curr_nr, l_lager, l_artikel, l_op, l_untergrup
        nonlocal l_store


        nonlocal t_list, l_store
        nonlocal t_list_list

        t_subgr:int = 0
        f_lager:int = 0
        t_lager:int = 0
        qty:decimal = 0
        val:decimal = 0
        t_qty:decimal = 0
        t_val:decimal = 0
        d_qty:decimal = 0
        d_val:decimal = 0
        m_qty:decimal = 0
        m_val:decimal = 0
        do_it:bool = False
        to_store:int = 0
        subd_qty:decimal = 0
        subd_val:decimal = 0
        subm_qty:decimal = 0
        subm_val:decimal = 0
        last_sub:str = ""
        L_store = L_lager
        t_list_list.clear()
        f_lager = 0

        for l_lager in db_session.query(L_lager).filter(
                (L_lager.lager_nr >= from_lager) &  (L_lager.lager_nr <= to_lager)).all():
            t_lager = 0
            qty = 0
            val = 0
            t_qty = 0
            t_val = 0

            l_op_obj_list = []
            for l_op, l_artikel, l_untergrup in db_session.query(L_op, L_artikel, L_untergrup).join(L_artikel,(L_artikel.artnr == L_op.artnr) &  (L_artikel.endkum == main_grp)).join(L_untergrup,(L_untergrup.zwkum == l_artikel.zwkum)).filter(
                    (L_op.lager_nr == l_lager.lager_nr) &  (L_op.datum >= from_date) &  (L_op.datum <= to_date) &  (L_op.artnr >= from_art) &  (L_op.artnr <= to_art) &  (L_op.op_art == 4) &  (L_op.herkunftflag == 1)).all():
                if l_op._recid in l_op_obj_list:
                    continue
                else:
                    l_op_obj_list.append(l_op._recid)


                do_it = True

                if (mattype == 1 and l_untergrup.betriebsnr == 1) or (mattype == 2 and l_untergrup.betriebsnr == 0):
                    do_it = False

                if do_it:

                    if to_store != l_op.pos and subm_qty != 0 or (t_subgr != 0 and t_subgr != l_artikel.zwkum):
                        t_list = T_list()
                        t_list_list.append(t_list)

                        curr_nr = curr_nr + 1
                        t_list.nr = curr_nr
                        t_list.bezeich = "SubTotal"
                        t_list.qty = subd_qty
                        t_list.val = subd_val
                        t_list.t_qty = subm_qty
                        t_list.t_val = subm_val
                        subd_qty = 0
                        subd_val = 0
                        subm_qty = 0
                        subm_val = 0


                    to_store = l_op.pos

                    if (t_subgr != l_artikel.zwkum) and t_qty != 0:
                        t_list = T_list()
                        t_list_list.append(t_list)

                        curr_nr = curr_nr + 1
                        t_list.nr = curr_nr
                        t_list.bezeich = "Total " + last_sub
                        t_list.qty = qty
                        t_list.val = val
                        t_list.t_qty = t_qty
                        t_list.t_val = t_val
                        qty = 0
                        val = 0
                        t_qty = 0
                        t_val = 0

                    t_list = query(t_list_list, filters=(lambda t_list :t_list.subgr == l_artikel.zwkum and t_list.f_lager == l_lager.lager_nr and t_list.t_lager == l_op.pos and to_int(t_list.artnr) == l_artikel.artnr), first=True)

                    if not t_list:

                        l_store = db_session.query(L_store).filter(
                                (L_store.lager_nr == l_op.pos)).first()
                        t_list = T_list()
                        t_list_list.append(t_list)

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
                        t_list.qty = t_list.qty + l_op.anzahl
                        t_list.val = t_list.val + l_op.warenwert
                        qty = qty + l_op.anzahl
                        val = val + l_op.warenwert
                        d_qty = d_qty + l_op.anzahl
                        d_val = d_val + l_op.warenwert
                        subd_qty = subd_qty + l_op.anzahl
                        subd_val = subd_val + l_op.warenwert
                    t_list.t_qty = t_list.t_qty + l_op.anzahl
                    t_list.t_val = t_list.t_val + l_op.warenwert
                    t_qty = t_qty + l_op.anzahl
                    t_val = t_val + l_op.warenwert
                    m_qty = m_qty + l_op.anzahl
                    m_val = m_val + l_op.warenwert
                    subm_qty = subm_qty + l_op.anzahl
                    subm_val = subm_val + l_op.warenwert

            if subm_qty != 0:
                t_list = T_list()
                t_list_list.append(t_list)

                curr_nr = curr_nr + 1
                t_list.nr = curr_nr
                t_list.bezeich = "SubTotal"
                t_list.qty = subd_qty
                t_list.val = subd_val
                t_list.t_qty = subm_qty
                t_list.t_val = subm_val
                subd_qty = 0
                subd_val = 0
                subm_qty = 0
                subm_val = 0

            if t_qty != 0:
                t_list = T_list()
                t_list_list.append(t_list)

                curr_nr = curr_nr + 1
                t_list.nr = curr_nr
                t_list.bezeich = "Total " + last_sub
                t_list.qty = qty
                t_list.val = val
                t_list.t_qty = t_qty
                t_list.t_val = t_val

        if m_qty != 0:
            t_list = T_list()
            t_list_list.append(t_list)

            curr_nr = curr_nr + 1
            t_list.nr = curr_nr
            t_list.bezeich = "GRAND TOTAL"
            t_list.qty = d_qty
            t_list.val = d_val
            t_list.t_qty = m_qty
            t_list.t_val = m_val

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