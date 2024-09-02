from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Htparam, L_artikel, Bediener, L_bestand, L_op, L_ophdr, L_lager, L_lieferant, Gl_acct, L_ophis

def stock_movelist_btn_gobl(pvilanguage:int, s_artnr:int, show_price:bool, from_lager:int, to_lager:int):
    str_list_list = []
    tot_anz:decimal = 0
    tot_val:decimal = 0
    t_anz:decimal = 0
    t_val:decimal = 0
    long_digit:bool = False
    lvcarea:str = "stock_movelist"
    htparam = l_artikel = bediener = l_bestand = l_op = l_ophdr = l_lager = l_lieferant = gl_acct = l_ophis = None

    str_list = usr = l_oh = l_op1 = buf_ophdr = None

    str_list_list, Str_list = create_model("Str_list", {"s":str, "id":str})

    Usr = Bediener
    L_oh = L_bestand
    L_op1 = L_op
    Buf_ophdr = L_ophdr

    db_session = local_storage.db_session

    def generate_output():
        nonlocal str_list_list, tot_anz, tot_val, t_anz, t_val, long_digit, lvcarea, htparam, l_artikel, bediener, l_bestand, l_op, l_ophdr, l_lager, l_lieferant, gl_acct, l_ophis
        nonlocal usr, l_oh, l_op1, buf_ophdr


        nonlocal str_list, usr, l_oh, l_op1, buf_ophdr
        nonlocal str_list_list
        return {"str-list": str_list_list}

    def create_list():

        nonlocal str_list_list, tot_anz, tot_val, t_anz, t_val, long_digit, lvcarea, htparam, l_artikel, bediener, l_bestand, l_op, l_ophdr, l_lager, l_lieferant, gl_acct, l_ophis
        nonlocal usr, l_oh, l_op1, buf_ophdr


        nonlocal str_list, usr, l_oh, l_op1, buf_ophdr
        nonlocal str_list_list

        t_qty:decimal = 0
        t_wert:decimal = 0
        bemerk:str = ""
        close_date:date = None
        preis:decimal = 0
        wert:decimal = 0
        it_exist:bool = False
        last_date:date = None
        first_rec:bool = False
        Usr = Bediener
        L_oh = L_bestand
        L_op1 = L_op
        Buf_ophdr = L_ophdr

        if l_artikel.endkum <= 2:

            htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == 224)).first()
        else:

            htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == 221)).first()
        close_date = htparam.fdate

        l_oh = db_session.query(L_oh).filter(
                (L_oh.artnr == s_artnr) &  (L_oh.lager_nr == 0)).first()

        if l_oh:
            t_qty = anz_anf_best + anz_eingang - anz_ausgang

            if show_price:
                t_wert = val_anf_best + wert_eingang - wert_ausgang
        str_list_list.clear()
        tot_anz = 0
        tot_val = 0

        for l_lager in db_session.query(L_lager).filter(
                (L_lager.lager_nr >= from_lager) &  (L_lager.lager_nr <= to_lager)).all():

            l_bestand = db_session.query(L_bestand).filter(
                    (L_bestand.lager_nr == l_lager.lager_nr) &  (L_bestand.artnr == s_artnr)).first()

            if l_bestand:
                t_anz = l_bestand.anz_anf_best

                if show_price:
                    t_val = l_bestand.val_anf_best
                str_list = Str_list()
                str_list_list.append(str_list)

                str_list.s = "        " + to_string(l_lager.lager_nr, "99") + " " + to_string(l_lager.bezeich, "x(13)")
                str_list = Str_list()
                str_list_list.append(str_list)


                if show_price:

                    if not long_digit:
                        str_list.s = to_string(l_bestand.anf_best_dat) + to_string(" ", "x(16)") + to_string(l_bestand.anz_anf_best, "->>>,>>9.99") + to_string(l_bestand.val_anf_best, "->>>,>>>,>>9.99")
                    else:
                        str_list.s = to_string(l_bestand.anf_best_dat) + to_string(" ", "x(16)") + to_string(l_bestand.anz_anf_best, "->>>,>>9.99") + to_string(l_bestand.val_anf_best, "->>,>>>,>>>,>>9")
                else:

                    if not long_digit:
                        str_list.s = to_string(l_bestand.anf_best_dat) + to_string(" ", "x(16)") + to_string(l_bestand.anz_anf_best, "->>>,>>9.99") + to_string(0, "->>>,>>>,>>9.99")
                    else:
                        str_list.s = to_string(l_bestand.anf_best_dat) + to_string(" ", "x(16)") + to_string(l_bestand.anz_anf_best, "->>>,>>9.99") + to_string(0, "->>,>>>,>>>,>>9")

            for l_op in db_session.query(L_op).filter(
                    (L_op.lager_nr == l_lager.lager_nr) &  (L_op.artnr == s_artnr) &  (L_op.loeschflag <= 1) &  (L_op.datum <= close_date)).all():
                it_exist = True

                if show_price:
                    preis = l_op.einzelpreis
                    wert = l_op.warenwert

                if l_op.op_art == 1:
                    bemerk = ""

                    l_lieferant = db_session.query(L_lieferant).filter(
                            (L_lieferant.lief_nr == l_op.lief_nr)).first()

                    if l_lieferant:
                        bemerk = l_lieferant.firma
                    t_anz = t_anz + l_op.anzahl
                    t_val = t_val + wert
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    add_id()
                    str_list.s = to_string(l_op.datum) + to_string(l_op.lscheinnr, "x(16)") + to_string(0, "->>>,>>9.99") + to_string(0, "->>>,>>>,>>9.99") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(wert, "->>,>>>,>>9.99") + to_string(0, "->,>>>,>>9.99") + to_string(0, "->>,>>>,>>9.99") + to_string(0, "->>>,>>9.99") + to_string(bemerk, "x(16)")

                elif l_op.op_art == 2:

                    if l_op.herkunftflag == 1:

                        l_op1 = db_session.query(L_op1).filter(
                                (L_op1.op_art == 4) &  (L_op1.datum == l_op.datum) &  (L_op1.artnr == l_op.artnr) &  (L_op1.anzahl == l_op.anzahl) &  (L_op1.pos == l_op.lager_nr) &  (L_op1.zeit == l_op.zeit)).first()

                        if l_op1:
                            bemerk = translateExtended ("From", lvcarea, "") + " " + to_string(l_op1.lager_nr)
                        else:
                            bemerk = translateExtended ("Transferred", lvcarea, "")

                    elif l_op.herkunftflag == 3:
                        bemerk = translateExtended ("Transform In", lvcarea, "")
                    t_anz = t_anz + l_op.anzahl
                    t_val = t_val + wert
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    add_id()
                    str_list.s = to_string(l_op.datum) + to_string(l_op.lscheinnr, "x(16)") + to_string(0, "->>>,>>9.99") + to_string(0, "->>>,>>>,>>9.99") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(wert, "->>,>>>,>>9.99") + to_string(0, "->,>>>,>>9.99") + to_string(0, "->>,>>>,>>9.99") + to_string(0, "->>>,>>9.99") + to_string(bemerk, "x(16)")

                elif l_op.op_art == 3:

                    if l_op.stornogrund != "":

                        gl_acct = db_session.query(Gl_acct).filter(
                                (Gl_acct.fibukonto == l_op.stornogrund)).first()
                    else:

                        l_ophdr = db_session.query(L_ophdr).filter(
                                (func.lower(L_ophdr.op_typ) == "STT") &  (L_ophdr.datum == l_op.datum) &  (L_ophdr.lscheinnr == l_op.lscheinnr) &  (L_ophdr.fibukonto != "")).first()

                        if l_ophdr:

                            gl_acct = db_session.query(Gl_acct).filter(
                                    (Gl_acct.fibukonto == l_ophdr.fibukonto)).first()
                    bemerk = ""

                    if gl_acct:
                        bemerk = gl_acct.fibukonto
                    t_anz = t_anz - l_op.anzahl
                    t_val = t_val - wert
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    add_id()
                    str_list.s = to_string(l_op.datum) + to_string(l_op.lscheinnr, "x(16)") + to_string(0, "->>>,>>9.99") + to_string(0, "->>>,>>>,>>9.99") + to_string(0, "->,>>>,>>9.99") + to_string(0, "->>,>>>,>>9.99") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(wert, "->>,>>>,>>9.99") + to_string(0, "->>>,>>9.99") + to_string(bemerk, "x(16)")

                elif l_op.op_art == 4:

                    if l_op.herkunftflag == 1:
                        bemerk = translateExtended ("To Store", lvcarea, "") + " " + to_string(l_op.pos)

                    elif l_op.herkunftflag == 3:
                        bemerk = translateExtended ("Transform Out", lvcarea, "")
                    t_anz = t_anz - l_op.anzahl
                    t_val = t_val - wert
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    add_id()
                    str_list.s = to_string(l_op.datum) + to_string(l_op.lscheinnr, "x(16)") + to_string(0, "->>>,>>9.99") + to_string(0, "->>>,>>>,>>9.99") + to_string(0, "->,>>>,>>9.99") + to_string(0, "->>,>>>,>>9.99") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(wert, "->>,>>>,>>9.99") + to_string(0, "->>>,>>9.99") + to_string(bemerk, "x(16)")

            if l_bestand:
                tot_anz = tot_anz + t_anz
                tot_val = tot_val + t_val

                if l_artikel.vk_preis != 0:
                    t_val = t_anz * l_artikel.vk_preis
                str_list = Str_list()
                str_list_list.append(str_list)

                str_list.s = "        " + to_string(translateExtended ("Stock Onhand:", lvcarea, "") , "x(16)") + to_string(t_anz, "->>>,>>9.99") + to_string(t_val, "->>>,>>>,>>9.99")
                str_list = Str_list()
                str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)


        if l_artikel.vk_preis != 0:
            t_wert = t_qty * l_artikel.vk_preis
        str_list.s = "        " + "T O T A L :     " + to_string(t_qty, "->>>,>>9.99") + to_string(t_wert, "->>>,>>>,>>9.99")

        if not it_exist:

            for l_ophis in db_session.query(L_ophis).filter(
                    (L_ophis.artnr == s_artnr) &  (L_ophis.op_art == 1)).all():
                last_date = l_ophis.datum
                break
            first_rec = True

            for l_ophis in db_session.query(L_ophis).filter(
                    (L_ophis.artnr == s_artnr) &  (L_ophis.op_art == 1) &  (L_ophis.datum == last_date)).all():
                str_list = Str_list()
                str_list_list.append(str_list)


                if first_rec:
                    str_list.s = to_string(l_ophis.datum) + to_string(translateExtended ("Last Receiving:", lvcarea, "") , "x(16)") + to_string("", "x(28)") + to_string(l_ophis.anzahl, "->>>,>>9.99") + to_string(l_ophis.warenwert, "->>,>>>,>>9.99")
                else:
                    str_list.s = to_string(l_ophis.datum) + to_string("", "x(16)") + to_string("", "x(28)") + to_string(l_ophis.anzahl, "->>>,>>9.99") + to_string(l_ophis.warenwert, "->>,>>>,>>9.99")
                first_rec = False

            for l_ophis in db_session.query(L_ophis).filter(
                    (L_ophis.artnr == s_artnr) &  (L_ophis.op_art == 3)).all():
                last_date = l_ophis.datum
                break
            first_rec = True

            for l_ophis in db_session.query(L_ophis).filter(
                    (L_ophis.artnr == s_artnr) &  (L_ophis.op_art == 3) &  (L_ophis.datum == last_date)).all():
                str_list = Str_list()
                str_list_list.append(str_list)


                if first_rec:
                    str_list.s = to_string(l_ophis.datum) + to_string(translateExtended ("Last Outgoing:", lvcarea, "") , "x(16)") + to_string("", "x(55)") + to_string(l_ophis.anzahl, "->>>,>>9.99") + to_string(l_ophis.warenwert, "->>,>>>,>>9.99")
                else:
                    str_list.s = to_string(l_ophis.datum) + to_string("", "x(16)") + to_string("", "x(55)") + to_string(l_ophis.anzahl, "->>>,>>9.99") + to_string(l_ophis.warenwert, "->>,>>>,>>9.99")

    def add_id():

        nonlocal str_list_list, tot_anz, tot_val, t_anz, t_val, long_digit, lvcarea, htparam, l_artikel, bediener, l_bestand, l_op, l_ophdr, l_lager, l_lieferant, gl_acct, l_ophis
        nonlocal usr, l_oh, l_op1, buf_ophdr


        nonlocal str_list, usr, l_oh, l_op1, buf_ophdr
        nonlocal str_list_list


        Usr = Bediener

        usr = db_session.query(Usr).filter(
                (Usr.nr == l_op.fuellflag)).first()

        if usr:
            str_list.ID = usr.userinit
        else:
            str_list.ID = "??"

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 246)).first()
    long_digit = htparam.flogical

    l_artikel = db_session.query(L_artikel).filter(
            (L_artikel.artnr == s_artnr)).first()

    if not l_artikel:

        return generate_output()
    create_list()

    return generate_output()