from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam, L_artikel, L_untergrup, Gl_acct, L_besthis, L_bestand

def inv_checking_end_glbl(frnr:int, tonr:int, d2:date, saldo:decimal):
    s_list3_list = []
    art_list_list = []
    inv_date:date = None
    saldo1:decimal = 0
    saldo2:decimal = 0
    htparam = l_artikel = l_untergrup = gl_acct = l_besthis = l_bestand = None

    s_list = s_list3 = art_list = None

    s_list_list, S_list = create_model("S_list", {"fibu":str, "saldo1":decimal, "saldo2":decimal, "saldo":decimal})
    s_list3_list, S_list3 = create_model("S_list3", {"fibu2":str, "saldo1b":decimal, "saldo2b":decimal, "saldo3a":decimal, "saldo11":decimal})
    art_list_list, Art_list = create_model("Art_list", {"artnr":int, "artname":str, "saldo1":decimal, "saldo2":decimal})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal s_list3_list, art_list_list, inv_date, saldo1, saldo2, htparam, l_artikel, l_untergrup, gl_acct, l_besthis, l_bestand


        nonlocal s_list, s_list3, art_list
        nonlocal s_list_list, s_list3_list, art_list_list
        return {"s-list3": s_list3_list, "art-list": art_list_list}

    def end_glhis():

        nonlocal s_list3_list, art_list_list, inv_date, saldo1, saldo2, htparam, l_artikel, l_untergrup, gl_acct, l_besthis, l_bestand


        nonlocal s_list, s_list3, art_list
        nonlocal s_list_list, s_list3_list, art_list_list


        s_list_list.clear()
        s_list3_list.clear()

        if get_month(d2) == 1:
            d2 = date_mdy(12, 31, get_year(d2) - 1)
        else:
            d2 = date_mdy(get_month(d2) , 1, get_year(d2)) - 1

        for l_artikel in db_session.query(L_artikel).filter(
                (L_artikel.artnr >= frnr) &  (L_artikel.artnr <= tonr)).all():
            saldo1 = 0
            saldo2 = 0

            l_untergrup = db_session.query(L_untergrup).filter(
                    (L_untergrup.zwkum == l_artikel.zwkum)).first()

            gl_acct = db_session.query(Gl_acct).filter(
                    (Gl_acct.fibukonto == l_untergrup.fibukonto)).first()

            s_list = query(s_list_list, filters=(lambda s_list :s_list.fibu == gl_acct.fibukonto), first=True)

            if not s_list:
                s_list = S_list()
                s_list_list.append(s_list)

                s_list.fibu = gl_acct.fibukonto
                s_list.saldo2 = gl_acct.actual[get_month(d2) - 1]
                saldo2 = gl_acct.actual[get_month(d2) - 1]

            l_besthis = db_session.query(L_besthis).filter(
                    (L_besthis.anf_best_dat == d2) &  (L_besthis.artnr == l_artikel.artnr) &  (L_besthis.lager_nr == 0)).first()

            if l_besthis:
                s_list.saldo1 = s_list.saldo1 + l_besthis.val_anf_best + l_besthis.wert_eingang -\
                        l_besthis.wert_ausgang
                saldo1 = l_besthis.val_anf_best + l_besthis.wert_eingang -\
                    l_besthis.wert_ausgang


            art_list = Art_list()
            art_list_list.append(art_list)

            art_list.artnr = l_artikel.artnr
            art_list.artname = l_artikel.bezeich
            art_list.saldo1 = saldo1
            art_list.saldo2 = saldo2

        for s_list in query(s_list_list):
            s_list.saldo = saldo
            s_list3 = S_list3()
            s_list3_list.append(s_list3)

            s_list3.fibu2 = s_list.fibu
            s_list3.saldo1b = s_list.saldo1
            s_list3.saldo2b = s_list.saldo2
            s_list3.saldo3a = s_list.saldo1 - s_list.saldo2

    def end_gl():

        nonlocal s_list3_list, art_list_list, inv_date, saldo1, saldo2, htparam, l_artikel, l_untergrup, gl_acct, l_besthis, l_bestand


        nonlocal s_list, s_list3, art_list
        nonlocal s_list_list, s_list3_list, art_list_list


        s_list_list.clear()
        s_list3_list.clear()

        for l_artikel in db_session.query(L_artikel).filter(
                (L_artikel.artnr >= frnr) &  (L_artikel.artnr <= tonr)).all():
            saldo1 = 0
            saldo2 = 0

            l_untergrup = db_session.query(L_untergrup).filter(
                    (L_untergrup.zwkum == l_artikel.zwkum)).first()

            gl_acct = db_session.query(Gl_acct).filter(
                    (Gl_acct.fibukonto == l_untergrup.fibukonto)).first()

            s_list = query(s_list_list, filters=(lambda s_list :s_list.fibu == gl_acct.fibukonto), first=True)

            if not s_list:
                s_list = S_list()
                s_list_list.append(s_list)

                s_list.fibu = gl_acct.fibukonto
                s_list.saldo2 = gl_acct.actual[get_month(d2) - 1]
                saldo2 = gl_acct.actual[get_month(d2) - 1]

            l_bestand = db_session.query(L_bestand).filter(
                    (L_bestand.artnr == l_artikel.artnr) &  (L_bestand.lager_nr == 0)).first()

            if l_bestand:
                s_list.saldo1 = s_list.saldo1 + l_bestand.val_anf_best + l_bestand.wert_eingang -\
                        l_bestand.wert_ausgang
                saldo1 = l_bestand.val_anf_best + l_bestand.wert_eingang -\
                    l_bestand.wert_ausgang


            art_list = Art_list()
            art_list_list.append(art_list)

            art_list.artnr = l_artikel.artnr
            art_list.artname = l_artikel.bezeich
            art_list.saldo1 = saldo1
            art_list.saldo2 = saldo2

        for s_list in query(s_list_list):
            s_list.saldo = saldo
            s_list3 = S_list3()
            s_list3_list.append(s_list3)

            s_list3.fibu2 = s_list.fibu
            s_list3.saldo1b = s_list.saldo1
            s_list3.saldo2b = s_list.saldo2
            s_list3.saldo3a = s_list.saldo1 - s_list.saldo2

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 224)).first()

    if htparam:
        inv_date = htparam.fdate

    if d2 < inv_date:
        end_glhis()
    else:
        end_gl()

    for s_list3 in query(s_list3_list):

        if s_list3.saldo3a == 0:
            s_list3_list.remove(s_list3)

    return generate_output()