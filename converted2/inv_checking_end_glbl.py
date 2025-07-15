#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, L_artikel, L_untergrup, Gl_acct, L_besthis, L_bestand

def inv_checking_end_glbl(frnr:int, tonr:int, d2:date, saldo:Decimal):

    prepare_cache ([Htparam, L_artikel, L_untergrup, Gl_acct, L_besthis, L_bestand])

    s_list3_data = []
    art_list_data = []
    inv_date:date = None
    saldo1:Decimal = to_decimal("0.0")
    saldo2:Decimal = to_decimal("0.0")
    htparam = l_artikel = l_untergrup = gl_acct = l_besthis = l_bestand = None

    s_list = s_list3 = art_list = None

    s_list_data, S_list = create_model("S_list", {"fibu":string, "saldo1":Decimal, "saldo2":Decimal, "saldo":Decimal})
    s_list3_data, S_list3 = create_model("S_list3", {"fibu2":string, "saldo1b":Decimal, "saldo2b":Decimal, "saldo3a":Decimal, "saldo11":Decimal})
    art_list_data, Art_list = create_model("Art_list", {"artnr":int, "artname":string, "saldo1":Decimal, "saldo2":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal s_list3_data, art_list_data, inv_date, saldo1, saldo2, htparam, l_artikel, l_untergrup, gl_acct, l_besthis, l_bestand
        nonlocal frnr, tonr, d2, saldo


        nonlocal s_list, s_list3, art_list
        nonlocal s_list_data, s_list3_data, art_list_data

        return {"s-list3": s_list3_data, "art-list": art_list_data}

    def end_glhis():

        nonlocal s_list3_data, art_list_data, inv_date, saldo1, saldo2, htparam, l_artikel, l_untergrup, gl_acct, l_besthis, l_bestand
        nonlocal frnr, tonr, d2, saldo


        nonlocal s_list, s_list3, art_list
        nonlocal s_list_data, s_list3_data, art_list_data


        s_list_data.clear()
        s_list3_data.clear()

        if get_month(d2) == 1:
            d2 = date_mdy(12, 31, get_year(d2) - timedelta(days=1))
        else:
            d2 = date_mdy(get_month(d2) , 1, get_year(d2)) - timedelta(days=1)

        for l_artikel in db_session.query(L_artikel).filter(
                 (L_artikel.artnr >= frnr) & (L_artikel.artnr <= tonr)).order_by(L_artikel._recid).all():
            saldo1 =  to_decimal("0")
            saldo2 =  to_decimal("0")

            l_untergrup = get_cache (L_untergrup, {"zwkum": [(eq, l_artikel.zwkum)]})

            gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, l_untergrup.fibukonto)]})

            s_list = query(s_list_data, filters=(lambda s_list: s_list.fibu == gl_acct.fibukonto), first=True)

            if not s_list:
                s_list = S_list()
                s_list_data.append(s_list)

                s_list.fibu = gl_acct.fibukonto
                s_list.saldo2 =  to_decimal(gl_acct.actual[get_month(d2) - 1])
                saldo2 =  to_decimal(gl_acct.actual[get_month(d2) - 1])

            l_besthis = get_cache (L_besthis, {"anf_best_dat": [(eq, d2)],"artnr": [(eq, l_artikel.artnr)],"lager_nr": [(eq, 0)]})

            if l_besthis:
                s_list.saldo1 =  to_decimal(s_list.saldo1) + to_decimal(l_besthis.val_anf_best) + to_decimal(l_besthis.wert_eingang) -\
                        l_besthis.wert_ausgang
                saldo1 =  to_decimal(l_besthis.val_anf_best) + to_decimal(l_besthis.wert_eingang) -\
                    l_besthis.wert_ausgang


            art_list = Art_list()
            art_list_data.append(art_list)

            art_list.artnr = l_artikel.artnr
            art_list.artname = l_artikel.bezeich
            art_list.saldo1 =  to_decimal(saldo1)
            art_list.saldo2 =  to_decimal(saldo2)

        for s_list in query(s_list_data):
            s_list.saldo =  to_decimal(saldo)
            s_list3 = S_list3()
            s_list3_data.append(s_list3)

            s_list3.fibu2 = s_list.fibu
            s_list3.saldo1b =  to_decimal(s_list.saldo1)
            s_list3.saldo2b =  to_decimal(s_list.saldo2)
            s_list3.saldo3a =  to_decimal(s_list.saldo1) - to_decimal(s_list.saldo2)


    def end_gl():

        nonlocal s_list3_data, art_list_data, inv_date, saldo1, saldo2, htparam, l_artikel, l_untergrup, gl_acct, l_besthis, l_bestand
        nonlocal frnr, tonr, d2, saldo


        nonlocal s_list, s_list3, art_list
        nonlocal s_list_data, s_list3_data, art_list_data


        s_list_data.clear()
        s_list3_data.clear()

        for l_artikel in db_session.query(L_artikel).filter(
                 (L_artikel.artnr >= frnr) & (L_artikel.artnr <= tonr)).order_by(L_artikel._recid).all():
            saldo1 =  to_decimal("0")
            saldo2 =  to_decimal("0")

            l_untergrup = get_cache (L_untergrup, {"zwkum": [(eq, l_artikel.zwkum)]})

            gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, l_untergrup.fibukonto)]})

            s_list = query(s_list_data, filters=(lambda s_list: s_list.fibu == gl_acct.fibukonto), first=True)

            if not s_list:
                s_list = S_list()
                s_list_data.append(s_list)

                s_list.fibu = gl_acct.fibukonto
                s_list.saldo2 =  to_decimal(gl_acct.actual[get_month(d2) - 1])
                saldo2 =  to_decimal(gl_acct.actual[get_month(d2) - 1])

            l_bestand = get_cache (L_bestand, {"artnr": [(eq, l_artikel.artnr)],"lager_nr": [(eq, 0)]})

            if l_bestand:
                s_list.saldo1 =  to_decimal(s_list.saldo1) + to_decimal(l_bestand.val_anf_best) + to_decimal(l_bestand.wert_eingang) -\
                        l_bestand.wert_ausgang
                saldo1 =  to_decimal(l_bestand.val_anf_best) + to_decimal(l_bestand.wert_eingang) -\
                    l_bestand.wert_ausgang


            art_list = Art_list()
            art_list_data.append(art_list)

            art_list.artnr = l_artikel.artnr
            art_list.artname = l_artikel.bezeich
            art_list.saldo1 =  to_decimal(saldo1)
            art_list.saldo2 =  to_decimal(saldo2)

        for s_list in query(s_list_data):
            s_list.saldo =  to_decimal(saldo)
            s_list3 = S_list3()
            s_list3_data.append(s_list3)

            s_list3.fibu2 = s_list.fibu
            s_list3.saldo1b =  to_decimal(s_list.saldo1)
            s_list3.saldo2b =  to_decimal(s_list.saldo2)
            s_list3.saldo3a =  to_decimal(s_list.saldo1) - to_decimal(s_list.saldo2)


    htparam = get_cache (Htparam, {"paramnr": [(eq, 224)]})

    if htparam:
        inv_date = htparam.fdate

    if d2 < inv_date:
        end_glhis()
    else:
        end_gl()

    for s_list3 in query(s_list3_data):

        if s_list3.saldo3a == 0:
            s_list3_data.remove(s_list3)

    return generate_output()