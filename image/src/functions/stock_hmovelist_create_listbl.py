from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Htparam, Bediener, L_ophis, L_besthis, L_lager, L_lieferant, Gl_acct, L_ophhis

def stock_hmovelist_create_listbl(pvilanguage:int, s_artnr:int, mm:int, yy:int, from_lager:int, to_lager:int, show_price:bool):
    anfdate = None
    enddate = None
    str_list_list = []
    lvcarea:str = "fb_flash1"
    tot_anz:decimal = 0
    tot_val:decimal = 0
    t_anz:decimal = 0
    t_val:decimal = 0
    long_digit:bool = False
    htparam = bediener = l_ophis = l_besthis = l_lager = l_lieferant = gl_acct = l_ophhis = None

    str_list = usr = l_op1 = l_oh = None

    str_list_list, Str_list = create_model("Str_list", {"s":str})

    Usr = Bediener
    L_op1 = L_ophis
    L_oh = L_besthis

    db_session = local_storage.db_session

    def generate_output():
        nonlocal anfdate, enddate, str_list_list, lvcarea, tot_anz, tot_val, t_anz, t_val, long_digit, htparam, bediener, l_ophis, l_besthis, l_lager, l_lieferant, gl_acct, l_ophhis
        nonlocal usr, l_op1, l_oh


        nonlocal str_list, usr, l_op1, l_oh
        nonlocal str_list_list
        return {"anfdate": anfdate, "enddate": enddate, "str-list": str_list_list}

    def create_list():

        nonlocal anfdate, enddate, str_list_list, lvcarea, tot_anz, tot_val, t_anz, t_val, long_digit, htparam, bediener, l_ophis, l_besthis, l_lager, l_lieferant, gl_acct, l_ophhis
        nonlocal usr, l_op1, l_oh


        nonlocal str_list, usr, l_op1, l_oh
        nonlocal str_list_list

        t_qty:decimal = 0
        t_wert:decimal = 0
        bemerk:str = ""
        preis:decimal = 0
        wert:decimal = 0
        Usr = Bediener
        L_op1 = L_ophis
        L_oh = L_besthis
        anfdate = date_mdy(mm, 1, yy)
        enddate = anfdate + 31
        enddate = date_mdy(get_month(enddate) , 1, get_year(enddate)) - 1

        l_oh = db_session.query(L_oh).filter(
                (L_oh.artnr == s_artnr) &  (L_oh.lager_nr == 0) &  (L_oh.anf_best_dat == anfdate)).first()

        if l_oh:
            t_qty = l_oh.anz_anf_best + l_oh.anz_eingang - l_oh.anz_ausgang

            if show_price:
                t_wert = l_oh.val_anf_best + l_oh.wert_eingang - l_oh.wert_ausgang
        str_list_list.clear()
        tot_anz = 0
        tot_val = 0

        for l_lager in db_session.query(L_lager).filter(
                (L_lager.lager_nr >= from_lager) &  (L_lager.lager_nr <= to_lager)).all():

            l_besthis = db_session.query(L_besthis).filter(
                    (L_besthis.lager_nr == l_lager.lager_nr) &  (L_besthis.artnr == s_artnr) &  (L_besthis.anf_best_dat == anfdate)).first()

            if l_besthis:
                t_anz = l_besthis.anz_anf_best

                if show_price:
                    t_val = l_besthis.val_anf_best
                str_list = Str_list()
                str_list_list.append(str_list)

                str_list.s = "        " + to_string(l_lager.lager_nr, "99") + " " + to_string(l_lager.bezeich, "x(13)")
                str_list = Str_list()
                str_list_list.append(str_list)


                if show_price:

                    if not long_digit:
                        str_list.s = to_string(l_besthis.anf_best_dat) + to_string(" ", "x(16)") + to_string(l_besthis.anz_anf_best, "->>>,>>9.99") + to_string(l_besthis.val_anf_best, "->>>,>>>,>>9.99")
                    else:
                        str_list.s = to_string(l_besthis.anf_best_dat) + to_string(" ", "x(16)") + to_string(l_besthis.anz_anf_best, "->>>,>>9.99") + to_string(l_besthis.val_anf_best, "->>,>>>,>>>,>>9")
                else:

                    if not long_digit:
                        str_list.s = to_string(l_besthis.anf_best_dat) + to_string(" ", "x(16)") + to_string(l_besthis.anz_anf_best, "->>>,>>9.99") + to_string(0, "->>>,>>>,>>9.99")
                    else:
                        str_list.s = to_string(l_besthis.anf_best_dat) + to_string(" ", "x(16)") + to_string(l_besthis.anz_anf_best, "->>>,>>9.99") + to_string(0, "->>,>>>,>>>,>>9")

            for l_ophis in db_session.query(L_ophis).filter(
                    (L_ophis.lager_nr == l_lager.lager_nr) &  (L_ophis.artnr == s_artnr) &  (L_ophis.datum >= anfdate) &  (L_ophis.datum <= enddate) &  (not L_ophis.fibukonto.op("~")(".*;CANCELLED.*"))).all():

                if show_price:
                    preis = l_ophis.einzelpreis
                    wert = l_ophis.warenwert

                if l_ophis.op_art == 1:
                    bemerk = ""

                    l_lieferant = db_session.query(L_lieferant).filter(
                            (L_lieferant.lief_nr == l_ophis.lief_nr)).first()

                    if l_lieferant:
                        bemerk = l_lieferant.firma
                    t_anz = t_anz + l_ophis.anzahl
                    t_val = t_val + wert
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    add_id()
                    str_list.s = to_string(l_ophis.datum) + to_string(l_ophis.lscheinnr, "x(16)") + to_string(0, "->>>,>>9.99") + to_string(0, "->>>,>>>,>>9.99") + to_string(l_ophis.anzahl, "->,>>>,>>9.99") + to_string(wert, "->>,>>>,>>9.99") + to_string(0, "->,>>>,>>9.99") + to_string(0, "->>,>>>,>>9.99") + to_string(0, "->>>,>>9.99") + to_string(bemerk, "x(16)")

                elif l_ophis.op_art == 2:

                    l_op1 = db_session.query(L_op1).filter(
                            (L_op1.op_art == 4) &  (L_op1.datum == l_ophis.datum) &  (L_op1.artnr == l_ophis.artnr) &  (L_op1.anzahl == l_ophis.anzahl) &  (L_op1.lief_nr == l_ophis.lager_nr)).first()

                    if l_op1:
                        bemerk = translateExtended ("From", lvcarea, "") + " " + to_string(l_op1.lager_nr)
                    else:
                        bemerk = translateExtended ("Transferred", lvcarea, "")
                    t_anz = t_anz + l_ophis.anzahl
                    t_val = t_val + wert
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    add_id()
                    str_list.s = to_string(l_ophis.datum) + to_string(l_ophis.lscheinnr, "x(16)") + to_string(0, "->>>,>>9.99") + to_string(0, "->>>,>>>,>>9.99") + to_string(l_ophis.anzahl, "->,>>>,>>9.99") + to_string(wert, "->>,>>>,>>9.99") + to_string(0, "->,>>>,>>9.99") + to_string(0, "->>,>>>,>>9.99") + to_string(0, "->>>,>>9.99") + to_string(bemerk, "x(16)")

                elif l_ophis.op_art == 3:

                    if l_ophis.fibukonto != "":

                        gl_acct = db_session.query(Gl_acct).filter(
                                (Gl_acct.fibukonto == l_ophis.fibukonto)).first()
                    else:

                        l_ophhis = db_session.query(L_ophhis).filter(
                                (func.lower(L_ophhis.op_typ) == "STT") &  (L_ophhis.datum == l_ophis.datum) &  (L_ophhis.lscheinnr == l_ophis.lscheinnr) &  (L_ophhis.fibukonto != "")).first()

                        if l_ophhis:

                            gl_acct = db_session.query(Gl_acct).filter(
                                    (Gl_acct.fibukonto == l_ophhis.fibukonto)).first()
                    bemerk = ""

                    if gl_acct:
                        bemerk = gl_acct.fibukonto
                    t_anz = t_anz - l_ophis.anzahl
                    t_val = t_val - wert
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    add_id()

                    if not long_digit:
                        str_list.s = to_string(l_ophis.datum) + to_string(l_ophis.lscheinnr, "x(16)") + to_string(0, "->>>,>>9.99") + to_string(0, "->>>,>>>,>>9.99") + to_string(0, "->,>>>,>>9.99") + to_string(0, "->>,>>>,>>9.99") + to_string(l_ophis.anzahl, "->,>>>,>>9.99") + to_string(wert, "->>,>>>,>>9.99") + to_string(0, "->>>,>>9.99") + to_string(bemerk, "x(16)")
                    else:
                        str_list.s = to_string(l_ophis.datum) + to_string(l_ophis.lscheinnr, "x(16)") + to_string(0, "->>>,>>9.99") + to_string(0, "   ->>>,>>>,>>9") + to_string(0, "->,>>>,>>9.99") + to_string(0, "->,>>>,>>>,>>9") + to_string(l_ophis.anzahl, "->,>>>,>>9.99") + to_string(wert, "->,>>>,>>>,>>9") + to_string(0, "->>,>>>,>>9") + to_string(bemerk, "x(16)")

                elif l_ophis.op_art == 4:
                    bemerk = translateExtended ("To Store", lvcarea, "") + " " + to_string(l_ophis.lief_nr)
                    t_anz = t_anz - l_ophis.anzahl
                    t_val = t_val - wert
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    add_id()
                    str_list.s = to_string(l_ophis.datum) + to_string(l_ophis.lscheinnr, "x(16)") + to_string(0, "->>>,>>9.99") + to_string(0, "->>>,>>>,>>9.99") + to_string(0, "->,>>>,>>9.99") + to_string(0, "->>,>>>,>>9.99") + to_string(l_ophis.anzahl, "->,>>>,>>9.99") + to_string(wert, "->>,>>>,>>9.99") + to_string(0, "->>>,>>9.99") + to_string(bemerk, "x(16)")

            if l_besthis:
                tot_anz = tot_anz + t_anz
                tot_val = tot_val + t_val
                str_list = Str_list()
                str_list_list.append(str_list)


                if not long_digit:
                    str_list.s = "        " + to_string(translateExtended ("Stock Onhand:", lvcarea, "") , "x(16)") + to_string(t_anz, "->>>,>>9.99") + to_string(t_val, "->>>,>>>,>>9.99")
                else:
                    str_list.s = "        " + to_string(translateExtended ("Stock Onhand:", lvcarea, "") , "x(16)") + to_string(t_anz, "->>>,>>9.99") + to_string(t_val, "   ->>>,>>>,>>9")
                str_list = Str_list()
                str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.s = "        " + "T O T A L :     " + to_string(t_qty, "->>>,>>9.99") + to_string(t_wert, "->>>,>>>,>>9.99")

    def add_id():

        nonlocal anfdate, enddate, str_list_list, lvcarea, tot_anz, tot_val, t_anz, t_val, long_digit, htparam, bediener, l_ophis, l_besthis, l_lager, l_lieferant, gl_acct, l_ophhis
        nonlocal usr, l_op1, l_oh


        nonlocal str_list, usr, l_op1, l_oh
        nonlocal str_list_list


        Usr = Bediener

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 246)).first()
    long_digit = htparam.flogical
    create_list()

    return generate_output()