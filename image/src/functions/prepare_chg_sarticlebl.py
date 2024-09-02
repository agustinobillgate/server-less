from functions.additional_functions import *
import decimal
import re
from models import L_artikel, Guestbook, L_bestand, L_ophis, Htparam, H_rezept, L_lieferant, L_untergrup, L_hauptgrp, Queasy

def prepare_chg_sarticlebl(artnr:int, changed:bool):
    fibukonto = ""
    dml_art = False
    bez_aend = False
    s_unit = ""
    tt_artnr_list = []
    tt_content_list = []
    tt_bezeich_list = []
    pict_file = ""
    recipe_bez = ""
    firma1 = ""
    firma2 = ""
    firma3 = ""
    zw_bezeich = ""
    end_bezeich = ""
    set_disp1 = False
    set_disp2 = False
    set_disp3 = False
    set_disp4 = False
    artnr_ok = False
    l_art_list = []
    t_l_art_list = []
    ttguestbook_list = []
    ss_artnr:[int] = [0, 0, 0, 0]
    ss_content:[int] = [0, 0, 0, 0]
    ss_bezeich:[str] = ["", "", "", ""]
    i_counter:int = 0
    strartnr:str = ""
    lp_price:int = 0
    l_artikel = guestbook = l_bestand = l_ophis = htparam = h_rezept = l_lieferant = l_untergrup = l_hauptgrp = queasy = None

    l_art = t_l_art = tt_artnr = tt_content = tt_bezeich = ttguestbook = lbuff = l_art1 = None

    l_art_list, L_art = create_model_like(L_artikel)
    t_l_art_list, T_l_art = create_model("T_l_art", {"artnr":int, "endkum":int, "zwkum":int, "t_recid":int})
    tt_artnr_list, Tt_artnr = create_model("Tt_artnr", {"curr_i":int, "ss_artnr":int})
    tt_content_list, Tt_content = create_model("Tt_content", {"curr_i":int, "ss_content":int})
    tt_bezeich_list, Tt_bezeich = create_model("Tt_bezeich", {"curr_i":int, "ss_bezeich":str})
    ttguestbook_list, Ttguestbook = create_model_like(Guestbook)

    Lbuff = L_artikel
    L_art1 = L_artikel

    db_session = local_storage.db_session

    def generate_output():
        nonlocal fibukonto, dml_art, bez_aend, s_unit, tt_artnr_list, tt_content_list, tt_bezeich_list, pict_file, recipe_bez, firma1, firma2, firma3, zw_bezeich, end_bezeich, set_disp1, set_disp2, set_disp3, set_disp4, artnr_ok, l_art_list, t_l_art_list, ttguestbook_list, ss_artnr, ss_content, ss_bezeich, i_counter, strartnr, lp_price, l_artikel, guestbook, l_bestand, l_ophis, htparam, h_rezept, l_lieferant, l_untergrup, l_hauptgrp, queasy
        nonlocal lbuff, l_art1


        nonlocal l_art, t_l_art, tt_artnr, tt_content, tt_bezeich, ttguestbook, lbuff, l_art1
        nonlocal l_art_list, t_l_art_list, tt_artnr_list, tt_content_list, tt_bezeich_list, ttguestbook_list
        return {"fibukonto": fibukonto, "dml_art": dml_art, "bez_aend": bez_aend, "s_unit": s_unit, "tt-artnr": tt_artnr_list, "tt-content": tt_content_list, "tt-bezeich": tt_bezeich_list, "pict_file": pict_file, "recipe_bez": recipe_bez, "firma1": firma1, "firma2": firma2, "firma3": firma3, "zw_bezeich": zw_bezeich, "end_bezeich": end_bezeich, "set_disp1": set_disp1, "set_disp2": set_disp2, "set_disp3": set_disp3, "set_disp4": set_disp4, "artnr_ok": artnr_ok, "l-art": l_art_list, "t-l-art": t_l_art_list, "ttGuestBook": ttguestbook_list}

    def check_artno():

        nonlocal fibukonto, dml_art, bez_aend, s_unit, tt_artnr_list, tt_content_list, tt_bezeich_list, pict_file, recipe_bez, firma1, firma2, firma3, zw_bezeich, end_bezeich, set_disp1, set_disp2, set_disp3, set_disp4, artnr_ok, l_art_list, t_l_art_list, ttguestbook_list, ss_artnr, ss_content, ss_bezeich, i_counter, strartnr, lp_price, l_artikel, guestbook, l_bestand, l_ophis, htparam, h_rezept, l_lieferant, l_untergrup, l_hauptgrp, queasy
        nonlocal lbuff, l_art1


        nonlocal l_art, t_l_art, tt_artnr, tt_content, tt_bezeich, ttguestbook, lbuff, l_art1
        nonlocal l_art_list, t_l_art_list, tt_artnr_list, tt_content_list, tt_bezeich_list, ttguestbook_list

        its_ok = False
        nr:int = 0
        s:str = ""

        def generate_inner_output():
            return its_ok

        if l_art.zwkum > 99:
            nr = l_art.endkum * 1000 + l_art.zwkum
        else:
            nr = l_art.endkum * 100 + l_art.zwkum

        if nr > 999:
            s = substring(to_string(l_art.artnr) , 0, 4)
        else:
            s = substring(to_string(l_art.artnr) , 0, 3)
        its_ok = (s == to_string(nr))


        return generate_inner_output()

    def fill_lart():

        nonlocal fibukonto, dml_art, bez_aend, s_unit, tt_artnr_list, tt_content_list, tt_bezeich_list, pict_file, recipe_bez, firma1, firma2, firma3, zw_bezeich, end_bezeich, set_disp1, set_disp2, set_disp3, set_disp4, artnr_ok, l_art_list, t_l_art_list, ttguestbook_list, ss_artnr, ss_content, ss_bezeich, i_counter, strartnr, lp_price, l_artikel, guestbook, l_bestand, l_ophis, htparam, h_rezept, l_lieferant, l_untergrup, l_hauptgrp, queasy
        nonlocal lbuff, l_art1


        nonlocal l_art, t_l_art, tt_artnr, tt_content, tt_bezeich, ttguestbook, lbuff, l_art1
        nonlocal l_art_list, t_l_art_list, tt_artnr_list, tt_content_list, tt_bezeich_list, ttguestbook_list


        L_art1 = L_artikel
        dml_art = l_artikel.bestellt

        if l_artikel.jahrgang == 0:
            bez_aend = False
        else:
            bez_aend = True
        l_art.artnr = l_artikel.artnr
        l_art.fibukonto = l_artikel.fibukonto
        l_art.bezeich = l_artikel.bezeich
        l_art.zwkum = l_artikel.zwkum
        l_art.endkum = l_artikel.endkum
        l_art.herkunft = entry(0, l_artikel.herkunft, ";")
        s_unit = entry(1, l_artikel.herkunft, ";")
        l_art.masseinheit = l_artikel.masseinheit
        l_art.betriebsnr = l_artikel.betriebsnr
        l_art.inhalt = l_artikel.inhalt
        l_art.traubensort = l_artikel.traubensort
        l_art.lief_einheit = l_artikel.lief_einheit
        l_art.min_bestand = l_artikel.min_bestand
        l_art.anzverbrauch = l_artikel.anzverbrauch
        l_art.alkoholgrad = l_artikel.alkoholgrad
        l_art.lief_nr1 = l_artikel.lief_nr1
        l_art.lief_artnr[0] = l_artikel.lief_artnr[1]
        l_art.lief_nr2 = l_artikel.lief_nr2
        l_art.lief_artnr[1] = l_artikel.lief_artnr[1]
        l_art.lief_nr3 = l_artikel.lief_nr3
        l_art.lief_artnr[2] = l_artikel.lief_artnr[2]
        l_art.ek_aktuell = l_artikel.ek_aktuell
        l_art.ek_letzter = l_artikel.ek_letzter
        l_art.vk_preis = l_artikel.vk_preis

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 20) &  (Queasy.number1 == l_artikel.artnr)).first()

        if queasy:
            ss_artnr[0] = to_int(queasy.deci1)
            ss_artnr[1] = to_int(queasy.deci2)
            ss_artnr[2] = to_int(queasy.deci3)

            if len(queasy.char3) == 12:
                ss_content[0] = to_int(substring(queasy.char3, 0, 3))
                ss_content[1] = to_int(substring(queasy.char3, 4, 3))
                ss_content[2] = to_int(substring(queasy.char3, 8, 3))


            else:
                ss_content[0] = to_int(substring(queasy.char2, 0, 3))
                ss_content[1] = to_int(substring(queasy.char2, 4, 3))
                ss_content[2] = to_int(substring(queasy.char2, 8, 3))
                pict_file = queasy.char3


            for i_counter in range(1,3 + 1) :
                tt_artnr = Tt_artnr()
                tt_artnr_list.append(tt_artnr)

                tt_artnr.curr_i = i_counter
                tt_artnr.ss_artnr = ss_artnr[i_counter - 1]


            for i_counter in range(1,3 + 1) :
                tt_content = Tt_content()
                tt_content_list.append(tt_content)

                tt_content.curr_i = i_counter
                tt_content.ss_content = ss_content[i_counter - 1]


            for i_counter in range(1,3 + 1) :
                tt_bezeich = Tt_bezeich()
                tt_bezeich_list.append(tt_bezeich)

                tt_bezeich.curr_i = i_counter
                tt_bezeich.ss_bezeich = ss_bezeich[i_counter - 1]

            if ss_artnr[0] != 0:

                l_art1 = db_session.query(L_art1).filter(
                        (L_art1.artnr == ss_artnr[0])).first()

                if l_art1:
                    ss_bezeich[0] = l_art1.bezeich

            if ss_artnr[1] != 0:

                l_art1 = db_session.query(L_art1).filter(
                        (L_art1.artnr == ss_artnr[1])).first()

                if l_art1:
                    ss_bezeich[1] = l_art1.bezeich

            if ss_artnr[2] != 0:

                l_art1 = db_session.query(L_art1).filter(
                        (L_art1.artnr == ss_artnr[2])).first()

                if l_art1:
                    ss_bezeich[2] = l_art1.bezeich


    l_artikel = db_session.query(L_artikel).filter(
            (L_artikel.artnr == artnr)).first()

    if not l_artikel:

        return generate_output()
    fibukonto = l_artikel.fibukonto

    if l_artikel.fibukonto == "":
        fibukonto = "00000000000000000000"

    if not re.match(".*;.*",l_artikel.herkunft):

        lbuff = db_session.query(Lbuff).filter(
                (Lbuff._recid == l_artikel._recid)).first()
        lbuff.herkunft = lbuff.herkunft + ";"

        lbuff = db_session.query(Lbuff).first()
    strartnr = "*" + to_string(artnr) + "*"

    guestbook = db_session.query(Guestbook).filter(
            (Guestbook.infostr.op("~")(strartnr))).first()

    if guestbook:
        ttguestbook = Ttguestbook()
        ttguestbook_list.append(ttguestbook)

        buffer_copy(guestbook, ttguestbook)
    l_art = L_art()
    l_art_list.append(l_art)

    fill_lart()

    if changed:

        l_bestand = db_session.query(L_bestand).filter(
                (L_bestand.artnr == artnr) &  (L_bestand.lager_nr == 0)).first()

        if l_bestand:
            set_disp1 = True

        if l_art.vk_preis != 0:
            set_disp2 = True

        l_ophis = db_session.query(L_ophis).filter(
                (L_ophis.artnr == artnr)).first()

        if l_ophis:
            set_disp3 = True
        artnr_ok = check_artno()
    else:

        l_artikel = db_session.query(L_artikel).filter(
                (L_artikel.artnr == artnr)).first()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 911)).first()

    if htparam.paramgruppe == 21 and htparam.flogical:
        set_disp4 = True

    if l_artikel.betriebsnr != 0:

        h_rezept = db_session.query(H_rezept).filter(
                (H_rezept.artnrrezept == l_artikel.betriebsnr)).first()

        if h_rezept:
            recipe_bez = h_rezept.bezeich

    if l_art.lief_nr1 != 0:

        l_lieferant = db_session.query(L_lieferant).filter(
                (L_lieferant.lief_nr == l_art.lief_nr1)).first()

        if l_lieferant:
            firma1 = l_lieferant.firma

    if l_art.lief_nr2 != 0:

        l_lieferant = db_session.query(L_lieferant).filter(
                (L_lieferant.lief_nr == l_art.lief_nr2)).first()

        if l_lieferant:
            firma2 = l_lieferant.firma

    if l_art.lief_nr3 != 0:

        l_lieferant = db_session.query(L_lieferant).filter(
                (L_lieferant.lief_nr == l_art.lief_nr3)).first()

        if l_lieferant:
            firma3 = l_lieferant.firma

    if l_art.zwkum != 0:

        l_untergrup = db_session.query(L_untergrup).filter(
                (L_untergrup.zwkum == l_art.zwkum)).first()

        if l_untergrup:
            zw_bezeich = l_untergrup.bezeich

    if l_art.endkum != 0:

        l_hauptgrp = db_session.query(L_hauptgrp).filter(
                (L_hauptgrp.endkum == l_art.endkum)).first()

        if l_hauptgrp:
            end_bezeich = l_hauptgrp.bezeich
    t_l_art = T_l_art()
    t_l_art_list.append(t_l_art)

    buffer_copy(l_artikel, t_l_art)
    t_l_art.t_recid = l_artikel._recid

    return generate_output()