from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import L_artikel, Gl_acct, L_untergrup, Queasy, Bediener, Res_history, L_op, L_ophis, L_order, L_bestand, L_lager, L_besthis, L_verbrauch, L_pprice, H_rezlin, dml_art, Dml_artdep

tt_artnr_list, Tt_artnr = create_model("Tt_artnr", {"curr_i":int, "ss_artnr":int})
tt_content_list, Tt_content = create_model("Tt_content", {"curr_i":int, "ss_content":int})
l_art_list, L_art = create_model_like(L_artikel)

def chg_sarticle_btn_gobl(pvilanguage:int, tt_artnr_list:[Tt_artnr], tt_content_list:[Tt_content], s_unit:str, artnr:int, t_recid:int, fibukonto:str, dml_art:bool, bez_aend:bool, picture_file:str, original_art:int, user_init:str, l_art_list:[L_art]):
    sss_artnr = False
    sss_cont = False
    str_msg = ""
    changed = False
    ss_artnr:List[int] = create_empty_list(3,0)
    ss_content:List[int] = create_empty_list(3,0)
    old_lastpc_price:decimal = to_decimal("0.0")
    lvcarea:str = "chg-sarticle"
    l_artikel = gl_acct = l_untergrup = queasy = bediener = res_history = l_op = l_ophis = l_order = l_bestand = l_lager = l_besthis = l_verbrauch = l_pprice = h_rezlin = dml_art = dml_artdep = None

    l_art = tt_artnr = tt_content = l_art1 = l_art2 = None

    L_art1 = create_buffer("L_art1",L_artikel)
    L_art2 = create_buffer("L_art2",L_artikel)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal sss_artnr, sss_cont, str_msg, changed, ss_artnr, ss_content, old_lastpc_price, lvcarea, l_artikel, gl_acct, l_untergrup, queasy, bediener, res_history, l_op, l_ophis, l_order, l_bestand, l_lager, l_besthis, l_verbrauch, l_pprice, h_rezlin, dml_art, dml_artdep
        nonlocal pvilanguage, s_unit, artnr, t_recid, fibukonto, dml_art, bez_aend, picture_file, original_art, user_init
        nonlocal l_art1, l_art2


        nonlocal l_art, tt_artnr, tt_content, l_art1, l_art2
        nonlocal l_art_list, tt_artnr_list, tt_content_list
        return {"sss_artnr": sss_artnr, "sss_cont": sss_cont, "str_msg": str_msg, "changed": changed}

    def update_l_artikel():

        nonlocal sss_artnr, sss_cont, str_msg, changed, ss_artnr, ss_content, old_lastpc_price, lvcarea, l_artikel, gl_acct, l_untergrup, queasy, bediener, res_history, l_op, l_ophis, l_order, l_bestand, l_lager, l_besthis, l_verbrauch, l_pprice, h_rezlin, dml_art, dml_artdep
        nonlocal pvilanguage, s_unit, artnr, t_recid, fibukonto, dml_art, bez_aend, picture_file, original_art, user_init
        nonlocal l_art1, l_art2


        nonlocal l_art, tt_artnr, tt_content, l_art1, l_art2
        nonlocal l_art_list, tt_artnr_list, tt_content_list

        l_artikel = db_session.query(L_artikel).filter(
                     (L_artikel._recid == t_recid)).first()
        old_lastpc_price =  to_decimal(l_artikel.ek_letzter)
        l_artikel.artnr = artnr
        l_artikel.fibukonto = fibukonto
        l_artikel.bestellt = dml_art
        l_artikel.jahrgang = to_int(bez_aend)
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
        l_artikel.alkoholgrad =  to_decimal(l_art.alkoholgrad)
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

        queasy = db_session.query(Queasy).filter(
                     (Queasy.key == 20) & (Queasy.number1 == artnr)).first()

        if ss_artnr[0] != 0 or ss_artnr[1] != 0 or ss_artnr[2] != 0 or picture_file != "":

            if not queasy:
                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 20
                queasy.number1 = artnr


            queasy.deci1 =  to_decimal(ss_artnr[0])
            queasy.deci2 =  to_decimal(ss_artnr[1])
            queasy.deci3 =  to_decimal(ss_artnr[2])
            queasy.char2 = to_string(ss_content[0], "999") + ";" +\
                    to_string(ss_content[1], "999") + ";" +\
                    to_string(ss_content[2], "999") + ";"
            queasy.char3 = picture_file
            queasy.date3 = get_current_date()


            pass
        else:

            if queasy:
                db_session.delete(queasy)

        if original_art != l_artikel.artnr:

            bediener = db_session.query(Bediener).filter(
                         (func.lower(Bediener.userinit) == (user_init).lower())).first()
            res_history = Res_history()
            db_session.add(res_history)

            res_history.nr = bediener.nr
            res_history.datum = get_current_date()
            res_history.zeit = get_current_time_in_seconds()
            res_history.action = "Inventory"
            res_history.aenderung = "Change Inventory ArtNo: " +\
                    to_string(original_art, "9999999") + " -> " +\
                    to_string(l_artikel.artnr, "9999999")


            pass

        if old_lastpc_price != l_art.ek_letzter:

            bediener = db_session.query(Bediener).filter(
                         (func.lower(Bediener.userinit) == (user_init).lower())).first()
            res_history = Res_history()
            db_session.add(res_history)

            res_history.nr = bediener.nr
            res_history.datum = get_current_date()
            res_history.zeit = get_current_time_in_seconds()
            res_history.action = "Inventory"
            res_history.aenderung = "Change Last Purchase Price " + l_artikel.bezeich + " : " +\
                    to_string(old_lastpc_price) + " --> " + to_string(l_art.ek_letzter)


            pass

    def update_artnr():

        nonlocal sss_artnr, sss_cont, str_msg, changed, ss_artnr, ss_content, old_lastpc_price, lvcarea, l_artikel, gl_acct, l_untergrup, queasy, bediener, res_history, l_op, l_ophis, l_order, l_bestand, l_lager, l_besthis, l_verbrauch, l_pprice, h_rezlin, dml_art, dml_artdep
        nonlocal pvilanguage, s_unit, artnr, t_recid, fibukonto, dml_art, bez_aend, picture_file, original_art, user_init
        nonlocal l_art1, l_art2


        nonlocal l_art, tt_artnr, tt_content, l_art1, l_art2
        nonlocal l_art_list, tt_artnr_list, tt_content_list

        l_op1 = None
        l_ophis1 = None
        l_od1 = None
        l_art1 = None
        L_op1 =  create_buffer("L_op1",L_op)
        L_ophis1 =  create_buffer("L_ophis1",L_ophis)
        L_od1 =  create_buffer("L_od1",L_order)
        L_art1 =  create_buffer("L_art1",L_artikel)

        l_bestand = db_session.query(L_bestand).filter(
                 (L_bestand.artnr == original_art) & (L_bestand.lager_nr == 0)).first()

        if l_bestand:
            l_bestand.artnr = artnr

        for l_lager in db_session.query(L_lager).order_by(L_lager._recid).all():

            l_bestand = db_session.query(L_bestand).filter(
                     (L_bestand.artnr == original_art) & (L_bestand.lager_nr == l_lager.lager_nr)).first()

            if l_bestand:
                l_bestand.artnr = artnr

            for l_op in db_session.query(L_op).filter(
                     (L_op.artnr == original_art) & (L_op.lager_nr == l_lager.lager_nr)).order_by(L_op._recid).all():

                l_op1 = db_session.query(L_op1).filter(
                         (L_op1._recid == l_op._recid)).first()
                l_op1.artnr = artnr

        l_besthis = db_session.query(L_besthis).filter(
                 (L_besthis.artnr == original_art)).first()
        while None != l_besthis:
            l_besthis.artnr = artnr

            curr_recid = l_besthis._recid
            l_besthis = db_session.query(L_besthis).filter(
                     (L_besthis.artnr == original_art)).filter(L_besthis._recid > curr_recid).first()

        for l_ophis in db_session.query(L_ophis).filter(
                 (L_ophis.artnr == original_art)).order_by(L_ophis._recid).all():

            l_ophis1 = db_session.query(L_ophis1).filter(
                     (L_ophis1._recid == l_ophis._recid)).first()
            l_ophis1.artnr = artnr

        for l_verbrauch in db_session.query(L_verbrauch).filter(
                 (L_verbrauch.artnr == original_art)).order_by(L_verbrauch._recid).all():
            l_verbrauch.artnr = artnr

        for l_order in db_session.query(L_order).filter(
                 (L_order.artnr == original_art)).order_by(L_order._recid).all():

            l_od1 = db_session.query(L_od1).filter(
                     (L_od1._recid == l_order._recid)).first()
            l_od1.artnr = artnr

        for l_pprice in db_session.query(L_pprice).filter(
                 (L_pprice.artnr == original_art)).order_by(L_pprice._recid).all():
            l_pprice.artnr = artnr

        for h_rezlin in db_session.query(H_rezlin).filter(
                 (H_rezlin.artnrlager == original_art)).order_by(H_rezlin._recid).all():
            h_rezlin.artnrlager = artnr

        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 20) & (Queasy.number1 == original_art)).first()

        if queasy:
            queasy.number1 = artnr
            pass

        dml_art = db_session.query(dml_art).filter(
                 (dml_art.artnr == original_art)).first()
        while None != dml_art:
            dml_art.artnr = artnr

            curr_recid = dml_art._recid
            dml_art = db_session.query(dml_art).filter(
                     (dml_art.artnr == original_art)).filter(dml_art._recid > curr_recid).first()

        dml_artdep = db_session.query(Dml_artdep).filter(
                 (Dml_artdep.artnr == original_art)).first()
        while None != dml_artdep:
            dml_artdep.artnr = artnr

            curr_recid = dml_artdep._recid
            dml_artdep = db_session.query(Dml_artdep).filter(
                     (Dml_artdep.artnr == original_art)).filter(Dml_artdep._recid > curr_recid).first()


    l_art = query(l_art_list, first=True)

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
                 (L_art1.artnr == ss_artnr[1])).first()

        if not l_art1 or l_art1.betriebsnr > 0:
            sss_artnr = True

            return generate_output()

        if ss_content[1] == 0:
            sss_cont = True

            return generate_output()

    if ss_artnr[2] != 0:

        l_art1 = db_session.query(L_art1).filter(
                 (L_art1.artnr == ss_artnr[2])).first()

        if not l_art1 or l_art1.betriebsnr > 0:
            sss_artnr = True

            return generate_output()

        if ss_content[2] == 0:
            sss_cont = True

            return generate_output()

    if artnr == 0:
        str_msg = translateExtended ("Article Number not yet defined", lvcarea, "")
    else:

        l_artikel = db_session.query(L_artikel).filter(
                 (L_artikel.artnr == artnr) & (L_artikel._recid != t_recid)).first()

        if l_artikel:
            str_msg = translateExtended ("Article Number ", lvcarea, "") + to_string(artnr) + " - " + l_artikel.bezeich + chr(2) + "already exists"
        else:

            gl_acct = db_session.query(Gl_acct).filter(
                     (func.lower(Gl_acct.fibukonto) == (fibukonto).lower())).first()

            if not gl_acct:

                l_untergrup = db_session.query(L_untergrup).filter(
                         (L_untergrup.zwkum == l_art.zwkum)).first()

                gl_acct = db_session.query(Gl_acct).filter(
                         (Gl_acct.fibukonto == l_untergrup.fibukonto)).first()

                if not gl_acct:
                    str_msg = "&W" + translateExtended ("Chart of Account not correctly defined.", lvcarea, "")
            update_l_artikel()
            update_artnr()
            changed = True

    return generate_output()