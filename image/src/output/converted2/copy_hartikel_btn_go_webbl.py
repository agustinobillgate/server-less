#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Wgrpdep, H_artikel, Artikel, Queasy, Hoteldpt, Bediener, Res_history

payload_list_list, Payload_list = create_model("Payload_list", {"all_flag":bool, "dept1":int, "dept2":int, "art1":int, "art2":int, "overwrite_flag":bool, "user_init":string})

def copy_hartikel_btn_go_webbl(payload_list_list:[Payload_list]):

    prepare_cache ([Wgrpdep, H_artikel, Artikel, Hoteldpt, Bediener, Res_history])

    anzahl = ""
    all_flag:bool = False
    dept1:int = 0
    dept2:int = 0
    art1:int = 0
    art2:int = 0
    overwrite_flag:bool = False
    user_init:string = ""
    wgrpdep = h_artikel = artikel = queasy = hoteldpt = bediener = res_history = None

    payload_list = subgrp = h_art = art = None

    Subgrp = create_buffer("Subgrp",Wgrpdep)
    H_art = create_buffer("H_art",H_artikel)
    Art = create_buffer("Art",Artikel)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal anzahl, all_flag, dept1, dept2, art1, art2, overwrite_flag, user_init, wgrpdep, h_artikel, artikel, queasy, hoteldpt, bediener, res_history
        nonlocal subgrp, h_art, art


        nonlocal payload_list, subgrp, h_art, art

        return {"anzahl": anzahl}

    def copy_sales():

        nonlocal anzahl, all_flag, dept1, dept2, art1, art2, overwrite_flag, user_init, wgrpdep, h_artikel, artikel, queasy, hoteldpt, bediener, res_history
        nonlocal subgrp, h_art, art


        nonlocal payload_list, subgrp, h_art, art

        n:int = 0
        qbuff = None
        Qbuff =  create_buffer("Qbuff",Queasy)
        anzahl = to_string(n)

        for h_art in db_session.query(H_art).filter(
                 (H_art.departement == dept1) & (H_art.activeflag) & (H_art.artart == 0) & (H_art.artnr >= art1) & (H_art.artnr <= art2)).order_by(H_art._recid).all():

            h_artikel = get_cache (H_artikel, {"artnr": [(eq, h_art.artnr)],"departement": [(eq, dept2)]})

            if h_artikel and not overwrite_flag:
                pass
            else:
                n = n + 1
                anzahl = to_string(n)

                subgrp = get_cache (Wgrpdep, {"departement": [(eq, dept1)],"zknr": [(eq, h_art.zwkum)]})

                wgrpdep = get_cache (Wgrpdep, {"departement": [(eq, dept2)],"zknr": [(eq, h_art.zwkum)]})

                if not wgrpdep and subgrp:
                    wgrpdep = Wgrpdep()
                    db_session.add(wgrpdep)

                    wgrpdep.departement = dept2
                    wgrpdep.zknr = subgrp.zknr
                    wgrpdep.bezeich = subgrp.bezeich

                if not h_artikel:
                    h_artikel = H_artikel()
                    db_session.add(h_artikel)

                h_artikel.artnr = h_art.artnr
                h_artikel.departement = dept2
                h_artikel.bezeich = h_art.bezeich
                h_artikel.epreis1 =  to_decimal(h_art.epreis1)
                h_artikel.epreis2 =  to_decimal(h_art.epreis2)
                h_artikel.zwkum = h_art.zwkum
                h_artikel.endkum = h_art.endkum
                h_artikel.mwst_code = h_art.mwst_code
                h_artikel.service_code = h_art.service_code
                h_artikel.autosaldo = h_art.autosaldo
                h_artikel.bezaendern = h_art.bezaendern
                h_artikel.bondruckernr[0] = h_art.bondruckernr[0]
                h_artikel.aenderwunsch = h_art.aenderwunsch
                h_artikel.s_gueltig = h_art.s_gueltig
                h_artikel.e_gueltig = h_art.e_gueltig
                h_artikel.artnrlager = h_art.artnrlager
                h_artikel.artnrrezept = h_art.artnrrezept
                h_artikel.lagernr = h_art.lagernr
                h_artikel.prozent =  to_decimal(h_art.prozent)
                h_artikel.artnrfront = h_art.artnrfront
                h_artikel.activeflag = True

                queasy = get_cache (Queasy, {"key": [(eq, 38)],"number1": [(eq, dept1)],"number2": [(eq, h_art.artnr)]})

                if queasy:
                    qbuff = Queasy()
                    db_session.add(qbuff)

                    buffer_copy(queasy, qbuff,except_fields=["number1"])
                    qbuff.number1 = dept2


                    pass

                art = get_cache (Artikel, {"artnr": [(eq, h_art.artnrfront)],"departement": [(eq, dept1)]})

                artikel = get_cache (Artikel, {"artnr": [(eq, h_art.artnrfront)],"departement": [(eq, dept2)]})

                if not artikel and art:
                    artikel = Artikel()
                    db_session.add(artikel)

                    artikel.departement = dept2
                    artikel.artnr = art.artnr
                    artikel.bezeich = art.bezeich
                    artikel.activeflag = True
                    artikel.fibukonto = art.fibukonto
                    artikel.bezeich1 = art.bezeich1
                    artikel.zwkum = art.zwkum
                    artikel.endkum = art.endkum
                    artikel.epreis =  to_decimal(art.epreis)
                    artikel.autosaldo = art.autosaldo
                    artikel.artart = art.artart
                    artikel.umsatzart = art.umsatzart
                    artikel.kassarapport = art.kassarapport
                    artikel.kassabuch = art.kassabuch
                    artikel.mwst_code = art.mwst_code
                    artikel.service_code = art.service_code
                    artikel.fibukonto = art.fibukonto
                    artikel.bezeich1 = art.bezeich
                    artikel.pricetab = art.pricetab
                    artikel.activeflag = art.activeflag
                    artikel.s_gueltig = art.s_gueltig
                    artikel.e_gueltig = art.e_gueltig
                    artikel.artnrlager = art.artnrlager
                    artikel.artnrrezept = art.artnrrezept
                    artikel.prozent =  to_decimal(art.prozent)
                    artikel.lagernr = art.lagernr


        create_log()


    def copy_all():

        nonlocal anzahl, all_flag, dept1, dept2, art1, art2, overwrite_flag, user_init, wgrpdep, h_artikel, artikel, queasy, hoteldpt, bediener, res_history
        nonlocal subgrp, h_art, art


        nonlocal payload_list, subgrp, h_art, art

        n:int = 0
        anzahl = to_string(n)

        for h_art in db_session.query(H_art).filter(
                 (H_art.departement == dept1) & (H_art.activeflag) & (H_art.artnr >= art1) & (H_art.artnr <= art2)).order_by(H_art._recid).all():

            h_artikel = get_cache (H_artikel, {"artnr": [(eq, h_art.artnr)],"departement": [(eq, dept2)]})

            if h_artikel and not overwrite_flag:
                pass
            else:
                n = n + 1
                anzahl = to_string(n)

                subgrp = get_cache (Wgrpdep, {"departement": [(eq, dept1)],"zknr": [(eq, h_art.zwkum)]})

                wgrpdep = get_cache (Wgrpdep, {"departement": [(eq, dept2)],"zknr": [(eq, h_art.zwkum)]})

                if not wgrpdep and subgrp:
                    wgrpdep = Wgrpdep()
                    db_session.add(wgrpdep)

                    wgrpdep.departement = dept2
                    wgrpdep.zknr = subgrp.zknr
                    wgrpdep.bezeich = subgrp.bezeich

                if not h_artikel:
                    h_artikel = H_artikel()
                    db_session.add(h_artikel)

                h_artikel.artnr = h_art.artnr
                h_artikel.artart = h_art.artart
                h_artikel.departement = dept2
                h_artikel.bezeich = h_art.bezeich
                h_artikel.epreis1 =  to_decimal(h_art.epreis1)
                h_artikel.epreis2 =  to_decimal(h_art.epreis2)
                h_artikel.zwkum = h_art.zwkum
                h_artikel.endkum = h_art.endkum
                h_artikel.mwst_code = h_art.mwst_code
                h_artikel.service_code = h_art.service_code
                h_artikel.autosaldo = h_art.autosaldo
                h_artikel.bezaendern = h_art.bezaendern
                h_artikel.bondruckernr[0] = h_art.bondruckernr[0]
                h_artikel.aenderwunsch = h_art.aenderwunsch
                h_artikel.s_gueltig = h_art.s_gueltig
                h_artikel.e_gueltig = h_art.e_gueltig
                h_artikel.artnrlager = h_art.artnrlager
                h_artikel.artnrrezept = h_art.artnrrezept
                h_artikel.lagernr = h_art.lagernr
                h_artikel.prozent =  to_decimal(h_art.prozent)
                h_artikel.artnrfront = h_art.artnrfront
                h_artikel.activeflag = True

                if h_art.artart == 0:

                    art = get_cache (Artikel, {"artnr": [(eq, h_art.artnrfront)],"departement": [(eq, dept1)]})

                    artikel = get_cache (Artikel, {"artnr": [(eq, h_art.artnrfront)],"departement": [(eq, dept2)]})

                    if not artikel and art:
                        artikel = Artikel()
                        db_session.add(artikel)

                        artikel.departement = dept2
                        artikel.artnr = art.artnr
                        artikel.bezeich = art.bezeich
                        artikel.activeflag = True
                        artikel.fibukonto = art.fibukonto
                        artikel.bezeich1 = art.bezeich1
                        artikel.zwkum = art.zwkum
                        artikel.endkum = art.endkum
                        artikel.epreis =  to_decimal(art.epreis)
                        artikel.autosaldo = art.autosaldo
                        artikel.artart = art.artart
                        artikel.umsatzart = art.umsatzart
                        artikel.kassarapport = art.kassarapport
                        artikel.kassabuch = art.kassabuch
                        artikel.mwst_code = art.mwst_code
                        artikel.service_code = art.service_code
                        artikel.fibukonto = art.fibukonto
                        artikel.bezeich1 = art.bezeich
                        artikel.pricetab = art.pricetab
                        artikel.activeflag = art.activeflag
                        artikel.s_gueltig = art.s_gueltig
                        artikel.e_gueltig = art.e_gueltig
                        artikel.artnrlager = art.artnrlager
                        artikel.artnrrezept = art.artnrrezept
                        artikel.prozent =  to_decimal(art.prozent)
                        artikel.lagernr = art.lagernr


        create_log()


    def create_log():

        nonlocal anzahl, all_flag, dept1, dept2, art1, art2, overwrite_flag, user_init, wgrpdep, h_artikel, artikel, queasy, hoteldpt, bediener, res_history
        nonlocal subgrp, h_art, art


        nonlocal payload_list, subgrp, h_art, art

        fdept_bezeich:string = ""
        tdept_bezeich:string = ""
        log_msg:string = ""
        overwrite_flag_str:string = "False"
        all_flag_str:string = "False"

        hoteldpt = get_cache (Hoteldpt, {"num": [(eq, dept1)]})

        if hoteldpt:
            fdept_bezeich = hoteldpt.depart

        hoteldpt = get_cache (Hoteldpt, {"num": [(eq, dept2)]})

        if hoteldpt:
            tdept_bezeich = hoteldpt.depart

        if overwrite_flag:
            overwrite_flag_str = "True"

        if all_flag:
            all_flag_str = "True"
        log_msg = "Copy Outlet Article from " + fdept_bezeich + " to " + tdept_bezeich
        log_msg = log_msg + " with article range " + to_string(art1) + " to " + to_string(art2) + "."
        log_msg = log_msg + " Overwrite article: " + to_string(overwrite_flag_str)
        log_msg = log_msg + " Include Payment article: " + to_string(all_flag_str)

        bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

        if bediener:
            res_history = Res_history()
            db_session.add(res_history)

            res_history.nr = bediener.nr
            res_history.datum = get_current_date()
            res_history.zeit = get_current_time_in_seconds()
            res_history.action = "Outlet Article Setup"
            res_history.aenderung = log_msg


    payload_list = query(payload_list_list, first=True)

    if payload_list:
        all_flag = payload_list.all_flag
        dept1 = payload_list.dept1
        dept2 = payload_list.dept2
        art1 = payload_list.art1
        art2 = payload_list.art2
        overwrite_flag = payload_list.overwrite_flag
        user_init = payload_list.user_init

        if not all_flag:
            copy_sales()
        else:
            copy_all()

    return generate_output()