from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import L_artikel, Bediener, Gl_acct, L_untergrup, Res_history, Queasy

tt_artnr_list, Tt_artnr = create_model("Tt_artnr", {"curr_i":int, "ss_artnr":int})
tt_content_list, Tt_content = create_model("Tt_content", {"curr_i":int, "ss_content":int})
l_art_list, L_art = create_model_like(L_artikel)

def mk_sarticle_btn_go_1bl(user_init:str, pvilanguage:int, tt_artnr_list:[Tt_artnr], tt_content_list:[Tt_content], artnr:int, dml_art:bool, fibukonto:str, bez_aend:bool, s_unit:str, l_art_list:[L_art]):
    sss_artnr = False
    sss_cont = False
    str_msg = ""
    created = False
    lvcarea:str = "mk-sarticle"
    ss_artnr:List[int] = create_empty_list(3,0)
    ss_content:List[int] = create_empty_list(3,0)
    l_artikel = bediener = gl_acct = l_untergrup = res_history = queasy = None

    l_art = tt_artnr = tt_content = t_bediener = l_art1 = None

    T_bediener = create_buffer("T_bediener",Bediener)
    L_art1 = create_buffer("L_art1",L_artikel)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal sss_artnr, sss_cont, str_msg, created, lvcarea, ss_artnr, ss_content, l_artikel, bediener, gl_acct, l_untergrup, res_history, queasy
        nonlocal user_init, pvilanguage, artnr, dml_art, fibukonto, bez_aend, s_unit
        nonlocal t_bediener, l_art1


        nonlocal l_art, tt_artnr, tt_content, t_bediener, l_art1
        nonlocal l_art_list, tt_artnr_list, tt_content_list
        return {"sss_artnr": sss_artnr, "sss_cont": sss_cont, "str_msg": str_msg, "created": created}

    def create_l_artikel():

        nonlocal sss_artnr, sss_cont, str_msg, created, lvcarea, ss_artnr, ss_content, l_artikel, bediener, gl_acct, l_untergrup, res_history, queasy
        nonlocal user_init, pvilanguage, artnr, dml_art, fibukonto, bez_aend, s_unit
        nonlocal t_bediener, l_art1


        nonlocal l_art, tt_artnr, tt_content, t_bediener, l_art1
        nonlocal l_art_list, tt_artnr_list, tt_content_list


        l_artikel = L_artikel()
        db_session.add(l_artikel)

        l_artikel.artnr = artnr
        l_artikel.fibukonto = fibukonto
        l_artikel.bezeich = l_art.bezeich
        l_artikel.zwkum = l_art.zwkum
        l_artikel.endkum = l_art.endkum
        l_artikel.herkunft = l_art.herkunft + ";" + s_unit + ";"
        l_artikel.masseinheit = l_art.masseinheit
        l_artikel.inhalt =  to_decimal(l_art.inhalt)
        l_artikel.traubensorte = l_art.traubensort
        l_artikel.lief_einheit =  to_decimal(l_art.lief_einheit)
        l_artikel.min_bestand =  to_decimal(l_art.min_bestand)
        l_artikel.anzverbrauch =  to_decimal(l_art.anzverbrauch)
        l_artikel.lief_nr1 = l_art.lief_nr1
        l_artikel.lief_artnr[0] = l_art.lief_artnr[0]
        l_artikel.lief_nr2 = l_art.lief_nr2
        l_artikel.lief_artnr[1] = l_art.lief_artnr[1]
        l_artikel.lief_nr3 = l_art.lief_nr3
        l_artikel.lief_artnr[2] = l_art.lief_artnr[2]
        l_artikel.betriebsnr = l_art.betriebsnr
        l_artikel.ek_aktuell =  to_decimal(l_art.ek_aktuell)
        l_artikel.ek_letzter =  to_decimal(l_art.ek_letzter)
        l_artikel.vk_preis =  to_decimal(l_art.vk_preis)
        l_artikel.bestellt = dml_art
        l_artikel.jahrgang = l_art.jahrgang


        res_history = Res_history()
        db_session.add(res_history)

        res_history.nr = t_bediener.nr
        res_history.datum = get_current_date()
        res_history.zeit = get_current_time_in_seconds()
        res_history.aenderung = "Stock article No : " + to_string(l_artikel.artnr, "9999999") +\
                " created - Description: " + l_artikel.bezeich


        res_history.action = "Stock Article Files"

        if ss_artnr[0] != 0 or ss_artnr[1] != 0 or ss_artnr[2] != 0:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 20
            queasy.number1 = artnr
            queasy.deci1 =  to_decimal(ss_artnr[0])
            queasy.deci2 =  to_decimal(ss_artnr[1])
            queasy.deci3 =  to_decimal(ss_artnr[2])
            queasy.char3 = to_string(ss_content[0], "999") + ";" +\
                    to_string(ss_content[1], "999") + ";" +\
                    to_string(ss_content[2], "999") + ";"
            queasy.date3 = get_current_date()


            pass

    l_art = query(l_art_list, first=True)

    t_bediener = db_session.query(T_bediener).filter(
             (func.lower(T_bediener.userinit) == (user_init).lower())).first()

    for tt_artnr in query(tt_artnr_list):
        ss_artnr[tt_artnr.curr_i - 1] = tt_artnr.ss_artnr

    for tt_content in query(tt_content_list):
        ss_content[tt_content.curr_i - 1] = tt_content.ss_content

    if ss_artnr[0] != 0:

        l_art1 = db_session.query(L_art1).filter(
                 (L_art1.artnr == ss_artnr[0])).first()

        if not l_art1 or l_art1.betriebsnr > 0:
            sss_artnr = True

            return generate_output()

        if ss_content[0] == 0:
            sss_cont = True

            return generate_output()

    if ss_artnr[1] != 0:

        l_art1 = db_session.query(L_art1).filter(
                 (L_art1.artnr == ss_artnr[1)]).first()

        if not l_art1 or l_art1.betriebsnr > 0:
            sss_artnr = True

            return generate_output()

        if ss_content[1] == 0:
            sss_cont = True

            return generate_output()

    if ss_artnr[2] != 0:

        l_art1 = db_session.query(L_art1).filter(
                 (L_art1.artnr == ss_artnr[2)]).first()

        if not l_art1 or l_art1.betriebsnr > 0:
            sss_artnr = True

            return generate_output()

        if ss_content[2] == 0:
            sss_cont = True

            return generate_output()

    if artnr == 0 or l_art.zwkum == 0 or l_art.endkum == 0 or l_art.inhalt == 0 or l_art.bezeich == "":
        str_msg = translateExtended ("Unfilled field(s) detected", lvcarea, "")
    else:

        l_artikel = db_session.query(L_artikel).filter(
                 (L_artikel.artnr == artnr)).first()

        if l_artikel:
            str_msg = translateExtended ("Article Number ", lvcarea, "") + to_string(artnr) + " - " + l_artikel.bezeich + chr(10) + "already exists"

            return generate_output()

        if l_art.zwkum >= 100:

            if substring(to_string(artnr) , 1, 3) != to_string(l_art.zwkum, "999") or substring(to_string(artnr) , 0, 1) != to_string(l_art.endkum, "9"):
                str_msg = translateExtended ("Article Number does not match to main group and/or subgroup.", lvcarea, "")

                return generate_output()
        else:

            if substring(to_string(artnr) , 1, 2) != to_string(l_art.zwkum, "99") or substring(to_string(artnr) , 0, 1) != to_string(l_art.endkum, "9"):
                str_msg = translateExtended ("Article Number does not match to main group and/or subgroup.", lvcarea, "")

                return generate_output()

        gl_acct = db_session.query(Gl_acct).filter(
                     (func.lower(Gl_acct.fibukonto) == (fibukonto).lower())).first()

        if not gl_acct:

            l_untergrup = db_session.query(L_untergrup).filter(
                         (L_untergrup.zwkum == l_art.zwkum)).first()

            gl_acct = db_session.query(Gl_acct).filter(
                         (Gl_acct.fibukonto == l_untergrup.fibukonto)).first()

            if not gl_acct:
                str_msg = "&W" + translateExtended ("Chart of Account not correctly defined.", lvcarea, "")
        create_l_artikel()
        created = True

    return generate_output()