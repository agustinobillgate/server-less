#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import H_artikel, Gl_acct, Htparam, Hoteldpt, H_compli, Exrate, Artikel, H_cost, H_bill_line

def gl_linkcompli1bl(pvilanguage:int, from_date:date, to_date:date, double_currency:bool, foreign_nr:int, exchg_rate:Decimal, user_init:string):

    prepare_cache ([H_artikel, Gl_acct, Htparam, Hoteldpt, H_compli, Exrate, Artikel, H_cost, H_bill_line])

    curr_anz = 0
    debits = to_decimal("0.0")
    credits = to_decimal("0.0")
    remains = to_decimal("0.0")
    msg_str = ""
    t_g_list_list = []
    s_list_list = []
    curr_i:int = 0
    lvcarea:string = "gl-linkcompli"
    h_artikel = gl_acct = htparam = hoteldpt = h_compli = exrate = artikel = h_cost = h_bill_line = None

    c_list = s_list = g_list = t_g_list = None

    c_list_list, C_list = create_model("C_list", {"datum":date, "dept":int, "bemerk":string, "add_note":string, "fibukonto":string, "f_acct":string, "b_acct":string, "o_acct":string, "rechnr":int, "p_artnr":int, "f_cost":Decimal, "b_cost":Decimal, "o_cost":Decimal, "t_cost":Decimal})
    s_list_list, S_list = create_model("S_list", {"fibukonto":string, "bezeich":string, "credit":Decimal, "debit":Decimal})
    g_list_list, G_list = create_model("G_list", {"docu_nr":string, "lscheinnr":string, "jnr":int, "fibukonto":string, "debit":Decimal, "credit":Decimal, "bemerk":string, "userinit":string, "sysdate":date, "zeit":int, "chginit":string, "chgdate":date, "add_note":string, "duplicate":bool, "acct_fibukonto":string, "bezeich":string}, {"sysdate": get_current_date(), "chgdate": None, "duplicate": True})
    t_g_list_list, T_g_list = create_model_like(G_list)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal curr_anz, debits, credits, remains, msg_str, t_g_list_list, s_list_list, curr_i, lvcarea, h_artikel, gl_acct, htparam, hoteldpt, h_compli, exrate, artikel, h_cost, h_bill_line
        nonlocal pvilanguage, from_date, to_date, double_currency, foreign_nr, exchg_rate, user_init


        nonlocal c_list, s_list, g_list, t_g_list
        nonlocal c_list_list, s_list_list, g_list_list, t_g_list_list

        return {"curr_anz": curr_anz, "debits": debits, "credits": credits, "remains": remains, "msg_str": msg_str, "t-g-list": t_g_list_list, "s-list": s_list_list}

    def step_two():

        nonlocal curr_anz, debits, credits, remains, msg_str, t_g_list_list, s_list_list, curr_i, lvcarea, h_artikel, gl_acct, htparam, hoteldpt, h_compli, exrate, artikel, h_cost, h_bill_line
        nonlocal pvilanguage, from_date, to_date, double_currency, foreign_nr, exchg_rate, user_init


        nonlocal c_list, s_list, g_list, t_g_list
        nonlocal c_list_list, s_list_list, g_list_list, t_g_list_list

        h_art = None
        gl_acc1 = None
        cost_account:string = ""
        cost_value:Decimal = to_decimal("0.0")
        cost:Decimal = to_decimal("0.0")
        rate:Decimal = 1
        curr_datum:date = None
        f_endkum:int = 0
        b_endkum:int = 0
        ldry:int = 0
        dstore:int = 0
        transfer_ldry:bool = False
        H_art =  create_buffer("H_art",H_artikel)
        Gl_acc1 =  create_buffer("Gl_acc1",Gl_acct)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 1081)]})
        ldry = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 1082)]})
        dstore = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 1106)]})
        transfer_ldry = htparam.flogical

        htparam = get_cache (Htparam, {"paramnr": [(eq, 862)]})
        f_endkum = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 892)]})
        b_endkum = htparam.finteger
        s_list_list.clear()

        for hoteldpt in db_session.query(Hoteldpt).filter(
                 (Hoteldpt.num != dstore)).order_by(Hoteldpt.num).all():

            if transfer_ldry or (not transfer_ldry and hoteldpt.num != ldry):

                h_compli_obj_list = {}
                h_compli = H_compli()
                h_art = H_artikel()
                for h_compli.datum, h_compli.departement, h_compli.rechnr, h_compli.p_artnr, h_compli.artnr, h_compli.anzahl, h_compli.epreis, h_compli._recid, h_art.artnrfront, h_art.departement, h_art.artnr, h_art.bezeich, h_art.prozent, h_art.epreis1, h_art.artart, h_art._recid in db_session.query(H_compli.datum, H_compli.departement, H_compli.rechnr, H_compli.p_artnr, H_compli.artnr, H_compli.anzahl, H_compli.epreis, H_compli._recid, H_art.artnrfront, H_art.departement, H_art.artnr, H_art.bezeich, H_art.prozent, H_art.epreis1, H_art.artart, H_art._recid).join(H_art,(H_art.departement == H_compli.departement) & (H_art.artnr == H_compli.p_artnr) & (H_art.artart == 11)).filter(
                         (H_compli.datum >= from_date) & (H_compli.datum <= to_date) & (H_compli.departement == hoteldpt.num) & (H_compli.betriebsnr == 0)).order_by(H_compli.rechnr).all():
                    if h_compli_obj_list.get(h_compli._recid):
                        continue
                    else:
                        h_compli_obj_list[h_compli._recid] = True

                    if double_currency and curr_datum != h_compli.datum:
                        curr_datum = h_compli.datum

                        if foreign_nr != 0:

                            exrate = get_cache (Exrate, {"artnr": [(eq, foreign_nr)],"datum": [(eq, curr_datum)]})
                        else:

                            exrate = get_cache (Exrate, {"datum": [(eq, curr_datum)]})

                        if exrate:
                            rate =  to_decimal(exrate.betrag)
                        else:
                            rate =  to_decimal(exchg_rate)

                    c_list = query(c_list_list, filters=(lambda c_list: c_list.datum == h_compli.datum and c_list.dept == h_compli.departement and c_list.rechnr == h_compli.rechnr and c_list.p_artnr == h_compli.p_artnr), first=True)

                    if not c_list:

                        h_artikel = get_cache (H_artikel, {"artnr": [(eq, h_compli.p_artnr)],"departement": [(eq, h_compli.departement)]})

                        artikel = get_cache (Artikel, {"artnr": [(eq, h_artikel.artnrfront)],"departement": [(eq, 0)]})

                        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, artikel.fibukonto)]})

                        if not gl_acct:
                            msg_str = msg_str + chr_unicode(2) + translateExtended ("G/L Account not found :", lvcarea, "") + " " + artikel.fibukonto + chr_unicode(10) + translateExtended ("Dept", lvcarea, "") + " " + to_string(h_artikel.departement, "99") + " - " + to_string(h_artikel.artnr) + " " + h_artikel.bezeich + chr_unicode(10) + translateExtended ("Check F/O Article :", lvcarea, "") + " " + to_string(artikel.artnr) + " " + artikel.bezeich
                        c_list = C_list()
                        c_list_list.append(c_list)

                        c_list.datum = h_compli.datum
                        c_list.dept = h_compli.departement
                        c_list.rechnr = h_compli.rechnr
                        c_list.p_artnr = h_compli.p_artnr
                        c_list.fibukonto = artikel.fibukonto
                        c_list.bemerk = "*" + to_string(h_compli.rechnr) + " - " + hoteldpt.depart
                        c_list.add_note = ";&&4;" + to_string(h_compli.departement, "99") + ";" + to_string(h_compli.rechnr) + ";"

                        h_artikel = get_cache (H_artikel, {"artnr": [(eq, h_compli.artnr)],"departement": [(eq, h_compli.departement)]})

                        artikel = get_cache (Artikel, {"artnr": [(eq, h_artikel.artnrfront)],"departement": [(eq, h_artikel.departement)]})
                    cost =  to_decimal("0")

                    h_cost = get_cache (H_cost, {"artnr": [(eq, h_compli.artnr)],"departement": [(eq, h_compli.departement)],"datum": [(eq, h_compli.datum)],"flag": [(eq, 1)]})

                    if h_cost and h_cost.betrag != 0:
                        cost =  to_decimal(h_compli.anzahl) * to_decimal(h_cost.betrag)
                        cost = cost_correction(cost)
                        cost = to_decimal(round(cost , 2))
                        c_list.t_cost =  to_decimal(c_list.t_cost) + to_decimal(cost)

                        h_artikel = get_cache (H_artikel, {"artnr": [(eq, h_cost.artnr)],"departement": [(eq, h_cost.departement)]})

                        artikel = get_cache (Artikel, {"artnr": [(eq, h_artikel.artnrfront)],"departement": [(eq, h_artikel.departement)]})

                        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, artikel.bezeich1)]})

                        if not gl_acct:
                            msg_str = msg_str + chr_unicode(2) + translateExtended ("cost Account not found :", lvcarea, "") + " " + artikel.bezeich1 + chr_unicode(10) + translateExtended ("Dept", lvcarea, "") + " " + to_string(h_artikel.departement, "99") + " - " + to_string(h_artikel.artnr) + " " + h_artikel.bezeich + chr_unicode(10) + translateExtended ("Check F/O Article :", lvcarea, "") + " " + to_string(artikel.artnr) + " " + artikel.bezeich

                        if artikel.umsatzart == 6:
                            c_list.b_cost =  to_decimal(c_list.b_cost) + to_decimal(cost)
                            c_list.b_acct = artikel.bezeich1

                        elif artikel.umsatzart == 3 or artikel.umsatzart == 5:
                            c_list.f_cost =  to_decimal(c_list.f_cost) + to_decimal(cost)
                            c_list.f_acct = artikel.bezeich1
                        else:
                            c_list.o_cost =  to_decimal(c_list.o_cost) + to_decimal(cost)
                            c_list.o_acct = artikel.bezeich1

                    if not h_cost or (h_cost and h_cost.betrag == 0):

                        h_artikel = get_cache (H_artikel, {"artnr": [(eq, h_compli.artnr)],"departement": [(eq, h_compli.departement)]})
                        cost =  to_decimal(h_compli.anzahl) * to_decimal(h_compli.epreis) * to_decimal(h_artikel.prozent) / to_decimal("100") * to_decimal(rate)
                        cost = cost_correction(cost)
                        cost = to_decimal(round(cost , 2))
                        c_list.t_cost =  to_decimal(c_list.t_cost) + to_decimal(cost)

                        artikel = get_cache (Artikel, {"artnr": [(eq, h_artikel.artnrfront)],"departement": [(eq, h_artikel.departement)]})

                        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, artikel.bezeich1)]})

                        if not gl_acct:
                            msg_str = msg_str + chr_unicode(2) + translateExtended ("cost Account not found :", lvcarea, "") + " " + artikel.bezeich1 + chr_unicode(10) + translateExtended ("Dept", lvcarea, "") + " " + to_string(h_artikel.departement, "99") + " - " + to_string(h_artikel.artnr) + " " + h_artikel.bezeich + chr_unicode(10) + translateExtended ("Check F/O Article :", lvcarea, "") + " " + to_string(artikel.artnr) + " " + artikel.bezeich

                        if artikel.umsatzart == 6:
                            c_list.b_cost =  to_decimal(c_list.b_cost) + to_decimal(cost)
                            c_list.b_acct = artikel.bezeich1

                        elif artikel.umsatzart == 3 or artikel.umsatzart == 5:
                            c_list.f_cost =  to_decimal(c_list.f_cost) + to_decimal(cost)
                            c_list.f_acct = artikel.bezeich1
                        else:
                            c_list.o_cost =  to_decimal(c_list.o_cost) + to_decimal(cost)
                            c_list.o_acct = artikel.bezeich1


        for c_list in query(c_list_list, filters=(lambda c_list: c_list.t_cost != 0), sort_by=[("dept",False),("rechnr",False)]):
            add_list()


    def disp_it():

        nonlocal curr_anz, debits, credits, remains, msg_str, t_g_list_list, s_list_list, curr_i, lvcarea, h_artikel, gl_acct, htparam, hoteldpt, h_compli, exrate, artikel, h_cost, h_bill_line
        nonlocal pvilanguage, from_date, to_date, double_currency, foreign_nr, exchg_rate, user_init


        nonlocal c_list, s_list, g_list, t_g_list
        nonlocal c_list_list, s_list_list, g_list_list, t_g_list_list

        gl_acct_obj_list = {}
        for gl_acct in db_session.query(Gl_acct).filter(
                 ((Gl_acct.fibukonto.in_(list(set([g_list.fibukonto for g_list in g_list_list])))))).order_by(g_list.zeit).all():
            if gl_acct_obj_list.get(gl_acct._recid):
                continue
            else:
                gl_acct_obj_list[gl_acct._recid] = True


            t_g_list = T_g_list()
            t_g_list_list.append(t_g_list)

            buffer_copy(g_list, t_g_list)
            t_g_list.acct_fibukonto = gl_acct.fibukonto
            t_g_list.bezeich = gl_acct.bezeich


    def add_list():

        nonlocal curr_anz, debits, credits, remains, msg_str, t_g_list_list, s_list_list, curr_i, lvcarea, h_artikel, gl_acct, htparam, hoteldpt, h_compli, exrate, artikel, h_cost, h_bill_line
        nonlocal pvilanguage, from_date, to_date, double_currency, foreign_nr, exchg_rate, user_init


        nonlocal c_list, s_list, g_list, t_g_list
        nonlocal c_list_list, s_list_list, g_list_list, t_g_list_list

        i:int = 0
        gl_acct1 = None
        Gl_acct1 =  create_buffer("Gl_acct1",Gl_acct)

        s_list = query(s_list_list, filters=(lambda s_list: s_list.fibukonto == c_list.fibukonto), first=True)

        if not s_list:

            gl_acct1 = get_cache (Gl_acct, {"fibukonto": [(eq, c_list.fibukonto)]})
            s_list = S_list()
            s_list_list.append(s_list)

            s_list.fibukonto = gl_acct1.fibukonto
            s_list.bezeich = gl_acct1.bezeich
        curr_anz = curr_anz + 1
        g_list = G_list()
        g_list_list.append(g_list)

        g_list.fibukonto = c_list.fibukonto
        g_list.bemerk = c_list.bemerk
        g_list.add_note = c_list.add_note

        if c_list.t_cost > 0:
            g_list.debit =  to_decimal(g_list.debit) + to_decimal(c_list.t_cost)
            debits =  to_decimal(debits) + to_decimal(c_list.t_cost)
            s_list.debit =  to_decimal(s_list.debit) + to_decimal(c_list.t_cost)
        else:
            g_list.credit =  to_decimal(g_list.credit) - to_decimal(c_list.t_cost)
            credits =  to_decimal(credits) - to_decimal(c_list.t_cost)
            s_list.credit =  to_decimal(s_list.credit) - to_decimal(c_list.t_cost)
        g_list.userinit = user_init
        g_list.zeit = get_current_time_in_seconds() + curr_i
        g_list.duplicate = False

        if c_list.f_acct != "":

            s_list = query(s_list_list, filters=(lambda s_list: s_list.fibukonto == c_list.f_acct), first=True)

            if not s_list:

                gl_acct1 = get_cache (Gl_acct, {"fibukonto": [(eq, c_list.f_acct)]})
                s_list = S_list()
                s_list_list.append(s_list)

                s_list.fibukonto = gl_acct1.fibukonto
                s_list.bezeich = gl_acct1.bezeich
            g_list = G_list()
            g_list_list.append(g_list)

            g_list.fibukonto = c_list.f_acct
            g_list.bemerk = c_list.bemerk
            g_list.add_note = c_list.add_note

            if c_list.f_cost < 0:
                g_list.debit =  to_decimal(g_list.debit) - to_decimal(c_list.f_cost)
                debits =  to_decimal(debits) - to_decimal(c_list.f_cost)
                s_list.debit =  to_decimal(s_list.debit) - to_decimal(c_list.f_cost)
            else:
                g_list.credit =  to_decimal(g_list.credit) + to_decimal(c_list.f_cost)
                credits =  to_decimal(credits) + to_decimal(c_list.f_cost)
                s_list.credit =  to_decimal(s_list.credit) + to_decimal(c_list.f_cost)
            curr_i = curr_i + 1
            g_list.userinit = user_init
            g_list.zeit = get_current_time_in_seconds() + curr_i
            g_list.duplicate = False

        if c_list.b_acct != "":

            s_list = query(s_list_list, filters=(lambda s_list: s_list.fibukonto == c_list.b_acct), first=True)

            if not s_list:

                gl_acct1 = get_cache (Gl_acct, {"fibukonto": [(eq, c_list.b_acct)]})
                s_list = S_list()
                s_list_list.append(s_list)

                s_list.fibukonto = gl_acct1.fibukonto
                s_list.bezeich = gl_acct1.bezeich
            g_list = G_list()
            g_list_list.append(g_list)

            g_list.fibukonto = c_list.b_acct
            g_list.bemerk = c_list.bemerk
            g_list.add_note = c_list.add_note

            if c_list.b_cost < 0:
                g_list.debit =  to_decimal(g_list.debit) - to_decimal(c_list.b_cost)
                debits =  to_decimal(debits) - to_decimal(c_list.b_cost)
                s_list.debit =  to_decimal(s_list.debit) - to_decimal(c_list.b_cost)
            else:
                g_list.credit =  to_decimal(g_list.credit) + to_decimal(c_list.b_cost)
                credits =  to_decimal(credits) + to_decimal(c_list.b_cost)
                s_list.credit =  to_decimal(s_list.credit) + to_decimal(c_list.b_cost)
            curr_i = curr_i + 1
            g_list.userinit = user_init
            g_list.zeit = get_current_time_in_seconds() + curr_i
            g_list.duplicate = False

        if c_list.o_acct != "":

            s_list = query(s_list_list, filters=(lambda s_list: s_list.fibukonto == c_list.o_acct), first=True)

            if not s_list:

                gl_acct1 = get_cache (Gl_acct, {"fibukonto": [(eq, c_list.o_acct)]})
                s_list = S_list()
                s_list_list.append(s_list)

                s_list.fibukonto = gl_acct1.fibukonto
                s_list.bezeich = gl_acct1.bezeich
            g_list = G_list()
            g_list_list.append(g_list)

            g_list.fibukonto = c_list.o_acct
            g_list.bemerk = c_list.bemerk
            g_list.add_note = c_list.add_note

            if c_list.o_cost < 0:
                g_list.debit =  to_decimal(g_list.debit) - to_decimal(c_list.o_cost)
                debits =  to_decimal(debits) - to_decimal(c_list.o_cost)
                s_list.debit =  to_decimal(s_list.debit) - to_decimal(c_list.o_cost)
            else:
                g_list.credit =  to_decimal(g_list.credit) + to_decimal(c_list.o_cost)
                credits =  to_decimal(credits) + to_decimal(c_list.o_cost)
                s_list.credit =  to_decimal(s_list.credit) + to_decimal(c_list.o_cost)
            curr_i = curr_i + 1
            g_list.userinit = user_init
            g_list.zeit = get_current_time_in_seconds() + curr_i
            g_list.duplicate = False
        remains =  to_decimal(debits) - to_decimal(credits)


    def cost_correction(cost:Decimal):

        nonlocal curr_anz, debits, credits, remains, msg_str, t_g_list_list, s_list_list, curr_i, lvcarea, h_artikel, gl_acct, htparam, hoteldpt, h_compli, exrate, artikel, h_cost, h_bill_line
        nonlocal pvilanguage, from_date, to_date, double_currency, foreign_nr, exchg_rate, user_init


        nonlocal c_list, s_list, g_list, t_g_list
        nonlocal c_list_list, s_list_list, g_list_list, t_g_list_list

        def generate_inner_output():
            return (cost)


        h_bill_line = get_cache (H_bill_line, {"rechnr": [(eq, h_compli.rechnr)],"bill_datum": [(eq, h_compli.datum)],"departement": [(eq, h_compli.departement)],"artnr": [(eq, h_compli.artnr)],"epreis": [(eq, h_compli.epreis)]})

        if h_bill_line and substring(h_bill_line.bezeich, length(h_bill_line.bezeich) - 1, 1) == ("*").lower()  and h_bill_line.epreis != 0:

            h_artikel = get_cache (H_artikel, {"artnr": [(eq, h_bill_line.artnr)],"departement": [(eq, h_bill_line.departement)]})

            if h_artikel and h_artikel.artart == 0 and h_artikel.epreis1 > h_bill_line.epreis:
                cost =  to_decimal(cost) * to_decimal(h_bill_line.epreis) / to_decimal(h_artikel.epreis1)

        return generate_inner_output()


    step_two()
    disp_it()

    return generate_output()