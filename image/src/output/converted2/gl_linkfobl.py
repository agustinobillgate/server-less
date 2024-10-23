from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from functions.calc_servtaxesbl import calc_servtaxesbl
from models import Gl_acct, Gl_jouhdr, Htparam, Artikel, Hoteldpt, Umsatz

trans_dept_list, Trans_dept = create_model("Trans_dept", {"nr":int})

def gl_linkfobl(trans_dept_list:[Trans_dept], from_date:date, to_date:date, user_init:str, refno:str, curr_anz:int):
    debits = None
    credits = None
    acct_error = 0
    remains = to_decimal("0.0")
    art_dpt = 0
    art_artnr = 0
    art_bezeich = ""
    buf_g_list_list = []
    curr_date:date = None
    artart_list:List[int] = [1, 9, 3, 9, 9, 2, 2, 4, 0]
    price_decimal:int = 0
    credit_betrag:decimal = to_decimal("0.0")
    debit_betrag:decimal = to_decimal("0.0")
    serv_acctno:str = ""
    vat_acctno:str = ""
    fibukonto:str = ""
    lastdate:date = None
    gl_acct = gl_jouhdr = htparam = artikel = hoteldpt = umsatz = None

    g_list = buf_g_list = trans_dept = gl_acct1 = None

    g_list_list, G_list = create_model("G_list", {"flag":int, "datum":date, "artnr":int, "dept":int, "jnr":int, "fibukonto":str, "debit":decimal, "credit":decimal, "bemerk":str, "userinit":str, "sysdate":date, "zeit":int, "chginit":str, "chgdate":date, "duplicate":bool, "acct_fibukonto":str, "bezeich":str}, {"sysdate": get_current_date(), "chgdate": None, "duplicate": True})
    buf_g_list_list, Buf_g_list = create_model_like(G_list)

    Gl_acct1 = create_buffer("Gl_acct1",Gl_acct)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal debits, credits, acct_error, remains, art_dpt, art_artnr, art_bezeich, buf_g_list_list, curr_date, artart_list, price_decimal, credit_betrag, debit_betrag, serv_acctno, vat_acctno, fibukonto, lastdate, gl_acct, gl_jouhdr, htparam, artikel, hoteldpt, umsatz
        nonlocal from_date, to_date, user_init, refno, curr_anz
        nonlocal gl_acct1


        nonlocal g_list, buf_g_list, trans_dept, gl_acct1
        nonlocal g_list_list, buf_g_list_list, trans_dept_list
        return {"curr_anz": curr_anz, "debits": debits, "credits": credits, "acct_error": acct_error, "remains": remains, "art_dpt": art_dpt, "art_artnr": art_artnr, "art_bezeich": art_bezeich, "buf-g-list": buf_g_list_list}

    def step_two():

        nonlocal debits, credits, acct_error, remains, art_dpt, art_artnr, art_bezeich, buf_g_list_list, curr_date, artart_list, price_decimal, credit_betrag, debit_betrag, serv_acctno, vat_acctno, fibukonto, lastdate, gl_acct, gl_jouhdr, htparam, artikel, hoteldpt, umsatz
        nonlocal from_date, to_date, user_init, refno, curr_anz
        nonlocal gl_acct1


        nonlocal g_list, buf_g_list, trans_dept, gl_acct1
        nonlocal g_list_list, buf_g_list_list, trans_dept_list

        art1 = None
        gl_acc1 = None
        sales:decimal = to_decimal("0.0")
        service:decimal = to_decimal("0.0")
        tax:decimal = to_decimal("0.0")
        tax2:decimal = to_decimal("0.0")
        serv:decimal = to_decimal("0.0")
        vat:decimal = to_decimal("0.0")
        vat2:decimal = to_decimal("0.0")
        fact:decimal = to_decimal("0.0")
        serv_vat:bool = False
        payment:decimal = to_decimal("0.0")
        gledger:decimal = to_decimal("0.0")
        fibu1:str = ""
        vat_fibu:str = ""
        vat2_fibu:str = ""
        serv_fibu:str = ""
        wert:decimal = to_decimal("0.0")
        Art1 =  create_buffer("Art1",Artikel)
        Gl_acc1 =  create_buffer("Gl_acc1",Gl_acct)

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 479)).first()
        serv_vat = htparam.flogical
        debits = 0
        credits = 0


        for curr_date in date_range(from_date,to_date) :
            gledger =  to_decimal("0")

            hoteldpt_obj_list = []
            for hoteldpt in db_session.query(Hoteldpt).order_by(Hoteldpt.num).all():
                trans_dept = query(trans_dept_list, (lambda trans_dept: trans_dept.nr == hoteldpt.num), first=True)
                if not trans_dept:
                    continue

                if hoteldpt._recid in hoteldpt_obj_list:
                    continue
                else:
                    hoteldpt_obj_list.append(hoteldpt._recid)

                for artikel in db_session.query(Artikel).filter(
                         (Artikel.departement == hoteldpt.num) & ((artart == 0) | (artart == 5) | (artart == 8) | (artart == 2) | (artart == 6) | (artart == 7))).order_by(artart_list[Artikel.artart + 1 - 1], Artikel.artnr).all():

                    umsatz = db_session.query(Umsatz).filter(
                             (Umsatz.artnr == artikel.artnr) & (Umsatz.departement == artikel.departement) & (Umsatz.datum == curr_date)).first()

                    if umsatz:

                        gl_acc1 = db_session.query(Gl_acc1).filter(
                                 (Gl_acc1.fibukonto == artikel.fibukonto)).first()

                        if not gl_acc1:
                            art_dpt = artikel.departement
                            art_artnr = artikel.artnr
                            art_bezeich = artikel.bezeich
                            acct_error = 2
                            g_list_list.clear()

                            return
                        else:
                            fibukonto = gl_acc1.fibukonto
                            fibu1 = fibukonto
                        serv =  to_decimal("0")
                        vat =  to_decimal("0")
                        serv_fibu = ""
                        vat_fibu = ""

                        if artikel.service_code != 0:

                            htparam = db_session.query(Htparam).filter(
                                     (Htparam.paramnr == artikel.service_code)).first()

                            if htparam:
                                serv_fibu = entry(0, htparam.fchar, chr(2))

                        if artikel.mwst_code != 0:

                            htparam = db_session.query(Htparam).filter(
                                     (Htparam.paramnr == artikel.mwst_code)).first()

                            if htparam:
                                vat_fibu = entry(0, htparam.fchar, chr(2))

                        if artikel.prov_code != 0:

                            htparam = db_session.query(Htparam).filter(
                                     (Htparam.paramnr == artikel.prov_code)).first()

                            if htparam:
                                vat2_fibu = entry(0, htparam.fchar, chr(2))

                                if trim(vat2_fibu) == "":
                                    acct_error = 3

                                    return

                    for umsatz in db_session.query(Umsatz).filter(
                             (Umsatz.datum == curr_date) & (Umsatz.artnr == artikel.artnr) & (Umsatz.departement == artikel.departement) & (Umsatz.betrag != 0)).order_by(Umsatz._recid).all():
                        serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, umsatz.artnr, umsatz.departement, umsatz.datum))

                        if not gl_acc1:
                            break
                        gledger =  to_decimal(gledger) + to_decimal(umsatz.betrag)

                        if artikel.artart == 0 or artikel.artart == 5 or artikel.artart == 8:
                            wert =  to_decimal(umsatz.betrag) / to_decimal(fact)
                            service = to_decimal(round(wert * serv , price_decimal))
                            tax = to_decimal(round(wert * vat , price_decimal))
                            tax2 = to_decimal(round(wert * vat2 , price_decimal))
                            sales =  to_decimal(umsatz.betrag) - to_decimal(service) - to_decimal(tax) - to_decimal(tax2)

                            if service > 0:
                                credit_betrag =  to_decimal(service)
                                debit_betrag =  to_decimal("0")

                                if serv_fibu != "":
                                    fibukonto = serv_fibu
                                else:
                                    fibukonto = serv_acctno

                                g_list = query(g_list_list, filters=(lambda g_list: g_list.fibukonto.lower()  == (fibukonto).lower()  and g_list.datum == curr_date), first=True)

                                if not g_list:
                                    add_list(-2, True, "", 0, 0)
                                else:
                                    add_list(-2, False, "", 0, 0)

                            elif service < 0:
                                debit_betrag =  - to_decimal(service)
                                credit_betrag =  to_decimal("0")

                                if serv_fibu != "":
                                    fibukonto = serv_fibu
                                else:
                                    fibukonto = serv_acctno

                                g_list = query(g_list_list, filters=(lambda g_list: g_list.fibukonto.lower()  == (fibukonto).lower()  and g_list.datum == curr_date), first=True)

                                if not g_list:
                                    add_list(-2, True, "", 0, 0)
                                else:
                                    add_list(-2, False, "", 0, 0)

                            if tax > 0:
                                credit_betrag =  to_decimal(tax)
                                debit_betrag =  to_decimal("0")

                                if vat_fibu != "":
                                    fibukonto = vat_fibu
                                else:
                                    fibukonto = vat_acctno

                                g_list = query(g_list_list, filters=(lambda g_list: g_list.fibukonto.lower()  == (fibukonto).lower()  and g_list.datum == curr_date), first=True)

                                if not g_list:
                                    add_list(-1, True, "", 0, 0)
                                else:
                                    add_list(-1, False, "", 0, 0)

                            elif tax < 0:
                                debit_betrag =  - to_decimal(tax)
                                credit_betrag =  to_decimal("0")

                                if vat_fibu != "":
                                    fibukonto = vat_fibu
                                else:
                                    fibukonto = vat_acctno

                                g_list = query(g_list_list, filters=(lambda g_list: g_list.fibukonto.lower()  == (fibukonto).lower()  and g_list.datum == curr_date), first=True)

                                if not g_list:
                                    add_list(-1, True, "", 0, 0)
                                else:
                                    add_list(-1, False, "", 0, 0)

                            if tax2 > 0:
                                credit_betrag =  to_decimal(tax2)
                                debit_betrag =  to_decimal("0")
                                fibukonto = vat2_fibu

                                g_list = query(g_list_list, filters=(lambda g_list: g_list.fibukonto.lower()  == (fibukonto).lower()  and g_list.datum == curr_date), first=True)

                                if not g_list:
                                    add_list(-1, True, "", 0, 0)
                                else:
                                    add_list(-1, False, "", 0, 0)

                            elif tax2 < 0:
                                debit_betrag =  - to_decimal(tax2)
                                credit_betrag =  to_decimal("0")
                                fibukonto = vat_fibu

                                g_list = query(g_list_list, filters=(lambda g_list: g_list.fibukonto.lower()  == (fibukonto).lower()  and g_list.datum == curr_date), first=True)

                                if not g_list:
                                    add_list(-1, True, "", 0, 0)
                                else:
                                    add_list(-1, False, "", 0, 0)

                            if sales > 0:
                                credit_betrag =  to_decimal(sales)
                                debit_betrag =  to_decimal("0")
                                fibukonto = gl_acc1.fibukonto

                                g_list = query(g_list_list, filters=(lambda g_list: g_list.artnr == artikel.artnr and g_list.dept == artikel.departement and g_list.fibukonto.lower()  == (fibukonto).lower()  and g_list.datum == curr_date), first=True)

                                if not g_list:
                                    add_list(0, True, (to_string(hoteldpt.num) + " - " + artikel.bezeich + ";&&;" + to_string(artikel.departement) + ";" + to_string(artikel.artnr)), artikel.artnr, artikel.departement)
                                else:
                                    add_list(0, False, (to_string(hoteldpt.num) + " - " + artikel.bezeich), artikel.artnr, artikel.departement)

                            elif sales < 0:
                                fibukonto = gl_acc1.fibukonto
                                debit_betrag =  - to_decimal(sales)
                                credit_betrag =  to_decimal("0")

                                g_list = query(g_list_list, filters=(lambda g_list: g_list.artnr == artikel.artnr and g_list.dept == artikel.departement and g_list.fibukonto.lower()  == (fibukonto).lower()  and g_list.datum == curr_date), first=True)

                                if not g_list:
                                    add_list(0, True, (to_string(hoteldpt.num) + " - " + artikel.bezeich + ";&&;" + to_string(artikel.departement) + ";" + to_string(artikel.artnr)), artikel.artnr, artikel.departement)
                                else:
                                    add_list(0, False, (to_string(hoteldpt.num) + " - " + artikel.bezeich + ";&&;" + to_string(artikel.departement) + ";" + to_string(artikel.artnr)), artikel.artnr, artikel.departement)
                        else:

                            if umsatz.betrag <= 0:
                                fibukonto = gl_acc1.fibukonto
                                debit_betrag =  - to_decimal(umsatz.betrag)
                                credit_betrag =  to_decimal("0")

                                g_list = query(g_list_list, filters=(lambda g_list: g_list.artnr == artikel.artnr and g_list.dept == artikel.departement and g_list.fibukonto.lower()  == (fibukonto).lower()  and g_list.datum == curr_date and g_list.flag != 9), first=True)

                                if not g_list:
                                    add_list(1, True, (to_string(hoteldpt.num) + " - " + artikel.bezeich + ";&&;" + to_string(artikel.departement) + ";" + to_string(artikel.artnr)), artikel.artnr, artikel.departement)
                                else:
                                    add_list(1, False, (to_string(hoteldpt.num) + " - " + artikel.bezeich + ";&&;" + to_string(artikel.departement) + ";" + to_string(artikel.artnr)), artikel.artnr, artikel.departement)

                            elif umsatz.betrag > 0:
                                fibukonto = gl_acc1.fibukonto
                                credit_betrag =  to_decimal(umsatz.betrag)
                                debit_betrag =  to_decimal("0")

                                g_list = query(g_list_list, filters=(lambda g_list: g_list.artnr == artikel.artnr and g_list.dept == artikel.departement and g_list.fibukonto.lower()  == (fibukonto).lower()  and g_list.datum == curr_date and g_list.flag != 9), first=True)

                                if not g_list:
                                    add_list(1, True, (to_string(hoteldpt.num) + " - " + artikel.bezeich + ";&&;" + to_string(artikel.departement) + ";" + to_string(artikel.artnr)), artikel.artnr, artikel.departement)
                                else:
                                    add_list(1, False, (to_string(hoteldpt.num) + " - " + artikel.bezeich + ";&&;" + to_string(artikel.departement) + ";" + to_string(artikel.artnr)), artikel.artnr, artikel.departement)

            htparam = db_session.query(Htparam).filter(
                     (Htparam.paramnr == 998)).first()
            fibukonto = htparam.fchar

            if gledger > 0:
                debit_betrag =  to_decimal(gledger)
                credit_betrag =  to_decimal("0")

                g_list = query(g_list_list, filters=(lambda g_list: g_list.fibukonto.lower()  == (fibukonto).lower()  and g_list.datum == curr_date), first=True)

                if not g_list:
                    add_list(2, True, "", 0, 0)
                else:
                    add_list(2, False, "", 0, 0)

            elif gledger < 0:
                credit_betrag =  - to_decimal(gledger)
                debit_betrag =  to_decimal("0")

                g_list = query(g_list_list, filters=(lambda g_list: g_list.fibukonto.lower()  == (fibukonto).lower()  and g_list.datum == curr_date), first=True)

                if not g_list:
                    add_list(2, True, "", 0, 0)
                else:
                    add_list(2, False, "", 0, 0)

        if acct_error > 0:
            g_list_list.clear()

            return
        modify_glist()

        gl_acct1_obj_list = []
        for gl_acct1 in db_session.query(Gl_acct1).filter(
                 ((Gl_acct1.fibukonto.in_(list(set([g_list.fibukonto for g_list in g_list_list)]))))).order_by(g_list.flag, g_list.sysdate, g_list.zeit).all():
            if gl_acct1._recid in gl_acct1_obj_list:
                continue
            else:
                gl_acct1_obj_list.append(gl_acct1._recid)


            lastdate = curr_date - timedelta(days=1)
            buf_g_list = Buf_g_list()
            buf_g_list_list.append(buf_g_list)

            buffer_copy(g_list, buf_g_list)
            buf_g_list.acct_fibukonto = gl_acct1.fibukonto
            buf_g_list.bezeich = gl_acct1.bezeich

            if buf_g_list.bemerk == "" and buf_g_list.acct_fibukonto == gl_acct1.fibukonto:
                buf_g_list.bemerk = gl_acct1.bezeich + " " + to_string(lastdate)


    def modify_glist():

        nonlocal debits, credits, acct_error, remains, art_dpt, art_artnr, art_bezeich, buf_g_list_list, curr_date, artart_list, price_decimal, credit_betrag, debit_betrag, serv_acctno, vat_acctno, fibukonto, lastdate, gl_acct, gl_jouhdr, htparam, artikel, hoteldpt, umsatz
        nonlocal from_date, to_date, user_init, refno, curr_anz
        nonlocal gl_acct1


        nonlocal g_list, buf_g_list, trans_dept, gl_acct1
        nonlocal g_list_list, buf_g_list_list, trans_dept_list

        for g_list in query(g_list_list):

            gl_acct = db_session.query(Gl_acct).filter(
                     (Gl_acct.fibukonto == g_list.fibukonto)).first()

            if gl_acct:

                if gl_acct.acc_type == 1 or gl_acct.acc_type == 4:

                    if g_list.debit != 0 and g_list.credit > g_list.debit:
                        g_list.credit = to_decimal(round(g_list.credit - g_list.debit , price_decimal))
                        credits = credits - g_list.debit
                        debits = debits - g_list.debit
                        g_list.debit =  to_decimal("0")
                else:

                    if g_list.credit != 0 and g_list.debit > g_list.credit:
                        g_list.debit = to_decimal(round(g_list.debit - g_list.credit , price_decimal))
                        credits = credits - g_list.credit
                        debits = debits - g_list.credit
                        g_list.credit =  to_decimal("0")


    def add_list(flag:int, create_it:bool, bemerk:str, artnr:int, dept:int):

        nonlocal debits, credits, acct_error, remains, art_dpt, art_artnr, art_bezeich, buf_g_list_list, curr_date, artart_list, price_decimal, credit_betrag, debit_betrag, serv_acctno, vat_acctno, fibukonto, lastdate, gl_acct, gl_jouhdr, htparam, artikel, hoteldpt, umsatz
        nonlocal from_date, to_date, user_init, refno, curr_anz
        nonlocal gl_acct1


        nonlocal g_list, buf_g_list, trans_dept, gl_acct1
        nonlocal g_list_list, buf_g_list_list, trans_dept_list


        curr_anz = curr_anz + 1

        if create_it:
            g_list = G_list()
            g_list_list.append(g_list)

            g_list.flag = flag
            g_list.fibukonto = fibukonto
            g_list.bemerk = ""
            g_list.datum = curr_date
            g_list.artnr = artnr
            g_list.dept = dept
        g_list.debit = to_decimal(round(g_list.debit + debit_betrag , price_decimal))
        g_list.credit = to_decimal(round(g_list.credit + credit_betrag , price_decimal))
        g_list.userinit = user_init
        g_list.zeit = get_current_time_in_seconds() + curr_anz
        g_list.duplicate = False
        g_list.bemerk = bemerk
        credits = credits + credit_betrag
        debits = debits + debit_betrag
        remains =  to_decimal(debits) - to_decimal(credits)
        debit_betrag =  to_decimal("0")
        credit_betrag =  to_decimal("0")


    def check_dept():

        nonlocal debits, credits, acct_error, remains, art_dpt, art_artnr, art_bezeich, buf_g_list_list, curr_date, artart_list, price_decimal, credit_betrag, debit_betrag, serv_acctno, vat_acctno, fibukonto, lastdate, gl_acct, gl_jouhdr, htparam, artikel, hoteldpt, umsatz
        nonlocal from_date, to_date, user_init, refno, curr_anz
        nonlocal gl_acct1


        nonlocal g_list, buf_g_list, trans_dept, gl_acct1
        nonlocal g_list_list, buf_g_list_list, trans_dept_list

        i:int = 0
        trans_dept_list.clear()

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 793)).first()

        if htparam.fchar != "":
            for i in range(1,num_entries(htparam.fchar, ",")  + 1) :

                trans_dept = query(trans_dept_list, filters=(lambda trans_dept: trans_dept.nr == to_int(entry(i - 1, htparam.fchar, ","))), first=True)

                if not trans_dept:
                    trans_dept = Trans_dept()
                    trans_dept_list.append(trans_dept)

                    nr = to_int(entry(i - 1, htparam.fchar, ","))


        else:

            for hoteldpt in db_session.query(Hoteldpt).order_by(Hoteldpt._recid).all():
                trans_dept = Trans_dept()
                trans_dept_list.append(trans_dept)

                nr = hoteldpt.num


    gl_jouhdr = db_session.query(Gl_jouhdr).filter(
             (func.lower(Gl_jouhdr.refno) == (refno).lower()) & (Gl_jouhdr.jtype == 1)).first()

    if gl_jouhdr:
        acct_error = 1

        return generate_output()

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 491)).first()
    price_decimal = htparam.finteger

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 133)).first()

    artikel = db_session.query(Artikel).filter(
             (Artikel.artnr == htparam.finteger) & (Artikel.departement == 0)).first()

    if artikel:
        serv_acctno = artikel.fibukonto

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 132)).first()

    artikel = db_session.query(Artikel).filter(
             (Artikel.artnr == htparam.finteger) & (Artikel.departement == 0)).first()

    if artikel:
        vat_acctno = artikel.fibukonto
    check_dept()
    step_two()

    return generate_output()