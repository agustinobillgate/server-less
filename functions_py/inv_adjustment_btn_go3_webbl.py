#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.inv_adjustment_sort3bl import inv_adjustment_sort3bl
from models import Gl_acct, Bediener, L_ophdr, L_artikel, L_bestand, L_op, L_verbrauch

c_list_data, C_list = create_model("C_list", {"artnr":int, "bezeich":string, "munit":string, "inhalt":string, "zwkum":string, "endkum":int, "qty":Decimal, "qty1":Decimal, "fibukonto":string, "avrg_price":Decimal, "cost_center":string}, {"fibukonto": "0000000000"})

def inv_adjustment_btn_go3_webbl(from_grp:int, transdate:date, curr_lager:int, sorttype:int, user_init:string, c_list_data:[C_list]):

    prepare_cache ([Bediener, L_ophdr, L_artikel, L_bestand, L_op, L_verbrauch])

    err_code = 0
    lscheinnr:string = ""
    zwkum:int = 0
    a_bez:string = ""
    gl_notfound:bool = False
    gl_acct = bediener = l_ophdr = l_artikel = l_bestand = l_op = l_verbrauch = None

    c_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_code, lscheinnr, zwkum, a_bez, gl_notfound, gl_acct, bediener, l_ophdr, l_artikel, l_bestand, l_op, l_verbrauch
        nonlocal from_grp, transdate, curr_lager, sorttype, user_init


        nonlocal c_list

        return {"c-list": c_list_data, "err_code": err_code}

    def do_adjustment():

        nonlocal err_code, lscheinnr, zwkum, a_bez, gl_notfound, gl_acct, bediener, l_ophdr, l_artikel, l_bestand, l_op, l_verbrauch
        nonlocal from_grp, transdate, curr_lager, sorttype, user_init


        nonlocal c_list

        curr_fibukonto:string = ""
        i:int = 0

        for c_list in query(c_list_data, filters=(lambda c_list: c_list.qty != c_list.qty1), sort_by=[("fibukonto",False)]):

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
                pass
            create_l_op(c_list.fibukonto)


    def journal_list():

        nonlocal err_code, lscheinnr, zwkum, a_bez, gl_notfound, gl_acct, bediener, l_ophdr, l_artikel, l_bestand, l_op, l_verbrauch
        nonlocal from_grp, transdate, curr_lager, sorttype, user_init


        nonlocal c_list


        c_list_data.clear()

        if sorttype <= 2:

            l_bestand_obj_list = {}
            l_bestand = L_bestand()
            l_artikel = L_artikel()
            for l_bestand.anz_anf_best, l_bestand.anz_eingang, l_bestand.anz_ausgang, l_bestand.val_anf_best, l_bestand.wert_eingang, l_bestand.wert_ausgang, l_bestand._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel.masseinheit, l_artikel.inhalt, l_artikel.endkum, l_artikel.zwkum, l_artikel.vk_preis, l_artikel._recid in db_session.query(L_bestand.anz_anf_best, L_bestand.anz_eingang, L_bestand.anz_ausgang, L_bestand.val_anf_best, L_bestand.wert_eingang, L_bestand.wert_ausgang, L_bestand._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel.masseinheit, L_artikel.inhalt, L_artikel.endkum, L_artikel.zwkum, L_artikel.vk_preis, L_artikel._recid).join(L_artikel,(L_artikel.artnr == L_bestand.artnr)).filter(
                     (L_bestand.lager_nr == curr_lager)).order_by(L_artikel.bezeich).all():
                if l_bestand_obj_list.get(l_bestand._recid):
                    continue
                else:
                    l_bestand_obj_list[l_bestand._recid] = True


                c_list = C_list()
                c_list_data.append(c_list)

                c_list.artnr = l_artikel.artnr
                c_list.bezeich = l_artikel.bezeich
                c_list.munit = l_artikel.masseinheit
                c_list.inhalt = to_string(l_artikel.inhalt, ">>>>9.99")
                c_list.endkum = l_artikel.endkum
                c_list.zwkum = to_string(l_artikel.zwkum, ">>>>>>9")
                c_list.qty =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)
                c_list.qty1 =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)


        elif sorttype == 3:

            l_bestand_obj_list = {}
            l_bestand = L_bestand()
            l_artikel = L_artikel()
            for l_bestand.anz_anf_best, l_bestand.anz_eingang, l_bestand.anz_ausgang, l_bestand.val_anf_best, l_bestand.wert_eingang, l_bestand.wert_ausgang, l_bestand._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel.masseinheit, l_artikel.inhalt, l_artikel.endkum, l_artikel.zwkum, l_artikel.vk_preis, l_artikel._recid in db_session.query(L_bestand.anz_anf_best, L_bestand.anz_eingang, L_bestand.anz_ausgang, L_bestand.val_anf_best, L_bestand.wert_eingang, L_bestand.wert_ausgang, L_bestand._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel.masseinheit, L_artikel.inhalt, L_artikel.endkum, L_artikel.zwkum, L_artikel.vk_preis, L_artikel._recid).join(L_artikel,(L_artikel.artnr == L_bestand.artnr)).filter(
                     (L_bestand.lager_nr == curr_lager)).order_by(L_artikel.zwkum, L_artikel.bezeich).all():
                if l_bestand_obj_list.get(l_bestand._recid):
                    continue
                else:
                    l_bestand_obj_list[l_bestand._recid] = True

                if zwkum != l_artikel.zwkum:
                    a_bez = get_output(inv_adjustment_sort3bl(l_artikel.zwkum))
                    c_list = C_list()
                    c_list_data.append(c_list)

                    c_list.bezeich = a_bez
                    c_list.zwkum = to_string(l_artikel.zwkum, ">>>>>>9")
                    c_list.fibukonto = " "


                c_list = C_list()
                c_list_data.append(c_list)

                c_list.artnr = l_artikel.artnr
                c_list.bezeich = l_artikel.bezeich
                c_list.munit = l_artikel.masseinheit
                c_list.inhalt = to_string(l_artikel.inhalt, ">>>>9.99")
                c_list.endkum = l_artikel.endkum
                c_list.zwkum = to_string(l_artikel.zwkum, ">>>>>>9")
                c_list.qty =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)
                c_list.qty1 =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)
                zwkum = l_artikel.zwkum


    def journal_list1():

        nonlocal err_code, lscheinnr, zwkum, a_bez, gl_notfound, gl_acct, bediener, l_ophdr, l_artikel, l_bestand, l_op, l_verbrauch
        nonlocal from_grp, transdate, curr_lager, sorttype, user_init


        nonlocal c_list


        c_list_data.clear()

        if sorttype <= 2:

            l_bestand_obj_list = {}
            l_bestand = L_bestand()
            l_artikel = L_artikel()
            for l_bestand.anz_anf_best, l_bestand.anz_eingang, l_bestand.anz_ausgang, l_bestand.val_anf_best, l_bestand.wert_eingang, l_bestand.wert_ausgang, l_bestand._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel.masseinheit, l_artikel.inhalt, l_artikel.endkum, l_artikel.zwkum, l_artikel.vk_preis, l_artikel._recid in db_session.query(L_bestand.anz_anf_best, L_bestand.anz_eingang, L_bestand.anz_ausgang, L_bestand.val_anf_best, L_bestand.wert_eingang, L_bestand.wert_ausgang, L_bestand._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel.masseinheit, L_artikel.inhalt, L_artikel.endkum, L_artikel.zwkum, L_artikel.vk_preis, L_artikel._recid).join(L_artikel,(L_artikel.artnr == L_bestand.artnr) & (L_artikel.endkum == from_grp)).filter(
                     (L_bestand.lager_nr == curr_lager)).order_by(L_artikel.bezeich).all():
                if l_bestand_obj_list.get(l_bestand._recid):
                    continue
                else:
                    l_bestand_obj_list[l_bestand._recid] = True


                c_list = C_list()
                c_list_data.append(c_list)

                c_list.artnr = l_artikel.artnr
                c_list.bezeich = l_artikel.bezeich
                c_list.munit = l_artikel.masseinheit
                c_list.inhalt = to_string(l_artikel.inhalt, ">>>>9.99")
                c_list.endkum = l_artikel.endkum
                c_list.zwkum = to_string(l_artikel.zwkum, ">>>>>>9")
                c_list.qty =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)
                c_list.qty1 =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)


        elif sorttype == 3:

            l_bestand_obj_list = {}
            l_bestand = L_bestand()
            l_artikel = L_artikel()
            for l_bestand.anz_anf_best, l_bestand.anz_eingang, l_bestand.anz_ausgang, l_bestand.val_anf_best, l_bestand.wert_eingang, l_bestand.wert_ausgang, l_bestand._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel.masseinheit, l_artikel.inhalt, l_artikel.endkum, l_artikel.zwkum, l_artikel.vk_preis, l_artikel._recid in db_session.query(L_bestand.anz_anf_best, L_bestand.anz_eingang, L_bestand.anz_ausgang, L_bestand.val_anf_best, L_bestand.wert_eingang, L_bestand.wert_ausgang, L_bestand._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel.masseinheit, L_artikel.inhalt, L_artikel.endkum, L_artikel.zwkum, L_artikel.vk_preis, L_artikel._recid).join(L_artikel,(L_artikel.artnr == L_bestand.artnr) & (L_artikel.endkum == from_grp)).filter(
                     (L_bestand.lager_nr == curr_lager)).order_by(L_artikel.zwkum, L_artikel.bezeich).all():
                if l_bestand_obj_list.get(l_bestand._recid):
                    continue
                else:
                    l_bestand_obj_list[l_bestand._recid] = True

                if zwkum != l_artikel.zwkum:
                    a_bez = get_output(inv_adjustment_sort3bl(l_artikel.zwkum))
                    c_list = C_list()
                    c_list_data.append(c_list)

                    c_list.bezeich = a_bez
                    c_list.zwkum = to_string(l_artikel.zwkum, ">>>>>>9")
                    c_list.fibukonto = " "


                c_list = C_list()
                c_list_data.append(c_list)

                c_list.artnr = l_artikel.artnr
                c_list.bezeich = l_artikel.bezeich
                c_list.munit = l_artikel.masseinheit
                c_list.inhalt = to_string(l_artikel.inhalt, ">>>>9.99")
                c_list.endkum = l_artikel.endkum
                c_list.zwkum = to_string(l_artikel.zwkum, ">>>>>>9")
                c_list.qty =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)
                c_list.qty1 =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)
                zwkum = l_artikel.zwkum


    def create_l_op(fibukonto:string):

        nonlocal err_code, lscheinnr, zwkum, a_bez, gl_notfound, gl_acct, bediener, l_ophdr, l_artikel, l_bestand, l_op, l_verbrauch
        nonlocal from_grp, transdate, curr_lager, sorttype, user_init


        nonlocal c_list

        anzahl:Decimal = to_decimal("0.0")
        wert:Decimal = to_decimal("0.0")
        delta_wert:Decimal = to_decimal("0.0")
        avrg_price:Decimal = to_decimal("0.0")
        anz_oh:Decimal = to_decimal("0.0")
        val_oh:Decimal = to_decimal("0.0")

        l_artikel = get_cache (L_artikel, {"artnr": [(eq, to_int(c_list.artnr))]})

        l_bestand = get_cache (L_bestand, {"lager_nr": [(eq, 0)],"artnr": [(eq, to_int(c_list.artnr))]})
        anz_oh =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)
        val_oh =  to_decimal(l_bestand.val_anf_best) + to_decimal(l_bestand.wert_eingang) - to_decimal(l_bestand.wert_ausgang)

        if anz_oh != 0:
            avrg_price =  to_decimal(val_oh) / to_decimal(anz_oh)
        else:
            avrg_price =  to_decimal(l_artikel.vk_preis)
        anzahl =  to_decimal(to_decimal(c_list.qty)) - to_decimal(to_decimal(c_list.qty1))
        wert =  to_decimal(anzahl) * to_decimal(avrg_price)

        l_bestand = get_cache (L_bestand, {"lager_nr": [(eq, curr_lager)],"artnr": [(eq, to_int(c_list.artnr))]})
        l_bestand.anz_ausgang =  to_decimal(l_bestand.anz_ausgang) + to_decimal(anzahl)
        l_bestand.wert_ausgang =  to_decimal(l_bestand.wert_ausgang) + to_decimal(wert)
        pass

        l_bestand = get_cache (L_bestand, {"lager_nr": [(eq, 0)],"artnr": [(eq, to_int(c_list.artnr))]})
        l_bestand.anz_ausgang =  to_decimal(l_bestand.anz_ausgang) + to_decimal(anzahl)
        l_bestand.wert_ausgang =  to_decimal(l_bestand.wert_ausgang) + to_decimal(wert)
        pass
        l_op = L_op()
        db_session.add(l_op)

        l_op.datum = transdate
        l_op.lager_nr = curr_lager
        l_op.artnr = to_int(c_list.artnr)
        l_op.zeit = get_current_time_in_seconds()
        l_op.anzahl =  to_decimal(anzahl)
        l_op.einzelpreis =  to_decimal(avrg_price)
        l_op.warenwert =  to_decimal(wert)
        l_op.deci1[0] = c_list.qty
        l_op.op_art = 3
        l_op.herkunftflag = 4
        l_op.lscheinnr = lscheinnr
        l_op.pos = 1
        l_op.fuellflag = bediener.nr
        l_op.stornogrund = fibukonto

        l_verbrauch = get_cache (L_verbrauch, {"artnr": [(eq, to_int(c_list.artnr))],"datum": [(eq, transdate)]})

        if not l_verbrauch:
            l_verbrauch = L_verbrauch()
            db_session.add(l_verbrauch)

            l_verbrauch.artnr = to_int(c_list.artnr)
            l_verbrauch.datum = transdate
        l_verbrauch.anz_verbrau =  to_decimal(l_verbrauch.anz_verbrau) + to_decimal(anzahl)
        l_verbrauch.wert_verbrau =  to_decimal(l_verbrauch.wert_verbrau) + to_decimal(wert)
        pass


    for c_list in query(c_list_data, filters=(lambda c_list: c_list.fibukonto != "" and c_list.fibukonto != None)):

        if trim(c_list.fibukonto) == ("0").lower()  or trim(c_list.fibukonto) == ("00").lower()  or trim(c_list.fibukonto) == ("000").lower()  or trim(c_list.fibukonto) == ("0000").lower()  or trim(c_list.fibukonto) == ("00000").lower()  or trim(c_list.fibukonto) == ("000000").lower()  or trim(c_list.fibukonto) == ("0000000").lower()  or trim(c_list.fibukonto) == ("00000000").lower()  or trim(c_list.fibukonto) == ("000000000").lower()  or trim(c_list.fibukonto) == ("0000000000").lower()  or trim(c_list.fibukonto) == ("00000000000").lower()  or trim(c_list.fibukonto) == ("000000000000").lower()  or trim(c_list.fibukonto) == ("0000000000000").lower() :
            gl_notfound = False
        else:

            gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, c_list.fibukonto)]})

            if not gl_acct:
                gl_notfound = True
                break
            else:
                gl_notfound = False

    if gl_notfound:
        err_code = 1

        return generate_output()

    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})
    do_adjustment()

    if from_grp == 0:
        journal_list()
    else:
        journal_list1()

    return generate_output()