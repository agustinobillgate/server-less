from functions.additional_functions import *
import decimal
from models import Htparam, L_bestand, L_lager, L_artikel, L_untergrup

def sall_onhand_btn_gobl(all_flag:bool, show_price:bool, zero_flag:bool, from_grp:int, sub_grp:int, from_lager:int, to_lager:int, sorttype:int, mattype:int):
    str_list_list = []
    long_digit:bool = False
    htparam = l_bestand = l_lager = l_artikel = l_untergrup = None

    str_list = l_oh = None

    str_list_list, Str_list = create_model("Str_list", {"flag":int, "s":str})

    L_oh = L_bestand

    db_session = local_storage.db_session

    def generate_output():
        nonlocal str_list_list, long_digit, htparam, l_bestand, l_lager, l_artikel, l_untergrup
        nonlocal l_oh


        nonlocal str_list, l_oh
        nonlocal str_list_list
        return {"str-list": str_list_list}

    def create_list():

        nonlocal str_list_list, long_digit, htparam, l_bestand, l_lager, l_artikel, l_untergrup
        nonlocal l_oh


        nonlocal str_list, l_oh
        nonlocal str_list_list

        i:int = 0
        j:int = 0
        tot_anz:decimal = 0
        tot_val:decimal = 0
        t_anz:decimal = 0
        t_val:decimal = 0
        t_value:decimal = 0
        avrg_price:decimal = 0
        zwkum:int = 0
        bezeich:str = ""
        must_order:decimal = 0
        qty:decimal = 0
        wert:decimal = 0
        tot_bezeich:str = ""
        tt_val:decimal = 0
        tt_value:decimal = 0
        L_oh = L_bestand
        str_list_list.clear()

        for l_lager in db_session.query(L_lager).filter(
                (L_lager.lager_nr >= from_lager) &  (L_lager.lager_nr <= to_lager)).all():
            tot_bezeich = "Ttl - " + l_lager.bezeich
            i = 0
            zwkum = 0
            t_anz = 0
            t_val = 0
            tt_val = 0

            if sorttype == 1:

                if sub_grp != 000:

                    l_bestand_obj_list = []
                    for l_bestand, l_artikel, l_oh, l_untergrup in db_session.query(L_bestand, L_artikel, L_oh, L_untergrup).join(L_artikel,(L_artikel.artnr == L_bestand.artnr) &  (L_artikel.zwkum == sub_grp)).join(L_oh,(L_oh.artnr == L_bestand.artnr) &  (L_oh.lager_nr == 0)).join(L_untergrup,(L_untergrup.zwkum == l_artikel.zwkum)).filter(
                            (L_bestand.lager_nr == l_lager.lager_nr)).all():
                        if l_bestand._recid in l_bestand_obj_list:
                            continue
                        else:
                            l_bestand_obj_list.append(l_bestand._recid)


                        i = i + 1
                        must_order = 0

                        if i == 1:
                            str_list = Str_list()
                            str_list_list.append(str_list)

                            str_list.s = "        " + to_string(l_lager.lager_nr, "99") + " " + to_string(l_lager.bezeich, "x(50)")

                        if zwkum == 0:
                            zwkum = l_artikel.zwkum
                            bezeich = l_untergrup.bezeich

                        if zwkum != l_artikel.zwkum:
                            str_list = Str_list()
                            str_list_list.append(str_list)

                            str_list.flag = 1
                            str_list.s = "       "
                            str_list.s = str_list.s + to_string(bezeich, "x(50)")
                            for j in range(1,84 + 1) :
                                str_list.s = str_list.s + " "

                            if not long_digit:
                                str_list.s = str_list.s + to_string(t_val, "->>>,>>>,>>9.99")
                            else:
                                str_list.s = str_list.s + to_string(t_val, "->>,>>>,>>>,>>9")
                            str_list = Str_list()
                            str_list_list.append(str_list)

                            t_anz = 0
                            t_val = 0
                            zwkum = l_untergrup.zwkum
                            bezeich = l_untergrup.bezeich
                        qty = l_oh.anz_anf_best + l_oh.anz_eingang - l_oh.anz_ausgang

                        if show_price:
                            wert = l_oh.val_anf_best + l_oh.wert_eingang - l_oh.wert_ausgang
                        tot_anz = l_bestand.anz_anf_best + l_bestand.anz_eingang - l_bestand.anz_ausgang

                        if l_artikel.anzverbrauch != 0:
                            must_order = l_artikel.anzverbrauch - tot_anz

                        if qty != 0:
                            tot_val = wert * tot_anz / qty
                        else:
                            tot_val = 0
                        t_anz = t_anz + tot_anz

                        if show_price:
                            t_val = t_val + tot_val
                            t_value = t_value + tot_val
                            tt_val = tt_val + tot_val
                            tt_value = tt_value + tot_val

                        if tot_anz != 0 or (tot_anz == 0 and zero_flag):
                            str_list = Str_list()
                            str_list_list.append(str_list)


                            if show_price:

                                if not long_digit:
                                    str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensort, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(l_artikel.ek_letzter, ">>>,>>>,>>9.99") + to_string(l_artikel.ek_aktuell, ">>>,>>>,>>9.99") + to_string(l_artikel.vk_preis, "->>,>>>,>>9.99") + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_val, "->>>,>>>,>>9.99") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                                else:
                                    str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensort, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(l_artikel.ek_letzter, ">,>>>,>>>,>>9") + to_string(l_artikel.ek_aktuell, ">,>>>,>>>,>>9") + to_string(l_artikel.vk_preis, "->,>>>,>>>,>>9") + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_val, "->>,>>>,>>>,>>9") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                            else:

                                if not long_digit:
                                    str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensort, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(tot_anz, "->,>>>,>>9.99") + to_string(0, "->>>,>>>,>>9.99") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                                else:
                                    str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensort, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(0, ">,>>>,>>>,>>9") + to_string(0, ">,>>>,>>>,>>9") + to_string(0, ">,>>>,>>>,>>9") + to_string(tot_anz, "->,>>>,>>9.99") + to_string(0, "->>,>>>,>>>,>>9") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")

            else:

                l_bestand_obj_list = []
                for l_bestand, l_artikel, l_oh, l_untergrup in db_session.query(L_bestand, L_artikel, L_oh, L_untergrup).join(L_artikel,(L_artikel.artnr == L_bestand.artnr)).join(L_oh,(L_oh.artnr == L_bestand.artnr) &  (L_oh.lager_nr == 0)).join(L_untergrup,(L_untergrup.zwkum == l_artikel.zwkum)).filter(
                        (L_bestand.lager_nr == l_lager.lager_nr)).all():
                    if l_bestand._recid in l_bestand_obj_list:
                        continue
                    else:
                        l_bestand_obj_list.append(l_bestand._recid)


                    i = i + 1
                    must_order = 0

                    if i == 1:
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        str_list.s = "        " + to_string(l_lager.lager_nr, "99") + " " + to_string(l_lager.bezeich, "x(50)")

                    if zwkum == 0:
                        zwkum = l_artikel.zwkum
                        bezeich = l_untergrup.bezeich

                    if zwkum != l_artikel.zwkum:
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        str_list.flag = 1
                        str_list.s = "       "
                        str_list.s = str_list.s + to_string(bezeich, "x(50)")
                        for j in range(1,84 + 1) :
                            str_list.s = str_list.s + " "

                        if not long_digit:
                            str_list.s = str_list.s + to_string(t_val, "->>>,>>>,>>9.99")
                        else:
                            str_list.s = str_list.s + to_string(t_val, "->>,>>>,>>>,>>9")
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        t_anz = 0
                        t_val = 0
                        zwkum = l_untergrup.zwkum
                        bezeich = l_untergrup.bezeich
                    qty = l_oh.anz_anf_best + l_oh.anz_eingang - l_oh.anz_ausgang

                    if show_price:
                        wert = l_oh.val_anf_best + l_oh.wert_eingang - l_oh.wert_ausgang
                    tot_anz = l_bestand.anz_anf_best + l_bestand.anz_eingang - l_bestand.anz_ausgang

                    if l_artikel.anzverbrauch != 0:
                        must_order = l_artikel.anzverbrauch - tot_anz

                    if qty != 0:
                        tot_val = wert * tot_anz / qty
                    else:
                        tot_val = 0
                    t_anz = t_anz + tot_anz

                    if show_price:
                        t_val = t_val + tot_val
                        t_value = t_value + tot_val
                        tt_val = tt_val + tot_val
                        tt_value = tt_value + tot_val

                    if tot_anz != 0 or (tot_anz == 0 and zero_flag):
                        str_list = Str_list()
                        str_list_list.append(str_list)


                        if show_price:

                            if not long_digit:
                                str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensort, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(l_artikel.ek_letzter, ">>>,>>>,>>9.99") + to_string(l_artikel.ek_aktuell, ">>>,>>>,>>9.99") + to_string(l_artikel.vk_preis, "->>,>>>,>>9.99") + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_val, "->>>,>>>,>>9.99") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                            else:
                                str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensort, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(l_artikel.ek_letzter, ">,>>>,>>>,>>9") + to_string(l_artikel.ek_aktuell, ">,>>>,>>>,>>9") + to_string(l_artikel.vk_preis, "->,>>>,>>>,>>9") + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_val, "->>,>>>,>>>,>>9") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                        else:

                            if not long_digit:
                                str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensort, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(tot_anz, "->,>>>,>>9.99") + to_string(0, "->>>,>>>,>>9.99") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                            else:
                                str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensort, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(0, ">,>>>,>>>,>>9") + to_string(0, ">,>>>,>>>,>>9") + to_string(0, ">,>>>,>>>,>>9") + to_string(tot_anz, "->,>>>,>>9.99") + to_string(0, "->>,>>>,>>>,>>9") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")


            elif sorttype == 2:

                if sub_grp != 000:

                    l_bestand_obj_list = []
                    for l_bestand, l_artikel, l_oh, l_untergrup in db_session.query(L_bestand, L_artikel, L_oh, L_untergrup).join(L_artikel,(L_artikel.artnr == L_bestand.artnr) &  (L_artikel.zwkum == sub_grp)).join(L_oh,(L_oh.artnr == L_bestand.artnr) &  (L_oh.lager_nr == 0)).join(L_untergrup,(L_untergrup.zwkum == l_artikel.zwkum)).filter(
                            (L_bestand.lager_nr == l_lager.lager_nr)).all():
                        if l_bestand._recid in l_bestand_obj_list:
                            continue
                        else:
                            l_bestand_obj_list.append(l_bestand._recid)


                        i = i + 1
                        must_order = 0

                        if i == 1:
                            str_list = Str_list()
                            str_list_list.append(str_list)

                            str_list.s = "        " + to_string(l_lager.lager_nr, "99") + " " + to_string(l_lager.bezeich, "x(13)")

                        if zwkum == 0:
                            zwkum = l_artikel.zwkum
                            bezeich = l_untergrup.bezeich

                        if zwkum != l_artikel.zwkum:
                            str_list = Str_list()
                            str_list_list.append(str_list)

                            str_list.flag = 1
                            str_list.s = "       "
                            str_list.s = str_list.s + to_string(bezeich, "x(50)")
                            for j in range(1,84 + 1) :
                                str_list.s = str_list.s + " "

                            if not long_digit:
                                str_list.s = str_list.s + to_string(t_val, "->>>,>>>,>>9.99")
                            else:
                                str_list.s = str_list.s + to_string(t_val, "->>,>>>,>>>,>>9")
                            str_list = Str_list()
                            str_list_list.append(str_list)

                            t_anz = 0
                            t_val = 0
                            zwkum = l_untergrup.zwkum
                            bezeich = l_untergrup.bezeich
                        qty = l_oh.anz_anf_best + l_oh.anz_eingang - l_oh.anz_ausgang

                        if show_price:
                            wert = l_oh.val_anf_best + l_oh.wert_eingang - l_oh.wert_ausgang
                        tot_anz = l_bestand.anz_anf_best + l_bestand.anz_eingang - l_bestand.anz_ausgang

                        if l_artikel.anzverbrauch != 0:
                            must_order = l_artikel.anzverbrauch - tot_anz

                        if qty != 0:
                            tot_val = wert * tot_anz / qty
                        else:
                            tot_val = 0
                        t_anz = t_anz + tot_anz

                        if show_price:
                            t_val = t_val + tot_val
                            t_value = t_value + tot_val
                            tt_val = tt_val + tot_val
                            tt_value = tt_value + tot_val

                        if tot_anz != 0 or (tot_anz == 0 and zero_flag):
                            str_list = Str_list()
                            str_list_list.append(str_list)


                            if show_price:

                                if not long_digit:
                                    str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensort, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(l_artikel.ek_letzter, ">>>,>>>,>>9.99") + to_string(l_artikel.ek_aktuell, ">>>,>>>,>>9.99") + to_string(l_artikel.vk_preis, "->>,>>>,>>9.99") + to_string(tot_anz, " ->>>,>>9.99") + to_string(tot_val, "->>>,>>>,>>9.99") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                                else:
                                    str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensort, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(l_artikel.ek_letzter, ">,>>>,>>>,>>9") + to_string(l_artikel.ek_aktuell, ">,>>>,>>>,>>9") + to_string(l_artikel.vk_preis, "->,>>>,>>>,>>9") + to_string(tot_anz, " ->>>,>>9.99") + to_string(tot_val, "->>,>>>,>>>,>>9") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                            else:

                                if not long_digit:
                                    str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensort, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(tot_anz, " ->>>,>>9.99") + to_string(0, "->>>,>>>,>>9.99") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                                else:
                                    str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensort, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(0, ">,>>>,>>>,>>9") + to_string(0, ">,>>>,>>>,>>9") + to_string(0, ">,>>>,>>>,>>9") + to_string(tot_anz, " ->>>,>>9.99") + to_string(0, "->>,>>>,>>>,>>9") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")

            else:

                l_bestand_obj_list = []
                for l_bestand, l_artikel, l_oh, l_untergrup in db_session.query(L_bestand, L_artikel, L_oh, L_untergrup).join(L_artikel,(L_artikel.artnr == L_bestand.artnr)).join(L_oh,(L_oh.artnr == L_bestand.artnr) &  (L_oh.lager_nr == 0)).join(L_untergrup,(L_untergrup.zwkum == l_artikel.zwkum)).filter(
                        (L_bestand.lager_nr == l_lager.lager_nr)).all():
                    if l_bestand._recid in l_bestand_obj_list:
                        continue
                    else:
                        l_bestand_obj_list.append(l_bestand._recid)


                    i = i + 1
                    must_order = 0

                    if i == 1:
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        str_list.s = "        " + to_string(l_lager.lager_nr, "99") + " " + to_string(l_lager.bezeich, "x(13)")

                    if zwkum == 0:
                        zwkum = l_artikel.zwkum
                        bezeich = l_untergrup.bezeich

                    if zwkum != l_artikel.zwkum:
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        str_list.flag = 1
                        str_list.s = "       "
                        str_list.s = str_list.s + to_string(bezeich, "x(50)")
                        for j in range(1,84 + 1) :
                            str_list.s = str_list.s + " "

                        if not long_digit:
                            str_list.s = str_list.s + to_string(t_val, "->>>,>>>,>>9.99")
                        else:
                            str_list.s = str_list.s + to_string(t_val, "->>,>>>,>>>,>>9")
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        t_anz = 0
                        t_val = 0
                        zwkum = l_untergrup.zwkum
                        bezeich = l_untergrup.bezeich
                    qty = l_oh.anz_anf_best + l_oh.anz_eingang - l_oh.anz_ausgang

                    if show_price:
                        wert = l_oh.val_anf_best + l_oh.wert_eingang - l_oh.wert_ausgang
                    tot_anz = l_bestand.anz_anf_best + l_bestand.anz_eingang - l_bestand.anz_ausgang

                    if l_artikel.anzverbrauch != 0:
                        must_order = l_artikel.anzverbrauch - tot_anz

                    if qty != 0:
                        tot_val = wert * tot_anz / qty
                    else:
                        tot_val = 0
                    t_anz = t_anz + tot_anz

                    if show_price:
                        t_val = t_val + tot_val
                        t_value = t_value + tot_val
                        tt_val = tt_val + tot_val
                        tt_value = tt_value + tot_val

                    if tot_anz != 0 or (tot_anz == 0 and zero_flag):
                        str_list = Str_list()
                        str_list_list.append(str_list)


                        if show_price:

                            if not long_digit:
                                str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensort, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(l_artikel.ek_letzter, ">>>,>>>,>>9.99") + to_string(l_artikel.ek_aktuell, ">>>,>>>,>>9.99") + to_string(l_artikel.vk_preis, "->>,>>>,>>9.99") + to_string(tot_anz, " ->>>,>>9.99") + to_string(tot_val, "->>>,>>>,>>9.99") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                            else:
                                str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensort, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(l_artikel.ek_letzter, ">,>>>,>>>,>>9") + to_string(l_artikel.ek_aktuell, ">,>>>,>>>,>>9") + to_string(l_artikel.vk_preis, "->,>>>,>>>,>>9") + to_string(tot_anz, " ->>>,>>9.99") + to_string(tot_val, "->>,>>>,>>>,>>9") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                        else:

                            if not long_digit:
                                str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensort, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(tot_anz, " ->>>,>>9.99") + to_string(0, "->>>,>>>,>>9.99") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                            else:
                                str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensort, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(0, ">,>>>,>>>,>>9") + to_string(0, ">,>>>,>>>,>>9") + to_string(0, ">,>>>,>>>,>>9") + to_string(tot_anz, " ->>>,>>9.99") + to_string(0, "->>,>>>,>>>,>>9") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")


            if t_val != 0:
                str_list = Str_list()
                str_list_list.append(str_list)

                str_list.flag = 1
                str_list.s = "       "
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
            str_list.s = "       "
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
        str_list.s = "       "
        str_list.s = str_list.s + to_string("GRAND T O T A L", "x(50)")
        for j in range(1,84 + 1) :
            str_list.s = str_list.s + " "

        if not long_digit:
            str_list.s = str_list.s + to_string(tt_value, "->>>,>>>,>>9.99")
        else:
            str_list.s = str_list.s + to_string(tt_value, "->>,>>>,>>>,>>9")

    def create_lista():

        nonlocal str_list_list, long_digit, htparam, l_bestand, l_lager, l_artikel, l_untergrup
        nonlocal l_oh


        nonlocal str_list, l_oh
        nonlocal str_list_list

        i:int = 0
        j:int = 0
        tot_anz:decimal = 0
        tot_val:decimal = 0
        t_anz:decimal = 0
        t_val:decimal = 0
        t_value:decimal = 0
        avrg_price:decimal = 0
        zwkum:int = 0
        bezeich:str = ""
        must_order:decimal = 0
        qty:decimal = 0
        wert:decimal = 0
        tot_bezeich:str = ""
        tt_val:decimal = 0
        tt_value:decimal = 0
        L_oh = L_bestand
        str_list_list.clear()
        i = 0
        zwkum = 0
        t_anz = 0
        t_val = 0
        tt_val = 0

        if sorttype == 1:

            if sub_grp != 000:

                l_bestand_obj_list = []
                for l_bestand, l_artikel, l_untergrup in db_session.query(L_bestand, L_artikel, L_untergrup).join(L_artikel,(L_artikel.artnr == L_bestand.artnr) &  (L_artikel.zwkum == sub_grp)).join(L_untergrup,(L_untergrup.zwkum == l_artikel.zwkum)).filter(
                            (L_bestand.lager_nr == 0)).all():
                    if l_bestand._recid in l_bestand_obj_list:
                        continue
                    else:
                        l_bestand_obj_list.append(l_bestand._recid)


                    i = i + 1
                    must_order = 0

                    if zwkum == 0:
                        zwkum = l_artikel.zwkum
                        bezeich = l_untergrup.bezeich

                    if zwkum != l_artikel.zwkum:
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        str_list.flag = 1
                        str_list.s = "       "
                        str_list.s = str_list.s + to_string(bezeich, "x(50)")
                        for j in range(1,84 + 1) :
                            str_list.s = str_list.s + " "

                        if not long_digit:
                            str_list.s = str_list.s + to_string(t_val, "->>>,>>>,>>9.99")
                        else:
                            str_list.s = str_list.s + to_string(t_val, "->>,>>>,>>>,>>9")
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        t_anz = 0
                        t_val = 0
                        zwkum = l_untergrup.zwkum
                        bezeich = l_untergrup.bezeich

                    if show_price:
                        tot_val = l_bestand.val_anf_best + l_bestand.wert_eingang - l_bestand.wert_ausgang
                    tot_anz = l_bestand.anz_anf_best + l_bestand.anz_eingang - l_bestand.anz_ausgang

                    if l_artikel.anzverbrauch != 0:
                        must_order = l_artikel.anzverbrauch - tot_anz
                    t_anz = t_anz + tot_anz

                    if show_price:
                        t_val = t_val + tot_val
                        t_value = t_value + tot_val
                        tt_val = tt_val + tot_val
                        tt_value = tt_value + tot_val

                    if tot_anz != 0 or (tot_anz == 0 and zero_flag):
                        str_list = Str_list()
                        str_list_list.append(str_list)


                        if show_price:

                            if not long_digit:
                                str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensort, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(l_artikel.ek_letzter, ">>>,>>>,>>9.99") + to_string(l_artikel.ek_aktuell, ">>>,>>>,>>9.99") + to_string(l_artikel.vk_preis, "->>,>>>,>>9.99") + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_val, "->>>,>>>,>>9.99") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                            else:
                                str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensort, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(l_artikel.ek_letzter, ">,>>>,>>>,>>9") + to_string(l_artikel.ek_aktuell, ">,>>>,>>>,>>9") + to_string(l_artikel.vk_preis, "->,>>>,>>>,>>9") + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_val, "->>,>>>,>>>,>>9") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                        else:

                            if not long_digit:
                                str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensort, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(tot_anz, "->,>>>,>>9.99") + to_string(0, "->>>,>>>,>>9.99") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                            else:
                                str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensort, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(0, ">,>>>,>>>,>>9") + to_string(0, ">,>>>,>>>,>>9") + to_string(0, ">,>>>,>>>,>>9") + to_string(tot_anz, "->,>>>,>>9.99") + to_string(0, "->>,>>>,>>>,>>9") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")

        else:

            l_bestand_obj_list = []
            for l_bestand, l_artikel, l_untergrup in db_session.query(L_bestand, L_artikel, L_untergrup).join(L_artikel,(L_artikel.artnr == L_bestand.artnr)).join(L_untergrup,(L_untergrup.zwkum == l_artikel.zwkum)).filter(
                        (L_bestand.lager_nr == 0)).all():
                if l_bestand._recid in l_bestand_obj_list:
                    continue
                else:
                    l_bestand_obj_list.append(l_bestand._recid)


                i = i + 1
                must_order = 0

                if zwkum == 0:
                    zwkum = l_artikel.zwkum
                    bezeich = l_untergrup.bezeich

                if zwkum != l_artikel.zwkum:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.flag = 1
                    str_list.s = "       "
                    str_list.s = str_list.s + to_string(bezeich, "x(50)")
                    for j in range(1,84 + 1) :
                        str_list.s = str_list.s + " "

                    if not long_digit:
                        str_list.s = str_list.s + to_string(t_val, "->>>,>>>,>>9.99")
                    else:
                        str_list.s = str_list.s + to_string(t_val, "->>,>>>,>>>,>>9")
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    t_anz = 0
                    t_val = 0
                    must_order = 0
                    zwkum = l_untergrup.zwkum
                    bezeich = l_untergrup.bezeich

                if show_price:
                    tot_val = l_bestand.val_anf_best + l_bestand.wert_eingang - l_bestand.wert_ausgang
                tot_anz = l_bestand.anz_anf_best + l_bestand.anz_eingang - l_bestand.anz_ausgang

                if l_artikel.anzverbrauch != 0:
                    must_order = l_artikel.anzverbrauch - tot_anz
                t_anz = t_anz + tot_anz

                if show_price:
                    t_val = t_val + tot_val
                    t_value = t_value + tot_val
                    tt_val = tt_val + tot_val
                    tt_value = tt_value + tot_val

                if tot_anz != 0 or (tot_anz == 0 and zero_flag):
                    str_list = Str_list()
                    str_list_list.append(str_list)


                    if show_price:

                        if not long_digit:
                            str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensort, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(l_artikel.ek_letzter, ">>>,>>>,>>9.99") + to_string(l_artikel.ek_aktuell, ">>>,>>>,>>9.99") + to_string(l_artikel.vk_preis, "->>,>>>,>>9.99") + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_val, "->>>,>>>,>>9.99") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                        else:
                            str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensort, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(l_artikel.ek_letzter, ">,>>>,>>>,>>9") + to_string(l_artikel.ek_aktuell, ">,>>>,>>>,>>9") + to_string(l_artikel.vk_preis, "->,>>>,>>>,>>9") + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_val, "->>,>>>,>>>,>>9") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                    else:

                        if not long_digit:
                            str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensort, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(tot_anz, "->,>>>,>>9.99") + to_string(0, "->>>,>>>,>>9.99") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                        else:
                            str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensort, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(0, ">,>>>,>>>,>>9") + to_string(0, ">,>>>,>>>,>>9") + to_string(0, ">,>>>,>>>,>>9") + to_string(tot_anz, "->,>>>,>>9.99") + to_string(0, "->>,>>>,>>>,>>9") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")


        elif sorttype == 2:

            if sub_grp != 000:

                l_bestand_obj_list = []
                for l_bestand, l_artikel, l_untergrup in db_session.query(L_bestand, L_artikel, L_untergrup).join(L_artikel,(L_artikel.artnr == L_bestand.artnr) &  (L_artikel.zwkum == sub_grp)).join(L_untergrup,(L_untergrup.zwkum == l_artikel.zwkum)).filter(
                            (L_bestand.lager_nr == 0)).all():
                    if l_bestand._recid in l_bestand_obj_list:
                        continue
                    else:
                        l_bestand_obj_list.append(l_bestand._recid)


                    i = i + 1
                    must_order = 0

                    if zwkum == 0:
                        zwkum = l_artikel.zwkum
                        bezeich = l_untergrup.bezeich

                    if zwkum != l_artikel.zwkum:
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        str_list.flag = 1
                        str_list.s = "       "
                        str_list.s = str_list.s + to_string(bezeich, "x(50)")
                        for j in range(1,84 + 1) :
                            str_list.s = str_list.s + " "

                        if not long_digit:
                            str_list.s = str_list.s + to_string(t_val, "->>>,>>>,>>9.99")
                        else:
                            str_list.s = str_list.s + to_string(t_val, "->>,>>>,>>>,>>9")
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        t_anz = 0
                        t_val = 0
                        zwkum = l_untergrup.zwkum
                        bezeich = l_untergrup.bezeich

                    if show_price:
                        tot_val = l_bestand.val_anf_best + l_bestand.wert_eingang - l_bestand.wert_ausgang
                    tot_anz = l_bestand.anz_anf_best + l_bestand.anz_eingang - l_bestand.anz_ausgang

                    if l_artikel.anzverbrauch != 0:
                        must_order = l_artikel.anzverbrauch - tot_anz
                    t_anz = t_anz + tot_anz

                    if show_price:
                        t_val = t_val + tot_val
                        t_value = t_value + tot_val
                        tt_val = tt_val + tot_val
                        tt_value = tt_value + tot_val

                    if tot_anz != 0 or (tot_anz == 0 and zero_flag):
                        str_list = Str_list()
                        str_list_list.append(str_list)


                        if show_price:

                            if not long_digit:
                                str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensort, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(l_artikel.ek_letzter, ">>>,>>>,>>9.99") + to_string(l_artikel.ek_aktuell, ">>>,>>>,>>9.99") + to_string(l_artikel.vk_preis, "->>,>>>,>>9.99") + to_string(tot_anz, " ->>>,>>9.99") + to_string(tot_val, "->>>,>>>,>>9.99") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                            else:
                                str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensort, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(l_artikel.ek_letzter, ">,>>>,>>>,>>9") + to_string(l_artikel.ek_aktuell, ">,>>>,>>>,>>9") + to_string(l_artikel.vk_preis, "->,>>>,>>>,>>9") + to_string(tot_anz, " ->>>,>>9.99") + to_string(tot_val, "->>,>>>,>>>,>>9") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                        else:

                            if not long_digit:
                                str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensort, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(tot_anz, " ->>>,>>9.99") + to_string(0, "->>>,>>>,>>9.99") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                            else:
                                str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensort, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(0, ">,>>>,>>>,>>9") + to_string(0, ">,>>>,>>>,>>9") + to_string(0, ">,>>>,>>>,>>9") + to_string(tot_anz, " ->>>,>>9.99") + to_string(0, "->>,>>>,>>>,>>9") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")

        else:

            l_bestand_obj_list = []
            for l_bestand, l_artikel, l_untergrup in db_session.query(L_bestand, L_artikel, L_untergrup).join(L_artikel,(L_artikel.artnr == L_bestand.artnr)).join(L_untergrup,(L_untergrup.zwkum == l_artikel.zwkum)).filter(
                        (L_bestand.lager_nr == 0)).all():
                if l_bestand._recid in l_bestand_obj_list:
                    continue
                else:
                    l_bestand_obj_list.append(l_bestand._recid)


                i = i + 1
                must_order = 0

                if zwkum == 0:
                    zwkum = l_artikel.zwkum
                    bezeich = l_untergrup.bezeich

                if zwkum != l_artikel.zwkum:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.flag = 1
                    str_list.s = "       "
                    str_list.s = str_list.s + to_string(bezeich, "x(50)")
                    for j in range(1,84 + 1) :
                        str_list.s = str_list.s + " "

                    if not long_digit:
                        str_list.s = str_list.s + to_string(t_val, "->>>,>>>,>>9.99")
                    else:
                        str_list.s = str_list.s + to_string(t_val, "->>,>>>,>>>,>>9")
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    t_anz = 0
                    t_val = 0
                    zwkum = l_untergrup.zwkum
                    bezeich = l_untergrup.bezeich

                if show_price:
                    tot_val = l_bestand.val_anf_best + l_bestand.wert_eingang - l_bestand.wert_ausgang
                tot_anz = l_bestand.anz_anf_best + l_bestand.anz_eingang - l_bestand.anz_ausgang

                if l_artikel.anzverbrauch != 0:
                    must_order = l_artikel.anzverbrauch - tot_anz
                t_anz = t_anz + tot_anz

                if show_price:
                    t_val = t_val + tot_val
                    t_value = t_value + tot_val
                    tt_val = tt_val + tot_val
                    tt_value = tt_value + tot_val

                if tot_anz != 0 or (tot_anz == 0 and zero_flag):
                    str_list = Str_list()
                    str_list_list.append(str_list)


                    if show_price:

                        if not long_digit:
                            str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensort, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(l_artikel.ek_letzter, ">>>,>>>,>>9.99") + to_string(l_artikel.ek_aktuell, ">>>,>>>,>>9.99") + to_string(l_artikel.vk_preis, "->>,>>>,>>9.99") + to_string(tot_anz, " ->>>,>>9.99") + to_string(tot_val, "->>>,>>>,>>9.99") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                        else:
                            str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensort, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(l_artikel.ek_letzter, ">,>>>,>>>,>>9") + to_string(l_artikel.ek_aktuell, ">,>>>,>>>,>>9") + to_string(l_artikel.vk_preis, "->,>>>,>>>,>>9") + to_string(tot_anz, " ->>>,>>9.99") + to_string(tot_val, "->>,>>>,>>>,>>9") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                    else:

                        if not long_digit:
                            str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensort, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(tot_anz, " ->>>,>>9.99") + to_string(0, "->>>,>>>,>>9.99") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                        else:
                            str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensort, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(0, ">,>>>,>>>,>>9") + to_string(0, ">,>>>,>>>,>>9") + to_string(0, ">,>>>,>>>,>>9") + to_string(tot_anz, " ->>>,>>9.99") + to_string(0, "->>,>>>,>>>,>>9") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")


        if t_val != 0:
            str_list = Str_list()
            str_list_list.append(str_list)

            str_list.flag = 1
            str_list.s = "       "
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
        str_list.s = "       "
        str_list.s = str_list.s + to_string("GRAND T O T A L", "x(50)")
        for j in range(1,84 + 1) :
            str_list.s = str_list.s + " "

        if not long_digit:
            str_list.s = str_list.s + to_string(tt_value, "->>>,>>>,>>9.99")
        else:
            str_list.s = str_list.s + to_string(tt_value, "->>,>>>,>>>,>>9")

    def create_list1():

        nonlocal str_list_list, long_digit, htparam, l_bestand, l_lager, l_artikel, l_untergrup
        nonlocal l_oh


        nonlocal str_list, l_oh
        nonlocal str_list_list

        i:int = 0
        j:int = 0
        tot_anz:decimal = 0
        tot_val:decimal = 0
        t_anz:decimal = 0
        t_val:decimal = 0
        t_value:decimal = 0
        tt_value:decimal = 0
        avrg_price:decimal = 0
        zwkum:int = 0
        bezeich:str = ""
        grp1:int = 0
        grp2:int = 1
        must_order:decimal = 0
        tt_val:decimal = 0
        qty:decimal = 0
        wert:decimal = 0
        tot_bezeich:str = ""
        L_oh = L_bestand
        str_list_list.clear()

        if mattype == 1:
            grp2 = 0

        elif mattype == 2:
            grp1 = 1

        for l_lager in db_session.query(L_lager).filter(
                (L_lager.lager_nr >= from_lager) &  (L_lager.lager_nr <= to_lager)).all():
            i = 0
            zwkum = 0
            t_anz = 0
            t_val = 0
            tt_val = 0
            tot_bezeich = "Ttl - " + l_lager.bezeich

            if sorttype == 1:

                if sub_grp != 000:

                    l_bestand_obj_list = []
                    for l_bestand, l_artikel, l_oh, l_untergrup in db_session.query(L_bestand, L_artikel, L_oh, L_untergrup).join(L_artikel,(L_artikel.artnr == L_bestand.artnr) &  (L_artikel.zwkum == sub_grp)).join(L_oh,(L_oh.artnr == L_bestand.artnr) &  (L_oh.lager_nr == 0)).join(L_untergrup,(L_untergrup.zwkum == l_artikel.zwkum) &  ((L_untergrup.betriebsnr >= grp1) &  (L_untergrup.betriebsnr <= grp2))).filter(
                            (L_bestand.lager_nr == l_lager.lager_nr)).all():
                        if l_bestand._recid in l_bestand_obj_list:
                            continue
                        else:
                            l_bestand_obj_list.append(l_bestand._recid)


                        i = i + 1
                        must_order = 0

                        if i == 1:
                            str_list = Str_list()
                            str_list_list.append(str_list)

                            str_list.s = "        " + to_string(l_lager.lager_nr, "99") + " " + to_string(l_lager.bezeich, "x(50)")

                        if zwkum == 0:
                            zwkum = l_artikel.zwkum
                            bezeich = l_untergrup.bezeich

                        if zwkum != l_artikel.zwkum:
                            str_list = Str_list()
                            str_list_list.append(str_list)

                            str_list.flag = 1
                            str_list.s = "       "
                            str_list.s = str_list.s + to_string(bezeich, "x(50)")
                            for j in range(1,84 + 1) :
                                str_list.s = str_list.s + " "

                            if not long_digit:
                                str_list.s = str_list.s + to_string(t_val, "->>>,>>>,>>9.99")
                            else:
                                str_list.s = str_list.s + to_string(t_val, "->>,>>>,>>>,>>9")
                            str_list = Str_list()
                            str_list_list.append(str_list)

                            t_anz = 0
                            t_val = 0
                            zwkum = l_untergrup.zwkum
                            bezeich = l_untergrup.bezeich
                        qty = l_oh.anz_anf_best + l_oh.anz_eingang - l_oh.anz_ausgang

                        if show_price:
                            wert = l_oh.val_anf_best + l_oh.wert_eingang - l_oh.wert_ausgang
                        tot_anz = l_bestand.anz_anf_best + l_bestand.anz_eingang - l_bestand.anz_ausgang

                        if l_artikel.anzverbrauch != 0:
                            must_order = l_artikel.anzverbrauch - tot_anz

                        if qty != 0:
                            tot_val = wert * tot_anz / qty
                        else:
                            tot_val = 0
                        t_anz = t_anz + tot_anz

                        if show_price:
                            t_val = t_val + tot_val
                            t_value = t_value + tot_val
                            tt_val = tt_val + tot_val
                            tt_value = tt_value + tot_val

                        if tot_anz != 0 or (tot_anz == 0 and zero_flag):
                            str_list = Str_list()
                            str_list_list.append(str_list)


                            if show_price:

                                if not long_digit:
                                    str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensort, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(l_artikel.ek_letzter, ">>>,>>>,>>9.99") + to_string(l_artikel.ek_aktuell, ">>>,>>>,>>9.99") + to_string(l_artikel.vk_preis, "->>,>>>,>>9.99") + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_val, "->>>,>>>,>>9.99") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                                else:
                                    str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensort, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(l_artikel.ek_letzter, ">,>>>,>>>,>>9") + to_string(l_artikel.ek_aktuell, ">,>>>,>>>,>>9") + to_string(l_artikel.vk_preis, "->,>>>,>>>,>>9") + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_val, "->>,>>>,>>>,>>9") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                            else:

                                if not long_digit:
                                    str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensort, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(tot_anz, "->,>>>,>>9.99") + to_string(0, "->>>,>>>,>>9.99") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                                else:
                                    str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensort, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(0, ">,>>>,>>>,>>9") + to_string(0, ">,>>>,>>>,>>9") + to_string(0, ">,>>>,>>>,>>9") + to_string(tot_anz, "->,>>>,>>9.99") + to_string(0, "->>,>>>,>>>,>>9") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")

            else:

                l_bestand_obj_list = []
                for l_bestand, l_artikel, l_oh, l_untergrup in db_session.query(L_bestand, L_artikel, L_oh, L_untergrup).join(L_artikel,(L_artikel.artnr == L_bestand.artnr) &  (L_artikel.endkum == from_grp)).join(L_oh,(L_oh.artnr == L_bestand.artnr) &  (L_oh.lager_nr == 0)).join(L_untergrup,(L_untergrup.zwkum == l_artikel.zwkum) &  ((L_untergrup.betriebsnr >= grp1) &  (L_untergrup.betriebsnr <= grp2))).filter(
                        (L_bestand.lager_nr == l_lager.lager_nr)).all():
                    if l_bestand._recid in l_bestand_obj_list:
                        continue
                    else:
                        l_bestand_obj_list.append(l_bestand._recid)


                    i = i + 1
                    must_order = 0

                    if i == 1:
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        str_list.s = "        " + to_string(l_lager.lager_nr, "99") + " " + to_string(l_lager.bezeich, "x(50)")

                    if zwkum == 0:
                        zwkum = l_artikel.zwkum
                        bezeich = l_untergrup.bezeich

                    if zwkum != l_artikel.zwkum:
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        str_list.flag = 1
                        str_list.s = "       "
                        str_list.s = str_list.s + to_string(bezeich, "x(50)")
                        for j in range(1,84 + 1) :
                            str_list.s = str_list.s + " "

                        if not long_digit:
                            str_list.s = str_list.s + to_string(t_val, "->>>,>>>,>>9.99")
                        else:
                            str_list.s = str_list.s + to_string(t_val, "->>,>>>,>>>,>>9")
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        t_anz = 0
                        t_val = 0
                        zwkum = l_untergrup.zwkum
                        bezeich = l_untergrup.bezeich
                    qty = l_oh.anz_anf_best + l_oh.anz_eingang - l_oh.anz_ausgang

                    if show_price:
                        wert = l_oh.val_anf_best + l_oh.wert_eingang - l_oh.wert_ausgang
                    tot_anz = l_bestand.anz_anf_best + l_bestand.anz_eingang - l_bestand.anz_ausgang

                    if l_artikel.anzverbrauch != 0:
                        must_order = l_artikel.anzverbrauch - tot_anz

                    if qty != 0:
                        tot_val = wert * tot_anz / qty
                    else:
                        tot_val = 0
                    t_anz = t_anz + tot_anz

                    if show_price:
                        t_val = t_val + tot_val
                        t_value = t_value + tot_val
                        tt_val = tt_val + tot_val
                        tt_value = tt_value + tot_val

                    if tot_anz != 0 or (tot_anz == 0 and zero_flag):
                        str_list = Str_list()
                        str_list_list.append(str_list)


                        if show_price:

                            if not long_digit:
                                str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensort, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(l_artikel.ek_letzter, ">>>,>>>,>>9.99") + to_string(l_artikel.ek_aktuell, ">>>,>>>,>>9.99") + to_string(l_artikel.vk_preis, "->>,>>>,>>9.99") + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_val, "->>>,>>>,>>9.99") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                            else:
                                str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensort, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(l_artikel.ek_letzter, ">,>>>,>>>,>>9") + to_string(l_artikel.ek_aktuell, ">,>>>,>>>,>>9") + to_string(l_artikel.vk_preis, "->,>>>,>>>,>>9") + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_val, "->>,>>>,>>>,>>9") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                        else:

                            if not long_digit:
                                str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensort, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(tot_anz, "->,>>>,>>9.99") + to_string(0, "->>>,>>>,>>9.99") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                            else:
                                str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensort, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(0, ">,>>>,>>>,>>9") + to_string(0, ">,>>>,>>>,>>9") + to_string(0, ">,>>>,>>>,>>9") + to_string(tot_anz, "->,>>>,>>9.99") + to_string(0, "->>,>>>,>>>,>>9") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")


            elif sorttype == 2:

                if sub_grp != 000:

                    l_bestand_obj_list = []
                    for l_bestand, l_artikel, l_oh, l_untergrup in db_session.query(L_bestand, L_artikel, L_oh, L_untergrup).join(L_artikel,(L_artikel.artnr == L_bestand.artnr) &  (L_artikel.zwkum == sub_grp)).join(L_oh,(L_oh.artnr == L_bestand.artnr) &  (L_oh.lager_nr == 0)).join(L_untergrup,(L_untergrup.zwkum == l_artikel.zwkum) &  ((L_untergrup.betriebsnr >= grp1) &  (L_untergrup.betriebsnr <= grp2))).filter(
                            (L_bestand.lager_nr == l_lager.lager_nr)).all():
                        if l_bestand._recid in l_bestand_obj_list:
                            continue
                        else:
                            l_bestand_obj_list.append(l_bestand._recid)


                        i = i + 1
                        must_order = 0

                        if i == 1:
                            str_list = Str_list()
                            str_list_list.append(str_list)

                            str_list.s = "        " + to_string(l_lager.lager_nr, "99") + " " + to_string(l_lager.bezeich, "x(13)")

                        if zwkum == 0:
                            zwkum = l_artikel.zwkum
                            bezeich = l_untergrup.bezeich

                        if zwkum != l_artikel.zwkum:
                            str_list = Str_list()
                            str_list_list.append(str_list)

                            str_list.flag = 1
                            str_list.s = "       "
                            str_list.s = str_list.s + to_string(bezeich, "x(50)")
                            for j in range(1,84 + 1) :
                                str_list.s = str_list.s + " "

                            if not long_digit:
                                str_list.s = str_list.s + to_string(t_val, "->>>,>>>,>>9.99")
                            else:
                                str_list.s = str_list.s + to_string(t_val, "->>,>>>,>>>,>>9")
                            str_list = Str_list()
                            str_list_list.append(str_list)

                            t_anz = 0
                            t_val = 0
                            zwkum = l_untergrup.zwkum
                            bezeich = l_untergrup.bezeich
                        qty = l_oh.anz_anf_best + l_oh.anz_eingang - l_oh.anz_ausgang

                        if show_price:
                            wert = l_oh.val_anf_best + l_oh.wert_eingang - l_oh.wert_ausgang
                        tot_anz = l_bestand.anz_anf_best + l_bestand.anz_eingang - l_bestand.anz_ausgang

                        if l_artikel.anzverbrauch != 0:
                            must_order = l_artikel.anzverbrauch - tot_anz

                        if qty != 0:
                            tot_val = wert * tot_anz / qty
                        else:
                            tot_val = 0
                        t_anz = t_anz + tot_anz

                        if show_price:
                            t_val = t_val + tot_val
                            t_value = t_value + tot_val
                            tt_val = tt_val + tot_val
                            tt_value = tt_value + tot_val

                        if tot_anz != 0 or (tot_anz == 0 and zero_flag):
                            str_list = Str_list()
                            str_list_list.append(str_list)


                            if show_price:

                                if not long_digit:
                                    str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensort, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(l_artikel.ek_letzter, ">>>,>>>,>>9.99") + to_string(l_artikel.ek_aktuell, ">>>,>>>,>>9.99") + to_string(l_artikel.vk_preis, "->>,>>>,>>9.99") + to_string(tot_anz, " ->>>,>>9.99") + to_string(tot_val, "->>>,>>>,>>9.99") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                                else:
                                    str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensort, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(l_artikel.ek_letzter, ">,>>>,>>>,>>9") + to_string(l_artikel.ek_aktuell, ">,>>>,>>>,>>9") + to_string(l_artikel.vk_preis, "->,>>>,>>>,>>9") + to_string(tot_anz, " ->>>,>>9.99") + to_string(tot_val, "->>,>>>,>>>,>>9") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                            else:

                                if not long_digit:
                                    str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensort, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(tot_anz, " ->>>,>>9.99") + to_string(0, "->>>,>>>,>>9.99") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                                else:
                                    str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensort, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(0, ">,>>>,>>>,>>9") + to_string(0, ">,>>>,>>>,>>9") + to_string(0, ">,>>>,>>>,>>9") + to_string(tot_anz, " ->>>,>>9.99") + to_string(0, "->>,>>>,>>>,>>9") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")

            else:

                l_bestand_obj_list = []
                for l_bestand, l_artikel, l_oh, l_untergrup in db_session.query(L_bestand, L_artikel, L_oh, L_untergrup).join(L_artikel,(L_artikel.artnr == L_bestand.artnr) &  (L_artikel.endkum == from_grp)).join(L_oh,(L_oh.artnr == L_bestand.artnr) &  (L_oh.lager_nr == 0)).join(L_untergrup,(L_untergrup.zwkum == l_artikel.zwkum) &  ((L_untergrup.betriebsnr >= grp1) &  (L_untergrup.betriebsnr <= grp2))).filter(
                        (L_bestand.lager_nr == l_lager.lager_nr)).all():
                    if l_bestand._recid in l_bestand_obj_list:
                        continue
                    else:
                        l_bestand_obj_list.append(l_bestand._recid)


                    i = i + 1
                    must_order = 0

                    if i == 1:
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        str_list.s = "        " + to_string(l_lager.lager_nr, "99") + " " + to_string(l_lager.bezeich, "x(13)")

                    if zwkum == 0:
                        zwkum = l_artikel.zwkum
                        bezeich = l_untergrup.bezeich

                    if zwkum != l_artikel.zwkum:
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        str_list.flag = 1
                        str_list.s = "       "
                        str_list.s = str_list.s + to_string(bezeich, "x(50)")
                        for j in range(1,84 + 1) :
                            str_list.s = str_list.s + " "

                        if not long_digit:
                            str_list.s = str_list.s + to_string(t_val, "->>>,>>>,>>9.99")
                        else:
                            str_list.s = str_list.s + to_string(t_val, "->>,>>>,>>>,>>9")
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        t_anz = 0
                        t_val = 0
                        zwkum = l_untergrup.zwkum
                        bezeich = l_untergrup.bezeich
                    qty = l_oh.anz_anf_best + l_oh.anz_eingang - l_oh.anz_ausgang

                    if show_price:
                        wert = l_oh.val_anf_best + l_oh.wert_eingang - l_oh.wert_ausgang
                    tot_anz = l_bestand.anz_anf_best + l_bestand.anz_eingang - l_bestand.anz_ausgang

                    if l_artikel.anzverbrauch != 0:
                        must_order = l_artikel.anzverbrauch - tot_anz

                    if qty != 0:
                        tot_val = wert * tot_anz / qty
                    else:
                        tot_val = 0
                    t_anz = t_anz + tot_anz

                    if show_price:
                        t_val = t_val + tot_val
                        t_value = t_value + tot_val
                        tt_val = tt_val + tot_val
                        tt_value = tt_value + tot_val

                    if tot_anz != 0 or (tot_anz == 0 and zero_flag):
                        str_list = Str_list()
                        str_list_list.append(str_list)


                        if show_price:

                            if not long_digit:
                                str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensort, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(l_artikel.ek_letzter, ">>>,>>>,>>9.99") + to_string(l_artikel.ek_aktuell, ">>>,>>>,>>9.99") + to_string(l_artikel.vk_preis, "->>,>>>,>>9.99") + to_string(tot_anz, " ->>>,>>9.99") + to_string(tot_val, "->>>,>>>,>>9.99") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                            else:
                                str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensort, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(l_artikel.ek_letzter, ">,>>>,>>>,>>9") + to_string(l_artikel.ek_aktuell, ">,>>>,>>>,>>9") + to_string(l_artikel.vk_preis, "->,>>>,>>>,>>9") + to_string(tot_anz, " ->>>,>>9.99") + to_string(tot_val, "->>,>>>,>>>,>>9") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                        else:

                            if not long_digit:
                                str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensort, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(tot_anz, " ->>>,>>9.99") + to_string(0, "->>>,>>>,>>9.99") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                            else:
                                str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensort, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(0, ">,>>>,>>>,>>9") + to_string(0, ">,>>>,>>>,>>9") + to_string(0, ">,>>>,>>>,>>9") + to_string(tot_anz, " ->>>,>>9.99") + to_string(0, "->>,>>>,>>>,>>9") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")


            if t_val != 0:
                str_list = Str_list()
                str_list_list.append(str_list)

                str_list.flag = 1
                str_list.s = "       "
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
                str_list.s = "       "
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
        str_list.s = "       "
        str_list.s = str_list.s + to_string("GRAND T O T A L", "x(50)")
        for j in range(1,84 + 1) :
            str_list.s = str_list.s + " "

        if not long_digit:
            str_list.s = str_list.s + to_string(tt_value, "->>>,>>>,>>9.99")
        else:
            str_list.s = str_list.s + to_string(tt_value, "->>,>>>,>>>,>>9")

    def create_list1a():

        nonlocal str_list_list, long_digit, htparam, l_bestand, l_lager, l_artikel, l_untergrup
        nonlocal l_oh


        nonlocal str_list, l_oh
        nonlocal str_list_list

        i:int = 0
        j:int = 0
        tot_anz:decimal = 0
        tot_val:decimal = 0
        t_anz:decimal = 0
        t_val:decimal = 0
        t_value:decimal = 0
        tt_value:decimal = 0
        avrg_price:decimal = 0
        zwkum:int = 0
        bezeich:str = ""
        grp1:int = 0
        grp2:int = 1
        must_order:decimal = 0
        tt_val:decimal = 0
        qty:decimal = 0
        wert:decimal = 0
        tot_bezeich:str = ""
        L_oh = L_bestand
        str_list_list.clear()

        if mattype == 1:
            grp2 = 0

        elif mattype == 2:
            grp1 = 1
        i = 0
        zwkum = 0
        t_anz = 0
        t_val = 0
        tt_val = 0

        if sorttype == 1:

            if sub_grp != 000:

                l_bestand_obj_list = []
                for l_bestand, l_artikel, l_untergrup in db_session.query(L_bestand, L_artikel, L_untergrup).join(L_artikel,(L_artikel.artnr == L_bestand.artnr) &  (L_artikel.zwkum == sub_grp)).join(L_untergrup,(L_untergrup.zwkum == l_artikel.zwkum) &  ((L_untergrup.betriebsnr >= grp1) &  (L_untergrup.betriebsnr <= grp2))).filter(
                            (L_bestand.lager_nr == 0)).all():
                    if l_bestand._recid in l_bestand_obj_list:
                        continue
                    else:
                        l_bestand_obj_list.append(l_bestand._recid)


                    i = i + 1
                    must_order = 0

                    if zwkum == 0:
                        zwkum = l_artikel.zwkum
                        bezeich = l_untergrup.bezeich

                    if zwkum != l_artikel.zwkum:
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        str_list.flag = 1
                        str_list.s = "       "
                        str_list.s = str_list.s + to_string(bezeich, "x(50)")
                        for j in range(1,84 + 1) :
                            str_list.s = str_list.s + " "

                        if not long_digit:
                            str_list.s = str_list.s + to_string(t_val, "->>>,>>>,>>9.99")
                        else:
                            str_list.s = str_list.s + to_string(t_val, "->>,>>>,>>>,>>9")
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        t_anz = 0
                        t_val = 0
                        zwkum = l_untergrup.zwkum
                        bezeich = l_untergrup.bezeich

                    if show_price:
                        tot_val = l_bestand.val_anf_best + l_bestand.wert_eingang - l_bestand.wert_ausgang
                    tot_anz = l_bestand.anz_anf_best + l_bestand.anz_eingang - l_bestand.anz_ausgang

                    if l_artikel.anzverbrauch != 0:
                        must_order = l_artikel.anzverbrauch - tot_anz
                    t_anz = t_anz + tot_anz

                    if show_price:
                        t_val = t_val + tot_val
                        t_value = t_value + tot_val
                        tt_val = tt_val + tot_val
                        tt_value = tt_value + tot_val

                    if tot_anz != 0 or (tot_anz == 0 and zero_flag):
                        str_list = Str_list()
                        str_list_list.append(str_list)


                        if show_price:

                            if not long_digit:
                                str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensort, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(l_artikel.ek_letzter, ">>>,>>>,>>9.99") + to_string(l_artikel.ek_aktuell, ">>>,>>>,>>9.99") + to_string(l_artikel.vk_preis, "->>,>>>,>>9.99") + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_val, "->>>,>>>,>>9.99") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                            else:
                                str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensort, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(l_artikel.ek_letzter, ">,>>>,>>>,>>9") + to_string(l_artikel.ek_aktuell, ">,>>>,>>>,>>9") + to_string(l_artikel.vk_preis, "->,>>>,>>>,>>9") + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_val, "->>,>>>,>>>,>>9") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                        else:

                            if not long_digit:
                                str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensort, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(tot_anz, "->,>>>,>>9.99") + to_string(0, "->>>,>>>,>>9.99") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                            else:
                                str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensort, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(0, ">,>>>,>>>,>>9") + to_string(0, ">,>>>,>>>,>>9") + to_string(0, ">,>>>,>>>,>>9") + to_string(tot_anz, "->,>>>,>>9.99") + to_string(0, "->>,>>>,>>>,>>9") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")

        else:

            l_bestand_obj_list = []
            for l_bestand, l_artikel, l_untergrup in db_session.query(L_bestand, L_artikel, L_untergrup).join(L_artikel,(L_artikel.artnr == L_bestand.artnr) &  (L_artikel.endkum == from_grp)).join(L_untergrup,(L_untergrup.zwkum == l_artikel.zwkum) &  ((L_untergrup.betriebsnr >= grp1) &  (L_untergrup.betriebsnr <= grp2))).filter(
                        (L_bestand.lager_nr == 0)).all():
                if l_bestand._recid in l_bestand_obj_list:
                    continue
                else:
                    l_bestand_obj_list.append(l_bestand._recid)


                i = i + 1
                must_order = 0

                if zwkum == 0:
                    zwkum = l_artikel.zwkum
                    bezeich = l_untergrup.bezeich

                if zwkum != l_artikel.zwkum:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.flag = 1
                    str_list.s = "       "
                    str_list.s = str_list.s + to_string(bezeich, "x(50)")
                    for j in range(1,84 + 1) :
                        str_list.s = str_list.s + " "

                    if not long_digit:
                        str_list.s = str_list.s + to_string(t_val, "->>>,>>>,>>9.99")
                    else:
                        str_list.s = str_list.s + to_string(t_val, "->>,>>>,>>>,>>9")
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    t_anz = 0
                    t_val = 0
                    zwkum = l_untergrup.zwkum
                    bezeich = l_untergrup.bezeich

                if show_price:
                    tot_val = l_bestand.val_anf_best + l_bestand.wert_eingang - l_bestand.wert_ausgang
                tot_anz = l_bestand.anz_anf_best + l_bestand.anz_eingang - l_bestand.anz_ausgang

                if l_artikel.anzverbrauch != 0:
                    must_order = l_artikel.anzverbrauch - tot_anz
                t_anz = t_anz + tot_anz

                if show_price:
                    t_val = t_val + tot_val
                    t_value = t_value + tot_val
                    tt_val = tt_val + tot_val
                    tt_value = tt_value + tot_val

                if tot_anz != 0 or (tot_anz == 0 and zero_flag):
                    str_list = Str_list()
                    str_list_list.append(str_list)


                    if show_price:

                        if not long_digit:
                            str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensort, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(l_artikel.ek_letzter, ">>>,>>>,>>9.99") + to_string(l_artikel.ek_aktuell, ">>>,>>>,>>9.99") + to_string(l_artikel.vk_preis, "->>,>>>,>>9.99") + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_val, "->>>,>>>,>>9.99") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                        else:
                            str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensort, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(l_artikel.ek_letzter, ">,>>>,>>>,>>9") + to_string(l_artikel.ek_aktuell, ">,>>>,>>>,>>9") + to_string(l_artikel.vk_preis, "->,>>>,>>>,>>9") + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_val, "->>,>>>,>>>,>>9") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                    else:

                        if not long_digit:
                            str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensort, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(tot_anz, "->,>>>,>>9.99") + to_string(0, "->>>,>>>,>>9.99") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                        else:
                            str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensort, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(0, ">,>>>,>>>,>>9") + to_string(0, ">,>>>,>>>,>>9") + to_string(0, ">,>>>,>>>,>>9") + to_string(tot_anz, "->,>>>,>>9.99") + to_string(0, "->>,>>>,>>>,>>9") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")


        elif sorttype == 2:

            if sub_grp != 000:

                l_bestand_obj_list = []
                for l_bestand, l_artikel, l_untergrup in db_session.query(L_bestand, L_artikel, L_untergrup).join(L_artikel,(L_artikel.artnr == L_bestand.artnr) &  (L_artikel.zwkum == sub_grp)).join(L_untergrup,(L_untergrup.zwkum == l_artikel.zwkum) &  ((L_untergrup.betriebsnr >= grp1) &  (L_untergrup.betriebsnr <= grp2))).filter(
                            (L_bestand.lager_nr == 0)).all():
                    if l_bestand._recid in l_bestand_obj_list:
                        continue
                    else:
                        l_bestand_obj_list.append(l_bestand._recid)


                    i = i + 1
                    must_order = 0

                    if zwkum == 0:
                        zwkum = l_artikel.zwkum
                        bezeich = l_untergrup.bezeich

                    if zwkum != l_artikel.zwkum:
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        str_list.flag = 1
                        str_list.s = "       "
                        str_list.s = str_list.s + to_string(bezeich, "x(50)")
                        for j in range(1,84 + 1) :
                            str_list.s = str_list.s + " "

                        if not long_digit:
                            str_list.s = str_list.s + to_string(t_val, "->>>,>>>,>>9.99")
                        else:
                            str_list.s = str_list.s + to_string(t_val, "->>,>>>,>>>,>>9")
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        t_anz = 0
                        t_val = 0
                        zwkum = l_untergrup.zwkum
                        bezeich = l_untergrup.bezeich
                    tot_anz = l_bestand.anz_anf_best + l_bestand.anz_eingang - l_bestand.anz_ausgang

                    if show_price:
                        tot_val = l_bestand.val_anf_best + l_bestand.wert_eingang - l_bestand.wert_ausgang

                    if l_artikel.anzverbrauch != 0:
                        must_order = l_artikel.anzverbrauch - tot_anz
                    t_anz = t_anz + tot_anz

                    if show_price:
                        t_val = t_val + tot_val
                        t_value = t_value + tot_val
                        tt_val = tt_val + tot_val
                        tt_value = tt_value + tot_val

                    if tot_anz != 0 or (tot_anz == 0 and zero_flag):
                        str_list = Str_list()
                        str_list_list.append(str_list)


                        if show_price:

                            if not long_digit:
                                str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensort, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(l_artikel.ek_letzter, ">>>,>>>,>>9.99") + to_string(l_artikel.ek_aktuell, ">>>,>>>,>>9.99") + to_string(l_artikel.vk_preis, "->>,>>>,>>9.99") + to_string(tot_anz, " ->>>,>>9.99") + to_string(tot_val, "->>>,>>>,>>9.99") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                            else:
                                str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensort, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(l_artikel.ek_letzter, ">,>>>,>>>,>>9") + to_string(l_artikel.ek_aktuell, ">,>>>,>>>,>>9") + to_string(l_artikel.vk_preis, "->,>>>,>>>,>>9") + to_string(tot_anz, " ->>>,>>9.99") + to_string(tot_val, "->>,>>>,>>>,>>9") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                        else:

                            if not long_digit:
                                str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensort, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(tot_anz, " ->>>,>>9.99") + to_string(0, "->>>,>>>,>>9.99") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                            else:
                                str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensort, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(0, ">,>>>,>>>,>>9") + to_string(0, ">,>>>,>>>,>>9") + to_string(0, ">,>>>,>>>,>>9") + to_string(tot_anz, " ->>>,>>9.99") + to_string(0, "->>,>>>,>>>,>>9") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")

        else:

            l_bestand_obj_list = []
            for l_bestand, l_artikel, l_untergrup in db_session.query(L_bestand, L_artikel, L_untergrup).join(L_artikel,(L_artikel.artnr == L_bestand.artnr) &  (L_artikel.endkum == from_grp)).join(L_untergrup,(L_untergrup.zwkum == l_artikel.zwkum) &  ((L_untergrup.betriebsnr >= grp1) &  (L_untergrup.betriebsnr <= grp2))).filter(
                        (L_bestand.lager_nr == 0)).all():
                if l_bestand._recid in l_bestand_obj_list:
                    continue
                else:
                    l_bestand_obj_list.append(l_bestand._recid)


                i = i + 1
                must_order = 0

                if zwkum == 0:
                    zwkum = l_artikel.zwkum
                    bezeich = l_untergrup.bezeich

                if zwkum != l_artikel.zwkum:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.flag = 1
                    str_list.s = "       "
                    str_list.s = str_list.s + to_string(bezeich, "x(50)")
                    for j in range(1,84 + 1) :
                        str_list.s = str_list.s + " "

                    if not long_digit:
                        str_list.s = str_list.s + to_string(t_val, "->>>,>>>,>>9.99")
                    else:
                        str_list.s = str_list.s + to_string(t_val, "->>,>>>,>>>,>>9")
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    t_anz = 0
                    t_val = 0
                    zwkum = l_untergrup.zwkum
                    bezeich = l_untergrup.bezeich
                tot_anz = l_bestand.anz_anf_best + l_bestand.anz_eingang - l_bestand.anz_ausgang

                if show_price:
                    tot_val = l_bestand.val_anf_best + l_bestand.wert_eingang - l_bestand.wert_ausgang

                if l_artikel.anzverbrauch != 0:
                    must_order = l_artikel.anzverbrauch - tot_anz
                t_anz = t_anz + tot_anz

                if show_price:
                    t_val = t_val + tot_val
                    t_value = t_value + tot_val
                    tt_val = tt_val + tot_val
                    tt_value = tt_value + tot_val

                if tot_anz != 0 or (tot_anz == 0 and zero_flag):
                    str_list = Str_list()
                    str_list_list.append(str_list)


                    if show_price:

                        if not long_digit:
                            str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensort, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(l_artikel.ek_letzter, ">>>,>>>,>>9.99") + to_string(l_artikel.ek_aktuell, ">>>,>>>,>>9.99") + to_string(l_artikel.vk_preis, "->>,>>>,>>9.99") + to_string(tot_anz, " ->>>,>>9.99") + to_string(tot_val, "->>>,>>>,>>9.99") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                        else:
                            str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensort, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(l_artikel.ek_letzter, ">,>>>,>>>,>>9") + to_string(l_artikel.ek_aktuell, ">,>>>,>>>,>>9") + to_string(l_artikel.vk_preis, "->,>>>,>>>,>>9") + to_string(tot_anz, " ->>>,>>9.99") + to_string(tot_val, "->>,>>>,>>>,>>9") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                    else:

                        if not long_digit:
                            str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensort, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(tot_anz, " ->>>,>>9.99") + to_string(0, "->>>,>>>,>>9.99") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")
                        else:
                            str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_artikel.masseinheit, "x(3)") + to_string(l_artikel.inhalt, ">>,>>9.99") + to_string(l_artikel.traubensort, "x(8)") + to_string(l_artikel.lief_einheit, ">>,>>9.99") + to_string(0, ">,>>>,>>>,>>9") + to_string(0, ">,>>>,>>>,>>9") + to_string(0, ">,>>>,>>>,>>9") + to_string(tot_anz, " ->>>,>>9.99") + to_string(0, "->>,>>>,>>>,>>9") + to_string(l_artikel.min_bestand, ">>,>>>") + to_string(must_order, "->,>>>,>>9.99")


        if t_val != 0:
            str_list = Str_list()
            str_list_list.append(str_list)

            str_list.flag = 1
            str_list.s = "       "
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
        str_list.s = "       "
        str_list.s = str_list.s + to_string("GRAND T O T A L", "x(50)")
        for j in range(1,84 + 1) :
            str_list.s = str_list.s + " "

        if not long_digit:
            str_list.s = str_list.s + to_string(tt_value, "->>>,>>>,>>9.99")
        else:
            str_list.s = str_list.s + to_string(tt_value, "->>,>>>,>>>,>>9")

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 246)).first()
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