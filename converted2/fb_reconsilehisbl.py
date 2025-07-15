from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from functions.calc_servvat import calc_servvat
from models import Htparam, H_artikel, L_besthis, Gl_acct, L_lager, L_ophis, L_ophhis, Hoteldpt, H_compli, Exrate, Artikel, Gl_main, H_cost, L_artikel, Umsatz

def fb_reconsilehisbl(pvilanguage:int, from_grp:int, food:int, bev:int, from_date:date, to_date:date, ldry:int, dstore:int, double_currency:bool, foreign_nr:int, exchg_rate:decimal, mi_opt_chk:bool, date1:date, date2:date):
    done = False
    output_list_list = []
    lvcarea:str = "fb_reconsilehis"
    type_of_acct:int = 0
    counter:int = 0
    curr_nr:int = 0
    curr_reihe:int = 0
    coa_format:str = ""
    betrag:decimal = 0
    long_digit:bool = False
    htparam = h_artikel = l_besthis = gl_acct = l_lager = l_ophis = l_ophhis = hoteldpt = h_compli = exrate = artikel = gl_main = h_cost = l_artikel = umsatz = None

    output_list = s_list = h_art = l_oh = gl_acct1 = None

    output_list_list, Output_list = create_model("Output_list", {"nr":int, "code":int, "bezeich":str, "s":str})
    s_list_list, S_list = create_model("S_list", {"code":int, "reihenfolge":int, "lager_nr":int, "l_bezeich":str, "fibukonto":str, "bezeich":str, "flag":int, "anf_wert":decimal, "end_wert":decimal, "betrag":decimal}, {"reihenfolge": 1, "flag": 2})

    H_art = H_artikel
    L_oh = L_besthis
    Gl_acct1 = Gl_acct

    db_session = local_storage.db_session

    def generate_output():
        nonlocal done, output_list_list, lvcarea, type_of_acct, counter, curr_nr, curr_reihe, coa_format, betrag, long_digit, htparam, h_artikel, l_besthis, gl_acct, l_lager, l_ophis, l_ophhis, hoteldpt, h_compli, exrate, artikel, gl_main, h_cost, l_artikel, umsatz
        nonlocal h_art, l_oh, gl_acct1


        nonlocal output_list, s_list, h_art, l_oh, gl_acct1
        nonlocal output_list_list, s_list_list
        return {"done": done, "output-list": output_list_list}

    def create_list():

        nonlocal done, output_list_list, lvcarea, type_of_acct, counter, curr_nr, curr_reihe, coa_format, betrag, long_digit, htparam, h_artikel, l_besthis, gl_acct, l_lager, l_ophis, l_ophhis, hoteldpt, h_compli, exrate, artikel, gl_main, h_cost, l_artikel, umsatz
        nonlocal h_art, l_oh, gl_acct1


        nonlocal output_list, s_list, h_art, l_oh, gl_acct1
        nonlocal output_list_list, s_list_list

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
        fb_str[0] = translateExtended ("Beverage to food", lvcarea, "")
        fb_str[1] = translateExtended ("food to Beverage", lvcarea, "")
        H_art = H_artikel
        L_oh = L_besthis
        Gl_acct1 = Gl_acct
        s_list_list.clear()
        output_list_list.clear()
        curr_nr = 0
        curr_reihe = 0

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 862)).first()
        f_eknr = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 892)).first()
        b_eknr = htparam.finteger

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

            l_besthis_obj_list = []
            for l_besthis, l_oh in db_session.query(L_besthis, L_oh).join(L_oh,(L_oh.anf_best_dat == from_date) &  (L_oh.lager_nr == 0) &  (L_oh.artnr == L_besthis.artnr)).filter(
                    (L_besthis.anf_best_dat == from_date) &  (L_besthis.lager_nr == l_lager.lager_nr) &  (L_besthis.artnr <= 2999999)).all():
                if l_besthis._recid in l_besthis_obj_list:
                    continue
                else:
                    l_besthis_obj_list.append(l_besthis._recid)

                if l_besthis.artnr <= 1999999:
                    flag = 1
                else:
                    flag = 2
                qty1 = l_besthis.anz_anf_best + l_besthis.anz_eingang - l_besthis.anz_ausgang
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
                s_list.anf_wert = s_list.anf_wert + l_besthis.val_anf_best

                if qty != 0:
                    s_list.end_wert = s_list.end_wert + wert * qty1 / qty

                for l_ophis in db_session.query(L_ophis).filter(
                        (L_ophis.datum >= from_date) &  (L_ophis.datum <= to_date) &  (L_ophis.artnr == l_besthis.artnr) &  (L_ophis.op_art == 1) &  (L_ophis.lager_nr == l_lager.lager_nr) &  (not L_ophis.fibukonto.op("~")(".*;CANCELLED.*"))).all():

                    l_ophhis = db_session.query(L_ophhis).filter(
                            (L_ophhis.lscheinnr == l_ophis.lscheinnr) &  (func.lower(L_ophhis.op_typ) == "STI")).first()

                    if l_ophis.anzahl >= 0:

                        s_list = query(s_list_list, filters=(lambda s_list :s_list.lager_nr == l_lager.lager_nr and s_list.reihenfolge == flag and s_list.flag == 11), first=True)

                        if not s_list:
                            s_list = S_list()
                            s_list_list.append(s_list)

                            s_list.reihenfolge = flag
                            s_list.lager_nr = l_lager.lager_nr
                            s_list.l_bezeich = l_lager.bezeich
                            s_list.flag = 11
                        s_list.betrag = s_list.betrag + l_ophis.warenwert

                    elif l_ophis.anzahl < 0:

                        s_list = query(s_list_list, filters=(lambda s_list :s_list.lager_nr == l_lager.lager_nr and s_list.reihenfolge == flag and s_list.flag == 12), first=True)

                        if not s_list:
                            s_list = S_list()
                            s_list_list.append(s_list)

                            s_list.reihenfolge = flag
                            s_list.lager_nr = l_lager.lager_nr
                            s_list.l_bezeich = l_lager.bezeich
                            s_list.flag = 12
                        s_list.betrag = s_list.betrag + l_ophis.warenwert

                l_ophis_obj_list = []
                for l_ophis, l_ophhis, gl_acct in db_session.query(L_ophis, L_ophhis, Gl_acct).join(L_ophhis,(L_ophhis.lscheinnr == L_ophis.lscheinnr) &  (func.lower(L_ophhis.op_typ) == "STT")).join(Gl_acct,(Gl_acct.fibukonto == l_ophhis.fibukonto)).filter(
                        (L_ophis.datum >= from_date) &  (L_ophis.datum <= to_date) &  (L_ophis.artnr == l_besthis.artnr) &  (L_ophis.op_art == 3) &  (L_ophis.lager_nr == l_lager.lager_nr) &  (not L_ophis.fibukonto.op("~")(".*;CANCELLED.*"))).all():
                    if l_ophis._recid in l_ophis_obj_list:
                        continue
                    else:
                        l_ophis_obj_list.append(l_ophis._recid)


                    type_of_acct = gl_acct.acc_type
                    fibukonto = gl_acct.fibukonto
                    bezeich = to_string(gl_acct.fibukonto, coa_format) + " " + gl_acct.bezeich.upper()

                    if l_ophis.fibukonto != "":

                        gl_acct1 = db_session.query(Gl_acct1).filter(
                                    (Gl_acct1.fibukonto == l_ophis.fibukonto)).first()

                        if gl_acct1:
                            type_of_acct = gl_acct1.acc_type
                            fibukonto = gl_acct1.fibukonto
                            bezeich = to_string(gl_acct1.fibukonto, coa_format) + " " + gl_acct1.bezeich.upper()

                    if flag == 1 and fibukonto.lower()  == (food_bev).lower() :

                        s_list = query(s_list_list, filters=(lambda s_list :s_list.lager_nr == 9999 and s_list.reihenfolge == 2), first=True)
                        s_list.anf_wert = s_list.anf_wert + l_ophis.warenwert

                    elif flag == 2 and fibukonto.lower()  == (bev_food).lower() :

                        s_list = query(s_list_list, filters=(lambda s_list :s_list.lager_nr == 9999 and s_list.reihenfolge == 1), first=True)
                        s_list.anf_wert = s_list.anf_wert + l_ophis.warenwert
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
                            s_list.betrag = s_list.betrag + l_ophis.warenwert

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

                    if h_cost.betrag == 1:
                        betrag = 0


                    else:
                        betrag = h_cost.betrag

                    if artikel.umsatzart == 6:
                        b_cost = h_compli.anzahl * betrag

                    elif artikel.umsatzart == 3 or artikel.umsatzart == 5:
                        f_cost = h_compli.anzahl * betrag

                elif not h_cost or (h_cost and h_cost.betrag == 0):

                    if artikel.umsatzart == 6:
                        b_cost = h_compli.anzahl * h_compli.epreis * h_artikel.prozent / 100 * rate

                    elif artikel.umsatzart == 3 or artikel.umsatzart == 5:
                        f_cost = h_compli.anzahl * h_compli.epreis * h_artikel.prozent / 100 * rate

                if f_cost != 0:

                    if mi_opt_chk == False:

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

                    if mi_opt_chk == False:

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
            output_list = Output_list()
            output_list_list.append(output_list)

            curr_nr = curr_nr + 1
            output_list.nr = curr_nr
            output_list.s = STRING ("", "x(24)") + to_string(translateExtended ("** food **", lvcarea, "") , "x(33)")
            output_list = Output_list()
            output_list_list.append(output_list)

            curr_nr = curr_nr + 1
            output_list.nr = curr_nr
            i = 0
            output_list = Output_list()
            output_list_list.append(output_list)

            curr_nr = curr_nr + 1
            output_list.nr = curr_nr
            output_list.s = to_string(translateExtended ("1. Opening Inventory", lvcarea, "") , "x(24)")

            for s_list in query(s_list_list, filters=(lambda s_list :s_list.flag == 0 and s_list.reihenfolge == 1 and s_list.lager_nr != 9999 and s_list.anf_wert != 0)):
                i = i + 1
                betrag1 = betrag1 + s_list.anf_wert

                if i > 1:
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    curr_nr = curr_nr + 1
                    output_list.nr = curr_nr
                    output_list.s = to_string("", "x(24)")

                if not long_digit:
                    pass
                    output_list.s = output_list.s + to_string(s_list.l_bezeich, "x(33)") + to_string(s_list.anf_wert, "->>>,>>>,>>9.99")
                else:
                    pass
                    output_list.s = output_list.s + to_string(s_list.l_bezeich, "x(33)") + to_string(s_list.anf_wert, "->>,>>>,>>>,>>9")
            output_list = Output_list()
            output_list_list.append(output_list)

            curr_nr = curr_nr + 1
            output_list.nr = curr_nr

            if not long_digit:
                output_list.s = to_string("", "x(24)") + to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)") + to_string("", "x(15)") + to_string(betrag1, "->>>,>>>,>>9.99")
            else:
                pass
                output_list.s = to_string("", "x(24)") + to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)") + to_string("", "x(15)") + to_string(betrag1, "->>,>>>,>>>,>>9")
            i = 0
            output_list = Output_list()
            output_list_list.append(output_list)

            curr_nr = curr_nr + 1
            output_list.nr = curr_nr
            output_list.s = to_string(translateExtended ("2. Incoming Stocks", lvcarea, "") , "x(24)")

            for s_list in query(s_list_list, filters=(lambda s_list :s_list.flag == 11 and s_list.reihenfolge == 1)):
                i = i + 1
                betrag2 = betrag2 + s_list.betrag

                if i > 1:
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    curr_nr = curr_nr + 1
                    output_list.nr = curr_nr
                    output_list.s = to_string("", "x(24)")

                if not long_digit:
                    pass
                    output_list.s = output_list.s + to_string(s_list.l_bezeich, "x(33)") + to_string(s_list.betrag, "->>>,>>>,>>9.99")
                else:
                    pass
                    output_list.s = output_list.s + to_string(s_list.l_bezeich, "x(33)") + to_string(s_list.betrag, "->>,>>>,>>>,>>9")
            output_list = Output_list()
            output_list_list.append(output_list)

            curr_nr = curr_nr + 1
            output_list.nr = curr_nr

            if not long_digit:
                output_list.s = to_string("", "x(24)") + to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)") + to_string("", "x(15)") + to_string(betrag2, "->>>,>>>,>>9.99")
            else:
                output_list.s = to_string("", "x(24)") + to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)") + to_string("", "x(15)") + to_string(betrag2, "->>,>>>,>>>,>>9")
            i = 0
            output_list = Output_list()
            output_list_list.append(output_list)

            curr_nr = curr_nr + 1
            output_list.nr = curr_nr
            output_list.s = to_string(translateExtended ("3. Returned Stocks", lvcarea, "") , "x(24)")

            for s_list in query(s_list_list, filters=(lambda s_list :s_list.flag == 12 and s_list.reihenfolge == 1)):
                i = i + 1
                betrag3 = betrag3 + s_list.betrag

                if i > 1:
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    curr_nr = curr_nr + 1
                    output_list.nr = curr_nr
                    output_list.s = to_string("", "x(24)")

                if not long_digit:
                    pass
                    output_list.s = output_list.s + to_string(s_list.l_bezeich, "x(33)") + to_string(s_list.betrag, "->>>,>>>,>>9.99")
                else:
                    pass
                    output_list.s = output_list.s + to_string(s_list.l_bezeich, "x(33)") + to_string(s_list.betrag, "->>,>>>,>>>,>>9")
            output_list = Output_list()
            output_list_list.append(output_list)

            curr_nr = curr_nr + 1
            output_list.nr = curr_nr

            if not long_digit:
                output_list.s = to_string("", "x(24)") + to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)") + to_string("", "x(15)") + to_string(betrag3, "->>>,>>>,>>9.99")
            else:
                output_list.s = to_string("", "x(24)") + to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)") + to_string("", "x(15)") + to_string(betrag3, "->>,>>>,>>>,>>9")

            s_list = query(s_list_list, filters=(lambda s_list :s_list.lager_nr == 9999 and s_list.reihenfolge == 1), first=True)
            output_list = Output_list()
            output_list_list.append(output_list)

            curr_nr = curr_nr + 1
            output_list.nr = curr_nr

            if not long_digit:
                output_list.s = to_string(("4. " + s_list.l_bezeich) , "x(24)") + to_string("", "x(33)") + to_string("", "x(15)") + to_string(s_list.anf_wert, "->>>,>>>,>>9.99")
            else:
                output_list.s = to_string(("4. " + s_list.l_bezeich) , "x(24)") + to_string("", "x(33)") + to_string("", "x(15)") + to_string(s_list.anf_wert, "->>,>>>,>>>,>>9")
            output_list = Output_list()
            output_list_list.append(output_list)

            curr_nr = curr_nr + 1
            output_list.nr = curr_nr
            betrag4 = betrag1 + betrag2 + betrag3 + s_list.anf_wert
            output_list = Output_list()
            output_list_list.append(output_list)

            curr_nr = curr_nr + 1
            output_list.nr = curr_nr

            if not long_digit:
                output_list.s = to_string(translateExtended ("5. Inventory Available", lvcarea, "") , "x(24)") + to_string("(1 + 2 + 3 + 4)", "x(33)") + to_string("", "x(15)") + to_string(betrag4, "->>>,>>>,>>9.99")
            else:
                output_list.s = to_string(translateExtended ("5. Inventory Available", lvcarea, "") , "x(24)") + to_string("(1 + 2 + 3 + 4)", "x(33)") + to_string("", "x(15)") + to_string(betrag4, "->>,>>>,>>>,>>9")
            output_list = Output_list()
            output_list_list.append(output_list)

            curr_nr = curr_nr + 1
            output_list.nr = curr_nr
            i = 0
            output_list = Output_list()
            output_list_list.append(output_list)

            curr_nr = curr_nr + 1
            output_list.nr = curr_nr
            output_list.s = to_string(translateExtended ("6. Closing Inventory", lvcarea, "") , "x(24)")

            for s_list in query(s_list_list, filters=(lambda s_list :s_list.flag == 0 and s_list.reihenfolge == 1 and s_list.lager_nr != 9999 and s_list.end_wert != 0)):
                i = i + 1
                betrag5 = betrag5 + s_list.end_wert

                if i > 1:
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    curr_nr = curr_nr + 1
                    output_list.nr = curr_nr
                    output_list.s = to_string("", "x(24)")

                if not long_digit:
                    output_list.s = output_list.s + to_string(s_list.l_bezeich, "x(33)") + to_string(s_list.end_wert, "->>>,>>>,>>9.99")
                else:
                    output_list.s = output_list.s + to_string(s_list.l_bezeich, "x(33)") + to_string(s_list.end_wert, "->>,>>>,>>>,>>9")
            output_list = Output_list()
            output_list_list.append(output_list)

            curr_nr = curr_nr + 1
            output_list.nr = curr_nr

            if not long_digit:
                output_list.s = to_string("", "x(24)") + to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)") + to_string("", "x(15)") + to_string(betrag5, "->>>,>>>,>>9.99")
            else:
                output_list.s = to_string("", "x(24)") + to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)") + to_string("", "x(15)") + to_string(betrag5, "->>,>>>,>>>,>>9")
            output_list = Output_list()
            output_list_list.append(output_list)

            curr_nr = curr_nr + 1
            output_list.nr = curr_nr
            betrag56 = betrag4 - betrag5

            if not long_digit:
                output_list.s = to_string(translateExtended ("7. Gross Consumption", lvcarea, "") , "x(24)") + to_string("(5 - 6)", "x(33)") + to_string("", "x(15)") + to_string(betrag56, "->>>,>>>,>>9.99")
            else:
                output_list.s = to_string(translateExtended ("7. Gross Consumption", lvcarea, "") , "x(24)") + to_string("(5 - 6)", "x(33)") + to_string("", "x(15)") + to_string(betrag56, "->>,>>>,>>>,>>9")
            output_list = Output_list()
            output_list_list.append(output_list)

            curr_nr = curr_nr + 1
            output_list.nr = curr_nr
            output_list = Output_list()
            output_list_list.append(output_list)

            curr_nr = curr_nr + 1
            output_list.nr = curr_nr
            output_list.s = to_string(translateExtended ("8. Credits", lvcarea, "") , "x(24)")

            if mi_opt_chk == False:
                output_list = Output_list()
                output_list_list.append(output_list)

                curr_nr = curr_nr + 1
                output_list.nr = curr_nr
                output_list.s = to_string(translateExtended ("- Compliment Cost", lvcarea, "") , "x(24)")
                counter = 0
            else:
                counter = 1

            for s_list in query(s_list_list, filters=(lambda s_list :s_list.flag == 4 and s_list.reihenfolge == 1 and s_list.betrag != 0)):
                betrag6 = betrag6 + s_list.betrag
                counter = counter + 1

                if counter > 1:
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.nr = curr_nr

                    if s_list.code > 0:
                        output_list.code = s_list.code
                    else:
                        output_list.code = counter
                    output_list.s = to_string("", "x(24)")

                if not long_digit:
                    output_list.s = output_list.s + to_string(s_list.bezeich, "x(33)") + to_string(s_list.betrag, "->>>,>>>,>>9.99")
                else:
                    output_list.s = output_list.s + to_string(s_list.bezeich, "x(33)") + to_string(s_list.betrag, "->>,>>>,>>>,>>9")

            if mi_opt_chk == False:
                output_list = Output_list()
                output_list_list.append(output_list)

                curr_nr = curr_nr + 1
                output_list.nr = curr_nr
                output_list = Output_list()
                output_list_list.append(output_list)

                curr_nr = curr_nr + 1
                output_list.nr = curr_nr
                output_list.s = to_string(translateExtended ("- Department Expenses", lvcarea, "") , "x(24)")
                counter = 0
            else:
                counter = 1

            for s_list in query(s_list_list, filters=(lambda s_list :s_list.flag == 5 and s_list.reihenfolge == 1 and s_list.betrag != 0)):
                betrag6 = betrag6 + s_list.betrag
                counter = counter + 1

                if counter > 1:
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.nr = curr_nr

                    if s_list.code > 0:
                        output_list.code = s_list.code
                    else:
                        output_list.code = counter
                    output_list.s = to_string("", "x(24)")

                if not long_digit:
                    output_list.s = output_list.s + to_string(s_list.bezeich, "x(33)") + to_string(s_list.betrag, "->>>,>>>,>>9.99")
                else:
                    output_list.s = output_list.s + to_string(s_list.bezeich, "x(33)") + to_string(s_list.betrag, "->>,>>>,>>>,>>9")

            s_list = query(s_list_list, filters=(lambda s_list :s_list.reihenfolge == 2 and s_list.lager_nr == 9999), first=True)
            output_list = Output_list()
            output_list_list.append(output_list)

            curr_nr = curr_nr + 1
            output_list.nr = curr_nr
            output_list.s = to_string("", "x(24)")

            if not long_digit:
                output_list.s = output_list.s + to_string(s_list.l_bezeich, "x(33)") + to_string(s_list.anf_wert, "->>>,>>>,>>9.99")
            else:
                output_list.s = output_list.s + to_string(s_list.l_bezeich, "x(33)") + to_string(s_list.anf_wert, "->>,>>>,>>>,>>9")
            betrag6 = betrag6 + s_list.anf_wert

            if mi_opt_chk == False:
                output_list = Output_list()
                output_list_list.append(output_list)

                curr_nr = curr_nr + 1
                output_list.nr = curr_nr
                output_list = Output_list()
                output_list_list.append(output_list)

                curr_nr = curr_nr + 1
                output_list.nr = curr_nr

                if not long_digit:
                    output_list.s = to_string("", "x(24)") + to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)") + to_string("", "x(15)") + to_string(betrag6, "->>>,>>>,>>9.99")
                else:
                    output_list.s = to_string("", "x(24)") + to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)") + to_string("", "x(15)") + to_string(betrag6, "->>,>>>,>>>,>>9")
            output_list = Output_list()
            output_list_list.append(output_list)

            curr_nr = curr_nr + 1
            output_list.nr = curr_nr
            consume2 = betrag56 - betrag6
            output_list = Output_list()
            output_list_list.append(output_list)

            curr_nr = curr_nr + 1
            output_list.nr = curr_nr

            if not long_digit:
                output_list.s = to_string(translateExtended ("9. Net Consumption", lvcarea, "") , "x(24)") + to_string("(7 - 8)", "x(33)") + to_string("", "x(15)") + to_string(consume2, "->>>,>>>,>>9.99")
            else:
                output_list.s = to_string(translateExtended ("9. Net Consumption", lvcarea, "") , "x(24)") + to_string("(7 - 8)", "x(33)") + to_string("", "x(15)") + to_string(consume2, "->>,>>>,>>>,>>9")
            output_list = Output_list()
            output_list_list.append(output_list)

            curr_nr = curr_nr + 1
            output_list.nr = curr_nr
            output_list = Output_list()
            output_list_list.append(output_list)

            curr_nr = curr_nr + 1
            output_list.nr = curr_nr
            f_ratio = 0

            if tf_sales != 0:
                f_ratio = consume2 / tf_sales * 100

            if not long_digit:
                output_list.s = to_string(translateExtended ("Net food Sales", lvcarea, "") , "x(24)") + to_string("", "x(16)") + to_string(tf_sales, "->,>>>,>>>,>>9.99") + to_string(translateExtended ("     Cost:Sales", lvcarea, "") , "x(15)") + to_string(f_ratio, "->,>>>,>>9.99 %")
            else:
                output_list.s = to_string(translateExtended ("Net food Sales", lvcarea, "") , "x(24)") + to_string("", "x(16)") + to_string(tf_sales, " ->>>,>>>,>>>,>>9") + to_string(translateExtended ("     Cost:Sales", lvcarea, "") , "x(15)") + to_string(f_ratio, "->,>>>,>>9.99 %")

        if from_grp == 1:

            return
        output_list = Output_list()
        output_list_list.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        output_list = Output_list()
        output_list_list.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        output_list = Output_list()
        output_list_list.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        output_list.s = to_string("", "x(24)") + to_string(translateExtended ("** BEVERAGE **", lvcarea, "") , "x(33)")
        output_list = Output_list()
        output_list_list.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        i = 0
        output_list = Output_list()
        output_list_list.append(output_list)

        betrag1 = 0
        output_list.s = to_string(translateExtended ("1. Opening Inventory", lvcarea, "") , "x(24)")

        for s_list in query(s_list_list, filters=(lambda s_list :s_list.flag == 0 and s_list.reihenfolge == 2 and s_list.lager_nr != 9999 and s_list.anf_wert != 0)):
            i = i + 1
            betrag1 = betrag1 + s_list.anf_wert

            if i > 1:
                output_list = Output_list()
                output_list_list.append(output_list)

                curr_nr = curr_nr + 1
                output_list.nr = curr_nr
                output_list.s = to_string("", "x(24)")

            if not long_digit:
                output_list.s = output_list.s + to_string(s_list.l_bezeich, "x(33)") + to_string(s_list.anf_wert, "->>>,>>>,>>9.99")
            else:
                output_list.s = output_list.s + to_string(s_list.l_bezeich, "x(33)") + to_string(s_list.anf_wert, "->>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_list.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr

        if not long_digit:
            output_list.s = to_string("", "x(24)") + to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)") + to_string("", "x(15)") + to_string(betrag1, "->>>,>>>,>>9.99")
        else:
            output_list.s = to_string("", "x(24)") + to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)") + to_string("", "x(15)") + to_string(betrag1, "->>,>>>,>>>,>>9")
        i = 0
        output_list = Output_list()
        output_list_list.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        output_list.s = to_string(translateExtended ("2. Incoming Stocks", lvcarea, "") , "x(24)")
        betrag2 = 0

        for s_list in query(s_list_list, filters=(lambda s_list :s_list.flag == 11 and s_list.reihenfolge == 2)):
            i = i + 1
            betrag2 = betrag2 + s_list.betrag

            if i > 1:
                output_list = Output_list()
                output_list_list.append(output_list)

                curr_nr = curr_nr + 1
                output_list.nr = curr_nr
                output_list.s = to_string("", "x(24)")

            if not long_digit:
                output_list.s = output_list.s + to_string(s_list.l_bezeich, "x(33)") + to_string(s_list.betrag, "->>>,>>>,>>9.99")
            else:
                output_list.s = output_list.s + to_string(s_list.l_bezeich, "x(33)") + to_string(s_list.betrag, "->>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_list.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr

        if not long_digit:
            output_list.s = to_string("", "x(24)") + to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)") + to_string("", "x(15)") + to_string(betrag2, "->>>,>>>,>>9.99")
        else:
            output_list.s = to_string("", "x(24)") + to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)") + to_string("", "x(15)") + to_string(betrag2, "->>,>>>,>>>,>>9")
        i = 0
        output_list = Output_list()
        output_list_list.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        output_list.s = to_string(translateExtended ("3. Returned Stocks", lvcarea, "") , "x(24)")
        betrag3 = 0

        for s_list in query(s_list_list, filters=(lambda s_list :s_list.flag == 12 and s_list.reihenfolge == 2)):
            i = i + 1
            betrag3 = betrag3 + s_list.betrag

            if i > 1:
                output_list = Output_list()
                output_list_list.append(output_list)

                curr_nr = curr_nr + 1
                output_list.nr = curr_nr
                output_list.s = to_string("", "x(24)")

            if not long_digit:
                output_list.s = output_list.s + to_string(s_list.l_bezeich, "x(33)") + to_string(s_list.betrag, "->>>,>>>,>>9.99")
            else:
                output_list.s = output_list.s + to_string(s_list.l_bezeich, "x(33)") + to_string(s_list.betrag, "->>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_list.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr

        if not long_digit:
            output_list.s = to_string("", "x(24)") + to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)") + to_string("", "x(15)") + to_string(betrag3, "->>>,>>>,>>9.99")
        else:
            output_list.s = to_string("", "x(24)") + to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)") + to_string("", "x(15)") + to_string(betrag3, "->>,>>>,>>>,>>9")

        s_list = query(s_list_list, filters=(lambda s_list :s_list.lager_nr == 9999 and s_list.reihenfolge == 2), first=True)
        output_list = Output_list()
        output_list_list.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr

        if not long_digit:
            output_list.s = to_string(("4. " + s_list.l_bezeich) , "x(24)") + to_string("", "x(33)") + to_string("", "x(15)") + to_string(s_list.anf_wert, "->>>,>>>,>>9.99")
        else:
            output_list.s = to_string(("4. " + s_list.l_bezeich) , "x(24)") + to_string("", "x(33)") + to_string("", "x(15)") + to_string(s_list.anf_wert, "->>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_list.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        betrag4 = betrag1 + betrag2 + betrag3 + s_list.anf_wert
        output_list = Output_list()
        output_list_list.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr

        if not long_digit:
            output_list.s = to_string(translateExtended ("5. Inventory Available", lvcarea, "") , "x(24)") + to_string("(1 + 2 + 3 + 4)", "x(33)") + to_string("", "x(15)") + to_string(betrag4, "->>>,>>>,>>9.99")
        else:
            output_list.s = to_string(translateExtended ("5. Inventory Available", lvcarea, "") , "x(24)") + to_string("(1 + 2 + 3 + 4)", "x(33)") + to_string("", "x(15)") + to_string(betrag4, "->>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_list.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        i = 0
        output_list = Output_list()
        output_list_list.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        output_list.s = to_string(translateExtended ("6. Closing Inventory", lvcarea, "") , "x(24)")
        betrag5 = 0

        for s_list in query(s_list_list, filters=(lambda s_list :s_list.flag == 0 and s_list.reihenfolge == 2 and s_list.lager_nr != 9999 and s_list.end_wert != 0)):
            i = i + 1
            betrag5 = betrag5 + s_list.end_wert

            if i > 1:
                output_list = Output_list()
                output_list_list.append(output_list)

                curr_nr = curr_nr + 1
                output_list.nr = curr_nr
                output_list.s = to_string("", "x(24)")

            if not long_digit:
                output_list.s = output_list.s + to_string(s_list.l_bezeich, "x(33)") + to_string(s_list.end_wert, "->>>,>>>,>>9.99")
            else:
                output_list.s = output_list.s + to_string(s_list.l_bezeich, "x(33)") + to_string(s_list.end_wert, "->>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_list.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr

        if not long_digit:
            output_list.s = to_string("", "x(24)") + to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)") + to_string("", "x(15)") + to_string(betrag5, "->>>,>>>,>>9.99")
        else:
            output_list.s = to_string("", "x(24)") + to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)") + to_string("", "x(15)") + to_string(betrag5, "->>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_list.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        betrag56 = betrag4 - betrag5

        if not long_digit:
            output_list.s = to_string(translateExtended ("7. Gross Consumption", lvcarea, "") , "x(24)") + to_string("(5 - 6)", "x(33)") + to_string("", "x(15)") + to_string(betrag56, "->>>,>>>,>>9.99")
        else:
            output_list.s = to_string(translateExtended ("7. Gross Consumption", lvcarea, "") , "x(24)") + to_string("(5 - 6)", "x(33)") + to_string("", "x(15)") + to_string(betrag56, "->>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_list.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        output_list = Output_list()
        output_list_list.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        output_list.s = to_string(translateExtended ("8. Credits", lvcarea, "") , "x(24)")
        betrag6 = 0

        if mi_opt_chk == False:
            output_list = Output_list()
            output_list_list.append(output_list)

            curr_nr = curr_nr + 1
            output_list.nr = curr_nr
            output_list.s = to_string(translateExtended ("- Compliment Cost", lvcarea, "") , "x(24)")
            counter = 0
        else:
            counter = 1

        for s_list in query(s_list_list, filters=(lambda s_list :s_list.flag == 4 and s_list.reihenfolge == 2 and s_list.betrag != 0)):
            betrag6 = betrag6 + s_list.betrag
            counter = counter + 1

            if counter > 1:
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.nr = curr_nr

                if s_list.code > 0:
                    output_list.code = s_list.code
                else:
                    output_list.code = counter
                output_list.s = to_string("", "x(24)")

            if not long_digit:
                output_list.s = output_list.s + to_string(s_list.bezeich, "x(33)") + to_string(s_list.betrag, "->>>,>>>,>>9.99")
            else:
                output_list.s = output_list.s + to_string(s_list.bezeich, "x(33)") + to_string(s_list.betrag, "->>,>>>,>>>,>>9")

        if mi_opt_chk == False:
            output_list = Output_list()
            output_list_list.append(output_list)

            curr_nr = curr_nr + 1
            output_list.nr = curr_nr
            output_list.s = to_string(translateExtended ("- Department Expenses", lvcarea, "") , "x(24)")
            counter = 0
        else:
            counter = 1

        for s_list in query(s_list_list, filters=(lambda s_list :s_list.flag == 5 and s_list.reihenfolge == 2 and s_list.betrag != 0)):
            counter = counter + 1
            betrag6 = betrag6 + s_list.betrag

            if counter > 1:
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.nr = curr_nr

                if s_list.code > 0:
                    output_list.code = s_list.code
                else:
                    output_list.code = counter
                output_list.s = to_string("", "x(24)")

            if not long_digit:
                output_list.s = output_list.s + to_string(s_list.bezeich, "x(33)") + to_string(s_list.betrag, "->>>,>>>,>>9.99")
            else:
                output_list.s = output_list.s + to_string(s_list.bezeich, "x(33)") + to_string(s_list.betrag, "->>,>>>,>>>,>>9")

        s_list = query(s_list_list, filters=(lambda s_list :s_list.reihenfolge == 1 and s_list.lager_nr == 9999), first=True)
        output_list = Output_list()
        output_list_list.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        output_list.s = to_string("", "x(24)")

        if not long_digit:
            output_list.s = output_list.s + to_string(s_list.l_bezeich, "x(33)") + to_string(s_list.anf_wert, "->>>,>>>,>>9.99")
        else:
            output_list.s = output_list.s + to_string(s_list.l_bezeich, "x(33)") + to_string(s_list.anf_wert, "->>,>>>,>>>,>>9")
        betrag6 = betrag6 + s_list.anf_wert

        if mi_opt_chk == False:
            output_list = Output_list()
            output_list_list.append(output_list)

            curr_nr = curr_nr + 1
            output_list.nr = curr_nr
        output_list = Output_list()
        output_list_list.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr

        if not long_digit:
            output_list.s = to_string("", "x(24)") + to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)") + to_string("", "x(15)") + to_string(betrag6, "->>>,>>>,>>9.99")
        else:
            output_list.s = to_string("", "x(24)") + to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)") + to_string("", "x(15)") + to_string(betrag6, "->>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_list.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        consume2 = betrag56 - betrag6
        output_list = Output_list()
        output_list_list.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr

        if not long_digit:
            output_list.s = to_string(translateExtended ("9. Net Consumption", lvcarea, "") , "x(24)") + to_string("(7 - 8)", "x(33)") + to_string("", "x(15)") + to_string(consume2, "->>>,>>>,>>9.99")
        else:
            output_list.s = to_string(translateExtended ("9. Net Consumption", lvcarea, "") , "x(24)") + to_string("(7 - 8)", "x(33)") + to_string("", "x(15)") + to_string(consume2, "->>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_list.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        output_list = Output_list()
        output_list_list.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        b_ratio = 0

        if tb_sales != 0:
            b_ratio = consume2 / tb_sales * 100

        if not long_digit:
            output_list.s = to_string(translateExtended ("Net Beverage Sales", lvcarea, "") , "x(24)") + to_string("", "x(16)") + to_string(tb_sales, "->,>>>,>>>,>>9.99") + to_string(translateExtended ("     Cost:Sales", lvcarea, "") , "x(15)") + to_string(b_ratio, "->,>>>,>>9.99 %")
        else:
            output_list.s = to_string(translateExtended ("Net Beverage Sales", lvcarea, "") , "x(24)") + to_string("", "x(16)") + to_string(tb_sales, " ->>>,>>>,>>>,>>9") + to_string(translateExtended ("     Cost:Sales", lvcarea, "") , "x(15)") + to_string(b_ratio, "->,>>>,>>9.99 %")
        done = True

    def create_food():

        nonlocal done, output_list_list, lvcarea, type_of_acct, counter, curr_nr, curr_reihe, coa_format, betrag, long_digit, htparam, h_artikel, l_besthis, gl_acct, l_lager, l_ophis, l_ophhis, hoteldpt, h_compli, exrate, artikel, gl_main, h_cost, l_artikel, umsatz
        nonlocal h_art, l_oh, gl_acct1


        nonlocal output_list, s_list, h_art, l_oh, gl_acct1
        nonlocal output_list_list, s_list_list

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
        fb_str[0] = translateExtended ("Beverage to food", lvcarea, "")
        fb_str[1] = translateExtended ("food to Beverage", lvcarea, "")
        H_art = H_artikel
        L_oh = L_besthis
        Gl_acct1 = Gl_acct
        s_list_list.clear()
        output_list_list.clear()
        curr_nr = 0
        curr_reihe = 0

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 862)).first()
        f_eknr = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 892)).first()
        b_eknr = htparam.finteger

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

            l_besthis_obj_list = []
            for l_besthis, l_oh in db_session.query(L_besthis, L_oh).join(L_oh,(L_oh.anf_best_dat == from_date) &  (L_oh.lager_nr == 0) &  (L_oh.artnr == L_besthis.artnr)).filter(
                    (L_besthis.anf_best_dat == from_date) &  (L_besthis.lager_nr == l_lager.lager_nr) &  (L_besthis.artnr >= 1000001) &  (L_besthis.artnr <= 1999999)).all():
                if l_besthis._recid in l_besthis_obj_list:
                    continue
                else:
                    l_besthis_obj_list.append(l_besthis._recid)


                qty1 = l_besthis.anz_anf_best + l_besthis.anz_eingang - l_besthis.anz_ausgang
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

                if l_oh.anz_anf_best != 0:
                    s_list.anf_wert = s_list.anf_wert + l_besthis.anz_anf_best * l_oh.val_anf_best / l_oh.anz_anf_best

                if qty != 0:
                    s_list.end_wert = s_list.end_wert + wert * qty1 / qty

                for l_ophis in db_session.query(L_ophis).filter(
                        (L_ophis.datum >= from_date) &  (L_ophis.datum <= to_date) &  (L_ophis.artnr == l_besthis.artnr) &  (L_ophis.op_art == 1) &  (L_ophis.lager_nr == l_lager.lager_nr) &  (not L_ophis.fibukonto.op("~")(".*;CANCELLED.*"))).all():

                    l_ophhis = db_session.query(L_ophhis).filter(
                            (L_ophhis.lscheinnr == l_ophis.lscheinnr) &  (func.lower(L_ophhis.op_typ) == "STI")).first()

                    if l_ophis.anzahl >= 0:

                        s_list = query(s_list_list, filters=(lambda s_list :s_list.lager_nr == l_lager.lager_nr and s_list.reihenfolge == flag and s_list.flag == 11), first=True)

                        if not s_list:
                            s_list = S_list()
                            s_list_list.append(s_list)

                            s_list.reihenfolge = flag
                            s_list.lager_nr = l_lager.lager_nr
                            s_list.l_bezeich = l_lager.bezeich
                            s_list.flag = 11
                        s_list.betrag = s_list.betrag + l_ophis.warenwert

                    elif l_ophis.anzahl < 0:

                        s_list = query(s_list_list, filters=(lambda s_list :s_list.lager_nr == l_lager.lager_nr and s_list.reihenfolge == flag and s_list.flag == 12), first=True)

                        if not s_list:
                            s_list = S_list()
                            s_list_list.append(s_list)

                            s_list.reihenfolge = flag
                            s_list.lager_nr = l_lager.lager_nr
                            s_list.l_bezeich = l_lager.bezeich
                            s_list.flag = 12
                        s_list.betrag = s_list.betrag + l_ophis.warenwert

                l_ophis_obj_list = []
                for l_ophis, gl_acct in db_session.query(L_ophis, Gl_acct).join(Gl_acct,(Gl_acct.fibukonto == L_ophis.fibukonto)).filter(
                        (L_ophis.datum >= from_date) &  (L_ophis.datum <= to_date) &  (L_ophis.artnr == l_besthis.artnr) &  (L_ophis.op_art == 3) &  (L_ophis.lager_nr == l_lager.lager_nr) &  (not L_ophis.fibukonto.op("~")(".*;CANCELLED.*"))).all():
                    if l_ophis._recid in l_ophis_obj_list:
                        continue
                    else:
                        l_ophis_obj_list.append(l_ophis._recid)


                    type_of_acct = gl_acct.acc_type

                    gl_main = db_session.query(Gl_main).filter(
                                (Gl_main.nr == gl_acct.main_nr)).first()
                    fibukonto = gl_acct.fibukonto
                    bezeich = to_string(gl_acct.fibukonto, coa_format) + " " + gl_acct.bezeich.upper()

                    if fibukonto.lower()  == (food_bev).lower() :
                        pass

                    elif fibukonto.lower()  == (bev_food).lower() :
                        pass
                    else:

                        if mi_opt_chk == False:

                            s_list = query(s_list_list, filters=(lambda s_list :s_list.(fibukonto).lower().lower()  == (fibukonto).lower()  and s_list.reihenfolge == 1 and s_list.flag == 5), first=True)

                            if not s_list:
                                s_list = S_list()
                                s_list_list.append(s_list)

                                s_list.reihenfolge = 1
                                s_list.fibukonto = fibukonto
                                s_list.bezeich = bezeich
                                s_list.flag = 5
                        else:

                            s_list = query(s_list_list, filters=(lambda s_list :s_list.code == gl_main.code and s_list.reihenfolge == flag and s_list.flag == 5), first=True)

                            if not s_list:
                                s_list = S_list()
                                s_list_list.append(s_list)

                                s_list.reihenfolge = 1
                                s_list.code = gl_main.code
                                s_list.bezeich = gl_main.bezeich
                                s_list.flag = 5

                        if type_of_acct == 5 or type_of_acct == 3 or type_of_acct == 4:
                            s_list.betrag = s_list.betrag + l_ophis.warenwert

        l_ophis_obj_list = []
        for l_ophis, l_artikel, l_ophhis, gl_acct in db_session.query(L_ophis, L_artikel, L_ophhis, Gl_acct).join(L_artikel,(L_artikel.artnr == L_ophis.artnr) &  ((L_artikel.endkum == fl_eknr) |  (L_artikel.endkum == bl_eknr))).join(L_ophhis,(L_ophhis.lscheinnr == L_ophis.lscheinnr) &  (func.lower(L_ophhis.op_typ) == "STT")).join(Gl_acct,(Gl_acct.fibukonto == l_ophhis.fibukonto)).filter(
                (L_ophis.datum >= from_date) &  (L_ophis.datum <= to_date) &  ((func.lower(L_ophis.fibukonto) == (bev_food).lower()) |  (func.lower(L_ophis.fibukonto) == food_bev)) &  (L_ophis.op_art == 3) &  (notfunc.lower(func.lower(L_ophis.fibukonto)).op("~")(".*;CANCELLED.*"))).all():
            if l_ophis._recid in l_ophis_obj_list:
                continue
            else:
                l_ophis_obj_list.append(l_ophis._recid)


            fibukonto = gl_acct.fibukonto

            if l_ophis.fibukonto != "":

                gl_acct1 = db_session.query(Gl_acct1).filter(
                        (Gl_acct1.fibukonto == l_ophis.fibukonto)).first()

                if gl_acct1:
                    fibukonto = gl_acct1.fibukonto

            if fibukonto.lower()  == (food_bev).lower()  and l_ophis.artnr >= 1000001 and l_ophis.artnr <= 1999999:

                s_list = query(s_list_list, filters=(lambda s_list :s_list.lager_nr == 9999 and s_list.reihenfolge == 2), first=True)
                s_list.anf_wert = s_list.anf_wert + l_ophis.warenwert

            elif fibukonto.lower()  == (bev_food).lower()  and l_ophis.artnr > 1999999:

                s_list = query(s_list_list, filters=(lambda s_list :s_list.lager_nr == 9999 and s_list.reihenfolge == 1), first=True)
                s_list.anf_wert = s_list.anf_wert + l_ophis.warenwert

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

                    if h_cost.betrag == 1:
                        betrag = 0


                    else:
                        betrag = h_cost.betrag

                    if artikel.umsatzart == 6:
                        b_cost = h_compli.anzahl * betrag

                    elif artikel.umsatzart == 3 or artikel.umsatzart == 5:
                        f_cost = h_compli.anzahl * betrag

                elif not h_cost or (h_cost and h_cost.betrag == 0):

                    if artikel.umsatzart == 6:
                        b_cost = h_compli.anzahl * h_compli.epreis * h_artikel.prozent / 100 * rate

                    elif artikel.umsatzart == 3 or artikel.umsatzart == 5:
                        f_cost = h_compli.anzahl * h_compli.epreis * h_artikel.prozent / 100 * rate

                if f_cost != 0:

                    if mi_opt_chk == False:

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
        output_list = Output_list()
        output_list_list.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        output_list.s = to_string("", "x(24)") + to_string(translateExtended ("** food **", lvcarea, "") , "x(33)")
        output_list = Output_list()
        output_list_list.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        i = 0
        output_list = Output_list()
        output_list_list.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        output_list.s = to_string(translateExtended ("1. Opening Inventory", lvcarea, "") , "x(24)")

        for s_list in query(s_list_list, filters=(lambda s_list :s_list.flag == 0 and s_list.reihenfolge == 1 and s_list.lager_nr != 9999 and s_list.anf_wert != 0)):
            i = i + 1
            betrag1 = betrag1 + s_list.anf_wert

            if i > 1:
                output_list = Output_list()
                output_list_list.append(output_list)

                curr_nr = curr_nr + 1
                output_list.nr = curr_nr
                output_list.s = to_string("", "x(24)")

            if not long_digit:
                output_list.s = output_list.s + to_string(s_list.l_bezeich, "x(33)") + to_string(s_list.anf_wert, "->>>,>>>,>>9.99")
            else:
                output_list.s = output_list.s + to_string(s_list.l_bezeich, "x(33)") + to_string(s_list.anf_wert, "->>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_list.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr

        if not long_digit:
            output_list.s = to_string("", "x(24)") + to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)") + to_string("", "x(15)") + to_string(betrag1, "->>>,>>>,>>9.99")
        else:
            output_list.s = to_string("", "x(24)") + to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)") + to_string("", "x(15)") + to_string(betrag1, "->>,>>>,>>>,>>9")
        i = 0
        output_list = Output_list()
        output_list_list.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        output_list.s = to_string(translateExtended ("2. Incoming Stocks", lvcarea, "") , "x(24)")

        for s_list in query(s_list_list, filters=(lambda s_list :s_list.flag == 11 and s_list.reihenfolge == 1)):
            i = i + 1
            betrag2 = betrag2 + s_list.betrag

            if i > 1:
                output_list = Output_list()
                output_list_list.append(output_list)

                curr_nr = curr_nr + 1
                output_list.nr = curr_nr
                output_list.s = to_string("", "x(24)")

            if not long_digit:
                output_list.s = output_list.s + to_string(s_list.l_bezeich, "x(33)") + to_string(s_list.betrag, "->>>,>>>,>>9.99")
            else:
                output_list.s = output_list.s + to_string(s_list.l_bezeich, "x(33)") + to_string(s_list.betrag, "->>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_list.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr

        if not long_digit:
            output_list.s = to_string("", "x(24)") + to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)") + to_string("", "x(15)") + to_string(betrag2, "->>>,>>>,>>9.99")
        else:
            output_list.s = to_string("", "x(24)") + to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)") + to_string("", "x(15)") + to_string(betrag2, "->>,>>>,>>>,>>9")
        i = 0
        output_list = Output_list()
        output_list_list.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        output_list.s = to_string(translateExtended ("3. Returned Stocks", lvcarea, "") , "x(24)")

        for s_list in query(s_list_list, filters=(lambda s_list :s_list.flag == 12 and s_list.reihenfolge == 1)):
            i = i + 1
            betrag3 = betrag3 + s_list.betrag

            if i > 1:
                output_list = Output_list()
                output_list_list.append(output_list)

                curr_nr = curr_nr + 1
                output_list.nr = curr_nr
                output_list.s = to_string("", "x(24)")

            if not long_digit:
                output_list.s = output_list.s + to_string(s_list.l_bezeich, "x(33)") + to_string(s_list.betrag, "->>>,>>>,>>9.99")
            else:
                output_list.s = output_list.s + to_string(s_list.l_bezeich, "x(33)") + to_string(s_list.betrag, "->>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_list.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr

        if not long_digit:
            output_list.s = to_string("", "x(24)") + to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)") + to_string("", "x(15)") + to_string(betrag3, "->>>,>>>,>>9.99")
        else:
            output_list.s = to_string("", "x(24)") + to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)") + to_string("", "x(15)") + to_string(betrag3, "->>,>>>,>>>,>>9")

        s_list = query(s_list_list, filters=(lambda s_list :s_list.lager_nr == 9999 and s_list.reihenfolge == 1), first=True)
        output_list = Output_list()
        output_list_list.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr

        if not long_digit:
            output_list.s = to_string(("4. " + s_list.l_bezeich) , "x(24)") + to_string("", "x(33)") + to_string("", "x(15)") + to_string(s_list.anf_wert, "->>>,>>>,>>9.99")
        else:
            output_list.s = to_string(("4. " + s_list.l_bezeich) , "x(24)") + to_string("", "x(33)") + to_string("", "x(15)") + to_string(s_list.anf_wert, "->>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_list.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        betrag4 = betrag1 + betrag2 + betrag3 + s_list.anf_wert
        output_list = Output_list()
        output_list_list.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr

        if not long_digit:
            output_list.s = to_string(translateExtended ("5. Inventory Available", lvcarea, "") , "x(24)") + to_string("(1 + 2 + 3 + 4)", "x(33)") + to_string("", "x(15)") + to_string(betrag4, "->>>,>>>,>>9.99")
        else:
            output_list.s = to_string(translateExtended ("5. Inventory Available", lvcarea, "") , "x(24)") + to_string("(1 + 2 + 3 + 4)", "x(33)") + to_string("", "x(15)") + to_string(betrag4, "->>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_list.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        i = 0
        output_list = Output_list()
        output_list_list.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        output_list.s = to_string(translateExtended ("6. Closing Inventory", lvcarea, "") , "x(24)")

        for s_list in query(s_list_list, filters=(lambda s_list :s_list.flag == 0 and s_list.reihenfolge == 1 and s_list.lager_nr != 9999 and s_list.end_wert != 0)):
            i = i + 1
            betrag5 = betrag5 + s_list.end_wert

            if i > 1:
                output_list = Output_list()
                output_list_list.append(output_list)

                curr_nr = curr_nr + 1
                output_list.nr = curr_nr
                output_list.s = to_string("", "x(24)")

            if not long_digit:
                output_list.s = output_list.s + to_string(s_list.l_bezeich, "x(33)") + to_string(s_list.end_wert, "->>>,>>>,>>9.99")
            else:
                output_list.s = output_list.s + to_string(s_list.l_bezeich, "x(33)") + to_string(s_list.end_wert, "->>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_list.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr

        if not long_digit:
            output_list.s = to_string("", "x(24)") + to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)") + to_string("", "x(15)") + to_string(betrag5, "->>>,>>>,>>9.99")
        else:
            output_list.s = to_string("", "x(24)") + to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)") + to_string("", "x(15)") + to_string(betrag5, "->>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_list.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        betrag56 = betrag4 - betrag5

        if not long_digit:
            output_list.s = to_string(translateExtended ("7. Gross Consumption", lvcarea, "") , "x(24)") + to_string("(5 - 6)", "x(33)") + to_string("", "x(15)") + to_string(betrag56, "->>>,>>>,>>9.99")
        else:
            output_list.s = to_string(translateExtended ("7. Gross Consumption", lvcarea, "") , "x(24)") + to_string("(5 - 6)", "x(33)") + to_string("", "x(15)") + to_string(betrag56, "->>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_list.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        output_list = Output_list()
        output_list_list.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        output_list.s = to_string(translateExtended ("8. Credits", lvcarea, "") , "x(24)")

        if mi_opt_chk == False:
            output_list = Output_list()
            output_list_list.append(output_list)

            curr_nr = curr_nr + 1
            output_list.nr = curr_nr
            output_list.s = to_string(translateExtended ("- Compliment Cost", lvcarea, "") , "x(24)")
            counter = 0
        else:
            counter = 1

        for s_list in query(s_list_list, filters=(lambda s_list :s_list.flag == 4 and s_list.reihenfolge == 1 and s_list.betrag != 0)):
            betrag6 = betrag6 + s_list.betrag
            counter = counter + 1

            if counter > 1:
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.nr = curr_nr

                if s_list.code > 0:
                    output_list.code = s_list.code
                else:
                    output_list.code = counter
                output_list.s = to_string("", "x(24)")

            if not long_digit:
                output_list.s = output_list.s + to_string(s_list.bezeich, "x(33)") + to_string(s_list.betrag, "->>>,>>>,>>9.99")
            else:
                output_list.s = output_list.s + to_string(s_list.bezeich, "x(33)") + to_string(s_list.betrag, "->>,>>>,>>>,>>9")

        if mi_opt_chk == False:
            output_list = Output_list()
            output_list_list.append(output_list)

            curr_nr = curr_nr + 1
            output_list.nr = curr_nr
            output_list = Output_list()
            output_list_list.append(output_list)

            curr_nr = curr_nr + 1
            output_list.nr = curr_nr
            output_list.s = to_string(translateExtended ("- Department Expenses", lvcarea, "") , "x(24)")
            counter = 0
        else:
            counter = 1

        for s_list in query(s_list_list, filters=(lambda s_list :s_list.flag == 5 and s_list.reihenfolge == 1 and s_list.betrag != 0)):
            betrag6 = betrag6 + s_list.betrag
            counter = counter + 1

            if counter > 1:
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.nr = curr_nr

                if s_list.code > 0:
                    output_list.code = s_list.code
                else:
                    output_list.code = counter
                output_list.s = to_string("", "x(24)")

            if not long_digit:
                output_list.s = output_list.s + to_string(s_list.bezeich, "x(33)") + to_string(s_list.betrag, "->>>,>>>,>>9.99")
            else:
                output_list.s = output_list.s + to_string(s_list.bezeich, "x(33)") + to_string(s_list.betrag, "->>,>>>,>>>,>>9")

        s_list = query(s_list_list, filters=(lambda s_list :s_list.reihenfolge == 2 and s_list.lager_nr == 9999), first=True)
        output_list = Output_list()
        output_list_list.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        output_list.s = to_string("", "x(24)")

        if not long_digit:
            output_list.s = output_list.s + to_string(s_list.l_bezeich, "x(33)") + to_string(s_list.anf_wert, "->>>,>>>,>>9.99")
        else:
            output_list.s = output_list.s + to_string(s_list.l_bezeich, "x(33)") + to_string(s_list.anf_wert, "->>,>>>,>>>,>>9")
        betrag6 = betrag6 + s_list.anf_wert

        if mi_opt_chk == False:
            output_list = Output_list()
            output_list_list.append(output_list)

            curr_nr = curr_nr + 1
            output_list.nr = curr_nr
        output_list = Output_list()
        output_list_list.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr

        if not long_digit:
            output_list.s = to_string("", "x(24)") + to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)") + to_string("", "x(15)") + to_string(betrag6, "->>>,>>>,>>9.99")
        else:
            output_list.s = to_string("", "x(24)") + to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)") + to_string("", "x(15)") + to_string(betrag6, "->>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_list.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        consume2 = betrag56 - betrag6
        output_list = Output_list()
        output_list_list.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr

        if not long_digit:
            output_list.s = to_string(translateExtended ("9. Net Consumption", lvcarea, "") , "x(24)") + to_string("(7 - 8)", "x(33)") + to_string("", "x(15)") + to_string(consume2, "->>>,>>>,>>9.99")
        else:
            output_list.s = to_string(translateExtended ("9. Net Consumption", lvcarea, "") , "x(24)") + to_string("(7 - 8)", "x(33)") + to_string("", "x(15)") + to_string(consume2, "->>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_list.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        output_list = Output_list()
        output_list_list.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        f_ratio = 0

        if tf_sales != 0:
            f_ratio = consume2 / tf_sales * 100

        if not long_digit:
            output_list.s = to_string(translateExtended ("Net food Sales", lvcarea, "") , "x(24)") + to_string("", "x(16)") + to_string(tf_sales, "->,>>>,>>>,>>9.99") + to_string(translateExtended ("     Cost:Sales", lvcarea, "") , "x(15)") + to_string(f_ratio, "->,>>>,>>9.99 %")
        else:
            output_list.s = to_string(translateExtended ("Net food Sales", lvcarea, "") , "x(24)") + to_string("", "x(16)") + to_string(tf_sales, " ->>>,>>>,>>>,>>9") + to_string(translateExtended ("     Cost:Sales", lvcarea, "") , "x(15)") + to_string(f_ratio, "->,>>>,>>9.99 %")
        done = True

    def create_beverage():

        nonlocal done, output_list_list, lvcarea, type_of_acct, counter, curr_nr, curr_reihe, coa_format, betrag, long_digit, htparam, h_artikel, l_besthis, gl_acct, l_lager, l_ophis, l_ophhis, hoteldpt, h_compli, exrate, artikel, gl_main, h_cost, l_artikel, umsatz
        nonlocal h_art, l_oh, gl_acct1


        nonlocal output_list, s_list, h_art, l_oh, gl_acct1
        nonlocal output_list_list, s_list_list

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
        fb_str[0] = translateExtended ("Beverage to food", lvcarea, "")
        fb_str[1] = translateExtended ("food to Beverage", lvcarea, "")
        H_art = H_artikel
        L_oh = L_besthis
        Gl_acct1 = Gl_acct
        s_list_list.clear()
        output_list_list.clear()
        curr_nr = 0
        curr_reihe = 0

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 862)).first()
        f_eknr = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 892)).first()
        b_eknr = htparam.finteger

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

            l_besthis_obj_list = []
            for l_besthis, l_oh in db_session.query(L_besthis, L_oh).join(L_oh,(L_oh.anf_best_dat == from_date) &  (L_oh.lager_nr == 0) &  (L_oh.artnr == L_besthis.artnr)).filter(
                    (L_besthis.anf_best_dat == from_date) &  (L_besthis.lager_nr == l_lager.lager_nr) &  (L_besthis.artnr >= 2000001) &  (L_besthis.artnr <= 2999999)).all():
                if l_besthis._recid in l_besthis_obj_list:
                    continue
                else:
                    l_besthis_obj_list.append(l_besthis._recid)


                qty1 = l_besthis.anz_anf_best + l_besthis.anz_eingang - l_besthis.anz_ausgang
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

                if l_oh.anz_anf_best != 0:
                    s_list.anf_wert = s_list.anf_wert + l_besthis.anz_anf_best * l_oh.val_anf_best / l_oh.anz_anf_best

                if qty != 0:
                    s_list.end_wert = s_list.end_wert + wert * qty1 / qty

                for l_ophis in db_session.query(L_ophis).filter(
                        (L_ophis.datum >= from_date) &  (L_ophis.datum <= to_date) &  (L_ophis.artnr == l_besthis.artnr) &  (L_ophis.op_art == 1) &  (L_ophis.lager_nr == l_lager.lager_nr) &  (not L_ophis.fibukonto.op("~")(".*;CANCELLED.*"))).all():

                    l_ophhis = db_session.query(L_ophhis).filter(
                            (L_ophhis.lscheinnr == l_ophis.lscheinnr) &  (func.lower(L_ophhis.op_typ) == "STI")).first()

                    if l_ophis.anzahl >= 0:

                        s_list = query(s_list_list, filters=(lambda s_list :s_list.lager_nr == l_lager.lager_nr and s_list.reihenfolge == flag and s_list.flag == 11), first=True)

                        if not s_list:
                            s_list = S_list()
                            s_list_list.append(s_list)

                            s_list.reihenfolge = flag
                            s_list.lager_nr = l_lager.lager_nr
                            s_list.l_bezeich = l_lager.bezeich
                            s_list.flag = 11
                        s_list.betrag = s_list.betrag + l_ophis.warenwert

                    elif l_ophis.anzahl < 0:

                        s_list = query(s_list_list, filters=(lambda s_list :s_list.lager_nr == l_lager.lager_nr and s_list.reihenfolge == flag and s_list.flag == 12), first=True)

                        if not s_list:
                            s_list = S_list()
                            s_list_list.append(s_list)

                            s_list.reihenfolge = flag
                            s_list.lager_nr = l_lager.lager_nr
                            s_list.l_bezeich = l_lager.bezeich
                            s_list.flag = 12
                        s_list.betrag = s_list.betrag + l_ophis.warenwert

                l_ophis_obj_list = []
                for l_ophis, gl_acct in db_session.query(L_ophis, Gl_acct).join(Gl_acct,(Gl_acct.fibukonto == L_ophis.fibukonto)).filter(
                        (L_ophis.datum >= from_date) &  (L_ophis.datum <= to_date) &  (L_ophis.artnr == l_besthis.artnr) &  (L_ophis.op_art == 3) &  (L_ophis.lager_nr == l_lager.lager_nr) &  (not L_ophis.fibukonto.op("~")(".*;CANCELLED.*"))).all():
                    if l_ophis._recid in l_ophis_obj_list:
                        continue
                    else:
                        l_ophis_obj_list.append(l_ophis._recid)


                    type_of_acct = gl_acct.acc_type

                    gl_main = db_session.query(Gl_main).filter(
                                (Gl_main.nr == gl_acct.main_nr)).first()
                    fibukonto = gl_acct.fibukonto
                    bezeich = to_string(gl_acct.fibukonto, coa_format) + " " + gl_acct.bezeich.upper()

                    if l_ophis.fibukonto != "":

                        gl_acct1 = db_session.query(Gl_acct1).filter(
                                    (Gl_acct1.fibukonto == l_ophis.fibukonto)).first()

                        if gl_acct1:
                            type_of_acct = gl_acct1.acc_type

                            gl_main = db_session.query(Gl_main).filter(
                                        (Gl_main.nr == gl_acct1.main_nr)).first()
                            fibukonto = gl_acct1.fibukonto
                            bezeich = to_string(gl_acct1.fibukonto, coa_format) + " " + gl_acct1.bezeich.upper()

                    if fibukonto.lower()  == (food_bev).lower() :
                        pass

                    elif fibukonto.lower()  == (bev_food).lower() :
                        pass
                    else:

                        if mi_opt_chk == False:

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
                            s_list.betrag = s_list.betrag + l_ophis.warenwert

        l_ophis_obj_list = []
        for l_ophis, l_artikel in db_session.query(L_ophis, L_artikel).join(L_artikel,(L_artikel.artnr == L_ophis.artnr) &  ((L_artikel.endkum == fl_eknr) |  (L_artikel.endkum == bl_eknr))).filter(
                (L_ophis.datum >= from_date) &  (L_ophis.datum <= to_date) &  ((func.lower(L_ophis.fibukonto) == (bev_food).lower()) |  (func.lower(L_ophis.fibukonto) == food_bev)) &  (L_ophis.op_art == 3) &  (notfunc.lower(func.lower(L_ophis.fibukonto)).op("~")(".*;CANCELLED.*"))).all():
            if l_ophis._recid in l_ophis_obj_list:
                continue
            else:
                l_ophis_obj_list.append(l_ophis._recid)

            if l_ophis.fibukonto.lower()  == (food_bev).lower()  and l_ophis.artnr >= 1000001 and l_ophis.artnr <= 1999999:

                s_list = query(s_list_list, filters=(lambda s_list :s_list.lager_nr == 9999 and s_list.reihenfolge == 2), first=True)
                s_list.anf_wert = s_list.anf_wert + l_ophis.warenwert

            elif l_ophis.fibukonto.lower()  == (bev_food).lower()  and l_ophis.artnr >= 1999999:

                s_list = query(s_list_list, filters=(lambda s_list :s_list.lager_nr == 9999 and s_list.reihenfolge == 1), first=True)
                s_list.anf_wert = s_list.anf_wert + l_ophis.warenwert

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

                    if h_cost.betrag == 1:
                        betrag = 0


                    else:
                        betrag = h_cost.betrag

                    if artikel.umsatzart == 6:
                        b_cost = h_compli.anzahl * betrag

                    elif artikel.umsatzart == 3 or artikel.umsatzart == 5:
                        f_cost = h_compli.anzahl * betrag

                elif not h_cost or (h_cost and h_cost.betrag == 0):

                    if artikel.umsatzart == 6:
                        b_cost = h_compli.anzahl * h_compli.epreis * h_artikel.prozent / 100 * rate

                    elif artikel.umsatzart == 3 or artikel.umsatzart == 5:
                        f_cost = h_compli.anzahl * h_compli.epreis * h_artikel.prozent / 100 * rate

                if b_cost != 0:

                    if mi_opt_chk == False:

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
        output_list = Output_list()
        output_list_list.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        output_list.s = to_string("", "x(24)") + to_string(translateExtended ("** BEVERAGE **", lvcarea, "") , "x(33)")
        output_list = Output_list()
        output_list_list.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        i = 0
        output_list = Output_list()
        output_list_list.append(output_list)

        betrag1 = 0
        output_list.s = to_string(translateExtended ("1. Opening Inventory", lvcarea, "") , "x(24)")

        for s_list in query(s_list_list, filters=(lambda s_list :s_list.flag == 0 and s_list.reihenfolge == 2 and s_list.lager_nr != 9999 and s_list.anf_wert != 0)):
            i = i + 1
            betrag1 = betrag1 + s_list.anf_wert

            if i > 1:
                output_list = Output_list()
                output_list_list.append(output_list)

                curr_nr = curr_nr + 1
                output_list.nr = curr_nr
                output_list.s = to_string("", "x(24)")

            if not long_digit:
                output_list.s = output_list.s + to_string(s_list.l_bezeich, "x(33)") + to_string(s_list.anf_wert, "->>>,>>>,>>9.99")
            else:
                output_list.s = output_list.s + to_string(s_list.l_bezeich, "x(33)") + to_string(s_list.anf_wert, "->>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_list.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr

        if not long_digit:
            output_list.s = to_string("", "x(24)") + to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)") + to_string("", "x(15)") + to_string(betrag1, "->>>,>>>,>>9.99")
        else:
            output_list.s = to_string("", "x(24)") + to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)") + to_string("", "x(15)") + to_string(betrag1, "->>,>>>,>>>,>>9")
        i = 0
        output_list = Output_list()
        output_list_list.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        output_list.s = to_string(translateExtended ("2. Incoming Stocks", lvcarea, "") , "x(24)")
        betrag2 = 0

        for s_list in query(s_list_list, filters=(lambda s_list :s_list.flag == 11 and s_list.reihenfolge == 2)):
            i = i + 1
            betrag2 = betrag2 + s_list.betrag

            if i > 1:
                output_list = Output_list()
                output_list_list.append(output_list)

                curr_nr = curr_nr + 1
                output_list.nr = curr_nr
                output_list.s = to_string("", "x(24)")

            if not long_digit:
                output_list.s = output_list.s + to_string(s_list.l_bezeich, "x(33)") + to_string(s_list.betrag, "->>>,>>>,>>9.99")
            else:
                output_list.s = output_list.s + to_string(s_list.l_bezeich, "x(33)") + to_string(s_list.betrag, "->>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_list.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr

        if not long_digit:
            output_list.s = to_string("", "x(24)") + to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)") + to_string("", "x(15)") + to_string(betrag2, "->>>,>>>,>>9.99")
        else:
            output_list.s = to_string("", "x(24)") + to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)") + to_string("", "x(15)") + to_string(betrag2, "->>,>>>,>>>,>>9")
        i = 0
        output_list = Output_list()
        output_list_list.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        output_list.s = to_string(translateExtended ("3. Returned Stocks", lvcarea, "") , "x(24)")
        betrag3 = 0

        for s_list in query(s_list_list, filters=(lambda s_list :s_list.flag == 12 and s_list.reihenfolge == 2)):
            i = i + 1
            betrag3 = betrag3 + s_list.betrag

            if i > 1:
                output_list = Output_list()
                output_list_list.append(output_list)

                curr_nr = curr_nr + 1
                output_list.nr = curr_nr
                output_list.s = to_string("", "x(24)")

            if not long_digit:
                output_list.s = output_list.s + to_string(s_list.l_bezeich, "x(33)") + to_string(s_list.betrag, "->>>,>>>,>>9.99")
            else:
                output_list.s = output_list.s + to_string(s_list.l_bezeich, "x(33)") + to_string(s_list.betrag, "->>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_list.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr

        if not long_digit:
            output_list.s = to_string("", "x(24)") + to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)") + to_string("", "x(15)") + to_string(betrag3, "->>>,>>>,>>9.99")
        else:
            output_list.s = to_string("", "x(24)") + to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)") + to_string("", "x(15)") + to_string(betrag3, "->>,>>>,>>>,>>9")

        s_list = query(s_list_list, filters=(lambda s_list :s_list.lager_nr == 9999 and s_list.reihenfolge == 2), first=True)
        output_list = Output_list()
        output_list_list.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr

        if not long_digit:
            output_list.s = to_string(("4. " + s_list.l_bezeich) , "x(24)") + to_string("", "x(33)") + to_string("", "x(15)") + to_string(s_list.anf_wert, "->>>,>>>,>>9.99")
        else:
            output_list.s = to_string(("4. " + s_list.l_bezeich) , "x(24)") + to_string("", "x(33)") + to_string("", "x(15)") + to_string(s_list.anf_wert, "->>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_list.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        betrag4 = betrag1 + betrag2 + betrag3 + s_list.anf_wert
        output_list = Output_list()
        output_list_list.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr

        if not long_digit:
            output_list.s = to_string(translateExtended ("5. Inventory Available", lvcarea, "") , "x(24)") + to_string("(1 + 2 + 3 + 4)", "x(33)") + to_string("", "x(15)") + to_string(betrag4, "->>>,>>>,>>9.99")
        else:
            output_list.s = to_string(translateExtended ("5. Inventory Available", lvcarea, "") , "x(24)") + to_string("(1 + 2 + 3 + 4)", "x(33)") + to_string("", "x(15)") + to_string(betrag4, "->>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_list.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        i = 0
        output_list = Output_list()
        output_list_list.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        output_list.s = to_string(translateExtended ("6. Closing Inventory", lvcarea, "") , "x(24)")
        betrag5 = 0

        for s_list in query(s_list_list, filters=(lambda s_list :s_list.flag == 0 and s_list.reihenfolge == 2 and s_list.lager_nr != 9999 and s_list.end_wert != 0)):
            i = i + 1
            betrag5 = betrag5 + s_list.end_wert

            if i > 1:
                output_list = Output_list()
                output_list_list.append(output_list)

                curr_nr = curr_nr + 1
                output_list.nr = curr_nr
                output_list.s = to_string("", "x(24)")

            if not long_digit:
                output_list.s = output_list.s + to_string(s_list.l_bezeich, "x(33)") + to_string(s_list.end_wert, "->>>,>>>,>>9.99")
            else:
                output_list.s = output_list.s + to_string(s_list.l_bezeich, "x(33)") + to_string(s_list.end_wert, "->>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_list.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr

        if not long_digit:
            output_list.s = to_string("", "x(24)") + to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)") + to_string("", "x(15)") + to_string(betrag5, "->>>,>>>,>>9.99")
        else:
            output_list.s = to_string("", "x(24)") + to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)") + to_string("", "x(15)") + to_string(betrag5, "->>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_list.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        betrag56 = betrag4 - betrag5

        if not long_digit:
            output_list.s = to_string(translateExtended ("7. Gross Consumption", lvcarea, "") , "x(24)") + to_string("(5 - 6)", "x(33)") + to_string("", "x(15)") + to_string(betrag56, "->>>,>>>,>>9.99")
        else:
            output_list.s = to_string(translateExtended ("7. Gross Consumption", lvcarea, "") , "x(24)") + to_string("(5 - 6)", "x(33)") + to_string("", "x(15)") + to_string(betrag56, "->>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_list.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        output_list = Output_list()
        output_list_list.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        output_list.s = to_string(translateExtended ("8. Credits", lvcarea, "") , "x(24)")
        betrag6 = 0

        if mi_opt_chk == False:
            output_list = Output_list()
            output_list_list.append(output_list)

            curr_nr = curr_nr + 1
            output_list.nr = curr_nr
            output_list.s = to_string(translateExtended ("- Compliment Cost", lvcarea, "") , "x(24)")
            counter = 0
        else:
            counter = 1

        for s_list in query(s_list_list, filters=(lambda s_list :s_list.flag == 4 and s_list.reihenfolge == 2 and s_list.betrag != 0)):
            betrag6 = betrag6 + s_list.betrag
            counter = counter + 1

            if counter > 1:
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.nr = curr_nr

                if s_list.code > 0:
                    output_list.code = s_list.code
                else:
                    output_list.code = counter
                output_list.s = to_string("", "x(24)")

            if not long_digit:
                output_list.s = output_list.s + to_string(s_list.bezeich, "x(33)") + to_string(s_list.betrag, "->>>,>>>,>>9.99")
            else:
                output_list.s = output_list.s + to_string(s_list.bezeich, "x(33)") + to_string(s_list.betrag, "->>,>>>,>>>,>>9")

        if mi_opt_chk == False:
            output_list = Output_list()
            output_list_list.append(output_list)

            curr_nr = curr_nr + 1
            output_list.nr = curr_nr
            output_list.s = to_string(translateExtended ("- Department Expenses", lvcarea, "") , "x(24)")
            counter = 0
        else:
            counter = 1

        for s_list in query(s_list_list, filters=(lambda s_list :s_list.flag == 5 and s_list.reihenfolge == 2 and s_list.betrag != 0)):
            counter = counter + 1
            betrag6 = betrag6 + s_list.betrag

            if counter > 1:
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.nr = curr_nr

                if s_list.code > 0:
                    output_list.code = s_list.code
                else:
                    output_list.code = counter
                output_list.s = to_string("", "x(24)")

            if not long_digit:
                output_list.s = output_list.s + to_string(s_list.bezeich, "x(33)") + to_string(s_list.betrag, "->>>,>>>,>>9.99")
            else:
                output_list.s = output_list.s + to_string(s_list.bezeich, "x(33)") + to_string(s_list.betrag, "->>,>>>,>>>,>>9")

        s_list = query(s_list_list, filters=(lambda s_list :s_list.reihenfolge == 1 and s_list.lager_nr == 9999), first=True)
        output_list = Output_list()
        output_list_list.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        output_list.s = to_string("", "x(24)")

        if not long_digit:
            output_list.s = output_list.s + to_string(s_list.l_bezeich, "x(33)") + to_string(s_list.anf_wert, "->>>,>>>,>>9.99")
        else:
            output_list.s = output_list.s + to_string(s_list.l_bezeich, "x(33)") + to_string(s_list.anf_wert, "->>,>>>,>>>,>>9")
        betrag6 = betrag6 + s_list.anf_wert

        if mi_opt_chk == False:
            output_list = Output_list()
            output_list_list.append(output_list)

            curr_nr = curr_nr + 1
            output_list.nr = curr_nr
        output_list = Output_list()
        output_list_list.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr

        if not long_digit:
            output_list.s = to_string("", "x(24)") + to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)") + to_string("", "x(15)") + to_string(betrag6, "->>>,>>>,>>9.99")
        else:
            output_list.s = to_string("", "x(24)") + to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)") + to_string("", "x(15)") + to_string(betrag6, "->>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_list.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        consume2 = betrag56 - betrag6
        output_list = Output_list()
        output_list_list.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr

        if not long_digit:
            output_list.s = to_string(translateExtended ("9. Net Consumption", lvcarea, "") , "x(24)") + to_string("(7 - 8)", "x(33)") + to_string("", "x(15)") + to_string(consume2, "->>>,>>>,>>9.99")
        else:
            output_list.s = to_string(translateExtended ("9. Net Consumption", lvcarea, "") , "x(24)") + to_string("(7 - 8)", "x(33)") + to_string("", "x(15)") + to_string(consume2, "->>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_list.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        output_list = Output_list()
        output_list_list.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        b_ratio = 0

        if tb_sales != 0:
            b_ratio = consume2 / tb_sales * 100

        if not long_digit:
            output_list.s = to_string(translateExtended ("Net Beverage Sales", lvcarea, "") , "x(24)") + to_string("", "x(16)") + to_string(tb_sales, "->,>>>,>>>,>>9.99") + to_string("     Cost:Sales", "x(15)") + to_string(b_ratio, "->,>>>,>>9.99 %")
        else:
            output_list.s = to_string(translateExtended ("Net Beverage Sales", lvcarea, "") , "x(24)") + to_string("", "x(16)") + to_string(tb_sales, " ->>>,>>>,>>>,>>9") + to_string(translateExtended ("     Cost:Sales", lvcarea, "") , "x(15)") + to_string(b_ratio, "->,>>>,>>9.99 %")
        done = True

    def fb_sales(f_eknr:int, b_eknr:int):

        nonlocal done, output_list_list, lvcarea, type_of_acct, counter, curr_nr, curr_reihe, coa_format, betrag, long_digit, htparam, h_artikel, l_besthis, gl_acct, l_lager, l_ophis, l_ophhis, hoteldpt, h_compli, exrate, artikel, gl_main, h_cost, l_artikel, umsatz
        nonlocal h_art, l_oh, gl_acct1


        nonlocal output_list, s_list, h_art, l_oh, gl_acct1
        nonlocal output_list_list, s_list_list

        tf_sales = 0
        tb_sales = 0
        f_sales:decimal = 0
        b_sales:decimal = 0
        h_service:decimal = 0
        h_mwst:decimal = 0
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
                    h_service = 0
                    h_mwst = 0
                    h_service, h_mwst = get_output(calc_servvat(umsatz.departement, umsatz.artnr, umsatz.datum, artikel.service_code, artikel.mwst_code))
                    amount = umsatz.betrag / (1 + h_service + h_mwst)

                    if artikel.endkum == f_eknr or artikel.umsatzart == 3 or artikel.umsatzart == 5:

                        if umsatz.datum == date2:
                            f_sales = f_sales + amount
                        tf_sales = tf_sales + amount

                    elif artikel.endkum == b_eknr or artikel.umsatzart == 6:

                        if umsatz.datum == date2:
                            b_sales = b_sales + amount
                        tb_sales = tb_sales + amount


        return generate_inner_output()


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 246)).first()
    long_digit = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 977)).first()
    coa_format = htparam.fchar

    if from_grp == 0:
        create_list()

    elif from_grp == food:
        create_food()

    elif from_grp == bev:
        create_beverage()

    return generate_output()