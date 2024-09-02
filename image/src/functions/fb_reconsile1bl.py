from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from functions.calc_servvat import calc_servvat
from models import Htparam, H_artikel, Gl_acct, L_bestand, L_lager, L_artikel, L_op, L_ophdr, Gl_main, H_compli, Hoteldpt, Exrate, Artikel, H_cost, Umsatz

def fb_reconsile1bl(pvilanguage:int, from_grp:int, food:int, bev:int, from_date:date, to_date:date, date1:date, date2:date, mi_opt_chk:bool, double_currency:bool, exchg_rate:decimal, foreign_nr:int):
    done = False
    output_list_list = []
    counter:int = 0
    output_counter:int = 0
    coa_format:str = ""
    lvcarea:str = "fb_reconsile1"
    type_of_acct:int = 0
    long_digit:bool = False
    htparam = h_artikel = gl_acct = l_bestand = l_lager = l_artikel = l_op = l_ophdr = gl_main = h_compli = hoteldpt = exrate = artikel = h_cost = umsatz = None

    s_list = s1_list = output_list = h_art = gl_acct1 = l_oh = l_oh1 = None

    s_list_list, S_list = create_model("S_list", {"code":int, "reihenfolge":int, "lager_nr":int, "l_bezeich":str, "fibukonto":str, "bezeich":str, "flag":int, "anf_wert":decimal, "end_wert":decimal, "betrag":decimal}, {"reihenfolge": 1, "flag": 2})
    output_list_list, Output_list = create_model("Output_list", {"curr_counter":int, "nr":int, "store":int, "amount":decimal, "bezeich":str, "s":str})

    S1_list = S_list
    s1_list_list = s_list_list

    H_art = H_artikel
    Gl_acct1 = Gl_acct
    L_oh = L_bestand
    L_oh1 = L_bestand

    db_session = local_storage.db_session

    def generate_output():
        nonlocal done, output_list_list, counter, output_counter, coa_format, lvcarea, type_of_acct, long_digit, htparam, h_artikel, gl_acct, l_bestand, l_lager, l_artikel, l_op, l_ophdr, gl_main, h_compli, hoteldpt, exrate, artikel, h_cost, umsatz
        nonlocal s1_list, h_art, gl_acct1, l_oh, l_oh1


        nonlocal s_list, s1_list, output_list, h_art, gl_acct1, l_oh, l_oh1
        nonlocal s_list_list, output_list_list
        return {"done": done, "output-list": output_list_list}

    def create_food():

        nonlocal done, output_list_list, counter, output_counter, coa_format, lvcarea, type_of_acct, long_digit, htparam, h_artikel, gl_acct, l_bestand, l_lager, l_artikel, l_op, l_ophdr, gl_main, h_compli, hoteldpt, exrate, artikel, h_cost, umsatz
        nonlocal s1_list, h_art, gl_acct1, l_oh, l_oh1


        nonlocal s_list, s1_list, output_list, h_art, gl_acct1, l_oh, l_oh1
        nonlocal s_list_list, output_list_list

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
        net_cost:decimal = 0
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
        onhand:decimal = 0
        fibukonto:str = ""
        bezeich:str = ""
        netcost_flag:bool = False
        tot_foodcost:decimal = 0
        H_art = H_artikel
        Gl_acct1 = Gl_acct
        L_oh = L_bestand
        L_oh1 = L_bestand
        output_list_list.clear()

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
        create_output_list()
        output_list.s = to_string("", "x(24)") + to_string(translateExtended ("** food **", lvcarea, "") , "x(33)")
        flag = 1

        for l_lager in db_session.query(L_lager).filter(
                (L_lager.betriebsnr > 0)).all():
            s_list_list.clear()
            betrag1 = 0
            betrag2 = 0
            betrag3 = 0
            betrag4 = 0
            betrag5 = 0
            betrag6 = 0
            net_cost = 0

            gl_acct = db_session.query(Gl_acct).filter(
                    (func.lower(Gl_acct.fibukonto) == (bev_food).lower())).first()
            s_list = S_list()
            s_list_list.append(s_list)

            s_list.reihenfolge = 1
            s_list.lager_nr = 9999
            s_list.l_bezeich = to_string(gl_acct.fibukonto, coa_format) + " " +\
                    gl_acct.bezeich.upper()
            s_list.flag = 0

            gl_acct = db_session.query(Gl_acct).filter(
                    (func.lower(Gl_acct.fibukonto) == (food_bev).lower())).first()
            s_list = S_list()
            s_list_list.append(s_list)

            s_list.reihenfolge = 2
            s_list.lager_nr = 9999
            s_list.l_bezeich = to_string(gl_acct.fibukonto, coa_format) + " " +\
                    gl_acct.bezeich.upper()
            s_list.flag = 0


            create_output_list()
            create_output_list()
            output_list.s = to_string("", "x(24)") + to_string(l_lager.lager_nr, "99 ") + to_string(l_lager.bezeich, "x(30)")

            l_bestand_obj_list = []
            for l_bestand, l_oh, l_artikel in db_session.query(L_bestand, L_oh, L_artikel).join(L_oh,(L_oh.artnr == L_bestand.artnr) &  (L_oh.lager_nr == 0)).join(L_artikel,(L_artikel.artnr == L_bestand.artnr) &  (L_artikel.endkum == fl_eknr)).filter(
                    (L_bestand.lager_nr == l_lager.lager_nr)).all():
                if l_bestand._recid in l_bestand_obj_list:
                    continue
                else:
                    l_bestand_obj_list.append(l_bestand._recid)


                qty1 = l_bestand.anz_anf_best + l_bestand.anz_eingang -\
                        l_bestand.anz_ausgang
                qty = l_oh.anz_anf_best + l_oh.anz_eingang -\
                        l_oh.anz_ausgang
                wert = l_oh.val_anf_best + l_oh.wert_eingang -\
                        l_oh.wert_ausgang

                s_list = query(s_list_list, filters=(lambda s_list :s_list.lager_nr == l_lager.lager_nr and s_list.reihenfolge == flag and s_list.flag == 0), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_list.append(s_list)

                    s_list.reihenfolge = flag
                    s_list.lager_nr = l_lager.lager_nr
                    s_list.l_bezeich = l_lager.bezeich
                    s_list.flag = 0

                s1_list = query(s1_list_list, filters=(lambda s1_list :s1_list.lager_nr == l_lager.lager_nr and s1_list.reihenfolge == flag and s1_list.flag == 1), first=True)

                if not s1_list:
                    s1_list = S1_list()
                    s1_list_list.append(s1_list)

                    s1_list.flag = 1
                    s1_list.reihenfolge = flag
                    s1_list.lager_nr = l_lager.lager_nr
                    s1_list.l_bezeich = l_lager.bezeich

                if l_oh.anz_anf_best != 0:
                    s_list.anf_wert = s_list.anf_wert + l_bestand.anz_anf_best *\
                            l_oh.val_anf_best / l_oh.anz_anf_best
                    s1_list.anf_wert = s1_list.anf_wert + l_bestand.anz_anf_best *\
                        (l_artikel.vk_preis - l_oh.val_anf_best / l_oh.anz_anf_best)

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

                            s_list.flag = 11
                            s_list.reihenfolge = flag
                            s_list.lager_nr = l_lager.lager_nr
                            s_list.l_bezeich = l_lager.bezeich


                        s_list.betrag = s_list.betrag + l_op.warenwert

                    elif l_op.anzahl < 0:

                        s_list = query(s_list_list, filters=(lambda s_list :s_list.lager_nr == l_lager.lager_nr and s_list.reihenfolge == flag and s_list.flag == 12), first=True)

                        if not s_list:
                            s_list = S_list()
                            s_list_list.append(s_list)

                            s_list.flag = 12
                            s_list.reihenfolge = flag
                            s_list.lager_nr = l_lager.lager_nr
                            s_list.l_bezeich = l_lager.bezeich


                        s_list.betrag = s_list.betrag + l_op.warenwert

                for l_op in db_session.query(L_op).filter(
                        (L_op.datum >= from_date) &  (L_op.datum <= to_date) &  (L_op.artnr == l_artikel.artnr) &  (L_op.loeschflag <= 1) &  (L_op.op_art == 3) &  (L_op.pos > 0) &  (L_op.lager_nr == l_lager.lager_nr)).all():

                    if substring(l_op.stornogrund, 0, 8) == "00000000":
                        net_cost = net_cost + l_op.warenwert
                    else:

                        gl_acct1 = db_session.query(Gl_acct1).filter(
                                (Gl_acct1.fibukonto == l_op.stornogrund)).first()

                        if gl_acct1:
                            fibukonto = gl_acct1.fibukonto
                            bezeich = to_string(gl_acct1.fibukonto, coa_format) + " " +\
                                    gl_acct1.bezeich.upper()
                            type_of_acct = gl_acct1.acc_type

                            gl_main = db_session.query(Gl_main).filter(
                                    (Gl_main.nr == gl_acct1.main_nr)).first()

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

                                    s_list.flag = 5
                                    s_list.reihenfolge = flag
                                    s_list.fibukonto = fibukonto
                                    s_list.bezeich = bezeich


                            else:

                                s_list = query(s_list_list, filters=(lambda s_list :s_list.code == gl_main.code and s_list.reihenfolge == flag and s_list.flag == 5), first=True)

                                if not s_list:
                                    s_list = S_list()
                                    s_list_list.append(s_list)

                                    s_list.flag = 5
                                    s_list.reihenfolge = flag
                                    s_list.code = gl_main.CODE
                                    s_list.bezeich = gl_main.bezeich

                            if type_of_acct == 5 or type_of_acct == 3 or type_of_acct == 4:
                                s_list.betrag = s_list.betrag + l_op.warenwert
            s_list = S_list()
            s_list_list.append(s_list)

            s_list.flag = 111
            s_list.reihenfolge = flag
            s_list.lager_nr = l_lager.lager_nr
            s_list.l_bezeich = l_lager.bezeich

            l_op_obj_list = []
            for l_op, l_artikel in db_session.query(L_op, L_artikel).join(L_artikel,(L_artikel.artnr == L_op.artnr) &  (L_artikel.endkum == fl_eknr)).filter(
                    (L_op.datum >= from_date) &  (L_op.datum <= to_date) &  (L_op.loeschflag <= 1) &  (L_op.op_art == 4) &  (L_op.herkunftflag == 1) &  ((L_op.lager_nr == l_lager.lager_nr) |  (L_op.pos == l_lager.lager_nr))).all():
                if l_op._recid in l_op_obj_list:
                    continue
                else:
                    l_op_obj_list.append(l_op._recid)

                if l_op.lager_nr == l_lager.lager_nr:
                    s_list.betrag = s_list.betrag - l_op.warenwert

                if l_op.pos == l_lager.lager_nr:
                    s_list.betrag = s_list.betrag + l_op.warenwert
            s_list = S_list()
            s_list_list.append(s_list)

            s_list.flag = 112
            s_list.reihenfolge = flag
            s_list.lager_nr = l_lager.lager_nr
            s_list.bezeich = "KITCHEN TRANSFER IN"


            s_list = S_list()
            s_list_list.append(s_list)

            s_list.flag = 113
            s_list.reihenfolge = flag
            s_list.lager_nr = l_lager.lager_nr
            s_list.bezeich = "KITCHEN TRANSFER OUT"

            for h_compli in db_session.query(H_compli).filter(
                    (H_compli.datum >= from_date) &  (H_compli.datum <= to_date) &  (H_compli.betriebsnr > 0) &  (H_compli.p_artnr == 1)).all():

                hoteldpt = db_session.query(Hoteldpt).filter(
                        (Hoteldpt.num == h_compli.betriebsnr)).first()

                if hoteldpt and hoteldpt.betriebsnr == l_lager.lager_nr:

                    s_list = query(s_list_list, filters=(lambda s_list :s_list.flag == 112), first=True)
                    s_list.betrag = s_list.betrag + h_compli.epreis
                else:

                    hoteldpt = db_session.query(Hoteldpt).filter(
                            (Hoteldpt.num == h_compli.departement)).first()

                    if hoteldpt and hoteldpt.betriebsnr == l_lager.lager_nr:

                        s_list = query(s_list_list, filters=(lambda s_list :s_list.flag == 113), first=True)
                        s_list.betrag = s_list.betrag - h_compli.epreis

            l_op_obj_list = []
            for l_op, l_artikel in db_session.query(L_op, L_artikel).join(L_artikel,(L_artikel.artnr == L_op.artnr) &  ((L_artikel.endkum == fl_eknr) |  (L_artikel.endkum == bl_eknr))).filter(
                    (L_op.op_art == 3) &  (L_op.loeschflag <= 1) &  (L_op.datum >= date1) &  (L_op.datum <= date2) &  ((func.lower(L_op.stornogrund) == (bev_food).lower()) |  (func.lower(L_op.stornogrund) == food_bev)) &  (L_op.lager_nr == l_lager.lager_nr)).all():
                if l_op._recid in l_op_obj_list:
                    continue
                else:
                    l_op_obj_list.append(l_op._recid)

                if l_op.stornogrund.lower()  == (food_bev).lower() :

                    s_list = query(s_list_list, filters=(lambda s_list :s_list.lager_nr == 9999 and s_list.reihenfolge == 2), first=True)
                    s_list.anf_wert = s_list.anf_wert + l_op.warenwert

                elif l_op.stornogrund.lower()  == (bev_food).lower() :

                    s_list = query(s_list_list, filters=(lambda s_list :s_list.lager_nr == 9999 and s_list.reihenfolge == 1), first=True)
                    s_list.anf_wert = s_list.anf_wert + l_op.warenwert

            for hoteldpt in db_session.query(Hoteldpt).filter(
                    (Hoteldpt.num > 0) &  ((Hoteldpt.num == l_lager.betriebsnr) |  (Hoteldpt.betriebsnr == l_lager.lager_nr))).all():

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

                        if artikel.endkum == b_eknr:
                            b_cost = h_compli.anzahl * h_cost.betrag

                        elif artikel.endkum == f_eknr:
                            f_cost = h_compli.anzahl * h_cost.betrag

                        if artikel.endkum == f_eknr:
                            tot_foodcost = tot_foodcost + f_cost

                    elif not h_cost or (h_cost and h_cost.betrag == 0):

                        if artikel.endkum == b_eknr:
                            b_cost = h_compli.anzahl * h_compli.epreis * h_artikel.prozent / 100 * rate

                        elif artikel.endkum == f_eknr:
                            f_cost = h_compli.anzahl * h_compli.epreis * h_artikel.prozent / 100 * rate

                        if artikel.endkum == f_eknr:
                            tot_foodcost = tot_foodcost + f_cost

                    if f_cost != 0:

                        if mi_opt_chk == False:

                            s_list = query(s_list_list, filters=(lambda s_list :s_list.fibukonto == gl_acct.fibukonto and s_list.reihenfolge == 1 and s_list.flag == 4), first=True)

                            if not s_list:
                                s_list = S_list()
                                s_list_list.append(s_list)

                                s_list.flag = 4
                                s_list.reihenfolge = flag
                                s_list.fibukonto = gl_acct.fibukonto
                                s_list.bezeich = to_string(gl_acct.fibukonto, coa_format) + " " +\
                                        gl_acct.bezeich.upper()


                        else:

                            s_list = query(s_list_list, filters=(lambda s_list :s_list.code == gl_main.code and s_list.reihenfolge == 1 and s_list.flag == 4), first=True)

                            if not s_list:
                                s_list = S_list()
                                s_list_list.append(s_list)

                                s_list.flag = 4
                                s_list.reihenfolge = 1
                                s_list.code = gl_main.CODE
                                s_list.bezeich = gl_main.bezeich


                        s_list.betrag = s_list.betrag + f_cost

            if l_lager.betriebsnr != 0:
                tf_sales, tb_sales = fb_sales(f_eknr, b_eknr)
            i = 0
            onhand = 0
            create_output_list()
            output_list.s = to_string(translateExtended ("1. Opening Inventory", lvcarea, "") , "x(24)")

            s_list = query(s_list_list, filters=(lambda s_list :s_list.flag == 0 and s_list.reihenfolge == flag and s_list.lager_nr != 9999 and s_list.anf_wert != 0), first=True)

            if s_list:
                onhand = s_list.anf_wert
            i = i + 1
            betrag1 = betrag1 + onhand

            if not long_digit:
                output_list.s = output_list.s + to_string("", "x(33)") + to_string(onhand, "->>>,>>>,>>9.99")
            else:
                output_list.s = output_list.s + to_string("", "x(33)") + to_string(onhand, "->>,>>>,>>>,>>9")
            i = 0
            onhand = 0

            s_list = query(s_list_list, filters=(lambda s_list :s_list.flag == 1 and s_list.reihenfolge == flag and s_list.lager_nr != 9999 and s_list.anf_wert != 0), first=True)

            if s_list:
                onhand = s_list.anf_wert
            i = i + 1
            betrag1 = betrag1 + onhand
            create_output_list()
            output_list.s = to_string(translateExtended ("   OpenInv Adjustment", lvcarea, "") , "x(24)") +\
                    to_string("", "x(33)")
            output_list.nr = 1
            output_list.store = l_lager.lager_nr
            output_list.amount = onhand

            if not long_digit:
                output_list.s = output_list.s + to_string(onhand, "->>>,>>>,>>9.99")
            else:
                output_list.s = output_list.s + to_string(onhand, "->>,>>>,>>>,>>9")
            i = 0
            onhand = 0
            create_output_list()
            output_list.s = to_string(translateExtended ("2. Incoming Stocks", lvcarea, "") , "x(24)")

            s_list = query(s_list_list, filters=(lambda s_list :s_list.flag == 11 and s_list.reihenfolge == flag), first=True)

            if s_list:
                onhand = s_list.betrag
            i = i + 1
            betrag2 = betrag2 + onhand

            if not long_digit:
                output_list.s = output_list.s + to_string("", "x(33)") + to_string(onhand, "->>>,>>>,>>9.99")
            else:
                output_list.s = output_list.s + to_string("", "x(33)") + to_string(onhand, "->>,>>>,>>>,>>9")
            i = 0
            onhand = 0
            create_output_list()
            output_list.s = to_string(translateExtended ("3. Returned Stocks", lvcarea, "") , "x(24)")

            s_list = query(s_list_list, filters=(lambda s_list :s_list.flag == 12 and s_list.reihenfolge == flag), first=True)

            if s_list:
                onhand = s_list.betrag
            i = i + 1
            betrag3 = betrag3 + onhand

            if not long_digit:
                output_list.s = output_list.s + to_string("", "x(33)") + to_string(onhand, "->>>,>>>,>>9.99")
            else:
                output_list.s = output_list.s + to_string("", "x(33)") + to_string(onhand, "->>,>>>,>>>,>>9")
            i = 0
            create_output_list()
            output_list.s = to_string(translateExtended ("4. Store Transfer", lvcarea, "") , "x(24)")

            for s_list in query(s_list_list, filters=(lambda s_list :s_list.flag == 111 and s_list.reihenfolge == flag)):
                i = i + 1
                betrag2 = betrag2 + s_list.betrag

                if not long_digit:
                    output_list.s = output_list.s + to_string("", "x(33)") + to_string(s_list.betrag, "->>>,>>>,>>9.99")
                else:
                    output_list.s = output_list.s + to_string("", "x(33)") + to_string(s_list.betrag, "->>,>>>,>>>,>>9")
            i = 0
            create_output_list()
            output_list.s = to_string(translateExtended ("5. Kitchen Transfer In", lvcarea, "") , "x(24)")

            for s_list in query(s_list_list, filters=(lambda s_list :s_list.flag == 112 and s_list.reihenfolge == flag)):
                i = i + 1
                betrag2 = betrag2 + s_list.betrag

                if not long_digit:
                    output_list.s = output_list.s + to_string("", "x(33)") + to_string(s_list.betrag, "->>>,>>>,>>9.99")
                else:
                    output_list.s = output_list.s + to_string("", "x(33)") + to_string(s_list.betrag, "->>,>>>,>>>,>>9")
            i = 0
            create_output_list()
            output_list.s = to_string(translateExtended ("   Kitchen Transfer Out", lvcarea, "") , "x(24)")

            for s_list in query(s_list_list, filters=(lambda s_list :s_list.flag == 113 and s_list.reihenfolge == flag)):
                i = i + 1
                betrag2 = betrag2 + s_list.betrag

                if not long_digit:
                    output_list.s = output_list.s + to_string("", "x(33)") + to_string(s_list.betrag, "->>>,>>>,>>9.99")
                else:
                    output_list.s = output_list.s + to_string("", "x(33)") + to_string(s_list.betrag, "->>,>>>,>>>,>>9")

            s_list = query(s_list_list, filters=(lambda s_list :s_list.lager_nr == 9999 and s_list.reihenfolge == flag), first=True)
            create_output_list()
            output_list.s = to_string(("6. " + s_list.l_bezeich) , "x(24)") + to_string("", "x(33)")

            if not long_digit:
                output_list.s = output_list.s + to_string(s_list.anf_wert, "->>>,>>>,>>9.99")
            else:
                output_list.s = output_list.s + to_string(s_list.anf_wert, "->>,>>>,>>>,>>9")
            betrag4 = betrag1 + betrag2 + betrag3 + s_list.anf_wert
            create_output_list()
            output_list.s = to_string(translateExtended ("7. Inventory Available", lvcarea, "") , "x(24)") +\
                    to_string("(1 + 2 + 3 + 4 + 5 + 6)", "x(33)") +\
                    to_string("", "x(15)")
            output_list.nr = 2
            output_list.store = l_lager.lager_nr
            output_list.amount = betrag4

            if not long_digit:
                output_list.s = output_list.s + to_string(betrag4, "->>>,>>>,>>9.99")
            else:
                output_list.s = output_list.s + to_string(betrag4, "->>,>>>,>>>,>>9")
            i = 0
            onhand = 0
            create_output_list()
            output_list.s = to_string(translateExtended ("8. Closing Inventory", lvcarea, "") , "x(24)")

            s_list = query(s_list_list, filters=(lambda s_list :s_list.flag == 0 and s_list.reihenfolge == flag and s_list.lager_nr != 9999 and s_list.end_wert != 0), first=True)

            if s_list:
                onhand = s_list.end_wert
            i = i + 1
            betrag5 = betrag5 + onhand

            if not long_digit:
                output_list.s = output_list.s + to_string("", "x(33)") + to_string("", "x(15)") + to_string(onhand, "->>>,>>>,>>9.99")
            else:
                output_list.s = output_list.s + to_string("", "x(33)") + to_string(onhand, "->>,>>>,>>>,>>9")
            create_output_list()
            betrag56 = betrag4 - betrag5
            output_list.s = to_string(translateExtended ("9. Tot. Cost Consumption", lvcarea, "") , "x(24)") +\
                    to_string("(7 - 8)", "x(33)") + to_string("", "x(15)")
            output_list.nr = 3
            output_list.store = l_lager.lager_nr
            output_list.amount = betrag56

            if not long_digit:
                output_list.s = output_list.s + to_string(betrag56, "->>>,>>>,>>9.99")
            else:
                output_list.s = output_list.s + to_string(betrag56, "->>,>>>,>>>,>>9")
            create_output_list()
            output_list.s = to_string(translateExtended ("10 Less by Expenses", lvcarea, "") , "x(24)")
            create_output_list()
            output_list.s = to_string(translateExtended ("-  Compliment Cost", lvcarea, "") , "x(24)")
            counter = 0

            for s_list in query(s_list_list, filters=(lambda s_list :s_list.flag == 4 and s_list.reihenfolge == flag and s_list.betrag != 0)):
                betrag6 = betrag6 + s_list.betrag
                counter = counter + 1

                if counter > 1:
                    create_output_list()
                    output_list.s = to_string("", "x(24)")

                if not long_digit:
                    output_list.s = output_list.s + to_string(s_list.bezeich, "x(33)") + to_string(s_list.betrag, "->>>,>>>,>>9.99")
                else:
                    output_list.s = output_list.s + to_string(s_list.bezeich, "x(33)") + to_string(s_list.betrag, "->>,>>>,>>>,>>9")
            create_output_list()
            output_list.s = to_string(translateExtended ("-  Department Expenses", lvcarea, "") , "x(24)")
            counter = 0

            for s_list in query(s_list_list, filters=(lambda s_list :s_list.flag == 5 and s_list.reihenfolge == flag and s_list.betrag != 0)):
                betrag6 = betrag6 + s_list.betrag
                counter = counter + 1

                if counter > 1:
                    create_output_list()
                    output_list.s = to_string("", "x(24)")

                if not long_digit:
                    output_list.s = output_list.s + to_string(s_list.bezeich, "x(33)") + to_string(s_list.betrag, "->>>,>>>,>>9.99")
                else:
                    output_list.s = output_list.s + to_string(s_list.bezeich, "x(33)") + to_string(s_list.betrag, "->>,>>>,>>>,>>9")

            s_list = query(s_list_list, filters=(lambda s_list :s_list.reihenfolge == 2 and s_list.lager_nr == 9999), first=True)
            create_output_list()
            output_list.s = to_string("", "x(24)")

            if not long_digit:
                output_list.s = output_list.s + to_string(s_list.l_bezeich, "x(33)") + to_string(s_list.anf_wert, "->>>,>>>,>>9.99")
            else:
                output_list.s = output_list.s + to_string(s_list.l_bezeich, "x(33)") + to_string(s_list.anf_wert, "->>,>>>,>>>,>>9")
            betrag6 = betrag6 + s_list.anf_wert
            create_output_list()

            if not long_digit:
                output_list.s = to_string("", "x(24)") + to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)") + to_string("", "x(15)") + to_string(betrag6, "->>>,>>>,>>9.99")
            else:
                output_list.s = to_string("", "x(24)") + to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)") + to_string("", "x(15)") + to_string(betrag6, "->>,>>>,>>>,>>9")
            consume2 = betrag56 - betrag6
            create_output_list()

            if not long_digit:
                output_list.s = to_string(translateExtended ("11 Net Cost Consumed", lvcarea, "") , "x(24)") + to_string("(9 - 10)", "x(33)") + to_string("", "x(15)") + to_string(consume2, "->>>,>>>,>>9.99")
            else:
                output_list.s = to_string("11 Net Cost Consumed", "x(24)") + to_string("(9 - 10)", "x(33)") + to_string("", "x(15)") + to_string(consume2, "->>,>>>,>>>,>>9")
            create_output_list()
            f_ratio = 0

            if tf_sales != 0:
                f_ratio = consume2 / tf_sales * 100

            if not long_digit:
                output_list.s = to_string(translateExtended (">> Net food Sales", lvcarea, "") , "x(24)") + to_string("", "x(16)") + to_string(tf_sales, "->,>>>,>>>,>>9.99") + to_string("     Cost:Sales", "x(15)") + to_string(f_ratio, "->,>>>,>>9.99 %")
            else:
                output_list.s = to_string("Net food Sales", "x(24)") + to_string("", "x(16)") + to_string(tf_sales, " ->>>,>>>,>>>,>>9") + to_string("     Cost:Sales", "x(15)") + to_string(f_ratio, "->,>>>,>>9.99 %")
        done = True

    def create_beverage():

        nonlocal done, output_list_list, counter, output_counter, coa_format, lvcarea, type_of_acct, long_digit, htparam, h_artikel, gl_acct, l_bestand, l_lager, l_artikel, l_op, l_ophdr, gl_main, h_compli, hoteldpt, exrate, artikel, h_cost, umsatz
        nonlocal s1_list, h_art, gl_acct1, l_oh, l_oh1


        nonlocal s_list, s1_list, output_list, h_art, gl_acct1, l_oh, l_oh1
        nonlocal s_list_list, output_list_list

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
        net_cost:decimal = 0
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
        onhand:decimal = 0
        fibukonto:str = ""
        bezeich:str = ""
        H_art = H_artikel
        L_oh = L_bestand
        L_oh1 = L_bestand
        Gl_acct1 = Gl_acct
        output_list_list.clear()

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
        create_output_list()
        output_list.s = to_string("", "x(24)") + to_string(translateExtended ("** BEVERAGE **", lvcarea, "") , "x(33)")
        flag = 2

        for l_lager in db_session.query(L_lager).filter(
                (L_lager.betriebsnr > 0)).all():
            s_list_list.clear()
            betrag1 = 0
            betrag2 = 0
            betrag3 = 0
            betrag4 = 0
            betrag5 = 0
            betrag6 = 0
            net_cost = 0

            gl_acct = db_session.query(Gl_acct).filter(
                    (func.lower(Gl_acct.fibukonto) == (bev_food).lower())).first()
            s_list = S_list()
            s_list_list.append(s_list)

            s_list.reihenfolge = 1
            s_list.lager_nr = 9999
            s_list.l_bezeich = to_string(gl_acct.fibukonto, coa_format) + " " +\
                    gl_acct.bezeich.upper()
            s_list.flag = 0

            gl_acct = db_session.query(Gl_acct).filter(
                    (func.lower(Gl_acct.fibukonto) == (food_bev).lower())).first()
            s_list = S_list()
            s_list_list.append(s_list)

            s_list.reihenfolge = 2
            s_list.lager_nr = 9999
            s_list.l_bezeich = to_string(gl_acct.fibukonto, coa_format) + " " +\
                    gl_acct.bezeich.upper()
            s_list.flag = 0


            create_output_list()
            create_output_list()
            output_list.s = to_string("", "x(24)") + to_string(l_lager.lager_nr, "99 ") + to_string(l_lager.bezeich, "x(30)")

            l_bestand_obj_list = []
            for l_bestand, l_oh, l_artikel in db_session.query(L_bestand, L_oh, L_artikel).join(L_oh,(L_oh.artnr == L_bestand.artnr) &  (L_oh.lager_nr == 0)).join(L_artikel,(L_artikel.artnr == L_bestand.artnr) &  (L_artikel.endkum == bl_eknr)).filter(
                    (L_bestand.lager_nr == l_lager.lager_nr)).all():
                if l_bestand._recid in l_bestand_obj_list:
                    continue
                else:
                    l_bestand_obj_list.append(l_bestand._recid)


                qty1 = l_bestand.anz_anf_best + l_bestand.anz_eingang -\
                        l_bestand.anz_ausgang
                qty = l_oh.anz_anf_best + l_oh.anz_eingang -\
                        l_oh.anz_ausgang
                wert = l_oh.val_anf_best + l_oh.wert_eingang -\
                        l_oh.wert_ausgang

                s_list = query(s_list_list, filters=(lambda s_list :s_list.lager_nr == l_lager.lager_nr and s_list.reihenfolge == flag and s_list.flag == 0), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_list.append(s_list)

                    s_list.reihenfolge = flag
                    s_list.lager_nr = l_lager.lager_nr
                    s_list.l_bezeich = l_lager.bezeich
                    s_list.flag = 0

                s1_list = query(s1_list_list, filters=(lambda s1_list :s1_list.lager_nr == l_lager.lager_nr and s1_list.reihenfolge == flag and s1_list.flag == 1), first=True)

                if not s1_list:
                    s1_list = S1_list()
                    s1_list_list.append(s1_list)

                    s1_list.flag = 1
                    s1_list.reihenfolge = flag
                    s1_list.lager_nr = l_lager.lager_nr
                    s1_list.l_bezeich = l_lager.bezeich

                if l_oh.anz_anf_best != 0:
                    s_list.anf_wert = s_list.anf_wert + l_bestand.anz_anf_best *\
                            l_oh.val_anf_best / l_oh.anz_anf_best
                    s1_list.anf_wert = s1_list.anf_wert + l_bestand.anz_anf_best *\
                        (l_artikel.vk_preis - l_oh.val_anf_best / l_oh.anz_anf_best)

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

                            s_list.flag = 11
                            s_list.reihenfolge = flag
                            s_list.lager_nr = l_lager.lager_nr
                            s_list.l_bezeich = l_lager.bezeich


                        s_list.betrag = s_list.betrag + l_op.warenwert

                    elif l_op.anzahl < 0:

                        s_list = query(s_list_list, filters=(lambda s_list :s_list.lager_nr == l_lager.lager_nr and s_list.reihenfolge == flag and s_list.flag == 12), first=True)

                        if not s_list:
                            s_list = S_list()
                            s_list_list.append(s_list)

                            s_list.flag = 12
                            s_list.reihenfolge = flag
                            s_list.lager_nr = l_lager.lager_nr
                            s_list.l_bezeich = l_lager.bezeich


                        s_list.betrag = s_list.betrag + l_op.warenwert

                for l_op in db_session.query(L_op).filter(
                        (L_op.datum >= from_date) &  (L_op.datum <= to_date) &  (L_op.artnr == l_artikel.artnr) &  (L_op.loeschflag <= 1) &  (L_op.op_art == 3) &  (L_op.pos > 0) &  (L_op.lager_nr == l_lager.lager_nr)).all():

                    if substring(l_op.stornogrund, 0, 8) == "00000000":
                        net_cost = net_cost + l_op.warenwert
                    else:

                        gl_acct1 = db_session.query(Gl_acct1).filter(
                                (Gl_acct1.fibukonto == l_op.stornogrund)).first()

                        if gl_acct1:
                            fibukonto = gl_acct1.fibukonto
                            bezeich = to_string(gl_acct1.fibukonto, coa_format) + " " +\
                                    gl_acct1.bezeich.upper()
                            type_of_acct = gl_acct1.acc_type


                            pass

                            gl_main = db_session.query(Gl_main).filter(
                                    (Gl_main.nr == gl_acct1.main_nr)).first()

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

                                    s_list.flag = 5
                                    s_list.reihenfolge = flag
                                    s_list.fibukonto = fibukonto
                                    s_list.bezeich = bezeich


                            else:

                                s_list = query(s_list_list, filters=(lambda s_list :s_list.code == gl_main.code and s_list.reihenfolge == flag and s_list.flag == 5), first=True)

                                if not s_list:
                                    s_list = S_list()
                                    s_list_list.append(s_list)

                                    s_list.flag = 5
                                    s_list.reihenfolge = flag
                                    s_list.code = gl_main.CODE
                                    s_list.bezeich = gl_main.bezeich

                            if type_of_acct == 5 or type_of_acct == 3 or type_of_acct == 4:
                                s_list.betrag = s_list.betrag + l_op.warenwert
            s_list = S_list()
            s_list_list.append(s_list)

            s_list.flag = 111
            s_list.reihenfolge = flag
            s_list.lager_nr = l_lager.lager_nr
            s_list.l_bezeich = l_lager.bezeich

            l_op_obj_list = []
            for l_op, l_artikel in db_session.query(L_op, L_artikel).join(L_artikel,(L_artikel.artnr == L_op.artnr) &  (L_artikel.endkum == bl_eknr)).filter(
                    (L_op.datum >= from_date) &  (L_op.datum <= to_date) &  (L_op.loeschflag <= 1) &  (L_op.op_art == 4) &  (L_op.herkunftflag == 1) &  ((L_op.lager_nr == l_lager.lager_nr) |  (L_op.pos == l_lager.lager_nr))).all():
                if l_op._recid in l_op_obj_list:
                    continue
                else:
                    l_op_obj_list.append(l_op._recid)

                if l_op.lager_nr == l_lager.lager_nr:
                    s_list.betrag = s_list.betrag - l_op.warenwert

                if l_op.pos == l_lager.lager_nr:
                    s_list.betrag = s_list.betrag + l_op.warenwert
            s_list = S_list()
            s_list_list.append(s_list)

            s_list.flag = 112
            s_list.reihenfolge = flag
            s_list.lager_nr = l_lager.lager_nr
            s_list.bezeich = "KITCHEN TRANSFER IN"


            s_list = S_list()
            s_list_list.append(s_list)

            s_list.reihenfolge = flag
            s_list.lager_nr = l_lager.lager_nr
            s_list.bezeich = "KITCHEN TRANSFER OUT"
            s_list.flag = 113

            for h_compli in db_session.query(H_compli).filter(
                    (H_compli.datum >= from_date) &  (H_compli.datum <= to_date) &  (H_compli.betriebsnr > 0) &  (H_compli.p_artnr == 2)).all():

                hoteldpt = db_session.query(Hoteldpt).filter(
                        (Hoteldpt.num == h_compli.betriebsnr)).first()

                if hoteldpt and hoteldpt.betriebsnr == l_lager.lager_nr:

                    s_list = query(s_list_list, filters=(lambda s_list :s_list.flag == 112), first=True)
                    s_list.betrag = s_list.betrag + h_compli.epreis
                else:

                    hoteldpt = db_session.query(Hoteldpt).filter(
                            (Hoteldpt.num == h_compli.departement)).first()

                    if hoteldpt and hoteldpt.betriebsnr == l_lager.lager_nr:

                        s_list = query(s_list_list, filters=(lambda s_list :s_list.flag == 113), first=True)
                        s_list.betrag = s_list.betrag - h_compli.epreis

            l_op_obj_list = []
            for l_op, l_artikel in db_session.query(L_op, L_artikel).join(L_artikel,(L_artikel.artnr == L_op.artnr) &  ((L_artikel.endkum == fl_eknr) |  (L_artikel.endkum == bl_eknr))).filter(
                    (L_op.op_art == 3) &  (L_op.loeschflag <= 1) &  (L_op.datum >= date1) &  (L_op.datum <= date2) &  ((func.lower(L_op.stornogrund) == (bev_food).lower()) |  (func.lower(L_op.stornogrund) == food_bev)) &  (L_op.lager_nr == l_lager.lager_nr)).all():
                if l_op._recid in l_op_obj_list:
                    continue
                else:
                    l_op_obj_list.append(l_op._recid)

                if l_op.stornogrund.lower()  == (food_bev).lower() :

                    s_list = query(s_list_list, filters=(lambda s_list :s_list.lager_nr == 9999 and s_list.reihenfolge == 2), first=True)
                    s_list.anf_wert = s_list.anf_wert + l_op.warenwert

                elif l_op.stornogrund.lower()  == (bev_food).lower() :

                    s_list = query(s_list_list, filters=(lambda s_list :s_list.lager_nr == 9999 and s_list.reihenfolge == 1), first=True)
                    s_list.anf_wert = s_list.anf_wert + l_op.warenwert

            for hoteldpt in db_session.query(Hoteldpt).filter(
                    (Hoteldpt.num > 0) &  ((Hoteldpt.num == l_lager.betriebsnr) |  (Hoteldpt.betriebsnr == l_lager.lager_nr))).all():

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

                        if artikel.endkum == b_eknr:
                            b_cost = h_compli.anzahl * h_cost.betrag

                        elif artikel.endkum == f_eknr:
                            f_cost = h_compli.anzahl * h_cost.betrag

                    elif not h_cost or (h_cost and h_cost.betrag == 0):

                        if artikel.endkum == b_eknr:
                            b_cost = h_compli.anzahl * h_compli.epreis * h_artikel.prozent / 100 * rate

                        elif artikel.endkum == f_eknr:
                            f_cost = h_compli.anzahl * h_compli.epreis * h_artikel.prozent / 100 * rate

                    if b_cost != 0:

                        if mi_opt_chk == False:

                            s_list = query(s_list_list, filters=(lambda s_list :s_list.fibukonto == gl_acct.fibukonto and s_list.reihenfolge == flag and s_list.flag == 4), first=True)

                            if not s_list:
                                s_list = S_list()
                                s_list_list.append(s_list)

                                s_list.flag = 4
                                s_list.reihenfolge = flag
                                s_list.fibukonto = gl_acct.fibukonto
                                s_list.bezeich = to_string(gl_acct.fibukonto, coa_format) + " " +\
                                        gl_acct.bezeich.upper()


                        else:

                            s_list = query(s_list_list, filters=(lambda s_list :s_list.code == gl_main.code and s_list.reihenfolge == 2 and s_list.flag == 4), first=True)

                            if not s_list:
                                s_list = S_list()
                                s_list_list.append(s_list)

                                s_list.flag = 4
                                s_list.reihenfolge = 2
                                s_list.code = gl_main.CODE
                                s_list.bezeich = gl_main.bezeich


                        s_list.betrag = s_list.betrag + b_cost

            if l_lager.betriebsnr != 0:
                tf_sales, tb_sales = fb_sales(f_eknr, b_eknr)
            i = 0
            onhand = 0
            create_output_list()
            output_list.s = to_string(translateExtended ("1. Opening Inventory", lvcarea, "") , "x(24)")

            s_list = query(s_list_list, filters=(lambda s_list :s_list.flag == 0 and s_list.reihenfolge == flag and s_list.lager_nr != 9999 and s_list.anf_wert != 0), first=True)

            if s_list:
                onhand = s_list.anf_wert
            i = i + 1
            betrag1 = betrag1 + onhand

            if not long_digit:
                output_list.s = output_list.s + to_string("", "x(33)") + to_string(onhand, "->>>,>>>,>>9.99")
            else:
                output_list.s = output_list.s + to_string("", "x(33)") + to_string(onhand, "->>,>>>,>>>,>>9")
            i = 0
            onhand = 0

            s_list = query(s_list_list, filters=(lambda s_list :s_list.flag == 1 and s_list.reihenfolge == flag and s_list.lager_nr != 9999 and s_list.anf_wert != 0), first=True)

            if s_list:
                onhand = s_list.anf_wert
            i = i + 1
            betrag1 = betrag1 + onhand
            create_output_list()
            output_list.s = to_string(translateExtended ("   OpenInv Adjustment", lvcarea, "") , "x(24)") +\
                    to_string("", "x(33)")
            output_list.nr = 1
            output_list.store = l_lager.lager_nr
            output_list.amount = onhand

            if not long_digit:
                output_list.s = output_list.s + to_string(onhand, "->>>,>>>,>>9.99")
            else:
                output_list.s = output_list.s + to_string(onhand, "->>,>>>,>>>,>>9")
            i = 0
            onhand = 0
            create_output_list()
            output_list.s = to_string(translateExtended ("2. Incoming Stocks", lvcarea, "") , "x(24)")

            s_list = query(s_list_list, filters=(lambda s_list :s_list.flag == 11 and s_list.reihenfolge == flag), first=True)

            if s_list:
                onhand = s_list.betrag
            i = i + 1
            betrag2 = betrag2 + onhand

            if not long_digit:
                output_list.s = output_list.s + to_string("", "x(33)") + to_string(onhand, "->>>,>>>,>>9.99")
            else:
                output_list.s = output_list.s + to_string("", "x(33)") + to_string(onhand, "->>,>>>,>>>,>>9")
            i = 0
            onhand = 0
            create_output_list()
            output_list.s = to_string(translateExtended ("3. Returned Stocks", lvcarea, "") , "x(24)")

            s_list = query(s_list_list, filters=(lambda s_list :s_list.flag == 12 and s_list.reihenfolge == flag), first=True)

            if s_list:
                onhand = s_list.betrag
            i = i + 1
            betrag3 = betrag3 + onhand

            if not long_digit:
                output_list.s = output_list.s + to_string("", "x(33)") + to_string(onhand, "->>>,>>>,>>9.99")
            else:
                output_list.s = output_list.s + to_string("", "x(33)") + to_string(onhand, "->>,>>>,>>>,>>9")
            i = 0
            create_output_list()
            output_list.s = to_string(translateExtended ("4. Store Transfer", lvcarea, "") , "x(24)")

            for s_list in query(s_list_list, filters=(lambda s_list :s_list.flag == 111 and s_list.reihenfolge == flag)):
                i = i + 1
                betrag2 = betrag2 + s_list.betrag

                if not long_digit:
                    output_list.s = output_list.s + to_string("", "x(33)") + to_string(s_list.betrag, "->>>,>>>,>>9.99")
                else:
                    output_list.s = output_list.s + to_string("", "x(33)") + to_string(s_list.betrag, "->>,>>>,>>>,>>9")
            i = 0
            create_output_list()
            output_list.s = to_string(translateExtended ("5. Kitchen Transfer In", lvcarea, "") , "x(24)")

            for s_list in query(s_list_list, filters=(lambda s_list :s_list.flag == 112 and s_list.reihenfolge == flag)):
                i = i + 1
                betrag2 = betrag2 + s_list.betrag

                if not long_digit:
                    output_list.s = output_list.s + to_string("", "x(33)") + to_string(s_list.betrag, "->>>,>>>,>>9.99")
                else:
                    output_list.s = output_list.s + to_string("", "x(33)") + to_string(s_list.betrag, "->>,>>>,>>>,>>9")
            i = 0
            create_output_list()
            output_list.s = to_string(translateExtended ("   Kitchen Transfer Out", lvcarea, "") , "x(24)")

            for s_list in query(s_list_list, filters=(lambda s_list :s_list.flag == 113 and s_list.reihenfolge == flag)):
                i = i + 1
                betrag2 = betrag2 + s_list.betrag

                if not long_digit:
                    output_list.s = output_list.s + to_string("", "x(33)") + to_string(s_list.betrag, "->>>,>>>,>>9.99")
                else:
                    output_list.s = output_list.s + to_string("", "x(33)") + to_string(s_list.betrag, "->>,>>>,>>>,>>9")

            s_list = query(s_list_list, filters=(lambda s_list :s_list.lager_nr == 9999 and s_list.reihenfolge == 2), first=True)
            create_output_list()
            output_list.s = to_string(("6. " + s_list.l_bezeich) , "x(24)") + to_string("", "x(33)")

            if not long_digit:
                output_list.s = output_list.s + to_string(s_list.anf_wert, "->>>,>>>,>>9.99")
            else:
                output_list.s = output_list.s + to_string(s_list.anf_wert, "->>,>>>,>>>,>>9")
            betrag4 = betrag1 + betrag2 + betrag3 + s_list.anf_wert
            create_output_list()
            output_list.s = to_string(translateExtended ("7. Inventory Available", lvcarea, "") , "x(24)") +\
                    to_string("(1 + 2 + 3 + 4 + 5 + 6)", "x(33)") +\
                    to_string("", "x(15)")
            output_list.nr = 2
            output_list.store = l_lager.lager_nr
            output_list.amount = betrag4

            if not long_digit:
                output_list.s = output_list.s + to_string(betrag4, "->>>,>>>,>>9.99")
            else:
                output_list.s = output_list.s + to_string(betrag4, "->>,>>>,>>>,>>9")
            i = 0
            onhand = 0
            create_output_list()
            output_list.s = to_string(translateExtended ("8. Closing Inventory", lvcarea, "") , "x(24)")

            s_list = query(s_list_list, filters=(lambda s_list :s_list.flag == 0 and s_list.reihenfolge == flag and s_list.lager_nr != 9999 and s_list.end_wert != 0), first=True)

            if s_list:
                onhand = s_list.end_wert
            i = i + 1
            betrag5 = betrag5 + onhand

            if not long_digit:
                output_list.s = output_list.s + to_string("", "x(33)") + to_string("", "x(15)") + to_string(onhand, "->>>,>>>,>>9.99")
            else:
                output_list.s = output_list.s + to_string("", "x(33)") + to_string(onhand, "->>,>>>,>>>,>>9")
            create_output_list()
            betrag56 = betrag4 - betrag5
            output_list.s = to_string(translateExtended ("9. Tot. Cost Consumption", lvcarea, "") , "x(24)") +\
                    to_string("(7 - 8)", "x(33)") + to_string("", "x(15)")
            output_list.nr = 3
            output_list.store = l_lager.lager_nr
            output_list.amount = betrag56

            if not long_digit:
                output_list.s = output_list.s + to_string(betrag56, "->>>,>>>,>>9.99")
            else:
                output_list.s = output_list.s + to_string(betrag56, "->>,>>>,>>>,>>9")
            create_output_list()
            output_list.s = to_string(translateExtended ("10 Less by Expenses", lvcarea, "") , "x(24)")
            create_output_list()
            output_list.s = to_string(translateExtended ("-  Compliment Cost", lvcarea, "") , "x(24)")
            counter = 0

            for s_list in query(s_list_list, filters=(lambda s_list :s_list.flag == 4 and s_list.reihenfolge == flag and s_list.betrag != 0)):
                betrag6 = betrag6 + s_list.betrag
                counter = counter + 1

                if counter > 1:
                    create_output_list()
                    output_list.s = to_string("", "x(24)")

                if not long_digit:
                    output_list.s = output_list.s + to_string(s_list.bezeich, "x(33)") + to_string(s_list.betrag, "->>>,>>>,>>9.99")
                else:
                    output_list.s = output_list.s + to_string(s_list.bezeich, "x(33)") + to_string(s_list.betrag, "->>,>>>,>>>,>>9")
            create_output_list()
            output_list.s = to_string(translateExtended ("-  Department Expenses", lvcarea, "") , "x(24)")
            counter = 0

            for s_list in query(s_list_list, filters=(lambda s_list :s_list.flag == 5 and s_list.reihenfolge == flag and s_list.betrag != 0)):
                betrag6 = betrag6 + s_list.betrag
                counter = counter + 1

                if counter > 1:
                    create_output_list()
                    output_list.s = to_string("", "x(24)")

                if not long_digit:
                    output_list.s = output_list.s + to_string(s_list.bezeich, "x(33)") + to_string(s_list.betrag, "->>>,>>>,>>9.99")
                else:
                    output_list.s = output_list.s + to_string(s_list.bezeich, "x(33)") + to_string(s_list.betrag, "->>,>>>,>>>,>>9")

            s_list = query(s_list_list, filters=(lambda s_list :s_list.reihenfolge == 1 and s_list.lager_nr == 9999), first=True)
            create_output_list()
            output_list.s = to_string("", "x(24)")

            if not long_digit:
                output_list.s = output_list.s + to_string(s_list.l_bezeich, "x(33)") + to_string(s_list.anf_wert, "->>>,>>>,>>9.99")
            else:
                output_list.s = output_list.s + to_string(s_list.l_bezeich, "x(33)") + to_string(s_list.anf_wert, "->>,>>>,>>>,>>9")
            betrag6 = betrag6 + s_list.anf_wert
            create_output_list()

            if not long_digit:
                output_list.s = to_string("", "x(24)") + to_string("", "x(24)") + to_string("SUB TOTAL", "x(9)") + to_string("", "x(15)") + to_string(betrag6, "->>>,>>>,>>9.99")
            else:
                output_list.s = to_string("", "x(24)") + to_string("", "x(24)") + to_string("SUB TOTAL", "x(9)") + to_string("", "x(15)") + to_string(betrag6, "->>,>>>,>>>,>>9")
            consume2 = betrag56 - betrag6
            create_output_list()

            if not long_digit:
                output_list.s = to_string(translateExtended ("11 Net Cost Consumed", lvcarea, "") , "x(24)") + to_string("(9 - 10)", "x(33)") + to_string("", "x(15)") + to_string(consume2, "->>>,>>>,>>9.99")
            else:
                output_list.s = to_string(translateExtended ("11 Net Cost Consumed", lvcarea, "") , "x(24)") + to_string("(9 - 10)", "x(33)") + to_string("", "x(15)") + to_string(consume2, "->>,>>>,>>>,>>9")
            create_output_list()
            b_ratio = 0

            if tb_sales != 0:
                b_ratio = consume2 / tb_sales * 100

            if not long_digit:
                output_list.s = to_string(translateExtended (">> Net Beverage Sales", lvcarea, "") , "x(24)") + to_string("", "x(16)") + to_string(tb_sales, "->,>>>,>>>,>>9.99") + to_string(translateExtended ("     Cost:Sales", lvcarea, "") , "x(15)") + to_string(b_ratio, "->,>>>,>>9.99 %")
            else:
                output_list.s = to_string(translateExtended ("Net Beverage Sales", lvcarea, "") , "x(24)") + to_string("", "x(16)") + to_string(tb_sales, " ->>>,>>>,>>>,>>9") + to_string(translateExtended ("     Cost:Sales", lvcarea, "") , "x(15)") + to_string(b_ratio, "->,>>>,>>9.99 %")
        done = True

    def fb_sales(f_eknr:int, b_eknr:int):

        nonlocal done, output_list_list, counter, output_counter, coa_format, lvcarea, type_of_acct, long_digit, htparam, h_artikel, gl_acct, l_bestand, l_lager, l_artikel, l_op, l_ophdr, gl_main, h_compli, hoteldpt, exrate, artikel, h_cost, umsatz
        nonlocal s1_list, h_art, gl_acct1, l_oh, l_oh1


        nonlocal s_list, s1_list, output_list, h_art, gl_acct1, l_oh, l_oh1
        nonlocal s_list_list, output_list_list

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
                ((Hoteldpt.num == l_lager.betriebsnr) |  (Hoteldpt.betriebsnr == l_lager.lager_nr))).all():

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

    if from_grp == food:
        create_food()

    elif from_grp == bev:
        create_beverage()
    output_counter = output_counter + 1
    output_list = Output_list()
    output_list_list.append(output_list)

    output_list.curr_counter = output_counter

    return generate_output()