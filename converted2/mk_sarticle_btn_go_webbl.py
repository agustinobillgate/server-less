#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.mk_sarticle_btn_gobl import mk_sarticle_btn_gobl

def mk_sarticle_btn_go_webbl(pvilanguage:int, artnr:int, dml_art:bool, bez_aend:bool, s_unit:string, zwkum:int, endkum:int, bezeich:string, jahrgang:int, min_bestand:Decimal, lieferfrist:int, inhalt:Decimal, lief_einheit:Decimal, masseinheit:string, herkunft:string, erfass_art:bool, bestellt:bool, fibukonto:string, alkoholgrad:Decimal, traubensorte:string, lief_nr1:int, lief_nr2:int, lief_nr3:int, letz_eingang:date, letz_ausgang:date, anzverbrauch:Decimal, ek_aktuell:Decimal, ek_letzter:Decimal, wert_verbrau:Decimal, vk_preis:Decimal, lief_artnr1:string, lief_artnr2:string, lief_artnr3:string, betriebsnr:int, tartnr_curr_i1:int, tartnr_curr_i2:int, tartnr_curr_i3:int, sartnr1:int, sartnr2:int, sartnr3:int, tcontent_curr_i1:int, tcontent_curr_i2:int, tcontent_curr_i3:int, scontent1:int, scontent2:int, scontent3:int):
    sss_artnr = False
    sss_cont = False
    str_msg = ""
    created = False
    lvcarea:string = "mk-sarticle"
    ss_artnr:List[int] = create_empty_list(3,0)
    ss_content:List[int] = create_empty_list(3,0)

    l_art = tt_artnr = tt_content = None

    l_art_data, L_art = create_model("L_art", {"artnr":int, "zwkum":int, "endkum":int, "bezeich":string, "jahrgang":int, "min_bestand":Decimal, "lieferfrist":int, "inhalt":Decimal, "lief_einheit":Decimal, "masseinheit":string, "herkunft":string, "erfass_art":bool, "bestellt":bool, "fibukonto":string, "alkoholgrad":Decimal, "traubensorte":string, "lief_nr1":int, "lief_nr2":int, "lief_nr3":int, "letz_eingang":date, "letz_ausgang":date, "anzverbrauch":Decimal, "ek_aktuell":Decimal, "ek_letzter":Decimal, "wert_verbrau":Decimal, "vk_preis":Decimal, "lief_artnr":[string,3], "betriebsnr":int})
    tt_artnr_data, Tt_artnr = create_model("Tt_artnr", {"curr_i":int, "ss_artnr":int})
    tt_content_data, Tt_content = create_model("Tt_content", {"curr_i":int, "ss_content":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal sss_artnr, sss_cont, str_msg, created, lvcarea, ss_artnr, ss_content
        nonlocal pvilanguage, artnr, dml_art, bez_aend, s_unit, zwkum, endkum, bezeich, jahrgang, min_bestand, lieferfrist, inhalt, lief_einheit, masseinheit, herkunft, erfass_art, bestellt, fibukonto, alkoholgrad, traubensorte, lief_nr1, lief_nr2, lief_nr3, letz_eingang, letz_ausgang, anzverbrauch, ek_aktuell, ek_letzter, wert_verbrau, vk_preis, lief_artnr1, lief_artnr2, lief_artnr3, betriebsnr, tartnr_curr_i1, tartnr_curr_i2, tartnr_curr_i3, sartnr1, sartnr2, sartnr3, tcontent_curr_i1, tcontent_curr_i2, tcontent_curr_i3, scontent1, scontent2, scontent3


        nonlocal l_art, tt_artnr, tt_content
        nonlocal l_art_data, tt_artnr_data, tt_content_data

        return {"sss_artnr": sss_artnr, "sss_cont": sss_cont, "str_msg": str_msg, "created": created}


    l_art = L_art()
    l_art_data.append(l_art)

    l_art.artnr = artnr
    l_art.zwkum = zwkum
    l_art.endkum = endkum
    l_art.bezeich = bezeich
    l_art.jahrgang = jahrgang
    l_art.min_bestand =  to_decimal(min_bestand)
    l_art.lieferfrist = lieferfrist
    l_art.inhalt =  to_decimal(inhalt)
    l_art.lief_einheit =  to_decimal(lief_einheit)
    l_art.masseinheit = masseinheit
    l_art.herkunft = herkunft
    l_art.erfass_art = erfass_art
    l_art.bestellt = bestellt
    l_art.fibukonto = fibukonto
    l_art.alkoholgrad =  to_decimal(alkoholgrad)
    l_art.traubensorte = traubensorte
    l_art.lief_nr1 = lief_nr1
    l_art.lief_nr2 = lief_nr2
    l_art.lief_nr3 = lief_nr3
    l_art.letz_eingang = letz_eingang
    l_art.letz_ausgang = letz_ausgang
    l_art.anzverbrauch =  to_decimal(anzverbrauch)
    l_art.ek_aktuell =  to_decimal(ek_aktuell)
    l_art.ek_letzter =  to_decimal(ek_letzter)
    l_art.wert_verbrau =  to_decimal(wert_verbrau)
    l_art.vk_preis =  to_decimal(vk_preis)
    l_art.lief_artnr[0] = lief_artnr1
    l_art.lief_artnr[1] = lief_artnr2
    l_art.lief_artnr[2] = lief_artnr3
    l_art.betriebsnr = betriebsnr


    tt_artnr = Tt_artnr()
    tt_artnr_data.append(tt_artnr)

    tt_artnr.curr_i = tartnr_curr_i1
    tt_artnr.ss_artnr = sartnr1


    tt_artnr = Tt_artnr()
    tt_artnr_data.append(tt_artnr)

    tt_artnr.curr_i = tartnr_curr_i2
    tt_artnr.ss_artnr = sartnr2


    tt_artnr = Tt_artnr()
    tt_artnr_data.append(tt_artnr)

    tt_artnr.curr_i = tartnr_curr_i3
    tt_artnr.ss_artnr = sartnr3


    tt_content = Tt_content()
    tt_content_data.append(tt_content)

    tt_content.curr_i = tcontent_curr_i1
    tt_content.ss_content = scontent1


    tt_content = Tt_content()
    tt_content_data.append(tt_content)

    tt_content.curr_i = tcontent_curr_i2
    tt_content.ss_content = scontent2


    tt_content = Tt_content()
    tt_content_data.append(tt_content)

    tt_content.curr_i = tcontent_curr_i3
    tt_content.ss_content = scontent3


    sss_artnr, sss_cont, str_msg, created = get_output(mk_sarticle_btn_gobl(pvilanguage, tt_artnr_data, tt_content_data, artnr, dml_art, fibukonto, bez_aend, s_unit, l_art_data))

    return generate_output()