#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from sqlalchemy import func
from models import L_ophis, L_op, L_verbrauch, Htparam, L_artikel, L_bestand

def slow_moving_btn_go_3bl(storeno:int, main_grp:int, tage:int, show_price:bool, disptype:string):

    prepare_cache ([L_ophis, L_op, L_verbrauch, Htparam, L_artikel, L_bestand])

    str_flag = ""
    s_list_list = []
    l_ophis = l_op = l_verbrauch = htparam = l_artikel = l_bestand = None

    s_list = lophis_buff = buf_lop = blophis = bl_op = bl_ophis = blop = bl_verbrauch = None

    s_list_list, S_list = create_model("S_list", {"artnr":int, "name":string, "min_oh":Decimal, "curr_oh":Decimal, "avrgprice":Decimal, "ek_aktuell":Decimal, "datum":date, "content":Decimal, "zwkum":int, "endkum":int, "unit":string, "datum2":date})

    Lophis_buff = create_buffer("Lophis_buff",L_ophis)
    Buf_lop = create_buffer("Buf_lop",L_op)
    Blophis = create_buffer("Blophis",L_ophis)
    Bl_op = create_buffer("Bl_op",L_op)
    Bl_ophis = create_buffer("Bl_ophis",L_ophis)
    Blop = create_buffer("Blop",L_op)
    Bl_verbrauch = create_buffer("Bl_verbrauch",L_verbrauch)

    set_cache(L_bestand, (L_bestand.artnr >= main_grp * 1000000) & (L_bestand.artnr <= (main_grp + 1) * 1000000 - 1),[["artnr", "lager_nr"]], True, [],[])
    set_cache(L_op, (L_op.artnr >= main_grp * 1000000) & (L_op.artnr <= (main_grp + 1) * 1000000 - 1),[["artnr", "op_art", "lager_nr"], ["artnr", "lager_nr"]], True, ["datum"],[])

    db_session = local_storage.db_session

    def generate_output():
        nonlocal str_flag, s_list_list, l_ophis, l_op, l_verbrauch, htparam, l_artikel, l_bestand
        nonlocal storeno, main_grp, tage, show_price, disptype
        nonlocal lophis_buff, buf_lop, blophis, bl_op, bl_ophis, blop, bl_verbrauch


        nonlocal s_list, lophis_buff, buf_lop, blophis, bl_op, bl_ophis, blop, bl_verbrauch
        nonlocal s_list_list

        return {"str_flag": str_flag, "s-list": s_list_list}

    def create_list():

        nonlocal str_flag, s_list_list, l_ophis, l_op, l_verbrauch, htparam, l_artikel, l_bestand
        nonlocal storeno, main_grp, tage, show_price, disptype
        nonlocal lophis_buff, buf_lop, blophis, bl_op, bl_ophis, blop, bl_verbrauch


        nonlocal s_list, lophis_buff, buf_lop, blophis, bl_op, bl_ophis, blop, bl_verbrauch
        nonlocal s_list_list

        n1:int = 0
        n2:int = 0
        curr_best:Decimal = to_decimal("0.0")
        transdate:date = None
        n1 = main_grp * 1000000
        n2 = (main_grp + 1) * 1000000 - 1

        htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
        transdate = htparam.fdate
        s_list_list.clear()
        str_flag = "INN"

        for l_artikel in db_session.query(L_artikel).filter(
                 (L_artikel.artnr >= n1) & (L_artikel.artnr <= n2)).order_by(L_artikel._recid).all():
            curr_best =  to_decimal("0")

            l_bestand = get_cache (L_bestand, {"artnr": [(eq, l_artikel.artnr)],"lager_nr": [(eq, storeno)]})

            if l_bestand:
                curr_best =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)

            if curr_best > 0:

                for l_op in db_session.query(L_op).filter(
                         (L_op.artnr == l_artikel.artnr) & (L_op.loeschflag <= 1) & (L_op.op_art == 1) & (L_op.lager_nr == storeno) & (L_op.datum <= transdate)).order_by(L_op.datum.desc()).all():

                    if l_op.datum <= (transdate - timedelta(days=tage)):

                        blop = get_cache (L_op, {"artnr": [(eq, l_op.artnr)],"op_art": [(eq, l_op.op_art)],"lager_nr": [(eq, l_op.lager_nr)],"datum": [(gt, l_op.datum)]})

                        if not blop:

                            s_list = query(s_list_list, filters=(lambda s_list: s_list.artnr == l_artikel.artnr), first=True)

                            if not s_list:

                                for bl_op in db_session.query(Bl_op).filter(
                                         (Bl_op.artnr == l_op.artnr) & (Bl_op.loeschflag <= 1) & (Bl_op.op_art == 1) & (Bl_op.lager_nr == storeno) & (Bl_op.datum <= (transdate - timedelta(days=tage)))).order_by(Bl_op.datum.desc()).yield_per(100):
                                    s_list = S_list()
                                    s_list_list.append(s_list)

                                    s_list.artnr = l_artikel.artnr
                                    s_list.name = l_artikel.bezeich
                                    s_list.min_oh =  to_decimal(l_artikel.min_bestand)
                                    s_list.curr_oh =  to_decimal(curr_best)
                                    s_list.content =  to_decimal(l_artikel.inhalt)
                                    s_list.zwkum = l_artikel.zwkum
                                    s_list.endkum = l_artikel.endkum
                                    s_list.unit = l_artikel.masseinheit
                                    s_list.datum = bl_op.datum

                                    if show_price:
                                        s_list.avrgprice =  to_decimal(l_artikel.vk_preis)
                                        s_list.ek_aktuell =  to_decimal(l_artikel.ek_aktuell)
                                    break

                                for bl_ophis in db_session.query(Bl_ophis).filter(
                                         (Bl_ophis.artnr == l_ophis.artnr) & (Bl_ophis.op_art == 3) & (Bl_ophis.lager_nr == storeno) & (Bl_ophis.datum <= l_ophis.datum) & (not_(matches(Bl_ophis.fibukonto,"*CANCELLED*")))).order_by(Bl_ophis.datum.desc()).yield_per(100):
                                    s_list.datum2 = bl_ophis.datum


                                    break

                for l_ophis in db_session.query(L_ophis).filter(
                         (L_ophis.artnr == l_artikel.artnr) & (L_ophis.op_art == 1) & (L_ophis.lager_nr == storeno) & (L_ophis.datum <= transdate) & (not_(matches(L_ophis.fibukonto,"CANCELLED")))).order_by(L_ophis.datum).all():

                    if l_ophis.datum <= (transdate - timedelta(days=tage)):

                        l_op = get_cache (L_op, {"artnr": [(eq, l_ophis.artnr)],"op_art": [(eq, l_ophis.op_art)],"lager_nr": [(eq, l_ophis.lager_nr)],"datum": [(gt, l_ophis.datum)]})

                        if not l_op:

                            blophis = get_cache (L_ophis, {"artnr": [(eq, l_ophis.artnr)],"op_art": [(eq, l_ophis.op_art)],"lager_nr": [(eq, l_ophis.lager_nr)],"datum": [(gt, l_ophis.datum)]})

                            if not blophis:

                                s_list = query(s_list_list, filters=(lambda s_list: s_list.artnr == l_artikel.artnr), first=True)

                                if not s_list:

                                    for bl_ophis in db_session.query(Bl_ophis).filter(
                                             (Bl_ophis.artnr == l_ophis.artnr) & (Bl_ophis.op_art == 1) & (Bl_ophis.lager_nr == storeno) & (Bl_ophis.datum <= (transdate - timedelta(days=tage))) & (not_(matches(Bl_ophis.fibukonto,"CANCELLED")))).order_by(Bl_ophis.datum.desc()).yield_per(100):
                                        s_list = S_list()
                                        s_list_list.append(s_list)

                                        s_list.artnr = l_artikel.artnr
                                        s_list.name = l_artikel.bezeich
                                        s_list.min_oh =  to_decimal(l_artikel.min_bestand)
                                        s_list.curr_oh =  to_decimal(curr_best)
                                        s_list.content =  to_decimal(l_artikel.inhalt)
                                        s_list.zwkum = l_artikel.zwkum
                                        s_list.endkum = l_artikel.endkum
                                        s_list.unit = l_artikel.masseinheit
                                        s_list.datum = bl_ophis.datum

                                        if show_price:
                                            s_list.avrgprice =  to_decimal(l_artikel.vk_preis)
                                            s_list.ek_aktuell =  to_decimal(l_artikel.ek_aktuell)
                                        break

                                    for bl_ophis in db_session.query(Bl_ophis).filter(
                                             (Bl_ophis.artnr == l_ophis.artnr) & (Bl_ophis.op_art == 3) & (Bl_ophis.lager_nr == storeno) & (Bl_ophis.datum <= l_ophis.datum) & (not_(matches(Bl_ophis.fibukonto,"*CANCELLED*")))).order_by(Bl_ophis.datum.desc()).yield_per(100):
                                        s_list.datum2 = bl_ophis.datum


                                        break


    def create_list2():

        nonlocal str_flag, s_list_list, l_ophis, l_op, l_verbrauch, htparam, l_artikel, l_bestand
        nonlocal storeno, main_grp, tage, show_price, disptype
        nonlocal lophis_buff, buf_lop, blophis, bl_op, bl_ophis, blop, bl_verbrauch


        nonlocal s_list, lophis_buff, buf_lop, blophis, bl_op, bl_ophis, blop, bl_verbrauch
        nonlocal s_list_list

        n1:int = 0
        n2:int = 0
        curr_best:Decimal = to_decimal("0.0")
        transdate:date = None
        n1 = main_grp * 1000000
        n2 = (main_grp + 1) * 1000000 - 1

        htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
        transdate = htparam.fdate
        s_list_list.clear()
        str_flag = "OUT"

        for l_artikel in db_session.query(L_artikel).filter(
                 (L_artikel.artnr >= n1) & (L_artikel.artnr <= n2)).order_by(L_artikel.artnr).all():
            curr_best =  to_decimal("0")

            l_bestand = get_cache (L_bestand, {"artnr": [(eq, l_artikel.artnr)],"lager_nr": [(eq, storeno)]})

            if l_bestand:
                curr_best =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)

            if curr_best > 0:

                for l_op in db_session.query(L_op).filter(
                         (L_op.artnr == l_artikel.artnr) & (L_op.op_art == 3) & (L_op.loeschflag <= 1) & (L_op.lager_nr == storeno) & (L_op.datum <= transdate)).order_by(L_op.datum.desc()).all():

                    if l_op.datum <= (transdate - timedelta(days=tage)):

                        blop = get_cache (L_op, {"artnr": [(eq, l_op.artnr)],"op_art": [(eq, l_op.op_art)],"lager_nr": [(eq, l_op.lager_nr)],"datum": [(gt, l_op.datum)]})

                        if not blop:

                            s_list = query(s_list_list, filters=(lambda s_list: s_list.artnr == l_artikel.artnr), first=True)

                            if not s_list:

                                for bl_op in db_session.query(Bl_op).filter(
                                         (Bl_op.artnr == l_op.artnr) & (Bl_op.op_art == 3) & (Bl_op.loeschflag <= 1) & (Bl_op.lager_nr == storeno) & (Bl_op.datum <= (transdate - timedelta(days=tage)))).order_by(Bl_op.datum.desc()).yield_per(100):

                                    bl_verbrauch = db_session.query(Bl_verbrauch).filter(
                                             (Bl_verbrauch.artnr == bl_op.artnr)).order_by(Bl_verbrauch._recid.desc()).first()

                                    if bl_verbrauch:

                                        if bl_verbrauch.datum == bl_op.datum:
                                            s_list = S_list()
                                            s_list_list.append(s_list)

                                            s_list.artnr = l_artikel.artnr
                                            s_list.name = l_artikel.bezeich
                                            s_list.min_oh =  to_decimal(l_artikel.min_bestand)
                                            s_list.curr_oh =  to_decimal(curr_best)
                                            s_list.content =  to_decimal(l_artikel.inhalt)
                                            s_list.zwkum = l_artikel.zwkum
                                            s_list.endkum = l_artikel.endkum
                                            s_list.unit = l_artikel.masseinheit
                                            s_list.datum2 = bl_op.datum

                                            if show_price:
                                                s_list.avrgprice =  to_decimal(l_artikel.vk_preis)
                                                s_list.ek_aktuell =  to_decimal(l_artikel.ek_aktuell)
                                            break

                for l_ophis in db_session.query(L_ophis).filter(
                         (L_ophis.artnr == l_artikel.artnr) & (L_ophis.op_art == 3) & (L_ophis.lager_nr == storeno) & (L_ophis.datum <= transdate) & (not_(matches(L_ophis.fibukonto,"*CANCELLED*")))).order_by(L_ophis.datum.desc()).all():

                    if l_ophis.datum <= (transdate - timedelta(days=tage)):

                        l_op = get_cache (L_op, {"artnr": [(eq, l_ophis.artnr)],"op_art": [(eq, l_ophis.op_art)],"lager_nr": [(eq, l_ophis.lager_nr)],"datum": [(gt, l_ophis.datum)]})

                        if not l_op:

                            blophis = get_cache (L_ophis, {"artnr": [(eq, l_ophis.artnr)],"op_art": [(eq, l_ophis.op_art)],"lager_nr": [(eq, l_ophis.lager_nr)],"datum": [(gt, l_ophis.datum)]})

                            if not blophis:

                                s_list = query(s_list_list, filters=(lambda s_list: s_list.artnr == l_artikel.artnr), first=True)

                                if not s_list:

                                    for bl_ophis in db_session.query(Bl_ophis).filter(
                                             (Bl_ophis.artnr == l_ophis.artnr) & (Bl_ophis.op_art == 3) & (Bl_ophis.lager_nr == storeno) & (Bl_ophis.datum <= (transdate - timedelta(days=tage))) & (not_(matches(Bl_ophis.fibukonto,"*CANCELLED*")))).order_by(Bl_ophis.datum.desc()).yield_per(100):

                                        bl_verbrauch = db_session.query(Bl_verbrauch).filter(
                                                 (Bl_verbrauch.artnr == bl_ophis.artnr)).order_by(Bl_verbrauch._recid.desc()).first()

                                        if bl_verbrauch:

                                            if bl_verbrauch.datum == bl_ophis.datum:
                                                s_list = S_list()
                                                s_list_list.append(s_list)

                                                s_list.artnr = l_artikel.artnr
                                                s_list.name = l_artikel.bezeich
                                                s_list.min_oh =  to_decimal(l_artikel.min_bestand)
                                                s_list.curr_oh =  to_decimal(curr_best)
                                                s_list.content =  to_decimal(l_artikel.inhalt)
                                                s_list.zwkum = l_artikel.zwkum
                                                s_list.endkum = l_artikel.endkum
                                                s_list.unit = l_artikel.masseinheit
                                                s_list.datum2 = bl_ophis.datum

                                                if show_price:
                                                    s_list.avrgprice =  to_decimal(l_artikel.vk_preis)
                                                    s_list.ek_aktuell =  to_decimal(l_artikel.ek_aktuell)
                                                break


    def create_list3():

        nonlocal str_flag, s_list_list, l_ophis, l_op, l_verbrauch, htparam, l_artikel, l_bestand
        nonlocal storeno, main_grp, tage, show_price, disptype
        nonlocal lophis_buff, buf_lop, blophis, bl_op, bl_ophis, blop, bl_verbrauch


        nonlocal s_list, lophis_buff, buf_lop, blophis, bl_op, bl_ophis, blop, bl_verbrauch
        nonlocal s_list_list

        n1:int = 0
        n2:int = 0
        curr_best:Decimal = to_decimal("0.0")
        transdate:date = None
        curr_time:int = 0
        n1 = main_grp * 1000000
        n2 = (main_grp + 1) * 1000000 - 1

        htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
        transdate = htparam.fdate
        s_list_list.clear()
        str_flag = "IN-OUT"

        for l_artikel in db_session.query(L_artikel).filter(
                 (L_artikel.artnr >= n1) & (L_artikel.artnr <= n2)).order_by(L_artikel.artnr).all():
            curr_best =  to_decimal("0")

            l_bestand = get_cache (L_bestand, {"artnr": [(eq, l_artikel.artnr)],"lager_nr": [(eq, storeno)]})

            if l_bestand:
                curr_best =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)

            if curr_best > 0:

                for l_op in db_session.query(L_op).filter(
                         (L_op.artnr == l_artikel.artnr) & ((L_op.op_art == 1) | (L_op.op_art == 3)) & (L_op.loeschflag <= 1) & (L_op.lager_nr == storeno) & (L_op.datum <= transdate)).order_by(L_op._recid).all():

                    if l_op.datum <= (transdate - timedelta(days=tage)):
                        curr_time = get_current_time_in_seconds()

                        if matches(l_op.docu_nr,r"T*") and l_op.stornogrund == "":
                            pass
                        else:

                            blop = get_cache (L_op, {"artnr": [(eq, l_op.artnr)],"op_art": [(eq, l_op.op_art)],"lager_nr": [(eq, l_op.lager_nr)],"datum": [(gt, l_op.datum)]})

                            if not blop:

                                s_list = query(s_list_list, filters=(lambda s_list: s_list.artnr == l_artikel.artnr), first=True)

                                if not s_list:

                                    for bl_op in db_session.query(Bl_op).filter(
                                             (Bl_op.artnr == l_op.artnr) & (Bl_op.op_art == 1) & (Bl_op.loeschflag <= 1) & (Bl_op.lager_nr == storeno) & (Bl_op.datum <= l_op.datum)).order_by(Bl_op.datum.desc()).yield_per(100):
                                        s_list = S_list()
                                        s_list_list.append(s_list)

                                        s_list.artnr = l_artikel.artnr
                                        s_list.name = l_artikel.bezeich
                                        s_list.min_oh =  to_decimal(l_artikel.min_bestand)
                                        s_list.curr_oh =  to_decimal(curr_best)
                                        s_list.content =  to_decimal(l_artikel.inhalt)
                                        s_list.zwkum = l_artikel.zwkum
                                        s_list.endkum = l_artikel.endkum
                                        s_list.unit = l_artikel.masseinheit
                                        s_list.datum = bl_op.datum

                                        if show_price:
                                            s_list.avrgprice =  to_decimal(l_artikel.vk_preis)
                                            s_list.ek_aktuell =  to_decimal(l_artikel.ek_aktuell)


                                        break

                                    for bl_op in db_session.query(Bl_op).filter(
                                             (Bl_op.artnr == l_op.artnr) & (Bl_op.op_art == 3) & (Bl_op.loeschflag <= 1) & (Bl_op.lager_nr == storeno) & (Bl_op.datum <= l_op.datum)).order_by(Bl_op.datum.desc()).yield_per(100):
                                        s_list.datum2 = bl_op.datum


                                        break

                for l_ophis in db_session.query(L_ophis).filter(
                             (L_ophis.artnr == l_artikel.artnr) & ((L_ophis.op_art == 1) | (L_ophis.op_art == 3)) & (L_ophis.lager_nr == storeno) & (L_ophis.datum <= transdate) & (not_(matches(L_ophis.fibukonto,"*CANCELLED*")))).order_by(L_ophis._recid).all():

                    if l_ophis.datum <= (transdate - timedelta(days=tage)):

                        l_op = get_cache (L_op, {"artnr": [(eq, l_ophis.artnr)],"lager_nr": [(eq, l_ophis.lager_nr)],"datum": [(gt, l_ophis.datum)]})

                        if not l_op:

                            blophis = get_cache (L_ophis, {"artnr": [(eq, l_ophis.artnr)],"lager_nr": [(eq, l_ophis.lager_nr)],"datum": [(gt, l_ophis.datum)]})

                            if not blophis:

                                s_list = query(s_list_list, filters=(lambda s_list: s_list.artnr == l_artikel.artnr), first=True)

                                if not s_list:

                                    for bl_ophis in db_session.query(Bl_ophis).filter(
                                                 (Bl_ophis.artnr == l_ophis.artnr) & (Bl_ophis.op_art == 1) & (Bl_ophis.lager_nr == storeno) & (Bl_ophis.datum <= l_ophis.datum) & (not_(matches(Bl_ophis.fibukonto,"*CANCELLED*")))).order_by(Bl_ophis.datum.desc()).yield_per(100):
                                        s_list = S_list()
                                        s_list_list.append(s_list)

                                        s_list.artnr = l_artikel.artnr
                                        s_list.name = l_artikel.bezeich
                                        s_list.min_oh =  to_decimal(l_artikel.min_bestand)
                                        s_list.curr_oh =  to_decimal(curr_best)
                                        s_list.content =  to_decimal(l_artikel.inhalt)
                                        s_list.zwkum = l_artikel.zwkum
                                        s_list.endkum = l_artikel.endkum
                                        s_list.unit = l_artikel.masseinheit
                                        s_list.datum = bl_ophis.datum

                                        if show_price:
                                            s_list.avrgprice =  to_decimal(l_artikel.vk_preis)
                                            s_list.ek_aktuell =  to_decimal(l_artikel.ek_aktuell)
                                        break

                                    for bl_ophis in db_session.query(Bl_ophis).filter(
                                                 (Bl_ophis.artnr == l_ophis.artnr) & (Bl_ophis.op_art == 3) & (Bl_ophis.lager_nr == storeno) & (Bl_ophis.datum <= l_ophis.datum) & (not_(matches(Bl_ophis.fibukonto,"*CANCELLED*")))).order_by(Bl_ophis.datum.desc()).yield_per(100):
                                        s_list.datum2 = bl_ophis.datum


                                        break

    s_list_list.clear()

    if disptype.lower()  == ("old").lower() :
        create_list()

    elif disptype.lower()  == ("new").lower() :
        create_list2()
    else:
        create_list3()

    return generate_output()