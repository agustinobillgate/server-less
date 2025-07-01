#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import L_bestand, Htparam, L_lager, L_artikel, L_untergrup

def sall_onhand_btn_go1_webbl(all_flag:bool, show_price:bool, zero_flag:bool, from_grp:int, sub_grp:int, from_lager:int, to_lager:int, sorttype:int, mattype:int, minoh_flag:bool):

    prepare_cache ([L_bestand, Htparam, L_lager, L_artikel, L_untergrup])

    soh_list_list = []
    curr_best:Decimal = to_decimal("0.0")
    long_digit:bool = False
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
    tot_bezeich:string = ""
    l_bestand = htparam = l_lager = l_artikel = l_untergrup = None

    str_list = soh_list = output_list = l_oh = None

    str_list_list, Str_list = create_model("Str_list", {"flag":int, "s":string})
    soh_list_list, Soh_list = create_model("Soh_list", {"artnr":int, "bezeich":string, "unit":string, "act_qty":Decimal, "act_val":Decimal, "cont1":string, "d_unit":string, "cont2":string, "last_price":Decimal, "act_price":Decimal, "avrg_price":Decimal, "min_oh":Decimal, "must_order":Decimal})
    output_list_list, Output_list = create_model("Output_list", {"flag":int, "artnr":int, "bezeich":string, "unit":string, "act_qty":Decimal, "act_val":Decimal, "cont1":string, "d_unit":string, "cont2":string, "last_price":Decimal, "act_price":Decimal, "avrg_price":Decimal, "min_oh":Decimal, "must_order":Decimal})

    L_oh = create_buffer("L_oh",L_bestand)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal soh_list_list, curr_best, long_digit, i, j, tot_anz, tot_val, t_anz, t_val, t_value, tt_value, avrg_price, zwkum, bezeich, grp1, grp2, must_order, tt_val, qty, wert, tot_bezeich, l_bestand, htparam, l_lager, l_artikel, l_untergrup
        nonlocal all_flag, show_price, zero_flag, from_grp, sub_grp, from_lager, to_lager, sorttype, mattype, minoh_flag
        nonlocal l_oh


        nonlocal str_list, soh_list, output_list, l_oh
        nonlocal str_list_list, soh_list_list, output_list_list

        return {"soh-list": soh_list_list}

    def create_list():

        nonlocal soh_list_list, curr_best, long_digit, i, j, tot_anz, tot_val, t_anz, t_val, t_value, tt_value, avrg_price, zwkum, bezeich, grp1, grp2, must_order, tt_val, qty, wert, tot_bezeich, l_bestand, htparam, l_lager, l_artikel, l_untergrup
        nonlocal all_flag, show_price, zero_flag, from_grp, sub_grp, from_lager, to_lager, sorttype, mattype, minoh_flag
        nonlocal l_oh


        nonlocal str_list, soh_list, output_list, l_oh
        nonlocal str_list_list, soh_list_list, output_list_list


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

                    if minoh_flag:

                        l_bestand_obj_list = {}
                        l_bestand = L_bestand()
                        l_artikel = L_artikel()
                        l_oh = L_bestand()
                        l_untergrup = L_untergrup()
                        for l_bestand.anz_anf_best, l_bestand.anz_eingang, l_bestand.anz_ausgang, l_bestand.val_anf_best, l_bestand.wert_eingang, l_bestand.wert_ausgang, l_bestand._recid, l_artikel.zwkum, l_artikel.anzverbrauch, l_artikel.bezeich, l_artikel.artnr, l_artikel.masseinheit, l_artikel.inhalt, l_artikel.traubensorte, l_artikel.lief_einheit, l_artikel.ek_letzter, l_artikel.ek_aktuell, l_artikel.vk_preis, l_artikel.min_bestand, l_artikel._recid, l_oh.anz_anf_best, l_oh.anz_eingang, l_oh.anz_ausgang, l_oh.val_anf_best, l_oh.wert_eingang, l_oh.wert_ausgang, l_oh._recid, l_untergrup.bezeich, l_untergrup.zwkum, l_untergrup._recid in db_session.query(L_bestand.anz_anf_best, L_bestand.anz_eingang, L_bestand.anz_ausgang, L_bestand.val_anf_best, L_bestand.wert_eingang, L_bestand.wert_ausgang, L_bestand._recid, L_artikel.zwkum, L_artikel.anzverbrauch, L_artikel.bezeich, L_artikel.artnr, L_artikel.masseinheit, L_artikel.inhalt, L_artikel.traubensorte, L_artikel.lief_einheit, L_artikel.ek_letzter, L_artikel.ek_aktuell, L_artikel.vk_preis, L_artikel.min_bestand, L_artikel._recid, L_oh.anz_anf_best, L_oh.anz_eingang, L_oh.anz_ausgang, L_oh.val_anf_best, L_oh.wert_eingang, L_oh.wert_ausgang, L_oh._recid, L_untergrup.bezeich, L_untergrup.zwkum, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_bestand.artnr) & (L_artikel.zwkum == sub_grp) & (L_artikel.min_bestand > 0)).join(L_oh,(L_oh.artnr == L_bestand.artnr) & (L_oh.lager_nr == 0)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                                 (L_bestand.lager_nr == l_lager.lager_nr)).order_by(L_artikel.zwkum, L_artikel.artnr).all():
                            if l_bestand_obj_list.get(l_bestand._recid):
                                continue
                            else:
                                l_bestand_obj_list[l_bestand._recid] = True


                            curr_best =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)

                            if curr_best < l_artikel.min_bestand:
                                create_lines()
                    else:

                        l_bestand_obj_list = {}
                        l_bestand = L_bestand()
                        l_artikel = L_artikel()
                        l_oh = L_bestand()
                        l_untergrup = L_untergrup()
                        for l_bestand.anz_anf_best, l_bestand.anz_eingang, l_bestand.anz_ausgang, l_bestand.val_anf_best, l_bestand.wert_eingang, l_bestand.wert_ausgang, l_bestand._recid, l_artikel.zwkum, l_artikel.anzverbrauch, l_artikel.bezeich, l_artikel.artnr, l_artikel.masseinheit, l_artikel.inhalt, l_artikel.traubensorte, l_artikel.lief_einheit, l_artikel.ek_letzter, l_artikel.ek_aktuell, l_artikel.vk_preis, l_artikel.min_bestand, l_artikel._recid, l_oh.anz_anf_best, l_oh.anz_eingang, l_oh.anz_ausgang, l_oh.val_anf_best, l_oh.wert_eingang, l_oh.wert_ausgang, l_oh._recid, l_untergrup.bezeich, l_untergrup.zwkum, l_untergrup._recid in db_session.query(L_bestand.anz_anf_best, L_bestand.anz_eingang, L_bestand.anz_ausgang, L_bestand.val_anf_best, L_bestand.wert_eingang, L_bestand.wert_ausgang, L_bestand._recid, L_artikel.zwkum, L_artikel.anzverbrauch, L_artikel.bezeich, L_artikel.artnr, L_artikel.masseinheit, L_artikel.inhalt, L_artikel.traubensorte, L_artikel.lief_einheit, L_artikel.ek_letzter, L_artikel.ek_aktuell, L_artikel.vk_preis, L_artikel.min_bestand, L_artikel._recid, L_oh.anz_anf_best, L_oh.anz_eingang, L_oh.anz_ausgang, L_oh.val_anf_best, L_oh.wert_eingang, L_oh.wert_ausgang, L_oh._recid, L_untergrup.bezeich, L_untergrup.zwkum, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_bestand.artnr) & (L_artikel.zwkum == sub_grp)).join(L_oh,(L_oh.artnr == L_bestand.artnr) & (L_oh.lager_nr == 0)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                                 (L_bestand.lager_nr == l_lager.lager_nr)).order_by(L_artikel.zwkum, L_artikel.artnr).all():
                            if l_bestand_obj_list.get(l_bestand._recid):
                                continue
                            else:
                                l_bestand_obj_list[l_bestand._recid] = True


                            create_lines()
                else:

                    if minoh_flag:

                        l_bestand_obj_list = {}
                        l_bestand = L_bestand()
                        l_artikel = L_artikel()
                        l_oh = L_bestand()
                        l_untergrup = L_untergrup()
                        for l_bestand.anz_anf_best, l_bestand.anz_eingang, l_bestand.anz_ausgang, l_bestand.val_anf_best, l_bestand.wert_eingang, l_bestand.wert_ausgang, l_bestand._recid, l_artikel.zwkum, l_artikel.anzverbrauch, l_artikel.bezeich, l_artikel.artnr, l_artikel.masseinheit, l_artikel.inhalt, l_artikel.traubensorte, l_artikel.lief_einheit, l_artikel.ek_letzter, l_artikel.ek_aktuell, l_artikel.vk_preis, l_artikel.min_bestand, l_artikel._recid, l_oh.anz_anf_best, l_oh.anz_eingang, l_oh.anz_ausgang, l_oh.val_anf_best, l_oh.wert_eingang, l_oh.wert_ausgang, l_oh._recid, l_untergrup.bezeich, l_untergrup.zwkum, l_untergrup._recid in db_session.query(L_bestand.anz_anf_best, L_bestand.anz_eingang, L_bestand.anz_ausgang, L_bestand.val_anf_best, L_bestand.wert_eingang, L_bestand.wert_ausgang, L_bestand._recid, L_artikel.zwkum, L_artikel.anzverbrauch, L_artikel.bezeich, L_artikel.artnr, L_artikel.masseinheit, L_artikel.inhalt, L_artikel.traubensorte, L_artikel.lief_einheit, L_artikel.ek_letzter, L_artikel.ek_aktuell, L_artikel.vk_preis, L_artikel.min_bestand, L_artikel._recid, L_oh.anz_anf_best, L_oh.anz_eingang, L_oh.anz_ausgang, L_oh.val_anf_best, L_oh.wert_eingang, L_oh.wert_ausgang, L_oh._recid, L_untergrup.bezeich, L_untergrup.zwkum, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_bestand.artnr) & (L_artikel.min_bestand > 0)).join(L_oh,(L_oh.artnr == L_bestand.artnr) & (L_oh.lager_nr == 0)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                                 (L_bestand.lager_nr == l_lager.lager_nr)).order_by(L_artikel.zwkum, L_artikel.artnr).all():
                            if l_bestand_obj_list.get(l_bestand._recid):
                                continue
                            else:
                                l_bestand_obj_list[l_bestand._recid] = True


                            curr_best =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)

                            if curr_best < l_artikel.min_bestand:
                                create_lines()
                    else:

                        l_bestand_obj_list = {}
                        l_bestand = L_bestand()
                        l_artikel = L_artikel()
                        l_oh = L_bestand()
                        l_untergrup = L_untergrup()
                        for l_bestand.anz_anf_best, l_bestand.anz_eingang, l_bestand.anz_ausgang, l_bestand.val_anf_best, l_bestand.wert_eingang, l_bestand.wert_ausgang, l_bestand._recid, l_artikel.zwkum, l_artikel.anzverbrauch, l_artikel.bezeich, l_artikel.artnr, l_artikel.masseinheit, l_artikel.inhalt, l_artikel.traubensorte, l_artikel.lief_einheit, l_artikel.ek_letzter, l_artikel.ek_aktuell, l_artikel.vk_preis, l_artikel.min_bestand, l_artikel._recid, l_oh.anz_anf_best, l_oh.anz_eingang, l_oh.anz_ausgang, l_oh.val_anf_best, l_oh.wert_eingang, l_oh.wert_ausgang, l_oh._recid, l_untergrup.bezeich, l_untergrup.zwkum, l_untergrup._recid in db_session.query(L_bestand.anz_anf_best, L_bestand.anz_eingang, L_bestand.anz_ausgang, L_bestand.val_anf_best, L_bestand.wert_eingang, L_bestand.wert_ausgang, L_bestand._recid, L_artikel.zwkum, L_artikel.anzverbrauch, L_artikel.bezeich, L_artikel.artnr, L_artikel.masseinheit, L_artikel.inhalt, L_artikel.traubensorte, L_artikel.lief_einheit, L_artikel.ek_letzter, L_artikel.ek_aktuell, L_artikel.vk_preis, L_artikel.min_bestand, L_artikel._recid, L_oh.anz_anf_best, L_oh.anz_eingang, L_oh.anz_ausgang, L_oh.val_anf_best, L_oh.wert_eingang, L_oh.wert_ausgang, L_oh._recid, L_untergrup.bezeich, L_untergrup.zwkum, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_bestand.artnr)).join(L_oh,(L_oh.artnr == L_bestand.artnr) & (L_oh.lager_nr == 0)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                                 (L_bestand.lager_nr == l_lager.lager_nr)).order_by(L_artikel.zwkum, L_artikel.artnr).all():
                            if l_bestand_obj_list.get(l_bestand._recid):
                                continue
                            else:
                                l_bestand_obj_list[l_bestand._recid] = True


                            create_lines()

            elif sorttype == 2:

                if sub_grp != 000:

                    if minoh_flag:

                        l_bestand_obj_list = {}
                        l_bestand = L_bestand()
                        l_artikel = L_artikel()
                        l_oh = L_bestand()
                        l_untergrup = L_untergrup()
                        for l_bestand.anz_anf_best, l_bestand.anz_eingang, l_bestand.anz_ausgang, l_bestand.val_anf_best, l_bestand.wert_eingang, l_bestand.wert_ausgang, l_bestand._recid, l_artikel.zwkum, l_artikel.anzverbrauch, l_artikel.bezeich, l_artikel.artnr, l_artikel.masseinheit, l_artikel.inhalt, l_artikel.traubensorte, l_artikel.lief_einheit, l_artikel.ek_letzter, l_artikel.ek_aktuell, l_artikel.vk_preis, l_artikel.min_bestand, l_artikel._recid, l_oh.anz_anf_best, l_oh.anz_eingang, l_oh.anz_ausgang, l_oh.val_anf_best, l_oh.wert_eingang, l_oh.wert_ausgang, l_oh._recid, l_untergrup.bezeich, l_untergrup.zwkum, l_untergrup._recid in db_session.query(L_bestand.anz_anf_best, L_bestand.anz_eingang, L_bestand.anz_ausgang, L_bestand.val_anf_best, L_bestand.wert_eingang, L_bestand.wert_ausgang, L_bestand._recid, L_artikel.zwkum, L_artikel.anzverbrauch, L_artikel.bezeich, L_artikel.artnr, L_artikel.masseinheit, L_artikel.inhalt, L_artikel.traubensorte, L_artikel.lief_einheit, L_artikel.ek_letzter, L_artikel.ek_aktuell, L_artikel.vk_preis, L_artikel.min_bestand, L_artikel._recid, L_oh.anz_anf_best, L_oh.anz_eingang, L_oh.anz_ausgang, L_oh.val_anf_best, L_oh.wert_eingang, L_oh.wert_ausgang, L_oh._recid, L_untergrup.bezeich, L_untergrup.zwkum, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_bestand.artnr) & (L_artikel.zwkum == sub_grp) & (L_artikel.min_bestand > 0)).join(L_oh,(L_oh.artnr == L_bestand.artnr) & (L_oh.lager_nr == 0)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                                 (L_bestand.lager_nr == l_lager.lager_nr)).order_by(L_artikel.zwkum, L_artikel.bezeich).all():
                            if l_bestand_obj_list.get(l_bestand._recid):
                                continue
                            else:
                                l_bestand_obj_list[l_bestand._recid] = True


                            curr_best =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)

                            if curr_best < l_artikel.min_bestand:
                                create_lines()
                    else:

                        l_bestand_obj_list = {}
                        l_bestand = L_bestand()
                        l_artikel = L_artikel()
                        l_oh = L_bestand()
                        l_untergrup = L_untergrup()
                        for l_bestand.anz_anf_best, l_bestand.anz_eingang, l_bestand.anz_ausgang, l_bestand.val_anf_best, l_bestand.wert_eingang, l_bestand.wert_ausgang, l_bestand._recid, l_artikel.zwkum, l_artikel.anzverbrauch, l_artikel.bezeich, l_artikel.artnr, l_artikel.masseinheit, l_artikel.inhalt, l_artikel.traubensorte, l_artikel.lief_einheit, l_artikel.ek_letzter, l_artikel.ek_aktuell, l_artikel.vk_preis, l_artikel.min_bestand, l_artikel._recid, l_oh.anz_anf_best, l_oh.anz_eingang, l_oh.anz_ausgang, l_oh.val_anf_best, l_oh.wert_eingang, l_oh.wert_ausgang, l_oh._recid, l_untergrup.bezeich, l_untergrup.zwkum, l_untergrup._recid in db_session.query(L_bestand.anz_anf_best, L_bestand.anz_eingang, L_bestand.anz_ausgang, L_bestand.val_anf_best, L_bestand.wert_eingang, L_bestand.wert_ausgang, L_bestand._recid, L_artikel.zwkum, L_artikel.anzverbrauch, L_artikel.bezeich, L_artikel.artnr, L_artikel.masseinheit, L_artikel.inhalt, L_artikel.traubensorte, L_artikel.lief_einheit, L_artikel.ek_letzter, L_artikel.ek_aktuell, L_artikel.vk_preis, L_artikel.min_bestand, L_artikel._recid, L_oh.anz_anf_best, L_oh.anz_eingang, L_oh.anz_ausgang, L_oh.val_anf_best, L_oh.wert_eingang, L_oh.wert_ausgang, L_oh._recid, L_untergrup.bezeich, L_untergrup.zwkum, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_bestand.artnr) & (L_artikel.zwkum == sub_grp)).join(L_oh,(L_oh.artnr == L_bestand.artnr) & (L_oh.lager_nr == 0)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                                 (L_bestand.lager_nr == l_lager.lager_nr)).order_by(L_artikel.zwkum, L_artikel.bezeich).all():
                            if l_bestand_obj_list.get(l_bestand._recid):
                                continue
                            else:
                                l_bestand_obj_list[l_bestand._recid] = True


                            create_lines()
                else:

                    if minoh_flag:

                        l_bestand_obj_list = {}
                        l_bestand = L_bestand()
                        l_artikel = L_artikel()
                        l_oh = L_bestand()
                        l_untergrup = L_untergrup()
                        for l_bestand.anz_anf_best, l_bestand.anz_eingang, l_bestand.anz_ausgang, l_bestand.val_anf_best, l_bestand.wert_eingang, l_bestand.wert_ausgang, l_bestand._recid, l_artikel.zwkum, l_artikel.anzverbrauch, l_artikel.bezeich, l_artikel.artnr, l_artikel.masseinheit, l_artikel.inhalt, l_artikel.traubensorte, l_artikel.lief_einheit, l_artikel.ek_letzter, l_artikel.ek_aktuell, l_artikel.vk_preis, l_artikel.min_bestand, l_artikel._recid, l_oh.anz_anf_best, l_oh.anz_eingang, l_oh.anz_ausgang, l_oh.val_anf_best, l_oh.wert_eingang, l_oh.wert_ausgang, l_oh._recid, l_untergrup.bezeich, l_untergrup.zwkum, l_untergrup._recid in db_session.query(L_bestand.anz_anf_best, L_bestand.anz_eingang, L_bestand.anz_ausgang, L_bestand.val_anf_best, L_bestand.wert_eingang, L_bestand.wert_ausgang, L_bestand._recid, L_artikel.zwkum, L_artikel.anzverbrauch, L_artikel.bezeich, L_artikel.artnr, L_artikel.masseinheit, L_artikel.inhalt, L_artikel.traubensorte, L_artikel.lief_einheit, L_artikel.ek_letzter, L_artikel.ek_aktuell, L_artikel.vk_preis, L_artikel.min_bestand, L_artikel._recid, L_oh.anz_anf_best, L_oh.anz_eingang, L_oh.anz_ausgang, L_oh.val_anf_best, L_oh.wert_eingang, L_oh.wert_ausgang, L_oh._recid, L_untergrup.bezeich, L_untergrup.zwkum, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_bestand.artnr) & (L_artikel.min_bestand > 0)).join(L_oh,(L_oh.artnr == L_bestand.artnr) & (L_oh.lager_nr == 0)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                                 (L_bestand.lager_nr == l_lager.lager_nr)).order_by(L_artikel.zwkum, L_artikel.bezeich).all():
                            if l_bestand_obj_list.get(l_bestand._recid):
                                continue
                            else:
                                l_bestand_obj_list[l_bestand._recid] = True


                            curr_best =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)

                            if curr_best < l_artikel.min_bestand:
                                create_lines()
                    else:

                        l_bestand_obj_list = {}
                        l_bestand = L_bestand()
                        l_artikel = L_artikel()
                        l_oh = L_bestand()
                        l_untergrup = L_untergrup()
                        for l_bestand.anz_anf_best, l_bestand.anz_eingang, l_bestand.anz_ausgang, l_bestand.val_anf_best, l_bestand.wert_eingang, l_bestand.wert_ausgang, l_bestand._recid, l_artikel.zwkum, l_artikel.anzverbrauch, l_artikel.bezeich, l_artikel.artnr, l_artikel.masseinheit, l_artikel.inhalt, l_artikel.traubensorte, l_artikel.lief_einheit, l_artikel.ek_letzter, l_artikel.ek_aktuell, l_artikel.vk_preis, l_artikel.min_bestand, l_artikel._recid, l_oh.anz_anf_best, l_oh.anz_eingang, l_oh.anz_ausgang, l_oh.val_anf_best, l_oh.wert_eingang, l_oh.wert_ausgang, l_oh._recid, l_untergrup.bezeich, l_untergrup.zwkum, l_untergrup._recid in db_session.query(L_bestand.anz_anf_best, L_bestand.anz_eingang, L_bestand.anz_ausgang, L_bestand.val_anf_best, L_bestand.wert_eingang, L_bestand.wert_ausgang, L_bestand._recid, L_artikel.zwkum, L_artikel.anzverbrauch, L_artikel.bezeich, L_artikel.artnr, L_artikel.masseinheit, L_artikel.inhalt, L_artikel.traubensorte, L_artikel.lief_einheit, L_artikel.ek_letzter, L_artikel.ek_aktuell, L_artikel.vk_preis, L_artikel.min_bestand, L_artikel._recid, L_oh.anz_anf_best, L_oh.anz_eingang, L_oh.anz_ausgang, L_oh.val_anf_best, L_oh.wert_eingang, L_oh.wert_ausgang, L_oh._recid, L_untergrup.bezeich, L_untergrup.zwkum, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_bestand.artnr)).join(L_oh,(L_oh.artnr == L_bestand.artnr) & (L_oh.lager_nr == 0)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                                 (L_bestand.lager_nr == l_lager.lager_nr)).order_by(L_artikel.zwkum, L_artikel.bezeich).all():
                            if l_bestand_obj_list.get(l_bestand._recid):
                                continue
                            else:
                                l_bestand_obj_list[l_bestand._recid] = True


                            create_lines()

            if t_val != 0:
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.flag = 1
                output_list.bezeich = bezeich
                output_list.act_val =  to_decimal(t_val)


                output_list = Output_list()
                output_list_list.append(output_list)

            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.flag = 1
            output_list.bezeich = tot_bezeich
            output_list.act_val =  to_decimal(tt_val)


            output_list = Output_list()
            output_list_list.append(output_list)

        output_list = Output_list()
        output_list_list.append(output_list)

        output_list.flag = 1
        output_list.bezeich = "GRAND T O T A L"
        output_list.act_val =  to_decimal(tt_value)


    def create_lista():

        nonlocal soh_list_list, curr_best, long_digit, i, j, tot_anz, tot_val, t_anz, t_val, t_value, tt_value, avrg_price, zwkum, bezeich, grp1, grp2, must_order, tt_val, qty, wert, tot_bezeich, l_bestand, htparam, l_lager, l_artikel, l_untergrup
        nonlocal all_flag, show_price, zero_flag, from_grp, sub_grp, from_lager, to_lager, sorttype, mattype, minoh_flag
        nonlocal l_oh


        nonlocal str_list, soh_list, output_list, l_oh
        nonlocal str_list_list, soh_list_list, output_list_list


        str_list_list.clear()
        i = 0
        zwkum = 0
        t_anz =  to_decimal("0")
        t_val =  to_decimal("0")
        tt_val =  to_decimal("0")

        if sorttype == 1:

            if sub_grp != 000:

                if minoh_flag:

                    l_bestand_obj_list = {}
                    l_bestand = L_bestand()
                    l_artikel = L_artikel()
                    l_untergrup = L_untergrup()
                    for l_bestand.anz_anf_best, l_bestand.anz_eingang, l_bestand.anz_ausgang, l_bestand.val_anf_best, l_bestand.wert_eingang, l_bestand.wert_ausgang, l_bestand._recid, l_artikel.zwkum, l_artikel.anzverbrauch, l_artikel.bezeich, l_artikel.artnr, l_artikel.masseinheit, l_artikel.inhalt, l_artikel.traubensorte, l_artikel.lief_einheit, l_artikel.ek_letzter, l_artikel.ek_aktuell, l_artikel.vk_preis, l_artikel.min_bestand, l_artikel._recid, l_untergrup.bezeich, l_untergrup.zwkum, l_untergrup._recid in db_session.query(L_bestand.anz_anf_best, L_bestand.anz_eingang, L_bestand.anz_ausgang, L_bestand.val_anf_best, L_bestand.wert_eingang, L_bestand.wert_ausgang, L_bestand._recid, L_artikel.zwkum, L_artikel.anzverbrauch, L_artikel.bezeich, L_artikel.artnr, L_artikel.masseinheit, L_artikel.inhalt, L_artikel.traubensorte, L_artikel.lief_einheit, L_artikel.ek_letzter, L_artikel.ek_aktuell, L_artikel.vk_preis, L_artikel.min_bestand, L_artikel._recid, L_untergrup.bezeich, L_untergrup.zwkum, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_bestand.artnr) & (L_artikel.zwkum == sub_grp) & (L_artikel.min_bestand > 0)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                                 (L_bestand.lager_nr == 0)).order_by(L_artikel.zwkum, L_artikel.artnr).all():
                        if l_bestand_obj_list.get(l_bestand._recid):
                            continue
                        else:
                            l_bestand_obj_list[l_bestand._recid] = True


                        curr_best =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)

                        if curr_best < l_artikel.min_bestand:
                            create_lines_global_oh()
                else:

                    l_bestand_obj_list = {}
                    l_bestand = L_bestand()
                    l_artikel = L_artikel()
                    l_untergrup = L_untergrup()
                    for l_bestand.anz_anf_best, l_bestand.anz_eingang, l_bestand.anz_ausgang, l_bestand.val_anf_best, l_bestand.wert_eingang, l_bestand.wert_ausgang, l_bestand._recid, l_artikel.zwkum, l_artikel.anzverbrauch, l_artikel.bezeich, l_artikel.artnr, l_artikel.masseinheit, l_artikel.inhalt, l_artikel.traubensorte, l_artikel.lief_einheit, l_artikel.ek_letzter, l_artikel.ek_aktuell, l_artikel.vk_preis, l_artikel.min_bestand, l_artikel._recid, l_untergrup.bezeich, l_untergrup.zwkum, l_untergrup._recid in db_session.query(L_bestand.anz_anf_best, L_bestand.anz_eingang, L_bestand.anz_ausgang, L_bestand.val_anf_best, L_bestand.wert_eingang, L_bestand.wert_ausgang, L_bestand._recid, L_artikel.zwkum, L_artikel.anzverbrauch, L_artikel.bezeich, L_artikel.artnr, L_artikel.masseinheit, L_artikel.inhalt, L_artikel.traubensorte, L_artikel.lief_einheit, L_artikel.ek_letzter, L_artikel.ek_aktuell, L_artikel.vk_preis, L_artikel.min_bestand, L_artikel._recid, L_untergrup.bezeich, L_untergrup.zwkum, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_bestand.artnr) & (L_artikel.zwkum == sub_grp)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                                 (L_bestand.lager_nr == 0)).order_by(L_artikel.zwkum, L_artikel.artnr).all():
                        if l_bestand_obj_list.get(l_bestand._recid):
                            continue
                        else:
                            l_bestand_obj_list[l_bestand._recid] = True


                        create_lines_global_oh()
            else:

                if minoh_flag:

                    l_bestand_obj_list = {}
                    l_bestand = L_bestand()
                    l_artikel = L_artikel()
                    l_untergrup = L_untergrup()
                    for l_bestand.anz_anf_best, l_bestand.anz_eingang, l_bestand.anz_ausgang, l_bestand.val_anf_best, l_bestand.wert_eingang, l_bestand.wert_ausgang, l_bestand._recid, l_artikel.zwkum, l_artikel.anzverbrauch, l_artikel.bezeich, l_artikel.artnr, l_artikel.masseinheit, l_artikel.inhalt, l_artikel.traubensorte, l_artikel.lief_einheit, l_artikel.ek_letzter, l_artikel.ek_aktuell, l_artikel.vk_preis, l_artikel.min_bestand, l_artikel._recid, l_untergrup.bezeich, l_untergrup.zwkum, l_untergrup._recid in db_session.query(L_bestand.anz_anf_best, L_bestand.anz_eingang, L_bestand.anz_ausgang, L_bestand.val_anf_best, L_bestand.wert_eingang, L_bestand.wert_ausgang, L_bestand._recid, L_artikel.zwkum, L_artikel.anzverbrauch, L_artikel.bezeich, L_artikel.artnr, L_artikel.masseinheit, L_artikel.inhalt, L_artikel.traubensorte, L_artikel.lief_einheit, L_artikel.ek_letzter, L_artikel.ek_aktuell, L_artikel.vk_preis, L_artikel.min_bestand, L_artikel._recid, L_untergrup.bezeich, L_untergrup.zwkum, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_bestand.artnr) & (L_artikel.min_bestand > 0)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                                 (L_bestand.lager_nr == 0)).order_by(L_artikel.zwkum, L_artikel.artnr).all():
                        if l_bestand_obj_list.get(l_bestand._recid):
                            continue
                        else:
                            l_bestand_obj_list[l_bestand._recid] = True


                        curr_best =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)

                        if curr_best < l_artikel.min_bestand:
                            create_lines_global_oh()
                else:

                    l_bestand_obj_list = {}
                    l_bestand = L_bestand()
                    l_artikel = L_artikel()
                    l_untergrup = L_untergrup()
                    for l_bestand.anz_anf_best, l_bestand.anz_eingang, l_bestand.anz_ausgang, l_bestand.val_anf_best, l_bestand.wert_eingang, l_bestand.wert_ausgang, l_bestand._recid, l_artikel.zwkum, l_artikel.anzverbrauch, l_artikel.bezeich, l_artikel.artnr, l_artikel.masseinheit, l_artikel.inhalt, l_artikel.traubensorte, l_artikel.lief_einheit, l_artikel.ek_letzter, l_artikel.ek_aktuell, l_artikel.vk_preis, l_artikel.min_bestand, l_artikel._recid, l_untergrup.bezeich, l_untergrup.zwkum, l_untergrup._recid in db_session.query(L_bestand.anz_anf_best, L_bestand.anz_eingang, L_bestand.anz_ausgang, L_bestand.val_anf_best, L_bestand.wert_eingang, L_bestand.wert_ausgang, L_bestand._recid, L_artikel.zwkum, L_artikel.anzverbrauch, L_artikel.bezeich, L_artikel.artnr, L_artikel.masseinheit, L_artikel.inhalt, L_artikel.traubensorte, L_artikel.lief_einheit, L_artikel.ek_letzter, L_artikel.ek_aktuell, L_artikel.vk_preis, L_artikel.min_bestand, L_artikel._recid, L_untergrup.bezeich, L_untergrup.zwkum, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_bestand.artnr)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                                 (L_bestand.lager_nr == 0)).order_by(L_artikel.zwkum, L_artikel.artnr).all():
                        if l_bestand_obj_list.get(l_bestand._recid):
                            continue
                        else:
                            l_bestand_obj_list[l_bestand._recid] = True


                        create_lines_global_oh()

        elif sorttype == 2:

            if sub_grp != 000:

                if minoh_flag:

                    l_bestand_obj_list = {}
                    l_bestand = L_bestand()
                    l_artikel = L_artikel()
                    l_untergrup = L_untergrup()
                    for l_bestand.anz_anf_best, l_bestand.anz_eingang, l_bestand.anz_ausgang, l_bestand.val_anf_best, l_bestand.wert_eingang, l_bestand.wert_ausgang, l_bestand._recid, l_artikel.zwkum, l_artikel.anzverbrauch, l_artikel.bezeich, l_artikel.artnr, l_artikel.masseinheit, l_artikel.inhalt, l_artikel.traubensorte, l_artikel.lief_einheit, l_artikel.ek_letzter, l_artikel.ek_aktuell, l_artikel.vk_preis, l_artikel.min_bestand, l_artikel._recid, l_untergrup.bezeich, l_untergrup.zwkum, l_untergrup._recid in db_session.query(L_bestand.anz_anf_best, L_bestand.anz_eingang, L_bestand.anz_ausgang, L_bestand.val_anf_best, L_bestand.wert_eingang, L_bestand.wert_ausgang, L_bestand._recid, L_artikel.zwkum, L_artikel.anzverbrauch, L_artikel.bezeich, L_artikel.artnr, L_artikel.masseinheit, L_artikel.inhalt, L_artikel.traubensorte, L_artikel.lief_einheit, L_artikel.ek_letzter, L_artikel.ek_aktuell, L_artikel.vk_preis, L_artikel.min_bestand, L_artikel._recid, L_untergrup.bezeich, L_untergrup.zwkum, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_bestand.artnr) & (L_artikel.zwkum == sub_grp) & (L_artikel.min_bestand > 0)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                                 (L_bestand.lager_nr == 0)).order_by(L_artikel.zwkum, L_artikel.bezeich).all():
                        if l_bestand_obj_list.get(l_bestand._recid):
                            continue
                        else:
                            l_bestand_obj_list[l_bestand._recid] = True


                        curr_best =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)

                        if curr_best < l_artikel.min_bestand:
                            create_lines_global_oh()
                else:

                    l_bestand_obj_list = {}
                    l_bestand = L_bestand()
                    l_artikel = L_artikel()
                    l_untergrup = L_untergrup()
                    for l_bestand.anz_anf_best, l_bestand.anz_eingang, l_bestand.anz_ausgang, l_bestand.val_anf_best, l_bestand.wert_eingang, l_bestand.wert_ausgang, l_bestand._recid, l_artikel.zwkum, l_artikel.anzverbrauch, l_artikel.bezeich, l_artikel.artnr, l_artikel.masseinheit, l_artikel.inhalt, l_artikel.traubensorte, l_artikel.lief_einheit, l_artikel.ek_letzter, l_artikel.ek_aktuell, l_artikel.vk_preis, l_artikel.min_bestand, l_artikel._recid, l_untergrup.bezeich, l_untergrup.zwkum, l_untergrup._recid in db_session.query(L_bestand.anz_anf_best, L_bestand.anz_eingang, L_bestand.anz_ausgang, L_bestand.val_anf_best, L_bestand.wert_eingang, L_bestand.wert_ausgang, L_bestand._recid, L_artikel.zwkum, L_artikel.anzverbrauch, L_artikel.bezeich, L_artikel.artnr, L_artikel.masseinheit, L_artikel.inhalt, L_artikel.traubensorte, L_artikel.lief_einheit, L_artikel.ek_letzter, L_artikel.ek_aktuell, L_artikel.vk_preis, L_artikel.min_bestand, L_artikel._recid, L_untergrup.bezeich, L_untergrup.zwkum, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_bestand.artnr) & (L_artikel.zwkum == sub_grp)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                                 (L_bestand.lager_nr == 0)).order_by(L_artikel.zwkum, L_artikel.bezeich).all():
                        if l_bestand_obj_list.get(l_bestand._recid):
                            continue
                        else:
                            l_bestand_obj_list[l_bestand._recid] = True


                        create_lines_global_oh()
            else:

                if minoh_flag:

                    l_bestand_obj_list = {}
                    l_bestand = L_bestand()
                    l_artikel = L_artikel()
                    l_untergrup = L_untergrup()
                    for l_bestand.anz_anf_best, l_bestand.anz_eingang, l_bestand.anz_ausgang, l_bestand.val_anf_best, l_bestand.wert_eingang, l_bestand.wert_ausgang, l_bestand._recid, l_artikel.zwkum, l_artikel.anzverbrauch, l_artikel.bezeich, l_artikel.artnr, l_artikel.masseinheit, l_artikel.inhalt, l_artikel.traubensorte, l_artikel.lief_einheit, l_artikel.ek_letzter, l_artikel.ek_aktuell, l_artikel.vk_preis, l_artikel.min_bestand, l_artikel._recid, l_untergrup.bezeich, l_untergrup.zwkum, l_untergrup._recid in db_session.query(L_bestand.anz_anf_best, L_bestand.anz_eingang, L_bestand.anz_ausgang, L_bestand.val_anf_best, L_bestand.wert_eingang, L_bestand.wert_ausgang, L_bestand._recid, L_artikel.zwkum, L_artikel.anzverbrauch, L_artikel.bezeich, L_artikel.artnr, L_artikel.masseinheit, L_artikel.inhalt, L_artikel.traubensorte, L_artikel.lief_einheit, L_artikel.ek_letzter, L_artikel.ek_aktuell, L_artikel.vk_preis, L_artikel.min_bestand, L_artikel._recid, L_untergrup.bezeich, L_untergrup.zwkum, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_bestand.artnr) & (L_artikel.min_bestand > 0)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                                 (L_bestand.lager_nr == 0)).order_by(L_artikel.zwkum, L_artikel.bezeich).all():
                        if l_bestand_obj_list.get(l_bestand._recid):
                            continue
                        else:
                            l_bestand_obj_list[l_bestand._recid] = True


                        curr_best =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)

                        if curr_best < l_artikel.min_bestand:
                            create_lines_global_oh()
                else:

                    l_bestand_obj_list = {}
                    l_bestand = L_bestand()
                    l_artikel = L_artikel()
                    l_untergrup = L_untergrup()
                    for l_bestand.anz_anf_best, l_bestand.anz_eingang, l_bestand.anz_ausgang, l_bestand.val_anf_best, l_bestand.wert_eingang, l_bestand.wert_ausgang, l_bestand._recid, l_artikel.zwkum, l_artikel.anzverbrauch, l_artikel.bezeich, l_artikel.artnr, l_artikel.masseinheit, l_artikel.inhalt, l_artikel.traubensorte, l_artikel.lief_einheit, l_artikel.ek_letzter, l_artikel.ek_aktuell, l_artikel.vk_preis, l_artikel.min_bestand, l_artikel._recid, l_untergrup.bezeich, l_untergrup.zwkum, l_untergrup._recid in db_session.query(L_bestand.anz_anf_best, L_bestand.anz_eingang, L_bestand.anz_ausgang, L_bestand.val_anf_best, L_bestand.wert_eingang, L_bestand.wert_ausgang, L_bestand._recid, L_artikel.zwkum, L_artikel.anzverbrauch, L_artikel.bezeich, L_artikel.artnr, L_artikel.masseinheit, L_artikel.inhalt, L_artikel.traubensorte, L_artikel.lief_einheit, L_artikel.ek_letzter, L_artikel.ek_aktuell, L_artikel.vk_preis, L_artikel.min_bestand, L_artikel._recid, L_untergrup.bezeich, L_untergrup.zwkum, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_bestand.artnr)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                                 (L_bestand.lager_nr == 0)).order_by(L_artikel.zwkum, L_artikel.bezeich).all():
                        if l_bestand_obj_list.get(l_bestand._recid):
                            continue
                        else:
                            l_bestand_obj_list[l_bestand._recid] = True


                        create_lines_global_oh()

        if t_val != 0:
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.flag = 1
            output_list.bezeich = bezeich
            output_list.act_val =  to_decimal(t_val)


            output_list = Output_list()
            output_list_list.append(output_list)

        output_list = Output_list()
        output_list_list.append(output_list)

        output_list.flag = 1
        output_list.bezeich = "GRAND T O T A L"
        output_list.act_val =  to_decimal(tt_value)


    def create_list1():

        nonlocal soh_list_list, curr_best, long_digit, i, j, tot_anz, tot_val, t_anz, t_val, t_value, tt_value, avrg_price, zwkum, bezeich, grp1, grp2, must_order, tt_val, qty, wert, tot_bezeich, l_bestand, htparam, l_lager, l_artikel, l_untergrup
        nonlocal all_flag, show_price, zero_flag, from_grp, sub_grp, from_lager, to_lager, sorttype, mattype, minoh_flag
        nonlocal l_oh


        nonlocal str_list, soh_list, output_list, l_oh
        nonlocal str_list_list, soh_list_list, output_list_list


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

                    if minoh_flag:

                        l_bestand_obj_list = {}
                        l_bestand = L_bestand()
                        l_artikel = L_artikel()
                        l_oh = L_bestand()
                        l_untergrup = L_untergrup()
                        for l_bestand.anz_anf_best, l_bestand.anz_eingang, l_bestand.anz_ausgang, l_bestand.val_anf_best, l_bestand.wert_eingang, l_bestand.wert_ausgang, l_bestand._recid, l_artikel.zwkum, l_artikel.anzverbrauch, l_artikel.bezeich, l_artikel.artnr, l_artikel.masseinheit, l_artikel.inhalt, l_artikel.traubensorte, l_artikel.lief_einheit, l_artikel.ek_letzter, l_artikel.ek_aktuell, l_artikel.vk_preis, l_artikel.min_bestand, l_artikel._recid, l_oh.anz_anf_best, l_oh.anz_eingang, l_oh.anz_ausgang, l_oh.val_anf_best, l_oh.wert_eingang, l_oh.wert_ausgang, l_oh._recid, l_untergrup.bezeich, l_untergrup.zwkum, l_untergrup._recid in db_session.query(L_bestand.anz_anf_best, L_bestand.anz_eingang, L_bestand.anz_ausgang, L_bestand.val_anf_best, L_bestand.wert_eingang, L_bestand.wert_ausgang, L_bestand._recid, L_artikel.zwkum, L_artikel.anzverbrauch, L_artikel.bezeich, L_artikel.artnr, L_artikel.masseinheit, L_artikel.inhalt, L_artikel.traubensorte, L_artikel.lief_einheit, L_artikel.ek_letzter, L_artikel.ek_aktuell, L_artikel.vk_preis, L_artikel.min_bestand, L_artikel._recid, L_oh.anz_anf_best, L_oh.anz_eingang, L_oh.anz_ausgang, L_oh.val_anf_best, L_oh.wert_eingang, L_oh.wert_ausgang, L_oh._recid, L_untergrup.bezeich, L_untergrup.zwkum, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_bestand.artnr) & (L_artikel.zwkum == sub_grp) & (L_artikel.min_bestand > 0)).join(L_oh,(L_oh.artnr == L_bestand.artnr) & (L_oh.lager_nr == 0)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum) & ((L_untergrup.betriebsnr >= grp1) & (L_untergrup.betriebsnr <= grp2))).filter(
                                 (L_bestand.lager_nr == l_lager.lager_nr)).order_by(L_artikel.zwkum, L_artikel.artnr).all():
                            if l_bestand_obj_list.get(l_bestand._recid):
                                continue
                            else:
                                l_bestand_obj_list[l_bestand._recid] = True


                            curr_best =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)

                            if curr_best < l_artikel.min_bestand:
                                create_lines()
                    else:

                        l_bestand_obj_list = {}
                        l_bestand = L_bestand()
                        l_artikel = L_artikel()
                        l_oh = L_bestand()
                        l_untergrup = L_untergrup()
                        for l_bestand.anz_anf_best, l_bestand.anz_eingang, l_bestand.anz_ausgang, l_bestand.val_anf_best, l_bestand.wert_eingang, l_bestand.wert_ausgang, l_bestand._recid, l_artikel.zwkum, l_artikel.anzverbrauch, l_artikel.bezeich, l_artikel.artnr, l_artikel.masseinheit, l_artikel.inhalt, l_artikel.traubensorte, l_artikel.lief_einheit, l_artikel.ek_letzter, l_artikel.ek_aktuell, l_artikel.vk_preis, l_artikel.min_bestand, l_artikel._recid, l_oh.anz_anf_best, l_oh.anz_eingang, l_oh.anz_ausgang, l_oh.val_anf_best, l_oh.wert_eingang, l_oh.wert_ausgang, l_oh._recid, l_untergrup.bezeich, l_untergrup.zwkum, l_untergrup._recid in db_session.query(L_bestand.anz_anf_best, L_bestand.anz_eingang, L_bestand.anz_ausgang, L_bestand.val_anf_best, L_bestand.wert_eingang, L_bestand.wert_ausgang, L_bestand._recid, L_artikel.zwkum, L_artikel.anzverbrauch, L_artikel.bezeich, L_artikel.artnr, L_artikel.masseinheit, L_artikel.inhalt, L_artikel.traubensorte, L_artikel.lief_einheit, L_artikel.ek_letzter, L_artikel.ek_aktuell, L_artikel.vk_preis, L_artikel.min_bestand, L_artikel._recid, L_oh.anz_anf_best, L_oh.anz_eingang, L_oh.anz_ausgang, L_oh.val_anf_best, L_oh.wert_eingang, L_oh.wert_ausgang, L_oh._recid, L_untergrup.bezeich, L_untergrup.zwkum, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_bestand.artnr) & (L_artikel.zwkum == sub_grp)).join(L_oh,(L_oh.artnr == L_bestand.artnr) & (L_oh.lager_nr == 0)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum) & ((L_untergrup.betriebsnr >= grp1) & (L_untergrup.betriebsnr <= grp2))).filter(
                                 (L_bestand.lager_nr == l_lager.lager_nr)).order_by(L_artikel.zwkum, L_artikel.artnr).all():
                            if l_bestand_obj_list.get(l_bestand._recid):
                                continue
                            else:
                                l_bestand_obj_list[l_bestand._recid] = True


                            create_lines()
                else:

                    if minoh_flag:

                        l_bestand_obj_list = {}
                        l_bestand = L_bestand()
                        l_artikel = L_artikel()
                        l_oh = L_bestand()
                        l_untergrup = L_untergrup()
                        for l_bestand.anz_anf_best, l_bestand.anz_eingang, l_bestand.anz_ausgang, l_bestand.val_anf_best, l_bestand.wert_eingang, l_bestand.wert_ausgang, l_bestand._recid, l_artikel.zwkum, l_artikel.anzverbrauch, l_artikel.bezeich, l_artikel.artnr, l_artikel.masseinheit, l_artikel.inhalt, l_artikel.traubensorte, l_artikel.lief_einheit, l_artikel.ek_letzter, l_artikel.ek_aktuell, l_artikel.vk_preis, l_artikel.min_bestand, l_artikel._recid, l_oh.anz_anf_best, l_oh.anz_eingang, l_oh.anz_ausgang, l_oh.val_anf_best, l_oh.wert_eingang, l_oh.wert_ausgang, l_oh._recid, l_untergrup.bezeich, l_untergrup.zwkum, l_untergrup._recid in db_session.query(L_bestand.anz_anf_best, L_bestand.anz_eingang, L_bestand.anz_ausgang, L_bestand.val_anf_best, L_bestand.wert_eingang, L_bestand.wert_ausgang, L_bestand._recid, L_artikel.zwkum, L_artikel.anzverbrauch, L_artikel.bezeich, L_artikel.artnr, L_artikel.masseinheit, L_artikel.inhalt, L_artikel.traubensorte, L_artikel.lief_einheit, L_artikel.ek_letzter, L_artikel.ek_aktuell, L_artikel.vk_preis, L_artikel.min_bestand, L_artikel._recid, L_oh.anz_anf_best, L_oh.anz_eingang, L_oh.anz_ausgang, L_oh.val_anf_best, L_oh.wert_eingang, L_oh.wert_ausgang, L_oh._recid, L_untergrup.bezeich, L_untergrup.zwkum, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_bestand.artnr) & (L_artikel.endkum == from_grp) & (L_artikel.min_bestand > 0)).join(L_oh,(L_oh.artnr == L_bestand.artnr) & (L_oh.lager_nr == 0)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum) & ((L_untergrup.betriebsnr >= grp1) & (L_untergrup.betriebsnr <= grp2))).filter(
                                 (L_bestand.lager_nr == l_lager.lager_nr)).order_by(L_artikel.zwkum, L_artikel.artnr).all():
                            if l_bestand_obj_list.get(l_bestand._recid):
                                continue
                            else:
                                l_bestand_obj_list[l_bestand._recid] = True


                            curr_best =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)

                            if curr_best < l_artikel.min_bestand:
                                create_lines()
                    else:

                        l_bestand_obj_list = {}
                        l_bestand = L_bestand()
                        l_artikel = L_artikel()
                        l_oh = L_bestand()
                        l_untergrup = L_untergrup()
                        for l_bestand.anz_anf_best, l_bestand.anz_eingang, l_bestand.anz_ausgang, l_bestand.val_anf_best, l_bestand.wert_eingang, l_bestand.wert_ausgang, l_bestand._recid, l_artikel.zwkum, l_artikel.anzverbrauch, l_artikel.bezeich, l_artikel.artnr, l_artikel.masseinheit, l_artikel.inhalt, l_artikel.traubensorte, l_artikel.lief_einheit, l_artikel.ek_letzter, l_artikel.ek_aktuell, l_artikel.vk_preis, l_artikel.min_bestand, l_artikel._recid, l_oh.anz_anf_best, l_oh.anz_eingang, l_oh.anz_ausgang, l_oh.val_anf_best, l_oh.wert_eingang, l_oh.wert_ausgang, l_oh._recid, l_untergrup.bezeich, l_untergrup.zwkum, l_untergrup._recid in db_session.query(L_bestand.anz_anf_best, L_bestand.anz_eingang, L_bestand.anz_ausgang, L_bestand.val_anf_best, L_bestand.wert_eingang, L_bestand.wert_ausgang, L_bestand._recid, L_artikel.zwkum, L_artikel.anzverbrauch, L_artikel.bezeich, L_artikel.artnr, L_artikel.masseinheit, L_artikel.inhalt, L_artikel.traubensorte, L_artikel.lief_einheit, L_artikel.ek_letzter, L_artikel.ek_aktuell, L_artikel.vk_preis, L_artikel.min_bestand, L_artikel._recid, L_oh.anz_anf_best, L_oh.anz_eingang, L_oh.anz_ausgang, L_oh.val_anf_best, L_oh.wert_eingang, L_oh.wert_ausgang, L_oh._recid, L_untergrup.bezeich, L_untergrup.zwkum, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_bestand.artnr) & (L_artikel.endkum == from_grp)).join(L_oh,(L_oh.artnr == L_bestand.artnr) & (L_oh.lager_nr == 0)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum) & ((L_untergrup.betriebsnr >= grp1) & (L_untergrup.betriebsnr <= grp2))).filter(
                                 (L_bestand.lager_nr == l_lager.lager_nr)).order_by(L_artikel.zwkum, L_artikel.artnr).all():
                            if l_bestand_obj_list.get(l_bestand._recid):
                                continue
                            else:
                                l_bestand_obj_list[l_bestand._recid] = True


                            create_lines()

            elif sorttype == 2:

                if sub_grp != 000:

                    if minoh_flag:

                        l_bestand_obj_list = {}
                        l_bestand = L_bestand()
                        l_artikel = L_artikel()
                        l_oh = L_bestand()
                        l_untergrup = L_untergrup()
                        for l_bestand.anz_anf_best, l_bestand.anz_eingang, l_bestand.anz_ausgang, l_bestand.val_anf_best, l_bestand.wert_eingang, l_bestand.wert_ausgang, l_bestand._recid, l_artikel.zwkum, l_artikel.anzverbrauch, l_artikel.bezeich, l_artikel.artnr, l_artikel.masseinheit, l_artikel.inhalt, l_artikel.traubensorte, l_artikel.lief_einheit, l_artikel.ek_letzter, l_artikel.ek_aktuell, l_artikel.vk_preis, l_artikel.min_bestand, l_artikel._recid, l_oh.anz_anf_best, l_oh.anz_eingang, l_oh.anz_ausgang, l_oh.val_anf_best, l_oh.wert_eingang, l_oh.wert_ausgang, l_oh._recid, l_untergrup.bezeich, l_untergrup.zwkum, l_untergrup._recid in db_session.query(L_bestand.anz_anf_best, L_bestand.anz_eingang, L_bestand.anz_ausgang, L_bestand.val_anf_best, L_bestand.wert_eingang, L_bestand.wert_ausgang, L_bestand._recid, L_artikel.zwkum, L_artikel.anzverbrauch, L_artikel.bezeich, L_artikel.artnr, L_artikel.masseinheit, L_artikel.inhalt, L_artikel.traubensorte, L_artikel.lief_einheit, L_artikel.ek_letzter, L_artikel.ek_aktuell, L_artikel.vk_preis, L_artikel.min_bestand, L_artikel._recid, L_oh.anz_anf_best, L_oh.anz_eingang, L_oh.anz_ausgang, L_oh.val_anf_best, L_oh.wert_eingang, L_oh.wert_ausgang, L_oh._recid, L_untergrup.bezeich, L_untergrup.zwkum, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_bestand.artnr) & (L_artikel.zwkum == sub_grp) & (L_artikel.min_bestand > 0)).join(L_oh,(L_oh.artnr == L_bestand.artnr) & (L_oh.lager_nr == 0)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum) & ((L_untergrup.betriebsnr >= grp1) & (L_untergrup.betriebsnr <= grp2))).filter(
                                 (L_bestand.lager_nr == l_lager.lager_nr)).order_by(L_artikel.zwkum, L_artikel.bezeich).all():
                            if l_bestand_obj_list.get(l_bestand._recid):
                                continue
                            else:
                                l_bestand_obj_list[l_bestand._recid] = True


                            curr_best =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)

                            if curr_best < l_artikel.min_bestand:
                                create_lines()
                    else:

                        l_bestand_obj_list = {}
                        l_bestand = L_bestand()
                        l_artikel = L_artikel()
                        l_oh = L_bestand()
                        l_untergrup = L_untergrup()
                        for l_bestand.anz_anf_best, l_bestand.anz_eingang, l_bestand.anz_ausgang, l_bestand.val_anf_best, l_bestand.wert_eingang, l_bestand.wert_ausgang, l_bestand._recid, l_artikel.zwkum, l_artikel.anzverbrauch, l_artikel.bezeich, l_artikel.artnr, l_artikel.masseinheit, l_artikel.inhalt, l_artikel.traubensorte, l_artikel.lief_einheit, l_artikel.ek_letzter, l_artikel.ek_aktuell, l_artikel.vk_preis, l_artikel.min_bestand, l_artikel._recid, l_oh.anz_anf_best, l_oh.anz_eingang, l_oh.anz_ausgang, l_oh.val_anf_best, l_oh.wert_eingang, l_oh.wert_ausgang, l_oh._recid, l_untergrup.bezeich, l_untergrup.zwkum, l_untergrup._recid in db_session.query(L_bestand.anz_anf_best, L_bestand.anz_eingang, L_bestand.anz_ausgang, L_bestand.val_anf_best, L_bestand.wert_eingang, L_bestand.wert_ausgang, L_bestand._recid, L_artikel.zwkum, L_artikel.anzverbrauch, L_artikel.bezeich, L_artikel.artnr, L_artikel.masseinheit, L_artikel.inhalt, L_artikel.traubensorte, L_artikel.lief_einheit, L_artikel.ek_letzter, L_artikel.ek_aktuell, L_artikel.vk_preis, L_artikel.min_bestand, L_artikel._recid, L_oh.anz_anf_best, L_oh.anz_eingang, L_oh.anz_ausgang, L_oh.val_anf_best, L_oh.wert_eingang, L_oh.wert_ausgang, L_oh._recid, L_untergrup.bezeich, L_untergrup.zwkum, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_bestand.artnr) & (L_artikel.zwkum == sub_grp)).join(L_oh,(L_oh.artnr == L_bestand.artnr) & (L_oh.lager_nr == 0)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum) & ((L_untergrup.betriebsnr >= grp1) & (L_untergrup.betriebsnr <= grp2))).filter(
                                 (L_bestand.lager_nr == l_lager.lager_nr)).order_by(L_artikel.zwkum, L_artikel.bezeich).all():
                            if l_bestand_obj_list.get(l_bestand._recid):
                                continue
                            else:
                                l_bestand_obj_list[l_bestand._recid] = True


                            create_lines()
                else:

                    if minoh_flag:

                        l_bestand_obj_list = {}
                        l_bestand = L_bestand()
                        l_artikel = L_artikel()
                        l_oh = L_bestand()
                        l_untergrup = L_untergrup()
                        for l_bestand.anz_anf_best, l_bestand.anz_eingang, l_bestand.anz_ausgang, l_bestand.val_anf_best, l_bestand.wert_eingang, l_bestand.wert_ausgang, l_bestand._recid, l_artikel.zwkum, l_artikel.anzverbrauch, l_artikel.bezeich, l_artikel.artnr, l_artikel.masseinheit, l_artikel.inhalt, l_artikel.traubensorte, l_artikel.lief_einheit, l_artikel.ek_letzter, l_artikel.ek_aktuell, l_artikel.vk_preis, l_artikel.min_bestand, l_artikel._recid, l_oh.anz_anf_best, l_oh.anz_eingang, l_oh.anz_ausgang, l_oh.val_anf_best, l_oh.wert_eingang, l_oh.wert_ausgang, l_oh._recid, l_untergrup.bezeich, l_untergrup.zwkum, l_untergrup._recid in db_session.query(L_bestand.anz_anf_best, L_bestand.anz_eingang, L_bestand.anz_ausgang, L_bestand.val_anf_best, L_bestand.wert_eingang, L_bestand.wert_ausgang, L_bestand._recid, L_artikel.zwkum, L_artikel.anzverbrauch, L_artikel.bezeich, L_artikel.artnr, L_artikel.masseinheit, L_artikel.inhalt, L_artikel.traubensorte, L_artikel.lief_einheit, L_artikel.ek_letzter, L_artikel.ek_aktuell, L_artikel.vk_preis, L_artikel.min_bestand, L_artikel._recid, L_oh.anz_anf_best, L_oh.anz_eingang, L_oh.anz_ausgang, L_oh.val_anf_best, L_oh.wert_eingang, L_oh.wert_ausgang, L_oh._recid, L_untergrup.bezeich, L_untergrup.zwkum, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_bestand.artnr) & (L_artikel.endkum == from_grp) & (L_artikel.min_bestand > 0)).join(L_oh,(L_oh.artnr == L_bestand.artnr) & (L_oh.lager_nr == 0)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum) & ((L_untergrup.betriebsnr >= grp1) & (L_untergrup.betriebsnr <= grp2))).filter(
                                 (L_bestand.lager_nr == l_lager.lager_nr)).order_by(L_artikel.zwkum, L_artikel.bezeich).all():
                            if l_bestand_obj_list.get(l_bestand._recid):
                                continue
                            else:
                                l_bestand_obj_list[l_bestand._recid] = True


                            curr_best =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)

                            if curr_best < l_artikel.min_bestand:
                                create_lines()
                    else:

                        l_bestand_obj_list = {}
                        l_bestand = L_bestand()
                        l_artikel = L_artikel()
                        l_oh = L_bestand()
                        l_untergrup = L_untergrup()
                        for l_bestand.anz_anf_best, l_bestand.anz_eingang, l_bestand.anz_ausgang, l_bestand.val_anf_best, l_bestand.wert_eingang, l_bestand.wert_ausgang, l_bestand._recid, l_artikel.zwkum, l_artikel.anzverbrauch, l_artikel.bezeich, l_artikel.artnr, l_artikel.masseinheit, l_artikel.inhalt, l_artikel.traubensorte, l_artikel.lief_einheit, l_artikel.ek_letzter, l_artikel.ek_aktuell, l_artikel.vk_preis, l_artikel.min_bestand, l_artikel._recid, l_oh.anz_anf_best, l_oh.anz_eingang, l_oh.anz_ausgang, l_oh.val_anf_best, l_oh.wert_eingang, l_oh.wert_ausgang, l_oh._recid, l_untergrup.bezeich, l_untergrup.zwkum, l_untergrup._recid in db_session.query(L_bestand.anz_anf_best, L_bestand.anz_eingang, L_bestand.anz_ausgang, L_bestand.val_anf_best, L_bestand.wert_eingang, L_bestand.wert_ausgang, L_bestand._recid, L_artikel.zwkum, L_artikel.anzverbrauch, L_artikel.bezeich, L_artikel.artnr, L_artikel.masseinheit, L_artikel.inhalt, L_artikel.traubensorte, L_artikel.lief_einheit, L_artikel.ek_letzter, L_artikel.ek_aktuell, L_artikel.vk_preis, L_artikel.min_bestand, L_artikel._recid, L_oh.anz_anf_best, L_oh.anz_eingang, L_oh.anz_ausgang, L_oh.val_anf_best, L_oh.wert_eingang, L_oh.wert_ausgang, L_oh._recid, L_untergrup.bezeich, L_untergrup.zwkum, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_bestand.artnr) & (L_artikel.endkum == from_grp)).join(L_oh,(L_oh.artnr == L_bestand.artnr) & (L_oh.lager_nr == 0)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum) & ((L_untergrup.betriebsnr >= grp1) & (L_untergrup.betriebsnr <= grp2))).filter(
                                 (L_bestand.lager_nr == l_lager.lager_nr)).order_by(L_artikel.zwkum, L_artikel.bezeich).all():
                            if l_bestand_obj_list.get(l_bestand._recid):
                                continue
                            else:
                                l_bestand_obj_list[l_bestand._recid] = True


                            create_lines()

            if t_val != 0:
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.flag = 1
                output_list.bezeich = bezeich
                output_list.act_val =  to_decimal(t_val)


                output_list = Output_list()
                output_list_list.append(output_list)

            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.flag = 1
            output_list.bezeich = tot_bezeich
            output_list.act_val =  to_decimal(tt_val)


            output_list = Output_list()
            output_list_list.append(output_list)

        output_list = Output_list()
        output_list_list.append(output_list)

        output_list.flag = 1
        output_list.bezeich = "GRAND T O T A L"
        output_list.act_val =  to_decimal(tt_value)


    def create_list1a():

        nonlocal soh_list_list, curr_best, long_digit, i, j, tot_anz, tot_val, t_anz, t_val, t_value, tt_value, avrg_price, zwkum, bezeich, grp1, grp2, must_order, tt_val, qty, wert, tot_bezeich, l_bestand, htparam, l_lager, l_artikel, l_untergrup
        nonlocal all_flag, show_price, zero_flag, from_grp, sub_grp, from_lager, to_lager, sorttype, mattype, minoh_flag
        nonlocal l_oh


        nonlocal str_list, soh_list, output_list, l_oh
        nonlocal str_list_list, soh_list_list, output_list_list


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

                if minoh_flag:

                    l_bestand_obj_list = {}
                    l_bestand = L_bestand()
                    l_artikel = L_artikel()
                    l_untergrup = L_untergrup()
                    for l_bestand.anz_anf_best, l_bestand.anz_eingang, l_bestand.anz_ausgang, l_bestand.val_anf_best, l_bestand.wert_eingang, l_bestand.wert_ausgang, l_bestand._recid, l_artikel.zwkum, l_artikel.anzverbrauch, l_artikel.bezeich, l_artikel.artnr, l_artikel.masseinheit, l_artikel.inhalt, l_artikel.traubensorte, l_artikel.lief_einheit, l_artikel.ek_letzter, l_artikel.ek_aktuell, l_artikel.vk_preis, l_artikel.min_bestand, l_artikel._recid, l_untergrup.bezeich, l_untergrup.zwkum, l_untergrup._recid in db_session.query(L_bestand.anz_anf_best, L_bestand.anz_eingang, L_bestand.anz_ausgang, L_bestand.val_anf_best, L_bestand.wert_eingang, L_bestand.wert_ausgang, L_bestand._recid, L_artikel.zwkum, L_artikel.anzverbrauch, L_artikel.bezeich, L_artikel.artnr, L_artikel.masseinheit, L_artikel.inhalt, L_artikel.traubensorte, L_artikel.lief_einheit, L_artikel.ek_letzter, L_artikel.ek_aktuell, L_artikel.vk_preis, L_artikel.min_bestand, L_artikel._recid, L_untergrup.bezeich, L_untergrup.zwkum, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_bestand.artnr) & (L_artikel.zwkum == sub_grp) & (L_artikel.min_bestand > 0)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum) & ((L_untergrup.betriebsnr >= grp1) & (L_untergrup.betriebsnr <= grp2))).filter(
                                 (L_bestand.lager_nr == 0)).order_by(L_artikel.zwkum, L_artikel.artnr).all():
                        if l_bestand_obj_list.get(l_bestand._recid):
                            continue
                        else:
                            l_bestand_obj_list[l_bestand._recid] = True


                        curr_best =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)

                        if curr_best < l_artikel.min_bestand:
                            create_lines_global_oh()
                else:

                    l_bestand_obj_list = {}
                    l_bestand = L_bestand()
                    l_artikel = L_artikel()
                    l_untergrup = L_untergrup()
                    for l_bestand.anz_anf_best, l_bestand.anz_eingang, l_bestand.anz_ausgang, l_bestand.val_anf_best, l_bestand.wert_eingang, l_bestand.wert_ausgang, l_bestand._recid, l_artikel.zwkum, l_artikel.anzverbrauch, l_artikel.bezeich, l_artikel.artnr, l_artikel.masseinheit, l_artikel.inhalt, l_artikel.traubensorte, l_artikel.lief_einheit, l_artikel.ek_letzter, l_artikel.ek_aktuell, l_artikel.vk_preis, l_artikel.min_bestand, l_artikel._recid, l_untergrup.bezeich, l_untergrup.zwkum, l_untergrup._recid in db_session.query(L_bestand.anz_anf_best, L_bestand.anz_eingang, L_bestand.anz_ausgang, L_bestand.val_anf_best, L_bestand.wert_eingang, L_bestand.wert_ausgang, L_bestand._recid, L_artikel.zwkum, L_artikel.anzverbrauch, L_artikel.bezeich, L_artikel.artnr, L_artikel.masseinheit, L_artikel.inhalt, L_artikel.traubensorte, L_artikel.lief_einheit, L_artikel.ek_letzter, L_artikel.ek_aktuell, L_artikel.vk_preis, L_artikel.min_bestand, L_artikel._recid, L_untergrup.bezeich, L_untergrup.zwkum, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_bestand.artnr) & (L_artikel.zwkum == sub_grp)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum) & ((L_untergrup.betriebsnr >= grp1) & (L_untergrup.betriebsnr <= grp2))).filter(
                                 (L_bestand.lager_nr == 0)).order_by(L_artikel.zwkum, L_artikel.artnr).all():
                        if l_bestand_obj_list.get(l_bestand._recid):
                            continue
                        else:
                            l_bestand_obj_list[l_bestand._recid] = True


                        create_lines_global_oh()
            else:

                if minoh_flag:

                    l_bestand_obj_list = {}
                    l_bestand = L_bestand()
                    l_artikel = L_artikel()
                    l_untergrup = L_untergrup()
                    for l_bestand.anz_anf_best, l_bestand.anz_eingang, l_bestand.anz_ausgang, l_bestand.val_anf_best, l_bestand.wert_eingang, l_bestand.wert_ausgang, l_bestand._recid, l_artikel.zwkum, l_artikel.anzverbrauch, l_artikel.bezeich, l_artikel.artnr, l_artikel.masseinheit, l_artikel.inhalt, l_artikel.traubensorte, l_artikel.lief_einheit, l_artikel.ek_letzter, l_artikel.ek_aktuell, l_artikel.vk_preis, l_artikel.min_bestand, l_artikel._recid, l_untergrup.bezeich, l_untergrup.zwkum, l_untergrup._recid in db_session.query(L_bestand.anz_anf_best, L_bestand.anz_eingang, L_bestand.anz_ausgang, L_bestand.val_anf_best, L_bestand.wert_eingang, L_bestand.wert_ausgang, L_bestand._recid, L_artikel.zwkum, L_artikel.anzverbrauch, L_artikel.bezeich, L_artikel.artnr, L_artikel.masseinheit, L_artikel.inhalt, L_artikel.traubensorte, L_artikel.lief_einheit, L_artikel.ek_letzter, L_artikel.ek_aktuell, L_artikel.vk_preis, L_artikel.min_bestand, L_artikel._recid, L_untergrup.bezeich, L_untergrup.zwkum, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_bestand.artnr) & (L_artikel.endkum == from_grp) & (L_artikel.min_bestand > 0)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum) & ((L_untergrup.betriebsnr >= grp1) & (L_untergrup.betriebsnr <= grp2))).filter(
                                 (L_bestand.lager_nr == 0)).order_by(L_artikel.zwkum, L_artikel.artnr).all():
                        if l_bestand_obj_list.get(l_bestand._recid):
                            continue
                        else:
                            l_bestand_obj_list[l_bestand._recid] = True


                        curr_best =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)

                        if curr_best < l_artikel.min_bestand:
                            create_lines_global_oh()
                else:

                    l_bestand_obj_list = {}
                    l_bestand = L_bestand()
                    l_artikel = L_artikel()
                    l_untergrup = L_untergrup()
                    for l_bestand.anz_anf_best, l_bestand.anz_eingang, l_bestand.anz_ausgang, l_bestand.val_anf_best, l_bestand.wert_eingang, l_bestand.wert_ausgang, l_bestand._recid, l_artikel.zwkum, l_artikel.anzverbrauch, l_artikel.bezeich, l_artikel.artnr, l_artikel.masseinheit, l_artikel.inhalt, l_artikel.traubensorte, l_artikel.lief_einheit, l_artikel.ek_letzter, l_artikel.ek_aktuell, l_artikel.vk_preis, l_artikel.min_bestand, l_artikel._recid, l_untergrup.bezeich, l_untergrup.zwkum, l_untergrup._recid in db_session.query(L_bestand.anz_anf_best, L_bestand.anz_eingang, L_bestand.anz_ausgang, L_bestand.val_anf_best, L_bestand.wert_eingang, L_bestand.wert_ausgang, L_bestand._recid, L_artikel.zwkum, L_artikel.anzverbrauch, L_artikel.bezeich, L_artikel.artnr, L_artikel.masseinheit, L_artikel.inhalt, L_artikel.traubensorte, L_artikel.lief_einheit, L_artikel.ek_letzter, L_artikel.ek_aktuell, L_artikel.vk_preis, L_artikel.min_bestand, L_artikel._recid, L_untergrup.bezeich, L_untergrup.zwkum, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_bestand.artnr) & (L_artikel.endkum == from_grp)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum) & ((L_untergrup.betriebsnr >= grp1) & (L_untergrup.betriebsnr <= grp2))).filter(
                                 (L_bestand.lager_nr == 0)).order_by(L_artikel.zwkum, L_artikel.artnr).all():
                        if l_bestand_obj_list.get(l_bestand._recid):
                            continue
                        else:
                            l_bestand_obj_list[l_bestand._recid] = True


                        create_lines_global_oh()

        elif sorttype == 2:

            if sub_grp != 000:

                if minoh_flag:

                    l_bestand_obj_list = {}
                    l_bestand = L_bestand()
                    l_artikel = L_artikel()
                    l_untergrup = L_untergrup()
                    for l_bestand.anz_anf_best, l_bestand.anz_eingang, l_bestand.anz_ausgang, l_bestand.val_anf_best, l_bestand.wert_eingang, l_bestand.wert_ausgang, l_bestand._recid, l_artikel.zwkum, l_artikel.anzverbrauch, l_artikel.bezeich, l_artikel.artnr, l_artikel.masseinheit, l_artikel.inhalt, l_artikel.traubensorte, l_artikel.lief_einheit, l_artikel.ek_letzter, l_artikel.ek_aktuell, l_artikel.vk_preis, l_artikel.min_bestand, l_artikel._recid, l_untergrup.bezeich, l_untergrup.zwkum, l_untergrup._recid in db_session.query(L_bestand.anz_anf_best, L_bestand.anz_eingang, L_bestand.anz_ausgang, L_bestand.val_anf_best, L_bestand.wert_eingang, L_bestand.wert_ausgang, L_bestand._recid, L_artikel.zwkum, L_artikel.anzverbrauch, L_artikel.bezeich, L_artikel.artnr, L_artikel.masseinheit, L_artikel.inhalt, L_artikel.traubensorte, L_artikel.lief_einheit, L_artikel.ek_letzter, L_artikel.ek_aktuell, L_artikel.vk_preis, L_artikel.min_bestand, L_artikel._recid, L_untergrup.bezeich, L_untergrup.zwkum, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_bestand.artnr) & (L_artikel.zwkum == sub_grp) & (L_artikel.min_bestand > 0)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum) & ((L_untergrup.betriebsnr >= grp1) & (L_untergrup.betriebsnr <= grp2))).filter(
                                 (L_bestand.lager_nr == 0)).order_by(L_artikel.zwkum, L_artikel.bezeich).all():
                        if l_bestand_obj_list.get(l_bestand._recid):
                            continue
                        else:
                            l_bestand_obj_list[l_bestand._recid] = True


                        curr_best =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)

                        if curr_best < l_artikel.min_bestand:
                            create_lines_global_oh()
                else:

                    l_bestand_obj_list = {}
                    l_bestand = L_bestand()
                    l_artikel = L_artikel()
                    l_untergrup = L_untergrup()
                    for l_bestand.anz_anf_best, l_bestand.anz_eingang, l_bestand.anz_ausgang, l_bestand.val_anf_best, l_bestand.wert_eingang, l_bestand.wert_ausgang, l_bestand._recid, l_artikel.zwkum, l_artikel.anzverbrauch, l_artikel.bezeich, l_artikel.artnr, l_artikel.masseinheit, l_artikel.inhalt, l_artikel.traubensorte, l_artikel.lief_einheit, l_artikel.ek_letzter, l_artikel.ek_aktuell, l_artikel.vk_preis, l_artikel.min_bestand, l_artikel._recid, l_untergrup.bezeich, l_untergrup.zwkum, l_untergrup._recid in db_session.query(L_bestand.anz_anf_best, L_bestand.anz_eingang, L_bestand.anz_ausgang, L_bestand.val_anf_best, L_bestand.wert_eingang, L_bestand.wert_ausgang, L_bestand._recid, L_artikel.zwkum, L_artikel.anzverbrauch, L_artikel.bezeich, L_artikel.artnr, L_artikel.masseinheit, L_artikel.inhalt, L_artikel.traubensorte, L_artikel.lief_einheit, L_artikel.ek_letzter, L_artikel.ek_aktuell, L_artikel.vk_preis, L_artikel.min_bestand, L_artikel._recid, L_untergrup.bezeich, L_untergrup.zwkum, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_bestand.artnr) & (L_artikel.zwkum == sub_grp)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum) & ((L_untergrup.betriebsnr >= grp1) & (L_untergrup.betriebsnr <= grp2))).filter(
                                 (L_bestand.lager_nr == 0)).order_by(L_artikel.zwkum, L_artikel.bezeich).all():
                        if l_bestand_obj_list.get(l_bestand._recid):
                            continue
                        else:
                            l_bestand_obj_list[l_bestand._recid] = True


                        create_lines_global_oh()
            else:

                if minoh_flag:

                    l_bestand_obj_list = {}
                    l_bestand = L_bestand()
                    l_artikel = L_artikel()
                    l_untergrup = L_untergrup()
                    for l_bestand.anz_anf_best, l_bestand.anz_eingang, l_bestand.anz_ausgang, l_bestand.val_anf_best, l_bestand.wert_eingang, l_bestand.wert_ausgang, l_bestand._recid, l_artikel.zwkum, l_artikel.anzverbrauch, l_artikel.bezeich, l_artikel.artnr, l_artikel.masseinheit, l_artikel.inhalt, l_artikel.traubensorte, l_artikel.lief_einheit, l_artikel.ek_letzter, l_artikel.ek_aktuell, l_artikel.vk_preis, l_artikel.min_bestand, l_artikel._recid, l_untergrup.bezeich, l_untergrup.zwkum, l_untergrup._recid in db_session.query(L_bestand.anz_anf_best, L_bestand.anz_eingang, L_bestand.anz_ausgang, L_bestand.val_anf_best, L_bestand.wert_eingang, L_bestand.wert_ausgang, L_bestand._recid, L_artikel.zwkum, L_artikel.anzverbrauch, L_artikel.bezeich, L_artikel.artnr, L_artikel.masseinheit, L_artikel.inhalt, L_artikel.traubensorte, L_artikel.lief_einheit, L_artikel.ek_letzter, L_artikel.ek_aktuell, L_artikel.vk_preis, L_artikel.min_bestand, L_artikel._recid, L_untergrup.bezeich, L_untergrup.zwkum, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_bestand.artnr) & (L_artikel.endkum == from_grp) & (L_artikel.min_bestand > 0)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum) & ((L_untergrup.betriebsnr >= grp1) & (L_untergrup.betriebsnr <= grp2))).filter(
                                 (L_bestand.lager_nr == 0)).order_by(L_artikel.zwkum, L_artikel.bezeich).all():
                        if l_bestand_obj_list.get(l_bestand._recid):
                            continue
                        else:
                            l_bestand_obj_list[l_bestand._recid] = True


                        curr_best =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)

                        if curr_best < l_artikel.min_bestand:
                            create_lines_global_oh()
                else:

                    l_bestand_obj_list = {}
                    l_bestand = L_bestand()
                    l_artikel = L_artikel()
                    l_untergrup = L_untergrup()
                    for l_bestand.anz_anf_best, l_bestand.anz_eingang, l_bestand.anz_ausgang, l_bestand.val_anf_best, l_bestand.wert_eingang, l_bestand.wert_ausgang, l_bestand._recid, l_artikel.zwkum, l_artikel.anzverbrauch, l_artikel.bezeich, l_artikel.artnr, l_artikel.masseinheit, l_artikel.inhalt, l_artikel.traubensorte, l_artikel.lief_einheit, l_artikel.ek_letzter, l_artikel.ek_aktuell, l_artikel.vk_preis, l_artikel.min_bestand, l_artikel._recid, l_untergrup.bezeich, l_untergrup.zwkum, l_untergrup._recid in db_session.query(L_bestand.anz_anf_best, L_bestand.anz_eingang, L_bestand.anz_ausgang, L_bestand.val_anf_best, L_bestand.wert_eingang, L_bestand.wert_ausgang, L_bestand._recid, L_artikel.zwkum, L_artikel.anzverbrauch, L_artikel.bezeich, L_artikel.artnr, L_artikel.masseinheit, L_artikel.inhalt, L_artikel.traubensorte, L_artikel.lief_einheit, L_artikel.ek_letzter, L_artikel.ek_aktuell, L_artikel.vk_preis, L_artikel.min_bestand, L_artikel._recid, L_untergrup.bezeich, L_untergrup.zwkum, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_bestand.artnr) & (L_artikel.endkum == from_grp)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum) & ((L_untergrup.betriebsnr >= grp1) & (L_untergrup.betriebsnr <= grp2))).filter(
                                 (L_bestand.lager_nr == 0)).order_by(L_artikel.zwkum, L_artikel.bezeich).all():
                        if l_bestand_obj_list.get(l_bestand._recid):
                            continue
                        else:
                            l_bestand_obj_list[l_bestand._recid] = True


                        create_lines_global_oh()

        if t_val != 0:
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.flag = 1
            output_list.bezeich = bezeich
            output_list.act_val =  to_decimal(t_val)


            output_list = Output_list()
            output_list_list.append(output_list)


        if tt_val != 0:
            pass
        output_list = Output_list()
        output_list_list.append(output_list)

        output_list.flag = 1
        output_list.bezeich = "GRAND T O T A L"
        output_list.act_val =  to_decimal(tt_value)


    def create_lines():

        nonlocal soh_list_list, curr_best, long_digit, i, j, tot_anz, tot_val, t_anz, t_val, t_value, tt_value, avrg_price, zwkum, bezeich, grp1, grp2, must_order, tt_val, qty, wert, tot_bezeich, l_bestand, htparam, l_lager, l_artikel, l_untergrup
        nonlocal all_flag, show_price, zero_flag, from_grp, sub_grp, from_lager, to_lager, sorttype, mattype, minoh_flag
        nonlocal l_oh


        nonlocal str_list, soh_list, output_list, l_oh
        nonlocal str_list_list, soh_list_list, output_list_list

        tmp_str:string = ""
        i = i + 1
        must_order =  to_decimal("0")

        if i == 1:
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.bezeich = " " + to_string(l_lager.lager_nr, "99") + " " + to_string(l_lager.bezeich, "x(50)")

        if zwkum == 0:
            zwkum = l_artikel.zwkum
            bezeich = l_untergrup.bezeich

        if zwkum != l_artikel.zwkum:
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.flag = 1
            output_list.bezeich = bezeich
            output_list.act_val =  to_decimal(t_val)


            output_list = Output_list()
            output_list_list.append(output_list)

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

        if length(l_artikel.bezeich) > 50 or length(l_artikel.bezeich) >= 50:
            tmp_str = l_artikel.bezeich
        else:
            tmp_str = to_string(l_artikel.bezeich) + " "

        if tot_anz != 0 or (tot_anz == 0 and zero_flag):

            if show_price:

                if not long_digit:
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.artnr = l_artikel.artnr
                    output_list.bezeich = substring(to_string(tmp_str) , 0, 50)
                    output_list.unit = l_artikel.masseinheit
                    output_list.act_qty =  to_decimal(tot_anz)
                    output_list.act_val =  to_decimal(tot_val)
                    output_list.cont1 = to_string(l_artikel.inhalt, ">>,>>9.99")
                    output_list.d_unit = to_string(l_artikel.traubensorte, "x(8)")
                    output_list.cont2 = to_string(l_artikel.lief_einheit, ">>,>>9.99")
                    output_list.last_price =  to_decimal(l_artikel.ek_letzter)
                    output_list.act_price =  to_decimal(l_artikel.ek_aktuell)
                    output_list.avrg_price =  to_decimal(l_artikel.vk_preis)
                    output_list.min_oh =  to_decimal(l_artikel.min_bestand)
                    output_list.must_order =  to_decimal(must_order)


                else:
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.artnr = l_artikel.artnr
                    output_list.bezeich = substring(to_string(tmp_str) , 0, 50)
                    output_list.unit = l_artikel.masseinheit
                    output_list.act_qty =  to_decimal(tot_anz)
                    output_list.act_val =  to_decimal(tot_val)
                    output_list.cont1 = to_string(l_artikel.inhalt, ">>,>>9.99")
                    output_list.d_unit = to_string(l_artikel.traubensorte, "x(8)")
                    output_list.cont2 = to_string(l_artikel.lief_einheit, ">>,>>9.99")
                    output_list.last_price =  to_decimal(l_artikel.ek_letzter)
                    output_list.act_price =  to_decimal(l_artikel.ek_aktuell)
                    output_list.avrg_price =  to_decimal(l_artikel.vk_preis)
                    output_list.min_oh =  to_decimal(l_artikel.min_bestand)
                    output_list.must_order =  to_decimal(must_order)


            else:

                if not long_digit:
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.artnr = l_artikel.artnr
                    output_list.bezeich = substring(to_string(tmp_str) , 0, 50)
                    output_list.unit = l_artikel.masseinheit
                    output_list.act_qty =  to_decimal(tot_anz)
                    output_list.act_val =  to_decimal("0")
                    output_list.cont1 = to_string(l_artikel.inhalt, ">>,>>9.99")
                    output_list.d_unit = to_string(l_artikel.traubensorte, "x(8)")
                    output_list.cont2 = to_string(l_artikel.lief_einheit, ">>,>>9.99")
                    output_list.last_price =  to_decimal("0")
                    output_list.act_price =  to_decimal("0")
                    output_list.avrg_price =  to_decimal("0")
                    output_list.min_oh =  to_decimal(l_artikel.min_bestand)
                    output_list.must_order =  to_decimal(must_order)


                else:
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.artnr = l_artikel.artnr
                    output_list.bezeich = substring(to_string(tmp_str) , 0, 50)
                    output_list.unit = l_artikel.masseinheit
                    output_list.act_qty =  to_decimal(tot_anz)
                    output_list.act_val =  to_decimal("0")
                    output_list.cont1 = to_string(l_artikel.inhalt, ">>,>>9.99")
                    output_list.d_unit = to_string(l_artikel.traubensorte, "x(8)")
                    output_list.cont2 = to_string(l_artikel.lief_einheit, ">>,>>9.99")
                    output_list.last_price =  to_decimal("0")
                    output_list.act_price =  to_decimal("0")
                    output_list.avrg_price =  to_decimal("0")
                    output_list.min_oh =  to_decimal(l_artikel.min_bestand)
                    output_list.must_order =  to_decimal(must_order)


    def create_lines_global_oh():

        nonlocal soh_list_list, curr_best, long_digit, i, j, tot_anz, tot_val, t_anz, t_val, t_value, tt_value, avrg_price, zwkum, bezeich, grp1, grp2, must_order, tt_val, qty, wert, tot_bezeich, l_bestand, htparam, l_lager, l_artikel, l_untergrup
        nonlocal all_flag, show_price, zero_flag, from_grp, sub_grp, from_lager, to_lager, sorttype, mattype, minoh_flag
        nonlocal l_oh


        nonlocal str_list, soh_list, output_list, l_oh
        nonlocal str_list_list, soh_list_list, output_list_list

        tmp_str:string = ""
        i = i + 1
        must_order =  to_decimal("0")

        if zwkum == 0:
            zwkum = l_artikel.zwkum
            bezeich = l_untergrup.bezeich

        if zwkum != l_artikel.zwkum:
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.flag = 1
            output_list.bezeich = bezeich
            output_list.act_val =  to_decimal(t_val)


            output_list = Output_list()
            output_list_list.append(output_list)

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

        if length(l_artikel.bezeich) > 50 or length(l_artikel.bezeich) >= 50:
            tmp_str = l_artikel.bezeich
        else:
            tmp_str = to_string(l_artikel.bezeich) + " "

        if tot_anz != 0 or (tot_anz == 0 and zero_flag):

            if show_price:

                if not long_digit:
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.artnr = l_artikel.artnr
                    output_list.bezeich = substring(to_string(tmp_str) , 0, 50)
                    output_list.unit = l_artikel.masseinheit
                    output_list.act_qty =  to_decimal(tot_anz)
                    output_list.act_val =  to_decimal(tot_val)
                    output_list.cont1 = to_string(l_artikel.inhalt, ">>,>>9.99")
                    output_list.d_unit = to_string(l_artikel.traubensorte, "x(8)")
                    output_list.cont2 = to_string(l_artikel.lief_einheit, ">>,>>9.99")
                    output_list.last_price =  to_decimal(l_artikel.ek_letzter)
                    output_list.act_price =  to_decimal(l_artikel.ek_aktuell)
                    output_list.avrg_price =  to_decimal(l_artikel.vk_preis)
                    output_list.min_oh =  to_decimal(l_artikel.min_bestand)
                    output_list.must_order =  to_decimal(must_order)


                else:
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.artnr = l_artikel.artnr
                    output_list.bezeich = substring(to_string(tmp_str) , 0, 50)
                    output_list.unit = l_artikel.masseinheit
                    output_list.act_qty =  to_decimal(tot_anz)
                    output_list.act_val =  to_decimal(tot_val)
                    output_list.cont1 = to_string(l_artikel.inhalt, ">>,>>9.99")
                    output_list.d_unit = to_string(l_artikel.traubensorte, "x(8)")
                    output_list.cont2 = to_string(l_artikel.lief_einheit, ">>,>>9.99")
                    output_list.last_price =  to_decimal(l_artikel.ek_letzter)
                    output_list.act_price =  to_decimal(l_artikel.ek_aktuell)
                    output_list.avrg_price =  to_decimal(l_artikel.vk_preis)
                    output_list.min_oh =  to_decimal(l_artikel.min_bestand)
                    output_list.must_order =  to_decimal(must_order)


            else:

                if not long_digit:
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.artnr = l_artikel.artnr
                    output_list.bezeich = substring(to_string(tmp_str) , 0, 50)
                    output_list.unit = l_artikel.masseinheit
                    output_list.act_qty =  to_decimal(tot_anz)
                    output_list.act_val =  to_decimal("0")
                    output_list.cont1 = to_string(l_artikel.inhalt, ">>,>>9.99")
                    output_list.d_unit = to_string(l_artikel.traubensorte, "x(8)")
                    output_list.cont2 = to_string(l_artikel.lief_einheit, ">>,>>9.99")
                    output_list.last_price =  to_decimal("0")
                    output_list.act_price =  to_decimal("0")
                    output_list.avrg_price =  to_decimal("0")
                    output_list.min_oh =  to_decimal(l_artikel.min_bestand)
                    output_list.must_order =  to_decimal(must_order)


                else:
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.artnr = l_artikel.artnr
                    output_list.bezeich = substring(to_string(tmp_str) , 0, 50)
                    output_list.unit = l_artikel.masseinheit
                    output_list.act_qty =  to_decimal(tot_anz)
                    output_list.act_val =  to_decimal("0")
                    output_list.cont1 = to_string(l_artikel.inhalt, ">>,>>9.99")
                    output_list.d_unit = to_string(l_artikel.traubensorte, "x(8)")
                    output_list.cont2 = to_string(l_artikel.lief_einheit, ">>,>>9.99")
                    output_list.last_price =  to_decimal("0")
                    output_list.act_price =  to_decimal("0")
                    output_list.avrg_price =  to_decimal("0")
                    output_list.min_oh =  to_decimal(l_artikel.min_bestand)
                    output_list.must_order =  to_decimal(must_order)


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
    soh_list_list.clear()

    for output_list in query(output_list_list):
        soh_list = Soh_list()
        soh_list_list.append(soh_list)

        soh_list.artnr = output_list.artnr
        soh_list.bezeich = output_list.bezeich
        soh_list.unit = output_list.unit
        soh_list.act_qty =  to_decimal(output_list.act_qty)
        soh_list.act_val =  to_decimal(output_list.act_val)
        soh_list.cont1 = output_list.cont1
        soh_list.d_unit = output_list.d_unit
        soh_list.cont2 = output_list.cont2
        soh_list.last_price =  to_decimal(output_list.last_price)
        soh_list.act_price =  to_decimal(output_list.act_price)
        soh_list.avrg_price =  to_decimal(output_list.avrg_price)
        soh_list.min_oh =  to_decimal(output_list.min_oh)
        soh_list.must_order =  to_decimal(output_list.must_order)

    return generate_output()