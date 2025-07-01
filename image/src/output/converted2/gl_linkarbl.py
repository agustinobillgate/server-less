#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Gl_acct, Gl_jouhdr, Artikel, Debitor, Guest

def gl_linkarbl(merge_flag:bool, from_date:date, to_date:date, user_init:string, refno:string, curr_anz:int):

    prepare_cache ([Gl_acct, Artikel, Debitor, Guest])

    acct_error = 0
    debits = None
    credits = None
    remains = to_decimal("0.0")
    buf_g_list_list = []
    s_list_list = []
    art_artnr = 0
    art_bezeich = ""
    add_info:string = ""
    fibukonto:string = ""
    credit_betrag:Decimal = to_decimal("0.0")
    debit_betrag:Decimal = to_decimal("0.0")
    gl_acct = gl_jouhdr = artikel = debitor = guest = None

    g_list = buf_g_list = s_list = pay_list = gl_acct1 = None

    g_list_list, G_list = create_model("G_list", {"rechnr":int, "dept":int, "jnr":int, "fibukonto":string, "debit":Decimal, "credit":Decimal, "bemerk":string, "userinit":string, "sysdate":date, "zeit":int, "chginit":string, "chgdate":date, "duplicate":bool, "add_info":string, "counter":int, "acct_fibukonto":string, "bezeich":string}, {"sysdate": get_current_date(), "chgdate": None, "duplicate": True})
    buf_g_list_list, Buf_g_list = create_model_like(G_list)
    s_list_list, S_list = create_model("S_list", {"fibukonto":string, "bezeich":string, "credit":Decimal, "debit":Decimal})
    pay_list_list, Pay_list = create_model("Pay_list", {"counter":int, "ar_recid":int, "name":string, "artnr":int, "zahlkonto":int, "amount":Decimal, "add_info":string})

    Gl_acct1 = create_buffer("Gl_acct1",Gl_acct)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal acct_error, debits, credits, remains, buf_g_list_list, s_list_list, art_artnr, art_bezeich, add_info, fibukonto, credit_betrag, debit_betrag, gl_acct, gl_jouhdr, artikel, debitor, guest
        nonlocal merge_flag, from_date, to_date, user_init, refno, curr_anz
        nonlocal gl_acct1


        nonlocal g_list, buf_g_list, s_list, pay_list, gl_acct1
        nonlocal g_list_list, buf_g_list_list, s_list_list, pay_list_list

        return {"curr_anz": curr_anz, "acct_error": acct_error, "debits": debits, "credits": credits, "remains": remains, "buf-g-list": buf_g_list_list, "s-list": s_list_list, "art_artnr": art_artnr, "art_bezeich": art_bezeich}

    def step_two():

        nonlocal acct_error, debits, credits, remains, buf_g_list_list, s_list_list, art_artnr, art_bezeich, add_info, fibukonto, credit_betrag, debit_betrag, gl_acct, gl_jouhdr, artikel, debitor, guest
        nonlocal merge_flag, from_date, to_date, user_init, refno, curr_anz
        nonlocal gl_acct1


        nonlocal g_list, buf_g_list, s_list, pay_list, gl_acct1
        nonlocal g_list_list, buf_g_list_list, s_list_list, pay_list_list

        art1 = None
        gl_acc1 = None
        Art1 =  create_buffer("Art1",Artikel)
        Gl_acc1 =  create_buffer("Gl_acc1",Gl_acct)

        for debitor in db_session.query(Debitor).filter(
                 (Debitor.rgdatum >= from_date) & (Debitor.rgdatum <= to_date) & (Debitor.opart > 0) & (Debitor.zahlkonto != 0)).order_by(Debitor._recid).all():
            add_info = ";&&1;" + to_string(debitor.artnr) + ";" + to_string(debitor.rechnr) + ";" + to_string(debitor.betriebsnr)

            art1 = get_cache (Artikel, {"artnr": [(eq, debitor.artnr)],"departement": [(eq, 0)]})

            gl_acc1 = get_cache (Gl_acct, {"fibukonto": [(eq, art1.fibukonto)]})

            if gl_acc1:
                fibukonto = gl_acc1.fibukonto

                if debitor.saldo < 0:
                    credit_betrag =  - to_decimal(debitor.saldo)
                    debit_betrag =  to_decimal("0")

                    g_list = query(g_list_list, filters=(lambda g_list: g_list.fibukonto == gl_acc1.fibukonto and g_list.rechnr == debitor.rechnr and g_list.dept == debitor.betriebsnr), first=True)

                    if not g_list:
                        add_list(True)
                    else:
                        add_list(False)

                elif debitor.saldo > 0:
                    debit_betrag =  to_decimal(debitor.saldo)
                    credit_betrag =  to_decimal("0")

                    g_list = query(g_list_list, filters=(lambda g_list: g_list.fibukonto == gl_acc1.fibukonto and g_list.rechnr == debitor.rechnr), first=True)

                    if not g_list:
                        add_list(True)
                    else:
                        add_list(False)
            else:
                art_artnr = art1.artnr
                art_bezeich = art1.bezeich
                acct_error = 2

                return
            add_info = ";&&2;" + to_string(debitor.artnr) + ";" + to_string(debitor.counter) + ";" + to_string(debitor.zahlkonto)

            artikel = get_cache (Artikel, {"artnr": [(eq, debitor.zahlkonto)],"departement": [(eq, 0)]})

            gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, artikel.fibukonto)]})

            if gl_acct:
                fibukonto = gl_acct.fibukonto

                if debitor.saldo <= 0:
                    debit_betrag =  - to_decimal(debitor.saldo)
                    credit_betrag =  to_decimal("0")
                    add_list(True)

                elif debitor.saldo > 0:
                    credit_betrag =  to_decimal(debitor.saldo)
                    debit_betrag =  to_decimal("0")
                    add_list(True)
            else:
                art_artnr = artikel.artnr
                art_bezeich = artikel.bezeich
                acct_error = 2

                return
        adjust_lists()

        for g_list in query(g_list_list, sort_by=[("sysdate",True),("zeit",True)]):

            gl_acct1 = get_cache (Gl_acct, {"fibukonto": [(eq, g_list.fibukonto)]})

            if gl_acct1:
                buf_g_list = Buf_g_list()
                buf_g_list_list.append(buf_g_list)

                buffer_copy(g_list, buf_g_list)
                buf_g_list.acct_fibukonto = gl_acct1.fibukonto
                buf_g_list.bezeich = gl_acct1.bezeich


    def adjust_lists():

        nonlocal acct_error, debits, credits, remains, buf_g_list_list, s_list_list, art_artnr, art_bezeich, add_info, fibukonto, credit_betrag, debit_betrag, gl_acct, gl_jouhdr, artikel, debitor, guest
        nonlocal merge_flag, from_date, to_date, user_init, refno, curr_anz
        nonlocal gl_acct1


        nonlocal g_list, buf_g_list, s_list, pay_list, gl_acct1
        nonlocal g_list_list, buf_g_list_list, s_list_list, pay_list_list

        for g_list in query(g_list_list):

            if g_list.credit == g_list.debit:
                g_list_list.remove(g_list)

            elif g_list.credit > g_list.debit:
                g_list.credit =  to_decimal(g_list.credit) - to_decimal(g_list.debit)
                g_list.debit =  to_decimal("0")


            else:
                g_list.debit =  to_decimal(g_list.debit) - to_decimal(g_list.credit)
                g_list.credit =  to_decimal("0")


        s_list_list.clear()

        for g_list in query(g_list_list):

            gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, g_list.fibukonto)]})

            s_list = query(s_list_list, filters=(lambda s_list: s_list.fibukonto == gl_acct.fibukonto), first=True)

            if not s_list:
                s_list = S_list()
                s_list_list.append(s_list)

                s_list.fibukonto = gl_acct.fibukonto
                s_list.bezeich = gl_acct.bezeich


            s_list.credit =  to_decimal(s_list.credit) + to_decimal(g_list.credit)
            s_list.debit =  to_decimal(s_list.debit) + to_decimal(g_list.debit)


    def step_twoa():

        nonlocal acct_error, debits, credits, remains, buf_g_list_list, s_list_list, art_artnr, art_bezeich, add_info, fibukonto, credit_betrag, debit_betrag, gl_acct, gl_jouhdr, artikel, debitor, guest
        nonlocal merge_flag, from_date, to_date, user_init, refno, curr_anz
        nonlocal gl_acct1


        nonlocal g_list, buf_g_list, s_list, pay_list, gl_acct1
        nonlocal g_list_list, buf_g_list_list, s_list_list, pay_list_list

        art1 = None
        gl_acc1 = None
        curr_art:int = 0
        curr_zahl:int = 0
        curr_count:int = 0
        curr_saldo:Decimal = to_decimal("0.0")
        curr_pay:Decimal = to_decimal("0.0")
        do_it:bool = False
        pay_it:bool = False
        Art1 =  create_buffer("Art1",Artikel)
        Gl_acc1 =  create_buffer("Gl_acc1",Gl_acct)
        pay_list_list.clear()
        g_list_list.clear()
        s_list_list.clear()

        for debitor in db_session.query(Debitor).filter(
                 (Debitor.rgdatum >= from_date) & (Debitor.rgdatum <= to_date) & (Debitor.opart > 0) & (Debitor.zahlkonto != 0)).order_by(Debitor.betriebsnr, Debitor.artnr, Debitor.zahlkonto, Debitor.rgdatum, Debitor.counter).all():

            if debitor.betriebsnr == 0:
                pay_list = Pay_list()
                pay_list_list.append(pay_list)

                pay_list.ar_recid = debitor._recid
            else:

                pay_list = query(pay_list_list, filters=(lambda pay_list: pay_list.counter == debitor.betriebsnr and pay_list.artnr == debitor.artnr), first=True)

                guest = get_cache (Guest, {"gastnr": [(eq, debitor.gastnr)]})

                if not pay_list:
                    add_info = ";&&3;" + to_string(debitor.artnr) + ";" + to_string(debitor.betriebsnr)
                    pay_list = Pay_list()
                    pay_list_list.append(pay_list)

                    pay_list.counter = debitor.betriebsnr
                    pay_list.name = guest.name
                    pay_list.artnr = debitor.artnr
                    pay_list.add_info = add_info

                    if debitor.vesrcod != "":
                        pay_list.name = debitor.vesrcod + ";" + pay_list.name
                pay_list.amount =  to_decimal(pay_list.amount) - to_decimal(debitor.saldo)

                pay_list = query(pay_list_list, filters=(lambda pay_list: pay_list.counter == debitor.betriebsnr and pay_list.zahlkonto == debitor.zahlkonto), first=True)

                if not pay_list:
                    add_info = ";&&4;" + to_string(debitor.artnr) + ";" + to_string(debitor.betriebsnr) + ";" + to_string(debitor.zahlkonto)
                    pay_list = Pay_list()
                    pay_list_list.append(pay_list)

                    pay_list.counter = debitor.betriebsnr
                    pay_list.name = guest.name
                    pay_list.zahlkonto = debitor.zahlkonto
                    pay_list.add_info = add_info

                    if debitor.vesrcod != "":
                        pay_list.name = debitor.vesrcod + ";" + pay_list.name
                pay_list.amount =  to_decimal(pay_list.amount) + to_decimal(debitor.saldo)

        for pay_list in query(pay_list_list):

            if pay_list.counter == 0:
                step_three1()

            elif pay_list.zahlkonto != 0:
                step_three2(pay_list.zahlkonto)

            elif pay_list.artnr != 0:
                step_three2(pay_list.artnr)
        adjust_lists()

        for g_list in query(g_list_list, sort_by=[("sysdate",True),("zeit",True)]):

            gl_acct1 = get_cache (Gl_acct, {"fibukonto": [(eq, g_list.fibukonto)]})

            if gl_acct1:
                buf_g_list = Buf_g_list()
                buf_g_list_list.append(buf_g_list)

                buffer_copy(g_list, buf_g_list)
                buf_g_list.acct_fibukonto = gl_acct1.fibukonto
                buf_g_list.bezeich = gl_acct1.bezeich


    def add_list(create_it:bool):

        nonlocal acct_error, debits, credits, remains, buf_g_list_list, s_list_list, art_artnr, art_bezeich, add_info, fibukonto, credit_betrag, debit_betrag, gl_acct, gl_jouhdr, artikel, debitor, guest
        nonlocal merge_flag, from_date, to_date, user_init, refno, curr_anz
        nonlocal gl_acct1


        nonlocal g_list, buf_g_list, s_list, pay_list, gl_acct1
        nonlocal g_list_list, buf_g_list_list, s_list_list, pay_list_list

        gl_acc1 = None
        Gl_acc1 =  create_buffer("Gl_acc1",Gl_acct)

        gl_acc1 = get_cache (Gl_acct, {"fibukonto": [(eq, fibukonto)]})
        curr_anz = curr_anz + 1

        if create_it:
            g_list = G_list()
            g_list_list.append(g_list)

            g_list.add_info = add_info
        g_list.fibukonto = fibukonto
        g_list.rechnr = debitor.rechnr
        g_list.dept = debitor.betriebsnr

        if debitor.vesrcod == "":
            g_list.bemerk = to_string(debitor.rechnr) + " - " + debitor.name
        else:
            g_list.bemerk = to_string(debitor.rechnr) + " - " + debit.vesrcod
        g_list.userinit = user_init
        g_list.zeit = get_current_time_in_seconds()
        g_list.duplicate = False
        g_list.debit =  to_decimal(g_list.debit) + to_decimal(debit_betrag)
        g_list.credit =  to_decimal(g_list.credit) + to_decimal(credit_betrag)

        s_list = query(s_list_list, filters=(lambda s_list: s_list.fibukonto == gl_acc1.fibukonto), first=True)

        if not s_list:
            s_list = S_list()
            s_list_list.append(s_list)

            s_list.fibukonto = gl_acc1.fibukonto
            s_list.bezeich = gl_acc1.bezeich
        s_list.credit =  to_decimal(s_list.credit) + to_decimal(credit_betrag)
        s_list.debit =  to_decimal(s_list.debit) + to_decimal(debit_betrag)
        credits = credits + credit_betrag
        debits = debits + debit_betrag
        remains =  to_decimal(debits) - to_decimal(credits)
        debit_betrag =  to_decimal("0")
        credit_betrag =  to_decimal("0")


    def step_three1():

        nonlocal acct_error, debits, credits, remains, buf_g_list_list, s_list_list, art_artnr, art_bezeich, add_info, fibukonto, credit_betrag, debit_betrag, gl_acct, gl_jouhdr, artikel, debitor, guest
        nonlocal merge_flag, from_date, to_date, user_init, refno, curr_anz
        nonlocal gl_acct1


        nonlocal g_list, buf_g_list, s_list, pay_list, gl_acct1
        nonlocal g_list_list, buf_g_list_list, s_list_list, pay_list_list

        art1 = None
        gl_acc1 = None
        Art1 =  create_buffer("Art1",Artikel)
        Gl_acc1 =  create_buffer("Gl_acc1",Gl_acct)

        debitor = get_cache (Debitor, {"_recid": [(eq, pay_list.ar_recid)]})
        add_info = ";&&1;" + to_string(debitor.artnr) + ";" + to_string(debitor.rechnr) + ";" + to_string(debitor.betriebsnr)

        art1 = get_cache (Artikel, {"artnr": [(eq, debitor.artnr)],"departement": [(eq, 0)]})

        gl_acc1 = get_cache (Gl_acct, {"fibukonto": [(eq, art1.fibukonto)]})

        if gl_acc1:
            fibukonto = gl_acc1.fibukonto

            if debitor.saldo < 0:
                credit_betrag =  - to_decimal(debitor.saldo)
                debit_betrag =  to_decimal("0")

                g_list = query(g_list_list, filters=(lambda g_list: g_list.fibukonto == gl_acc1.fibukonto and g_list.rechnr == debitor.rechnr and g_list.dept == debitor.betriebsnr), first=True)

                if not g_list:
                    add_list(True)
                else:
                    add_list(False)

            elif debitor.saldo > 0:
                debit_betrag =  to_decimal(debitor.saldo)
                credit_betrag =  to_decimal("0")

                g_list = query(g_list_list, filters=(lambda g_list: g_list.fibukonto == gl_acc1.fibukonto and g_list.rechnr == debitor.rechnr), first=True)

                if not g_list:
                    add_list(True)
                else:
                    add_list(False)
        else:
            art_artnr = art1.artnr
            art_bezeich = art1.bezeich
            acct_error = 2

            return
        add_info = ";&&2;" + to_string(debitor.artnr) + ";" + to_string(debitor.counter) + ";" + to_string(debitor.zahlkonto)

        artikel = get_cache (Artikel, {"artnr": [(eq, debitor.zahlkonto)],"departement": [(eq, 0)]})

        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, artikel.fibukonto)]})

        if gl_acct:
            fibukonto = gl_acct.fibukonto

            if debitor.saldo <= 0:
                debit_betrag =  - to_decimal(debitor.saldo)
                credit_betrag =  to_decimal("0")
                add_list(True)

            elif debitor.saldo > 0:
                credit_betrag =  to_decimal(debitor.saldo)
                debit_betrag =  to_decimal("0")
                add_list(True)
        else:
            art_artnr = artikel.artnr


            art_bezeich = artikel.bezeich
            acct_error = 2

            return


    def step_three2(artnr:int):

        nonlocal acct_error, debits, credits, remains, buf_g_list_list, s_list_list, art_artnr, art_bezeich, add_info, fibukonto, credit_betrag, debit_betrag, gl_acct, gl_jouhdr, artikel, debitor, guest
        nonlocal merge_flag, from_date, to_date, user_init, refno, curr_anz
        nonlocal gl_acct1


        nonlocal g_list, buf_g_list, s_list, pay_list, gl_acct1
        nonlocal g_list_list, buf_g_list_list, s_list_list, pay_list_list

        artikel = get_cache (Artikel, {"artnr": [(eq, artnr)],"departement": [(eq, 0)]})

        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, artikel.fibukonto)]})

        if gl_acct:
            fibukonto = gl_acct.fibukonto

            if pay_list.amount <= 0:
                debit_betrag =  - to_decimal(pay_list.amount)
                credit_betrag =  to_decimal("0")
                add_lista()

            elif pay_list.amount > 0:
                credit_betrag =  to_decimal(pay_list.amount)
                debit_betrag =  to_decimal("0")
                add_lista()
        else:
            art_artnr = artikel.artnr
            art_bezeich = artikel.bezeich
            acct_error = 2

            return


    def add_lista():

        nonlocal acct_error, debits, credits, remains, buf_g_list_list, s_list_list, art_artnr, art_bezeich, add_info, fibukonto, credit_betrag, debit_betrag, gl_acct, gl_jouhdr, artikel, debitor, guest
        nonlocal merge_flag, from_date, to_date, user_init, refno, curr_anz
        nonlocal gl_acct1


        nonlocal g_list, buf_g_list, s_list, pay_list, gl_acct1
        nonlocal g_list_list, buf_g_list_list, s_list_list, pay_list_list

        gl_acc1 = None
        Gl_acc1 =  create_buffer("Gl_acc1",Gl_acct)

        gl_acc1 = get_cache (Gl_acct, {"fibukonto": [(eq, fibukonto)]})
        curr_anz = curr_anz + 1

        g_list = query(g_list_list, filters=(lambda g_list: g_list.fibukonto.lower()  == (fibukonto).lower()  and g_list.counter == pay_list.counter), first=True)

        if not g_list:
            g_list = G_list()
            g_list_list.append(g_list)

            g_list.fibukonto = fibukonto
            g_list.counter = pay_list.counter
            g_list.bemerk = pay_list.name
            g_list.userinit = user_init
            g_list.zeit = get_current_time_in_seconds()
            g_list.duplicate = False
            g_list.add_info = pay_list.add_info

        if g_list.credit != 0 and debit_betrag != 0:

            if g_list.credit >= debit_betrag:
                g_list.credit =  to_decimal(g_list.credit) - to_decimal(debit_betrag)
            else:
                g_list.debit =  to_decimal(debit_betrag) - to_decimal(g_list.credit)
                g_list.credit =  to_decimal("0")

        elif g_list.debit != 0 and credit_betrag != 0:

            if g_list.debit >= credit_betrag:
                g_list.debit =  to_decimal(g_list.debit) - to_decimal(credit_betrag)
            else:
                g_list.credit =  to_decimal(credit_betrag) - to_decimal(g_list.debit)
                g_list.debit =  to_decimal("0")
        else:
            g_list.debit =  to_decimal(g_list.debit) + to_decimal(debit_betrag)
            g_list.credit =  to_decimal(g_list.credit) + to_decimal(credit_betrag)

        s_list = query(s_list_list, filters=(lambda s_list: s_list.fibukonto == gl_acc1.fibukonto), first=True)

        if not s_list:
            s_list = S_list()
            s_list_list.append(s_list)

            s_list.fibukonto = gl_acc1.fibukonto
            s_list.bezeich = gl_acc1.bezeich
        s_list.credit =  to_decimal(s_list.credit) + to_decimal(credit_betrag)
        s_list.debit =  to_decimal(s_list.debit) + to_decimal(debit_betrag)
        credits = credits + credit_betrag
        debits = debits + debit_betrag
        remains =  to_decimal(debits) - to_decimal(credits)
        debit_betrag =  to_decimal("0")
        credit_betrag =  to_decimal("0")

    gl_jouhdr = get_cache (Gl_jouhdr, {"refno": [(eq, refno)],"jtype": [(eq, 2)]})

    if gl_jouhdr:
        acct_error = 1

        return generate_output()

    if not merge_flag:
        step_two()
    else:
        step_twoa()

    return generate_output()