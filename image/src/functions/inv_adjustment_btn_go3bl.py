from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from functions.inv_adjustment_sort3bl import inv_adjustment_sort3bl
from models import Bediener, L_ophdr, L_artikel, L_bestand, L_op, L_verbrauch

def inv_adjustment_btn_go3bl(from_grp:int, transdate:date, curr_lager:int, sorttype:int, user_init:str, c_list:[C_list]):
    lscheinnr:str = ""
    zwkum:int = 0
    a_bez:str = ""
    bediener = l_ophdr = l_artikel = l_bestand = l_op = l_verbrauch = None

    c_list = None

    c_list_list, C_list = create_model("C_list", {"artnr":int, "bezeich":str, "munit":str, "inhalt":str, "zwkum":str, "endkum":int, "qty":decimal, "qty1":decimal, "fibukonto":str, "avrg_price":decimal, "cost_center":str}, {"fibukonto": "0000000000"})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal lscheinnr, zwkum, a_bez, bediener, l_ophdr, l_artikel, l_bestand, l_op, l_verbrauch


        nonlocal c_list
        nonlocal c_list_list
        return {}

    def do_adjustment():

        nonlocal lscheinnr, zwkum, a_bez, bediener, l_ophdr, l_artikel, l_bestand, l_op, l_verbrauch


        nonlocal c_list
        nonlocal c_list_list

        curr_fibukonto:str = ""
        i:int = 0

        for c_list in query(c_list_list, filters=(lambda c_list :c_list.qty != c_list.qty1)):

            if curr_fibukonto != c_list.fibukonto:
                curr_fibukonto = c_list.fibukonto
                i = i + 1
                lscheinnr = "INV" + to_string(get_month(transdate)) + to_string(get_day(transdate)) + to_string((get_current_time_in_seconds() + i) , ">>>>9")
                l_ophdr = L_ophdr()
                db_session.add(l_ophdr)

                l_ophdr.datum = transdate
                l_ophdr.lager_nr = curr_lager
                l_ophdr.docu_nr = lscheinnr
                l_ophdr.lscheinnr = lscheinnr
                l_ophdr.op_typ = "STT"
                l_ophdr.fibukonto = c_list.fibukonto

                l_ophdr = db_session.query(L_ophdr).first()
            create_l_op(c_list.fibukonto)

    def journal_list():

        nonlocal lscheinnr, zwkum, a_bez, bediener, l_ophdr, l_artikel, l_bestand, l_op, l_verbrauch


        nonlocal c_list
        nonlocal c_list_list


        c_list_list.clear()

        if sorttype <= 2:

            l_bestand_obj_list = []
            for l_bestand, l_artikel in db_session.query(L_bestand, L_artikel).join(L_artikel,(L_artikel.artnr == L_bestand.artnr)).filter(
                    (L_bestand.lager_nr == curr_lager)).all():
                if l_bestand._recid in l_bestand_obj_list:
                    continue
                else:
                    l_bestand_obj_list.append(l_bestand._recid)


                c_list = C_list()
                c_list_list.append(c_list)

                c_list.artnr = l_artikel.artnr
                c_list.bezeich = l_artikel.bezeich
                c_list.munit = l_artikel.masseinheit
                c_list.inhalt = to_string(l_artikel.inhalt, ">>>>9.99")
                c_list.endkum = l_artikel.endkum
                c_list.zwkum = to_string(l_artikel.zwkum, ">>>>>>9")
                c_list.qty = l_bestand.anz_anf_best + anz_eingang - anz_ausgang
                c_list.qty1 = l_bestand.anz_anf_best + anz_eingang - anz_ausgang
                c_list.avrg_price = l_artikel.vk_preis


                pass


        elif sorttype == 3:

            l_bestand_obj_list = []
            for l_bestand, l_artikel in db_session.query(L_bestand, L_artikel).join(L_artikel,(L_artikel.artnr == L_bestand.artnr)).filter(
                    (L_bestand.lager_nr == curr_lager)).all():
                if l_bestand._recid in l_bestand_obj_list:
                    continue
                else:
                    l_bestand_obj_list.append(l_bestand._recid)

                if zwkum != l_artikel.zwkum:
                    a_bez = get_output(inv_adjustment_sort3bl(l_artikel.zwkum))
                    c_list = C_list()
                    c_list_list.append(c_list)

                    c_list.bezeich = a_bez
                    c_list.zwkum = to_string(l_artikel.zwkum, ">>>>>>9")
                    c_list.fibukonto = " "


                c_list = C_list()
                c_list_list.append(c_list)

                c_list.artnr = l_artikel.artnr
                c_list.bezeich = l_artikel.bezeich
                c_list.munit = l_artikel.masseinheit
                c_list.inhalt = to_string(l_artikel.inhalt, ">>>>9.99")
                c_list.endkum = l_artikel.endkum
                c_list.zwkum = to_string(l_artikel.zwkum, ">>>>>>9")
                c_list.qty = l_bestand.anz_anf_best + anz_eingang - anz_ausgang
                c_list.qty1 = l_bestand.anz_anf_best + anz_eingang - anz_ausgang
                zwkum = l_artikel.zwkum
                c_list.avrg_price = l_artikel.vk_preis


                pass

    def journal_list1():

        nonlocal lscheinnr, zwkum, a_bez, bediener, l_ophdr, l_artikel, l_bestand, l_op, l_verbrauch


        nonlocal c_list
        nonlocal c_list_list


        c_list_list.clear()

        if sorttype <= 2:

            l_bestand_obj_list = []
            for l_bestand, l_artikel in db_session.query(L_bestand, L_artikel).join(L_artikel,(L_artikel.artnr == L_bestand.artnr) &  (L_artikel.endkum == from_grp)).filter(
                    (L_bestand.lager_nr == curr_lager)).all():
                if l_bestand._recid in l_bestand_obj_list:
                    continue
                else:
                    l_bestand_obj_list.append(l_bestand._recid)


                c_list = C_list()
                c_list_list.append(c_list)

                c_list.artnr = l_artikel.artnr
                c_list.bezeich = l_artikel.bezeich
                c_list.munit = l_artikel.masseinheit
                c_list.inhalt = to_string(l_artikel.inhalt, ">>>>9.99")
                c_list.endkum = l_artikel.endkum
                c_list.zwkum = to_string(l_artikel.zwkum, ">>>>>>9")
                c_list.qty = l_bestand.anz_anf_best + anz_eingang - anz_ausgang
                c_list.qty1 = l_bestand.anz_anf_best + anz_eingang - anz_ausgang
                c_list.avrg_price = l_artikel.vk_preis


                pass


        elif sorttype == 3:

            l_bestand_obj_list = []
            for l_bestand, l_artikel in db_session.query(L_bestand, L_artikel).join(L_artikel,(L_artikel.artnr == L_bestand.artnr) &  (L_artikel.endkum == from_grp)).filter(
                    (L_bestand.lager_nr == curr_lager)).all():
                if l_bestand._recid in l_bestand_obj_list:
                    continue
                else:
                    l_bestand_obj_list.append(l_bestand._recid)

                if zwkum != l_artikel.zwkum:
                    a_bez = get_output(inv_adjustment_sort3bl(l_artikel.zwkum))
                    c_list = C_list()
                    c_list_list.append(c_list)

                    c_list.bezeich = a_bez
                    c_list.zwkum = to_string(l_artikel.zwkum, ">>>>>>9")
                    c_list.fibukonto = " "


                c_list = C_list()
                c_list_list.append(c_list)

                c_list.artnr = l_artikel.artnr
                c_list.bezeich = l_artikel.bezeich
                c_list.munit = l_artikel.masseinheit
                c_list.inhalt = to_string(l_artikel.inhalt, ">>>>9.99")
                c_list.endkum = l_artikel.endkum
                c_list.zwkum = to_string(l_artikel.zwkum, ">>>>>>9")
                c_list.qty = l_bestand.anz_anf_best + anz_eingang - anz_ausgang
                c_list.qty1 = l_bestand.anz_anf_best + anz_eingang - anz_ausgang
                zwkum = l_artikel.zwkum
                c_list.avrg_price = l_artikel.vk_preis


                pass

    def create_l_op(fibukonto:str):

        nonlocal lscheinnr, zwkum, a_bez, bediener, l_ophdr, l_artikel, l_bestand, l_op, l_verbrauch


        nonlocal c_list
        nonlocal c_list_list

        anzahl:decimal = 0
        wert:decimal = 0
        delta_wert:decimal = 0
        avrg_price:decimal = 0
        anz_oh:decimal = 0
        val_oh:decimal = 0

        l_artikel = db_session.query(L_artikel).filter(
                (L_artikel.artnr == to_int(c_list.artnr))).first()

        l_bestand = db_session.query(L_bestand).filter(
                (L_bestand.lager_nr == 0) &  (L_bestand.artnr == to_int(c_list.artnr))).first()
        anz_oh = l_bestand.anz_anf_best + l_bestand.anz_eingang - l_bestand.anz_ausgang
        val_oh = l_bestand.val_anf_best + l_bestand.wert_eingang - l_bestand.wert_ausgang

        if anz_oh != 0:
            avrg_price = val_oh / anz_oh
        else:
            avrg_price = l_artikel.vk_preis
        anzahl = decimal.Decimal(c_list.qty) - decimal.Decimal(c_list.qty1)
        wert = anzahl * avrg_price

        l_bestand = db_session.query(L_bestand).filter(
                (L_bestand.lager_nr == curr_lager) &  (L_bestand.artnr == to_int(c_list.artnr))).first()
        l_bestand.anz_ausgang = l_bestand.anz_ausgang + anzahl
        l_bestand.wert_ausgang = l_bestand.wert_ausgang + wert

        l_bestand = db_session.query(L_bestand).first()

        l_bestand = db_session.query(L_bestand).filter(
                (L_bestand.lager_nr == 0) &  (L_bestand.artnr == to_int(c_list.artnr))).first()
        l_bestand.anz_ausgang = l_bestand.anz_ausgang + anzahl
        l_bestand.wert_ausgang = l_bestand.wert_ausgang + wert

        l_bestand = db_session.query(L_bestand).first()
        l_op = L_op()
        db_session.add(l_op)

        l_op.datum = transdate
        l_op.lager_nr = curr_lager
        l_op.artnr = to_int(c_list.artnr)
        l_op.zeit = get_current_time_in_seconds()
        l_op.anzahl = anzahl
        l_op.einzelpreis = avrg_price
        l_op.warenwert = wert
        l_op.deci1[0] = decimal.Decimal(c_list.qty)
        l_op.op_art = 3
        l_op.herkunftflag = 4
        l_op.lscheinnr = lscheinnr
        l_op.pos = 1
        l_op.fuellflag = bediener.nr
        l_op.stornogrund = fibukonto

        l_op = db_session.query(L_op).first()

        l_verbrauch = db_session.query(L_verbrauch).filter(
                    (L_verbrauch.artnr == to_int(c_list.artnr)) &  (L_verbrauch.datum == transdate)).first()

        if not l_verbrauch:
            l_verbrauch = L_verbrauch()
            db_session.add(l_verbrauch)

            l_verbrauch.artnr = to_int(c_list.artnr)
            l_verbrauch.datum = transdate
        l_verbrauch.anz_verbrau = l_verbrauch.anz_verbrau + anzahl
        l_verbrauch.wert_verbrau = l_verbrauch.wert_verbrau + wert

        l_verbrauch = db_session.query(L_verbrauch).first()

    bediener = db_session.query(Bediener).filter(
            (func.lower(Bediener.userinit) == (user_init).lower())).first()
    do_adjustment()

    if from_grp == 0:
        journal_list()
    else:
        journal_list1()

    return generate_output()