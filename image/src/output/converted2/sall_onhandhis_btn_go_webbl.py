#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, L_besthis, L_lager, L_artikel, L_untergrup

def sall_onhandhis_btn_go_webbl(anf_date:date, end_date:date, all_flag:bool, show_price:bool, zero_flag:bool, from_grp:int, sub_grp:int, from_lager:int, to_lager:int, sorttype:int, mattype:int):

    prepare_cache ([Htparam, L_besthis, L_lager, L_artikel, L_untergrup])

    done = True
    out_list_list = []
    long_digit:bool = False
    vk_preis:Decimal = to_decimal("0.0")
    htparam = l_besthis = l_lager = l_artikel = l_untergrup = None

    out_list = None

    out_list_list, Out_list = create_model("Out_list", {"artnr":int, "bezeich":string, "unit":string, "qty":Decimal, "val":Decimal, "content":Decimal, "d_unit":string, "d_content":Decimal, "last_price":Decimal, "act_price":Decimal, "avrg_price":Decimal, "flag":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal done, out_list_list, long_digit, vk_preis, htparam, l_besthis, l_lager, l_artikel, l_untergrup
        nonlocal anf_date, end_date, all_flag, show_price, zero_flag, from_grp, sub_grp, from_lager, to_lager, sorttype, mattype


        nonlocal out_list
        nonlocal out_list_list

        return {"done": done, "out-list": out_list_list}

    def create_list():

        nonlocal done, out_list_list, long_digit, vk_preis, htparam, l_besthis, l_lager, l_artikel, l_untergrup
        nonlocal anf_date, end_date, all_flag, show_price, zero_flag, from_grp, sub_grp, from_lager, to_lager, sorttype, mattype


        nonlocal out_list
        nonlocal out_list_list

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
        qty:Decimal = to_decimal("0.0")
        wert:Decimal = to_decimal("0.0")
        tot_bezeich:string = ""
        tt_val:Decimal = to_decimal("0.0")
        tt_value:Decimal = to_decimal("0.0")
        l_oh = None
        s_bezeich:string = ""
        L_oh =  create_buffer("L_oh",L_besthis)

        for l_lager in db_session.query(L_lager).filter(
                 (L_lager.lager_nr >= from_lager) & (L_lager.lager_nr <= to_lager)).order_by(L_lager._recid).all():
            tot_bezeich = "Ttl - " + l_lager.bezeich
            out_list = Out_list()
            out_list_list.append(out_list)

            s_bezeich = to_string(l_lager.lager_nr, "99") + " " + to_string(l_lager.bezeich, "x(13)")
            out_list.bezeich = to_string(l_lager.lager_nr, "99") + " " + to_string(l_lager.bezeich, "x(13)")
            i = 0
            zwkum = 0
            t_anz =  to_decimal("0")
            t_val =  to_decimal("0")
            tt_val =  to_decimal("0")

            if sorttype == 1:

                l_besthis_obj_list = {}
                l_besthis = L_besthis()
                l_artikel = L_artikel()
                l_oh = L_besthis()
                l_untergrup = L_untergrup()
                for l_besthis.anz_anf_best, l_besthis.anz_eingang, l_besthis.anz_ausgang, l_besthis.val_anf_best, l_besthis.wert_eingang, l_besthis.wert_ausgang, l_besthis._recid, l_artikel.endkum, l_artikel.zwkum, l_artikel.artnr, l_artikel.bezeich, l_artikel.masseinheit, l_artikel.inhalt, l_artikel.traubensorte, l_artikel.lief_einheit, l_artikel.ek_letzter, l_artikel.ek_aktuell, l_artikel._recid, l_oh.anz_anf_best, l_oh.anz_eingang, l_oh.anz_ausgang, l_oh.val_anf_best, l_oh.wert_eingang, l_oh.wert_ausgang, l_oh._recid, l_untergrup.bezeich, l_untergrup.zwkum, l_untergrup._recid in db_session.query(L_besthis.anz_anf_best, L_besthis.anz_eingang, L_besthis.anz_ausgang, L_besthis.val_anf_best, L_besthis.wert_eingang, L_besthis.wert_ausgang, L_besthis._recid, L_artikel.endkum, L_artikel.zwkum, L_artikel.artnr, L_artikel.bezeich, L_artikel.masseinheit, L_artikel.inhalt, L_artikel.traubensorte, L_artikel.lief_einheit, L_artikel.ek_letzter, L_artikel.ek_aktuell, L_artikel._recid, L_oh.anz_anf_best, L_oh.anz_eingang, L_oh.anz_ausgang, L_oh.val_anf_best, L_oh.wert_eingang, L_oh.wert_ausgang, L_oh._recid, L_untergrup.bezeich, L_untergrup.zwkum, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_besthis.artnr)).join(L_oh,(L_oh.anf_best_dat >= anf_date) & (L_oh.anf_best_dat <= end_date) & (L_oh.lager_nr == 0) & (L_oh.artnr == L_besthis.artnr)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                         (L_besthis.anf_best_dat >= anf_date) & (L_besthis.anf_best_dat <= end_date) & (L_besthis.lager_nr == l_lager.lager_nr)).order_by(L_artikel.zwkum, L_artikel.artnr).all():
                    if l_besthis_obj_list.get(l_besthis._recid):
                        continue
                    else:
                        l_besthis_obj_list[l_besthis._recid] = True

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
                                out_list.val =  to_decimal(t_val)


                                out_list = Out_list()
                                out_list_list.append(out_list)

                            out_list.flag = 0
                            t_anz =  to_decimal("0")
                            t_val =  to_decimal("0")
                            zwkum = l_untergrup.zwkum
                            bezeich = l_untergrup.bezeich


                        qty =  to_decimal(l_oh.anz_anf_best) + to_decimal(l_oh.anz_eingang) - to_decimal(l_oh.anz_ausgang)

                        if show_price:
                            wert =  to_decimal(l_oh.val_anf_best) + to_decimal(l_oh.wert_eingang) - to_decimal(l_oh.wert_ausgang)
                        tot_anz =  to_decimal(l_besthis.anz_anf_best) + to_decimal(l_besthis.anz_eingang) - to_decimal(l_besthis.anz_ausgang)

                        if qty != 0:
                            tot_val =  to_decimal(wert) * to_decimal(tot_anz) / to_decimal(qty)
                        else:
                            tot_val =  to_decimal("0")

                        if tot_anz != 0:
                            vk_preis =  to_decimal(tot_val) / to_decimal(tot_anz)
                        else:
                            vk_preis =  to_decimal("0")
                        t_anz =  to_decimal(t_anz) + to_decimal(tot_anz)

                        if show_price:
                            t_val =  to_decimal(t_val) + to_decimal(tot_val)


                            t_value =  to_decimal(t_value) + to_decimal(tot_val)
                            tt_val =  to_decimal(tt_val) + to_decimal(tot_val)
                            tt_value =  to_decimal(tt_value) + to_decimal(tot_val)

                        if tot_anz != 0 or (tot_anz == 0 and zero_flag):
                            out_list = Out_list()
                            out_list_list.append(out_list)

                            out_list.flag = 2

                            if show_price:
                                out_list.artnr = l_artikel.artnr
                                out_list.bezeich = l_artikel.bezeich
                                out_list.unit = l_artikel.masseinheit
                                out_list.content =  to_decimal(l_artikel.inhalt)
                                out_list.d_unit = l_artikel.traubensorte
                                out_list.d_content =  to_decimal(l_artikel.lief_einheit)
                                out_list.last_price =  to_decimal(l_artikel.ek_letzter)
                                out_list.act_price =  to_decimal(l_artikel.ek_aktuell)
                                out_list.avrg_price =  to_decimal(vk_preis)
                                out_list.qty =  to_decimal(tot_anz)
                                out_list.val =  to_decimal(tot_val)


                            else:
                                out_list.artnr = l_artikel.artnr
                                out_list.bezeich = l_artikel.bezeich
                                out_list.unit = l_artikel.masseinheit
                                out_list.content =  to_decimal(l_artikel.inhalt)
                                out_list.d_unit = l_artikel.traubensorte
                                out_list.d_content =  to_decimal(l_artikel.lief_einheit)
                                out_list.last_price =  to_decimal("0")
                                out_list.act_price =  to_decimal("0")
                                out_list.avrg_price =  to_decimal("0")
                                out_list.qty =  to_decimal(tot_anz)
                                out_list.val =  to_decimal("0")

            elif sorttype == 2:

                l_besthis_obj_list = {}
                l_besthis = L_besthis()
                l_artikel = L_artikel()
                l_oh = L_besthis()
                l_untergrup = L_untergrup()
                for l_besthis.anz_anf_best, l_besthis.anz_eingang, l_besthis.anz_ausgang, l_besthis.val_anf_best, l_besthis.wert_eingang, l_besthis.wert_ausgang, l_besthis._recid, l_artikel.endkum, l_artikel.zwkum, l_artikel.artnr, l_artikel.bezeich, l_artikel.masseinheit, l_artikel.inhalt, l_artikel.traubensorte, l_artikel.lief_einheit, l_artikel.ek_letzter, l_artikel.ek_aktuell, l_artikel._recid, l_oh.anz_anf_best, l_oh.anz_eingang, l_oh.anz_ausgang, l_oh.val_anf_best, l_oh.wert_eingang, l_oh.wert_ausgang, l_oh._recid, l_untergrup.bezeich, l_untergrup.zwkum, l_untergrup._recid in db_session.query(L_besthis.anz_anf_best, L_besthis.anz_eingang, L_besthis.anz_ausgang, L_besthis.val_anf_best, L_besthis.wert_eingang, L_besthis.wert_ausgang, L_besthis._recid, L_artikel.endkum, L_artikel.zwkum, L_artikel.artnr, L_artikel.bezeich, L_artikel.masseinheit, L_artikel.inhalt, L_artikel.traubensorte, L_artikel.lief_einheit, L_artikel.ek_letzter, L_artikel.ek_aktuell, L_artikel._recid, L_oh.anz_anf_best, L_oh.anz_eingang, L_oh.anz_ausgang, L_oh.val_anf_best, L_oh.wert_eingang, L_oh.wert_ausgang, L_oh._recid, L_untergrup.bezeich, L_untergrup.zwkum, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_besthis.artnr)).join(L_oh,(L_oh.anf_best_dat >= anf_date) & (L_oh.anf_best_dat <= end_date) & (L_oh.lager_nr == 0) & (L_oh.artnr == L_besthis.artnr)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                         (L_besthis.anf_best_dat >= anf_date) & (L_besthis.anf_best_dat <= end_date) & (L_besthis.lager_nr == l_lager.lager_nr)).order_by(L_artikel.zwkum, L_artikel.bezeich).all():
                    if l_besthis_obj_list.get(l_besthis._recid):
                        continue
                    else:
                        l_besthis_obj_list[l_besthis._recid] = True

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
                                out_list.val =  to_decimal(t_val)


                                out_list = Out_list()
                                out_list_list.append(out_list)

                            t_anz =  to_decimal("0")
                            t_val =  to_decimal("0")
                            zwkum = l_untergrup.zwkum
                            bezeich = l_untergrup.bezeich


                        qty =  to_decimal(l_oh.anz_anf_best) + to_decimal(l_oh.anz_eingang) - to_decimal(l_oh.anz_ausgang)

                        if show_price:
                            wert =  to_decimal(l_oh.val_anf_best) + to_decimal(l_oh.wert_eingang) - to_decimal(l_oh.wert_ausgang)
                        tot_anz =  to_decimal(l_besthis.anz_anf_best) + to_decimal(l_besthis.anz_eingang) - to_decimal(l_besthis.anz_ausgang)

                        if qty != 0:
                            tot_val =  to_decimal(wert) * to_decimal(tot_anz) / to_decimal(qty)
                        else:
                            tot_val =  to_decimal("0")

                        if tot_anz != 0:
                            vk_preis =  to_decimal(tot_val) / to_decimal(tot_anz)
                        else:
                            vk_preis =  to_decimal("0")
                        t_anz =  to_decimal(t_anz) + to_decimal(tot_anz)

                        if show_price:
                            t_val =  to_decimal(t_val) + to_decimal(tot_val)


                            t_value =  to_decimal(t_value) + to_decimal(tot_val)
                            tt_val =  to_decimal(tt_val) + to_decimal(tot_val)
                            tt_value =  to_decimal(tt_value) + to_decimal(tot_val)

                        if tot_anz != 0 or (tot_anz == 0 and zero_flag):
                            out_list = Out_list()
                            out_list_list.append(out_list)

                            out_list.flag = 2

                            if show_price:
                                out_list.artnr = l_artikel.artnr
                                out_list.bezeich = l_artikel.bezeich
                                out_list.unit = l_artikel.masseinheit
                                out_list.content =  to_decimal(l_artikel.inhalt)
                                out_list.d_unit = l_artikel.traubensorte
                                out_list.d_content =  to_decimal(l_artikel.lief_einheit)
                                out_list.last_price =  to_decimal(l_artikel.ek_letzter)
                                out_list.act_price =  to_decimal(l_artikel.ek_aktuell)
                                out_list.avrg_price =  to_decimal(vk_preis)
                                out_list.qty =  to_decimal(tot_anz)
                                out_list.val =  to_decimal(tot_val)


                            else:
                                out_list.artnr = l_artikel.artnr
                                out_list.bezeich = l_artikel.bezeich
                                out_list.unit = l_artikel.masseinheit
                                out_list.content =  to_decimal(l_artikel.inhalt)
                                out_list.d_unit = l_artikel.traubensorte
                                out_list.d_content =  to_decimal(l_artikel.lief_einheit)
                                out_list.last_price =  to_decimal("0")
                                out_list.act_price =  to_decimal("0")
                                out_list.avrg_price =  to_decimal("0")
                                out_list.qty =  to_decimal(tot_anz)
                                out_list.val =  to_decimal("0")

            if t_val != 0:
                out_list = Out_list()
                out_list_list.append(out_list)

                out_list.flag = 1
                out_list.bezeich = bezeich
                out_list.val =  to_decimal(t_val)


                out_list = Out_list()
                out_list_list.append(out_list)


            if tt_val == 0:

                out_list = query(out_list_list, filters=(lambda out_list: out_list.bezeich.lower()  == (s_bezeich).lower()), first=True)
                out_list_list.remove(out_list)
            else:
                out_list = Out_list()
                out_list_list.append(out_list)

                out_list.flag = 1
                out_list.bezeich = tot_bezeich
                out_list.val =  to_decimal(tt_val)

        if tt_value != 0:
            out_list = Out_list()
            out_list_list.append(out_list)

            out_list.flag = 1
            out_list.bezeich = "GRAND T O T A L"
            out_list.val =  to_decimal(tt_value)


    def create_lista():

        nonlocal done, out_list_list, long_digit, vk_preis, htparam, l_besthis, l_lager, l_artikel, l_untergrup
        nonlocal anf_date, end_date, all_flag, show_price, zero_flag, from_grp, sub_grp, from_lager, to_lager, sorttype, mattype


        nonlocal out_list
        nonlocal out_list_list

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
        l_oh = None
        qty:Decimal = to_decimal("0.0")
        wert:Decimal = to_decimal("0.0")
        tot_bezeich:string = ""
        tt_val:Decimal = to_decimal("0.0")
        tt_value:Decimal = to_decimal("0.0")
        L_oh =  create_buffer("L_oh",L_besthis)
        i = 0
        zwkum = 0
        t_anz =  to_decimal("0")
        t_val =  to_decimal("0")
        tt_val =  to_decimal("0")

        if sorttype == 1:

            l_besthis_obj_list = {}
            l_besthis = L_besthis()
            l_artikel = L_artikel()
            l_untergrup = L_untergrup()
            for l_besthis.anz_anf_best, l_besthis.anz_eingang, l_besthis.anz_ausgang, l_besthis.val_anf_best, l_besthis.wert_eingang, l_besthis.wert_ausgang, l_besthis._recid, l_artikel.endkum, l_artikel.zwkum, l_artikel.artnr, l_artikel.bezeich, l_artikel.masseinheit, l_artikel.inhalt, l_artikel.traubensorte, l_artikel.lief_einheit, l_artikel.ek_letzter, l_artikel.ek_aktuell, l_artikel._recid, l_untergrup.bezeich, l_untergrup.zwkum, l_untergrup._recid in db_session.query(L_besthis.anz_anf_best, L_besthis.anz_eingang, L_besthis.anz_ausgang, L_besthis.val_anf_best, L_besthis.wert_eingang, L_besthis.wert_ausgang, L_besthis._recid, L_artikel.endkum, L_artikel.zwkum, L_artikel.artnr, L_artikel.bezeich, L_artikel.masseinheit, L_artikel.inhalt, L_artikel.traubensorte, L_artikel.lief_einheit, L_artikel.ek_letzter, L_artikel.ek_aktuell, L_artikel._recid, L_untergrup.bezeich, L_untergrup.zwkum, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_besthis.artnr)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                     (L_besthis.anf_best_dat >= anf_date) & (L_besthis.anf_best_dat <= end_date) & (L_besthis.lager_nr == 0)).order_by(L_artikel.zwkum, L_artikel.artnr).all():
                if l_besthis_obj_list.get(l_besthis._recid):
                    continue
                else:
                    l_besthis_obj_list[l_besthis._recid] = True

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
                            out_list.val =  to_decimal(t_val)


                            out_list = Out_list()
                            out_list_list.append(out_list)

                        t_anz =  to_decimal("0")
                        t_val =  to_decimal("0")
                        zwkum = l_untergrup.zwkum
                        bezeich = l_untergrup.bezeich

                    if show_price:
                        tot_val =  to_decimal(l_besthis.val_anf_best) + to_decimal(l_besthis.wert_eingang) - to_decimal(l_besthis.wert_ausgang)
                    tot_anz =  to_decimal(l_besthis.anz_anf_best) + to_decimal(l_besthis.anz_eingang) - to_decimal(l_besthis.anz_ausgang)

                    if tot_anz != 0:
                        vk_preis =  to_decimal(tot_val) / to_decimal(tot_anz)
                    else:
                        vk_preis =  to_decimal("0")
                    t_anz =  to_decimal(t_anz) + to_decimal(tot_anz)

                    if show_price:
                        t_val =  to_decimal(t_val) + to_decimal(tot_val)
                        t_value =  to_decimal(t_value) + to_decimal(tot_val)
                        tt_val =  to_decimal(tt_val) + to_decimal(tot_val)
                        tt_value =  to_decimal(tt_value) + to_decimal(tot_val)

                    if tot_anz != 0 or (tot_anz == 0 and zero_flag):
                        out_list = Out_list()
                        out_list_list.append(out_list)

                        out_list.flag = 2

                        if show_price:
                            out_list.artnr = l_artikel.artnr
                            out_list.bezeich = l_artikel.bezeich
                            out_list.unit = l_artikel.masseinheit
                            out_list.content =  to_decimal(l_artikel.inhalt)
                            out_list.d_unit = l_artikel.traubensorte
                            out_list.d_content =  to_decimal(l_artikel.lief_einheit)
                            out_list.last_price =  to_decimal(l_artikel.ek_letzter)
                            out_list.act_price =  to_decimal(l_artikel.ek_aktuell)
                            out_list.avrg_price =  to_decimal(vk_preis)
                            out_list.qty =  to_decimal(tot_anz)
                            out_list.val =  to_decimal(tot_val)


                        else:
                            out_list.artnr = l_artikel.artnr
                            out_list.bezeich = l_artikel.bezeich
                            out_list.unit = l_artikel.masseinheit
                            out_list.content =  to_decimal(l_artikel.inhalt)
                            out_list.d_unit = l_artikel.traubensorte
                            out_list.d_content =  to_decimal(l_artikel.lief_einheit)
                            out_list.last_price =  to_decimal("0")
                            out_list.act_price =  to_decimal("0")
                            out_list.avrg_price =  to_decimal("0")
                            out_list.qty =  to_decimal(tot_anz)
                            out_list.val =  to_decimal("0")

        elif sorttype == 2:

            l_besthis_obj_list = {}
            l_besthis = L_besthis()
            l_artikel = L_artikel()
            l_untergrup = L_untergrup()
            for l_besthis.anz_anf_best, l_besthis.anz_eingang, l_besthis.anz_ausgang, l_besthis.val_anf_best, l_besthis.wert_eingang, l_besthis.wert_ausgang, l_besthis._recid, l_artikel.endkum, l_artikel.zwkum, l_artikel.artnr, l_artikel.bezeich, l_artikel.masseinheit, l_artikel.inhalt, l_artikel.traubensorte, l_artikel.lief_einheit, l_artikel.ek_letzter, l_artikel.ek_aktuell, l_artikel._recid, l_untergrup.bezeich, l_untergrup.zwkum, l_untergrup._recid in db_session.query(L_besthis.anz_anf_best, L_besthis.anz_eingang, L_besthis.anz_ausgang, L_besthis.val_anf_best, L_besthis.wert_eingang, L_besthis.wert_ausgang, L_besthis._recid, L_artikel.endkum, L_artikel.zwkum, L_artikel.artnr, L_artikel.bezeich, L_artikel.masseinheit, L_artikel.inhalt, L_artikel.traubensorte, L_artikel.lief_einheit, L_artikel.ek_letzter, L_artikel.ek_aktuell, L_artikel._recid, L_untergrup.bezeich, L_untergrup.zwkum, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_besthis.artnr)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                     (L_besthis.anf_best_dat >= anf_date) & (L_besthis.anf_best_dat <= end_date) & (L_besthis.lager_nr == 0)).order_by(L_artikel.zwkum, L_artikel.bezeich).all():
                if l_besthis_obj_list.get(l_besthis._recid):
                    continue
                else:
                    l_besthis_obj_list[l_besthis._recid] = True

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
                            out_list.val =  to_decimal(t_val)


                            out_list = Out_list()
                            out_list_list.append(out_list)

                        t_anz =  to_decimal("0")
                        t_val =  to_decimal("0")
                        zwkum = l_untergrup.zwkum
                        bezeich = l_untergrup.bezeich

                    if show_price:
                        tot_val =  to_decimal(l_besthis.val_anf_best) + to_decimal(l_besthis.wert_eingang) - to_decimal(l_besthis.wert_ausgang)
                    tot_anz =  to_decimal(l_besthis.anz_anf_best) + to_decimal(l_besthis.anz_eingang) - to_decimal(l_besthis.anz_ausgang)

                    if tot_anz != 0:
                        vk_preis =  to_decimal(tot_val) / to_decimal(tot_anz)
                    else:
                        vk_preis =  to_decimal("0")
                    t_anz =  to_decimal(t_anz) + to_decimal(tot_anz)

                    if show_price:
                        t_val =  to_decimal(t_val) + to_decimal(tot_val)
                        t_value =  to_decimal(t_value) + to_decimal(tot_val)
                        tt_val =  to_decimal(tt_val) + to_decimal(tot_val)
                        tt_value =  to_decimal(tt_value) + to_decimal(tot_val)

                    if tot_anz != 0 or (tot_anz == 0 and zero_flag):
                        out_list = Out_list()
                        out_list_list.append(out_list)

                        out_list.flag = 2

                        if show_price:
                            out_list.artnr = l_artikel.artnr
                            out_list.bezeich = l_artikel.bezeich
                            out_list.unit = l_artikel.masseinheit
                            out_list.content =  to_decimal(l_artikel.inhalt)
                            out_list.d_unit = l_artikel.traubensorte
                            out_list.d_content =  to_decimal(l_artikel.lief_einheit)
                            out_list.last_price =  to_decimal(l_artikel.ek_letzter)
                            out_list.act_price =  to_decimal(l_artikel.ek_aktuell)
                            out_list.avrg_price =  to_decimal(vk_preis)
                            out_list.qty =  to_decimal(tot_anz)
                            out_list.val =  to_decimal(tot_val)


                        else:
                            out_list.artnr = l_artikel.artnr
                            out_list.bezeich = l_artikel.bezeich
                            out_list.unit = l_artikel.masseinheit
                            out_list.content =  to_decimal(l_artikel.inhalt)
                            out_list.d_unit = l_artikel.traubensorte
                            out_list.d_content =  to_decimal(l_artikel.lief_einheit)
                            out_list.last_price =  to_decimal("0")
                            out_list.act_price =  to_decimal("0")
                            out_list.avrg_price =  to_decimal("0")
                            out_list.qty =  to_decimal(tot_anz)
                            out_list.val =  to_decimal("0")

        if t_val != 0:
            out_list = Out_list()
            out_list_list.append(out_list)

            out_list.flag = 1
            out_list.bezeich = bezeich
            out_list.val =  to_decimal(t_val)


            out_list = Out_list()
            out_list_list.append(out_list)

        out_list = Out_list()
        out_list_list.append(out_list)

        out_list.flag = 1
        out_list.bezeich = "GRAND T O T A L"
        out_list.val =  to_decimal(tt_value)


    htparam = get_cache (Htparam, {"paramnr": [(eq, 246)]})
    long_digit = htparam.flogical

    l_besthis = get_cache (L_besthis, {"anf_best_dat": [(ge, anf_date),(le, end_date)]})

    if not l_besthis:
        done = False

    if not done:

        return generate_output()

    if not all_flag:
        create_list()
    else:
        create_lista()

    return generate_output()