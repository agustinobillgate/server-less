from functions.additional_functions import *
import decimal
from datetime import date
from functions.mk_sarticle_btn_gobl import mk_sarticle_btn_gobl

def mk_sarticle_btn_go_webbl(pvilanguage:int, artnr:int, dml_art:bool, bez_aend:bool, s_unit:str, zwkum:int, endkum:int, bezeich:str, jahrgang:int, min_bestand:decimal, lieferfrist:int, inhalt:decimal, lief_einheit:decimal, masseinheit:str, herkunft:str, erfass_art:bool, bestellt:bool, fibukonto:str, alkoholgrad:decimal, traubensorte:str, lief_nr1:int, lief_nr2:int, lief_nr3:int, letz_eingang:date, letz_ausgang:date, anzverbrauch:decimal, ek_aktuell:decimal, ek_letzter:decimal, wert_verbrau:decimal, vk_preis:decimal, lief_artnr1:str, lief_artnr2:str, lief_artnr3:str, betriebsnr:int, tartnr_curr_i1:int, tartnr_curr_i2:int, tartnr_curr_i3:int, sartnr1:int, sartnr2:int, sartnr3:int, tcontent_curr_i1:int, tcontent_curr_i2:int, tcontent_curr_i3:int, scontent1:int, scontent2:int, scontent3:int):
    sss_artnr = False
    sss_cont = False
    str_msg = ""
    created = False
    lvcarea:str = "mk_sarticle"
    ss_artnr:[int] = [0, 0, 0, 0]
    ss_content:[int] = [0, 0, 0, 0]

    l_art = tt_artnr = tt_content = None

    l_art_list, L_art = create_model("L_art", {"artnr":int, "zwkum":int, "endkum":int, "bezeich":str, "jahrgang":int, "min_bestand":decimal, "lieferfrist":int, "inhalt":decimal, "lief_einheit":decimal, "masseinheit":str, "herkunft":str, "erfass_art":bool, "bestellt":bool, "fibukonto":str, "alkoholgrad":decimal, "traubensorte":str, "lief_nr1":int, "lief_nr2":int, "lief_nr3":int, "letz_eingang":date, "letz_ausgang":date, "anzverbrauch":decimal, "ek_aktuell":decimal, "ek_letzter":decimal, "wert_verbrau":decimal, "vk_preis":decimal, "lief_artnr":[str, 3], "betriebsnr":int})
    tt_artnr_list, Tt_artnr = create_model("Tt_artnr", {"curr_i":int, "ss_artnr":int})
    tt_content_list, Tt_content = create_model("Tt_content", {"curr_i":int, "ss_content":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal sss_artnr, sss_cont, str_msg, created, lvcarea, ss_artnr, ss_content


        nonlocal l_art, tt_artnr, tt_content
        nonlocal l_art_list, tt_artnr_list, tt_content_list
        return {"sss_artnr": sss_artnr, "sss_cont": sss_cont, "str_msg": str_msg, "created": created}


    l_art = L_art()
    l_art_list.append(l_art)

    l_art.artnr = artnr
    l_art.zwkum = zwkum
    l_art.endkum = endkum
    l_art.bezeich = bezeich
    l_art.jahrgang = jahrgang
    l_art.min_bestand = min_bestand
    l_art.lieferfrist = lieferfrist
    l_art.inhalt = inhalt
    l_art.lief_einheit = lief_einheit
    l_art.masseinheit = masseinheit
    l_art.herkunft = herkunft
    l_art.erfass_art = erfass_art
    l_art.bestellt = bestellt
    l_art.fibukonto = fibukonto
    l_art.alkoholgrad = alkoholgrad
    l_art.traubensorte = traubensorte
    l_art.lief_nr1 = lief_nr1
    l_art.lief_nr2 = lief_nr2
    l_art.lief_nr3 = lief_nr3
    l_art.letz_eingang = letz_eingang
    l_art.letz_ausgang = letz_ausgang
    l_art.anzverbrauch = anzverbrauch
    l_art.ek_aktuell = ek_aktuell
    l_art.ek_letzter = ek_letzter
    l_art.wert_verbrau = wert_verbrau
    l_art.vk_preis = vk_preis
    l_art.lief_artnr[0] = lief_artnr1
    l_art.lief_artnr[1] = lief_artnr2
    l_art.lief_artnr[2] = lief_artnr3
    l_art.betriebsnr = betriebsnr


    tt_artnr = Tt_artnr()
    tt_artnr_list.append(tt_artnr)

    tt_artnr.curr_i = tartnr_curr_i1
    tt_artnr.ss_artnr = sartnr1


    tt_artnr = Tt_artnr()
    tt_artnr_list.append(tt_artnr)

    tt_artnr.curr_i = tartnr_curr_i2
    tt_artnr.ss_artnr = sartnr2


    tt_artnr = Tt_artnr()
    tt_artnr_list.append(tt_artnr)

    tt_artnr.curr_i = tartnr_curr_i3
    tt_artnr.ss_artnr = sartnr3


    tt_content = Tt_content()
    tt_content_list.append(tt_content)

    tt_content.curr_i = tcontent_curr_i1
    tt_content.ss_content = scontent1


    tt_content = Tt_content()
    tt_content_list.append(tt_content)

    tt_content.curr_i = tcontent_curr_i2
    tt_content.ss_content = scontent2


    tt_content = Tt_content()
    tt_content_list.append(tt_content)

    tt_content.curr_i = tcontent_curr_i3
    tt_content.ss_content = scontent3


    sss_artnr, sss_cont, str_msg, created = get_output(mk_sarticle_btn_gobl(pvilanguage, tt_artnr, tt_content, artnr, dml_art, fibukonto, bez_aend, s_unit, l_art))

    return generate_output()