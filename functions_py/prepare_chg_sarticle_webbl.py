#using conversion tools version: 1.0.0.119

from functions.additional_functions import *
from decimal import Decimal
from sqlalchemy import func
from models import L_artikel, Guestbook, Htparam, L_bestand, L_ophis, H_rezept, L_lieferant, L_untergrup, L_hauptgrp, L_op, H_rezlin, Queasy

def prepare_chg_sarticle_webbl(artnr:int, changed:bool):

    prepare_cache ([L_artikel, Htparam, H_rezept, L_lieferant, L_untergrup, L_hauptgrp, Queasy])

    fibukonto = ""
    dml_art = False
    bez_aend = False
    s_unit = ""
    tt_artnr_data = []
    tt_content_data = []
    tt_bezeich_data = []
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
    param89 = False
    f_endkum = 0
    b_endkum = 0
    o_endkum = 0
    l_art_data = []
    t_l_art_data = []
    ttguestbook_data = []
    t_message_list_data = []
    ss_artnr:List[int] = [0, 0, 0]
    ss_content:List[int] = [0, 0, 0]
    ss_bezeich:List[string] = ["", "", ""]
    i_counter:int = 0
    strartnr:string = ""
    lp_price:int = 0
    count_lophis:int = 0
    count_lop:int = 0
    l_artikel = guestbook = htparam = l_bestand = l_ophis = h_rezept = l_lieferant = l_untergrup = l_hauptgrp = l_op = h_rezlin = queasy = None

    l_art = t_l_art = tt_artnr = tt_content = tt_bezeich = t_message_list = ttguestbook = lbuff = None

    l_art_data, L_art = create_model_like(L_artikel)
    t_l_art_data, T_l_art = create_model("T_l_art", {"artnr":int, "endkum":int, "zwkum":int, "t_recid":int})
    tt_artnr_data, Tt_artnr = create_model("Tt_artnr", {"curr_i":int, "ss_artnr":int})
    tt_content_data, Tt_content = create_model("Tt_content", {"curr_i":int, "ss_content":int})
    tt_bezeich_data, Tt_bezeich = create_model("Tt_bezeich", {"curr_i":int, "ss_bezeich":string})
    t_message_list_data, T_message_list = create_model("T_message_list", {"lock_flag1":bool, "lock_flag2":bool})
    ttguestbook_data, Ttguestbook = create_model_like(Guestbook)

    Lbuff = create_buffer("Lbuff",L_artikel)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal fibukonto, dml_art, bez_aend, s_unit, tt_artnr_data, tt_content_data, tt_bezeich_data, pict_file, recipe_bez, firma1, firma2, firma3, zw_bezeich, end_bezeich, set_disp1, set_disp2, set_disp3, set_disp4, artnr_ok, param89, f_endkum, b_endkum, o_endkum, l_art_data, t_l_art_data, ttguestbook_data, t_message_list_data, ss_artnr, ss_content, ss_bezeich, i_counter, strartnr, lp_price, count_lophis, count_lop, l_artikel, guestbook, htparam, l_bestand, l_ophis, h_rezept, l_lieferant, l_untergrup, l_hauptgrp, l_op, h_rezlin, queasy
        nonlocal artnr, changed
        nonlocal lbuff


        nonlocal l_art, t_l_art, tt_artnr, tt_content, tt_bezeich, t_message_list, ttguestbook, lbuff
        nonlocal l_art_data, t_l_art_data, tt_artnr_data, tt_content_data, tt_bezeich_data, t_message_list_data, ttguestbook_data

        return {"fibukonto": fibukonto, "dml_art": dml_art, "bez_aend": bez_aend, "s_unit": s_unit, "tt-artnr": tt_artnr_data, "tt-content": tt_content_data, "tt-bezeich": tt_bezeich_data, "pict_file": pict_file, "recipe_bez": recipe_bez, "firma1": firma1, "firma2": firma2, "firma3": firma3, "zw_bezeich": zw_bezeich, "end_bezeich": end_bezeich, "set_disp1": set_disp1, "set_disp2": set_disp2, "set_disp3": set_disp3, "set_disp4": set_disp4, "artnr_ok": artnr_ok, "param89": param89, "f_endkum": f_endkum, "b_endkum": b_endkum, "o_endkum": o_endkum, "l-art": l_art_data, "t-l-art": t_l_art_data, "ttGuestBook": ttguestbook_data, "t-message-list": t_message_list_data}

    def check_artno():

        nonlocal fibukonto, dml_art, bez_aend, s_unit, tt_artnr_data, tt_content_data, tt_bezeich_data, pict_file, recipe_bez, firma1, firma2, firma3, zw_bezeich, end_bezeich, set_disp1, set_disp2, set_disp3, set_disp4, artnr_ok, param89, f_endkum, b_endkum, o_endkum, l_art_data, t_l_art_data, ttguestbook_data, t_message_list_data, ss_artnr, ss_content, ss_bezeich, i_counter, strartnr, lp_price, count_lophis, count_lop, l_artikel, guestbook, htparam, l_bestand, l_ophis, h_rezept, l_lieferant, l_untergrup, l_hauptgrp, l_op, h_rezlin, queasy
        nonlocal artnr, changed
        nonlocal lbuff


        nonlocal l_art, t_l_art, tt_artnr, tt_content, tt_bezeich, t_message_list, ttguestbook, lbuff
        nonlocal l_art_data, t_l_art_data, tt_artnr_data, tt_content_data, tt_bezeich_data, t_message_list_data, ttguestbook_data

        its_ok = True
        nr:int = 0
        s:string = ""

        def generate_inner_output():
            return (its_ok)


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

        nonlocal fibukonto, dml_art, bez_aend, s_unit, tt_artnr_data, tt_content_data, tt_bezeich_data, pict_file, recipe_bez, firma1, firma2, firma3, zw_bezeich, end_bezeich, set_disp1, set_disp2, set_disp3, set_disp4, artnr_ok, param89, f_endkum, b_endkum, o_endkum, l_art_data, t_l_art_data, ttguestbook_data, t_message_list_data, ss_artnr, ss_content, ss_bezeich, i_counter, strartnr, lp_price, count_lophis, count_lop, l_artikel, guestbook, htparam, l_bestand, l_ophis, h_rezept, l_lieferant, l_untergrup, l_hauptgrp, l_op, h_rezlin, queasy
        nonlocal artnr, changed
        nonlocal lbuff


        nonlocal l_art, t_l_art, tt_artnr, tt_content, tt_bezeich, t_message_list, ttguestbook, lbuff
        nonlocal l_art_data, t_l_art_data, tt_artnr_data, tt_content_data, tt_bezeich_data, t_message_list_data, ttguestbook_data

        l_art1 = None
        L_art1 =  create_buffer("L_art1",L_artikel)
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
        l_art.inhalt =  to_decimal(l_artikel.inhalt)
        l_art.traubensorte = l_artikel.traubensorte
        l_art.lief_einheit =  to_decimal(l_artikel.lief_einheit)
        l_art.min_bestand =  to_decimal(l_artikel.min_bestand)
        l_art.anzverbrauch =  to_decimal(l_artikel.anzverbrauch)
        l_art.alkoholgrad =  to_decimal(l_artikel.alkoholgrad)
        l_art.lief_nr1 = l_artikel.lief_nr1
        l_art.lief_artnr[0] = l_artikel.lief_artnr[1]
        l_art.lief_nr2 = l_artikel.lief_nr2
        l_art.lief_artnr[1] = l_artikel.lief_artnr[1]
        l_art.lief_nr3 = l_artikel.lief_nr3
        l_art.lief_artnr[2] = l_artikel.lief_artnr[2]
        l_art.ek_aktuell =  to_decimal(l_artikel.ek_aktuell)
        l_art.ek_letzter =  to_decimal(l_artikel.ek_letzter)
        l_art.vk_preis =  to_decimal(l_artikel.vk_preis)

        queasy = get_cache (Queasy, {"key": [(eq, 20)],"number1": [(eq, l_artikel.artnr)]})

        if queasy:
            ss_artnr[0] = to_int(queasy.deci1)
            ss_artnr[1] = to_int(queasy.deci2)
            ss_artnr[2] = to_int(queasy.deci3)

            if length(queasy.char3) == 12:
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
                tt_artnr_data.append(tt_artnr)

                tt_artnr.curr_i = i_counter
                tt_artnr.ss_artnr = ss_artnr[i_counter - 1]


            for i_counter in range(1,3 + 1) :
                tt_content = Tt_content()
                tt_content_data.append(tt_content)

                tt_content.curr_i = i_counter
                tt_content.ss_content = ss_content[i_counter - 1]


            for i_counter in range(1,3 + 1) :
                tt_bezeich = Tt_bezeich()
                tt_bezeich_data.append(tt_bezeich)

                tt_bezeich.curr_i = i_counter
                tt_bezeich.ss_bezeich = ss_bezeich[i_counter - 1]

            if ss_artnr[0] != 0:

                l_art1 = get_cache (L_artikel, {"artnr": [(eq, ss_artnr[0])]})

                if l_art1:
                    ss_bezeich[0] = l_art1.bezeich

            if ss_artnr[1] != 0:

                l_art1 = get_cache (L_artikel, {"artnr": [(eq, ss_artnr[1])]})

                if l_art1:
                    ss_bezeich[1] = l_art1.bezeich

            if ss_artnr[2] != 0:

                l_art1 = get_cache (L_artikel, {"artnr": [(eq, ss_artnr[2])]})

                if l_art1:
                    ss_bezeich[2] = l_art1.bezeich


    htparam = get_cache (Htparam, {"paramnr": [(eq, 89)]})

    if htparam:
        param89 = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 257)]})

    if htparam:
        f_endkum = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 258)]})

    if htparam:
        b_endkum = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 268)]})

    if htparam:
        o_endkum = htparam.finteger

    l_artikel = get_cache (L_artikel, {"artnr": [(eq, artnr)]})

    if not l_artikel:

        return generate_output()
    fibukonto = l_artikel.fibukonto

    if l_artikel.fibukonto == "":
        fibukonto = "00000000000000000000"

    if not matches(l_artikel.herkunft,r"*;*"):

        # lbuff = get_cache (L_artikel, {"_recid": [(eq, l_artikel._recid)]})
        lbuff = db_session.query(Lbuff).filter(Lbuff._recid == l_artikel._recid).with_for_update().first()

        lbuff.herkunft = lbuff.herkunft + ";"
        
    strartnr = "*" + to_string(artnr) + "*"

    guestbook = db_session.query(Guestbook).filter(
             (matches(Guestbook.infostr,strartnr))).first()

    if guestbook:
        ttguestbook = Ttguestbook()
        ttguestbook_data.append(ttguestbook)

        buffer_copy(guestbook, ttguestbook)
    l_art = L_art()
    l_art_data.append(l_art)

    fill_lart()

    if changed:

        l_bestand = get_cache (L_bestand, {"artnr": [(eq, artnr)],"lager_nr": [(eq, 0)]})

        if l_bestand:
            set_disp1 = True

        if l_art.vk_preis != 0:
            set_disp2 = True

        l_ophis = get_cache (L_ophis, {"artnr": [(eq, artnr)]})

        if l_ophis:
            set_disp3 = True
        artnr_ok = check_artno()
    else:

        l_artikel = get_cache (L_artikel, {"artnr": [(eq, artnr)]})

    htparam = get_cache (Htparam, {"paramnr": [(eq, 911)]})

    if htparam.paramgruppe == 21 and htparam.flogical:
        set_disp4 = True

    if l_artikel.betriebsnr != 0:

        h_rezept = get_cache (H_rezept, {"artnrrezept": [(eq, l_artikel.betriebsnr)]})

        if h_rezept:
            recipe_bez = h_rezept.bezeich

    if l_art.lief_nr1 != 0:

        l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, l_art.lief_nr1)]})

        if l_lieferant:
            firma1 = l_lieferant.firma

    if l_art.lief_nr2 != 0:

        l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, l_art.lief_nr2)]})

        if l_lieferant:
            firma2 = l_lieferant.firma

    if l_art.lief_nr3 != 0:

        l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, l_art.lief_nr3)]})

        if l_lieferant:
            firma3 = l_lieferant.firma

    if l_art.zwkum != 0:

        l_untergrup = get_cache (L_untergrup, {"zwkum": [(eq, l_art.zwkum)]})

        if l_untergrup:
            zw_bezeich = l_untergrup.bezeich

    if l_art.endkum != 0:

        l_hauptgrp = get_cache (L_hauptgrp, {"endkum": [(eq, l_art.endkum)]})

        if l_hauptgrp:
            end_bezeich = l_hauptgrp.bezeich
    t_l_art = T_l_art()
    t_l_art_data.append(t_l_art)

    buffer_copy(l_artikel, t_l_art)
    t_l_art.t_recid = l_artikel._recid
    t_message_list = T_message_list()
    t_message_list_data.append(t_message_list)


    l_ophis = get_cache (L_ophis, {"artnr": [(eq, artnr)],"op_art": [(eq, 1)]})

    if l_ophis:
        t_message_list.lock_flag1 = True
    else:

        for l_op in db_session.query(L_op).filter(
                 (L_op.artnr == artnr) & (L_op.loeschflag != 2) & (L_op.op_art == 1)).order_by(L_op._recid).all():
            count_lop = count_lop + 1

            if count_lop >= 5:
                break

        if count_lop != 0:
            t_message_list.lock_flag1 = True

    h_rezlin = get_cache (H_rezlin, {"artnrlager": [(eq, artnr)]})

    if h_rezlin:
        t_message_list.lock_flag2 = True

    return generate_output()