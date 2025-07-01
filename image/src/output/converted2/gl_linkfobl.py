#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.calc_servtaxesbl import calc_servtaxesbl
from models import Gl_acct, Gl_jouhdr, Htparam, Artikel, Hoteldpt, Umsatz

trans_dept_list, Trans_dept = create_model("Trans_dept", {"nr":int})

def gl_linkfobl(trans_dept_list:[Trans_dept], from_date:date, to_date:date, user_init:string, refno:string, curr_anz:int):

    prepare_cache ([Gl_acct, Htparam, Artikel, Hoteldpt, Umsatz])

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
    credit_betrag:Decimal = to_decimal("0.0")
    debit_betrag:Decimal = to_decimal("0.0")
    serv_acctno:string = ""
    vat_acctno:string = ""
    fibukonto:string = ""
    lastdate:date = None
    gl_acct = gl_jouhdr = htparam = artikel = hoteldpt = umsatz = None

    g_list = buf_g_list = trans_dept = gl_acct1 = None

    g_list_list, G_list = create_model("G_list", {"flag":int, "datum":date, "artnr":int, "dept":int, "jnr":int, "fibukonto":string, "debit":Decimal, "credit":Decimal, "bemerk":string, "userinit":string, "sysdate":date, "zeit":int, "chginit":string, "chgdate":date, "duplicate":bool, "acct_fibukonto":string, "bezeich":string}, {"sysdate": get_current_date(), "chgdate": None, "duplicate": True})
    buf_g_list_list, Buf_g_list = create_model_like(G_list)

    Gl_acct1 = create_buffer("Gl_acct1",Gl_acct)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal debits, credits, acct_error, remains, art_dpt, art_artnr, art_bezeich, buf_g_list_list, curr_date, artart_list, price_decimal, credit_betrag, debit_betrag, serv_acctno, vat_acctno, fibukonto, lastdate, gl_acct, gl_jouhdr, htparam, artikel, hoteldpt, umsatz
        nonlocal from_date, to_date, user_init, refno, curr_anz
        nonlocal gl_acct1


        nonlocal g_list, buf_g_list, trans_dept, gl_acct1
        nonlocal g_list_list, buf_g_list_list

        return {"curr_anz": curr_anz, "debits": debits, "credits": credits, "acct_error": acct_error, "remains": remains, "art_dpt": art_dpt, "art_artnr": art_artnr, "art_bezeich": art_bezeich, "buf-g-list": buf_g_list_list}

    def step_two():

        nonlocal debits, credits, acct_error, remains, art_dpt, art_artnr, art_bezeich, buf_g_list_list, curr_date, artart_list, price_decimal, credit_betrag, debit_betrag, serv_acctno, vat_acctno, fibukonto, lastdate, gl_acct, gl_jouhdr, htparam, artikel, hoteldpt, umsatz
        nonlocal from_date, to_date, user_init, refno, curr_anz
        nonlocal gl_acct1


        nonlocal g_list, buf_g_list, trans_dept, gl_acct1
        nonlocal g_list_list, buf_g_list_list

        art1 = None
        gl_acc1 = None
        sales:Decimal = to_decimal("0.0")
        service:Decimal = to_decimal("0.0")
        tax:Decimal = to_decimal("0.0")
        tax2:Decimal = to_decimal("0.0")
        serv:Decimal = to_decimal("0.0")
        vat:Decimal = to_decimal("0.0")
        vat2:Decimal = to_decimal("0.0")
        fact:Decimal = to_decimal("0.0")
        serv_vat:bool = False
        payment:Decimal = to_decimal("0.0")
        gledger:Decimal = to_decimal("0.0")
        fibu1:string = ""
        vat_fibu:string = ""
        vat2_fibu:string = ""
        serv_fibu:string = ""
        wert:Decimal = to_decimal("0.0")
        divered_rental:int = 0
        bartikel = None
        Art1 =  create_buffer("Art1",Artikel)
        Gl_acc1 =  create_buffer("Gl_acc1",Gl_acct)
        Bartikel =  create_buffer("Bartikel",Artikel)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 1052)]})

        if htparam:
            divered_rental = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 479)]})
        serv_vat = htparam.flogical
        debits = 0
        credits = 0


        for curr_date in date_range(from_date,to_date) :
            gledger =  to_decimal("0")

            hoteldpt_obj_list = {}
            for hoteldpt in db_session.query(Hoteldpt).order_by(Hoteldpt.num).all():
                trans_dept = query(trans_dept_list, (lambda trans_dept: trans_dept.nr == hoteldpt.num), first=True)
                if not trans_dept:
                    continue

                if hoteldpt_obj_list.get(hoteldpt._recid):
                    continue
                else:
                    hoteldpt_obj_list[hoteldpt._recid] = True

                for artikel in db_session.query(Artikel).filter(
                         (Artikel.departement == hoteldpt.num) & ((Artikel.artart == 0) | (Artikel.artart == 5) | (Artikel.artart == 8) | (Artikel.artart == 2) | (Artikel.artart == 6) | (Artikel.artart == 7))).order_by(artart_list[Artikel.artart + 1 - 1], Artikel.artnr).all():

                    umsatz = get_cache (Umsatz, {"artnr": [(eq, artikel.artnr)],"departement": [(eq, artikel.departement)],"datum": [(eq, curr_date)]})

                    if umsatz:

                        gl_acc1 = get_cache (Gl_acct, {"fibukonto": [(eq, artikel.fibukonto)]})

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

                            htparam = get_cache (Htparam, {"paramnr": [(eq, artikel.service_code)]})

                            if htparam:
                                serv_fibu = entry(0, htparam.fchar, chr_unicode(2))

                        if artikel.mwst_code != 0:

                            htparam = get_cache (Htparam, {"paramnr": [(eq, artikel.mwst_code)]})

                            if htparam:
                                vat_fibu = entry(0, htparam.fchar, chr_unicode(2))

                        if artikel.prov_code != 0:

                            htparam = get_cache (Htparam, {"paramnr": [(eq, artikel.prov_code)]})

                            if htparam:
                                vat2_fibu = entry(0, htparam.fchar, chr_unicode(2))

                                if trim(vat2_fibu) == "":
                                    acct_error = 3

                                    return

                    for umsatz in db_session.query(Umsatz).filter(
                             (Umsatz.datum == curr_date) & (Umsatz.artnr == artikel.artnr) & (Umsatz.departement == artikel.departement) & (Umsatz.betrag != 0)).order_by(Umsatz._recid).yield_per(100):
                        serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, umsatz.artnr, umsatz.departement, umsatz.datum))

                        if not gl_acc1:
                            break
                        gledger =  to_decimal(gledger) + to_decimal(umsatz.betrag)

                        if artikel.artart == 0 or artikel.artart == 5 or artikel.artart == 8:
                            wert =  to_decimal(umsatz.betrag) / to_decimal(fact)
                            service =  to_decimal(wert) * to_decimal(serv)
                            tax =  to_decimal(wert) * to_decimal(vat)
                            tax2 =  to_decimal(wert) * to_decimal(vat2)

                            if price_decimal == 0:
                                service = to_decimal(round(service , 0))
                                tax = to_decimal(round(tax , 0))
                                tax2 = to_decimal(round(tax2 , 0))


                            else:
                                service = to_decimal(round(service , price_decimal))
                                tax = to_decimal(round(tax , price_decimal))
                                tax2 = to_decimal(round(tax2 , price_decimal))


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

                for artikel in db_session.query(Artikel).filter(
                         (Artikel.departement == hoteldpt.num) & (Artikel.artart == 13)).order_by(artart_list[Artikel.artart + 1 - 1], Artikel.artnr).all():

                    umsatz = get_cache (Umsatz, {"artnr": [(eq, artikel.artnr)],"departement": [(eq, artikel.departement)],"datum": [(eq, curr_date)]})

                    if umsatz:

                        gl_acc1 = get_cache (Gl_acct, {"fibukonto": [(eq, artikel.fibukonto)]})

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

                            htparam = get_cache (Htparam, {"paramnr": [(eq, artikel.service_code)]})

                            if htparam:
                                serv_fibu = entry(0, htparam.fchar, chr_unicode(2))

                        if artikel.mwst_code != 0:

                            htparam = get_cache (Htparam, {"paramnr": [(eq, artikel.mwst_code)]})

                            if htparam:
                                vat_fibu = entry(0, htparam.fchar, chr_unicode(2))

                        if artikel.prov_code != 0:

                            htparam = get_cache (Htparam, {"paramnr": [(eq, artikel.prov_code)]})

                            if htparam:
                                vat2_fibu = entry(0, htparam.fchar, chr_unicode(2))

                                if trim(vat2_fibu) == "":
                                    acct_error = 3

                                    return

                    for umsatz in db_session.query(Umsatz).filter(
                             (Umsatz.datum == curr_date) & (Umsatz.artnr == artikel.artnr) & (Umsatz.departement == artikel.departement) & (Umsatz.betrag != 0)).order_by(Umsatz._recid).yield_per(100):
                        serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, umsatz.artnr, umsatz.departement, umsatz.datum))

                        if not gl_acc1:
                            break

                        if artikel.artart == 13:
                            wert =  to_decimal(umsatz.betrag) / to_decimal(fact)
                            service =  to_decimal(wert) * to_decimal(serv)
                            tax =  to_decimal(wert) * to_decimal(vat)
                            tax2 =  to_decimal(wert) * to_decimal(vat2)

                            if price_decimal == 0:
                                service = to_decimal(round(service , 0))
                                tax = to_decimal(round(tax , 0))
                                tax2 = to_decimal(round(tax2 , 0))


                            else:
                                service = to_decimal(round(service , price_decimal))
                                tax = to_decimal(round(tax , price_decimal))
                                tax2 = to_decimal(round(tax2 , price_decimal))


                            sales =  to_decimal(umsatz.betrag) - to_decimal(service) - to_decimal(tax) - to_decimal(tax2)

                            if sales > 0:
                                credit_betrag =  to_decimal(sales)
                                debit_betrag =  to_decimal("0")
                                fibukonto = gl_acc1.fibukonto

                                g_list = query(g_list_list, filters=(lambda g_list: g_list.artnr == artikel.artnr and g_list.dept == artikel.departement and g_list.fibukonto.lower()  == (fibukonto).lower()  and g_list.datum == curr_date), first=True)

                                if not g_list:
                                    add_list(0, True, (to_string(hoteldpt.num) + " - " + artikel.bezeich + ";&&;" + to_string(artikel.departement) + ";" + to_string(artikel.artnr)), artikel.artnr, artikel.departement)
                                else:
                                    add_list(0, False, (to_string(hoteldpt.num) + " - " + artikel.bezeich), artikel.artnr, artikel.departement)

                                bartikel = get_cache (Artikel, {"artnr": [(eq, divered_rental)],"departement": [(eq, 0)]})
                                credit_betrag =  to_decimal("0")
                                debit_betrag =  - to_decimal(sales)
                                fibukonto = bartikel.fibukonto

                                g_list = query(g_list_list, filters=(lambda g_list: g_list.artnr == bartikel.artnr and g_list.dept == bartikel.departement and g_list.fibukonto.lower()  == (fibukonto).lower()  and g_list.datum == curr_date), first=True)

                                if not g_list:
                                    add_list(0, True, (to_string(hoteldpt.num) + " - " + bartikel.bezeich + ";&&;" + to_string(bartikel.departement) + ";" + to_string(bartikel.artnr)), bartikel.artnr, bartikel.departement)
                                else:
                                    add_list(0, False, (to_string(hoteldpt.num) + " - " + bartikel.bezeich), bartikel.artnr, bartikel.departement)

                            elif sales < 0:
                                fibukonto = gl_acc1.fibukonto
                                debit_betrag =  - to_decimal(sales)
                                credit_betrag =  to_decimal("0")

                                g_list = query(g_list_list, filters=(lambda g_list: g_list.artnr == artikel.artnr and g_list.dept == artikel.departement and g_list.fibukonto.lower()  == (fibukonto).lower()  and g_list.datum == curr_date), first=True)

                                if not g_list:
                                    add_list(0, True, (to_string(hoteldpt.num) + " - " + artikel.bezeich + ";&&;" + to_string(artikel.departement) + ";" + to_string(artikel.artnr)), artikel.artnr, artikel.departement)
                                else:
                                    add_list(0, False, (to_string(hoteldpt.num) + " - " + artikel.bezeich + ";&&;" + to_string(artikel.departement) + ";" + to_string(artikel.artnr)), artikel.artnr, artikel.departement)

                                bartikel = get_cache (Artikel, {"artnr": [(eq, divered_rental)],"departement": [(eq, 0)]})
                                credit_betrag =  to_decimal(sales)
                                debit_betrag =  to_decimal("0")
                                fibukonto = bartikel.fibukonto

                                g_list = query(g_list_list, filters=(lambda g_list: g_list.artnr == bartikel.artnr and g_list.dept == bartikel.departement and g_list.fibukonto.lower()  == (fibukonto).lower()  and g_list.datum == curr_date), first=True)

                                if not g_list:
                                    add_list(0, True, (to_string(hoteldpt.num) + " - " + bartikel.bezeich + ";&&;" + to_string(bartikel.departement) + ";" + to_string(bartikel.artnr)), bartikel.artnr, bartikel.departement)
                                else:
                                    add_list(0, False, (to_string(hoteldpt.num) + " - " + bartikel.bezeich), bartikel.artnr, bartikel.departement)

            htparam = get_cache (Htparam, {"paramnr": [(eq, 998)]})
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

        gl_acct1_obj_list = {}
        for gl_acct1 in db_session.query(Gl_acct1).filter(
                 ((Gl_acct1.fibukonto.in_(list(set([g_list.fibukonto for g_list in g_list_list])))))).order_by(g_list.flag, g_list.sysdate, g_list.zeit).all():
            if gl_acct1_obj_list.get(gl_acct1._recid):
                continue
            else:
                gl_acct1_obj_list[gl_acct1._recid] = True


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
        nonlocal g_list_list, buf_g_list_list

        for g_list in query(g_list_list):

            gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, g_list.fibukonto)]})

            if gl_acct:

                if gl_acct.acc_type == 1 or gl_acct.acc_type == 4:

                    if g_list.debit != 0 and g_list.credit > g_list.debit:
                        g_list.credit =  to_decimal(g_list.credit) - to_decimal(g_list.debit)
                        credits = credits - g_list.debit
                        debits = debits - g_list.debit
                        g_list.debit =  to_decimal("0")
                else:

                    if g_list.credit != 0 and g_list.debit > g_list.credit:
                        g_list.debit =  to_decimal(g_list.debit) - to_decimal(g_list.credit)
                        credits = credits - g_list.credit
                        debits = debits - g_list.credit
                        g_list.credit =  to_decimal("0")


    def add_list(flag:int, create_it:bool, bemerk:string, artnr:int, dept:int):

        nonlocal debits, credits, acct_error, remains, art_dpt, art_artnr, art_bezeich, buf_g_list_list, curr_date, artart_list, price_decimal, credit_betrag, debit_betrag, serv_acctno, vat_acctno, fibukonto, lastdate, gl_acct, gl_jouhdr, htparam, artikel, hoteldpt, umsatz
        nonlocal from_date, to_date, user_init, refno, curr_anz
        nonlocal gl_acct1


        nonlocal g_list, buf_g_list, trans_dept, gl_acct1
        nonlocal g_list_list, buf_g_list_list


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
        g_list.debit =  to_decimal(g_list.debit) + to_decimal(debit_betrag)
        g_list.credit =  to_decimal(g_list.credit) + to_decimal(credit_betrag)
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
        nonlocal g_list_list, buf_g_list_list

        i:int = 0
        trans_dept_list.clear()

        htparam = get_cache (Htparam, {"paramnr": [(eq, 793)]})

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


    gl_jouhdr = get_cache (Gl_jouhdr, {"refno": [(eq, refno)],"jtype": [(eq, 1)]})

    if gl_jouhdr:
        acct_error = 1

        return generate_output()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
    price_decimal = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 133)]})

    artikel = get_cache (Artikel, {"artnr": [(eq, finteger)],"departement": [(eq, 0)]})

    if artikel:
        serv_acctno = artikel.fibukonto

    htparam = get_cache (Htparam, {"paramnr": [(eq, 132)]})

    artikel = get_cache (Artikel, {"artnr": [(eq, finteger)],"departement": [(eq, 0)]})

    if artikel:
        vat_acctno = artikel.fibukonto
    check_dept()
    step_two()

    return generate_output()