from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam, L_artikel, L_bestand, L_op, L_ophis, L_pprice

def slow_moving_btn_gobl(storeno:int, main_grp:int, tage:int, show_price:bool):
    s_list_list = []
    htparam = l_artikel = l_bestand = l_op = l_ophis = l_pprice = None

    s_list = None

    s_list_list, S_list = create_model("S_list", {"artnr":int, "name":str, "min_oh":decimal, "curr_oh":decimal, "avrgprice":decimal, "ek_aktuell":decimal, "datum":date})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal s_list_list, htparam, l_artikel, l_bestand, l_op, l_ophis, l_pprice


        nonlocal s_list
        nonlocal s_list_list
        return {"s-list": s_list_list}

    def create_list1():

        nonlocal s_list_list, htparam, l_artikel, l_bestand, l_op, l_ophis, l_pprice


        nonlocal s_list
        nonlocal s_list_list

        n1:int = 0
        n2:int = 0
        curr_best:decimal = 0
        transdate:date = None
        n1 = main_grp * 1000000
        n2 = (main_grp + 1) * 1000000 - 1

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 110)).first()
        transdate = htparam.fdate
        s_list_list.clear()

        for l_artikel in db_session.query(L_artikel).filter(
                (L_artikel.artnr >= n1) &  (L_artikel.artnr <= n2)).all():
            curr_best = 0

            l_bestand = db_session.query(L_bestand).filter(
                    (L_bestand.artnr == l_artikel.artnr) &  (L_bestand.lager_nr == storeno)).first()

            if l_bestand:
                curr_best = l_bestand.anz_anf_best + l_bestand.anz_eingang - l_bestand.anz_ausgang

            if curr_best > 0:

                l_op = db_session.query(L_op).filter(
                        (L_op.op_art == 3) &  (L_op.loeschflag <= 1) &  (L_op.artnr == l_artikel.artnr) &  (L_op.lager_nr == storeno)).first()

                if not l_op:

                    l_op = db_session.query(L_op).filter(
                            (L_op.op_art == 1) &  (L_op.loeschflag <= 1) &  (L_op.artnr == l_artikel.artnr) &  (L_op.lager_nr == storeno)).first()

                if not l_op:

                    l_ophis = db_session.query(L_ophis).filter(
                            (L_ophis.artnr == l_artikel.artnr) &  (L_ophis.op_art == 3) &  (L_ophis.datum >= (transdate - tage)) &  (L_ophis.lager_nr == storeno)).first()

                    if not l_ophis:

                        l_ophis = db_session.query(L_ophis).filter(
                                (L_ophis.artnr == l_artikel.artnr) &  (L_ophis.op_art == 1) &  (L_ophis.datum >= (transdate - tage)) &  (L_ophis.lager_nr == storeno)).first()

                    if not l_ophis:
                        s_list = S_list()
                        s_list_list.append(s_list)

                        s_list.artnr = l_artikel.artnr
                        s_list.name = l_artikel.bezeich
                        s_list.min_oh = l_artikel.min_best
                        s_list.curr_oh = curr_best

                        if show_price:
                            s_list.avrgprice = l_artikel.vk_preis
                            s_list.ek_aktuell = l_artikel.ek_aktuell

                        if l_artikel.lieferfrist > 0:

                            l_pprice = db_session.query(L_pprice).filter(
                                    (L_pprice.artnr == l_artikel.artnr) &  (L_pprice.counter == l_artikel.lieferfrist)).first()

                            if l_pprice:
                                s_list.datum = l_pprice.bestelldatum

    def create_list():

        nonlocal s_list_list, htparam, l_artikel, l_bestand, l_op, l_ophis, l_pprice


        nonlocal s_list
        nonlocal s_list_list

        n1:int = 0
        n2:int = 0
        curr_best:decimal = 0
        transdate:date = None
        n1 = main_grp * 1000000
        n2 = (main_grp + 1) * 1000000 - 1

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 110)).first()
        transdate = htparam.fdate
        s_list_list.clear()

        for l_artikel in db_session.query(L_artikel).filter(
                (L_artikel.artnr >= n1) &  (L_artikel.artnr <= n2)).all():
            curr_best = 0

            l_bestand = db_session.query(L_bestand).filter(
                    (L_bestand.artnr == l_artikel.artnr) &  (L_bestand.lager_nr == 0)).first()

            if l_bestand:
                curr_best = l_bestand.anz_anf_best + l_bestand.anz_eingang - l_bestand.anz_ausgang

            if curr_best > 0:

                l_op = db_session.query(L_op).filter(
                        (L_op.op_art == 3) &  (L_op.loeschflag <= 1) &  (L_op.artnr == l_artikel.artnr)).first()

                if not l_op:

                    l_op = db_session.query(L_op).filter(
                            (L_op.op_art == 1) &  (L_op.loeschflag <= 1) &  (L_op.artnr == l_artikel.artnr)).first()

                if not l_op:

                    l_ophis = db_session.query(L_ophis).filter(
                            (L_ophis.artnr == l_artikel.artnr) &  (L_ophis.op_art == 3) &  (L_ophis.datum >= (transdate - tage))).first()

                    if not l_ophis:

                        l_ophis = db_session.query(L_ophis).filter(
                                (L_ophis.artnr == l_artikel.artnr) &  (L_ophis.op_art == 1) &  (L_ophis.datum >= (transdate - tage))).first()

                    if not l_ophis:
                        s_list = S_list()
                        s_list_list.append(s_list)

                        s_list.artnr = l_artikel.artnr
                        s_list.name = l_artikel.bezeich
                        s_list.min_oh = l_artikel.min_best
                        s_list.curr_oh = curr_best

                        if show_price:
                            s_list.avrgprice = l_artikel.vk_preis
                            s_list.ek_aktuell = l_artikel.ek_aktuell

                        if l_artikel.lieferfrist > 0:

                            l_pprice = db_session.query(L_pprice).filter(
                                    (L_pprice.artnr == l_artikel.artnr) &  (L_pprice.counter == l_artikel.lieferfrist)).first()

                            if l_pprice:
                                s_list.datum = l_pprice.bestelldatum

    if storeno == 0:
        create_list()
    else:
        create_list1()

    return generate_output()