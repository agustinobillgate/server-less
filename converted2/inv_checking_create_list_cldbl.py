#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, L_artikel, L_untergrup, Gl_acct, L_besthis, L_bestand

def inv_checking_create_list_cldbl(invtype:int, d1:date):

    prepare_cache ([Htparam, L_artikel, L_untergrup, Gl_acct, L_besthis, L_bestand])

    saldo = to_decimal("0.0")
    s_list2_data = []
    art_list2_data = []
    mon:int = 0
    art1:int = 0
    art2:int = 0
    frnr:int = 0
    tonr:int = 0
    saldo1:Decimal = to_decimal("0.0")
    saldo2:Decimal = to_decimal("0.0")
    inv_date:date = None
    htparam = l_artikel = l_untergrup = gl_acct = l_besthis = l_bestand = None

    s_list2 = s_list = coa_list = art_list2 = None

    s_list2_data, S_list2 = create_model("S_list2", {"fibu1":string, "saldo1a":Decimal, "saldo2a":Decimal, "saldo1":Decimal, "saldo3":Decimal})
    s_list_data, S_list = create_model("S_list", {"fibu":string, "saldo1":Decimal, "saldo2":Decimal, "saldo":Decimal})
    coa_list_data, Coa_list = create_model("Coa_list", {"fibukonto":string, "datum":date, "wert":Decimal, "debit":Decimal, "credit":Decimal})
    art_list2_data, Art_list2 = create_model("Art_list2", {"artnr":int, "artname":string, "saldo1":Decimal, "saldo2":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal saldo, s_list2_data, art_list2_data, mon, art1, art2, frnr, tonr, saldo1, saldo2, inv_date, htparam, l_artikel, l_untergrup, gl_acct, l_besthis, l_bestand
        nonlocal invtype, d1


        nonlocal s_list2, s_list, coa_list, art_list2
        nonlocal s_list2_data, s_list_data, coa_list_data, art_list2_data

        return {"saldo": saldo, "s-list2": s_list2_data, "art-list2": art_list2_data}

    def create_listhis():

        nonlocal saldo, s_list2_data, art_list2_data, mon, art1, art2, frnr, tonr, saldo1, saldo2, inv_date, htparam, l_artikel, l_untergrup, gl_acct, l_besthis, l_bestand
        nonlocal invtype, d1


        nonlocal s_list2, s_list, coa_list, art_list2
        nonlocal s_list2_data, s_list_data, coa_list_data, art_list2_data


        coa_list_data.clear()
        s_list_data.clear()
        s_list2_data.clear()

        if invtype == 0:

            return
        mon = get_month(d1) - 1
        d1 = date_mdy(get_month(d1) , get_day(d1) , get_year(d1)) - timedelta(days=1)
        d1 = date_mdy(get_month(d1) , 1, get_year(d1))

        if invtype == 1:
            art1 = 3
            art2 = 5
            frnr = 1000000
            tonr = 1999999

        elif invtype == 2:
            art1 = 6
            art2 = 6
            frnr = 2000000
            tonr = 2999999

        if invtype == 3:
            frnr = 3000000
            tonr = 9999999

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


                if mon > 0:
                    s_list.fibu = gl_acct.fibukonto
                    s_list.saldo2 =  to_decimal(gl_acct.actual[mon - 1])
                    saldo2 =  to_decimal(gl_acct.actual[mon - 1])


                else:
                    s_list.fibu = gl_acct.fibukonto
                    s_list.saldo2 =  to_decimal(gl_acct.last_yr[11])
                    saldo2 =  to_decimal(gl_acct.last_yr[11])

            l_besthis = get_cache (L_besthis, {"anf_best_dat": [(eq, d1)],"artnr": [(eq, l_artikel.artnr)],"lager_nr": [(eq, 0)]})

            if l_besthis:
                s_list.saldo1 =  to_decimal(s_list.saldo1) + to_decimal(l_besthis.val_anf_best)
                saldo1 =  to_decimal(l_besthis.val_anf_best)


            art_list2 = Art_list2()
            art_list2_data.append(art_list2)

            art_list2.artnr = l_artikel.artnr
            art_list2.artname = l_artikel.bezeich
            art_list2.saldo1 =  to_decimal(saldo1)
            art_list2.saldo2 =  to_decimal(saldo2)


        saldo =  to_decimal("0")

        for s_list in query(s_list_data):
            saldo =  to_decimal(saldo) + to_decimal(s_list.saldo1) - to_decimal(s_list.saldo2)
            s_list.saldo =  to_decimal(saldo)
            s_list2 = S_list2()
            s_list2_data.append(s_list2)

            s_list2.fibu = s_list.fibu
            s_list2.saldo1a =  to_decimal(s_list.saldo1)
            s_list2.saldo2a =  to_decimal(s_list.saldo2)
            s_list2.saldo3 =  to_decimal(s_list.saldo1) - to_decimal(s_list.saldo2)
            s_list2.saldo1 =  to_decimal(s_list.saldo)


    def create_list():

        nonlocal saldo, s_list2_data, art_list2_data, mon, art1, art2, frnr, tonr, saldo1, saldo2, inv_date, htparam, l_artikel, l_untergrup, gl_acct, l_besthis, l_bestand
        nonlocal invtype, d1


        nonlocal s_list2, s_list, coa_list, art_list2
        nonlocal s_list2_data, s_list_data, coa_list_data, art_list2_data


        coa_list_data.clear()
        s_list_data.clear()
        s_list2_data.clear()

        if invtype == 0:

            return
        mon = get_month(d1) - 1

        if invtype == 1:
            art1 = 3
            art2 = 5
            frnr = 1000000
            tonr = 1999999

        elif invtype == 2:
            art1 = 6
            art2 = 6
            frnr = 2000000
            tonr = 2999999

        if invtype == 3:
            frnr = 3000000
            tonr = 9999999

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


                if mon > 0:
                    s_list.fibu = gl_acct.fibukonto
                    s_list.saldo2 =  to_decimal(gl_acct.actual[mon - 1])
                    saldo2 =  to_decimal(gl_acct.actual[mon - 1])


                else:
                    s_list.fibu = gl_acct.fibukonto
                    s_list.saldo2 =  to_decimal(gl_acct.last_yr[11])
                    saldo2 =  to_decimal(gl_acct.last_yr[11])

            l_bestand = get_cache (L_bestand, {"artnr": [(eq, l_artikel.artnr)],"lager_nr": [(eq, 0)]})

            if l_bestand:
                s_list.saldo1 =  to_decimal(s_list.saldo1) + to_decimal(l_bestand.val_anf_best)
                saldo1 =  to_decimal(l_bestand.val_anf_best)


            art_list2 = Art_list2()
            art_list2_data.append(art_list2)

            art_list2.artnr = l_artikel.artnr
            art_list2.artname = l_artikel.bezeich
            art_list2.saldo1 =  to_decimal(saldo1)
            art_list2.saldo2 =  to_decimal(saldo2)


        saldo =  to_decimal("0")

        for s_list in query(s_list_data):
            saldo =  to_decimal(saldo) + to_decimal(s_list.saldo1) - to_decimal(s_list.saldo2)
            s_list.saldo =  to_decimal(saldo)
            s_list2 = S_list2()
            s_list2_data.append(s_list2)

            s_list2.fibu = s_list.fibu
            s_list2.saldo1a =  to_decimal(s_list.saldo1)
            s_list2.saldo2a =  to_decimal(s_list.saldo2)
            s_list2.saldo3 =  to_decimal(s_list.saldo1) - to_decimal(s_list.saldo2)
            s_list2.saldo1 =  to_decimal(s_list.saldo)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 224)]})

    if htparam:
        inv_date = htparam.fdate

    if d1 < inv_date:
        create_listhis()
    else:
        create_list()

    return generate_output()