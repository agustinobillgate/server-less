#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Paramtext

tt_prices_list, Tt_prices = create_model("Tt_prices", {"i_counter":int, "prices":int})
tt_zeiten_list, Tt_zeiten = create_model("Tt_zeiten", {"i_counter":int, "zeiten":int})

def h_2ndprice_paramtextbl(tt_prices_list:[Tt_prices], tt_zeiten_list:[Tt_zeiten], case_type:int, dept:int, tolerance:int):

    prepare_cache ([Paramtext])

    avail_paramtext = False
    t_sprachcode = 0
    t_ptexte = ""
    t_notes = ""
    prices:List[int] = create_empty_list(24,0)
    zeiten:List[int] = create_empty_list(24,0)
    curr_i:int = 0
    paramtext = None

    tt_prices = tt_zeiten = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_paramtext, t_sprachcode, t_ptexte, t_notes, prices, zeiten, curr_i, paramtext
        nonlocal case_type, dept, tolerance


        nonlocal tt_prices, tt_zeiten

        return {"avail_paramtext": avail_paramtext, "t_sprachcode": t_sprachcode, "t_ptexte": t_ptexte, "t_notes": t_notes}

    def fill_paramtext():

        nonlocal avail_paramtext, t_sprachcode, t_ptexte, t_notes, prices, zeiten, curr_i, paramtext
        nonlocal case_type, dept, tolerance


        nonlocal tt_prices, tt_zeiten

        i:int = 0
        paramtext.ptexte = ""
        paramtext.notes = ""
        for i in range(1,24 + 1) :
            paramtext.ptexte = paramtext.ptexte + to_string(prices[i - 1], "9")
            paramtext.notes = paramtext.notes + to_string(zeiten[i - 1], "9")
        paramtext.sprachcode = tolerance

    tt_prices = query(tt_prices_list, first=True)

    tt_zeiten = query(tt_zeiten_list, first=True)

    for tt_prices in query(tt_prices_list):
        prices[tt_prices.i_counter - 1] = tt_prices.prices

    for tt_zeiten in query(tt_zeiten_list):
        zeiten[tt_zeiten.i_counter - 1] = tt_zeiten.zeiten

    paramtext = get_cache (Paramtext, {"txtnr": [(eq, (10000 + dept))],"number": [(eq, dept)]})

    if paramtext:
        avail_paramtext = True
        t_sprachcode = paramtext.sprachcode
        t_ptexte = paramtext.ptexte
        t_notes = paramtext.notes

    if case_type == 1:

        if not paramtext:
            paramtext = Paramtext()
            db_session.add(paramtext)

            paramtext.txtnr = 10000 + dept
            paramtext.number = dept
        fill_paramtext()

    return generate_output()