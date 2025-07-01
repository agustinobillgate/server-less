#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Bediener, Htparam, L_lager, L_artikel, L_ophis, L_lieferant, L_op

def stock_inlistbl(from_date:date, to_date:date, from_lager:int, to_lager:int, from_art:int, to_art:int, user_init:string):

    prepare_cache ([Bediener, Htparam, L_lager, L_artikel, L_ophis, L_lieferant, L_op])

    stockin_list_list = []
    note_str:List[string] = [" ", "Transfer"]
    tot_anz:Decimal = to_decimal("0.0")
    tot_amount:Decimal = to_decimal("0.0")
    beg_date:date = None
    end_date:date = None
    show_price:bool = False
    long_digit:bool = False
    fdate:date = None
    bediener = htparam = l_lager = l_artikel = l_ophis = l_lieferant = l_op = None

    stockin_list = None

    stockin_list_list, Stockin_list = create_model("Stockin_list", {"ddate":date, "ist":int, "sdocument":string, "iarticle":int, "sdesc":string, "dquantity":Decimal, "samount":string, "ssupplier":string, "sdelnote":string, "snote":string, "imark":int, "id":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal stockin_list_list, note_str, tot_anz, tot_amount, beg_date, end_date, show_price, long_digit, fdate, bediener, htparam, l_lager, l_artikel, l_ophis, l_lieferant, l_op
        nonlocal from_date, to_date, from_lager, to_lager, from_art, to_art, user_init


        nonlocal stockin_list
        nonlocal stockin_list_list

        return {"stockin-list": stockin_list_list}

    def add_id():

        nonlocal stockin_list_list, note_str, tot_anz, tot_amount, beg_date, end_date, show_price, long_digit, fdate, bediener, htparam, l_lager, l_artikel, l_ophis, l_lieferant, l_op
        nonlocal from_date, to_date, from_lager, to_lager, from_art, to_art, user_init


        nonlocal stockin_list
        nonlocal stockin_list_list

        usr = None
                    Usr =  create_buffer("Usr",Bediener)

                    usr = get_cache (Bediener, {"nr": [(eq, l_op.fuellflag)]})

                    if usr:
                        stockin_list.id = usr.userinit
                    else:
                        stockin_list.id = "??"


    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

    htparam = get_cache (Htparam, {"paramnr": [(eq, 43)]})
    show_price = htparam.flogical

    if substring(bediener.permissions, 21, 1) != ("0").lower() :
        show_price = True

    htparam = get_cache (Htparam, {"paramnr": [(eq, 246)]})
    long_digit = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 224)]})
    fdate = date_mdy(get_month(htparam.fdate) , 1, get_year(htparam.fdate))
    beg_date = fdate - timedelta(days=1)
    tot_anz =  to_decimal("0")
    tot_amount =  to_decimal("0")
    end_date = beg_date

    if to_date < beg_date:
        end_date = to_date

    for l_lager in db_session.query(L_lager).filter(
             (L_lager.lager_nr >= from_lager) & (L_lager.lager_nr <= to_lager)).order_by(L_lager._recid).all():

        if from_date <= beg_date:

            l_ophis_obj_list = {}
            l_ophis = L_ophis()
            l_artikel = L_artikel()
            for l_ophis.anzahl, l_ophis.warenwert, l_ophis.datum, l_ophis.lager_nr, l_ophis.docu_nr, l_ophis.lscheinnr, l_ophis.lief_nr, l_ophis._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel._recid in db_session.query(L_ophis.anzahl, L_ophis.warenwert, L_ophis.datum, L_ophis.lager_nr, L_ophis.docu_nr, L_ophis.lscheinnr, L_ophis.lief_nr, L_ophis._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel._recid).join(L_artikel,(L_artikel.artnr == L_ophis.artnr)).filter(
                     (L_ophis.lager_nr == l_lager.lager_nr) & (L_ophis.datum >= from_date) & (L_ophis.datum <= end_date) & (L_ophis.artnr >= from_art) & (L_ophis.artnr <= to_art) & (L_ophis.op_art == 1)).order_by(L_ophis.artnr, L_ophis.datum).all():
                if l_ophis_obj_list.get(l_ophis._recid):
                    continue
                else:
                    l_ophis_obj_list[l_ophis._recid] = True


                stockin_list = Stockin_list()
                stockin_list_list.append(stockin_list)

                tot_anz =  to_decimal(tot_anz) + to_decimal(l_ophis.anzahl)
                tot_amount =  to_decimal(tot_amount) + to_decimal(l_ophis.warenwert)
                stockin_list.ddate = l_ophis.datum
                stockin_list.ist = l_ophis.lager_nr
                stockin_list.iarticle = l_artikel.artnr
                stockin_list.sdocument = l_ophis.docu_nr
                stockin_list.sdesc = l_artikel.bezeich
                stockin_list.dquantity =  to_decimal(l_ophis.anzahl)
                stockin_list.snote = note_str[l_ophis.op_art - 1]
                stockin_list.sdelnote = substring(l_ophis.lscheinnr, MAX (1, length(l_ophis.lscheinnr) - 15) - 1, 16)

                if show_price:
                    else:
                        stockin_list.samount = \
                                IF long_digit THEN
                        to_string(l_ophis.warenwert, " ->>>,>>>,>>>,>>9")
                        ELSE
                        to_string(l_ophis.warenwert, "->>>,>>>,>>>,>>9.99")

                    if l_ophis.lief_nr != 0:

                        l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, l_ophis.lief_nr)]})

                        if l_lieferant:
                            stockin_list.ssupplier = l_lieferant.firma

            l_op_obj_list = {}
            l_op = L_op()
            l_artikel = L_artikel()
            for l_op.fuellflag, l_op.anzahl, l_op.warenwert, l_op.datum, l_op.lager_nr, l_op.docu_nr, l_op.lscheinnr, l_op.lief_nr, l_op._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel._recid in db_session.query(L_op.fuellflag, L_op.anzahl, L_op.warenwert, L_op.datum, L_op.lager_nr, L_op.docu_nr, L_op.lscheinnr, L_op.lief_nr, L_op._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel._recid).join(L_artikel,(L_artikel.artnr == L_op.artnr)).filter(
                     (L_op.lager_nr == l_lager.lager_nr) & (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.artnr >= from_art) & (L_op.artnr <= to_art) & (L_op.loeschflag < 2) & (L_op.op_art == 1)).order_by(L_op.artnr, L_op.datum).all():
                if l_op_obj_list.get(l_op._recid):
                    continue
                else:
                    l_op_obj_list[l_op._recid] = True


                stockin_list = Stockin_list()
                stockin_list_list.append(stockin_list)

                tot_anz =  to_decimal(tot_anz) + to_decimal(l_op.anzahl)
                tot_amount =  to_decimal(tot_amount) + to_decimal(l_op.warenwert)
                stockin_list.ddate = l_op.datum
                stockin_list.ist = l_op.lager_nr
                stockin_list.iarticle = l_artikel.artnr
                stockin_list.sdocument = l_op.docu_nr
                stockin_list.sdesc = l_artikel.bezeich
                stockin_list.dquantity =  to_decimal(l_op.anzahl)
                stockin_list.snote = note_str[l_op.op_art - 1]
                stockin_list.sdelnote = substring(l_op.lscheinnr, MAX (1, length(l_op.lscheinnr) - 15) - 1, 16)
                stockin_list.imark = 0


                add_id()

                if show_price:
                    else:
                        stockin_list.samount = \
                                IF long_digit THEN
                        to_string(l_op.warenwert, " ->>>,>>>,>>>,>>9")
                        ELSE
                        to_string(l_op.warenwert, "->>>,>>>,>>>,>>9.99")

                    if l_op.lief_nr != 0:

                        l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, l_op.lief_nr)]})

                        if l_lieferant:
                            stockin_list.ssupplier = l_lieferant.firma


            stockin_list = Stockin_list()
            stockin_list_list.append(stockin_list)

            stockin_list.sdesc = "T O T A L"
            stockin_list.dquantity =  to_decimal(tot_anz)
            stockin_list.imark = 1

            if show_price:
                else:
                    stockin_list.samount = \
                            IF long_digit THEN
                    to_string(tot_amount, " ->>>,>>>,>>>,>>9")
                    ELSE
                    to_string(tot_amount, "->>>,>>>,>>>,>>9.99")

    return generate_output()