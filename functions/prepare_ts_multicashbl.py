#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Waehrung, H_artikel, Artikel, Exrate

def prepare_ts_multicashbl(dept:int, transdate:date, amt:Decimal):

    prepare_cache ([Htparam, Waehrung, H_artikel, Artikel, Exrate])

    price_decimal = 0
    billdate = None
    curr_local = ""
    billart = 0
    max_gpos = 0
    art_exrate = to_decimal("0.0")
    amount = to_decimal("0.0")
    paid = to_decimal("0.0")
    lpaid = to_decimal("0.0")
    change = to_decimal("0.0")
    lchange = to_decimal("0.0")
    err_flag = 0
    grp_list_data = []
    htparam = waehrung = h_artikel = artikel = exrate = None

    grp_list = None

    grp_list_data, Grp_list = create_model("Grp_list", {"pos":int, "num":int, "bezeich":string, "artname":string, "curr":string, "exrate":Decimal, "exrate1":Decimal}, {"exrate": 1, "exrate1": 1})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal price_decimal, billdate, curr_local, billart, max_gpos, art_exrate, amount, paid, lpaid, change, lchange, err_flag, grp_list_data, htparam, waehrung, h_artikel, artikel, exrate
        nonlocal dept, transdate, amt


        nonlocal grp_list
        nonlocal grp_list_data

        return {"price_decimal": price_decimal, "billdate": billdate, "curr_local": curr_local, "billart": billart, "max_gpos": max_gpos, "art_exrate": art_exrate, "amount": amount, "paid": paid, "lpaid": lpaid, "change": change, "lchange": lchange, "err_flag": err_flag, "grp-list": grp_list_data}

    def build_glist():

        nonlocal price_decimal, billdate, curr_local, billart, max_gpos, art_exrate, amount, paid, lpaid, change, lchange, err_flag, grp_list_data, htparam, waehrung, h_artikel, artikel, exrate
        nonlocal dept, transdate, amt


        nonlocal grp_list
        nonlocal grp_list_data

        i:int = 1
        local_artnr:int = 0

        htparam = get_cache (Htparam, {"paramnr": [(eq, 855)]})

        h_artikel = get_cache (H_artikel, {"departement": [(eq, dept)],"artnr": [(eq, htparam.finteger)]})

        if not h_artikel:
            err_flag = 1

            return

        htparam = get_cache (Htparam, {"paramnr": [(eq, 152)]})
        curr_local = htparam.fchar
        grp_list = Grp_list()
        grp_list_data.append(grp_list)

        grp_list.pos = 1
        grp_list.num = h_artikel.artnr
        grp_list.bezeich = curr_local
        grp_list.artname = h_artikel.bezeich
        local_artnr = h_artikel.artnr
        billart = h_artikel.artnr

        for h_artikel in db_session.query(H_artikel).filter(
                 (H_artikel.departement == dept) & (H_artikel.artart == 6) & (H_artikel.artnr != local_artnr)).order_by(H_artikel.bezeich).all():

            artikel = get_cache (Artikel, {"departement": [(eq, 0)],"artnr": [(eq, h_artikel.artnrfront)],"pricetab": [(eq, True)]})

            if artikel:

                if artikel.pricetab:

                    waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, artikel.betriebsnr)]})

                    if waehrung:
                        i = i + 1
                        grp_list = Grp_list()
                        grp_list_data.append(grp_list)

                        grp_list.pos = i
                        grp_list.num = h_artikel.artnr
                        grp_list.bezeich = waehrung.wabkurz
                        grp_list.artname = h_artikel.bezeich
                        grp_list.exrate = ( to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit) )
                        grp_list.exrate1 =  to_decimal(waehrung.einheit)

                        if (transdate != None) and (transdate < billdate):

                            exrate = get_cache (Exrate, {"artnr": [(eq, waehrung.waehrungsnr)],"datum": [(eq, transdate)]})

                            if exrate:
                                grp_list.exrate =  to_decimal(exrate.betrag)
                                grp_list.exrate1 =  to_decimal(exrate.betrag)


                else:
                    i = i + 1
                    grp_list = Grp_list()
                    grp_list_data.append(grp_list)

                    grp_list.pos = i
                    grp_list.num = h_artikel.artnr
                    grp_list.bezeich = curr_local
                    grp_list.artname = h_artikel.bezeich


        max_gpos = i


    htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
    price_decimal = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    billdate = htparam.fdate
    build_glist()

    grp_list = query(grp_list_data, first=True)

    waehrung = get_cache (Waehrung, {"wabkurz": [(eq, grp_list.bezeich)]})
    art_exrate =  to_decimal(grp_list.exrate)
    amount = to_decimal(round(amt / grp_list.exrate , 2))
    paid =  - to_decimal(amount)
    lpaid =  - to_decimal(amt)
    change =  to_decimal("0")
    lchange =  to_decimal("0")

    return generate_output()