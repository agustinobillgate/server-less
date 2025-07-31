#using conversion tools version: 1.0.0.117
#-----------------------------------------
# Rd, 25/7/2025
# gitlab: 648
#-----------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_op, Bediener, L_artikel, L_ophdr, Queasy, Dml_art, Dml_artdep, L_bestand, L_lieferant, L_liefumsatz, Reslin_queasy, Htparam, Gl_acct, L_kredit, Ap_journal, L_pprice

op_list_data, Op_list = create_model_like(L_op, {"bezeich":string, "username":string, "dml_code":string})

def dml_stockin_btn_go_webbl(pvilanguage:int, op_list_data:[Op_list], curr_dept:int, billdate:date, curr_lager:int, lscheinnr:string, lief_nr:int, f_endkum:int, b_endkum:int, m_endkum:int, fb_closedate:date, m_closedate:date, user_init:string, t_amount:Decimal):

    prepare_cache ([L_op, Bediener, L_artikel, L_ophdr, L_bestand, L_liefumsatz, Reslin_queasy, Htparam, L_kredit, Ap_journal, L_pprice])

    s_artnr = 0
    qty = to_decimal("0.0")
    price = to_decimal("0.0")
    err_code = 0
    msg_str = ""
    curr_pos:int = 0
    created:bool = False
    dml_code:string = ""
    lvcarea:string = "dml-stockin"
    l_op = bediener = l_artikel = l_ophdr = queasy = dml_art = dml_artdep = l_bestand = l_lieferant = l_liefumsatz = reslin_queasy = htparam = gl_acct = l_kredit = ap_journal = l_pprice = None

    op_list = t_op_list = sys_user = l_art = None

    t_op_list_data, T_op_list = create_model_like(L_op, {"bezeich":string, "username":string, "dml_code":string})

    Sys_user = create_buffer("Sys_user",Bediener)
    L_art = create_buffer("L_art",L_artikel)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal s_artnr, qty, price, err_code, msg_str, curr_pos, created, dml_code, lvcarea, l_op, bediener, l_artikel, l_ophdr, queasy, dml_art, dml_artdep, l_bestand, l_lieferant, l_liefumsatz, reslin_queasy, htparam, gl_acct, l_kredit, ap_journal, l_pprice
        nonlocal pvilanguage, curr_dept, billdate, curr_lager, lscheinnr, lief_nr, f_endkum, b_endkum, m_endkum, fb_closedate, m_closedate, user_init, t_amount
        nonlocal sys_user, l_art


        nonlocal op_list, t_op_list, sys_user, l_art
        nonlocal t_op_list_data

        return {"op-list": op_list_data, "t_amount": t_amount, "s_artnr": s_artnr, "qty": qty, "price": price, "err_code": err_code, "msg_str": msg_str}

    def l_op_pos():

        nonlocal s_artnr, qty, price, err_code, msg_str, curr_pos, created, dml_code, lvcarea, l_op, bediener, l_artikel, l_ophdr, queasy, dml_art, dml_artdep, l_bestand, l_lieferant, l_liefumsatz, reslin_queasy, htparam, gl_acct, l_kredit, ap_journal, l_pprice
        nonlocal pvilanguage, curr_dept, billdate, curr_lager, lscheinnr, lief_nr, f_endkum, b_endkum, m_endkum, fb_closedate, m_closedate, user_init, t_amount
        nonlocal sys_user, l_art


        nonlocal op_list, t_op_list, sys_user, l_art
        nonlocal t_op_list_data

        pos = 0
        l_op1 = None

        def generate_inner_output():
            return (pos)

        L_op1 =  create_buffer("L_op1",L_op)
        pos = 1

        return generate_inner_output()


    def create_l_op():

        nonlocal s_artnr, qty, price, err_code, msg_str, curr_pos, created, dml_code, lvcarea, l_op, bediener, l_artikel, l_ophdr, queasy, dml_art, dml_artdep, l_bestand, l_lieferant, l_liefumsatz, reslin_queasy, htparam, gl_acct, l_kredit, ap_journal, l_pprice
        nonlocal pvilanguage, curr_dept, billdate, curr_lager, lscheinnr, lief_nr, f_endkum, b_endkum, m_endkum, fb_closedate, m_closedate, user_init, t_amount
        nonlocal sys_user, l_art


        nonlocal op_list, t_op_list, sys_user, l_art
        nonlocal t_op_list_data

        anzahl:Decimal = to_decimal("0.0")
        wert:Decimal = to_decimal("0.0")
        tot_anz:Decimal = to_decimal("0.0")
        tot_wert:Decimal = to_decimal("0.0")
        avrg_price:Decimal = to_decimal("0.0")
        dmlcode:string = ""
        d_art = None
        d_art1 = None
        D_art =  create_buffer("D_art",Dml_art)
        D_art1 =  create_buffer("D_art1",Dml_artdep)
        anzahl =  to_decimal(qty)
        wert =  to_decimal(qty) * to_decimal(price)
        wert = to_decimal(round(wert , 2))

        if ((l_artikel.endkum == f_endkum or l_artikel.endkum == b_endkum) and billdate <= fb_closedate) or (l_artikel.endkum >= m_endkum and billdate <= m_closedate):

            l_bestand = get_cache (L_bestand, {"lager_nr": [(eq, 0)],"artnr": [(eq, s_artnr)]})

            if not l_bestand:
                l_bestand = L_bestand()
                db_session.add(l_bestand)

                l_bestand.artnr = s_artnr
                l_bestand.anf_best_dat = billdate
            l_bestand.anz_eingang =  to_decimal(l_bestand.anz_eingang) + to_decimal(anzahl)
            l_bestand.wert_eingang =  to_decimal(l_bestand.wert_eingang) + to_decimal(wert)
            pass
            tot_anz =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)
            tot_wert =  to_decimal(l_bestand.val_anf_best) + to_decimal(l_bestand.wert_eingang) - to_decimal(l_bestand.wert_ausgang)

            if tot_anz != 0:
                avrg_price =  to_decimal(tot_wert) / to_decimal(tot_anz)
                pass
                l_artikel.vk_preis =  to_decimal(avrg_price)
                pass

            l_bestand = get_cache (L_bestand, {"lager_nr": [(eq, curr_lager)],"artnr": [(eq, s_artnr)]})

            if not l_bestand:
                l_bestand = L_bestand()
                db_session.add(l_bestand)

                l_bestand.lager_nr = curr_lager
                l_bestand.artnr = s_artnr
                l_bestand.anf_best_dat = billdate


            l_bestand.anz_eingang =  to_decimal(l_bestand.anz_eingang) + to_decimal(anzahl)
            l_bestand.wert_eingang =  to_decimal(l_bestand.wert_eingang) + to_decimal(wert)


            pass

        l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, lief_nr)]})

        if l_lieferant:

            l_liefumsatz = get_cache (L_liefumsatz, {"lief_nr": [(eq, lief_nr)],"datum": [(eq, billdate)]})

            if not l_liefumsatz:
                l_liefumsatz = L_liefumsatz()
                db_session.add(l_liefumsatz)

                l_liefumsatz.datum = billdate
                l_liefumsatz.lief_nr = lief_nr


            l_liefumsatz.gesamtumsatz =  to_decimal(l_liefumsatz.gesamtumsatz) + to_decimal(wert)
            pass
        l_op = L_op()
        db_session.add(l_op)

        l_op.lief_nr = lief_nr
        l_op.datum = billdate
        l_op.lager_nr = curr_lager
        l_op.artnr = s_artnr
        l_op.zeit = get_current_time_in_seconds()
        l_op.anzahl =  to_decimal(anzahl)
        l_op.einzelpreis =  to_decimal(price)
        l_op.warenwert =  to_decimal(wert)
        l_op.op_art = 1
        l_op.herkunftflag = 1
        l_op.docu_nr = dml_code
        l_op.lscheinnr = lscheinnr
        l_op.pos = curr_pos
        l_op.fuellflag = bediener.nr


        pass

        if curr_dept == 0:

            d_art = db_session.query(D_art).filter(
                         (D_art.artnr == s_artnr) & (D_art.datum == billdate) & (num_entries(D_art.chginit, ";") != 1)).first()

            if d_art:

                if entry(1, d_art.chginit, ";") != "" and entry(1, d_art.chginit, ";") == (dml_code).lower() :
                    pass
                    d_art.geliefert =  to_decimal(d_art.geliefert) + to_decimal(anzahl)
                    pass
            else:

                d_art = db_session.query(D_art).filter(
                             (D_art.artnr == s_artnr) & (D_art.datum == billdate)).first()

                if d_art:
                    pass
                    d_art.geliefert =  to_decimal(d_art.geliefert) + to_decimal(anzahl)
                    pass

        elif curr_dept > 0:

            d_art1 = db_session.query(D_art1).filter(
                         (D_art1.artnr == s_artnr) & (D_art1.datum == billdate) & (D_art1.departement == curr_dept) & (num_entries(D_art1.chginit, ";") > 1) & (entry(1, D_art1.chginit, ";") == (dml_code).lower())).first()

            if d_art1:

                if entry(1, d_art1.chginit, ";") != "" and entry(1, d_art1.chginit, ";") == (dml_code).lower() :
                    pass
                    d_art1.geliefert =  to_decimal(d_art1.geliefert) + to_decimal(anzahl)
                    pass
            else:

                reslin_queasy = db_session.query(Reslin_queasy).filter(
                             (Reslin_queasy.key == ("DML").lower()) & (Reslin_queasy.date1 == billdate) & (to_int(entry(0, Reslin_queasy.char1, ";")) == s_artnr) & (to_int(entry(1, Reslin_queasy.char1, ";")) == curr_dept) & (num_entries(Reslin_queasy.char3, ";") > 1) & (entry(1, Reslin_queasy.char3, ";") == (dml_code).lower())).first()

                if reslin_queasy:

                    if entry(1, reslin_queasy.char3, ";") != "" and entry(1, reslin_queasy.char3, ";") == (dml_code).lower() :
                        pass
                        reslin_queasy.deci3 =  to_decimal(reslin_queasy.deci3) + to_decimal(anzahl)


                        pass
                else:

                    d_art1 = db_session.query(D_art1).filter(
                                 (D_art1.artnr == s_artnr) & (D_art1.datum == billdate) & (D_art1.departement == curr_dept) & (num_entries(D_art1.chginit, ";") != 1)).first()

                    if d_art1:

                        if entry(1, d_art1.chginit, ";") != "" and entry(1, d_art1.chginit, ";") == (dml_code).lower() :
                            pass
                            d_art1.geliefert =  to_decimal(d_art1.geliefert) + to_decimal(anzahl)
                            pass
        create_purchase_book(s_artnr, price, anzahl, billdate, lief_nr)

        if (l_artikel.ek_aktuell != price) and price != 0:
            pass
            l_artikel.ek_letzter =  to_decimal(l_artikel.ek_aktuell)
            l_artikel.ek_aktuell =  to_decimal(price)


            pass

        return
        msg_str = msg_str + chr_unicode(2) + translateExtended ("Incoming record can not be ctreated : ", lvcarea, "") + to_string(s_artnr, "9999999")


    def create_ap():

        nonlocal s_artnr, qty, price, err_code, msg_str, curr_pos, created, dml_code, lvcarea, l_op, bediener, l_artikel, l_ophdr, queasy, dml_art, dml_artdep, l_bestand, l_lieferant, l_liefumsatz, reslin_queasy, htparam, gl_acct, l_kredit, ap_journal, l_pprice
        nonlocal pvilanguage, curr_dept, billdate, curr_lager, lscheinnr, lief_nr, f_endkum, b_endkum, m_endkum, fb_closedate, m_closedate, user_init, t_amount
        nonlocal sys_user, l_art


        nonlocal op_list, t_op_list, sys_user, l_art
        nonlocal t_op_list_data

        ap_license:bool = False
        ap_acct:string = ""
        do_it:bool = True
        l_op1 = None
        L_op1 =  create_buffer("L_op1",L_op)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 1016)]})
        ap_license = htparam.flogical

        if not ap_license:

            return

        l_op1 = get_cache (L_op, {"lscheinnr": [(eq, lscheinnr)],"loeschflag": [(eq, 0)],"pos": [(ge, 1)]})

        if not l_op1:
            err_code = 1

            return

        htparam = get_cache (Htparam, {"paramnr": [(eq, 986)]})
        ap_acct = htparam.fchar

        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, ap_acct)]})

        if not gl_acct:
            do_it = False

        if not do_it:

            return
        l_kredit = L_kredit()
        db_session.add(l_kredit)

        l_kredit.name = lscheinnr
        l_kredit.lief_nr = lief_nr
        l_kredit.lscheinnr = lscheinnr
        l_kredit.rgdatum = billdate
        l_kredit.datum = None
        l_kredit.saldo =  to_decimal(t_amount)
        l_kredit.ziel = 30
        l_kredit.netto =  to_decimal(t_amount)
        l_kredit.bediener_nr = bediener.nr


        ap_journal = Ap_journal()
        db_session.add(ap_journal)

        ap_journal.lief_nr = lief_nr
        ap_journal.docu_nr = lscheinnr
        ap_journal.lscheinnr = lscheinnr
        ap_journal.rgdatum = billdate
        ap_journal.saldo =  to_decimal(t_amount)
        ap_journal.netto =  to_decimal(t_amount)
        ap_journal.userinit = bediener.userinit
        ap_journal.zeit = get_current_time_in_seconds()


    def create_purchase_book(s_artnr:int, price:Decimal, qty:Decimal, datum:date, lief_nr:int):

        nonlocal err_code, msg_str, curr_pos, dml_code, lvcarea, l_op, bediener, l_artikel, l_ophdr, queasy, dml_art, dml_artdep, l_bestand, l_lieferant, l_liefumsatz, reslin_queasy, htparam, gl_acct, l_kredit, ap_journal, l_pprice
        nonlocal pvilanguage, curr_dept, billdate, curr_lager, lscheinnr, f_endkum, b_endkum, m_endkum, fb_closedate, m_closedate, user_init, t_amount
        nonlocal sys_user, l_art


        nonlocal op_list, t_op_list, sys_user, l_art
        nonlocal t_op_list_data

        max_anz:int = 0
        curr_anz:int = 0
        created:bool = False
        i:int = 0
        l_art = None
        l_price1 = None
        L_art =  create_buffer("L_art",L_artikel)
        L_price1 =  create_buffer("L_price1",L_pprice)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 225)]})
        max_anz = htparam.finteger

        if max_anz == 0:
            max_anz = 1

        l_art = get_cache (L_artikel, {"artnr": [(eq, s_artnr)]})
        curr_anz = l_art.lieferfrist

        if curr_anz >= max_anz:

            l_price1 = get_cache (L_pprice, {"artnr": [(eq, s_artnr)],"counter": [(eq, 1)]})

            if l_price1:
                l_price1.docu_nr = lscheinnr
                l_price1.artnr = s_artnr
                l_price1.anzahl =  to_decimal(qty)
                l_price1.einzelpreis =  to_decimal(price)
                l_price1.warenwert =  to_decimal(qty) * to_decimal(price)
                l_price1.bestelldatum = datum
                l_price1.lief_nr = lief_nr
                l_price1.counter = 0


                created = True
            for i in range(2,curr_anz + 1) :

                l_pprice = get_cache (L_pprice, {"artnr": [(eq, s_artnr)],"counter": [(eq, i)]})

                if l_pprice:
                    pass
                    l_pprice.counter = l_pprice.counter - 1
                    pass

            if created:
                l_price1.counter = curr_anz
                pass

        if not created:
            l_pprice = L_pprice()
            db_session.add(l_pprice)

            l_pprice.docu_nr = lscheinnr
            l_pprice.artnr = s_artnr
            l_pprice.anzahl =  to_decimal(qty)
            l_pprice.einzelpreis =  to_decimal(price)
            l_pprice.warenwert =  to_decimal(qty) * to_decimal(price)
            l_pprice.bestelldatum = datum
            l_pprice.lief_nr = lief_nr
            l_pprice.counter = curr_anz + 1


            pass
            pass
            l_art.lieferfrist = curr_anz + 1
            pass

    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

    l_ophdr = get_cache (L_ophdr, {"lscheinnr": [(eq, lscheinnr)],"op_typ": [(eq, "sti")]})

    if not l_ophdr:
        l_ophdr = L_ophdr()
        db_session.add(l_ophdr)

        l_ophdr.datum = billdate
        l_ophdr.lager_nr = curr_lager
        l_ophdr.lscheinnr = lscheinnr
        l_ophdr.op_typ = "STI"
        pass
    curr_pos = l_op_pos()
    curr_pos = curr_pos - 1
    t_amount =  to_decimal("0")

    for op_list in query(op_list_data):
        op_list.docu_nr = lscheinnr
        op_list.lscheinnr = lscheinnr
        curr_pos = curr_pos + 1
        s_artnr = op_list.artnr
        qty =  to_decimal(op_list.anzahl)
        price =  to_decimal(op_list.warenwert) / to_decimal(qty)
        t_amount =  to_decimal(t_amount) + to_decimal(op_list.warenwert)
        curr_lager = op_list.lager_nr
        dml_code = op_list.dml_code

        l_artikel = get_cache (L_artikel, {"artnr": [(eq, s_artnr)]})
        create_l_op()
        created = True

    if lief_nr != 0 and t_amount != 0:
        create_ap()

    l_art_obj_list = {}

    # Rd 25/7/2025
    # for l_art, sys_user in db_session.query(L_art, Sys_user).join(Sys_user,(Sys_user.nr == op_list.fuellflag)).filter(
    #         ((L_art.artnr.in_(list(set([op_list.artnr for op_list in op_list_data])))))).order_by(op_list.pos).all():

    artnr_set = {op.artnr for op in op_list_data if op.artnr is not None}

    # Rd 31/7/2025
    # Remark order by pos, cuman 1 pos saja.
    # err di order by (not sure, how to fix)
    for l_art, sys_user in (
                db_session.query(L_art, Sys_user)
                .join(Sys_user, Sys_user.nr == op_list.fuellflag)
                .filter(L_art.artnr.in_(artnr_set))
                # .order_by(op_list.pos)  # Only if pos is a column of L_art
                .all()
            ):

        if l_art_obj_list.get(l_art._recid):
            continue
        else:
            l_art_obj_list[l_art._recid] = True


        t_op_list = T_op_list()
        t_op_list_data.append(t_op_list)

        buffer_copy(op_list, t_op_list)
        t_op_list.bezeich = l_artikel.bezeich
        t_op_list.username = bediener.username


    op_list_data.clear()

    for t_op_list in query(t_op_list_data):
        op_list = Op_list()
        op_list_data.append(op_list)

        buffer_copy(t_op_list, op_list)

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 331) & ((Queasy.char2 == ("Inv-Cek Reciving").lower()) | (Queasy.char2 == ("Inv-Cek Reorg").lower()) | (Queasy.char2 == ("Inv-Cek Journal").lower()))).order_by(Queasy._recid).all():
        db_session.delete(queasy)

    return generate_output()