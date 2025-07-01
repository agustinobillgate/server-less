#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import L_artikel, Gl_acct, L_untergrup, Queasy

tt_artnr_list, Tt_artnr = create_model("Tt_artnr", {"curr_i":int, "ss_artnr":int})
tt_content_list, Tt_content = create_model("Tt_content", {"curr_i":int, "ss_content":int})
l_art_list, L_art = create_model_like(L_artikel)

def mk_sarticle_btn_gobl(pvilanguage:int, tt_artnr_list:[Tt_artnr], tt_content_list:[Tt_content], artnr:int, dml_art:bool, fibukonto:string, bez_aend:bool, s_unit:string, l_art_list:[L_art]):

    prepare_cache ([L_artikel, L_untergrup, Queasy])

    sss_artnr = False
    sss_cont = False
    str_msg = ""
    created = False
    lvcarea:string = "mk-sarticle"
    ss_artnr:List[int] = create_empty_list(3,0)
    ss_content:List[int] = create_empty_list(3,0)
    l_artikel = gl_acct = l_untergrup = queasy = None

    l_art = tt_artnr = tt_content = l_art1 = None

    L_art1 = create_buffer("L_art1",L_artikel)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal sss_artnr, sss_cont, str_msg, created, lvcarea, ss_artnr, ss_content, l_artikel, gl_acct, l_untergrup, queasy
        nonlocal pvilanguage, artnr, dml_art, fibukonto, bez_aend, s_unit
        nonlocal l_art1


        nonlocal l_art, tt_artnr, tt_content, l_art1

        return {"sss_artnr": sss_artnr, "sss_cont": sss_cont, "str_msg": str_msg, "created": created}

    def create_l_artikel():

        nonlocal sss_artnr, sss_cont, str_msg, created, lvcarea, ss_artnr, ss_content, l_artikel, gl_acct, l_untergrup, queasy
        nonlocal pvilanguage, artnr, dml_art, fibukonto, bez_aend, s_unit
        nonlocal l_art1


        nonlocal l_art, tt_artnr, tt_content, l_art1


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
        l_artikel.traubensorte = l_art.traubensorte
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

    for tt_artnr in query(tt_artnr_list):
        ss_artnr[tt_artnr.curr_i - 1] = tt_artnr.ss_artnr

    for tt_content in query(tt_content_list):
        ss_content[tt_content.curr_i - 1] = tt_content.ss_content

    if ss_artnr[0] != 0:

        l_art1 = get_cache (L_artikel, {"artnr": [(eq, ss_artnr[0])]})

        if not l_art1 or l_art1.betriebsnr > 0:
            sss_artnr = True

            return generate_output()

        if ss_content[0] == 0:
            sss_cont = True

            return generate_output()

    if ss_artnr[1] != 0:

        l_art1 = get_cache (L_artikel, {"artnr": [(eq, ss_artnr[1])]})

        if not l_art1 or l_art1.betriebsnr > 0:
            sss_artnr = True

            return generate_output()

        if ss_content[1] == 0:
            sss_cont = True

            return generate_output()

    if ss_artnr[2] != 0:

        l_art1 = get_cache (L_artikel, {"artnr": [(eq, ss_artnr[2])]})

        if not l_art1 or l_art1.betriebsnr > 0:
            sss_artnr = True

            return generate_output()

        if ss_content[2] == 0:
            sss_cont = True

            return generate_output()

    if artnr == 0 or l_art.zwkum == 0 or l_art.endkum == 0 or l_art.inhalt == 0 or l_art.bezeich == "":
        str_msg = translateExtended ("Unfilled field(s) detected", lvcarea, "")
    else:

        l_artikel = get_cache (L_artikel, {"artnr": [(eq, artnr)]})

        if l_artikel:
            str_msg = translateExtended ("Article Number ", lvcarea, "") + to_string(artnr) + " - " + l_artikel.bezeich + chr_unicode(10) + "already exists"

            return generate_output()

        if l_art.zwkum >= 100:

            if substring(to_string(artnr) , 1, 3) != to_string(l_art.zwkum, "999") or substring(to_string(artnr) , 0, 1) != to_string(l_art.endkum, "9"):
                str_msg = translateExtended ("Article Number does not match to main group and/or subgroup.", lvcarea, "")

                return generate_output()
        else:

            if substring(to_string(artnr) , 1, 2) != to_string(l_art.zwkum, "99") or substring(to_string(artnr) , 0, 1) != to_string(l_art.endkum, "9"):
                str_msg = translateExtended ("Article Number does not match to main group and/or subgroup.", lvcarea, "")

                return generate_output()

        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, fibukonto)]})

        if not gl_acct:

            l_untergrup = get_cache (L_untergrup, {"zwkum": [(eq, l_art.zwkum)]})

            gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, l_untergrup.fibukonto)]})

            if not gl_acct:
                str_msg = "&W" + translateExtended ("Chart of Account not correctly defined.", lvcarea, "")
        create_l_artikel()
        created = True

    return generate_output()