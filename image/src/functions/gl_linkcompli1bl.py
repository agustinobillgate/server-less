from functions.additional_functions import *
import decimal
from datetime import date
from models import H_artikel, Gl_acct, Htparam, Hoteldpt, H_compli, Exrate, Artikel, H_cost, H_bill_line

def gl_linkcompli1bl(pvilanguage:int, from_date:date, to_date:date, double_currency:bool, foreign_nr:int, exchg_rate:decimal, user_init:str):
    curr_anz = 0
    debits = 0
    credits = 0
    remains = 0
    msg_str = ""
    t_g_list_list = []
    s_list_list = []
    curr_i:int = 0
    lvcarea:str = "gl_linkcompli"
    h_artikel = gl_acct = htparam = hoteldpt = h_compli = exrate = artikel = h_cost = h_bill_line = None

    c_list = s_list = g_list = t_g_list = h_art = gl_acc1 = gl_acct1 = None

    c_list_list, C_list = create_model("C_list", {"datum":date, "dept":int, "bemerk":str, "add_note":str, "fibukonto":str, "f_acct":str, "b_acct":str, "o_acct":str, "rechnr":int, "p_artnr":int, "f_cost":decimal, "b_cost":decimal, "o_cost":decimal, "t_cost":decimal})
    s_list_list, S_list = create_model("S_list", {"fibukonto":str, "bezeich":str, "credit":decimal, "debit":decimal})
    g_list_list, G_list = create_model("G_list", {"docu_nr":str, "lscheinnr":str, "jnr":int, "fibukonto":str, "debit":decimal, "credit":decimal, "bemerk":str, "userinit":str, "sysdate":date, "zeit":int, "chginit":str, "chgdate":date, "add_note":str, "duplicate":bool, "acct_fibukonto":str, "bezeich":str}, {"sysdate": get_current_date(), "chgdate": None, "duplicate": True})
    t_g_list_list, T_g_list = create_model_like(G_list)

    H_art = H_artikel
    Gl_acc1 = Gl_acct
    Gl_acct1 = Gl_acct

    db_session = local_storage.db_session

    def generate_output():
        nonlocal curr_anz, debits, credits, remains, msg_str, t_g_list_list, s_list_list, curr_i, lvcarea, h_artikel, gl_acct, htparam, hoteldpt, h_compli, exrate, artikel, h_cost, h_bill_line
        nonlocal h_art, gl_acc1, gl_acct1


        nonlocal c_list, s_list, g_list, t_g_list, h_art, gl_acc1, gl_acct1
        nonlocal c_list_list, s_list_list, g_list_list, t_g_list_list
        return {"curr_anz": curr_anz, "debits": debits, "credits": credits, "remains": remains, "msg_str": msg_str, "t-g-list": t_g_list_list, "s-list": s_list_list}

    def step_two():

        nonlocal curr_anz, debits, credits, remains, msg_str, t_g_list_list, s_list_list, curr_i, lvcarea, h_artikel, gl_acct, htparam, hoteldpt, h_compli, exrate, artikel, h_cost, h_bill_line
        nonlocal h_art, gl_acc1, gl_acct1


        nonlocal c_list, s_list, g_list, t_g_list, h_art, gl_acc1, gl_acct1
        nonlocal c_list_list, s_list_list, g_list_list, t_g_list_list

        cost_account:str = ""
        cost_value:decimal = 0
        cost:decimal = 0
        rate:decimal = 1
        curr_datum:date = None
        f_endkum:int = 0
        b_endkum:int = 0
        ldry:int = 0
        dstore:int = 0
        transfer_ldry:bool = False
        H_art = H_artikel
        Gl_acc1 = Gl_acct

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1081)).first()
        ldry = finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1082)).first()
        dstore = finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1106)).first()
        transfer_ldry = flogical

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 862)).first()
        f_endkum = finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 892)).first()
        b_endkum = finteger
        s_list_list.clear()

        for hoteldpt in db_session.query(Hoteldpt).filter(
                (Hoteldpt.num != dstore)).all():

            if transfer_ldry or (not transfer_ldry and hoteldpt.num != ldry):

                h_compli_obj_list = []
                for h_compli, h_art in db_session.query(H_compli, H_art).join(H_art,(H_art.departement == H_compli.departement) &  (H_art.artnr == H_compli.p_artnr) &  (H_art.artart == 11)).filter(
                        (H_compli.datum >= from_date) &  (H_compli.datum <= to_date) &  (H_compli.departement == hoteldpt.num) &  (H_compli.betriebsnr == 0)).all():
                    if h_compli._recid in h_compli_obj_list:
                        continue
                    else:
                        h_compli_obj_list.append(h_compli._recid)

                    if double_currency and curr_datum != h_compli.datum:
                        curr_datum = h_compli.datum

                        if foreign_nr != 0:

                            exrate = db_session.query(Exrate).filter(
                                    (Exrate.artnr == foreign_nr) &  (Exrate.datum == curr_datum)).first()
                        else:

                            exrate = db_session.query(Exrate).filter(
                                    (Exrate.datum == curr_datum)).first()

                        if exrate:
                            rate = exrate.betrag
                        else:
                            rate = exchg_rate

                    c_list = query(c_list_list, filters=(lambda c_list :c_list.datum == h_compli.datum and c_list.dept == h_compli.departement and c_list.rechnr == h_compli.rechnr and c_list.p_artnr == h_compli.p_artnr), first=True)

                    if not c_list:

                        h_artikel = db_session.query(H_artikel).filter(
                                (H_artikel.artnr == h_compli.p_artnr) &  (H_artikel.departement == h_compli.departement)).first()

                        artikel = db_session.query(Artikel).filter(
                                (Artikel.artnr == h_Artikel.artnrfront) &  (Artikel.departement == 0)).first()

                        gl_acct = db_session.query(Gl_acct).filter(
                                (Gl_acct.fibukonto == artikel.fibukonto)).first()

                        if not gl_acct:
                            msg_str = msg_str + chr(2) + translateExtended ("G/L Account not found :", lvcarea, "") + " " + artikel.fibukonto + chr(10) + translateExtended ("Dept", lvcarea, "") + " " + to_string(h_artikel.departement, "99") + " - " + to_string(h_artikel.artnr) + " " + h_artikel.bezeich + chr(10) + translateExtended ("Check F/O Article :", lvcarea, "") + " " + to_string(artikel.artnr) + " " + artikel.bezeich
                        c_list = C_list()
                        c_list_list.append(c_list)

                        c_list.datum = h_compli.datum
                        c_list.dept = h_compli.departement
                        c_list.rechnr = h_compli.rechnr
                        c_list.p_artnr = h_compli.p_artnr
                        c_list.fibukonto = artikel.fibukonto
                        c_list.bemerk = "*" + to_string(h_compli.rechnr) + " - " + hoteldpt.depart
                        c_list.add_note = ";&&4;" + to_string(h_compli.departement, "99") + ";" + to_string(h_compli.rechnr) + ";"

                        h_artikel = db_session.query(H_artikel).filter(
                                (H_artikel.artnr == h_compli.artnr) &  (H_artikel.departement == h_compli.departement)).first()

                        artikel = db_session.query(Artikel).filter(
                                (Artikel.artnr == h_Artikel.artnrfront) &  (Artikel.departement == h_Artikel.departement)).first()
                    cost = 0

                    h_cost = db_session.query(H_cost).filter(
                            (H_cost.artnr == h_compli.artnr) &  (H_cost.departement == h_compli.departement) &  (H_cost.datum == h_compli.datum) &  (H_cost.flag == 1)).first()

                    if h_cost and h_cost.betrag != 0:
                        cost = h_compli.anzahl * h_cost.betrag
                        cost = cost_correction(cost)
                        cost = round(cost, 2)
                        c_list.t_cost = c_list.t_cost + cost

                        h_artikel = db_session.query(H_artikel).filter(
                                (H_artikel.artnr == h_cost.artnr) &  (H_artikel.departement == h_cost.departement)).first()

                        artikel = db_session.query(Artikel).filter(
                                (Artikel.artnr == h_Artikel.artnrfront) &  (Artikel.departement == h_Artikel.departement)).first()

                        gl_acct = db_session.query(Gl_acct).filter(
                                (Gl_acct.fibukonto == artikel.bezeich1)).first()

                        if not gl_acct:
                            msg_str = msg_str + chr(2) + translateExtended ("cost Account not found :", lvcarea, "") + " " + artikel.bezeich1 + chr(10) + translateExtended ("Dept", lvcarea, "") + " " + to_string(h_artikel.departement, "99") + " - " + to_string(h_artikel.artnr) + " " + h_artikel.bezeich + chr(10) + translateExtended ("Check F/O Article :", lvcarea, "") + " " + to_string(artikel.artnr) + " " + artikel.bezeich

                        if artikel.umsatzart == 6:
                            c_list.b_cost = c_list.b_cost + cost
                            c_list.b_acct = artikel.bezeich1

                        elif artikel.umsatzart == 3 or artikel.umsatzart == 5:
                            c_list.f_cost = c_list.f_cost + cost
                            c_list.f_acct = artikel.bezeich1
                        else:
                            c_list.o_cost = c_list.o_cost + cost
                            c_list.o_acct = artikel.bezeich1

                    if not h_cost or (h_cost and h_cost.betrag == 0):

                        h_artikel = db_session.query(H_artikel).filter(
                                (H_artikel.artnr == h_compli.artnr) &  (H_artikel.departement == h_compli.departement)).first()
                        cost = h_compli.anzahl * h_compli.epreis * h_artikel.prozent / 100 * rate
                        cost = cost_correction(cost)
                        cost = round(cost, 2)
                        c_list.t_cost = c_list.t_cost + cost

                        artikel = db_session.query(Artikel).filter(
                                (Artikel.artnr == h_Artikel.artnrfront) &  (Artikel.departement == h_Artikel.departement)).first()

                        gl_acct = db_session.query(Gl_acct).filter(
                                (Gl_acct.fibukonto == artikel.bezeich1)).first()

                        if not gl_acct:
                            msg_str = msg_str + chr(2) + translateExtended ("cost Account not found :", lvcarea, "") + " " + artikel.bezeich1 + chr(10) + translateExtended ("Dept", lvcarea, "") + " " + to_string(h_artikel.departement, "99") + " - " + to_string(h_artikel.artnr) + " " + h_artikel.bezeich + chr(10) + translateExtended ("Check F/O Article :", lvcarea, "") + " " + to_string(artikel.artnr) + " " + artikel.bezeich

                        if artikel.umsatzart == 6:
                            c_list.b_cost = c_list.b_cost + cost
                            c_list.b_acct = artikel.bezeich1

                        elif artikel.umsatzart == 3 or artikel.umsatzart == 5:
                            c_list.f_cost = c_list.f_cost + cost
                            c_list.f_acct = artikel.bezeich1
                        else:
                            c_list.o_cost = c_list.o_cost + cost
                            c_list.o_acct = artikel.bezeich1


        for c_list in query(c_list_list, filters=(lambda c_list :c_list.t_cost != 0)):
            add_list()

    def disp_it():

        nonlocal curr_anz, debits, credits, remains, msg_str, t_g_list_list, s_list_list, curr_i, lvcarea, h_artikel, gl_acct, htparam, hoteldpt, h_compli, exrate, artikel, h_cost, h_bill_line
        nonlocal h_art, gl_acc1, gl_acct1


        nonlocal c_list, s_list, g_list, t_g_list, h_art, gl_acc1, gl_acct1
        nonlocal c_list_list, s_list_list, g_list_list, t_g_list_list

        for g_list in query(g_list_list):
            gl_acct = db_session.query(Gl_acct).filter((Gl_acct.fibukonto == g_list.fibukonto)).first()
            if not gl_acct:
                continue

            t_g_list = T_g_list()
            t_g_list_list.append(t_g_list)

            buffer_copy(g_list, t_g_list)
            t_g_list.acct_fibukonto = gl_acct.fibukonto
            t_g_list.bezeich = gl_acct.bezeich

    def add_list():

        nonlocal curr_anz, debits, credits, remains, msg_str, t_g_list_list, s_list_list, curr_i, lvcarea, h_artikel, gl_acct, htparam, hoteldpt, h_compli, exrate, artikel, h_cost, h_bill_line
        nonlocal h_art, gl_acc1, gl_acct1


        nonlocal c_list, s_list, g_list, t_g_list, h_art, gl_acc1, gl_acct1
        nonlocal c_list_list, s_list_list, g_list_list, t_g_list_list

        i:int = 0
        Gl_acct1 = Gl_acct

        s_list = query(s_list_list, filters=(lambda s_list :s_list.fibukonto == c_list.fibukonto), first=True)

        if not s_list:

            gl_acct1 = db_session.query(Gl_acct1).filter(
                    (Gl_acct1.fibukonto == c_list.fibukonto)).first()
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
            g_list.debit = g_list.debit + c_list.t_cost
            debits = debits + c_list.t_cost
            s_list.debit = s_list.debit + c_list.t_cost
        else:
            g_list.credit = g_list.credit - c_list.t_cost
            credits = credits - c_list.t_cost
            s_list.credit = s_list.credit - c_list.t_cost
        g_list.userinit = user_init
        g_list.zeit = get_current_time_in_seconds() + curr_i
        g_list.duplicate = False

        if c_list.f_acct != "":

            s_list = query(s_list_list, filters=(lambda s_list :s_list.fibukonto == c_list.f_acct), first=True)

            if not s_list:

                gl_acct1 = db_session.query(Gl_acct1).filter(
                        (Gl_acct1.fibukonto == c_list.f_acct)).first()
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
                g_list.debit = g_list.debit - c_list.f_cost
                debits = debits - c_list.f_cost
                s_list.debit = s_list.debit - c_list.f_cost
            else:
                g_list.credit = g_list.credit + c_list.f_cost
                credits = credits + c_list.f_cost
                s_list.credit = s_list.credit + c_list.f_cost
            curr_i = curr_i + 1
            g_list.userinit = user_init
            g_list.zeit = get_current_time_in_seconds() + curr_i
            g_list.duplicate = False

        if c_list.b_acct != "":

            s_list = query(s_list_list, filters=(lambda s_list :s_list.fibukonto == c_list.b_acct), first=True)

            if not s_list:

                gl_acct1 = db_session.query(Gl_acct1).filter(
                        (Gl_acct1.fibukonto == c_list.b_acct)).first()
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
                g_list.debit = g_list.debit - c_list.b_cost
                debits = debits - c_list.b_cost
                s_list.debit = s_list.debit - c_list.b_cost
            else:
                g_list.credit = g_list.credit + c_list.b_cost
                credits = credits + c_list.b_cost
                s_list.credit = s_list.credit + c_list.b_cost
            curr_i = curr_i + 1
            g_list.userinit = user_init
            g_list.zeit = get_current_time_in_seconds() + curr_i
            g_list.duplicate = False

        if c_list.o_acct != "":

            s_list = query(s_list_list, filters=(lambda s_list :s_list.fibukonto == c_list.o_acct), first=True)

            if not s_list:

                gl_acct1 = db_session.query(Gl_acct1).filter(
                        (Gl_acct1.fibukonto == c_list.o_acct)).first()
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
                g_list.debit = g_list.debit - c_list.o_cost
                debits = debits - c_list.o_cost
                s_list.debit = s_list.debit - c_list.o_cost
            else:
                g_list.credit = g_list.credit + c_list.o_cost
                credits = credits + c_list.o_cost
                s_list.credit = s_list.credit + c_list.o_cost
            curr_i = curr_i + 1
            g_list.userinit = user_init
            g_list.zeit = get_current_time_in_seconds() + curr_i
            g_list.duplicate = False
        remains = debits - credits

    def cost_correction(cost:decimal):

        nonlocal curr_anz, debits, credits, remains, msg_str, t_g_list_list, s_list_list, curr_i, lvcarea, h_artikel, gl_acct, htparam, hoteldpt, h_compli, exrate, artikel, h_cost, h_bill_line
        nonlocal h_art, gl_acc1, gl_acct1


        nonlocal c_list, s_list, g_list, t_g_list, h_art, gl_acc1, gl_acct1
        nonlocal c_list_list, s_list_list, g_list_list, t_g_list_list

        h_bill_line = db_session.query(H_bill_line).filter(
                (H_bill_line.rechnr == h_compli.rechnr) &  (H_bill_line.bill_datum == h_compli.datum) &  (H_bill_line.departement == h_compli.departement) &  (H_bill_line.artnr == h_compli.artnr) &  (H_bill_line.epreis == h_compli.epreis)).first()

        if h_bill_line and substring(h_bill_line.bezeich, len(h_bill_line.bezeich) - 1, 1) == "*" and h_bill_line.epreis != 0:

            h_artikel = db_session.query(H_artikel).filter(
                    (H_artikel.artnr == h_bill_line.artnr) &  (H_artikel.departement == h_bill_line.departement)).first()

            if h_artikel and h_artikel.artart == 0 and h_artikel.epreis1 > h_bill_line.epreis:
                cost = cost * h_bill_line.epreis / h_artikel.epreis1

    step_two()
    disp_it()

    return generate_output()