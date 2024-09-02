from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam, Waehrung, L_lieferant, L_artikel, L_quote

def prepare_quote_listbl(artno:int, supno:int, docuno:str):
    prog_path = ""
    prog_name = ""
    bill_date = None
    local_curr = ""
    quote_list_list = []
    htparam = waehrung = l_lieferant = l_artikel = l_quote = None

    quote_list = None

    quote_list_list, Quote_list = create_model("Quote_list", {"artnr":int, "lief_nr":int, "supname":str, "artname":str, "devunit":str, "content":decimal, "unitprice":decimal, "curr":str, "from_date":date, "to_date":date, "remark":str, "filname":str, "activeflag":bool, "docu_nr":str, "minqty":decimal, "delivday":int, "disc":decimal, "avl":bool}, {"activeflag": True, "avl": True})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal prog_path, prog_name, bill_date, local_curr, quote_list_list, htparam, waehrung, l_lieferant, l_artikel, l_quote


        nonlocal quote_list
        nonlocal quote_list_list
        return {"prog_path": prog_path, "prog_name": prog_name, "bill_date": bill_date, "local_curr": local_curr, "quote-list": quote_list_list}

    def cr_lquote():

        nonlocal prog_path, prog_name, bill_date, local_curr, quote_list_list, htparam, waehrung, l_lieferant, l_artikel, l_quote


        nonlocal quote_list
        nonlocal quote_list_list


        quote_list = Quote_list()
        quote_list_list.append(quote_list)

        buffer_copy(l_quote, quote_list)
        quote_list.supName = trim(l_lieferant.anredefirma + " " + firma)
        quote_list.artName = l_artikel.bezeich
        quote_list.devUnit = l_artikel.traubensorte
        quote_list.content = l_artikel.lief_einheit
        quote_list.curr = l_quote.reserve_char[0]
        quote_list.minqty = l_quote.reserve_deci[0]
        quote_list.disc = l_quote.reserve_deci[1]
        quote_list.avl = not l_quote.reserve_logic[0]
        quote_list.delivday = l_quote.reserve_int[0]

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 110)).first()

    if htparam:
        bill_date = htparam.fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 400)).first()

    if htparam.fchar != "":
        prog_path = htparam.fchar
    else:
        prog_path = "\\""program files""\\""microsoft office""\\office\\"

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 405)).first()

    if htparam.fchar != "":
        prog_name = htparam.fchar
    else:
        prog_name = "winword.exe"

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 152)).first()

    waehrung = db_session.query(Waehrung).filter(
            (Waehrung.wabkurz == htparam.fchar)).first()

    if not waehrung:

        waehrung = db_session.query(Waehrung).first()

    if waehrung:
        local_curr = waehrung.wabkurz

    if artno != 0 and supno == 0 and docuno == "":

        l_quote_obj_list = []
        for l_quote, l_lieferant, l_artikel in db_session.query(L_quote, L_lieferant, L_artikel).join(L_lieferant,(L_lieferant.lief_nr == L_quote.lief_nr)).join(L_artikel,(L_artikel.artnr == L_quote.artnr)).filter(
                (L_quote.reserve_int[4] <= 1) &  (L_quote.artnr == artno)).all():
            if l_quote._recid in l_quote_obj_list:
                continue
            else:
                l_quote_obj_list.append(l_quote._recid)


            cr_lquote()


    elif supno != 0 and artno == 0 and docuno == "":

        l_quote_obj_list = []
        for l_quote, l_lieferant, l_artikel in db_session.query(L_quote, L_lieferant, L_artikel).join(L_lieferant,(L_lieferant.lief_nr == L_quote.lief_nr)).join(L_artikel,(L_artikel.artnr == L_quote.artnr)).filter(
                (L_quote.reserve_int[4] <= 1) &  (L_quote.lief_nr == supno)).all():
            if l_quote._recid in l_quote_obj_list:
                continue
            else:
                l_quote_obj_list.append(l_quote._recid)


            cr_lquote()


    elif docuno != "" and artno == 0 and supno == 0:

        l_quote_obj_list = []
        for l_quote, l_lieferant, l_artikel in db_session.query(L_quote, L_lieferant, L_artikel).join(L_lieferant,(L_lieferant.lief_nr == L_quote.lief_nr)).join(L_artikel,(L_artikel.artnr == L_quote.artnr)).filter(
                (L_quote.reserve_int[4] <= 1) &  (L_quote.docu_nr == docuno)).all():
            if l_quote._recid in l_quote_obj_list:
                continue
            else:
                l_quote_obj_list.append(l_quote._recid)


            cr_lquote()


    elif artno != 0 and supno != 0 and docuno == "":

        l_quote_obj_list = []
        for l_quote, l_lieferant, l_artikel in db_session.query(L_quote, L_lieferant, L_artikel).join(L_lieferant,(L_lieferant.lief_nr == L_quote.lief_nr)).join(L_artikel,(L_artikel.artnr == L_quote.artnr)).filter(
                (L_quote.reserve_int[4] <= 1) &  (L_quote.lief_nr == supno) &  (L_quote.artnr == artno)).all():
            if l_quote._recid in l_quote_obj_list:
                continue
            else:
                l_quote_obj_list.append(l_quote._recid)


            cr_lquote()


    elif artno != 0 and supno == 0 and docuno != "":

        l_quote_obj_list = []
        for l_quote, l_lieferant, l_artikel in db_session.query(L_quote, L_lieferant, L_artikel).join(L_lieferant,(L_lieferant.lief_nr == L_quote.lief_nr)).join(L_artikel,(L_artikel.artnr == L_quote.artnr)).filter(
                (L_quote.reserve_int[4] <= 1) &  (L_quote.artnr == artno) &  (L_quote.docu_nr == docuno)).all():
            if l_quote._recid in l_quote_obj_list:
                continue
            else:
                l_quote_obj_list.append(l_quote._recid)


            cr_lquote()


    elif artno == 0 and supno != 0 and docuno != "":

        l_quote_obj_list = []
        for l_quote, l_lieferant, l_artikel in db_session.query(L_quote, L_lieferant, L_artikel).join(L_lieferant,(L_lieferant.lief_nr == L_quote.lief_nr)).join(L_artikel,(L_artikel.artnr == L_quote.artnr)).filter(
                (L_quote.reserve_int[4] <= 1) &  (L_quote.lief_nr == supno) &  (L_quote.docu_nr == docuno)).all():
            if l_quote._recid in l_quote_obj_list:
                continue
            else:
                l_quote_obj_list.append(l_quote._recid)


            cr_lquote()


    return generate_output()