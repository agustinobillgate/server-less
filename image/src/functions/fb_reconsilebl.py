from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from functions.calc_servtaxesbl import calc_servtaxesbl
from models import Htparam, Waehrung, H_artikel, L_bestand, L_besthis, Gl_acct, L_lager, L_artikel, L_op, L_ophdr, Hoteldpt, H_compli, Exrate, Artikel, Gl_main, H_cost, Umsatz, H_bill_line

def fb_reconsilebl(pvilanguage:int, case_type:int, from_date:date, to_date:date, from_grp:int, mi_opt:bool, date1:date, date2:date):
    done = False
    fbreconsile_list_list = []
    curr_nr:int = 0
    curr_reihe:int = 0
    ldry:int = 0
    dstore:int = 0
    long_digit:bool = False
    foreign_nr:int = 0
    exchg_rate:decimal = 1
    double_currency:bool = False
    type_of_acct:int = 0
    counter:int = 0
    coa_format:str = ""
    f_date:date = None
    lvcarea:str = "fb_reconsile"
    htparam = waehrung = h_artikel = l_bestand = l_besthis = gl_acct = l_lager = l_artikel = l_op = l_ophdr = hoteldpt = h_compli = exrate = artikel = gl_main = h_cost = umsatz = h_bill_line = None

    fbreconsile_list = s_list = h_art = l_oh = l_ohist = gl_acct1 = None

    fbreconsile_list_list, Fbreconsile_list = create_model("Fbreconsile_list", {"nr":int, "code":int, "bezeich":str, "col1":str, "col2":str, "col3":str, "col4":str, "col5":str})
    s_list_list, S_list = create_model("S_list", {"code":int, "reihenfolge":int, "lager_nr":int, "l_bezeich":str, "fibukonto":str, "bezeich":str, "flag":int, "anf_wert":decimal, "end_wert":decimal, "betrag":decimal}, {"reihenfolge": 1, "flag": 2})

    H_art = H_artikel
    L_oh = L_bestand
    L_ohist = L_besthis
    Gl_acct1 = Gl_acct

    db_session = local_storage.db_session

    def generate_output():
        nonlocal done, fbreconsile_list_list, curr_nr, curr_reihe, ldry, dstore, long_digit, foreign_nr, exchg_rate, double_currency, type_of_acct, counter, coa_format, f_date, lvcarea, htparam, waehrung, h_artikel, l_bestand, l_besthis, gl_acct, l_lager, l_artikel, l_op, l_ophdr, hoteldpt, h_compli, exrate, artikel, gl_main, h_cost, umsatz, h_bill_line
        nonlocal h_art, l_oh, l_ohist, gl_acct1


        nonlocal fbreconsile_list, s_list, h_art, l_oh, l_ohist, gl_acct1
        nonlocal fbreconsile_list_list, s_list_list
        return {"done": done, "fbreconsile-list": fbreconsile_list_list}

    def create_list():

        nonlocal done, fbreconsile_list_list, curr_nr, curr_reihe, ldry, dstore, long_digit, foreign_nr, exchg_rate, double_currency, type_of_acct, counter, coa_format, f_date, lvcarea, htparam, waehrung, h_artikel, l_bestand, l_besthis, gl_acct, l_lager, l_artikel, l_op, l_ophdr, hoteldpt, h_compli, exrate, artikel, gl_main, h_cost, umsatz, h_bill_line
        nonlocal h_art, l_oh, l_ohist, gl_acct1


        nonlocal fbreconsile_list, s_list, h_art, l_oh, l_ohist, gl_acct1
        nonlocal fbreconsile_list_list, s_list_list

        betrag1:decimal = 0
        betrag2:decimal = 0
        betrag3:decimal = 0
        betrag4:decimal = 0
        betrag5:decimal = 0
        betrag6:decimal = 0
        betrag61:decimal = 0
        betrag62:decimal = 0
        betrag56:decimal = 0
        consume2:decimal = 0
        flag:int = 0
        f_eknr:int = 0
        b_eknr:int = 0
        fl_eknr:int = 0
        bl_eknr:int = 0
        f_cost:decimal = 0
        b_cost:decimal = 0
        f_sales:decimal = 0
        b_sales:decimal = 0
        tf_sales:decimal = 0
        tb_sales:decimal = 0
        f_ratio:decimal = 0
        b_ratio:decimal = 0
        fibu:str = ""
        h_service:decimal = 0
        h_mwst:decimal = 0
        amount:decimal = 0
        i:int = 0
        bev_food:str = ""
        food_bev:str = ""
        curr_datum:date = None
        rate:decimal = 1
        qty1:decimal = 0
        qty:decimal = 0
        wert:decimal = 0
        fibukonto:str = ""
        bezeich:str = ""
        H_art = H_artikel
        L_oh = L_bestand
        L_ohist = L_besthis
        Gl_acct1 = Gl_acct
        s_list_list.clear()
        fbreconsile_list_list.clear()
        curr_nr = 0
        curr_reihe = 0

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 862)).first()
        f_eknr = finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 892)).first()
        b_eknr = finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 257)).first()
        fl_eknr = finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 258)).first()
        bl_eknr = finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 272)).first()
        bev_food = fchar

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 275)).first()
        food_bev = fchar

        gl_acct = db_session.query(Gl_acct).filter(
                (func.lower(Gl_acct.fibukonto) == (bev_food).lower())).first()
        s_list = S_list()
        s_list_list.append(s_list)

        s_list.reihenfolge = 1
        s_list.lager_nr = 9999
        s_list.l_bezeich = to_string(gl_acct.fibukonto, coa_format) + " " + gl_acct.bezeich.upper()
        s_list.flag = 0

        gl_acct = db_session.query(Gl_acct).filter(
                (func.lower(Gl_acct.fibukonto) == (food_bev).lower())).first()
        s_list = S_list()
        s_list_list.append(s_list)

        s_list.reihenfolge = 2
        s_list.lager_nr = 9999
        s_list.l_bezeich = to_string(gl_acct.fibukonto, coa_format) + " " + gl_acct.bezeich.upper()
        s_list.flag = 0

        for l_lager in db_session.query(L_lager).all():

            l_bestand_obj_list = []
            for l_bestand, l_oh, l_artikel in db_session.query(L_bestand, L_oh, L_artikel).join(L_oh,(L_oh.artnr == L_bestand.artnr) &  (L_oh.lager_nr == 0)).join(L_artikel,(L_artikel.artnr == L_bestand.artnr) &  ((L_artikel.endkum == fl_eknr) |  (L_artikel.endkum == bl_eknr))).filter(
                    (L_bestand.lager_nr == l_lager.lager_nr)).all():
                if l_bestand._recid in l_bestand_obj_list:
                    continue
                else:
                    l_bestand_obj_list.append(l_bestand._recid)

                if l_artikel.endkum == fl_eknr:
                    flag = 1

                elif l_artikel.endkum == bl_eknr:
                    flag = 2
                qty1 = l_bestand.anz_anf_best + l_bestand.anz_eingang - l_bestand.anz_ausgang
                qty = l_oh.anz_anf_best + l_oh.anz_eingang - l_oh.anz_ausgang
                wert = l_oh.val_anf_best + l_oh.wert_eingang - l_oh.wert_ausgang

                s_list = query(s_list_list, filters=(lambda s_list :s_list.lager_nr == l_lager.lager_nr and s_list.reihenfolge == flag and s_list.flag == 0), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_list.append(s_list)

                    s_list.reihenfolge = flag
                    s_list.lager_nr = l_lager.lager_nr
                    s_list.l_bezeich = l_lager.bezeich
                    s_list.flag = 0

                if l_bestand.anz_anf_best != 0:
                    s_list.anf_wert = s_list.anf_wert + l_bestand.anz_anf_best * l_bestand.val_anf_best / l_bestand.anz_anf_best

                if qty != 0:
                    s_list.end_wert = s_list.end_wert + wert * qty1 / qty

                for l_op in db_session.query(L_op).filter(
                        (L_op.datum >= from_date) &  (L_op.datum <= to_date) &  (L_op.artnr == l_artikel.artnr) &  (L_op.op_art == 1) &  (L_op.loeschflag <= 1) &  (L_op.lager_nr == l_lager.lager_nr)).all():

                    l_ophdr = db_session.query(L_ophdr).filter(
                            (L_ophdr.lscheinnr == l_op.lscheinnr) &  (func.lower(L_ophdr.op_typ) == "STI")).first()

                    if l_op.anzahl >= 0:

                        s_list = query(s_list_list, filters=(lambda s_list :s_list.lager_nr == l_lager.lager_nr and s_list.reihenfolge == flag and s_list.flag == 11), first=True)

                        if not s_list:
                            s_list = S_list()
                            s_list_list.append(s_list)

                            s_list.reihenfolge = flag
                            s_list.lager_nr = l_lager.lager_nr
                            s_list.l_bezeich = l_lager.bezeich
                            s_list.flag = 11
                        s_list.betrag = s_list.betrag + l_op.warenwert

                    elif l_op.anzahl < 0:

                        s_list = query(s_list_list, filters=(lambda s_list :s_list.lager_nr == l_lager.lager_nr and s_list.reihenfolge == flag and s_list.flag == 12), first=True)

                        if not s_list:
                            s_list = S_list()
                            s_list_list.append(s_list)

                            s_list.reihenfolge = flag
                            s_list.lager_nr = l_lager.lager_nr
                            s_list.l_bezeich = l_lager.bezeich
                            s_list.flag = 12
                        s_list.betrag = s_list.betrag + l_op.warenwert

                l_op_obj_list = []
                for l_op, l_ophdr, gl_acct in db_session.query(L_op, L_ophdr, Gl_acct).join(L_ophdr,(L_ophdr.lscheinnr == L_op.lscheinnr) &  (func.lower(L_ophdr.op_typ) == "STT") &  (L_ophdr.fibukonto != "")).join(Gl_acct,(Gl_acct.fibukonto == l_ophdr.fibukonto)).filter(
                        (L_op.datum >= from_date) &  (L_op.datum <= to_date) &  (L_op.artnr == l_artikel.artnr) &  (L_op.loeschflag <= 1) &  (L_op.op_art == 3) &  (L_op.lager_nr == l_lager.lager_nr)).all():
                    if l_op._recid in l_op_obj_list:
                        continue
                    else:
                        l_op_obj_list.append(l_op._recid)


                    type_of_acct = gl_acct.acc_type
                    fibukonto = gl_acct.fibukonto
                    bezeich = to_string(gl_acct.fibukonto, coa_format) + " " + gl_acct.bezeich.upper()

                    if l_op.stornogrund != "":

                        gl_acct1 = db_session.query(Gl_acct1).filter(
                                    (Gl_acct1.fibukonto == l_op.stornogrund)).first()

                        if gl_acct1:
                            type_of_acct = gl_acct1.acc_type
                            fibukonto = gl_acct1.fibukonto
                            bezeich = to_string(gl_acct1.fibukonto, coa_format) + " " + gl_acct1.bezeich.upper()

                    if flag == 1 and fibukonto.lower()  == (food_bev).lower() :

                        s_list = query(s_list_list, filters=(lambda s_list :s_list.lager_nr == 9999 and s_list.reihenfolge == 2), first=True)
                        s_list.anf_wert = s_list.anf_wert + l_op.warenwert

                    elif flag == 2 and fibukonto.lower()  == (bev_food).lower() :

                        s_list = query(s_list_list, filters=(lambda s_list :s_list.lager_nr == 9999 and s_list.reihenfolge == 1), first=True)
                        s_list.anf_wert = s_list.anf_wert + l_op.warenwert
                    else:

                        s_list = query(s_list_list, filters=(lambda s_list :s_list.(fibukonto).lower().lower()  == (fibukonto).lower()  and s_list.reihenfolge == flag and s_list.flag == 5), first=True)

                        if not s_list:
                            s_list = S_list()
                            s_list_list.append(s_list)

                            s_list.reihenfolge = flag
                            s_list.fibukonto = fibukonto
                            s_list.bezeich = bezeich
                            s_list.flag = 5

                        if type_of_acct == 5 or type_of_acct == 3 or type_of_acct == 4:
                            s_list.betrag = s_list.betrag + l_op.warenwert

        for hoteldpt in db_session.query(Hoteldpt).filter(
                (Hoteldpt.num != ldry) &  (Hoteldpt.num != dstore)).all():

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

                artikel = db_session.query(Artikel).filter(
                        (Artikel.artnr == h_art.artnrfront) &  (Artikel.departement == 0)).first()

                gl_acct = db_session.query(Gl_acct).filter(
                        (Gl_acct.fibukonto == artikel.fibukonto)).first()

                gl_main = db_session.query(Gl_main).filter(
                        (Gl_main.nr == gl_acct.main_nr)).first()

                h_artikel = db_session.query(H_artikel).filter(
                        (H_artikel.departement == h_compli.departement) &  (H_artikel.artnr == h_compli.artnr)).first()

                artikel = db_session.query(Artikel).filter(
                        (Artikel.artnr == h_Artikel.artnrfront) &  (Artikel.departement == h_Artikel.departement)).first()
                f_cost = 0
                b_cost = 0

                h_cost = db_session.query(H_cost).filter(
                        (H_cost.artnr == h_compli.artnr) &  (H_cost.departement == h_compli.departement) &  (H_cost.datum == h_compli.datum) &  (H_cost.flag == 1)).first()

                if h_cost and h_cost.betrag != 0:

                    if artikel.umsatzart == 6:
                        b_cost = h_compli.anzahl * h_cost.betrag

                    elif artikel.umsatzart == 3 or artikel.umsatzart == 5:
                        f_cost = h_compli.anzahl * h_cost.betrag
                    f_cost = cost_correction(f_cost)

                elif not h_cost or (h_cost and h_cost.betrag == 0):

                    if artikel.umsatzart == 6:
                        b_cost = h_compli.anzahl * h_compli.epreis * h_artikel.prozent / 100 * rate

                    elif artikel.umsatzart == 3 or artikel.umsatzart == 5:
                        f_cost = h_compli.anzahl * h_compli.epreis * h_artikel.prozent / 100 * rate

                if f_cost != 0:

                    if mi_opt == False:

                        s_list = query(s_list_list, filters=(lambda s_list :s_list.fibukonto == gl_acct.fibukonto and s_list.reihenfolge == 1 and s_list.flag == 4), first=True)

                        if not s_list:
                            s_list = S_list()
                            s_list_list.append(s_list)

                            s_list.reihenfolge = 1
                            s_list.fibukonto = gl_acct.fibukonto
                            s_list.bezeich = to_string(gl_acct.fibukonto, coa_format) + " " + gl_acct.bezeich.upper()
                            s_list.flag = 4
                    else:

                        s_list = query(s_list_list, filters=(lambda s_list :s_list.code == gl_main.code and s_list.reihenfolge == 1 and s_list.flag == 4), first=True)

                        if not s_list:
                            s_list = S_list()
                            s_list_list.append(s_list)

                            s_list.reihenfolge = 1
                            s_list.code = gl_main.code
                            s_list.bezeich = gl_main.bezeich
                            s_list.flag = 4
                    s_list.betrag = s_list.betrag + f_cost

                if b_cost != 0:

                    if mi_opt == False:

                        s_list = query(s_list_list, filters=(lambda s_list :s_list.fibukonto == gl_acct.fibukonto and s_list.reihenfolge == 2 and s_list.flag == 4), first=True)

                        if not s_list:
                            s_list = S_list()
                            s_list_list.append(s_list)

                            s_list.reihenfolge = 2
                            s_list.fibukonto = gl_acct.fibukonto
                            s_list.bezeich = to_string(gl_acct.fibukonto, coa_format) + " " + gl_acct.bezeich.upper()
                            s_list.flag = 4
                    else:

                        s_list = query(s_list_list, filters=(lambda s_list :s_list.code == gl_main.code and s_list.reihenfolge == 2 and s_list.flag == 4), first=True)

                        if not s_list:
                            s_list = S_list()
                            s_list_list.append(s_list)

                            s_list.reihenfolge = 2
                            s_list.code = gl_main.code
                            s_list.bezeich = gl_main.bezeich
                            s_list.flag = 4
                    s_list.betrag = s_list.betrag + b_cost
        tf_sales, tb_sales = fb_sales(f_eknr, b_eknr)

        if from_grp == 0 or from_grp == 1:
            fbreconsile_list = Fbreconsile_list()
            fbreconsile_list_list.append(fbreconsile_list)

            curr_nr = curr_nr + 1
            fbreconsile_list.nr = curr_nr
            fbreconsile_list.col2 = to_string(translateExtended ("** FOOD **", lvcarea, "") , "x(33)")
            fbreconsile_list = Fbreconsile_list()
            fbreconsile_list_list.append(fbreconsile_list)

            curr_nr = curr_nr + 1
            fbreconsile_list.nr = curr_nr
            i = 0
            fbreconsile_list = Fbreconsile_list()
            fbreconsile_list_list.append(fbreconsile_list)

            curr_nr = curr_nr + 1
            fbreconsile_list.nr = curr_nr
            fbreconsile_list.col1 = to_string(translateExtended ("1. Opening Inventory", lvcarea, "") , "x(24)")

            for s_list in query(s_list_list, filters=(lambda s_list :s_list.flag == 0 and s_list.reihenfolge == 1 and s_list.lager_nr != 9999 and s_list.anf_wert != 0)):
                i = i + 1
                betrag1 = betrag1 + s_list.anf_wert

                if i > 1:
                    fbreconsile_list = Fbreconsile_list()
                    fbreconsile_list_list.append(fbreconsile_list)

                    curr_nr = curr_nr + 1
                    fbreconsile_list.nr = curr_nr
                    fbreconsile_list.col1 = to_string("", "x(24)")

                if not long_digit:
                    pass
                    fbreconsile_list.col2 = to_string(s_list.l_bezeich, "x(33)")
                    fbreconsile_list.col3 = to_string(s_list.anf_wert, "->>>,>>>,>>9.99")
                else:
                    pass
                    fbreconsile_list.col2 = to_string(s_list.l_bezeich, "x(33)")
                    fbreconsile_list.col3 = to_string(s_list.anf_wert, "->>,>>>,>>>,>>9")
            fbreconsile_list = Fbreconsile_list()
            fbreconsile_list_list.append(fbreconsile_list)

            curr_nr = curr_nr + 1
            fbreconsile_list.nr = curr_nr

            if not long_digit:
                fbreconsile_list.col2 = to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)")
                fbreconsile_list.col4 = to_string(betrag1, "->>>,>>>,>>9.99")


            else:
                fbreconsile_list.col2 = to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)")
                fbreconsile_list.col4 = to_string(betrag1, "->>,>>>,>>>,>>9")


            i = 0
            fbreconsile_list = Fbreconsile_list()
            fbreconsile_list_list.append(fbreconsile_list)

            curr_nr = curr_nr + 1
            fbreconsile_list.nr = curr_nr
            fbreconsile_list.col1 = to_string(translateExtended ("2. Incoming Stocks", lvcarea, "") , "x(24)")

            for s_list in query(s_list_list, filters=(lambda s_list :s_list.flag == 11 and s_list.reihenfolge == 1)):
                i = i + 1
                betrag2 = betrag2 + s_list.betrag

                if i > 1:
                    fbreconsile_list = Fbreconsile_list()
                    fbreconsile_list_list.append(fbreconsile_list)

                    curr_nr = curr_nr + 1
                    fbreconsile_list.nr = curr_nr
                    fbreconsile_list.col1 = to_string("", "x(24)")

                if not long_digit:
                    pass
                    fbreconsile_list.col2 = to_string(s_list.l_bezeich, "x(33)")
                    fbreconsile_list.col3 = to_string(s_list.betrag, "->>>,>>>,>>9.99")
                else:
                    pass
                    fbreconsile_list.col2 = to_string(s_list.l_bezeich, "x(33)")
                    fbreconsile_list.col3 = to_string(s_list.betrag, "->>,>>>,>>>,>>9")
            fbreconsile_list = Fbreconsile_list()
            fbreconsile_list_list.append(fbreconsile_list)

            curr_nr = curr_nr + 1
            fbreconsile_list.nr = curr_nr

            if not long_digit:
                fbreconsile_list.col2 = to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)")
                fbreconsile_list.col4 = to_string(betrag2, "->>>,>>>,>>9.99")
            else:
                fbreconsile_list.col2 = to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)")
                fbreconsile_list.col4 = to_string(betrag2, "->>,>>>,>>>,>>9")
            i = 0
            fbreconsile_list = Fbreconsile_list()
            fbreconsile_list_list.append(fbreconsile_list)

            curr_nr = curr_nr + 1
            fbreconsile_list.nr = curr_nr
            fbreconsile_list.col1 = to_string(translateExtended ("3. Returned Stocks", lvcarea, "") , "x(24)")

            for s_list in query(s_list_list, filters=(lambda s_list :s_list.flag == 12 and s_list.reihenfolge == 1)):
                i = i + 1
                betrag3 = betrag3 + s_list.betrag

                if i > 1:
                    fbreconsile_list = Fbreconsile_list()
                    fbreconsile_list_list.append(fbreconsile_list)

                    curr_nr = curr_nr + 1
                    fbreconsile_list.nr = curr_nr
                    fbreconsile_list.col1 = to_string("", "x(24)")

                if not long_digit:
                    pass
                    fbreconsile_list.col2 = to_string(s_list.l_bezeich, "x(33)")
                    fbreconsile_list.col3 = to_string(s_list.betrag, "->>>,>>>,>>9.99")
                else:
                    pass
                    fbreconsile_list.col2 = to_string(s_list.l_bezeich, "x(33)")
                    fbreconsile_list.col3 = to_string(s_list.betrag, "->>,>>>,>>>,>>9")
            fbreconsile_list = Fbreconsile_list()
            fbreconsile_list_list.append(fbreconsile_list)

            curr_nr = curr_nr + 1
            fbreconsile_list.nr = curr_nr

            if not long_digit:
                fbreconsile_list.col2 = to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)")
                fbreconsile_list.col4 = to_string(betrag3, "->>>,>>>,>>9.99")
            else:
                fbreconsile_list.col2 = to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)")
                fbreconsile_list.col4 = to_string(betrag3, "->>,>>>,>>>,>>9")

            s_list = query(s_list_list, filters=(lambda s_list :s_list.lager_nr == 9999 and s_list.reihenfolge == 1), first=True)
            fbreconsile_list = Fbreconsile_list()
            fbreconsile_list_list.append(fbreconsile_list)

            curr_nr = curr_nr + 1
            fbreconsile_list.nr = curr_nr

            if not long_digit:
                fbreconsile_list.col1 = ("4. " + s_list.l_bezeich)
                fbreconsile_list.col4 = to_string(s_list.anf_wert, "->>>,>>>,>>9.99")
            else:
                fbreconsile_list.col1 = ("4. " + s_list.l_bezeich)
                fbreconsile_list.col4 = to_string(s_list.anf_wert, "->>,>>>,>>>,>>9")
            fbreconsile_list = Fbreconsile_list()
            fbreconsile_list_list.append(fbreconsile_list)

            curr_nr = curr_nr + 1
            fbreconsile_list.nr = curr_nr
            betrag4 = betrag1 + betrag2 + betrag3 + s_list.anf_wert
            fbreconsile_list = Fbreconsile_list()
            fbreconsile_list_list.append(fbreconsile_list)

            curr_nr = curr_nr + 1
            fbreconsile_list.nr = curr_nr

            if not long_digit:
                fbreconsile_list.col1 = to_string(translateExtended ("5. Inventory Available", lvcarea, "") , "x(24)")
                fbreconsile_list.col2 = to_string("(1 + 2 + 3 + 4)", "x(33)")
                fbreconsile_list.col3 = to_string("", "x(15)")
                fbreconsile_list.col4 = to_string(betrag4, "->>>,>>>,>>9.99")
            else:
                fbreconsile_list.col1 = to_string(translateExtended ("5. Inventory Available", lvcarea, "") , "x(24)")
                fbreconsile_list.col2 = to_string("(1 + 2 + 3 + 4)", "x(33)")
                fbreconsile_list.col3 = to_string("", "x(15)")
                fbreconsile_list.col4 = to_string(betrag4, "->>,>>>,>>>,>>9")
            fbreconsile_list = Fbreconsile_list()
            fbreconsile_list_list.append(fbreconsile_list)

            curr_nr = curr_nr + 1
            fbreconsile_list.nr = curr_nr
            i = 0
            fbreconsile_list = Fbreconsile_list()
            fbreconsile_list_list.append(fbreconsile_list)

            curr_nr = curr_nr + 1
            fbreconsile_list.nr = curr_nr
            fbreconsile_list.col1 = to_string(translateExtended ("6. Closing Inventory", lvcarea, "") , "x(24)")

            for s_list in query(s_list_list, filters=(lambda s_list :s_list.flag == 0 and s_list.reihenfolge == 1 and s_list.lager_nr != 9999 and s_list.end_wert != 0)):
                i = i + 1
                betrag5 = betrag5 + s_list.end_wert

                if i > 1:
                    fbreconsile_list = Fbreconsile_list()
                    fbreconsile_list_list.append(fbreconsile_list)

                    curr_nr = curr_nr + 1
                    fbreconsile_list.nr = curr_nr
                    fbreconsile_list.col1 = to_string("", "x(24)")

                if not long_digit:
                    fbreconsile_list.col2 = to_string(s_list.l_bezeich, "x(33)")
                    fbreconsile_list.col3 = to_string(s_list.end_wert, "->>>,>>>,>>9.99")


                else:
                    fbreconsile_list.col2 = to_string(s_list.l_bezeich, "x(33)")
                    fbreconsile_list.col3 = to_string(s_list.end_wert, "->>,>>>,>>>,>>9")


            fbreconsile_list = Fbreconsile_list()
            fbreconsile_list_list.append(fbreconsile_list)

            curr_nr = curr_nr + 1
            fbreconsile_list.nr = curr_nr

            if not long_digit:
                fbreconsile_list.col2 = to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)")
                fbreconsile_list.col4 = to_string(betrag5, "->>>,>>>,>>9.99")
            else:
                fbreconsile_list.col2 = to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)")
                fbreconsile_list.col4 = to_string(betrag5, "->>,>>>,>>>,>>9")
            fbreconsile_list = Fbreconsile_list()
            fbreconsile_list_list.append(fbreconsile_list)

            curr_nr = curr_nr + 1
            fbreconsile_list.nr = curr_nr
            betrag56 = betrag4 - betrag5

            if not long_digit:
                fbreconsile_list.col1 = to_string(translateExtended ("7. Gross Consumption", lvcarea, "") , "x(24)")
                fbreconsile_list.col2 = to_string("(5 - 6)", "x(33)")
                fbreconsile_list.col4 = to_string(betrag56, "->>>,>>>,>>9.99")
            else:
                fbreconsile_list.col1 = to_string(translateExtended ("7. Gross Consumption", lvcarea, "") , "x(24)")
                fbreconsile_list.col2 = to_string("(5 - 6)", "x(33)")
                fbreconsile_list.col4 = to_string(betrag56, "->>,>>>,>>>,>>9")
            fbreconsile_list = Fbreconsile_list()
            fbreconsile_list_list.append(fbreconsile_list)

            curr_nr = curr_nr + 1
            fbreconsile_list.nr = curr_nr
            fbreconsile_list = Fbreconsile_list()
            fbreconsile_list_list.append(fbreconsile_list)

            curr_nr = curr_nr + 1
            fbreconsile_list.nr = curr_nr
            fbreconsile_list.col1 = to_string(translateExtended ("8. Credits", lvcarea, "") , "x(24)")

            if mi_opt == False:
                fbreconsile_list = Fbreconsile_list()
                fbreconsile_list_list.append(fbreconsile_list)

                curr_nr = curr_nr + 1
                fbreconsile_list.nr = curr_nr
                fbreconsile_list.col1 = to_string(translateExtended ("- Compliment cost", lvcarea, "") , "x(24)")
                counter = 0
            else:
                counter = 1

            for s_list in query(s_list_list, filters=(lambda s_list :s_list.flag == 4 and s_list.reihenfolge == 1 and s_list.betrag != 0)):
                betrag6 = betrag6 + s_list.betrag
                counter = counter + 1

                if counter > 1:
                    fbreconsile_list = Fbreconsile_list()
                    fbreconsile_list_list.append(fbreconsile_list)

                    fbreconsile_list.nr = curr_nr

                    if s_list.code > 0:
                        fbreconsile_list.code = s_list.code
                    else:
                        fbreconsile_list.code = counter
                    fbreconsile_list.col1 = to_string("", "x(24)")

                if not long_digit:
                    fbreconsile_list.col2 = to_string(s_list.bezeich, "x(33)")
                    fbreconsile_list.col3 = to_string(s_list.betrag, "->>>,>>>,>>9.99")


                else:
                    fbreconsile_list.col2 = to_string(s_list.bezeich, "x(33)")
                    fbreconsile_list.col3 = to_string(s_list.betrag, "->>,>>>,>>>,>>9")

            if mi_opt == False:
                fbreconsile_list = Fbreconsile_list()
                fbreconsile_list_list.append(fbreconsile_list)

                curr_nr = curr_nr + 1
                fbreconsile_list.nr = curr_nr
                fbreconsile_list = Fbreconsile_list()
                fbreconsile_list_list.append(fbreconsile_list)

                curr_nr = curr_nr + 1
                fbreconsile_list.nr = curr_nr
                fbreconsile_list.col1 = to_string(translateExtended ("- Department Expenses", lvcarea, "") , "x(24)")
                counter = 0
            else:
                counter = 1

            for s_list in query(s_list_list, filters=(lambda s_list :s_list.flag == 5 and s_list.reihenfolge == 1 and s_list.betrag != 0)):
                betrag6 = betrag6 + s_list.betrag
                counter = counter + 1

                if counter > 1:
                    fbreconsile_list = Fbreconsile_list()
                    fbreconsile_list_list.append(fbreconsile_list)

                    fbreconsile_list.nr = curr_nr

                    if s_list.code > 0:
                        fbreconsile_list.code = s_list.code
                    else:
                        fbreconsile_list.code = counter
                    fbreconsile_list.col1 = to_string("", "x(24)")

                if not long_digit:
                    fbreconsile_list.col2 = to_string(s_list.bezeich, "x(33)")
                    fbreconsile_list.col3 = to_string(s_list.betrag, "->>>,>>>,>>9.99")


                else:
                    fbreconsile_list.col2 = to_string(s_list.bezeich, "x(33)")
                    fbreconsile_list.col3 = to_string(s_list.betrag, "->>,>>>,>>>,>>9")

            s_list = query(s_list_list, filters=(lambda s_list :s_list.reihenfolge == 2 and s_list.lager_nr == 9999), first=True)
            fbreconsile_list = Fbreconsile_list()
            fbreconsile_list_list.append(fbreconsile_list)

            curr_nr = curr_nr + 1
            fbreconsile_list.nr = curr_nr
            fbreconsile_list.col1 = to_string("", "x(24)")

            if not long_digit:
                fbreconsile_list.col2 = to_string(s_list.l_bezeich, "x(33)")
                fbreconsile_list.col3 = to_string(s_list.anf_wert, "->>>,>>>,>>9.99")


            else:
                fbreconsile_list.col2 = to_string(s_list.l_bezeich, "x(33)")
                fbreconsile_list.col3 = to_string(s_list.anf_wert, "->>,>>>,>>>,>>9")


            betrag6 = betrag6 + s_list.anf_wert

            if mi_opt == False:
                fbreconsile_list = Fbreconsile_list()
                fbreconsile_list_list.append(fbreconsile_list)

                curr_nr = curr_nr + 1
                fbreconsile_list.nr = curr_nr
                fbreconsile_list = Fbreconsile_list()
                fbreconsile_list_list.append(fbreconsile_list)

                curr_nr = curr_nr + 1
                fbreconsile_list.nr = curr_nr

                if not long_digit:
                    fbreconsile_list.col2 = to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)")
                    fbreconsile_list.col4 = to_string(betrag6, "->>>,>>>,>>9.99")


                else:
                    fbreconsile_list.col2 = to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)")
                    fbreconsile_list.col4 = to_string(betrag6, "->>,>>>,>>>,>>9")


            fbreconsile_list = Fbreconsile_list()
            fbreconsile_list_list.append(fbreconsile_list)

            curr_nr = curr_nr + 1
            fbreconsile_list.nr = curr_nr
            consume2 = betrag56 - betrag6
            fbreconsile_list = Fbreconsile_list()
            fbreconsile_list_list.append(fbreconsile_list)

            curr_nr = curr_nr + 1
            fbreconsile_list.nr = curr_nr

            if not long_digit:
                fbreconsile_list.col1 = to_string(translateExtended ("9. Net Consumption", lvcarea, "") , "x(24)")
                fbreconsile_list.col2 = to_string("(7 - 8)", "x(33)")
                fbreconsile_list.col4 = to_string(consume2, "->>>,>>>,>>9.99")


            else:
                fbreconsile_list.col1 = to_string(translateExtended ("9. Net Consumption", lvcarea, "") , "x(24)")
                fbreconsile_list.col2 = to_string("(7 - 8)", "x(33)")
                fbreconsile_list.col4 = to_string(consume2, "->>,>>>,>>>,>>9")


            fbreconsile_list = Fbreconsile_list()
            fbreconsile_list_list.append(fbreconsile_list)

            curr_nr = curr_nr + 1
            fbreconsile_list.nr = curr_nr
            fbreconsile_list = Fbreconsile_list()
            fbreconsile_list_list.append(fbreconsile_list)

            curr_nr = curr_nr + 1
            fbreconsile_list.nr = curr_nr
            f_ratio = 0

            if tf_sales != 0:
                f_ratio = round(consume2, 2) / round(tf_sales, 2) * 100

            if f_ratio == None:
                f_ratio = 0

            if not long_digit:
                fbreconsile_list.col1 = to_string(translateExtended ("Net Food Sales", lvcarea, "") , "x(24)")
                fbreconsile_list.col2 = to_string("", "x(16)") + to_string(tf_sales, "->,>>>,>>>,>>9.99")
                fbreconsile_list.col3 = to_string(translateExtended ("     cost:Sales", lvcarea, "") , "x(15)")
                fbreconsile_list.col4 = to_string(f_ratio, "->,>>>,>>9.99 %")


            else:
                fbreconsile_list.col1 = to_string(translateExtended ("Net Food Sales", lvcarea, "") , "x(24)")
                fbreconsile_list.col2 = to_string("", "x(16)") + to_string(tf_sales, " ->>>,>>>,>>>,>>9")
                fbreconsile_list.col3 = to_string(translateExtended ("     cost:Sales", lvcarea, "") , "x(15)")
                fbreconsile_list.col4 = to_string(f_ratio, "->,>>>,>>9.99 %")

        if from_grp == 1:

            return
        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_list.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr
        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_list.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr
        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_list.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr
        fbreconsile_list.col2 = to_string(translateExtended ("** BEVERAGE **", lvcarea, "") , "x(33)")
        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_list.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr
        i = 0
        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_list.append(fbreconsile_list)

        betrag1 = 0
        fbreconsile_list.col1 = to_string(translateExtended ("1. Opening Inventory", lvcarea, "") , "x(24)")

        for s_list in query(s_list_list, filters=(lambda s_list :s_list.flag == 0 and s_list.reihenfolge == 2 and s_list.lager_nr != 9999 and s_list.anf_wert != 0)):
            i = i + 1
            betrag1 = betrag1 + s_list.anf_wert

            if i > 1:
                fbreconsile_list = Fbreconsile_list()
                fbreconsile_list_list.append(fbreconsile_list)

                curr_nr = curr_nr + 1
                fbreconsile_list.nr = curr_nr
                fbreconsile_list.col1 = to_string("", "x(24)")

            if not long_digit:
                fbreconsile_list.col2 = to_string(s_list.l_bezeich, "x(33)")
                fbreconsile_list.col3 = to_string(s_list.anf_wert, "->>>,>>>,>>9.99")


            else:
                fbreconsile_list.col2 = to_string(s_list.l_bezeich, "x(33)")
                fbreconsile_list.col3 = to_string(s_list.anf_wert, "->>,>>>,>>>,>>9")


        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_list.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr

        if not long_digit:
            fbreconsile_list.col2 = to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)")
            fbreconsile_list.col4 = to_string(betrag1, "->>>,>>>,>>9.99")


        else:
            fbreconsile_list.col2 = to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)")
            fbreconsile_list.col4 = to_string(betrag1, "->>,>>>,>>>,>>9")


        i = 0
        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_list.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr
        fbreconsile_list.col1 = to_string(translateExtended ("2. Incoming Stocks", lvcarea, "") , "x(24)")
        betrag2 = 0

        for s_list in query(s_list_list, filters=(lambda s_list :s_list.flag == 11 and s_list.reihenfolge == 2)):
            i = i + 1
            betrag2 = betrag2 + s_list.betrag

            if i > 1:
                fbreconsile_list = Fbreconsile_list()
                fbreconsile_list_list.append(fbreconsile_list)

                curr_nr = curr_nr + 1
                fbreconsile_list.nr = curr_nr
                fbreconsile_list.col1 = to_string("", "x(24)")

            if not long_digit:
                fbreconsile_list.col2 = to_string(s_list.l_bezeich, "x(33)")
                fbreconsile_list.col3 = to_string(s_list.betrag, "->>>,>>>,>>9.99")


            else:
                fbreconsile_list.col2 = to_string(s_list.l_bezeich, "x(33)")
                fbreconsile_list.col3 = to_string(s_list.betrag, "->>,>>>,>>>,>>9")


        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_list.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr

        if not long_digit:
            fbreconsile_list.col2 = to_string("", "x(24)") + translateExtended ("SUB TOTAL", lvcarea, "")
            fbreconsile_list.col4 = to_string(betrag2, "->>>,>>>,>>9.99")


        else:
            fbreconsile_list.col2 = to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)")
            fbreconsile_list.col4 = to_string(betrag2, "->>,>>>,>>>,>>9")


        i = 0
        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_list.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr
        fbreconsile_list.col1 = to_string(translateExtended ("3. Returned Stocks", lvcarea, "") , "x(24)")
        betrag3 = 0

        for s_list in query(s_list_list, filters=(lambda s_list :s_list.flag == 12 and s_list.reihenfolge == 2)):
            i = i + 1
            betrag3 = betrag3 + s_list.betrag

            if i > 1:
                fbreconsile_list = Fbreconsile_list()
                fbreconsile_list_list.append(fbreconsile_list)

                curr_nr = curr_nr + 1
                fbreconsile_list.nr = curr_nr
                fbreconsile_list.col1 = to_string("", "x(24)")

            if not long_digit:
                fbreconsile_list.col2 = to_string(s_list.l_bezeich, "x(33)")
                fbreconsile_list.col4 = to_string(s_list.betrag, "->>>,>>>,>>9.99")


            else:
                fbreconsile_list.col2 = to_string(s_list.l_bezeich, "x(33)")
                fbreconsile_list.col4 = to_string(s_list.betrag, "->>,>>>,>>>,>>9")


        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_list.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr

        if not long_digit:
            fbreconsile_list.col2 = to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)")
            fbreconsile_list.col4 = to_string(betrag3, "->>>,>>>,>>9.99")


        else:
            fbreconsile_list.col2 = to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)")
            fbreconsile_list.col4 = to_string(betrag3, "->>,>>>,>>>,>>9")

        s_list = query(s_list_list, filters=(lambda s_list :s_list.lager_nr == 9999 and s_list.reihenfolge == 2), first=True)
        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_list.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr

        if not long_digit:
            fbreconsile_list.col1 = to_string(("4. " + s_list.l_bezeich) , "x(24)")
            fbreconsile_list.col4 = to_string(s_list.anf_wert, "->>>,>>>,>>9.99")


        else:
            fbreconsile_list.col1 = to_string(("4. " + s_list.l_bezeich) , "x(24)")
            fbreconsile_list.col4 = to_string(s_list.anf_wert, "->>,>>>,>>>,>>9")


        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_list.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr
        betrag4 = betrag1 + betrag2 + betrag3 + s_list.anf_wert
        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_list.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr

        if not long_digit:
            fbreconsile_list.col1 = to_string(translateExtended ("5. Inventory Available", lvcarea, "") , "x(24)")
            fbreconsile_list.col2 = to_string("(1 + 2 + 3 + 4)", "x(33)")
            fbreconsile_list.col4 = to_string(betrag4, "->>>,>>>,>>9.99")


        else:
            fbreconsile_list.col1 = to_string(translateExtended ("5. Inventory Available", lvcarea, "") , "x(24)")
            fbreconsile_list.col2 = to_string("(1 + 2 + 3 + 4)", "x(33)")
            fbreconsile_list.col4 = to_string(betrag4, "->>,>>>,>>>,>>9")


        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_list.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr
        i = 0
        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_list.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr
        fbreconsile_list.col1 = to_string(translateExtended ("6. Closing Inventory", lvcarea, "") , "x(24)")


        betrag5 = 0

        for s_list in query(s_list_list, filters=(lambda s_list :s_list.flag == 0 and s_list.reihenfolge == 2 and s_list.lager_nr != 9999 and s_list.end_wert != 0)):
            i = i + 1
            betrag5 = betrag5 + s_list.end_wert

            if i > 1:
                fbreconsile_list = Fbreconsile_list()
                fbreconsile_list_list.append(fbreconsile_list)

                curr_nr = curr_nr + 1
                fbreconsile_list.nr = curr_nr
                fbreconsile_list.col1 = to_string("", "x(24)")

            if not long_digit:
                fbreconsile_list.col2 = to_string(s_list.l_bezeich, "x(33)")
                fbreconsile_list.col3 = to_string(s_list.end_wert, "->>>,>>>,>>9.99")


            else:
                fbreconsile_list.col2 = to_string(s_list.l_bezeich, "x(33)")
                fbreconsile_list.col3 = to_string(s_list.end_wert, "->>,>>>,>>>,>>9")


        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_list.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr

        if not long_digit:
            fbreconsile_list.col2 = to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)")
            fbreconsile_list.col4 = to_string(betrag5, "->>>,>>>,>>9.99")


        else:
            fbreconsile_list.col2 = to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)")
            fbreconsile_list.col4 = to_string(betrag5, "->>,>>>,>>>,>>9")


        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_list.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr
        betrag56 = betrag4 - betrag5

        if not long_digit:
            fbreconsile_list.col1 = to_string(translateExtended ("7. Gross Consumption", lvcarea, "") , "x(24)")
            fbreconsile_list.col2 = to_string("(5 - 6)", "x(33)")
            fbreconsile_list.col4 = to_string(betrag56, "->>>,>>>,>>9.99")


        else:
            fbreconsile_list.col1 = to_string(translateExtended ("7. Gross Consumption", lvcarea, "") , "x(24)")
            fbreconsile_list.col2 = to_string("(5 - 6)", "x(33)")
            fbreconsile_list.col4 = to_string(betrag56, "->>,>>>,>>>,>>9")


        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_list.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr
        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_list.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr
        fbreconsile_list.col1 = to_string(translateExtended ("8. Credits", lvcarea, "") , "x(24)")
        betrag6 = 0

        if mi_opt == False:
            fbreconsile_list = Fbreconsile_list()
            fbreconsile_list_list.append(fbreconsile_list)

            curr_nr = curr_nr + 1
            fbreconsile_list.nr = curr_nr
            fbreconsile_list.col1 = to_string(translateExtended ("- Compliment cost", lvcarea, "") , "x(24)")
            counter = 0
        else:
            counter = 1

        for s_list in query(s_list_list, filters=(lambda s_list :s_list.flag == 4 and s_list.reihenfolge == 2 and s_list.betrag != 0)):
            betrag6 = betrag6 + s_list.betrag
            counter = counter + 1

            if counter > 1:
                fbreconsile_list = Fbreconsile_list()
                fbreconsile_list_list.append(fbreconsile_list)

                fbreconsile_list.nr = curr_nr

                if s_list.code > 0:
                    fbreconsile_list.code = s_list.code
                else:
                    fbreconsile_list.code = counter
                fbreconsile_list.col1 = to_string("", "x(24)")

            if not long_digit:
                fbreconsile_list.col2 = to_string(s_list.bezeich, "x(33)")
                fbreconsile_list.col3 = to_string(s_list.betrag, "->>>,>>>,>>9.99")


            else:
                fbreconsile_list.col2 = to_string(s_list.bezeich, "x(33)")
                fbreconsile_list.col3 = to_string(s_list.betrag, "->>,>>>,>>>,>>9")

        if mi_opt == False:
            fbreconsile_list = Fbreconsile_list()
            fbreconsile_list_list.append(fbreconsile_list)

            curr_nr = curr_nr + 1
            fbreconsile_list.nr = curr_nr
            fbreconsile_list.col1 = to_string(translateExtended ("- Department Expenses", lvcarea, "") , "x(24)")
            counter = 0
        else:
            counter = 1

        for s_list in query(s_list_list, filters=(lambda s_list :s_list.flag == 5 and s_list.reihenfolge == 2 and s_list.betrag != 0)):
            counter = counter + 1
            betrag6 = betrag6 + s_list.betrag

            if counter > 1:
                fbreconsile_list = Fbreconsile_list()
                fbreconsile_list_list.append(fbreconsile_list)

                fbreconsile_list.nr = curr_nr

                if s_list.code > 0:
                    fbreconsile_list.code = s_list.code
                else:
                    fbreconsile_list.code = counter
                fbreconsile_list.col1 = to_string("", "x(24)")

            if not long_digit:
                fbreconsile_list.col2 = to_string(s_list.bezeich, "x(33)")
                fbreconsile_list.col3 = to_string(s_list.betrag, "->>>,>>>,>>9.99")


            else:
                fbreconsile_list.col2 = to_string(s_list.bezeich, "x(33)")
                fbreconsile_list.col3 = to_string(s_list.betrag, "->>,>>>,>>>,>>9")

        s_list = query(s_list_list, filters=(lambda s_list :s_list.reihenfolge == 1 and s_list.lager_nr == 9999), first=True)
        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_list.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr
        fbreconsile_list.col1 = to_string("", "x(24)")

        if not long_digit:
            fbreconsile_list.col2 = to_string(s_list.l_bezeich, "x(33)")
            fbreconsile_list.col3 = to_string(s_list.anf_wert, "->>>,>>>,>>9.99")


        else:
            fbreconsile_list.col2 = to_string(s_list.l_bezeich, "x(33)")
            fbreconsile_list.col3 = to_string(s_list.anf_wert, "->>,>>>,>>>,>>9")


        betrag6 = betrag6 + s_list.anf_wert

        if mi_opt == False:
            fbreconsile_list = Fbreconsile_list()
            fbreconsile_list_list.append(fbreconsile_list)

            curr_nr = curr_nr + 1
            fbreconsile_list.nr = curr_nr
        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_list.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr

        if not long_digit:
            fbreconsile_list.col2 = to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)")
            fbreconsile_list.col4 = to_string(betrag6, "->>>,>>>,>>9.99")


        else:
            fbreconsile_list.col2 = to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)")
            fbreconsile_list.col4 = to_string(betrag6, "->>,>>>,>>>,>>9")


        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_list.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr
        consume2 = betrag56 - betrag6
        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_list.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr

        if not long_digit:
            fbreconsile_list.col1 = to_string(translateExtended ("9. Net Consumption", lvcarea, "") , "x(24)")
            fbreconsile_list.col2 = to_string("(7 - 8)", "x(33)")
            fbreconsile_list.col4 = to_string(consume2, "->>>,>>>,>>9.99")


        else:
            fbreconsile_list.col1 = to_string(translateExtended ("9. Net Consumption", lvcarea, "") , "x(24)")
            fbreconsile_list.col2 = to_string("(7 - 8)", "x(33)")
            fbreconsile_list.col4 = to_string(consume2, "->>,>>>,>>>,>>9")


        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_list.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr
        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_list.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr
        b_ratio = 0

        if tb_sales != 0:
            b_ratio = consume2 / tb_sales * 100

        if not long_digit:
            fbreconsile_list.col1 = to_string(translateExtended ("Net Beverage Sales", lvcarea, "") , "x(24)")
            fbreconsile_list.col2 = to_string("", "x(16)") + to_string(tb_sales, "->,>>>,>>>,>>9.99")
            fbreconsile_list.col3 = to_string(translateExtended ("     cost:Sales", lvcarea, "") , "x(15)")
            fbreconsile_list.col4 = to_string(b_ratio, "->,>>>,>>9.99 %")


        else:
            fbreconsile_list.col1 = to_string(translateExtended ("Net Beverage Sales", lvcarea, "") , "x(24)")
            fbreconsile_list.col2 = to_string("", "x(16)") + to_string(tb_sales, " ->>>,>>>,>>>,>>9")
            fbreconsile_list.col3 = to_string(translateExtended ("     cost:Sales", lvcarea, "") , "x(15)")
            fbreconsile_list.col4 = to_string(b_ratio, "->,>>>,>>9.99 %")


        done = True

    def create_food():

        nonlocal done, fbreconsile_list_list, curr_nr, curr_reihe, ldry, dstore, long_digit, foreign_nr, exchg_rate, double_currency, type_of_acct, counter, coa_format, f_date, lvcarea, htparam, waehrung, h_artikel, l_bestand, l_besthis, gl_acct, l_lager, l_artikel, l_op, l_ophdr, hoteldpt, h_compli, exrate, artikel, gl_main, h_cost, umsatz, h_bill_line
        nonlocal h_art, l_oh, l_ohist, gl_acct1


        nonlocal fbreconsile_list, s_list, h_art, l_oh, l_ohist, gl_acct1
        nonlocal fbreconsile_list_list, s_list_list

        betrag1:decimal = 0
        betrag2:decimal = 0
        betrag3:decimal = 0
        betrag4:decimal = 0
        betrag5:decimal = 0
        betrag6:decimal = 0
        betrag61:decimal = 0
        betrag62:decimal = 0
        betrag56:decimal = 0
        consume2:decimal = 0
        flag:int = 0
        f_eknr:int = 0
        b_eknr:int = 0
        fl_eknr:int = 0
        bl_eknr:int = 0
        f_cost:decimal = 0
        b_cost:decimal = 0
        f_sales:decimal = 0
        b_sales:decimal = 0
        tf_sales:decimal = 0
        tb_sales:decimal = 0
        f_ratio:decimal = 0
        b_ratio:decimal = 0
        fibu:str = ""
        h_service:decimal = 0
        h_mwst:decimal = 0
        amount:decimal = 0
        i:int = 0
        bev_food:str = ""
        food_bev:str = ""
        fb_str:[str] = ["", "", ""]
        curr_datum:date = None
        rate:decimal = 1
        qty1:decimal = 0
        qty:decimal = 0
        wert:decimal = 0
        fibukonto:str = ""
        bezeich:str = ""
        fb_str[0] = translateExtended ("Beverage to Food", lvcarea, "")
        fb_str[1] = translateExtended ("Food to Beverage", lvcarea, "")
        H_art = H_artikel
        L_oh = L_bestand
        Gl_acct1 = Gl_acct
        curr_nr = 0
        curr_reihe = 0

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 862)).first()
        f_eknr = finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 892)).first()
        b_eknr = finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 257)).first()
        fl_eknr = finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 258)).first()
        bl_eknr = finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 272)).first()
        bev_food = fchar

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 275)).first()
        food_bev = fchar

        gl_acct = db_session.query(Gl_acct).filter(
                (func.lower(Gl_acct.fibukonto) == (bev_food).lower())).first()
        s_list = S_list()
        s_list_list.append(s_list)

        s_list.reihenfolge = 1
        s_list.lager_nr = 9999
        s_list.l_bezeich = to_string(gl_acct.fibukonto, coa_format) + " " + gl_acct.bezeich.upper()
        s_list.flag = 0

        gl_acct = db_session.query(Gl_acct).filter(
                (func.lower(Gl_acct.fibukonto) == (food_bev).lower())).first()
        s_list = S_list()
        s_list_list.append(s_list)

        s_list.reihenfolge = 2
        s_list.lager_nr = 9999
        s_list.l_bezeich = to_string(gl_acct.fibukonto, coa_format) + " " + gl_acct.bezeich.upper()
        s_list.flag = 0
        flag = 1

        for l_lager in db_session.query(L_lager).all():

            l_bestand_obj_list = []
            for l_bestand, l_oh, l_artikel in db_session.query(L_bestand, L_oh, L_artikel).join(L_oh,(L_oh.artnr == L_bestand.artnr) &  (L_oh.lager_nr == 0)).join(L_artikel,(L_artikel.artnr == L_bestand.artnr) &  ((L_artikel.endkum == fl_eknr) |  (L_artikel.endkum == bl_eknr))).filter(
                    (L_bestand.lager_nr == l_lager.lager_nr)).all():
                if l_bestand._recid in l_bestand_obj_list:
                    continue
                else:
                    l_bestand_obj_list.append(l_bestand._recid)

                if l_artikel.endkum == fl_eknr:
                    flag = 1

                elif l_artikel.endkum == bl_eknr:
                    flag = 2
                qty1 = l_bestand.anz_anf_best + l_bestand.anz_eingang - l_bestand.anz_ausgang
                qty = l_oh.anz_anf_best + l_oh.anz_eingang - l_oh.anz_ausgang
                wert = l_oh.val_anf_best + l_oh.wert_eingang - l_oh.wert_ausgang

                s_list = query(s_list_list, filters=(lambda s_list :s_list.lager_nr == l_lager.lager_nr and s_list.reihenfolge == flag and s_list.flag == 0), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_list.append(s_list)

                    s_list.reihenfolge = flag
                    s_list.lager_nr = l_lager.lager_nr
                    s_list.l_bezeich = l_lager.bezeich
                    s_list.flag = 0

                if l_bestand.anz_anf_best != 0:
                    s_list.anf_wert = s_list.anf_wert + l_bestand.anz_anf_best * l_bestand.val_anf_best / l_bestand.anz_anf_best

                if qty != 0:
                    s_list.end_wert = s_list.end_wert + wert * qty1 / qty

                for l_op in db_session.query(L_op).filter(
                        (L_op.datum >= from_date) &  (L_op.datum <= to_date) &  (L_op.artnr == l_artikel.artnr) &  (L_op.op_art == 1) &  (L_op.loeschflag <= 1) &  (L_op.lager_nr == l_lager.lager_nr)).all():

                    l_ophdr = db_session.query(L_ophdr).filter(
                            (L_ophdr.lscheinnr == l_op.lscheinnr) &  (func.lower(L_ophdr.op_typ) == "STI")).first()

                    if l_op.anzahl >= 0:

                        s_list = query(s_list_list, filters=(lambda s_list :s_list.lager_nr == l_lager.lager_nr and s_list.reihenfolge == flag and s_list.flag == 11), first=True)

                        if not s_list:
                            s_list = S_list()
                            s_list_list.append(s_list)

                            s_list.reihenfolge = flag
                            s_list.lager_nr = l_lager.lager_nr
                            s_list.l_bezeich = l_lager.bezeich
                            s_list.flag = 11
                        s_list.betrag = s_list.betrag + l_op.warenwert

                    elif l_op.anzahl < 0:

                        s_list = query(s_list_list, filters=(lambda s_list :s_list.lager_nr == l_lager.lager_nr and s_list.reihenfolge == flag and s_list.flag == 12), first=True)

                        if not s_list:
                            s_list = S_list()
                            s_list_list.append(s_list)

                            s_list.reihenfolge = flag
                            s_list.lager_nr = l_lager.lager_nr
                            s_list.l_bezeich = l_lager.bezeich
                            s_list.flag = 12
                        s_list.betrag = s_list.betrag + l_op.warenwert

                l_op_obj_list = []
                for l_op, l_ophdr, gl_acct in db_session.query(L_op, L_ophdr, Gl_acct).join(L_ophdr,(L_ophdr.lscheinnr == L_op.lscheinnr) &  (func.lower(L_ophdr.op_typ) == "STT") &  (L_ophdr.fibukonto != "")).join(Gl_acct,(Gl_acct.fibukonto == l_ophdr.fibukonto)).filter(
                        (L_op.datum >= from_date) &  (L_op.datum <= to_date) &  (L_op.artnr == l_artikel.artnr) &  (L_op.loeschflag <= 1) &  (L_op.op_art == 3) &  (L_op.lager_nr == l_lager.lager_nr)).all():
                    if l_op._recid in l_op_obj_list:
                        continue
                    else:
                        l_op_obj_list.append(l_op._recid)


                    type_of_acct = gl_acct.acc_type

                    gl_main = db_session.query(Gl_main).filter(
                                (Gl_main.nr == gl_acct.main_nr)).first()
                    fibukonto = gl_acct.fibukonto
                    bezeich = to_string(gl_acct.fibukonto, coa_format) + " " + gl_acct.bezeich.upper()

                    if l_op.stornogrund != "":

                        gl_acct1 = db_session.query(Gl_acct1).filter(
                                    (Gl_acct1.fibukonto == l_op.stornogrund)).first()

                        if gl_acct1:
                            type_of_acct = gl_acct1.acc_type
                            fibukonto = gl_acct1.fibukonto
                            bezeich = to_string(gl_acct1.fibukonto, coa_format) + " " + gl_acct1.bezeich.upper()

                            gl_main = db_session.query(Gl_main).filter(
                                        (Gl_main.nr == gl_acct1.main_nr)).first()

                    if flag == 1 and fibukonto.lower()  == (food_bev).lower() :

                        s_list = query(s_list_list, filters=(lambda s_list :s_list.lager_nr == 9999 and s_list.reihenfolge == 2), first=True)
                        s_list.anf_wert = s_list.anf_wert + l_op.warenwert

                    elif flag == 2 and fibukonto.lower()  == (bev_food).lower() :

                        s_list = query(s_list_list, filters=(lambda s_list :s_list.lager_nr == 9999 and s_list.reihenfolge == 1), first=True)
                        s_list.anf_wert = s_list.anf_wert + l_op.warenwert
                    else:

                        if mi_opt == False:

                            s_list = query(s_list_list, filters=(lambda s_list :s_list.(fibukonto).lower().lower()  == (fibukonto).lower()  and s_list.reihenfolge == flag and s_list.flag == 5), first=True)

                            if not s_list:
                                s_list = S_list()
                                s_list_list.append(s_list)

                                s_list.reihenfolge = flag
                                s_list.fibukonto = fibukonto
                                s_list.bezeich = bezeich
                                s_list.flag = 5
                        else:

                            s_list = query(s_list_list, filters=(lambda s_list :s_list.code == gl_main.code and s_list.reihenfolge == flag and s_list.flag == 5), first=True)

                            if not s_list:
                                s_list = S_list()
                                s_list_list.append(s_list)

                                s_list.reihenfolge = flag
                                s_list.code = gl_main.code
                                s_list.bezeich = gl_main.bezeich
                                s_list.flag = 5

                        if type_of_acct == 5 or type_of_acct == 3 or type_of_acct == 4:
                            s_list.betrag = s_list.betrag + l_op.warenwert

        for hoteldpt in db_session.query(Hoteldpt).filter(
                (Hoteldpt.num != ldry) &  (Hoteldpt.num != dstore)).all():

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

                artikel = db_session.query(Artikel).filter(
                        (Artikel.artnr == h_art.artnrfront) &  (Artikel.departement == 0)).first()

                gl_acct = db_session.query(Gl_acct).filter(
                        (Gl_acct.fibukonto == artikel.fibukonto)).first()

                gl_main = db_session.query(Gl_main).filter(
                        (Gl_main.nr == gl_acct.main_nr)).first()

                h_artikel = db_session.query(H_artikel).filter(
                        (H_artikel.departement == h_compli.departement) &  (H_artikel.artnr == h_compli.artnr)).first()

                artikel = db_session.query(Artikel).filter(
                        (Artikel.artnr == h_Artikel.artnrfront) &  (Artikel.departement == h_Artikel.departement)).first()
                f_cost = 0
                b_cost = 0

                h_cost = db_session.query(H_cost).filter(
                        (H_cost.artnr == h_compli.artnr) &  (H_cost.departement == h_compli.departement) &  (H_cost.datum == h_compli.datum) &  (H_cost.flag == 1)).first()

                if h_cost and h_cost.betrag != 0:

                    if artikel.umsatzart == 6:
                        b_cost = h_compli.anzahl * h_cost.betrag

                    elif artikel.umsatzart == 3 or artikel.umsatzart == 5:
                        f_cost = h_compli.anzahl * h_cost.betrag
                    f_cost = cost_correction(f_cost)

                elif not h_cost or (h_cost and h_cost.betrag == 0):

                    if artikel.umsatzart == 6:
                        b_cost = h_compli.anzahl * h_compli.epreis * h_artikel.prozent / 100 * rate

                    elif artikel.umsatzart == 3 or artikel.umsatzart == 5:
                        f_cost = h_compli.anzahl * h_compli.epreis * h_artikel.prozent / 100 * rate

                if f_cost != 0:

                    if mi_opt == False:

                        s_list = query(s_list_list, filters=(lambda s_list :s_list.fibukonto == gl_acct.fibukonto and s_list.reihenfolge == 1 and s_list.flag == 4), first=True)

                        if not s_list:
                            s_list = S_list()
                            s_list_list.append(s_list)

                            s_list.reihenfolge = 1
                            s_list.fibukonto = gl_acct.fibukonto
                            s_list.bezeich = to_string(gl_acct.fibukonto, coa_format) + " " + gl_acct.bezeich.upper()
                            s_list.flag = 4
                    else:

                        s_list = query(s_list_list, filters=(lambda s_list :s_list.code == gl_main.code and s_list.reihenfolge == 1 and s_list.flag == 4), first=True)

                        if not s_list:
                            s_list = S_list()
                            s_list_list.append(s_list)

                            s_list.reihenfolge = 1
                            s_list.code = gl_main.code
                            s_list.bezeich = gl_main.bezeich
                            s_list.flag = 4
                    s_list.betrag = s_list.betrag + f_cost
        tf_sales, tb_sales = fb_sales(f_eknr, b_eknr)
        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_list.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr
        fbreconsile_list.col2 = to_string(translateExtended ("** FOOD **", lvcarea, "") , "x(33)")
        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_list.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr
        i = 0
        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_list.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr
        fbreconsile_list.col1 = to_string(translateExtended ("1. Opening Inventory", lvcarea, "") , "x(24)")

        for s_list in query(s_list_list, filters=(lambda s_list :s_list.flag == 0 and s_list.reihenfolge == 1 and s_list.lager_nr != 9999 and s_list.anf_wert != 0)):
            i = i + 1
            betrag1 = betrag1 + s_list.anf_wert

            if i > 1:
                fbreconsile_list = Fbreconsile_list()
                fbreconsile_list_list.append(fbreconsile_list)

                curr_nr = curr_nr + 1
                fbreconsile_list.nr = curr_nr
                fbreconsile_list.col1 = to_string("", "x(24)")

            if not long_digit:
                fbreconsile_list.col2 = to_string(s_list.l_bezeich, "x(33)")
                fbreconsile_list.col3 = to_string(s_list.anf_wert, "->>>,>>>,>>9.99")


            else:
                fbreconsile_list.col2 = to_string(s_list.l_bezeich, "x(33)")
                fbreconsile_list.col3 = to_string(s_list.anf_wert, "->>,>>>,>>>,>>9")


        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_list.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr

        if not long_digit:
            fbreconsile_list.col2 = to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)")
            fbreconsile_list.col4 = to_string(betrag1, "->>>,>>>,>>9.99")


        else:
            fbreconsile_list.col2 = to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)")
            fbreconsile_list.col4 = to_string(betrag1, "->>,>>>,>>>,>>9")


        i = 0
        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_list.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr
        fbreconsile_list.col1 = to_string(translateExtended ("2. Incoming Stocks", lvcarea, "") , "x(24)")

        for s_list in query(s_list_list, filters=(lambda s_list :s_list.flag == 11 and s_list.reihenfolge == 1)):
            i = i + 1
            betrag2 = betrag2 + s_list.betrag

            if i > 1:
                fbreconsile_list = Fbreconsile_list()
                fbreconsile_list_list.append(fbreconsile_list)

                curr_nr = curr_nr + 1
                fbreconsile_list.nr = curr_nr
                fbreconsile_list.col1 = to_string("", "x(24)")

            if not long_digit:
                fbreconsile_list.col2 = to_string(s_list.l_bezeich, "x(33)")
                fbreconsile_list.col3 = to_string(s_list.betrag, "->>>,>>>,>>9.99")


            else:
                fbreconsile_list.col2 = to_string(s_list.l_bezeich, "x(33)")
                fbreconsile_list.col3 = to_string(s_list.betrag, "->>,>>>,>>>,>>9")


        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_list.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr

        if not long_digit:
            fbreconsile_list.col2 = to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)")
            fbreconsile_list.col4 = to_string(betrag2, "->>>,>>>,>>9.99")


        else:
            fbreconsile_list.col2 = to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)")
            fbreconsile_list.col4 = to_string(betrag2, "->>,>>>,>>>,>>9")


        i = 0
        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_list.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr
        fbreconsile_list.col1 = to_string(translateExtended ("3. Returned Stocks", lvcarea, "") , "x(24)")

        for s_list in query(s_list_list, filters=(lambda s_list :s_list.flag == 12 and s_list.reihenfolge == 1)):
            i = i + 1
            betrag3 = betrag3 + s_list.betrag

            if i > 1:
                fbreconsile_list = Fbreconsile_list()
                fbreconsile_list_list.append(fbreconsile_list)

                curr_nr = curr_nr + 1
                fbreconsile_list.nr = curr_nr
                fbreconsile_list.col1 = to_string("", "x(24)")

            if not long_digit:
                fbreconsile_list.col2 = to_string(s_list.l_bezeich, "x(33)")
                fbreconsile_list.col3 = to_string(s_list.betrag, "->>>,>>>,>>9.99")


            else:
                fbreconsile_list.col2 = to_string(s_list.l_bezeich, "x(33)")
                fbreconsile_list.col3 = to_string(s_list.betrag, "->>,>>>,>>>,>>9")


        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_list.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr

        if not long_digit:
            fbreconsile_list.col2 = to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)")
            fbreconsile_list.col4 = to_string(betrag3, "->>>,>>>,>>9.99")


        else:
            fbreconsile_list.col2 = to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)")
            fbreconsile_list.col4 = to_string(betrag3, "->>,>>>,>>>,>>9")

        s_list = query(s_list_list, filters=(lambda s_list :s_list.lager_nr == 9999 and s_list.reihenfolge == 1), first=True)
        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_list.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr

        if not long_digit:
            fbreconsile_list.col1 = to_string(("4. " + s_list.l_bezeich) , "x(24)")
            fbreconsile_list.col4 = to_string(s_list.anf_wert, "->>>,>>>,>>9.99")


        else:
            fbreconsile_list.col1 = to_string(("4. " + s_list.l_bezeich) , "x(24)")
            fbreconsile_list.col4 = to_string(s_list.anf_wert, "->>,>>>,>>>,>>9")


        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_list.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr
        betrag4 = betrag1 + betrag2 + betrag3 + s_list.anf_wert
        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_list.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr

        if not long_digit:
            fbreconsile_list.col1 = to_string(translateExtended ("5. Inventory Available", lvcarea, "") , "x(24)")
            fbreconsile_list.col2 = to_string("(1 + 2 + 3 + 4)", "x(33)")
            fbreconsile_list.col4 = to_string(betrag4, "->>>,>>>,>>9.99")


        else:
            fbreconsile_list.col1 = to_string(translateExtended ("5. Inventory Available", lvcarea, "") , "x(24)")
            fbreconsile_list.col2 = to_string("(1 + 2 + 3 + 4)", "x(33)")
            fbreconsile_list.col4 = to_string(betrag4, "->>,>>>,>>>,>>9")


        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_list.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr
        i = 0
        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_list.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr
        fbreconsile_list.col1 = to_string(translateExtended ("6. Closing Inventory", lvcarea, "") , "x(24)")

        for s_list in query(s_list_list, filters=(lambda s_list :s_list.flag == 0 and s_list.reihenfolge == 1 and s_list.lager_nr != 9999 and s_list.end_wert != 0)):
            i = i + 1
            betrag5 = betrag5 + s_list.end_wert

            if i > 1:
                fbreconsile_list = Fbreconsile_list()
                fbreconsile_list_list.append(fbreconsile_list)

                curr_nr = curr_nr + 1
                fbreconsile_list.nr = curr_nr
                fbreconsile_list.col1 = to_string("", "x(24)")

            if not long_digit:
                fbreconsile_list.col2 = to_string(s_list.l_bezeich, "x(33)")
                fbreconsile_list.col3 = to_string(s_list.end_wert, "->>>,>>>,>>9.99")


            else:
                fbreconsile_list.col2 = to_string(s_list.l_bezeich, "x(33)")
                fbreconsile_list.col3 = to_string(s_list.end_wert, "->>,>>>,>>>,>>9")


        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_list.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr

        if not long_digit:
            fbreconsile_list.col2 = to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)")
            fbreconsile_list.col4 = to_string(betrag5, "->>>,>>>,>>9.99")


        else:
            fbreconsile_list.col2 = to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)")
            fbreconsile_list.col4 = to_string(betrag5, "->>,>>>,>>>,>>9")


        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_list.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr
        betrag56 = betrag4 - betrag5

        if not long_digit:
            fbreconsile_list.col1 = to_string(translateExtended ("7. Gross Consumption", lvcarea, "") , "x(24)")
            fbreconsile_list.col2 = to_string("(5 - 6)", "x(33)")
            fbreconsile_list.col4 = to_string(betrag56, "->>>,>>>,>>9.99")


        else:
            fbreconsile_list.col1 = to_string(translateExtended ("7. Gross Consumption", lvcarea, "") , "x(24)")
            fbreconsile_list.col2 = to_string("(5 - 6)", "x(33)")
            fbreconsile_list.col4 = to_string(betrag56, "->>,>>>,>>>,>>9")


        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_list.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr
        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_list.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr
        fbreconsile_list.col1 = to_string(translateExtended ("8. Credits", lvcarea, "") , "x(24)")

        if mi_opt == False:
            fbreconsile_list = Fbreconsile_list()
            fbreconsile_list_list.append(fbreconsile_list)

            curr_nr = curr_nr + 1
            fbreconsile_list.nr = curr_nr
            fbreconsile_list.col1 = to_string(translateExtended ("- Compliment cost", lvcarea, "") , "x(24)")
            counter = 0
        else:
            counter = 1

        for s_list in query(s_list_list, filters=(lambda s_list :s_list.flag == 4 and s_list.reihenfolge == 1 and s_list.betrag != 0)):
            betrag6 = betrag6 + s_list.betrag
            counter = counter + 1

            if counter > 1:
                fbreconsile_list = Fbreconsile_list()
                fbreconsile_list_list.append(fbreconsile_list)

                fbreconsile_list.nr = curr_nr

                if s_list.code > 0:
                    fbreconsile_list.code = s_list.code
                else:
                    fbreconsile_list.code = counter
                fbreconsile_list.col1 = to_string("", "x(24)")

            if not long_digit:
                fbreconsile_list.col2 = to_string(s_list.bezeich, "x(33)")
                fbreconsile_list.col3 = to_string(s_list.betrag, "->>>,>>>,>>9.99")


            else:
                fbreconsile_list.col2 = to_string(s_list.bezeich, "x(33)")
                fbreconsile_list.col3 = to_string(s_list.betrag, "->>,>>>,>>>,>>9")

        if mi_opt == False:
            fbreconsile_list = Fbreconsile_list()
            fbreconsile_list_list.append(fbreconsile_list)

            curr_nr = curr_nr + 1
            fbreconsile_list.nr = curr_nr
            fbreconsile_list = Fbreconsile_list()
            fbreconsile_list_list.append(fbreconsile_list)

            curr_nr = curr_nr + 1
            fbreconsile_list.nr = curr_nr
            fbreconsile_list.col1 = to_string(translateExtended ("- Department Expenses", lvcarea, "") , "x(24)")
            counter = 0
        else:
            counter = 1

        for s_list in query(s_list_list, filters=(lambda s_list :s_list.flag == 5 and s_list.reihenfolge == 1 and s_list.betrag != 0)):
            betrag6 = betrag6 + s_list.betrag
            counter = counter + 1

            if counter > 1:
                fbreconsile_list = Fbreconsile_list()
                fbreconsile_list_list.append(fbreconsile_list)

                fbreconsile_list.nr = curr_nr

                if s_list.code > 0:
                    fbreconsile_list.code = s_list.code
                else:
                    fbreconsile_list.code = counter
                fbreconsile_list.col1 = to_string("", "x(24)")

            if not long_digit:
                fbreconsile_list.col2 = to_string(s_list.bezeich, "x(33)")
                fbreconsile_list.col3 = to_string(s_list.betrag, "->>>,>>>,>>9.99")


            else:
                fbreconsile_list.col2 = to_string(s_list.bezeich, "x(33)")
                fbreconsile_list.col3 = to_string(s_list.betrag, "->>,>>>,>>>,>>9")

        s_list = query(s_list_list, filters=(lambda s_list :s_list.reihenfolge == 2 and s_list.lager_nr == 9999), first=True)
        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_list.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr
        fbreconsile_list.col1 = to_string("", "x(24)")

        if not long_digit:
            fbreconsile_list.col2 = to_string(s_list.l_bezeich, "x(33)")
            fbreconsile_list.col3 = to_string(s_list.anf_wert, "->>>,>>>,>>9.99")


        else:
            fbreconsile_list.col2 = to_string(s_list.l_bezeich, "x(33)")
            fbreconsile_list.col3 = to_string(s_list.anf_wert, "->>,>>>,>>>,>>9")


        betrag6 = betrag6 + s_list.anf_wert

        if mi_opt == False:
            fbreconsile_list = Fbreconsile_list()
            fbreconsile_list_list.append(fbreconsile_list)

            curr_nr = curr_nr + 1
            fbreconsile_list.nr = curr_nr
        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_list.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr

        if not long_digit:
            fbreconsile_list.col2 = to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)")
            fbreconsile_list.col4 = to_string(betrag6, "->>>,>>>,>>9.99")


        else:
            fbreconsile_list.col2 = to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)")
            fbreconsile_list.col4 = to_string(betrag6, "->>,>>>,>>>,>>9")


        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_list.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr
        consume2 = betrag56 - betrag6
        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_list.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr

        if not long_digit:
            fbreconsile_list.col1 = to_string(translateExtended ("9. Net Consumption", lvcarea, "") , "x(24)")
            fbreconsile_list.col2 = to_string("(7 - 8)", "x(33)")
            fbreconsile_list.col4 = to_string(consume2, "->>>,>>>,>>9.99")


        else:
            fbreconsile_list.col1 = to_string(translateExtended ("9. Net Consumption", lvcarea, "") , "x(24)")
            fbreconsile_list.col2 = to_string("(7 - 8)", "x(33)")
            fbreconsile_list.col4 = to_string(consume2, "->>,>>>,>>>,>>9")


        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_list.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr
        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_list.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr
        f_ratio = 0

        if tf_sales != 0:
            f_ratio = round(consume2, 2) / round(tf_sales, 2) * 100

        if f_ratio == None:
            f_ratio = 0

        if not long_digit:
            fbreconsile_list.col1 = to_string(translateExtended ("Net Food Sales", lvcarea, "") , "x(24)")
            fbreconsile_list.col2 = to_string("", "x(16)") + to_string(tf_sales, "->,>>>,>>>,>>9.99")
            fbreconsile_list.col3 = to_string(translateExtended ("     cost:Sales", lvcarea, "") , "x(15)")
            fbreconsile_list.col4 = to_string(f_ratio, "->,>>>,>>9.99 %")


        else:
            fbreconsile_list.col1 = to_string(translateExtended ("Net Food Sales", lvcarea, "") , "x(24)")
            fbreconsile_list.col2 = to_string("", "x(16)") + to_string(tf_sales, " ->>>,>>>,>>>,>>9")
            fbreconsile_list.col3 = to_string(translateExtended ("     cost:Sales", lvcarea, "") , "x(15)")
            fbreconsile_list.col4 = to_string(f_ratio, "->,>>>,>>9.99 %")


        done = True

    def create_beverage():

        nonlocal done, fbreconsile_list_list, curr_nr, curr_reihe, ldry, dstore, long_digit, foreign_nr, exchg_rate, double_currency, type_of_acct, counter, coa_format, f_date, lvcarea, htparam, waehrung, h_artikel, l_bestand, l_besthis, gl_acct, l_lager, l_artikel, l_op, l_ophdr, hoteldpt, h_compli, exrate, artikel, gl_main, h_cost, umsatz, h_bill_line
        nonlocal h_art, l_oh, l_ohist, gl_acct1


        nonlocal fbreconsile_list, s_list, h_art, l_oh, l_ohist, gl_acct1
        nonlocal fbreconsile_list_list, s_list_list

        betrag1:decimal = 0
        betrag2:decimal = 0
        betrag3:decimal = 0
        betrag4:decimal = 0
        betrag5:decimal = 0
        betrag6:decimal = 0
        betrag61:decimal = 0
        betrag62:decimal = 0
        betrag56:decimal = 0
        consume2:decimal = 0
        flag:int = 0
        f_eknr:int = 0
        b_eknr:int = 0
        fl_eknr:int = 0
        bl_eknr:int = 0
        f_cost:decimal = 0
        b_cost:decimal = 0
        f_sales:decimal = 0
        b_sales:decimal = 0
        tf_sales:decimal = 0
        tb_sales:decimal = 0
        f_ratio:decimal = 0
        b_ratio:decimal = 0
        fibu:str = ""
        h_service:decimal = 0
        h_mwst:decimal = 0
        amount:decimal = 0
        i:int = 0
        bev_food:str = ""
        food_bev:str = ""
        fb_str:[str] = ["", "", ""]
        curr_datum:date = None
        rate:decimal = 1
        qty1:decimal = 0
        qty:decimal = 0
        wert:decimal = 0
        fibukonto:str = ""
        bezeich:str = ""
        fb_str[0] = translateExtended ("Beverage to Food", lvcarea, "")
        fb_str[1] = translateExtended ("Food to Beverage", lvcarea, "")
        H_art = H_artikel
        L_oh = L_bestand
        Gl_acct1 = Gl_acct
        s_list_list.clear()
        fbreconsile_list_list.clear()
        curr_nr = 0
        curr_reihe = 0

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 862)).first()
        f_eknr = finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 892)).first()
        b_eknr = finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 257)).first()
        fl_eknr = finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 258)).first()
        bl_eknr = finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 272)).first()
        bev_food = fchar

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 275)).first()
        food_bev = fchar

        gl_acct = db_session.query(Gl_acct).filter(
                (func.lower(Gl_acct.fibukonto) == (bev_food).lower())).first()
        s_list = S_list()
        s_list_list.append(s_list)

        s_list.reihenfolge = 1
        s_list.lager_nr = 9999
        s_list.l_bezeich = to_string(gl_acct.fibukonto, coa_format) + " " + gl_acct.bezeich.upper()
        s_list.flag = 0

        gl_acct = db_session.query(Gl_acct).filter(
                (func.lower(Gl_acct.fibukonto) == (food_bev).lower())).first()
        s_list = S_list()
        s_list_list.append(s_list)

        s_list.reihenfolge = 2
        s_list.lager_nr = 9999
        s_list.l_bezeich = to_string(gl_acct.fibukonto, coa_format) + " " + gl_acct.bezeich.upper()
        s_list.flag = 0
        flag = 2

        for l_lager in db_session.query(L_lager).all():

            l_bestand_obj_list = []
            for l_bestand, l_oh, l_artikel in db_session.query(L_bestand, L_oh, L_artikel).join(L_oh,(L_oh.artnr == L_bestand.artnr) &  (L_oh.lager_nr == 0)).join(L_artikel,(L_artikel.artnr == L_bestand.artnr) &  ((L_artikel.endkum == fl_eknr) |  (L_artikel.endkum == bl_eknr))).filter(
                    (L_bestand.lager_nr == l_lager.lager_nr)).all():
                if l_bestand._recid in l_bestand_obj_list:
                    continue
                else:
                    l_bestand_obj_list.append(l_bestand._recid)

                if l_artikel.endkum == fl_eknr:
                    flag = 1

                elif l_artikel.endkum == bl_eknr:
                    flag = 2
                qty1 = l_bestand.anz_anf_best + l_bestand.anz_eingang - l_bestand.anz_ausgang
                qty = l_oh.anz_anf_best + l_oh.anz_eingang - l_oh.anz_ausgang
                wert = l_oh.val_anf_best + l_oh.wert_eingang - l_oh.wert_ausgang

                s_list = query(s_list_list, filters=(lambda s_list :s_list.lager_nr == l_lager.lager_nr and s_list.reihenfolge == flag and s_list.flag == 0), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_list.append(s_list)

                    s_list.reihenfolge = flag
                    s_list.lager_nr = l_lager.lager_nr
                    s_list.l_bezeich = l_lager.bezeich
                    s_list.flag = 0

                if l_bestand.anz_anf_best != 0:
                    s_list.anf_wert = s_list.anf_wert + l_bestand.anz_anf_best * l_bestand.val_anf_best / l_bestand.anz_anf_best

                if qty != 0:
                    s_list.end_wert = s_list.end_wert + wert * qty1 / qty

                for l_op in db_session.query(L_op).filter(
                        (L_op.datum >= from_date) &  (L_op.datum <= to_date) &  (L_op.artnr == l_artikel.artnr) &  (L_op.op_art == 1) &  (L_op.loeschflag <= 1) &  (L_op.lager_nr == l_lager.lager_nr)).all():

                    l_ophdr = db_session.query(L_ophdr).filter(
                            (L_ophdr.lscheinnr == l_op.lscheinnr) &  (func.lower(L_ophdr.op_typ) == "STI")).first()

                    if l_op.anzahl >= 0:

                        s_list = query(s_list_list, filters=(lambda s_list :s_list.lager_nr == l_lager.lager_nr and s_list.reihenfolge == flag and s_list.flag == 11), first=True)

                        if not s_list:
                            s_list = S_list()
                            s_list_list.append(s_list)

                            s_list.reihenfolge = flag
                            s_list.lager_nr = l_lager.lager_nr
                            s_list.l_bezeich = l_lager.bezeich
                            s_list.flag = 11
                        s_list.betrag = s_list.betrag + l_op.warenwert

                    elif l_op.anzahl < 0:

                        s_list = query(s_list_list, filters=(lambda s_list :s_list.lager_nr == l_lager.lager_nr and s_list.reihenfolge == flag and s_list.flag == 12), first=True)

                        if not s_list:
                            s_list = S_list()
                            s_list_list.append(s_list)

                            s_list.reihenfolge = flag
                            s_list.lager_nr = l_lager.lager_nr
                            s_list.l_bezeich = l_lager.bezeich
                            s_list.flag = 12
                        s_list.betrag = s_list.betrag + l_op.warenwert

                l_op_obj_list = []
                for l_op, l_ophdr, gl_acct in db_session.query(L_op, L_ophdr, Gl_acct).join(L_ophdr,(L_ophdr.lscheinnr == L_op.lscheinnr) &  (func.lower(L_ophdr.op_typ) == "STT") &  (L_ophdr.fibukonto != "")).join(Gl_acct,(Gl_acct.fibukonto == l_ophdr.fibukonto)).filter(
                        (L_op.datum >= from_date) &  (L_op.datum <= to_date) &  (L_op.artnr == l_artikel.artnr) &  (L_op.loeschflag <= 1) &  (L_op.op_art == 3) &  (L_op.lager_nr == l_lager.lager_nr)).all():
                    if l_op._recid in l_op_obj_list:
                        continue
                    else:
                        l_op_obj_list.append(l_op._recid)


                    type_of_acct = gl_acct.acc_type

                    gl_main = db_session.query(Gl_main).filter(
                                (Gl_main.nr == gl_acct.main_nr)).first()
                    fibukonto = gl_acct.fibukonto
                    bezeich = to_string(gl_acct.fibukonto, coa_format) + " " + gl_acct.bezeich.upper()

                    if l_op.stornogrund != "":

                        gl_acct1 = db_session.query(Gl_acct1).filter(
                                    (Gl_acct1.fibukonto == l_op.stornogrund)).first()

                        if gl_acct1:
                            type_of_acct = gl_acct1.acc_type

                            gl_main = db_session.query(Gl_main).filter(
                                        (Gl_main.nr == gl_acct1.main_nr)).first()
                            fibukonto = gl_acct1.fibukonto
                            bezeich = to_string(gl_acct1.fibukonto, coa_format) + " " + gl_acct1.bezeich.upper()

                    if flag == 1 and fibukonto.lower()  == (food_bev).lower() :

                        s_list = query(s_list_list, filters=(lambda s_list :s_list.lager_nr == 9999 and s_list.reihenfolge == 2), first=True)
                        s_list.anf_wert = s_list.anf_wert + l_op.warenwert

                    elif flag == 2 and fibukonto.lower()  == (bev_food).lower() :

                        s_list = query(s_list_list, filters=(lambda s_list :s_list.lager_nr == 9999 and s_list.reihenfolge == 1), first=True)
                        s_list.anf_wert = s_list.anf_wert + l_op.warenwert
                    else:

                        if mi_opt == False:

                            s_list = query(s_list_list, filters=(lambda s_list :s_list.(fibukonto).lower().lower()  == (fibukonto).lower()  and s_list.reihenfolge == flag and s_list.flag == 5), first=True)

                            if not s_list:
                                s_list = S_list()
                                s_list_list.append(s_list)

                                s_list.reihenfolge = flag
                                s_list.fibukonto = fibukonto
                                s_list.bezeich = bezeich
                                s_list.flag = 5
                        else:

                            s_list = query(s_list_list, filters=(lambda s_list :s_list.code == gl_main.code and s_list.reihenfolge == flag and s_list.flag == 5), first=True)

                            if not s_list:
                                s_list = S_list()
                                s_list_list.append(s_list)

                                s_list.reihenfolge = flag
                                s_list.code = gl_main.code
                                s_list.bezeich = gl_main.bezeich
                                s_list.flag = 5

                        if type_of_acct == 5 or type_of_acct == 3 or type_of_acct == 4:
                            s_list.betrag = s_list.betrag + l_op.warenwert

        for hoteldpt in db_session.query(Hoteldpt).filter(
                (Hoteldpt.num != ldry) &  (Hoteldpt.num != dstore)).all():

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

                artikel = db_session.query(Artikel).filter(
                        (Artikel.artnr == h_art.artnrfront) &  (Artikel.departement == 0)).first()

                gl_acct = db_session.query(Gl_acct).filter(
                        (Gl_acct.fibukonto == artikel.fibukonto)).first()

                gl_main = db_session.query(Gl_main).filter(
                        (Gl_main.nr == gl_acct.main_nr)).first()

                h_artikel = db_session.query(H_artikel).filter(
                        (H_artikel.departement == h_compli.departement) &  (H_artikel.artnr == h_compli.artnr)).first()

                artikel = db_session.query(Artikel).filter(
                        (Artikel.artnr == h_Artikel.artnrfront) &  (Artikel.departement == h_Artikel.departement)).first()
                f_cost = 0
                b_cost = 0

                h_cost = db_session.query(H_cost).filter(
                        (H_cost.artnr == h_compli.artnr) &  (H_cost.departement == h_compli.departement) &  (H_cost.datum == h_compli.datum) &  (H_cost.flag == 1)).first()

                if h_cost and h_cost.betrag != 0:

                    if artikel.umsatzart == 6:
                        b_cost = h_compli.anzahl * h_cost.betrag

                    elif artikel.umsatzart == 3 or artikel.umsatzart == 5:
                        f_cost = h_compli.anzahl * h_cost.betrag
                    f_cost = cost_correction(f_cost)

                elif not h_cost or (h_cost and h_cost.betrag == 0):

                    if artikel.umsatzart == 6:
                        b_cost = h_compli.anzahl * h_compli.epreis * h_artikel.prozent / 100 * rate

                    elif artikel.umsatzart == 3 or artikel.umsatzart == 5:
                        f_cost = h_compli.anzahl * h_compli.epreis * h_artikel.prozent / 100 * rate

                if b_cost != 0:

                    if mi_opt == False:

                        s_list = query(s_list_list, filters=(lambda s_list :s_list.fibukonto == gl_acct.fibukonto and s_list.reihenfolge == 2 and s_list.flag == 4), first=True)

                        if not s_list:
                            s_list = S_list()
                            s_list_list.append(s_list)

                            s_list.reihenfolge = 2
                            s_list.fibukonto = gl_acct.fibukonto
                            s_list.bezeich = to_string(gl_acct.fibukonto, coa_format) + " " + gl_acct.bezeich.upper()
                            s_list.flag = 4
                    else:

                        s_list = query(s_list_list, filters=(lambda s_list :s_list.code == gl_main.code and s_list.reihenfolge == 2 and s_list.flag == 4), first=True)

                        if not s_list:
                            s_list = S_list()
                            s_list_list.append(s_list)

                            s_list.reihenfolge = 2
                            s_list.code = gl_main.code
                            s_list.bezeich = gl_main.bezeich
                            s_list.flag = 4
                    s_list.betrag = s_list.betrag + b_cost
        tf_sales, tb_sales = fb_sales(f_eknr, b_eknr)
        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_list.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr
        fbreconsile_list.col2 = to_string(translateExtended ("** BEVERAGE **", lvcarea, "") , "x(33)")
        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_list.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr
        i = 0
        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_list.append(fbreconsile_list)

        betrag1 = 0
        fbreconsile_list.col1 = to_string(translateExtended ("1. Opening Inventory", lvcarea, "") , "x(24)")

        for s_list in query(s_list_list, filters=(lambda s_list :s_list.flag == 0 and s_list.reihenfolge == 2 and s_list.lager_nr != 9999 and s_list.anf_wert != 0)):
            i = i + 1
            betrag1 = betrag1 + s_list.anf_wert

            if i > 1:
                fbreconsile_list = Fbreconsile_list()
                fbreconsile_list_list.append(fbreconsile_list)

                curr_nr = curr_nr + 1
                fbreconsile_list.nr = curr_nr
                fbreconsile_list.col1 = to_string("", "x(24)")

            if not long_digit:
                fbreconsile_list.col2 = to_string(s_list.l_bezeich, "x(33)")
                fbreconsile_list.col3 = to_string(s_list.anf_wert, "->>>,>>>,>>9.99")


            else:
                fbreconsile_list.col2 = to_string(s_list.l_bezeich, "x(33)")
                fbreconsile_list.col3 = to_string(s_list.anf_wert, "->>,>>>,>>>,>>9")


        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_list.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr

        if not long_digit:
            fbreconsile_list.col2 = to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)")
            fbreconsile_list.col4 = to_string(betrag1, "->>>,>>>,>>9.99")


        else:
            fbreconsile_list.col2 = to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)")
            fbreconsile_list.col4 = to_string(betrag1, "->>,>>>,>>>,>>9")


        i = 0
        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_list.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr
        fbreconsile_list.col1 = to_string(translateExtended ("2. Incoming Stocks", lvcarea, "") , "x(24)")
        betrag2 = 0

        for s_list in query(s_list_list, filters=(lambda s_list :s_list.flag == 11 and s_list.reihenfolge == 2)):
            i = i + 1
            betrag2 = betrag2 + s_list.betrag

            if i > 1:
                fbreconsile_list = Fbreconsile_list()
                fbreconsile_list_list.append(fbreconsile_list)

                curr_nr = curr_nr + 1
                fbreconsile_list.nr = curr_nr
                fbreconsile_list.col1 = to_string("", "x(24)")

            if not long_digit:
                fbreconsile_list.col2 = to_string(s_list.l_bezeich, "x(33)")
                fbreconsile_list.col3 = to_string(s_list.betrag, "->>>,>>>,>>9.99")


            else:
                fbreconsile_list.col2 = to_string(s_list.l_bezeich, "x(33)")
                fbreconsile_list.col3 = to_string(s_list.betrag, "->>,>>>,>>>,>>9")


        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_list.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr

        if not long_digit:
            fbreconsile_list.col2 = to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)")
            fbreconsile_list.col4 = to_string(betrag2, "->>>,>>>,>>9.99")


        else:
            fbreconsile_list.col2 = to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)")
            fbreconsile_list.col4 = to_string(betrag2, "->>,>>>,>>>,>>9")


        i = 0
        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_list.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr
        fbreconsile_list.col1 = to_string(translateExtended ("3. Returned Stocks", lvcarea, "") , "x(24)")
        betrag3 = 0

        for s_list in query(s_list_list, filters=(lambda s_list :s_list.flag == 12 and s_list.reihenfolge == 2)):
            i = i + 1
            betrag3 = betrag3 + s_list.betrag

            if i > 1:
                fbreconsile_list = Fbreconsile_list()
                fbreconsile_list_list.append(fbreconsile_list)

                curr_nr = curr_nr + 1
                fbreconsile_list.nr = curr_nr
                fbreconsile_list.col1 = to_string("", "x(24)")

            if not long_digit:
                fbreconsile_list.col2 = to_string(s_list.l_bezeich, "x(33)")
                fbreconsile_list.col3 = to_string(s_list.betrag, "->>>,>>>,>>9.99")


            else:
                fbreconsile_list.col2 = to_string(s_list.l_bezeich, "x(33)")
                fbreconsile_list.col3 = to_string(s_list.betrag, "->>,>>>,>>>,>>9")


        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_list.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr

        if not long_digit:
            fbreconsile_list.col2 = to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)")
            fbreconsile_list.col4 = to_string(betrag3, "->>>,>>>,>>9.99")


        else:
            fbreconsile_list.col2 = to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)")
            fbreconsile_list.col4 = to_string(betrag3, "->>,>>>,>>>,>>9")

        s_list = query(s_list_list, filters=(lambda s_list :s_list.lager_nr == 9999 and s_list.reihenfolge == 2), first=True)
        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_list.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr

        if not long_digit:
            fbreconsile_list.col1 = to_string(("4. " + s_list.l_bezeich) , "x(24)")
            fbreconsile_list.col4 = to_string(s_list.anf_wert, "->>>,>>>,>>9.99")


        else:
            fbreconsile_list.col1 = to_string(("4. " + s_list.l_bezeich) , "x(24)")
            fbreconsile_list.col4 = to_string(s_list.anf_wert, "->>,>>>,>>>,>>9")


        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_list.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr
        betrag4 = betrag1 + betrag2 + betrag3 + s_list.anf_wert
        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_list.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr

        if not long_digit:
            fbreconsile_list.col1 = to_string(translateExtended ("5. Inventory Available", lvcarea, "") , "x(24)")
            fbreconsile_list.col2 = to_string("(1 + 2 + 3 + 4)", "x(33)")
            fbreconsile_list.col4 = to_string(betrag4, "->>>,>>>,>>9.99")


        else:
            fbreconsile_list.col1 = to_string(translateExtended ("5. Inventory Available", lvcarea, "") , "x(24)")
            fbreconsile_list.col2 = to_string("(1 + 2 + 3 + 4)", "x(33)")
            fbreconsile_list.col4 = to_string(betrag4, "->>,>>>,>>>,>>9")


        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_list.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr
        i = 0
        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_list.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr
        fbreconsile_list.col1 = to_string(translateExtended ("6. Closing Inventory", lvcarea, "") , "x(24)")
        betrag5 = 0

        for s_list in query(s_list_list, filters=(lambda s_list :s_list.flag == 0 and s_list.reihenfolge == 2 and s_list.lager_nr != 9999 and s_list.end_wert != 0)):
            i = i + 1
            betrag5 = betrag5 + s_list.end_wert

            if i > 1:
                fbreconsile_list = Fbreconsile_list()
                fbreconsile_list_list.append(fbreconsile_list)

                curr_nr = curr_nr + 1
                fbreconsile_list.nr = curr_nr
                fbreconsile_list.col1 = to_string("", "x(24)")

            if not long_digit:
                fbreconsile_list.col2 = to_string(s_list.l_bezeich, "x(33)")
                fbreconsile_list.col3 = to_string(s_list.end_wert, "->>>,>>>,>>9.99")


            else:
                fbreconsile_list.col2 = to_string(s_list.l_bezeich, "x(33)")
                fbreconsile_list.col3 = to_string(s_list.end_wert, "->>,>>>,>>>,>>9")


        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_list.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr

        if not long_digit:
            fbreconsile_list.col2 = to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)")
            fbreconsile_list.col4 = to_string(betrag5, "->>>,>>>,>>9.99")


        else:
            fbreconsile_list.col2 = to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)")
            fbreconsile_list.col4 = to_string(betrag5, "->>,>>>,>>>,>>9")


        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_list.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr
        betrag56 = betrag4 - betrag5

        if not long_digit:
            fbreconsile_list.col1 = to_string(translateExtended ("7. Gross Consumption", lvcarea, "") , "x(24)")
            fbreconsile_list.col2 = to_string("(5 - 6)", "x(33)")
            fbreconsile_list.col4 = to_string(betrag56, "->>>,>>>,>>9.99")


        else:
            fbreconsile_list.col1 = to_string(translateExtended ("7. Gross Consumption", lvcarea, "") , "x(24)")
            fbreconsile_list.col2 = to_string("(5 - 6)", "x(33)")
            fbreconsile_list.col4 = to_string(betrag56, "->>,>>>,>>>,>>9")


        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_list.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr
        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_list.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr
        fbreconsile_list.col1 = to_string(translateExtended ("8. Credits", lvcarea, "") , "x(24)")
        betrag6 = 0

        if mi_opt == False:
            fbreconsile_list = Fbreconsile_list()
            fbreconsile_list_list.append(fbreconsile_list)

            curr_nr = curr_nr + 1
            fbreconsile_list.nr = curr_nr
            fbreconsile_list.col1 = to_string(translateExtended ("- Compliment cost", lvcarea, "") , "x(24)")
            counter = 0
        else:
            counter = 1

        for s_list in query(s_list_list, filters=(lambda s_list :s_list.flag == 4 and s_list.reihenfolge == 2 and s_list.betrag != 0)):
            betrag6 = betrag6 + s_list.betrag
            counter = counter + 1

            if counter > 1:
                fbreconsile_list = Fbreconsile_list()
                fbreconsile_list_list.append(fbreconsile_list)

                fbreconsile_list.nr = curr_nr

                if s_list.code > 0:
                    fbreconsile_list.code = s_list.code
                else:
                    fbreconsile_list.code = counter
                fbreconsile_list.col1 = to_string("", "x(24)")

            if not long_digit:
                fbreconsile_list.col2 = to_string(s_list.bezeich, "x(33)")
                fbreconsile_list.col3 = to_string(s_list.betrag, "->>>,>>>,>>9.99")


            else:
                fbreconsile_list.col2 = to_string(s_list.bezeich, "x(33)")
                fbreconsile_list.col3 = to_string(s_list.betrag, "->>,>>>,>>>,>>9")

        if mi_opt == False:
            fbreconsile_list = Fbreconsile_list()
            fbreconsile_list_list.append(fbreconsile_list)

            curr_nr = curr_nr + 1
            fbreconsile_list.nr = curr_nr
            fbreconsile_list.col1 = to_string(translateExtended ("- Department Expenses", lvcarea, "") , "x(24)")
            counter = 0
        else:
            counter = 1

        for s_list in query(s_list_list, filters=(lambda s_list :s_list.flag == 5 and s_list.reihenfolge == 2 and s_list.betrag != 0)):
            counter = counter + 1
            betrag6 = betrag6 + s_list.betrag

            if counter > 1:
                fbreconsile_list = Fbreconsile_list()
                fbreconsile_list_list.append(fbreconsile_list)

                fbreconsile_list.nr = curr_nr

                if s_list.code > 0:
                    fbreconsile_list.code = s_list.code
                else:
                    fbreconsile_list.code = counter
                fbreconsile_list.col1 = to_string("", "x(24)")

            if not long_digit:
                fbreconsile_list.col2 = to_string(s_list.bezeich, "x(33)")
                fbreconsile_list.col3 = to_string(s_list.betrag, "->>>,>>>,>>9.99")


            else:
                fbreconsile_list.col2 = to_string(s_list.bezeich, "x(33)")
                fbreconsile_list.col3 = to_string(s_list.betrag, "->>,>>>,>>>,>>9")

        s_list = query(s_list_list, filters=(lambda s_list :s_list.reihenfolge == 1 and s_list.lager_nr == 9999), first=True)
        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_list.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr
        fbreconsile_list.col1 = to_string("", "x(24)")

        if not long_digit:
            fbreconsile_list.col2 = to_string(s_list.l_bezeich, "x(33)")
            fbreconsile_list.col3 = to_string(s_list.anf_wert, "->>>,>>>,>>9.99")


        else:
            fbreconsile_list.col2 = to_string(s_list.l_bezeich, "x(33)")
            fbreconsile_list.col3 = to_string(s_list.anf_wert, "->>,>>>,>>>,>>9")


        betrag6 = betrag6 + s_list.anf_wert

        if mi_opt == False:
            fbreconsile_list = Fbreconsile_list()
            fbreconsile_list_list.append(fbreconsile_list)

            curr_nr = curr_nr + 1
            fbreconsile_list.nr = curr_nr
        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_list.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr

        if not long_digit:
            fbreconsile_list.col2 = to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)")
            fbreconsile_list.col4 = to_string(betrag6, "->>>,>>>,>>9.99")


        else:
            fbreconsile_list.col2 = to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)")
            fbreconsile_list.col4 = to_string(betrag6, "->>,>>>,>>>,>>9")


        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_list.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr
        consume2 = betrag56 - betrag6
        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_list.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr

        if not long_digit:
            fbreconsile_list.col1 = to_string(translateExtended ("9. Net Consumption", lvcarea, "") , "x(24)")
            fbreconsile_list.col2 = to_string("(7 - 8)", "x(33)")
            fbreconsile_list.col4 = to_string(consume2, "->>>,>>>,>>9.99")


        else:
            fbreconsile_list.col1 = to_string(translateExtended ("9. Net Consumption", lvcarea, "") , "x(24)")
            fbreconsile_list.col2 = to_string("(7 - 8)", "x(33)")
            fbreconsile_list.col4 = to_string(consume2, "->>,>>>,>>>,>>9")


        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_list.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr
        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_list.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr
        b_ratio = 0

        if tb_sales != 0:
            b_ratio = consume2 / tb_sales * 100

        if not long_digit:
            fbreconsile_list.col1 = to_string(translateExtended ("Net Beverage Sales", lvcarea, "") , "x(24)")
            fbreconsile_list.col2 = to_string("", "x(16)") + to_string(tb_sales, "->,>>>,>>>,>>9.99")
            fbreconsile_list.col3 = to_string("     cost:Sales", "x(15)")
            fbreconsile_list.col4 = to_string(b_ratio, "->,>>>,>>9.99 %")


        else:
            fbreconsile_list.col1 = to_string(translateExtended ("Net Beverage Sales", lvcarea, "") , "x(24)")
            fbreconsile_list.col2 = to_string("", "x(16)") + to_string(tb_sales, " ->>>,>>>,>>>,>>9")
            fbreconsile_list.col3 = to_string("     cost:Sales", "x(15)")
            fbreconsile_list.col4 = to_string(b_ratio, "->,>>>,>>9.99 %")


        done = True

    def fb_sales(f_eknr:int, b_eknr:int):

        nonlocal done, fbreconsile_list_list, curr_nr, curr_reihe, ldry, dstore, long_digit, foreign_nr, exchg_rate, double_currency, type_of_acct, counter, coa_format, f_date, lvcarea, htparam, waehrung, h_artikel, l_bestand, l_besthis, gl_acct, l_lager, l_artikel, l_op, l_ophdr, hoteldpt, h_compli, exrate, artikel, gl_main, h_cost, umsatz, h_bill_line
        nonlocal h_art, l_oh, l_ohist, gl_acct1


        nonlocal fbreconsile_list, s_list, h_art, l_oh, l_ohist, gl_acct1
        nonlocal fbreconsile_list_list, s_list_list

        tf_sales = 0
        tb_sales = 0
        f_sales:decimal = 0
        b_sales:decimal = 0
        h_service:decimal = 0
        h_mwst:decimal = 0
        vat2:decimal = 0
        fact:decimal = 0
        amount:decimal = 0
        serv_taxable:bool = False

        def generate_inner_output():
            return tf_sales, tb_sales
        f_sales = 0
        b_sales = 0
        tf_sales = 0
        tb_sales = 0

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 479)).first()
        serv_taxable = htparam.flogical

        for hoteldpt in db_session.query(Hoteldpt).filter(
                (Hoteldpt.num != ldry) &  (Hoteldpt.num != dstore)).all():

            for artikel in db_session.query(Artikel).filter(
                    (Artikel.artart == 0) &  (Artikel.departement == hoteldpt.num) &  ((Artikel.endkum == f_eknr) |  (Artikel.endkum == b_eknr) |  (Artikel.umsatzart == 3) |  (Artikel.umsatzart == 5) |  (Artikel.umsatzart == 6))).all():

                for umsatz in db_session.query(Umsatz).filter(
                        (Umsatz.datum >= date1) &  (Umsatz.datum <= date2) &  (Umsatz.departement == artikel.departement) &  (Umsatz.artnr == artikel.artnr)).all():
                    h_service, h_mwst, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, umsatz.datum))
                    h_mwst = h_mwst + vat2


                    amount = umsatz.betrag / fact

                    if artikel.endkum == f_eknr or artikel.umsatzart == 3 or artikel.umsatzart == 5:

                        if umsatz.datum == date2:
                            f_sales = f_sales + amount
                        tf_sales = tf_sales + amount

                    elif artikel.endkum == b_eknr or artikel.umsatzart == 6:

                        if umsatz.datum == date2:
                            b_sales = b_sales + amount
                        tb_sales = tb_sales + amount


        return generate_inner_output()

    def cost_correction(cost:decimal):

        nonlocal done, fbreconsile_list_list, curr_nr, curr_reihe, ldry, dstore, long_digit, foreign_nr, exchg_rate, double_currency, type_of_acct, counter, coa_format, f_date, lvcarea, htparam, waehrung, h_artikel, l_bestand, l_besthis, gl_acct, l_lager, l_artikel, l_op, l_ophdr, hoteldpt, h_compli, exrate, artikel, gl_main, h_cost, umsatz, h_bill_line
        nonlocal h_art, l_oh, l_ohist, gl_acct1


        nonlocal fbreconsile_list, s_list, h_art, l_oh, l_ohist, gl_acct1
        nonlocal fbreconsile_list_list, s_list_list

        h_bill_line = db_session.query(H_bill_line).filter(
                (H_bill_line.rechnr == h_compli.rechnr) &  (H_bill_line.bill_datum == h_compli.datum) &  (H_bill_line.departement == h_compli.departement) &  (H_bill_line.artnr == h_compli.artnr) &  (H_bill_line.epreis == h_compli.epreis)).first()

        if h_bill_line and substring(h_bill_line.bezeich, len(h_bill_line.bezeich) - 1, 1) == "*" and h_bill_line.epreis != 0:

            h_artikel = db_session.query(H_artikel).filter(
                    (H_artikel.artnr == h_bill_line.artnr) &  (H_artikel.departement == h_bill_line.departement)).first()

            if h_artikel and h_artikel.artart == 0 and h_artikel.epreis1 > h_bill_line.epreis:
                cost = cost * h_bill_line.epreis / h_artikel.epreis1


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1081)).first()
    ldry = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1082)).first()
    dstore = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 246)).first()
    long_digit = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 977)).first()
    coa_format = htparam.fchar

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 240)).first()

    if htparam.flogical:
        double_currency = True

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 144)).first()

        waehrung = db_session.query(Waehrung).filter(
                (Waehrung.wabkurz == htparam.fchar)).first()

        if waehrung:
            foreign_nr = waehrungsnr
            exchg_rate = waehrung.ankauf / waehrung.einheit
        else:
            exchg_rate = 1

    if case_type == 0:
        create_list()

    elif case_type == 1:
        create_food()

    elif case_type == 2:
        create_beverage()

    return generate_output()