#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_op, Gl_acct, Bediener, L_ophdr, Dml_art, Dml_artdep, L_artikel, L_lieferant, L_liefumsatz, Htparam, L_kredit, Ap_journal, L_pprice, L_bestand

op_list_list, Op_list = create_model_like(L_op, {"bezeich":string, "username":string})

def dml_issue_btn_go_webbl(op_list_list:[Op_list], billdate:date, closedate:date, curr_lager:int, curr_dept:int, cost_acct:string, lief_nr:int, lscheinnr:string, user_init:string, t_amount:Decimal):

    prepare_cache ([L_op, Bediener, L_ophdr, L_artikel, L_liefumsatz, Htparam, L_kredit, Ap_journal, L_pprice, L_bestand])

    curr_pos = 0
    s_artnr = 0
    qty = to_decimal("0.0")
    price = to_decimal("0.0")
    created = False
    err_code = 0
    gl_notfound:bool = False
    l_op = gl_acct = bediener = l_ophdr = dml_art = dml_artdep = l_artikel = l_lieferant = l_liefumsatz = htparam = l_kredit = ap_journal = l_pprice = l_bestand = None

    op_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal curr_pos, s_artnr, qty, price, created, err_code, gl_notfound, l_op, gl_acct, bediener, l_ophdr, dml_art, dml_artdep, l_artikel, l_lieferant, l_liefumsatz, htparam, l_kredit, ap_journal, l_pprice, l_bestand
        nonlocal billdate, closedate, curr_lager, curr_dept, cost_acct, lief_nr, lscheinnr, user_init, t_amount


        nonlocal op_list

        return {"op-list": op_list_list, "curr_pos": curr_pos, "s_artnr": s_artnr, "qty": qty, "price": price, "created": created, "err_code": err_code}

    def l_op_pos():

        nonlocal curr_pos, s_artnr, qty, price, created, err_code, gl_notfound, l_op, gl_acct, bediener, l_ophdr, dml_art, dml_artdep, l_artikel, l_lieferant, l_liefumsatz, htparam, l_kredit, ap_journal, l_pprice, l_bestand
        nonlocal billdate, closedate, curr_lager, curr_dept, cost_acct, lief_nr, lscheinnr, user_init, t_amount


        nonlocal op_list

        pos = 0
        l_op1 = None

        def generate_inner_output():
            return (pos)

        L_op1 =  create_buffer("L_op1",L_op)
        pos = 1

        return generate_inner_output()


    def create_l_op():

        nonlocal curr_pos, s_artnr, qty, price, created, err_code, gl_notfound, l_op, gl_acct, bediener, l_ophdr, dml_art, dml_artdep, l_artikel, l_lieferant, l_liefumsatz, htparam, l_kredit, ap_journal, l_pprice, l_bestand
        nonlocal billdate, closedate, curr_lager, curr_dept, cost_acct, lief_nr, lscheinnr, user_init, t_amount


        nonlocal op_list

        anzahl:Decimal = to_decimal("0.0")
        wert:Decimal = to_decimal("0.0")
        tot_anz:Decimal = to_decimal("0.0")
        tot_wert:Decimal = to_decimal("0.0")
        avrg_price:Decimal = to_decimal("0.0")
        d_art = None
        d_art1 = None
        D_art =  create_buffer("D_art",Dml_art)
        D_art1 =  create_buffer("D_art1",Dml_artdep)
        anzahl =  to_decimal(qty)
        wert =  to_decimal(qty) * to_decimal(price)
        wert = to_decimal(round(wert , 2))

        l_artikel = get_cache (L_artikel, {"artnr": [(eq, s_artnr)]})

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
        l_op.herkunftflag = 2
        l_op.docu_nr = lscheinnr
        l_op.lscheinnr = lscheinnr
        l_op.pos = curr_pos
        l_op.fuellflag = bediener.nr


        pass

        if curr_dept == 0:

            d_art = db_session.query(D_art).filter(
                     (D_art.artnr == s_artnr) & (D_art.datum == billdate)).first()
            d_art.geliefert =  to_decimal(d_art.geliefert) + to_decimal(anzahl)
            pass

        elif curr_dept > 0:

            d_art1 = db_session.query(D_art1).filter(
                     (D_art1.artnr == s_artnr) & (D_art1.datum == billdate) & (D_art1.departement == curr_dept)).first()
            d_art1.geliefert =  to_decimal(d_art1.geliefert) + to_decimal(anzahl)
            pass
        create_purchase_book(s_artnr, price, anzahl, billdate, lief_nr)

        if (l_artikel.ek_aktuell != price) and price != 0:
            pass
            l_artikel.ek_letzter =  to_decimal(l_artikel.ek_aktuell)
            l_artikel.ek_aktuell =  to_decimal(price)
            pass


    def create_ap():

        nonlocal curr_pos, s_artnr, qty, price, created, err_code, gl_notfound, l_op, gl_acct, bediener, l_ophdr, dml_art, dml_artdep, l_artikel, l_lieferant, l_liefumsatz, htparam, l_kredit, ap_journal, l_pprice, l_bestand
        nonlocal billdate, closedate, curr_lager, curr_dept, cost_acct, lief_nr, lscheinnr, user_init, t_amount


        nonlocal op_list

        ap_license:bool = False
        ap_acct:string = ""
        do_it:bool = True

        htparam = get_cache (Htparam, {"paramnr": [(eq, 1016)]})
        ap_license = htparam.flogical

        if not ap_license:

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

        nonlocal curr_pos, err_code, gl_notfound, l_op, gl_acct, bediener, l_ophdr, dml_art, dml_artdep, l_artikel, l_lieferant, l_liefumsatz, htparam, l_kredit, ap_journal, l_pprice, l_bestand
        nonlocal billdate, closedate, curr_lager, curr_dept, cost_acct, lscheinnr, user_init, t_amount


        nonlocal op_list

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


    def create_l_op1():

        nonlocal curr_pos, s_artnr, qty, price, created, err_code, gl_notfound, l_op, gl_acct, bediener, l_ophdr, dml_art, dml_artdep, l_artikel, l_lieferant, l_liefumsatz, htparam, l_kredit, ap_journal, l_pprice, l_bestand
        nonlocal billdate, closedate, curr_lager, curr_dept, cost_acct, lief_nr, lscheinnr, user_init, t_amount


        nonlocal op_list

        anzahl:Decimal = to_decimal("0.0")
        wert:Decimal = to_decimal("0.0")
        tot_anz:Decimal = to_decimal("0.0")
        tot_wert:Decimal = to_decimal("0.0")
        avrg_price:Decimal = to_decimal("0.0")
        anzahl =  to_decimal(qty)
        wert =  to_decimal(qty) * to_decimal(price)
        wert = to_decimal(round(wert , 2))


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
        l_op.op_art = 3
        l_op.herkunftflag = 2
        l_op.docu_nr = lscheinnr
        l_op.lscheinnr = lscheinnr
        l_op.pos = curr_pos
        l_op.fuellflag = bediener.nr
        l_op.flag = True
        l_op.stornogrund = cost_acct


        pass

        if billdate <= closedate:

            l_bestand = get_cache (L_bestand, {"lager_nr": [(eq, curr_lager)],"artnr": [(eq, s_artnr)]})

            if not l_bestand:
                l_bestand = L_bestand()
                db_session.add(l_bestand)

                l_bestand.artnr = s_artnr
                l_bestand.lager_nr = curr_lager
                l_bestand.anf_best_dat = billdate


            l_bestand.anz_eingang =  to_decimal(l_bestand.anz_eingang) + to_decimal(anzahl)
            l_bestand.wert_eingang =  to_decimal(l_bestand.wert_eingang) + to_decimal(wert)
            l_bestand.anz_ausgang =  to_decimal(l_bestand.anz_ausgang) + to_decimal(anzahl)
            l_bestand.wert_ausgang =  to_decimal(l_bestand.wert_ausgang) + to_decimal(wert)


            pass

            l_bestand = get_cache (L_bestand, {"lager_nr": [(eq, 0)],"artnr": [(eq, s_artnr)]})

            if not l_bestand:
                l_bestand = L_bestand()
                db_session.add(l_bestand)

                l_bestand.artnr = s_artnr
                l_bestand.anf_best_dat = billdate


            l_bestand.anz_eingang =  to_decimal(l_bestand.anz_eingang) + to_decimal(anzahl)
            l_bestand.wert_eingang =  to_decimal(l_bestand.wert_eingang) + to_decimal(wert)
            l_bestand.anz_ausgang =  to_decimal(l_bestand.anz_ausgang) + to_decimal(anzahl)
            l_bestand.wert_ausgang =  to_decimal(l_bestand.wert_ausgang) + to_decimal(wert)


            pass


    if cost_acct.lower()  != "" and cost_acct.lower()  != ("00000000").lower()  and cost_acct.lower()  != None:

        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, cost_acct)]})

        if not gl_acct:
            err_code = 1

            return generate_output()

    for op_list in query(op_list_list, filters=(lambda op_list: op_list.stornogrund.lower()  != "" and op_list.stornogrund.lower()  != ("00000000").lower()  and op_list.stornogrund.lower()  != None)):

        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, op_list.stornogrund)]})

        if not gl_acct:
            gl_notfound = True
            break

    if gl_notfound:
        err_code = 1

        return generate_output()

    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

    l_ophdr = get_cache (L_ophdr, {"lscheinnr": [(eq, lscheinnr)],"op_typ": [(eq, "sti")]})

    if not l_ophdr:
        l_ophdr = L_ophdr()
        db_session.add(l_ophdr)

        l_ophdr.datum = billdate
        l_ophdr.lager_nr = curr_lager
        l_ophdr.lscheinnr = lscheinnr
        l_ophdr.fibukonto = cost_acct
        l_ophdr.op_typ = "STI"
        pass
    curr_pos = l_op_pos()
    curr_pos = curr_pos - 1

    for op_list in query(op_list_list):
        created = True
        curr_pos = curr_pos + 1
        s_artnr = op_list.artnr
        qty =  to_decimal(op_list.anzahl)
        price =  to_decimal(op_list.warenwert) / to_decimal(qty)
        create_l_op()

    if lief_nr != 0 and t_amount != 0:
        create_ap()

    l_ophdr = get_cache (L_ophdr, {"lscheinnr": [(eq, lscheinnr)],"op_typ": [(eq, "stt")]})

    if not l_ophdr:
        l_ophdr = L_ophdr()
        db_session.add(l_ophdr)

        l_ophdr.datum = billdate
        l_ophdr.lager_nr = curr_lager
        l_ophdr.lscheinnr = lscheinnr
        l_ophdr.op_typ = "STT"
        l_ophdr.fibukonto = cost_acct
        pass
    curr_pos = l_op_pos()
    curr_pos = curr_pos - 1

    for op_list in query(op_list_list):
        curr_pos = curr_pos + 1
        s_artnr = op_list.artnr
        qty =  to_decimal(op_list.anzahl)
        price =  to_decimal(op_list.warenwert) / to_decimal(qty)
        create_l_op1()

    return generate_output()