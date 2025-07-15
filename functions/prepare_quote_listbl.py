#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Waehrung, L_lieferant, L_artikel, L_quote

def prepare_quote_listbl(artno:int, supno:int, docuno:string):

    prepare_cache ([Htparam, Waehrung, L_lieferant, L_artikel])

    prog_path = ""
    prog_name = ""
    bill_date = None
    local_curr = ""
    quote_list_data = []
    htparam = waehrung = l_lieferant = l_artikel = l_quote = None

    quote_list = None

    quote_list_data, Quote_list = create_model("Quote_list", {"artnr":int, "lief_nr":int, "supname":string, "artname":string, "devunit":string, "content":Decimal, "unitprice":Decimal, "curr":string, "from_date":date, "to_date":date, "remark":string, "filname":string, "activeflag":bool, "docu_nr":string, "minqty":Decimal, "delivday":int, "disc":Decimal, "avl":bool}, {"activeflag": True, "avl": True})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal prog_path, prog_name, bill_date, local_curr, quote_list_data, htparam, waehrung, l_lieferant, l_artikel, l_quote
        nonlocal artno, supno, docuno


        nonlocal quote_list
        nonlocal quote_list_data

        return {"prog_path": prog_path, "prog_name": prog_name, "bill_date": bill_date, "local_curr": local_curr, "quote-list": quote_list_data}

    def cr_lquote():

        nonlocal prog_path, prog_name, bill_date, local_curr, quote_list_data, htparam, waehrung, l_lieferant, l_artikel, l_quote
        nonlocal artno, supno, docuno


        nonlocal quote_list
        nonlocal quote_list_data


        quote_list = Quote_list()
        quote_list_data.append(quote_list)

        buffer_copy(l_quote, quote_list)
        quote_list.supname = trim(l_lieferant.anredefirma + " " + firma)
        quote_list.artname = l_artikel.bezeich
        quote_list.devunit = l_artikel.traubensorte
        quote_list.content =  to_decimal(l_artikel.lief_einheit)
        quote_list.curr = l_quote.reserve_char[0]
        quote_list.minqty =  to_decimal(l_quote.reserve_deci[0])
        quote_list.disc =  to_decimal(l_quote.reserve_deci[1])
        quote_list.avl = not l_quote.reserve_logic[0]
        quote_list.delivday = l_quote.reserve_int[0]


    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})

    if htparam:
        bill_date = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 400)]})

    if htparam.fchar != "":
        prog_path = htparam.fchar
    else:
        prog_path = "\\""program files""\\""microsoft office""\\office\\"

    htparam = get_cache (Htparam, {"paramnr": [(eq, 405)]})

    if htparam.fchar != "":
        prog_name = htparam.fchar
    else:
        prog_name = "winword.exe"

    htparam = get_cache (Htparam, {"paramnr": [(eq, 152)]})

    waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

    if not waehrung:

        waehrung = db_session.query(Waehrung).first()

    if waehrung:
        local_curr = waehrung.wabkurz

    if artno != 0 and supno == 0 and docuno == "":

        l_quote_obj_list = {}
        for l_quote, l_lieferant, l_artikel in db_session.query(L_quote, L_lieferant, L_artikel).join(L_lieferant,(L_lieferant.lief_nr == L_quote.lief_nr)).join(L_artikel,(L_artikel.artnr == L_quote.artnr)).filter(
                 (L_quote.reserve_int[inc_value(4)] <= 1) & (L_quote.artnr == artno)).order_by(L_quote._recid).all():
            if l_quote_obj_list.get(l_quote._recid):
                continue
            else:
                l_quote_obj_list[l_quote._recid] = True


            cr_lquote()


    elif supno != 0 and artno == 0 and docuno == "":

        l_quote_obj_list = {}
        for l_quote, l_lieferant, l_artikel in db_session.query(L_quote, L_lieferant, L_artikel).join(L_lieferant,(L_lieferant.lief_nr == L_quote.lief_nr)).join(L_artikel,(L_artikel.artnr == L_quote.artnr)).filter(
                 (L_quote.reserve_int[inc_value(4)] <= 1) & (L_quote.lief_nr == supno)).order_by(L_quote._recid).all():
            if l_quote_obj_list.get(l_quote._recid):
                continue
            else:
                l_quote_obj_list[l_quote._recid] = True


            cr_lquote()


    elif docuno != "" and artno == 0 and supno == 0:

        l_quote_obj_list = {}
        for l_quote, l_lieferant, l_artikel in db_session.query(L_quote, L_lieferant, L_artikel).join(L_lieferant,(L_lieferant.lief_nr == L_quote.lief_nr)).join(L_artikel,(L_artikel.artnr == L_quote.artnr)).filter(
                 (L_quote.reserve_int[inc_value(4)] <= 1) & (L_quote.docu_nr == docuno)).order_by(L_quote._recid).all():
            if l_quote_obj_list.get(l_quote._recid):
                continue
            else:
                l_quote_obj_list[l_quote._recid] = True


            cr_lquote()


    elif artno != 0 and supno != 0 and docuno == "":

        l_quote_obj_list = {}
        for l_quote, l_lieferant, l_artikel in db_session.query(L_quote, L_lieferant, L_artikel).join(L_lieferant,(L_lieferant.lief_nr == L_quote.lief_nr)).join(L_artikel,(L_artikel.artnr == L_quote.artnr)).filter(
                 (L_quote.reserve_int[inc_value(4)] <= 1) & (L_quote.lief_nr == supno) & (L_quote.artnr == artno)).order_by(L_quote._recid).all():
            if l_quote_obj_list.get(l_quote._recid):
                continue
            else:
                l_quote_obj_list[l_quote._recid] = True


            cr_lquote()


    elif artno != 0 and supno == 0 and docuno != "":

        l_quote_obj_list = {}
        for l_quote, l_lieferant, l_artikel in db_session.query(L_quote, L_lieferant, L_artikel).join(L_lieferant,(L_lieferant.lief_nr == L_quote.lief_nr)).join(L_artikel,(L_artikel.artnr == L_quote.artnr)).filter(
                 (L_quote.reserve_int[inc_value(4)] <= 1) & (L_quote.artnr == artno) & (L_quote.docu_nr == docuno)).order_by(L_quote._recid).all():
            if l_quote_obj_list.get(l_quote._recid):
                continue
            else:
                l_quote_obj_list[l_quote._recid] = True


            cr_lquote()


    elif artno == 0 and supno != 0 and docuno != "":

        l_quote_obj_list = {}
        for l_quote, l_lieferant, l_artikel in db_session.query(L_quote, L_lieferant, L_artikel).join(L_lieferant,(L_lieferant.lief_nr == L_quote.lief_nr)).join(L_artikel,(L_artikel.artnr == L_quote.artnr)).filter(
                 (L_quote.reserve_int[inc_value(4)] <= 1) & (L_quote.lief_nr == supno) & (L_quote.docu_nr == docuno)).order_by(L_quote._recid).all():
            if l_quote_obj_list.get(l_quote._recid):
                continue
            else:
                l_quote_obj_list[l_quote._recid] = True


            cr_lquote()


    return generate_output()