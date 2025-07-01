#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Htparam, L_bestand, L_lager, L_artikel, L_untergrup

def sall_onhand_btn_gobl(all_flag:bool, show_price:bool, zero_flag:bool, from_grp:int, sub_grp:int, from_lager:int, to_lager:int, sorttype:int, mattype:int):

    prepare_cache ([Htparam, L_bestand, L_lager, L_artikel, L_untergrup])

    str_list_list = []
    long_digit:bool = False
    htparam = l_bestand = l_lager = l_artikel = l_untergrup = None

    str_list = None

    str_list_list, Str_list = create_model("Str_list", {"flag":int, "s":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal str_list_list, long_digit, htparam, l_bestand, l_lager, l_artikel, l_untergrup
        nonlocal all_flag, show_price, zero_flag, from_grp, sub_grp, from_lager, to_lager, sorttype, mattype


        nonlocal str_list
        nonlocal str_list_list

        return {"str-list": str_list_list}

    def create_list():

        nonlocal str_list_list, long_digit, htparam, l_bestand, l_lager, l_artikel, l_untergrup
        nonlocal all_flag, show_price, zero_flag, from_grp, sub_grp, from_lager, to_lager, sorttype, mattype


        nonlocal str_list
        nonlocal str_list_list

        i:int = 0
        j:int = 0
        tot_anz:Decimal = to_decimal("0.0")
        tot_val:Decimal = to_decimal("0.0")
        t_anz:Decimal = to_decimal("0.0")
        t_val:Decimal = to_decimal("0.0")
        t_value:Decimal = to_decimal("0.0")
        avrg_price:Decimal = to_decimal("0.0")
        zwkum:int = 0
        bezeich:string = ""
        must_order:Decimal = to_decimal("0.0")
        l_oh = None
        qty:Decimal = to_decimal("0.0")
        wert:Decimal = to_decimal("0.0")
        tot_bezeich:string = ""
        tt_val:Decimal = to_decimal("0.0")
        tt_value:Decimal = to_decimal("0.0")
        L_oh =  create_buffer("L_oh",L_bestand)
        str_list_list.clear()

        for l_lager in db_session.query(L_lager).filter(
                 (L_lager.lager_nr >= from_lager) & (L_lager.lager_nr <= to_lager)).order_by(L_lager._recid).all():
            tot_bezeich = "Ttl - " + l_lager.bezeich
            i = 0
            zwkum = 0
            t_anz =  to_decimal("0")
            t_val =  to_decimal("0")
            tt_val =  to_decimal("0")

            if sorttype == 1:

                if sub_grp != 000:

                    l_bestand_obj_list = {}
                    l_bestand = L_bestand()
                    l_artikel = L_artikel()
                    l_oh = L_bestand()
                    l_untergrup = L_untergrup()
                    for l_bestand.anz_anf_best, l_bestand.anz_eingang, l_bestand.anz_ausgang, l_bestand.val_anf_best, l_bestand.wert_eingang, l_bestand.wert_ausgang, l_bestand._recid, l_artikel.zwkum, l_artikel.anzverbrauch, l_artikel.artnr, l_artikel.bezeich, l_artikel.masseinheit, l_artikel.inhalt, l_artikel.traubensorte, l_artikel.lief_einheit, l_artikel.ek_letzter, l_artikel.ek_aktuell, l_artikel.vk_preis, l_artikel.min_bestand, l_artikel._recid, l_oh.anz_anf_best, l_oh.anz_eingang, l_oh.anz_ausgang, l_oh.val_anf_best, l_oh.wert_eingang, l_oh.wert_ausgang, l_oh._recid, l_untergrup.bezeich, l_untergrup.zwkum, l_untergrup._recid in db_session.query(L_bestand.anz_anf_best, L_bestand.anz_eingang, L_bestand.anz_ausgang, L_bestand.val_anf_best, L_bestand.wert_eingang, L_bestand.wert_ausgang, L_bestand._recid, L_artikel.zwkum, L_artikel.anzverbrauch, L_artikel.artnr, L_artikel.bezeich, L_artikel.masseinheit, L_artikel.inhalt, L_artikel.traubensorte, L_artikel.lief_einheit, L_artikel.ek_letzter, L_artikel.ek_aktuell, L_artikel.vk_preis, L_artikel.min_bestand, L_artikel._recid, L_oh.anz_anf_best, L_oh.anz_eingang, L_oh.anz_ausgang, L_oh.val_anf_best, L_oh.wert_eingang, L_oh.wert_ausgang, L_oh._recid, L_untergrup.bezeich, L_untergrup.zwkum, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_bestand.artnr) & (L_artikel.zwkum == sub_grp)).join(L_oh,(L_oh.artnr == L_bestand.artnr) & (L_oh.lager_nr == 0)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                             (L_bestand.lager_nr == l_lager.lager_nr)).order_by(L_artikel.zwkum, L_artikel.artnr).all():
                        if l_bestand_obj_list.get(l_bestand._recid):
                            continue
                        else:
                            l_bestand_obj_list[l_bestand._recid] = True


                        i = i + 1
                        must_order =  to_decimal("0")

                        if i == 1:
                            str_list = Str_list()
                            str_list_list.append(str_list)

                            str_list.s = " " + to_string(l_lager.lager_nr, "99") + " " + to_string(l_lager.bezeich, "x(50)")

                        if zwkum == 0:
                            zwkum = l_artikel.zwkum
                            bezeich = l_untergrup.bezeich

                        if zwkum != l_artikel.zwkum:
                            str_list = Str_list()
                            str_list_list.append(str_list)

                            str_list.flag = 1
                            str_list.s = " "
                            str_list.s = str_list.s + to_string(bezeich, "x(50)")
                            for j in range(1,84 + 1) :
                                str_list.s = str_list.s + " "

                            if not long_digit:
                                str_list.s = str_list.s + to_string(t_val, "->>>,>>>,>>9.99")
                            else:
                                str_list.s = str_list.s + to_string(t_val, "->>,>>>,>>>,>>9")
                            str_list = Str_list()
                            str_list_list.append(str_list)

                            t_anz =  to_decimal("0")
                            t_val =  to_decimal("0")
                            zwkum = l_untergrup.zwkum
                            bezeich = l_untergrup.bezeich
                        qty =  to_decimal(l_oh.anz_anf_best) + to_decimal(l_oh.anz_eingang) - to_decimal(l_oh.anz_ausgang)

                        if show_price:
                            wert =  to_decimal(l_oh.val_anf_best) + to_decimal(l_oh.wert_eingang) - to_decimal(l_oh.wert_ausgang)
                        tot_anz =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)

                        if l_artikel.anzverbrauch != 0:
                            must_order =  to_decimal(l_artikel.anzverbrauch) - to_decimal(tot_anz)

                        if qty != 0:
                            tot_val =  to_decimal(wert) * to_decimal(tot_anz) / to_decimal(qty)
                        else:
                            tot_val =  to_decimal("0")
                        t_anz =  to_decimal(t_anz) + to_decimal(tot_anz)

                        if show_price:
                            t_val =  to_decimal(t_val) + to_decimal(tot_val)
                            t_value =  to_decimal(t_value) + to_decimal(tot_val)
                            tt_val =  to_decimal(tt_val) + to_decimal(tot_val)
                            tt_value =  to_decimal(tt_value) + to_decimal(tot_val)

                        if tot_anz != 0 or (tot_anz == 0 and zero_flag):
                            str_list = Str_list()
                            str_list_list.append(str_list)


                            if show_price:

                                if not long_digit:
                                    str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensorte, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(l_artikel.ek_letzter, ">>>,>>>,>>9.99") + to_string(l_artikel.ek_aktuell, ">>>,>>>,>>9.99") + to_string(l_artikel.vk_preis, "->>,>>>,>>9.99") + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_val, "->>>,>>>,>>9.99") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                                else:
                                    str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensorte, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(l_artikel.ek_letzter, ">,>>>,>>>,>>9") + to_string(l_artikel.ek_aktuell, ">,>>>,>>>,>>9") + to_string(l_artikel.vk_preis, "->,>>>,>>>,>>9") + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_val, "->>,>>>,>>>,>>9") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                            else:

                                if not long_digit:
                                    str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensorte, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(tot_anz, "->,>>>,>>9.99") + to_string(0, "->>>,>>>,>>9.99") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                                else:
                                    str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensorte, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(0, ">,>>>,>>>,>>9") + to_string(0, ">,>>>,>>>,>>9") + to_string(0, ">,>>>,>>>,>>9") + to_string(tot_anz, "->,>>>,>>9.99") + to_string(0, "->>,>>>,>>>,>>9") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")

            else:

                l_bestand_obj_list = {}
                l_bestand = L_bestand()
                l_artikel = L_artikel()
                l_oh = L_bestand()
                l_untergrup = L_untergrup()
                for l_bestand.anz_anf_best, l_bestand.anz_eingang, l_bestand.anz_ausgang, l_bestand.val_anf_best, l_bestand.wert_eingang, l_bestand.wert_ausgang, l_bestand._recid, l_artikel.zwkum, l_artikel.anzverbrauch, l_artikel.artnr, l_artikel.bezeich, l_artikel.masseinheit, l_artikel.inhalt, l_artikel.traubensorte, l_artikel.lief_einheit, l_artikel.ek_letzter, l_artikel.ek_aktuell, l_artikel.vk_preis, l_artikel.min_bestand, l_artikel._recid, l_oh.anz_anf_best, l_oh.anz_eingang, l_oh.anz_ausgang, l_oh.val_anf_best, l_oh.wert_eingang, l_oh.wert_ausgang, l_oh._recid, l_untergrup.bezeich, l_untergrup.zwkum, l_untergrup._recid in db_session.query(L_bestand.anz_anf_best, L_bestand.anz_eingang, L_bestand.anz_ausgang, L_bestand.val_anf_best, L_bestand.wert_eingang, L_bestand.wert_ausgang, L_bestand._recid, L_artikel.zwkum, L_artikel.anzverbrauch, L_artikel.artnr, L_artikel.bezeich, L_artikel.masseinheit, L_artikel.inhalt, L_artikel.traubensorte, L_artikel.lief_einheit, L_artikel.ek_letzter, L_artikel.ek_aktuell, L_artikel.vk_preis, L_artikel.min_bestand, L_artikel._recid, L_oh.anz_anf_best, L_oh.anz_eingang, L_oh.anz_ausgang, L_oh.val_anf_best, L_oh.wert_eingang, L_oh.wert_ausgang, L_oh._recid, L_untergrup.bezeich, L_untergrup.zwkum, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_bestand.artnr)).join(L_oh,(L_oh.artnr == L_bestand.artnr) & (L_oh.lager_nr == 0)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                         (L_bestand.lager_nr == l_lager.lager_nr)).order_by(L_artikel.zwkum, L_artikel.artnr).all():
                    if l_bestand_obj_list.get(l_bestand._recid):
                        continue
                    else:
                        l_bestand_obj_list[l_bestand._recid] = True


                    i = i + 1
                    must_order =  to_decimal("0")

                    if i == 1:
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        str_list.s = " " + to_string(l_lager.lager_nr, "99") + " " + to_string(l_lager.bezeich, "x(50)")

                    if zwkum == 0:
                        zwkum = l_artikel.zwkum
                        bezeich = l_untergrup.bezeich

                    if zwkum != l_artikel.zwkum:
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        str_list.flag = 1
                        str_list.s = " "
                        str_list.s = str_list.s + to_string(bezeich, "x(50)")
                        for j in range(1,84 + 1) :
                            str_list.s = str_list.s + " "

                        if not long_digit:
                            str_list.s = str_list.s + to_string(t_val, "->>>,>>>,>>9.99")
                        else:
                            str_list.s = str_list.s + to_string(t_val, "->>,>>>,>>>,>>9")
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        t_anz =  to_decimal("0")
                        t_val =  to_decimal("0")
                        zwkum = l_untergrup.zwkum
                        bezeich = l_untergrup.bezeich
                    qty =  to_decimal(l_oh.anz_anf_best) + to_decimal(l_oh.anz_eingang) - to_decimal(l_oh.anz_ausgang)

                    if show_price:
                        wert =  to_decimal(l_oh.val_anf_best) + to_decimal(l_oh.wert_eingang) - to_decimal(l_oh.wert_ausgang)
                    tot_anz =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)

                    if l_artikel.anzverbrauch != 0:
                        must_order =  to_decimal(l_artikel.anzverbrauch) - to_decimal(tot_anz)

                    if qty != 0:
                        tot_val =  to_decimal(wert) * to_decimal(tot_anz) / to_decimal(qty)
                    else:
                        tot_val =  to_decimal("0")
                    t_anz =  to_decimal(t_anz) + to_decimal(tot_anz)

                    if show_price:
                        t_val =  to_decimal(t_val) + to_decimal(tot_val)
                        t_value =  to_decimal(t_value) + to_decimal(tot_val)
                        tt_val =  to_decimal(tt_val) + to_decimal(tot_val)
                        tt_value =  to_decimal(tt_value) + to_decimal(tot_val)

                    if tot_anz != 0 or (tot_anz == 0 and zero_flag):
                        str_list = Str_list()
                        str_list_list.append(str_list)


                        if show_price:

                            if not long_digit:
                                str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensorte, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(l_artikel.ek_letzter, ">>>,>>>,>>9.99") + to_string(l_artikel.ek_aktuell, ">>>,>>>,>>9.99") + to_string(l_artikel.vk_preis, "->>,>>>,>>9.99") + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_val, "->>>,>>>,>>9.99") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                            else:
                                str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensorte, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(l_artikel.ek_letzter, ">,>>>,>>>,>>9") + to_string(l_artikel.ek_aktuell, ">,>>>,>>>,>>9") + to_string(l_artikel.vk_preis, "->,>>>,>>>,>>9") + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_val, "->>,>>>,>>>,>>9") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                        else:

                            if not long_digit:
                                str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensorte, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(tot_anz, "->,>>>,>>9.99") + to_string(0, "->>>,>>>,>>9.99") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                            else:
                                str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensorte, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(0, ">,>>>,>>>,>>9") + to_string(0, ">,>>>,>>>,>>9") + to_string(0, ">,>>>,>>>,>>9") + to_string(tot_anz, "->,>>>,>>9.99") + to_string(0, "->>,>>>,>>>,>>9") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")


            elif sorttype == 2:

                if sub_grp != 000:

                    l_bestand_obj_list = {}
                    l_bestand = L_bestand()
                    l_artikel = L_artikel()
                    l_oh = L_bestand()
                    l_untergrup = L_untergrup()
                    for l_bestand.anz_anf_best, l_bestand.anz_eingang, l_bestand.anz_ausgang, l_bestand.val_anf_best, l_bestand.wert_eingang, l_bestand.wert_ausgang, l_bestand._recid, l_artikel.zwkum, l_artikel.anzverbrauch, l_artikel.artnr, l_artikel.bezeich, l_artikel.masseinheit, l_artikel.inhalt, l_artikel.traubensorte, l_artikel.lief_einheit, l_artikel.ek_letzter, l_artikel.ek_aktuell, l_artikel.vk_preis, l_artikel.min_bestand, l_artikel._recid, l_oh.anz_anf_best, l_oh.anz_eingang, l_oh.anz_ausgang, l_oh.val_anf_best, l_oh.wert_eingang, l_oh.wert_ausgang, l_oh._recid, l_untergrup.bezeich, l_untergrup.zwkum, l_untergrup._recid in db_session.query(L_bestand.anz_anf_best, L_bestand.anz_eingang, L_bestand.anz_ausgang, L_bestand.val_anf_best, L_bestand.wert_eingang, L_bestand.wert_ausgang, L_bestand._recid, L_artikel.zwkum, L_artikel.anzverbrauch, L_artikel.artnr, L_artikel.bezeich, L_artikel.masseinheit, L_artikel.inhalt, L_artikel.traubensorte, L_artikel.lief_einheit, L_artikel.ek_letzter, L_artikel.ek_aktuell, L_artikel.vk_preis, L_artikel.min_bestand, L_artikel._recid, L_oh.anz_anf_best, L_oh.anz_eingang, L_oh.anz_ausgang, L_oh.val_anf_best, L_oh.wert_eingang, L_oh.wert_ausgang, L_oh._recid, L_untergrup.bezeich, L_untergrup.zwkum, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_bestand.artnr) & (L_artikel.zwkum == sub_grp)).join(L_oh,(L_oh.artnr == L_bestand.artnr) & (L_oh.lager_nr == 0)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                             (L_bestand.lager_nr == l_lager.lager_nr)).order_by(L_artikel.zwkum, L_artikel.bezeich).all():
                        if l_bestand_obj_list.get(l_bestand._recid):
                            continue
                        else:
                            l_bestand_obj_list[l_bestand._recid] = True


                        i = i + 1
                        must_order =  to_decimal("0")

                        if i == 1:
                            str_list = Str_list()
                            str_list_list.append(str_list)

                            str_list.s = " " + to_string(l_lager.lager_nr, "99") + " " + to_string(l_lager.bezeich, "x(13)")

                        if zwkum == 0:
                            zwkum = l_artikel.zwkum
                            bezeich = l_untergrup.bezeich

                        if zwkum != l_artikel.zwkum:
                            str_list = Str_list()
                            str_list_list.append(str_list)

                            str_list.flag = 1
                            str_list.s = " "
                            str_list.s = str_list.s + to_string(bezeich, "x(50)")
                            for j in range(1,84 + 1) :
                                str_list.s = str_list.s + " "

                            if not long_digit:
                                str_list.s = str_list.s + to_string(t_val, "->>>,>>>,>>9.99")
                            else:
                                str_list.s = str_list.s + to_string(t_val, "->>,>>>,>>>,>>9")
                            str_list = Str_list()
                            str_list_list.append(str_list)

                            t_anz =  to_decimal("0")
                            t_val =  to_decimal("0")
                            zwkum = l_untergrup.zwkum
                            bezeich = l_untergrup.bezeich
                        qty =  to_decimal(l_oh.anz_anf_best) + to_decimal(l_oh.anz_eingang) - to_decimal(l_oh.anz_ausgang)

                        if show_price:
                            wert =  to_decimal(l_oh.val_anf_best) + to_decimal(l_oh.wert_eingang) - to_decimal(l_oh.wert_ausgang)
                        tot_anz =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)

                        if l_artikel.anzverbrauch != 0:
                            must_order =  to_decimal(l_artikel.anzverbrauch) - to_decimal(tot_anz)

                        if qty != 0:
                            tot_val =  to_decimal(wert) * to_decimal(tot_anz) / to_decimal(qty)
                        else:
                            tot_val =  to_decimal("0")
                        t_anz =  to_decimal(t_anz) + to_decimal(tot_anz)

                        if show_price:
                            t_val =  to_decimal(t_val) + to_decimal(tot_val)
                            t_value =  to_decimal(t_value) + to_decimal(tot_val)
                            tt_val =  to_decimal(tt_val) + to_decimal(tot_val)
                            tt_value =  to_decimal(tt_value) + to_decimal(tot_val)

                        if tot_anz != 0 or (tot_anz == 0 and zero_flag):
                            str_list = Str_list()
                            str_list_list.append(str_list)


                            if show_price:

                                if not long_digit:
                                    str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensorte, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(l_artikel.ek_letzter, ">>>,>>>,>>9.99") + to_string(l_artikel.ek_aktuell, ">>>,>>>,>>9.99") + to_string(l_artikel.vk_preis, "->>,>>>,>>9.99") + to_string(tot_anz, " ->>>,>>9.99") + to_string(tot_val, "->>>,>>>,>>9.99") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                                else:
                                    str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensorte, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(l_artikel.ek_letzter, ">,>>>,>>>,>>9") + to_string(l_artikel.ek_aktuell, ">,>>>,>>>,>>9") + to_string(l_artikel.vk_preis, "->,>>>,>>>,>>9") + to_string(tot_anz, " ->>>,>>9.99") + to_string(tot_val, "->>,>>>,>>>,>>9") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                            else:

                                if not long_digit:
                                    str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensorte, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(tot_anz, " ->>>,>>9.99") + to_string(0, "->>>,>>>,>>9.99") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                                else:
                                    str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensorte, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(0, ">,>>>,>>>,>>9") + to_string(0, ">,>>>,>>>,>>9") + to_string(0, ">,>>>,>>>,>>9") + to_string(tot_anz, " ->>>,>>9.99") + to_string(0, "->>,>>>,>>>,>>9") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")

            else:

                l_bestand_obj_list = {}
                l_bestand = L_bestand()
                l_artikel = L_artikel()
                l_oh = L_bestand()
                l_untergrup = L_untergrup()
                for l_bestand.anz_anf_best, l_bestand.anz_eingang, l_bestand.anz_ausgang, l_bestand.val_anf_best, l_bestand.wert_eingang, l_bestand.wert_ausgang, l_bestand._recid, l_artikel.zwkum, l_artikel.anzverbrauch, l_artikel.artnr, l_artikel.bezeich, l_artikel.masseinheit, l_artikel.inhalt, l_artikel.traubensorte, l_artikel.lief_einheit, l_artikel.ek_letzter, l_artikel.ek_aktuell, l_artikel.vk_preis, l_artikel.min_bestand, l_artikel._recid, l_oh.anz_anf_best, l_oh.anz_eingang, l_oh.anz_ausgang, l_oh.val_anf_best, l_oh.wert_eingang, l_oh.wert_ausgang, l_oh._recid, l_untergrup.bezeich, l_untergrup.zwkum, l_untergrup._recid in db_session.query(L_bestand.anz_anf_best, L_bestand.anz_eingang, L_bestand.anz_ausgang, L_bestand.val_anf_best, L_bestand.wert_eingang, L_bestand.wert_ausgang, L_bestand._recid, L_artikel.zwkum, L_artikel.anzverbrauch, L_artikel.artnr, L_artikel.bezeich, L_artikel.masseinheit, L_artikel.inhalt, L_artikel.traubensorte, L_artikel.lief_einheit, L_artikel.ek_letzter, L_artikel.ek_aktuell, L_artikel.vk_preis, L_artikel.min_bestand, L_artikel._recid, L_oh.anz_anf_best, L_oh.anz_eingang, L_oh.anz_ausgang, L_oh.val_anf_best, L_oh.wert_eingang, L_oh.wert_ausgang, L_oh._recid, L_untergrup.bezeich, L_untergrup.zwkum, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_bestand.artnr)).join(L_oh,(L_oh.artnr == L_bestand.artnr) & (L_oh.lager_nr == 0)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                         (L_bestand.lager_nr == l_lager.lager_nr)).order_by(L_artikel.zwkum, L_artikel.bezeich).all():
                    if l_bestand_obj_list.get(l_bestand._recid):
                        continue
                    else:
                        l_bestand_obj_list[l_bestand._recid] = True


                    i = i + 1
                    must_order =  to_decimal("0")

                    if i == 1:
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        str_list.s = " " + to_string(l_lager.lager_nr, "99") + " " + to_string(l_lager.bezeich, "x(13)")

                    if zwkum == 0:
                        zwkum = l_artikel.zwkum
                        bezeich = l_untergrup.bezeich

                    if zwkum != l_artikel.zwkum:
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        str_list.flag = 1
                        str_list.s = " "
                        str_list.s = str_list.s + to_string(bezeich, "x(50)")
                        for j in range(1,84 + 1) :
                            str_list.s = str_list.s + " "

                        if not long_digit:
                            str_list.s = str_list.s + to_string(t_val, "->>>,>>>,>>9.99")
                        else:
                            str_list.s = str_list.s + to_string(t_val, "->>,>>>,>>>,>>9")
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        t_anz =  to_decimal("0")
                        t_val =  to_decimal("0")
                        zwkum = l_untergrup.zwkum
                        bezeich = l_untergrup.bezeich
                    qty =  to_decimal(l_oh.anz_anf_best) + to_decimal(l_oh.anz_eingang) - to_decimal(l_oh.anz_ausgang)

                    if show_price:
                        wert =  to_decimal(l_oh.val_anf_best) + to_decimal(l_oh.wert_eingang) - to_decimal(l_oh.wert_ausgang)
                    tot_anz =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)

                    if l_artikel.anzverbrauch != 0:
                        must_order =  to_decimal(l_artikel.anzverbrauch) - to_decimal(tot_anz)

                    if qty != 0:
                        tot_val =  to_decimal(wert) * to_decimal(tot_anz) / to_decimal(qty)
                    else:
                        tot_val =  to_decimal("0")
                    t_anz =  to_decimal(t_anz) + to_decimal(tot_anz)

                    if show_price:
                        t_val =  to_decimal(t_val) + to_decimal(tot_val)
                        t_value =  to_decimal(t_value) + to_decimal(tot_val)
                        tt_val =  to_decimal(tt_val) + to_decimal(tot_val)
                        tt_value =  to_decimal(tt_value) + to_decimal(tot_val)

                    if tot_anz != 0 or (tot_anz == 0 and zero_flag):
                        str_list = Str_list()
                        str_list_list.append(str_list)


                        if show_price:

                            if not long_digit:
                                str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensorte, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(l_artikel.ek_letzter, ">>>,>>>,>>9.99") + to_string(l_artikel.ek_aktuell, ">>>,>>>,>>9.99") + to_string(l_artikel.vk_preis, "->>,>>>,>>9.99") + to_string(tot_anz, " ->>>,>>9.99") + to_string(tot_val, "->>>,>>>,>>9.99") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                            else:
                                str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensorte, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(l_artikel.ek_letzter, ">,>>>,>>>,>>9") + to_string(l_artikel.ek_aktuell, ">,>>>,>>>,>>9") + to_string(l_artikel.vk_preis, "->,>>>,>>>,>>9") + to_string(tot_anz, " ->>>,>>9.99") + to_string(tot_val, "->>,>>>,>>>,>>9") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                        else:

                            if not long_digit:
                                str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensorte, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(tot_anz, " ->>>,>>9.99") + to_string(0, "->>>,>>>,>>9.99") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                            else:
                                str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensorte, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(0, ">,>>>,>>>,>>9") + to_string(0, ">,>>>,>>>,>>9") + to_string(0, ">,>>>,>>>,>>9") + to_string(tot_anz, " ->>>,>>9.99") + to_string(0, "->>,>>>,>>>,>>9") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")


            if t_val != 0:
                str_list = Str_list()
                str_list_list.append(str_list)

                str_list.flag = 1
                str_list.s = " "
                str_list.s = str_list.s + to_string(bezeich, "x(50)")
                for j in range(1,84 + 1) :
                    str_list.s = str_list.s + " "

                if not long_digit:
                    str_list.s = str_list.s + to_string(t_val, "->>>,>>>,>>9.99")
                else:
                    str_list.s = str_list.s + to_string(t_val, "->>,>>>,>>>,>>9")
                str_list = Str_list()
                str_list_list.append(str_list)

            str_list = Str_list()
            str_list_list.append(str_list)

            str_list.flag = 1
            str_list.s = " "
            str_list.s = str_list.s + to_string(tot_bezeich, "x(50)")
            for j in range(1,84 + 1) :
                str_list.s = str_list.s + " "

            if not long_digit:
                str_list.s = str_list.s + to_string(tt_val, "->>>,>>>,>>9.99")
            else:
                str_list.s = str_list.s + to_string(tt_val, "->>,>>>,>>>,>>9")
            str_list = Str_list()
            str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.flag = 1
        str_list.s = " "
        str_list.s = str_list.s + to_string("GRAND T O T A L", "x(50)")
        for j in range(1,84 + 1) :
            str_list.s = str_list.s + " "

        if not long_digit:
            str_list.s = str_list.s + to_string(tt_value, "->>>,>>>,>>9.99")
        else:
            str_list.s = str_list.s + to_string(tt_value, "->>,>>>,>>>,>>9")


    def create_lista():

        nonlocal str_list_list, long_digit, htparam, l_bestand, l_lager, l_artikel, l_untergrup
        nonlocal all_flag, show_price, zero_flag, from_grp, sub_grp, from_lager, to_lager, sorttype, mattype


        nonlocal str_list
        nonlocal str_list_list

        i:int = 0
        j:int = 0
        tot_anz:Decimal = to_decimal("0.0")
        tot_val:Decimal = to_decimal("0.0")
        t_anz:Decimal = to_decimal("0.0")
        t_val:Decimal = to_decimal("0.0")
        t_value:Decimal = to_decimal("0.0")
        avrg_price:Decimal = to_decimal("0.0")
        zwkum:int = 0
        bezeich:string = ""
        must_order:Decimal = to_decimal("0.0")
        l_oh = None
        qty:Decimal = to_decimal("0.0")
        wert:Decimal = to_decimal("0.0")
        tot_bezeich:string = ""
        tt_val:Decimal = to_decimal("0.0")
        tt_value:Decimal = to_decimal("0.0")
        L_oh =  create_buffer("L_oh",L_bestand)
        str_list_list.clear()
        i = 0
        zwkum = 0
        t_anz =  to_decimal("0")
        t_val =  to_decimal("0")
        tt_val =  to_decimal("0")

        if sorttype == 1:

            if sub_grp != 000:

                l_bestand_obj_list = {}
                l_bestand = L_bestand()
                l_artikel = L_artikel()
                l_untergrup = L_untergrup()
                for l_bestand.anz_anf_best, l_bestand.anz_eingang, l_bestand.anz_ausgang, l_bestand.val_anf_best, l_bestand.wert_eingang, l_bestand.wert_ausgang, l_bestand._recid, l_artikel.zwkum, l_artikel.anzverbrauch, l_artikel.artnr, l_artikel.bezeich, l_artikel.masseinheit, l_artikel.inhalt, l_artikel.traubensorte, l_artikel.lief_einheit, l_artikel.ek_letzter, l_artikel.ek_aktuell, l_artikel.vk_preis, l_artikel.min_bestand, l_artikel._recid, l_untergrup.bezeich, l_untergrup.zwkum, l_untergrup._recid in db_session.query(L_bestand.anz_anf_best, L_bestand.anz_eingang, L_bestand.anz_ausgang, L_bestand.val_anf_best, L_bestand.wert_eingang, L_bestand.wert_ausgang, L_bestand._recid, L_artikel.zwkum, L_artikel.anzverbrauch, L_artikel.artnr, L_artikel.bezeich, L_artikel.masseinheit, L_artikel.inhalt, L_artikel.traubensorte, L_artikel.lief_einheit, L_artikel.ek_letzter, L_artikel.ek_aktuell, L_artikel.vk_preis, L_artikel.min_bestand, L_artikel._recid, L_untergrup.bezeich, L_untergrup.zwkum, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_bestand.artnr) & (L_artikel.zwkum == sub_grp)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                             (L_bestand.lager_nr == 0)).order_by(L_artikel.zwkum, L_artikel.artnr).all():
                    if l_bestand_obj_list.get(l_bestand._recid):
                        continue
                    else:
                        l_bestand_obj_list[l_bestand._recid] = True


                    i = i + 1
                    must_order =  to_decimal("0")

                    if zwkum == 0:
                        zwkum = l_artikel.zwkum
                        bezeich = l_untergrup.bezeich

                    if zwkum != l_artikel.zwkum:
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        str_list.flag = 1
                        str_list.s = " "
                        str_list.s = str_list.s + to_string(bezeich, "x(50)")
                        for j in range(1,84 + 1) :
                            str_list.s = str_list.s + " "

                        if not long_digit:
                            str_list.s = str_list.s + to_string(t_val, "->>>,>>>,>>9.99")
                        else:
                            str_list.s = str_list.s + to_string(t_val, "->>,>>>,>>>,>>9")
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        t_anz =  to_decimal("0")
                        t_val =  to_decimal("0")
                        zwkum = l_untergrup.zwkum
                        bezeich = l_untergrup.bezeich

                    if show_price:
                        tot_val =  to_decimal(l_bestand.val_anf_best) + to_decimal(l_bestand.wert_eingang) - to_decimal(l_bestand.wert_ausgang)
                    tot_anz =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)

                    if l_artikel.anzverbrauch != 0:
                        must_order =  to_decimal(l_artikel.anzverbrauch) - to_decimal(tot_anz)
                    t_anz =  to_decimal(t_anz) + to_decimal(tot_anz)

                    if show_price:
                        t_val =  to_decimal(t_val) + to_decimal(tot_val)
                        t_value =  to_decimal(t_value) + to_decimal(tot_val)
                        tt_val =  to_decimal(tt_val) + to_decimal(tot_val)
                        tt_value =  to_decimal(tt_value) + to_decimal(tot_val)

                    if tot_anz != 0 or (tot_anz == 0 and zero_flag):
                        str_list = Str_list()
                        str_list_list.append(str_list)


                        if show_price:

                            if not long_digit:
                                str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensorte, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(l_artikel.ek_letzter, ">>>,>>>,>>9.99") + to_string(l_artikel.ek_aktuell, ">>>,>>>,>>9.99") + to_string(l_artikel.vk_preis, "->>,>>>,>>9.99") + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_val, "->>>,>>>,>>9.99") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                            else:
                                str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensorte, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(l_artikel.ek_letzter, ">,>>>,>>>,>>9") + to_string(l_artikel.ek_aktuell, ">,>>>,>>>,>>9") + to_string(l_artikel.vk_preis, "->,>>>,>>>,>>9") + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_val, "->>,>>>,>>>,>>9") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                        else:

                            if not long_digit:
                                str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensorte, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(tot_anz, "->,>>>,>>9.99") + to_string(0, "->>>,>>>,>>9.99") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                            else:
                                str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensorte, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(0, ">,>>>,>>>,>>9") + to_string(0, ">,>>>,>>>,>>9") + to_string(0, ">,>>>,>>>,>>9") + to_string(tot_anz, "->,>>>,>>9.99") + to_string(0, "->>,>>>,>>>,>>9") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")

        else:

            l_bestand_obj_list = {}
            l_bestand = L_bestand()
            l_artikel = L_artikel()
            l_untergrup = L_untergrup()
            for l_bestand.anz_anf_best, l_bestand.anz_eingang, l_bestand.anz_ausgang, l_bestand.val_anf_best, l_bestand.wert_eingang, l_bestand.wert_ausgang, l_bestand._recid, l_artikel.zwkum, l_artikel.anzverbrauch, l_artikel.artnr, l_artikel.bezeich, l_artikel.masseinheit, l_artikel.inhalt, l_artikel.traubensorte, l_artikel.lief_einheit, l_artikel.ek_letzter, l_artikel.ek_aktuell, l_artikel.vk_preis, l_artikel.min_bestand, l_artikel._recid, l_untergrup.bezeich, l_untergrup.zwkum, l_untergrup._recid in db_session.query(L_bestand.anz_anf_best, L_bestand.anz_eingang, L_bestand.anz_ausgang, L_bestand.val_anf_best, L_bestand.wert_eingang, L_bestand.wert_ausgang, L_bestand._recid, L_artikel.zwkum, L_artikel.anzverbrauch, L_artikel.artnr, L_artikel.bezeich, L_artikel.masseinheit, L_artikel.inhalt, L_artikel.traubensorte, L_artikel.lief_einheit, L_artikel.ek_letzter, L_artikel.ek_aktuell, L_artikel.vk_preis, L_artikel.min_bestand, L_artikel._recid, L_untergrup.bezeich, L_untergrup.zwkum, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_bestand.artnr)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                         (L_bestand.lager_nr == 0)).order_by(L_artikel.zwkum, L_artikel.artnr).all():
                if l_bestand_obj_list.get(l_bestand._recid):
                    continue
                else:
                    l_bestand_obj_list[l_bestand._recid] = True


                i = i + 1
                must_order =  to_decimal("0")

                if zwkum == 0:
                    zwkum = l_artikel.zwkum
                    bezeich = l_untergrup.bezeich

                if zwkum != l_artikel.zwkum:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.flag = 1
                    str_list.s = " "
                    str_list.s = str_list.s + to_string(bezeich, "x(50)")
                    for j in range(1,84 + 1) :
                        str_list.s = str_list.s + " "

                    if not long_digit:
                        str_list.s = str_list.s + to_string(t_val, "->>>,>>>,>>9.99")
                    else:
                        str_list.s = str_list.s + to_string(t_val, "->>,>>>,>>>,>>9")
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    t_anz =  to_decimal("0")
                    t_val =  to_decimal("0")
                    must_order =  to_decimal("0")
                    zwkum = l_untergrup.zwkum
                    bezeich = l_untergrup.bezeich

                if show_price:
                    tot_val =  to_decimal(l_bestand.val_anf_best) + to_decimal(l_bestand.wert_eingang) - to_decimal(l_bestand.wert_ausgang)
                tot_anz =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)

                if l_artikel.anzverbrauch != 0:
                    must_order =  to_decimal(l_artikel.anzverbrauch) - to_decimal(tot_anz)
                t_anz =  to_decimal(t_anz) + to_decimal(tot_anz)

                if show_price:
                    t_val =  to_decimal(t_val) + to_decimal(tot_val)
                    t_value =  to_decimal(t_value) + to_decimal(tot_val)
                    tt_val =  to_decimal(tt_val) + to_decimal(tot_val)
                    tt_value =  to_decimal(tt_value) + to_decimal(tot_val)

                if tot_anz != 0 or (tot_anz == 0 and zero_flag):
                    str_list = Str_list()
                    str_list_list.append(str_list)


                    if show_price:

                        if not long_digit:
                            str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensorte, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(l_artikel.ek_letzter, ">>>,>>>,>>9.99") + to_string(l_artikel.ek_aktuell, ">>>,>>>,>>9.99") + to_string(l_artikel.vk_preis, "->>,>>>,>>9.99") + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_val, "->>>,>>>,>>9.99") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                        else:
                            str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensorte, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(l_artikel.ek_letzter, ">,>>>,>>>,>>9") + to_string(l_artikel.ek_aktuell, ">,>>>,>>>,>>9") + to_string(l_artikel.vk_preis, "->,>>>,>>>,>>9") + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_val, "->>,>>>,>>>,>>9") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                    else:

                        if not long_digit:
                            str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensorte, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(tot_anz, "->,>>>,>>9.99") + to_string(0, "->>>,>>>,>>9.99") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                        else:
                            str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensorte, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(0, ">,>>>,>>>,>>9") + to_string(0, ">,>>>,>>>,>>9") + to_string(0, ">,>>>,>>>,>>9") + to_string(tot_anz, "->,>>>,>>9.99") + to_string(0, "->>,>>>,>>>,>>9") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")


        elif sorttype == 2:

            if sub_grp != 000:

                l_bestand_obj_list = {}
                l_bestand = L_bestand()
                l_artikel = L_artikel()
                l_untergrup = L_untergrup()
                for l_bestand.anz_anf_best, l_bestand.anz_eingang, l_bestand.anz_ausgang, l_bestand.val_anf_best, l_bestand.wert_eingang, l_bestand.wert_ausgang, l_bestand._recid, l_artikel.zwkum, l_artikel.anzverbrauch, l_artikel.artnr, l_artikel.bezeich, l_artikel.masseinheit, l_artikel.inhalt, l_artikel.traubensorte, l_artikel.lief_einheit, l_artikel.ek_letzter, l_artikel.ek_aktuell, l_artikel.vk_preis, l_artikel.min_bestand, l_artikel._recid, l_untergrup.bezeich, l_untergrup.zwkum, l_untergrup._recid in db_session.query(L_bestand.anz_anf_best, L_bestand.anz_eingang, L_bestand.anz_ausgang, L_bestand.val_anf_best, L_bestand.wert_eingang, L_bestand.wert_ausgang, L_bestand._recid, L_artikel.zwkum, L_artikel.anzverbrauch, L_artikel.artnr, L_artikel.bezeich, L_artikel.masseinheit, L_artikel.inhalt, L_artikel.traubensorte, L_artikel.lief_einheit, L_artikel.ek_letzter, L_artikel.ek_aktuell, L_artikel.vk_preis, L_artikel.min_bestand, L_artikel._recid, L_untergrup.bezeich, L_untergrup.zwkum, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_bestand.artnr) & (L_artikel.zwkum == sub_grp)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                             (L_bestand.lager_nr == 0)).order_by(L_artikel.zwkum, L_artikel.bezeich).all():
                    if l_bestand_obj_list.get(l_bestand._recid):
                        continue
                    else:
                        l_bestand_obj_list[l_bestand._recid] = True


                    i = i + 1
                    must_order =  to_decimal("0")

                    if zwkum == 0:
                        zwkum = l_artikel.zwkum
                        bezeich = l_untergrup.bezeich

                    if zwkum != l_artikel.zwkum:
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        str_list.flag = 1
                        str_list.s = " "
                        str_list.s = str_list.s + to_string(bezeich, "x(50)")
                        for j in range(1,84 + 1) :
                            str_list.s = str_list.s + " "

                        if not long_digit:
                            str_list.s = str_list.s + to_string(t_val, "->>>,>>>,>>9.99")
                        else:
                            str_list.s = str_list.s + to_string(t_val, "->>,>>>,>>>,>>9")
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        t_anz =  to_decimal("0")
                        t_val =  to_decimal("0")
                        zwkum = l_untergrup.zwkum
                        bezeich = l_untergrup.bezeich

                    if show_price:
                        tot_val =  to_decimal(l_bestand.val_anf_best) + to_decimal(l_bestand.wert_eingang) - to_decimal(l_bestand.wert_ausgang)
                    tot_anz =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)

                    if l_artikel.anzverbrauch != 0:
                        must_order =  to_decimal(l_artikel.anzverbrauch) - to_decimal(tot_anz)
                    t_anz =  to_decimal(t_anz) + to_decimal(tot_anz)

                    if show_price:
                        t_val =  to_decimal(t_val) + to_decimal(tot_val)
                        t_value =  to_decimal(t_value) + to_decimal(tot_val)
                        tt_val =  to_decimal(tt_val) + to_decimal(tot_val)
                        tt_value =  to_decimal(tt_value) + to_decimal(tot_val)

                    if tot_anz != 0 or (tot_anz == 0 and zero_flag):
                        str_list = Str_list()
                        str_list_list.append(str_list)


                        if show_price:

                            if not long_digit:
                                str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensorte, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(l_artikel.ek_letzter, ">>>,>>>,>>9.99") + to_string(l_artikel.ek_aktuell, ">>>,>>>,>>9.99") + to_string(l_artikel.vk_preis, "->>,>>>,>>9.99") + to_string(tot_anz, " ->>>,>>9.99") + to_string(tot_val, "->>>,>>>,>>9.99") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                            else:
                                str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensorte, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(l_artikel.ek_letzter, ">,>>>,>>>,>>9") + to_string(l_artikel.ek_aktuell, ">,>>>,>>>,>>9") + to_string(l_artikel.vk_preis, "->,>>>,>>>,>>9") + to_string(tot_anz, " ->>>,>>9.99") + to_string(tot_val, "->>,>>>,>>>,>>9") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                        else:

                            if not long_digit:
                                str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensorte, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(tot_anz, " ->>>,>>9.99") + to_string(0, "->>>,>>>,>>9.99") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                            else:
                                str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensorte, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(0, ">,>>>,>>>,>>9") + to_string(0, ">,>>>,>>>,>>9") + to_string(0, ">,>>>,>>>,>>9") + to_string(tot_anz, " ->>>,>>9.99") + to_string(0, "->>,>>>,>>>,>>9") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")

        else:

            l_bestand_obj_list = {}
            l_bestand = L_bestand()
            l_artikel = L_artikel()
            l_untergrup = L_untergrup()
            for l_bestand.anz_anf_best, l_bestand.anz_eingang, l_bestand.anz_ausgang, l_bestand.val_anf_best, l_bestand.wert_eingang, l_bestand.wert_ausgang, l_bestand._recid, l_artikel.zwkum, l_artikel.anzverbrauch, l_artikel.artnr, l_artikel.bezeich, l_artikel.masseinheit, l_artikel.inhalt, l_artikel.traubensorte, l_artikel.lief_einheit, l_artikel.ek_letzter, l_artikel.ek_aktuell, l_artikel.vk_preis, l_artikel.min_bestand, l_artikel._recid, l_untergrup.bezeich, l_untergrup.zwkum, l_untergrup._recid in db_session.query(L_bestand.anz_anf_best, L_bestand.anz_eingang, L_bestand.anz_ausgang, L_bestand.val_anf_best, L_bestand.wert_eingang, L_bestand.wert_ausgang, L_bestand._recid, L_artikel.zwkum, L_artikel.anzverbrauch, L_artikel.artnr, L_artikel.bezeich, L_artikel.masseinheit, L_artikel.inhalt, L_artikel.traubensorte, L_artikel.lief_einheit, L_artikel.ek_letzter, L_artikel.ek_aktuell, L_artikel.vk_preis, L_artikel.min_bestand, L_artikel._recid, L_untergrup.bezeich, L_untergrup.zwkum, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_bestand.artnr)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                         (L_bestand.lager_nr == 0)).order_by(L_artikel.zwkum, L_artikel.bezeich).all():
                if l_bestand_obj_list.get(l_bestand._recid):
                    continue
                else:
                    l_bestand_obj_list[l_bestand._recid] = True


                i = i + 1
                must_order =  to_decimal("0")

                if zwkum == 0:
                    zwkum = l_artikel.zwkum
                    bezeich = l_untergrup.bezeich

                if zwkum != l_artikel.zwkum:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.flag = 1
                    str_list.s = " "
                    str_list.s = str_list.s + to_string(bezeich, "x(50)")
                    for j in range(1,84 + 1) :
                        str_list.s = str_list.s + " "

                    if not long_digit:
                        str_list.s = str_list.s + to_string(t_val, "->>>,>>>,>>9.99")
                    else:
                        str_list.s = str_list.s + to_string(t_val, "->>,>>>,>>>,>>9")
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    t_anz =  to_decimal("0")
                    t_val =  to_decimal("0")
                    zwkum = l_untergrup.zwkum
                    bezeich = l_untergrup.bezeich

                if show_price:
                    tot_val =  to_decimal(l_bestand.val_anf_best) + to_decimal(l_bestand.wert_eingang) - to_decimal(l_bestand.wert_ausgang)
                tot_anz =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)

                if l_artikel.anzverbrauch != 0:
                    must_order =  to_decimal(l_artikel.anzverbrauch) - to_decimal(tot_anz)
                t_anz =  to_decimal(t_anz) + to_decimal(tot_anz)

                if show_price:
                    t_val =  to_decimal(t_val) + to_decimal(tot_val)
                    t_value =  to_decimal(t_value) + to_decimal(tot_val)
                    tt_val =  to_decimal(tt_val) + to_decimal(tot_val)
                    tt_value =  to_decimal(tt_value) + to_decimal(tot_val)

                if tot_anz != 0 or (tot_anz == 0 and zero_flag):
                    str_list = Str_list()
                    str_list_list.append(str_list)


                    if show_price:

                        if not long_digit:
                            str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensorte, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(l_artikel.ek_letzter, ">>>,>>>,>>9.99") + to_string(l_artikel.ek_aktuell, ">>>,>>>,>>9.99") + to_string(l_artikel.vk_preis, "->>,>>>,>>9.99") + to_string(tot_anz, " ->>>,>>9.99") + to_string(tot_val, "->>>,>>>,>>9.99") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                        else:
                            str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensorte, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(l_artikel.ek_letzter, ">,>>>,>>>,>>9") + to_string(l_artikel.ek_aktuell, ">,>>>,>>>,>>9") + to_string(l_artikel.vk_preis, "->,>>>,>>>,>>9") + to_string(tot_anz, " ->>>,>>9.99") + to_string(tot_val, "->>,>>>,>>>,>>9") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                    else:

                        if not long_digit:
                            str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensorte, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(tot_anz, " ->>>,>>9.99") + to_string(0, "->>>,>>>,>>9.99") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                        else:
                            str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensorte, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(0, ">,>>>,>>>,>>9") + to_string(0, ">,>>>,>>>,>>9") + to_string(0, ">,>>>,>>>,>>9") + to_string(tot_anz, " ->>>,>>9.99") + to_string(0, "->>,>>>,>>>,>>9") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")


        if t_val != 0:
            str_list = Str_list()
            str_list_list.append(str_list)

            str_list.flag = 1
            str_list.s = " "
            str_list.s = str_list.s + to_string(bezeich, "x(50)")
            for j in range(1,84 + 1) :
                str_list.s = str_list.s + " "

            if not long_digit:
                str_list.s = str_list.s + to_string(t_val, "->>>,>>>,>>9.99")
            else:
                str_list.s = str_list.s + to_string(t_val, "->>,>>>,>>>,>>9")
            str_list = Str_list()
            str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.flag = 1
        str_list.s = " "
        str_list.s = str_list.s + to_string("GRAND T O T A L", "x(50)")
        for j in range(1,84 + 1) :
            str_list.s = str_list.s + " "

        if not long_digit:
            str_list.s = str_list.s + to_string(tt_value, "->>>,>>>,>>9.99")
        else:
            str_list.s = str_list.s + to_string(tt_value, "->>,>>>,>>>,>>9")


    def create_list1():

        nonlocal str_list_list, long_digit, htparam, l_bestand, l_lager, l_artikel, l_untergrup
        nonlocal all_flag, show_price, zero_flag, from_grp, sub_grp, from_lager, to_lager, sorttype, mattype


        nonlocal str_list
        nonlocal str_list_list

        i:int = 0
        j:int = 0
        tot_anz:Decimal = to_decimal("0.0")
        tot_val:Decimal = to_decimal("0.0")
        t_anz:Decimal = to_decimal("0.0")
        t_val:Decimal = to_decimal("0.0")
        t_value:Decimal = to_decimal("0.0")
        tt_value:Decimal = to_decimal("0.0")
        avrg_price:Decimal = to_decimal("0.0")
        zwkum:int = 0
        bezeich:string = ""
        grp1:int = 0
        grp2:int = 1
        must_order:Decimal = to_decimal("0.0")
        tt_val:Decimal = to_decimal("0.0")
        qty:Decimal = to_decimal("0.0")
        wert:Decimal = to_decimal("0.0")
        l_oh = None
        tot_bezeich:string = ""
        L_oh =  create_buffer("L_oh",L_bestand)
        str_list_list.clear()

        if mattype == 1:
            grp2 = 0

        elif mattype == 2:
            grp1 = 1

        for l_lager in db_session.query(L_lager).filter(
                 (L_lager.lager_nr >= from_lager) & (L_lager.lager_nr <= to_lager)).order_by(L_lager._recid).all():
            i = 0
            zwkum = 0
            t_anz =  to_decimal("0")
            t_val =  to_decimal("0")
            tt_val =  to_decimal("0")
            tot_bezeich = "Ttl - " + l_lager.bezeich

            if sorttype == 1:

                if sub_grp != 000:

                    l_bestand_obj_list = {}
                    l_bestand = L_bestand()
                    l_artikel = L_artikel()
                    l_oh = L_bestand()
                    l_untergrup = L_untergrup()
                    for l_bestand.anz_anf_best, l_bestand.anz_eingang, l_bestand.anz_ausgang, l_bestand.val_anf_best, l_bestand.wert_eingang, l_bestand.wert_ausgang, l_bestand._recid, l_artikel.zwkum, l_artikel.anzverbrauch, l_artikel.artnr, l_artikel.bezeich, l_artikel.masseinheit, l_artikel.inhalt, l_artikel.traubensorte, l_artikel.lief_einheit, l_artikel.ek_letzter, l_artikel.ek_aktuell, l_artikel.vk_preis, l_artikel.min_bestand, l_artikel._recid, l_oh.anz_anf_best, l_oh.anz_eingang, l_oh.anz_ausgang, l_oh.val_anf_best, l_oh.wert_eingang, l_oh.wert_ausgang, l_oh._recid, l_untergrup.bezeich, l_untergrup.zwkum, l_untergrup._recid in db_session.query(L_bestand.anz_anf_best, L_bestand.anz_eingang, L_bestand.anz_ausgang, L_bestand.val_anf_best, L_bestand.wert_eingang, L_bestand.wert_ausgang, L_bestand._recid, L_artikel.zwkum, L_artikel.anzverbrauch, L_artikel.artnr, L_artikel.bezeich, L_artikel.masseinheit, L_artikel.inhalt, L_artikel.traubensorte, L_artikel.lief_einheit, L_artikel.ek_letzter, L_artikel.ek_aktuell, L_artikel.vk_preis, L_artikel.min_bestand, L_artikel._recid, L_oh.anz_anf_best, L_oh.anz_eingang, L_oh.anz_ausgang, L_oh.val_anf_best, L_oh.wert_eingang, L_oh.wert_ausgang, L_oh._recid, L_untergrup.bezeich, L_untergrup.zwkum, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_bestand.artnr) & (L_artikel.zwkum == sub_grp)).join(L_oh,(L_oh.artnr == L_bestand.artnr) & (L_oh.lager_nr == 0)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum) & ((L_untergrup.betriebsnr >= grp1) & (L_untergrup.betriebsnr <= grp2))).filter(
                             (L_bestand.lager_nr == l_lager.lager_nr)).order_by(L_artikel.zwkum, L_artikel.artnr).all():
                        if l_bestand_obj_list.get(l_bestand._recid):
                            continue
                        else:
                            l_bestand_obj_list[l_bestand._recid] = True


                        i = i + 1
                        must_order =  to_decimal("0")

                        if i == 1:
                            str_list = Str_list()
                            str_list_list.append(str_list)

                            str_list.s = " " + to_string(l_lager.lager_nr, "99") + " " + to_string(l_lager.bezeich, "x(50)")

                        if zwkum == 0:
                            zwkum = l_artikel.zwkum
                            bezeich = l_untergrup.bezeich

                        if zwkum != l_artikel.zwkum:
                            str_list = Str_list()
                            str_list_list.append(str_list)

                            str_list.flag = 1
                            str_list.s = " "
                            str_list.s = str_list.s + to_string(bezeich, "x(50)")
                            for j in range(1,84 + 1) :
                                str_list.s = str_list.s + " "

                            if not long_digit:
                                str_list.s = str_list.s + to_string(t_val, "->>>,>>>,>>9.99")
                            else:
                                str_list.s = str_list.s + to_string(t_val, "->>,>>>,>>>,>>9")
                            str_list = Str_list()
                            str_list_list.append(str_list)

                            t_anz =  to_decimal("0")
                            t_val =  to_decimal("0")
                            zwkum = l_untergrup.zwkum
                            bezeich = l_untergrup.bezeich
                        qty =  to_decimal(l_oh.anz_anf_best) + to_decimal(l_oh.anz_eingang) - to_decimal(l_oh.anz_ausgang)

                        if show_price:
                            wert =  to_decimal(l_oh.val_anf_best) + to_decimal(l_oh.wert_eingang) - to_decimal(l_oh.wert_ausgang)
                        tot_anz =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)

                        if l_artikel.anzverbrauch != 0:
                            must_order =  to_decimal(l_artikel.anzverbrauch) - to_decimal(tot_anz)

                        if qty != 0:
                            tot_val =  to_decimal(wert) * to_decimal(tot_anz) / to_decimal(qty)
                        else:
                            tot_val =  to_decimal("0")
                        t_anz =  to_decimal(t_anz) + to_decimal(tot_anz)

                        if show_price:
                            t_val =  to_decimal(t_val) + to_decimal(tot_val)
                            t_value =  to_decimal(t_value) + to_decimal(tot_val)
                            tt_val =  to_decimal(tt_val) + to_decimal(tot_val)
                            tt_value =  to_decimal(tt_value) + to_decimal(tot_val)

                        if tot_anz != 0 or (tot_anz == 0 and zero_flag):
                            str_list = Str_list()
                            str_list_list.append(str_list)


                            if show_price:

                                if not long_digit:
                                    str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensorte, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(l_artikel.ek_letzter, ">>>,>>>,>>9.99") + to_string(l_artikel.ek_aktuell, ">>>,>>>,>>9.99") + to_string(l_artikel.vk_preis, "->>,>>>,>>9.99") + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_val, "->>>,>>>,>>9.99") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                                else:
                                    str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensorte, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(l_artikel.ek_letzter, ">,>>>,>>>,>>9") + to_string(l_artikel.ek_aktuell, ">,>>>,>>>,>>9") + to_string(l_artikel.vk_preis, "->,>>>,>>>,>>9") + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_val, "->>,>>>,>>>,>>9") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                            else:

                                if not long_digit:
                                    str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensorte, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(tot_anz, "->,>>>,>>9.99") + to_string(0, "->>>,>>>,>>9.99") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                                else:
                                    str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensorte, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(0, ">,>>>,>>>,>>9") + to_string(0, ">,>>>,>>>,>>9") + to_string(0, ">,>>>,>>>,>>9") + to_string(tot_anz, "->,>>>,>>9.99") + to_string(0, "->>,>>>,>>>,>>9") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")

            else:

                l_bestand_obj_list = {}
                l_bestand = L_bestand()
                l_artikel = L_artikel()
                l_oh = L_bestand()
                l_untergrup = L_untergrup()
                for l_bestand.anz_anf_best, l_bestand.anz_eingang, l_bestand.anz_ausgang, l_bestand.val_anf_best, l_bestand.wert_eingang, l_bestand.wert_ausgang, l_bestand._recid, l_artikel.zwkum, l_artikel.anzverbrauch, l_artikel.artnr, l_artikel.bezeich, l_artikel.masseinheit, l_artikel.inhalt, l_artikel.traubensorte, l_artikel.lief_einheit, l_artikel.ek_letzter, l_artikel.ek_aktuell, l_artikel.vk_preis, l_artikel.min_bestand, l_artikel._recid, l_oh.anz_anf_best, l_oh.anz_eingang, l_oh.anz_ausgang, l_oh.val_anf_best, l_oh.wert_eingang, l_oh.wert_ausgang, l_oh._recid, l_untergrup.bezeich, l_untergrup.zwkum, l_untergrup._recid in db_session.query(L_bestand.anz_anf_best, L_bestand.anz_eingang, L_bestand.anz_ausgang, L_bestand.val_anf_best, L_bestand.wert_eingang, L_bestand.wert_ausgang, L_bestand._recid, L_artikel.zwkum, L_artikel.anzverbrauch, L_artikel.artnr, L_artikel.bezeich, L_artikel.masseinheit, L_artikel.inhalt, L_artikel.traubensorte, L_artikel.lief_einheit, L_artikel.ek_letzter, L_artikel.ek_aktuell, L_artikel.vk_preis, L_artikel.min_bestand, L_artikel._recid, L_oh.anz_anf_best, L_oh.anz_eingang, L_oh.anz_ausgang, L_oh.val_anf_best, L_oh.wert_eingang, L_oh.wert_ausgang, L_oh._recid, L_untergrup.bezeich, L_untergrup.zwkum, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_bestand.artnr) & (L_artikel.endkum == from_grp)).join(L_oh,(L_oh.artnr == L_bestand.artnr) & (L_oh.lager_nr == 0)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum) & ((L_untergrup.betriebsnr >= grp1) & (L_untergrup.betriebsnr <= grp2))).filter(
                         (L_bestand.lager_nr == l_lager.lager_nr)).order_by(L_artikel.zwkum, L_artikel.artnr).all():
                    if l_bestand_obj_list.get(l_bestand._recid):
                        continue
                    else:
                        l_bestand_obj_list[l_bestand._recid] = True


                    i = i + 1
                    must_order =  to_decimal("0")

                    if i == 1:
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        str_list.s = " " + to_string(l_lager.lager_nr, "99") + " " + to_string(l_lager.bezeich, "x(50)")

                    if zwkum == 0:
                        zwkum = l_artikel.zwkum
                        bezeich = l_untergrup.bezeich

                    if zwkum != l_artikel.zwkum:
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        str_list.flag = 1
                        str_list.s = " "
                        str_list.s = str_list.s + to_string(bezeich, "x(50)")
                        for j in range(1,84 + 1) :
                            str_list.s = str_list.s + " "

                        if not long_digit:
                            str_list.s = str_list.s + to_string(t_val, "->>>,>>>,>>9.99")
                        else:
                            str_list.s = str_list.s + to_string(t_val, "->>,>>>,>>>,>>9")
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        t_anz =  to_decimal("0")
                        t_val =  to_decimal("0")
                        zwkum = l_untergrup.zwkum
                        bezeich = l_untergrup.bezeich
                    qty =  to_decimal(l_oh.anz_anf_best) + to_decimal(l_oh.anz_eingang) - to_decimal(l_oh.anz_ausgang)

                    if show_price:
                        wert =  to_decimal(l_oh.val_anf_best) + to_decimal(l_oh.wert_eingang) - to_decimal(l_oh.wert_ausgang)
                    tot_anz =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)

                    if l_artikel.anzverbrauch != 0:
                        must_order =  to_decimal(l_artikel.anzverbrauch) - to_decimal(tot_anz)

                    if qty != 0:
                        tot_val =  to_decimal(wert) * to_decimal(tot_anz) / to_decimal(qty)
                    else:
                        tot_val =  to_decimal("0")
                    t_anz =  to_decimal(t_anz) + to_decimal(tot_anz)

                    if show_price:
                        t_val =  to_decimal(t_val) + to_decimal(tot_val)
                        t_value =  to_decimal(t_value) + to_decimal(tot_val)
                        tt_val =  to_decimal(tt_val) + to_decimal(tot_val)
                        tt_value =  to_decimal(tt_value) + to_decimal(tot_val)

                    if tot_anz != 0 or (tot_anz == 0 and zero_flag):
                        str_list = Str_list()
                        str_list_list.append(str_list)


                        if show_price:

                            if not long_digit:
                                str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensorte, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(l_artikel.ek_letzter, ">>>,>>>,>>9.99") + to_string(l_artikel.ek_aktuell, ">>>,>>>,>>9.99") + to_string(l_artikel.vk_preis, "->>,>>>,>>9.99") + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_val, "->>>,>>>,>>9.99") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                            else:
                                str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensorte, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(l_artikel.ek_letzter, ">,>>>,>>>,>>9") + to_string(l_artikel.ek_aktuell, ">,>>>,>>>,>>9") + to_string(l_artikel.vk_preis, "->,>>>,>>>,>>9") + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_val, "->>,>>>,>>>,>>9") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                        else:

                            if not long_digit:
                                str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensorte, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(tot_anz, "->,>>>,>>9.99") + to_string(0, "->>>,>>>,>>9.99") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                            else:
                                str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensorte, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(0, ">,>>>,>>>,>>9") + to_string(0, ">,>>>,>>>,>>9") + to_string(0, ">,>>>,>>>,>>9") + to_string(tot_anz, "->,>>>,>>9.99") + to_string(0, "->>,>>>,>>>,>>9") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")


            elif sorttype == 2:

                if sub_grp != 000:

                    l_bestand_obj_list = {}
                    l_bestand = L_bestand()
                    l_artikel = L_artikel()
                    l_oh = L_bestand()
                    l_untergrup = L_untergrup()
                    for l_bestand.anz_anf_best, l_bestand.anz_eingang, l_bestand.anz_ausgang, l_bestand.val_anf_best, l_bestand.wert_eingang, l_bestand.wert_ausgang, l_bestand._recid, l_artikel.zwkum, l_artikel.anzverbrauch, l_artikel.artnr, l_artikel.bezeich, l_artikel.masseinheit, l_artikel.inhalt, l_artikel.traubensorte, l_artikel.lief_einheit, l_artikel.ek_letzter, l_artikel.ek_aktuell, l_artikel.vk_preis, l_artikel.min_bestand, l_artikel._recid, l_oh.anz_anf_best, l_oh.anz_eingang, l_oh.anz_ausgang, l_oh.val_anf_best, l_oh.wert_eingang, l_oh.wert_ausgang, l_oh._recid, l_untergrup.bezeich, l_untergrup.zwkum, l_untergrup._recid in db_session.query(L_bestand.anz_anf_best, L_bestand.anz_eingang, L_bestand.anz_ausgang, L_bestand.val_anf_best, L_bestand.wert_eingang, L_bestand.wert_ausgang, L_bestand._recid, L_artikel.zwkum, L_artikel.anzverbrauch, L_artikel.artnr, L_artikel.bezeich, L_artikel.masseinheit, L_artikel.inhalt, L_artikel.traubensorte, L_artikel.lief_einheit, L_artikel.ek_letzter, L_artikel.ek_aktuell, L_artikel.vk_preis, L_artikel.min_bestand, L_artikel._recid, L_oh.anz_anf_best, L_oh.anz_eingang, L_oh.anz_ausgang, L_oh.val_anf_best, L_oh.wert_eingang, L_oh.wert_ausgang, L_oh._recid, L_untergrup.bezeich, L_untergrup.zwkum, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_bestand.artnr) & (L_artikel.zwkum == sub_grp)).join(L_oh,(L_oh.artnr == L_bestand.artnr) & (L_oh.lager_nr == 0)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum) & ((L_untergrup.betriebsnr >= grp1) & (L_untergrup.betriebsnr <= grp2))).filter(
                             (L_bestand.lager_nr == l_lager.lager_nr)).order_by(L_artikel.zwkum, L_artikel.bezeich).all():
                        if l_bestand_obj_list.get(l_bestand._recid):
                            continue
                        else:
                            l_bestand_obj_list[l_bestand._recid] = True


                        i = i + 1
                        must_order =  to_decimal("0")

                        if i == 1:
                            str_list = Str_list()
                            str_list_list.append(str_list)

                            str_list.s = " " + to_string(l_lager.lager_nr, "99") + " " + to_string(l_lager.bezeich, "x(13)")

                        if zwkum == 0:
                            zwkum = l_artikel.zwkum
                            bezeich = l_untergrup.bezeich

                        if zwkum != l_artikel.zwkum:
                            str_list = Str_list()
                            str_list_list.append(str_list)

                            str_list.flag = 1
                            str_list.s = " "
                            str_list.s = str_list.s + to_string(bezeich, "x(50)")
                            for j in range(1,84 + 1) :
                                str_list.s = str_list.s + " "

                            if not long_digit:
                                str_list.s = str_list.s + to_string(t_val, "->>>,>>>,>>9.99")
                            else:
                                str_list.s = str_list.s + to_string(t_val, "->>,>>>,>>>,>>9")
                            str_list = Str_list()
                            str_list_list.append(str_list)

                            t_anz =  to_decimal("0")
                            t_val =  to_decimal("0")
                            zwkum = l_untergrup.zwkum
                            bezeich = l_untergrup.bezeich
                        qty =  to_decimal(l_oh.anz_anf_best) + to_decimal(l_oh.anz_eingang) - to_decimal(l_oh.anz_ausgang)

                        if show_price:
                            wert =  to_decimal(l_oh.val_anf_best) + to_decimal(l_oh.wert_eingang) - to_decimal(l_oh.wert_ausgang)
                        tot_anz =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)

                        if l_artikel.anzverbrauch != 0:
                            must_order =  to_decimal(l_artikel.anzverbrauch) - to_decimal(tot_anz)

                        if qty != 0:
                            tot_val =  to_decimal(wert) * to_decimal(tot_anz) / to_decimal(qty)
                        else:
                            tot_val =  to_decimal("0")
                        t_anz =  to_decimal(t_anz) + to_decimal(tot_anz)

                        if show_price:
                            t_val =  to_decimal(t_val) + to_decimal(tot_val)
                            t_value =  to_decimal(t_value) + to_decimal(tot_val)
                            tt_val =  to_decimal(tt_val) + to_decimal(tot_val)
                            tt_value =  to_decimal(tt_value) + to_decimal(tot_val)

                        if tot_anz != 0 or (tot_anz == 0 and zero_flag):
                            str_list = Str_list()
                            str_list_list.append(str_list)


                            if show_price:

                                if not long_digit:
                                    str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensorte, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(l_artikel.ek_letzter, ">>>,>>>,>>9.99") + to_string(l_artikel.ek_aktuell, ">>>,>>>,>>9.99") + to_string(l_artikel.vk_preis, "->>,>>>,>>9.99") + to_string(tot_anz, " ->>>,>>9.99") + to_string(tot_val, "->>>,>>>,>>9.99") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                                else:
                                    str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensorte, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(l_artikel.ek_letzter, ">,>>>,>>>,>>9") + to_string(l_artikel.ek_aktuell, ">,>>>,>>>,>>9") + to_string(l_artikel.vk_preis, "->,>>>,>>>,>>9") + to_string(tot_anz, " ->>>,>>9.99") + to_string(tot_val, "->>,>>>,>>>,>>9") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                            else:

                                if not long_digit:
                                    str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensorte, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(tot_anz, " ->>>,>>9.99") + to_string(0, "->>>,>>>,>>9.99") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                                else:
                                    str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensorte, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(0, ">,>>>,>>>,>>9") + to_string(0, ">,>>>,>>>,>>9") + to_string(0, ">,>>>,>>>,>>9") + to_string(tot_anz, " ->>>,>>9.99") + to_string(0, "->>,>>>,>>>,>>9") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")

            else:

                l_bestand_obj_list = {}
                l_bestand = L_bestand()
                l_artikel = L_artikel()
                l_oh = L_bestand()
                l_untergrup = L_untergrup()
                for l_bestand.anz_anf_best, l_bestand.anz_eingang, l_bestand.anz_ausgang, l_bestand.val_anf_best, l_bestand.wert_eingang, l_bestand.wert_ausgang, l_bestand._recid, l_artikel.zwkum, l_artikel.anzverbrauch, l_artikel.artnr, l_artikel.bezeich, l_artikel.masseinheit, l_artikel.inhalt, l_artikel.traubensorte, l_artikel.lief_einheit, l_artikel.ek_letzter, l_artikel.ek_aktuell, l_artikel.vk_preis, l_artikel.min_bestand, l_artikel._recid, l_oh.anz_anf_best, l_oh.anz_eingang, l_oh.anz_ausgang, l_oh.val_anf_best, l_oh.wert_eingang, l_oh.wert_ausgang, l_oh._recid, l_untergrup.bezeich, l_untergrup.zwkum, l_untergrup._recid in db_session.query(L_bestand.anz_anf_best, L_bestand.anz_eingang, L_bestand.anz_ausgang, L_bestand.val_anf_best, L_bestand.wert_eingang, L_bestand.wert_ausgang, L_bestand._recid, L_artikel.zwkum, L_artikel.anzverbrauch, L_artikel.artnr, L_artikel.bezeich, L_artikel.masseinheit, L_artikel.inhalt, L_artikel.traubensorte, L_artikel.lief_einheit, L_artikel.ek_letzter, L_artikel.ek_aktuell, L_artikel.vk_preis, L_artikel.min_bestand, L_artikel._recid, L_oh.anz_anf_best, L_oh.anz_eingang, L_oh.anz_ausgang, L_oh.val_anf_best, L_oh.wert_eingang, L_oh.wert_ausgang, L_oh._recid, L_untergrup.bezeich, L_untergrup.zwkum, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_bestand.artnr) & (L_artikel.endkum == from_grp)).join(L_oh,(L_oh.artnr == L_bestand.artnr) & (L_oh.lager_nr == 0)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum) & ((L_untergrup.betriebsnr >= grp1) & (L_untergrup.betriebsnr <= grp2))).filter(
                         (L_bestand.lager_nr == l_lager.lager_nr)).order_by(L_artikel.zwkum, L_artikel.bezeich).all():
                    if l_bestand_obj_list.get(l_bestand._recid):
                        continue
                    else:
                        l_bestand_obj_list[l_bestand._recid] = True


                    i = i + 1
                    must_order =  to_decimal("0")

                    if i == 1:
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        str_list.s = " " + to_string(l_lager.lager_nr, "99") + " " + to_string(l_lager.bezeich, "x(13)")

                    if zwkum == 0:
                        zwkum = l_artikel.zwkum
                        bezeich = l_untergrup.bezeich

                    if zwkum != l_artikel.zwkum:
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        str_list.flag = 1
                        str_list.s = " "
                        str_list.s = str_list.s + to_string(bezeich, "x(50)")
                        for j in range(1,84 + 1) :
                            str_list.s = str_list.s + " "

                        if not long_digit:
                            str_list.s = str_list.s + to_string(t_val, "->>>,>>>,>>9.99")
                        else:
                            str_list.s = str_list.s + to_string(t_val, "->>,>>>,>>>,>>9")
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        t_anz =  to_decimal("0")
                        t_val =  to_decimal("0")
                        zwkum = l_untergrup.zwkum
                        bezeich = l_untergrup.bezeich
                    qty =  to_decimal(l_oh.anz_anf_best) + to_decimal(l_oh.anz_eingang) - to_decimal(l_oh.anz_ausgang)

                    if show_price:
                        wert =  to_decimal(l_oh.val_anf_best) + to_decimal(l_oh.wert_eingang) - to_decimal(l_oh.wert_ausgang)
                    tot_anz =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)

                    if l_artikel.anzverbrauch != 0:
                        must_order =  to_decimal(l_artikel.anzverbrauch) - to_decimal(tot_anz)

                    if qty != 0:
                        tot_val =  to_decimal(wert) * to_decimal(tot_anz) / to_decimal(qty)
                    else:
                        tot_val =  to_decimal("0")
                    t_anz =  to_decimal(t_anz) + to_decimal(tot_anz)

                    if show_price:
                        t_val =  to_decimal(t_val) + to_decimal(tot_val)
                        t_value =  to_decimal(t_value) + to_decimal(tot_val)
                        tt_val =  to_decimal(tt_val) + to_decimal(tot_val)
                        tt_value =  to_decimal(tt_value) + to_decimal(tot_val)

                    if tot_anz != 0 or (tot_anz == 0 and zero_flag):
                        str_list = Str_list()
                        str_list_list.append(str_list)


                        if show_price:

                            if not long_digit:
                                str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensorte, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(l_artikel.ek_letzter, ">>>,>>>,>>9.99") + to_string(l_artikel.ek_aktuell, ">>>,>>>,>>9.99") + to_string(l_artikel.vk_preis, "->>,>>>,>>9.99") + to_string(tot_anz, " ->>>,>>9.99") + to_string(tot_val, "->>>,>>>,>>9.99") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                            else:
                                str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensorte, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(l_artikel.ek_letzter, ">,>>>,>>>,>>9") + to_string(l_artikel.ek_aktuell, ">,>>>,>>>,>>9") + to_string(l_artikel.vk_preis, "->,>>>,>>>,>>9") + to_string(tot_anz, " ->>>,>>9.99") + to_string(tot_val, "->>,>>>,>>>,>>9") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                        else:

                            if not long_digit:
                                str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensorte, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(tot_anz, " ->>>,>>9.99") + to_string(0, "->>>,>>>,>>9.99") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                            else:
                                str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensorte, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(0, ">,>>>,>>>,>>9") + to_string(0, ">,>>>,>>>,>>9") + to_string(0, ">,>>>,>>>,>>9") + to_string(tot_anz, " ->>>,>>9.99") + to_string(0, "->>,>>>,>>>,>>9") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")


            if t_val != 0:
                str_list = Str_list()
                str_list_list.append(str_list)

                str_list.flag = 1
                str_list.s = " "
                str_list.s = str_list.s + to_string(bezeich, "x(50)")
                for j in range(1,84 + 1) :
                    str_list.s = str_list.s + " "

                if not long_digit:
                    str_list.s = str_list.s + to_string(t_val, "->>>,>>>,>>9.99")
                else:
                    str_list.s = str_list.s + to_string(t_val, "->>,>>>,>>>,>>9")
                str_list = Str_list()
                str_list_list.append(str_list)


            if tt_val != 0:
                str_list = Str_list()
                str_list_list.append(str_list)

                str_list.flag = 1
                str_list.s = " "
                str_list.s = str_list.s + to_string(tot_bezeich, "x(50)")
                for j in range(1,84 + 1) :
                    str_list.s = str_list.s + " "

                if not long_digit:
                    str_list.s = str_list.s + to_string(tt_val, "->>>,>>>,>>9.99")
                else:
                    str_list.s = str_list.s + to_string(tt_val, "->>,>>>,>>>,>>9")
                str_list = Str_list()
                str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.flag = 1
        str_list.s = " "
        str_list.s = str_list.s + to_string("GRAND T O T A L", "x(50)")
        for j in range(1,84 + 1) :
            str_list.s = str_list.s + " "

        if not long_digit:
            str_list.s = str_list.s + to_string(tt_value, "->>>,>>>,>>9.99")
        else:
            str_list.s = str_list.s + to_string(tt_value, "->>,>>>,>>>,>>9")


    def create_list1a():

        nonlocal str_list_list, long_digit, htparam, l_bestand, l_lager, l_artikel, l_untergrup
        nonlocal all_flag, show_price, zero_flag, from_grp, sub_grp, from_lager, to_lager, sorttype, mattype


        nonlocal str_list
        nonlocal str_list_list

        i:int = 0
        j:int = 0
        tot_anz:Decimal = to_decimal("0.0")
        tot_val:Decimal = to_decimal("0.0")
        t_anz:Decimal = to_decimal("0.0")
        t_val:Decimal = to_decimal("0.0")
        t_value:Decimal = to_decimal("0.0")
        tt_value:Decimal = to_decimal("0.0")
        avrg_price:Decimal = to_decimal("0.0")
        zwkum:int = 0
        bezeich:string = ""
        grp1:int = 0
        grp2:int = 1
        must_order:Decimal = to_decimal("0.0")
        tt_val:Decimal = to_decimal("0.0")
        qty:Decimal = to_decimal("0.0")
        wert:Decimal = to_decimal("0.0")
        l_oh = None
        tot_bezeich:string = ""
        L_oh =  create_buffer("L_oh",L_bestand)
        str_list_list.clear()

        if mattype == 1:
            grp2 = 0

        elif mattype == 2:
            grp1 = 1
        i = 0
        zwkum = 0
        t_anz =  to_decimal("0")
        t_val =  to_decimal("0")
        tt_val =  to_decimal("0")

        if sorttype == 1:

            if sub_grp != 000:

                l_bestand_obj_list = {}
                l_bestand = L_bestand()
                l_artikel = L_artikel()
                l_untergrup = L_untergrup()
                for l_bestand.anz_anf_best, l_bestand.anz_eingang, l_bestand.anz_ausgang, l_bestand.val_anf_best, l_bestand.wert_eingang, l_bestand.wert_ausgang, l_bestand._recid, l_artikel.zwkum, l_artikel.anzverbrauch, l_artikel.artnr, l_artikel.bezeich, l_artikel.masseinheit, l_artikel.inhalt, l_artikel.traubensorte, l_artikel.lief_einheit, l_artikel.ek_letzter, l_artikel.ek_aktuell, l_artikel.vk_preis, l_artikel.min_bestand, l_artikel._recid, l_untergrup.bezeich, l_untergrup.zwkum, l_untergrup._recid in db_session.query(L_bestand.anz_anf_best, L_bestand.anz_eingang, L_bestand.anz_ausgang, L_bestand.val_anf_best, L_bestand.wert_eingang, L_bestand.wert_ausgang, L_bestand._recid, L_artikel.zwkum, L_artikel.anzverbrauch, L_artikel.artnr, L_artikel.bezeich, L_artikel.masseinheit, L_artikel.inhalt, L_artikel.traubensorte, L_artikel.lief_einheit, L_artikel.ek_letzter, L_artikel.ek_aktuell, L_artikel.vk_preis, L_artikel.min_bestand, L_artikel._recid, L_untergrup.bezeich, L_untergrup.zwkum, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_bestand.artnr) & (L_artikel.zwkum == sub_grp)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum) & ((L_untergrup.betriebsnr >= grp1) & (L_untergrup.betriebsnr <= grp2))).filter(
                             (L_bestand.lager_nr == 0)).order_by(L_artikel.zwkum, L_artikel.artnr).all():
                    if l_bestand_obj_list.get(l_bestand._recid):
                        continue
                    else:
                        l_bestand_obj_list[l_bestand._recid] = True


                    i = i + 1
                    must_order =  to_decimal("0")

                    if zwkum == 0:
                        zwkum = l_artikel.zwkum
                        bezeich = l_untergrup.bezeich

                    if zwkum != l_artikel.zwkum:
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        str_list.flag = 1
                        str_list.s = " "
                        str_list.s = str_list.s + to_string(bezeich, "x(50)")
                        for j in range(1,84 + 1) :
                            str_list.s = str_list.s + " "

                        if not long_digit:
                            str_list.s = str_list.s + to_string(t_val, "->>>,>>>,>>9.99")
                        else:
                            str_list.s = str_list.s + to_string(t_val, "->>,>>>,>>>,>>9")
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        t_anz =  to_decimal("0")
                        t_val =  to_decimal("0")
                        zwkum = l_untergrup.zwkum
                        bezeich = l_untergrup.bezeich

                    if show_price:
                        tot_val =  to_decimal(l_bestand.val_anf_best) + to_decimal(l_bestand.wert_eingang) - to_decimal(l_bestand.wert_ausgang)
                    tot_anz =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)

                    if l_artikel.anzverbrauch != 0:
                        must_order =  to_decimal(l_artikel.anzverbrauch) - to_decimal(tot_anz)
                    t_anz =  to_decimal(t_anz) + to_decimal(tot_anz)

                    if show_price:
                        t_val =  to_decimal(t_val) + to_decimal(tot_val)
                        t_value =  to_decimal(t_value) + to_decimal(tot_val)
                        tt_val =  to_decimal(tt_val) + to_decimal(tot_val)
                        tt_value =  to_decimal(tt_value) + to_decimal(tot_val)

                    if tot_anz != 0 or (tot_anz == 0 and zero_flag):
                        str_list = Str_list()
                        str_list_list.append(str_list)


                        if show_price:

                            if not long_digit:
                                str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensorte, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(l_artikel.ek_letzter, ">>>,>>>,>>9.99") + to_string(l_artikel.ek_aktuell, ">>>,>>>,>>9.99") + to_string(l_artikel.vk_preis, "->>,>>>,>>9.99") + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_val, "->>>,>>>,>>9.99") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                            else:
                                str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensorte, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(l_artikel.ek_letzter, ">,>>>,>>>,>>9") + to_string(l_artikel.ek_aktuell, ">,>>>,>>>,>>9") + to_string(l_artikel.vk_preis, "->,>>>,>>>,>>9") + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_val, "->>,>>>,>>>,>>9") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                        else:

                            if not long_digit:
                                str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensorte, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(tot_anz, "->,>>>,>>9.99") + to_string(0, "->>>,>>>,>>9.99") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                            else:
                                str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensorte, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(0, ">,>>>,>>>,>>9") + to_string(0, ">,>>>,>>>,>>9") + to_string(0, ">,>>>,>>>,>>9") + to_string(tot_anz, "->,>>>,>>9.99") + to_string(0, "->>,>>>,>>>,>>9") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")

        else:

            l_bestand_obj_list = {}
            l_bestand = L_bestand()
            l_artikel = L_artikel()
            l_untergrup = L_untergrup()
            for l_bestand.anz_anf_best, l_bestand.anz_eingang, l_bestand.anz_ausgang, l_bestand.val_anf_best, l_bestand.wert_eingang, l_bestand.wert_ausgang, l_bestand._recid, l_artikel.zwkum, l_artikel.anzverbrauch, l_artikel.artnr, l_artikel.bezeich, l_artikel.masseinheit, l_artikel.inhalt, l_artikel.traubensorte, l_artikel.lief_einheit, l_artikel.ek_letzter, l_artikel.ek_aktuell, l_artikel.vk_preis, l_artikel.min_bestand, l_artikel._recid, l_untergrup.bezeich, l_untergrup.zwkum, l_untergrup._recid in db_session.query(L_bestand.anz_anf_best, L_bestand.anz_eingang, L_bestand.anz_ausgang, L_bestand.val_anf_best, L_bestand.wert_eingang, L_bestand.wert_ausgang, L_bestand._recid, L_artikel.zwkum, L_artikel.anzverbrauch, L_artikel.artnr, L_artikel.bezeich, L_artikel.masseinheit, L_artikel.inhalt, L_artikel.traubensorte, L_artikel.lief_einheit, L_artikel.ek_letzter, L_artikel.ek_aktuell, L_artikel.vk_preis, L_artikel.min_bestand, L_artikel._recid, L_untergrup.bezeich, L_untergrup.zwkum, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_bestand.artnr) & (L_artikel.endkum == from_grp)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum) & ((L_untergrup.betriebsnr >= grp1) & (L_untergrup.betriebsnr <= grp2))).filter(
                         (L_bestand.lager_nr == 0)).order_by(L_artikel.zwkum, L_artikel.artnr).all():
                if l_bestand_obj_list.get(l_bestand._recid):
                    continue
                else:
                    l_bestand_obj_list[l_bestand._recid] = True


                i = i + 1
                must_order =  to_decimal("0")

                if zwkum == 0:
                    zwkum = l_artikel.zwkum
                    bezeich = l_untergrup.bezeich

                if zwkum != l_artikel.zwkum:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.flag = 1
                    str_list.s = " "
                    str_list.s = str_list.s + to_string(bezeich, "x(50)")
                    for j in range(1,84 + 1) :
                        str_list.s = str_list.s + " "

                    if not long_digit:
                        str_list.s = str_list.s + to_string(t_val, "->>>,>>>,>>9.99")
                    else:
                        str_list.s = str_list.s + to_string(t_val, "->>,>>>,>>>,>>9")
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    t_anz =  to_decimal("0")
                    t_val =  to_decimal("0")
                    zwkum = l_untergrup.zwkum
                    bezeich = l_untergrup.bezeich

                if show_price:
                    tot_val =  to_decimal(l_bestand.val_anf_best) + to_decimal(l_bestand.wert_eingang) - to_decimal(l_bestand.wert_ausgang)
                tot_anz =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)

                if l_artikel.anzverbrauch != 0:
                    must_order =  to_decimal(l_artikel.anzverbrauch) - to_decimal(tot_anz)
                t_anz =  to_decimal(t_anz) + to_decimal(tot_anz)

                if show_price:
                    t_val =  to_decimal(t_val) + to_decimal(tot_val)
                    t_value =  to_decimal(t_value) + to_decimal(tot_val)
                    tt_val =  to_decimal(tt_val) + to_decimal(tot_val)
                    tt_value =  to_decimal(tt_value) + to_decimal(tot_val)

                if tot_anz != 0 or (tot_anz == 0 and zero_flag):
                    str_list = Str_list()
                    str_list_list.append(str_list)


                    if show_price:

                        if not long_digit:
                            str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensorte, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(l_artikel.ek_letzter, ">>>,>>>,>>9.99") + to_string(l_artikel.ek_aktuell, ">>>,>>>,>>9.99") + to_string(l_artikel.vk_preis, "->>,>>>,>>9.99") + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_val, "->>>,>>>,>>9.99") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                        else:
                            str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensorte, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(l_artikel.ek_letzter, ">,>>>,>>>,>>9") + to_string(l_artikel.ek_aktuell, ">,>>>,>>>,>>9") + to_string(l_artikel.vk_preis, "->,>>>,>>>,>>9") + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_val, "->>,>>>,>>>,>>9") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                    else:

                        if not long_digit:
                            str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensorte, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(tot_anz, "->,>>>,>>9.99") + to_string(0, "->>>,>>>,>>9.99") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                        else:
                            str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensorte, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(0, ">,>>>,>>>,>>9") + to_string(0, ">,>>>,>>>,>>9") + to_string(0, ">,>>>,>>>,>>9") + to_string(tot_anz, "->,>>>,>>9.99") + to_string(0, "->>,>>>,>>>,>>9") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")


        elif sorttype == 2:

            if sub_grp != 000:

                l_bestand_obj_list = {}
                l_bestand = L_bestand()
                l_artikel = L_artikel()
                l_untergrup = L_untergrup()
                for l_bestand.anz_anf_best, l_bestand.anz_eingang, l_bestand.anz_ausgang, l_bestand.val_anf_best, l_bestand.wert_eingang, l_bestand.wert_ausgang, l_bestand._recid, l_artikel.zwkum, l_artikel.anzverbrauch, l_artikel.artnr, l_artikel.bezeich, l_artikel.masseinheit, l_artikel.inhalt, l_artikel.traubensorte, l_artikel.lief_einheit, l_artikel.ek_letzter, l_artikel.ek_aktuell, l_artikel.vk_preis, l_artikel.min_bestand, l_artikel._recid, l_untergrup.bezeich, l_untergrup.zwkum, l_untergrup._recid in db_session.query(L_bestand.anz_anf_best, L_bestand.anz_eingang, L_bestand.anz_ausgang, L_bestand.val_anf_best, L_bestand.wert_eingang, L_bestand.wert_ausgang, L_bestand._recid, L_artikel.zwkum, L_artikel.anzverbrauch, L_artikel.artnr, L_artikel.bezeich, L_artikel.masseinheit, L_artikel.inhalt, L_artikel.traubensorte, L_artikel.lief_einheit, L_artikel.ek_letzter, L_artikel.ek_aktuell, L_artikel.vk_preis, L_artikel.min_bestand, L_artikel._recid, L_untergrup.bezeich, L_untergrup.zwkum, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_bestand.artnr) & (L_artikel.zwkum == sub_grp)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum) & ((L_untergrup.betriebsnr >= grp1) & (L_untergrup.betriebsnr <= grp2))).filter(
                             (L_bestand.lager_nr == 0)).order_by(L_artikel.zwkum, L_artikel.bezeich).all():
                    if l_bestand_obj_list.get(l_bestand._recid):
                        continue
                    else:
                        l_bestand_obj_list[l_bestand._recid] = True


                    i = i + 1
                    must_order =  to_decimal("0")

                    if zwkum == 0:
                        zwkum = l_artikel.zwkum
                        bezeich = l_untergrup.bezeich

                    if zwkum != l_artikel.zwkum:
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        str_list.flag = 1
                        str_list.s = " "
                        str_list.s = str_list.s + to_string(bezeich, "x(50)")
                        for j in range(1,84 + 1) :
                            str_list.s = str_list.s + " "

                        if not long_digit:
                            str_list.s = str_list.s + to_string(t_val, "->>>,>>>,>>9.99")
                        else:
                            str_list.s = str_list.s + to_string(t_val, "->>,>>>,>>>,>>9")
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        t_anz =  to_decimal("0")
                        t_val =  to_decimal("0")
                        zwkum = l_untergrup.zwkum
                        bezeich = l_untergrup.bezeich
                    tot_anz =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)

                    if show_price:
                        tot_val =  to_decimal(l_bestand.val_anf_best) + to_decimal(l_bestand.wert_eingang) - to_decimal(l_bestand.wert_ausgang)

                    if l_artikel.anzverbrauch != 0:
                        must_order =  to_decimal(l_artikel.anzverbrauch) - to_decimal(tot_anz)
                    t_anz =  to_decimal(t_anz) + to_decimal(tot_anz)

                    if show_price:
                        t_val =  to_decimal(t_val) + to_decimal(tot_val)
                        t_value =  to_decimal(t_value) + to_decimal(tot_val)
                        tt_val =  to_decimal(tt_val) + to_decimal(tot_val)
                        tt_value =  to_decimal(tt_value) + to_decimal(tot_val)

                    if tot_anz != 0 or (tot_anz == 0 and zero_flag):
                        str_list = Str_list()
                        str_list_list.append(str_list)


                        if show_price:

                            if not long_digit:
                                str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensorte, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(l_artikel.ek_letzter, ">>>,>>>,>>9.99") + to_string(l_artikel.ek_aktuell, ">>>,>>>,>>9.99") + to_string(l_artikel.vk_preis, "->>,>>>,>>9.99") + to_string(tot_anz, " ->>>,>>9.99") + to_string(tot_val, "->>>,>>>,>>9.99") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                            else:
                                str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensorte, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(l_artikel.ek_letzter, ">,>>>,>>>,>>9") + to_string(l_artikel.ek_aktuell, ">,>>>,>>>,>>9") + to_string(l_artikel.vk_preis, "->,>>>,>>>,>>9") + to_string(tot_anz, " ->>>,>>9.99") + to_string(tot_val, "->>,>>>,>>>,>>9") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                        else:

                            if not long_digit:
                                str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensorte, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(tot_anz, " ->>>,>>9.99") + to_string(0, "->>>,>>>,>>9.99") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                            else:
                                str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensorte, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(0, ">,>>>,>>>,>>9") + to_string(0, ">,>>>,>>>,>>9") + to_string(0, ">,>>>,>>>,>>9") + to_string(tot_anz, " ->>>,>>9.99") + to_string(0, "->>,>>>,>>>,>>9") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")

        else:

            l_bestand_obj_list = {}
            l_bestand = L_bestand()
            l_artikel = L_artikel()
            l_untergrup = L_untergrup()
            for l_bestand.anz_anf_best, l_bestand.anz_eingang, l_bestand.anz_ausgang, l_bestand.val_anf_best, l_bestand.wert_eingang, l_bestand.wert_ausgang, l_bestand._recid, l_artikel.zwkum, l_artikel.anzverbrauch, l_artikel.artnr, l_artikel.bezeich, l_artikel.masseinheit, l_artikel.inhalt, l_artikel.traubensorte, l_artikel.lief_einheit, l_artikel.ek_letzter, l_artikel.ek_aktuell, l_artikel.vk_preis, l_artikel.min_bestand, l_artikel._recid, l_untergrup.bezeich, l_untergrup.zwkum, l_untergrup._recid in db_session.query(L_bestand.anz_anf_best, L_bestand.anz_eingang, L_bestand.anz_ausgang, L_bestand.val_anf_best, L_bestand.wert_eingang, L_bestand.wert_ausgang, L_bestand._recid, L_artikel.zwkum, L_artikel.anzverbrauch, L_artikel.artnr, L_artikel.bezeich, L_artikel.masseinheit, L_artikel.inhalt, L_artikel.traubensorte, L_artikel.lief_einheit, L_artikel.ek_letzter, L_artikel.ek_aktuell, L_artikel.vk_preis, L_artikel.min_bestand, L_artikel._recid, L_untergrup.bezeich, L_untergrup.zwkum, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_bestand.artnr) & (L_artikel.endkum == from_grp)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum) & ((L_untergrup.betriebsnr >= grp1) & (L_untergrup.betriebsnr <= grp2))).filter(
                         (L_bestand.lager_nr == 0)).order_by(L_artikel.zwkum, L_artikel.bezeich).all():
                if l_bestand_obj_list.get(l_bestand._recid):
                    continue
                else:
                    l_bestand_obj_list[l_bestand._recid] = True


                i = i + 1
                must_order =  to_decimal("0")

                if zwkum == 0:
                    zwkum = l_artikel.zwkum
                    bezeich = l_untergrup.bezeich

                if zwkum != l_artikel.zwkum:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.flag = 1
                    str_list.s = " "
                    str_list.s = str_list.s + to_string(bezeich, "x(50)")
                    for j in range(1,84 + 1) :
                        str_list.s = str_list.s + " "

                    if not long_digit:
                        str_list.s = str_list.s + to_string(t_val, "->>>,>>>,>>9.99")
                    else:
                        str_list.s = str_list.s + to_string(t_val, "->>,>>>,>>>,>>9")
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    t_anz =  to_decimal("0")
                    t_val =  to_decimal("0")
                    zwkum = l_untergrup.zwkum
                    bezeich = l_untergrup.bezeich
                tot_anz =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)

                if show_price:
                    tot_val =  to_decimal(l_bestand.val_anf_best) + to_decimal(l_bestand.wert_eingang) - to_decimal(l_bestand.wert_ausgang)

                if l_artikel.anzverbrauch != 0:
                    must_order =  to_decimal(l_artikel.anzverbrauch) - to_decimal(tot_anz)
                t_anz =  to_decimal(t_anz) + to_decimal(tot_anz)

                if show_price:
                    t_val =  to_decimal(t_val) + to_decimal(tot_val)
                    t_value =  to_decimal(t_value) + to_decimal(tot_val)
                    tt_val =  to_decimal(tt_val) + to_decimal(tot_val)
                    tt_value =  to_decimal(tt_value) + to_decimal(tot_val)

                if tot_anz != 0 or (tot_anz == 0 and zero_flag):
                    str_list = Str_list()
                    str_list_list.append(str_list)


                    if show_price:

                        if not long_digit:
                            str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensorte, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(l_artikel.ek_letzter, ">>>,>>>,>>9.99") + to_string(l_artikel.ek_aktuell, ">>>,>>>,>>9.99") + to_string(l_artikel.vk_preis, "->>,>>>,>>9.99") + to_string(tot_anz, " ->>>,>>9.99") + to_string(tot_val, "->>>,>>>,>>9.99") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                        else:
                            str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensorte, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(l_artikel.ek_letzter, ">,>>>,>>>,>>9") + to_string(l_artikel.ek_aktuell, ">,>>>,>>>,>>9") + to_string(l_artikel.vk_preis, "->,>>>,>>>,>>9") + to_string(tot_anz, " ->>>,>>9.99") + to_string(tot_val, "->>,>>>,>>>,>>9") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                    else:

                        if not long_digit:
                            str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensorte, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(tot_anz, " ->>>,>>9.99") + to_string(0, "->>>,>>>,>>9.99") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                        else:
                            str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensorte, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(0, ">,>>>,>>>,>>9") + to_string(0, ">,>>>,>>>,>>9") + to_string(0, ">,>>>,>>>,>>9") + to_string(tot_anz, " ->>>,>>9.99") + to_string(0, "->>,>>>,>>>,>>9") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")


        if t_val != 0:
            str_list = Str_list()
            str_list_list.append(str_list)

            str_list.flag = 1
            str_list.s = " "
            str_list.s = str_list.s + to_string(bezeich, "x(50)")
            for j in range(1,84 + 1) :
                str_list.s = str_list.s + " "

            if not long_digit:
                str_list.s = str_list.s + to_string(t_val, "->>>,>>>,>>9.99")
            else:
                str_list.s = str_list.s + to_string(t_val, "->>,>>>,>>>,>>9")
            str_list = Str_list()
            str_list_list.append(str_list)


        if tt_val != 0:
            pass
        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.flag = 1
        str_list.s = " "
        str_list.s = str_list.s + to_string("GRAND T O T A L", "x(50)")
        for j in range(1,84 + 1) :
            str_list.s = str_list.s + " "

        if not long_digit:
            str_list.s = str_list.s + to_string(tt_value, "->>>,>>>,>>9.99")
        else:
            str_list.s = str_list.s + to_string(tt_value, "->>,>>>,>>>,>>9")


    htparam = get_cache (Htparam, {"paramnr": [(eq, 246)]})
    long_digit = htparam.flogical

    if not all_flag:

        if from_grp == 0:
            create_list()
        else:
            create_list1()
    else:

        if from_grp == 0:
            create_lista()
        else:
            create_list1a()

    return generate_output()