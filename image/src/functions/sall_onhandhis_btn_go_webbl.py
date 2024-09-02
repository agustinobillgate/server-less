from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam, L_besthis, L_lager, L_artikel, L_untergrup

def sall_onhandhis_btn_go_webbl(anf_date:date, end_date:date, all_flag:bool, show_price:bool, zero_flag:bool, from_grp:int, sub_grp:int, from_lager:int, to_lager:int, sorttype:int, mattype:int):
    done = False
    out_list_list = []
    long_digit:bool = False
    vk_preis:decimal = 0
    htparam = l_besthis = l_lager = l_artikel = l_untergrup = None

    out_list = l_oh = None

    out_list_list, Out_list = create_model("Out_list", {"artnr":int, "bezeich":str, "unit":str, "qty":decimal, "val":decimal, "content":decimal, "d_unit":str, "d_content":decimal, "last_price":decimal, "act_price":decimal, "avrg_price":decimal, "flag":int})

    L_oh = L_besthis

    db_session = local_storage.db_session

    def generate_output():
        nonlocal done, out_list_list, long_digit, vk_preis, htparam, l_besthis, l_lager, l_artikel, l_untergrup
        nonlocal l_oh


        nonlocal out_list, l_oh
        nonlocal out_list_list
        return {"done": done, "out-list": out_list_list}

    def create_list():

        nonlocal done, out_list_list, long_digit, vk_preis, htparam, l_besthis, l_lager, l_artikel, l_untergrup
        nonlocal l_oh


        nonlocal out_list, l_oh
        nonlocal out_list_list

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
        qty:decimal = 0
        wert:decimal = 0
        tot_bezeich:str = ""
        tt_val:decimal = 0
        tt_value:decimal = 0
        s_bezeich:str = ""
        L_oh = L_besthis

        for l_lager in db_session.query(L_lager).filter(
                (L_lager.lager_nr >= from_lager) &  (L_lager.lager_nr <= to_lager)).all():
            tot_bezeich = "Ttl - " + l_lager.bezeich
            out_list = Out_list()
            out_list_list.append(out_list)

            s_bezeich = to_string(l_lager.lager_nr, "99") + " " + to_string(l_lager.bezeich, "x(13)")
            out_list.bezeich = to_string(l_lager.lager_nr, "99") + " " + to_string(l_lager.bezeich, "x(13)")
            i = 0
            zwkum = 0
            t_anz = 0
            t_val = 0
            tt_val = 0

            if sorttype == 1:

                l_besthis_obj_list = []
                for l_besthis, l_artikel, l_oh, l_untergrup in db_session.query(L_besthis, L_artikel, L_oh, L_untergrup).join(L_artikel,(L_artikel.artnr == L_besthis.artnr)).join(L_oh,(L_oh.anf_best_dat >= anf_date) &  (L_oh.anf_best_dat <= end_date) &  (L_oh.lager_nr == 0) &  (L_oh.artnr == L_besthis.artnr)).join(L_untergrup,(L_untergrup.zwkum == l_artikel.zwkum)).filter(
                        (L_besthis.anf_best_dat >= anf_date) &  (L_besthis.anf_best_dat <= end_date) &  (L_besthis.lager_nr == l_lager.lager_nr)).all():
                    if l_besthis._recid in l_besthis_obj_list:
                        continue
                    else:
                        l_besthis_obj_list.append(l_besthis._recid)

                    if (from_grp == 0 and sub_grp == 0) or (l_artikel.endkum == from_grp and sub_grp == 0) or (l_artikel.endkum == from_grp and l_artikel.zwkum == sub_grp) or (from_grp == 0 and l_artikel.zwkum == sub_grp):

                        if zwkum == 0:
                            zwkum = l_artikel.zwkum
                            bezeich = l_untergrup.bezeich

                        if zwkum != l_artikel.zwkum:

                            if t_val != 0:
                                out_list = Out_list()
                                out_list_list.append(out_list)

                                out_list.flag = 1
                                out_list.bezeich = bezeich
                                out_list.val = t_val


                                out_list = Out_list()
                                out_list_list.append(out_list)

                            out_list.flag = 0
                            t_anz = 0
                            t_val = 0
                            zwkum = l_untergrup.zwkum
                            bezeich = l_untergrup.bezeich


                        qty = l_oh.anz_anf_best + l_oh.anz_eingang - l_oh.anz_ausgang

                        if show_price:
                            wert = l_oh.val_anf_best + l_oh.wert_eingang - l_oh.wert_ausgang
                        tot_anz = l_besthis.anz_anf_best + l_besthis.anz_eingang - l_besthis.anz_ausgang

                        if qty != 0:
                            tot_val = wert * tot_anz / qty
                        else:
                            tot_val = 0

                        if tot_anz != 0:
                            vk_preis = tot_val / tot_anz
                        else:
                            vk_preis = 0
                        t_anz = t_anz + tot_anz

                        if show_price:
                            t_val = t_val + tot_val


                            t_value = t_value + tot_val
                            tt_val = tt_val + tot_val
                            tt_value = tt_value + tot_val

                        if tot_anz != 0 or (tot_anz == 0 and zero_flag):
                            out_list = Out_list()
                            out_list_list.append(out_list)

                            out_list.flag = 2

                            if show_price:
                                out_list.artnr = l_artikel.artnr
                                out_list.bezeich = l_artikel.bezeich
                                out_list.unit = l_artikel.masseinheit
                                out_list.content = l_artikel.inhalt
                                out_list.d_unit = l_artikel.traubensort
                                out_list.d_content = l_artikel.lief_einheit
                                out_list.last_price = l_artikel.ek_letzter
                                out_list.act_price = l_artikel.ek_aktuell
                                out_list.avrg_price = vk_preis
                                out_list.qty = tot_anz
                                out_list.val = tot_val


                            else:
                                out_list.artnr = l_artikel.artnr
                                out_list.bezeich = l_artikel.bezeich
                                out_list.unit = l_artikel.masseinheit
                                out_list.content = l_artikel.inhalt
                                out_list.d_unit = l_artikel.traubensort
                                out_list.d_content = l_artikel.lief_einheit
                                out_list.last_price = 0
                                out_list.act_price = 0
                                out_list.avrg_price = 0
                                out_list.qty = tot_anz
                                out_list.val = 0

            elif sorttype == 2:

                l_besthis_obj_list = []
                for l_besthis, l_artikel, l_oh, l_untergrup in db_session.query(L_besthis, L_artikel, L_oh, L_untergrup).join(L_artikel,(L_artikel.artnr == L_besthis.artnr)).join(L_oh,(L_oh.anf_best_dat >= anf_date) &  (L_oh.anf_best_dat <= end_date) &  (L_oh.lager_nr == 0) &  (L_oh.artnr == L_besthis.artnr)).join(L_untergrup,(L_untergrup.zwkum == l_artikel.zwkum)).filter(
                        (L_besthis.anf_best_dat >= anf_date) &  (L_besthis.anf_best_dat <= end_date) &  (L_besthis.lager_nr == l_lager.lager_nr)).all():
                    if l_besthis._recid in l_besthis_obj_list:
                        continue
                    else:
                        l_besthis_obj_list.append(l_besthis._recid)

                    if (from_grp == 0 and sub_grp == 0) or (l_artikel.endkum == from_grp and sub_grp == 0) or (l_artikel.endkum == from_grp and l_artikel.zwkum == sub_grp) or (from_grp == 0 and l_artikel.zwkum == sub_grp):

                        if zwkum == 0:
                            zwkum = l_artikel.zwkum
                            bezeich = l_untergrup.bezeich

                        if zwkum != l_artikel.zwkum:

                            if t_val != 0:
                                out_list = Out_list()
                                out_list_list.append(out_list)

                                out_list.flag = 1
                                out_list.bezeich = bezeich
                                out_list.val = t_val


                                out_list = Out_list()
                                out_list_list.append(out_list)

                            t_anz = 0
                            t_val = 0
                            zwkum = l_untergrup.zwkum
                            bezeich = l_untergrup.bezeich


                        qty = l_oh.anz_anf_best + l_oh.anz_eingang - l_oh.anz_ausgang

                        if show_price:
                            wert = l_oh.val_anf_best + l_oh.wert_eingang - l_oh.wert_ausgang
                        tot_anz = l_besthis.anz_anf_best + l_besthis.anz_eingang - l_besthis.anz_ausgang

                        if qty != 0:
                            tot_val = wert * tot_anz / qty
                        else:
                            tot_val = 0

                        if tot_anz != 0:
                            vk_preis = tot_val / tot_anz
                        else:
                            vk_preis = 0
                        t_anz = t_anz + tot_anz

                        if show_price:
                            t_val = t_val + tot_val


                            t_value = t_value + tot_val
                            tt_val = tt_val + tot_val
                            tt_value = tt_value + tot_val

                        if tot_anz != 0 or (tot_anz == 0 and zero_flag):
                            out_list = Out_list()
                            out_list_list.append(out_list)

                            out_list.flag = 2

                            if show_price:
                                out_list.artnr = l_artikel.artnr
                                out_list.bezeich = l_artikel.bezeich
                                out_list.unit = l_artikel.masseinheit
                                out_list.content = l_artikel.inhalt
                                out_list.d_unit = l_artikel.traubensort
                                out_list.d_content = l_artikel.lief_einheit
                                out_list.last_price = l_artikel.ek_letzter
                                out_list.act_price = l_artikel.ek_aktuell
                                out_list.avrg_price = vk_preis
                                out_list.qty = tot_anz
                                out_list.val = tot_val


                            else:
                                out_list.artnr = l_artikel.artnr
                                out_list.bezeich = l_artikel.bezeich
                                out_list.unit = l_artikel.masseinheit
                                out_list.content = l_artikel.inhalt
                                out_list.d_unit = l_artikel.traubensort
                                out_list.d_content = l_artikel.lief_einheit
                                out_list.last_price = 0
                                out_list.act_price = 0
                                out_list.avrg_price = 0
                                out_list.qty = tot_anz
                                out_list.val = 0

            if t_val != 0:
                out_list = Out_list()
                out_list_list.append(out_list)

                out_list.flag = 1
                out_list.bezeich = bezeich
                out_list.val = t_val


                out_list = Out_list()
                out_list_list.append(out_list)


            if tt_val == 0:

                out_list = query(out_list_list, filters=(lambda out_list :out_list.bezeich.lower()  == (s_bezeich).lower()), first=True)
                out_list_list.remove(out_list)
            else:
                out_list = Out_list()
                out_list_list.append(out_list)

                out_list.flag = 1
                out_list.bezeich = tot_bezeich
                out_list.val = tt_val

        if tt_value != 0:
            out_list = Out_list()
            out_list_list.append(out_list)

            out_list.flag = 1
            out_list.bezeich = "GRAND T O T A L"
            out_list.val = tt_value

    def create_lista():

        nonlocal done, out_list_list, long_digit, vk_preis, htparam, l_besthis, l_lager, l_artikel, l_untergrup
        nonlocal l_oh


        nonlocal out_list, l_oh
        nonlocal out_list_list

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
        qty:decimal = 0
        wert:decimal = 0
        tot_bezeich:str = ""
        tt_val:decimal = 0
        tt_value:decimal = 0
        L_oh = L_besthis
        i = 0
        zwkum = 0
        t_anz = 0
        t_val = 0
        tt_val = 0

        if sorttype == 1:

            l_besthis_obj_list = []
            for l_besthis, l_artikel, l_untergrup in db_session.query(L_besthis, L_artikel, L_untergrup).join(L_artikel,(L_artikel.artnr == L_besthis.artnr)).join(L_untergrup,(L_untergrup.zwkum == l_artikel.zwkum)).filter(
                    (L_besthis.anf_best_dat >= anf_date) &  (L_besthis.anf_best_dat <= end_date) &  (L_besthis.lager_nr == 0)).all():
                if l_besthis._recid in l_besthis_obj_list:
                    continue
                else:
                    l_besthis_obj_list.append(l_besthis._recid)

                if (from_grp == 0 and sub_grp == 0) or (l_artikel.endkum == from_grp and sub_grp == 0) or (l_artikel.endkum == from_grp and l_artikel.zwkum == sub_grp) or (from_grp == 0 and l_artikel.zwkum == sub_grp):

                    if zwkum == 0:
                        zwkum = l_artikel.zwkum
                        bezeich = l_untergrup.bezeich

                    if zwkum != l_artikel.zwkum:

                        if t_val != 0:
                            out_list = Out_list()
                            out_list_list.append(out_list)

                            out_list.flag = 1
                            out_list.bezeich = bezeich
                            out_list.val = t_val


                            out_list = Out_list()
                            out_list_list.append(out_list)

                        t_anz = 0
                        t_val = 0
                        zwkum = l_untergrup.zwkum
                        bezeich = l_untergrup.bezeich

                    if show_price:
                        tot_val = l_besthis.val_anf_best + l_besthis.wert_eingang - l_besthis.wert_ausgang
                    tot_anz = l_besthis.anz_anf_best + l_besthis.anz_eingang - l_besthis.anz_ausgang

                    if tot_anz != 0:
                        vk_preis = tot_val / tot_anz
                    else:
                        vk_preis = 0
                    t_anz = t_anz + tot_anz

                    if show_price:
                        t_val = t_val + tot_val
                        t_value = t_value + tot_val
                        tt_val = tt_val + tot_val
                        tt_value = tt_value + tot_val

                    if tot_anz != 0 or (tot_anz == 0 and zero_flag):
                        out_list = Out_list()
                        out_list_list.append(out_list)

                        out_list.flag = 2

                        if show_price:
                            out_list.artnr = l_artikel.artnr
                            out_list.bezeich = l_artikel.bezeich
                            out_list.unit = l_artikel.masseinheit
                            out_list.content = l_artikel.inhalt
                            out_list.d_unit = l_artikel.traubensort
                            out_list.d_content = l_artikel.lief_einheit
                            out_list.last_price = l_artikel.ek_letzter
                            out_list.act_price = l_artikel.ek_aktuell
                            out_list.avrg_price = vk_preis
                            out_list.qty = tot_anz
                            out_list.val = tot_val


                        else:
                            out_list.artnr = l_artikel.artnr
                            out_list.bezeich = l_artikel.bezeich
                            out_list.unit = l_artikel.masseinheit
                            out_list.content = l_artikel.inhalt
                            out_list.d_unit = l_artikel.traubensort
                            out_list.d_content = l_artikel.lief_einheit
                            out_list.last_price = 0
                            out_list.act_price = 0
                            out_list.avrg_price = 0
                            out_list.qty = tot_anz
                            out_list.val = 0

        elif sorttype == 2:

            l_besthis_obj_list = []
            for l_besthis, l_artikel, l_untergrup in db_session.query(L_besthis, L_artikel, L_untergrup).join(L_artikel,(L_artikel.artnr == L_besthis.artnr)).join(L_untergrup,(L_untergrup.zwkum == l_artikel.zwkum)).filter(
                    (L_besthis.anf_best_dat >= anf_date) &  (L_besthis.anf_best_dat <= end_date) &  (L_besthis.lager_nr == 0)).all():
                if l_besthis._recid in l_besthis_obj_list:
                    continue
                else:
                    l_besthis_obj_list.append(l_besthis._recid)

                if (from_grp == 0 and sub_grp == 0) or (l_artikel.endkum == from_grp and sub_grp == 0) or (l_artikel.endkum == from_grp and l_artikel.zwkum == sub_grp) or (from_grp == 0 and l_artikel.zwkum == sub_grp):

                    if zwkum == 0:
                        zwkum = l_artikel.zwkum
                        bezeich = l_untergrup.bezeich

                    if zwkum != l_artikel.zwkum:

                        if t_val != 0:
                            out_list = Out_list()
                            out_list_list.append(out_list)

                            out_list.flag = 1
                            out_list.bezeich = bezeich
                            out_list.val = t_val


                            out_list = Out_list()
                            out_list_list.append(out_list)

                        t_anz = 0
                        t_val = 0
                        zwkum = l_untergrup.zwkum
                        bezeich = l_untergrup.bezeich

                    if show_price:
                        tot_val = l_besthis.val_anf_best + l_besthis.wert_eingang - l_besthis.wert_ausgang
                    tot_anz = l_besthis.anz_anf_best + l_besthis.anz_eingang - l_besthis.anz_ausgang

                    if tot_anz != 0:
                        vk_preis = tot_val / tot_anz
                    else:
                        vk_preis = 0
                    t_anz = t_anz + tot_anz

                    if show_price:
                        t_val = t_val + tot_val
                        t_value = t_value + tot_val
                        tt_val = tt_val + tot_val
                        tt_value = tt_value + tot_val

                    if tot_anz != 0 or (tot_anz == 0 and zero_flag):
                        out_list = Out_list()
                        out_list_list.append(out_list)

                        out_list.flag = 2

                        if show_price:
                            out_list.artnr = l_artikel.artnr
                            out_list.bezeich = l_artikel.bezeich
                            out_list.unit = l_artikel.masseinheit
                            out_list.content = l_artikel.inhalt
                            out_list.d_unit = l_artikel.traubensort
                            out_list.d_content = l_artikel.lief_einheit
                            out_list.last_price = l_artikel.ek_letzter
                            out_list.act_price = l_artikel.ek_aktuell
                            out_list.avrg_price = vk_preis
                            out_list.qty = tot_anz
                            out_list.val = tot_val


                        else:
                            out_list.artnr = l_artikel.artnr
                            out_list.bezeich = l_artikel.bezeich
                            out_list.unit = l_artikel.masseinheit
                            out_list.content = l_artikel.inhalt
                            out_list.d_unit = l_artikel.traubensort
                            out_list.d_content = l_artikel.lief_einheit
                            out_list.last_price = 0
                            out_list.act_price = 0
                            out_list.avrg_price = 0
                            out_list.qty = tot_anz
                            out_list.val = 0

        if t_val != 0:
            out_list = Out_list()
            out_list_list.append(out_list)

            out_list.flag = 1
            out_list.bezeich = bezeich
            out_list.val = t_val


            out_list = Out_list()
            out_list_list.append(out_list)

        out_list = Out_list()
        out_list_list.append(out_list)

        out_list.flag = 1
        out_list.bezeich = "GRAND T O T A L"
        out_list.val = tt_value

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 246)).first()
    long_digit = htparam.flogical

    l_besthis = db_session.query(L_besthis).filter(
            (L_besthis.anf_best_dat >= anf_date) &  (L_besthis.anf_best_dat <= end_date)).first()

    if not l_besthis:
        done = False

    if not done:

        return generate_output()

    if not all_flag:
        create_list()
    else:
        create_lista()

    return generate_output()