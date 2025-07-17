#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from sqlalchemy import func
from models import Htparam, L_artikel, L_besthis, L_ophis, L_lager, L_untergrup

def stock_hohlist2_webbl(from_lager:int, to_lager:int, from_art:int, to_art:int, to_date:date, move_art:bool, end_notzero:bool, global_oh:bool, from_date:date):

    prepare_cache ([Htparam, L_artikel, L_besthis, L_ophis, L_lager, L_untergrup])

    stockoh_list_data = []
    do_it:bool = False
    curr_art:int = 0
    curr_lager:int = 0
    out_bestand:Decimal = to_decimal("0.0")
    zwkum:int = 0
    t_val:Decimal = to_decimal("0.0")
    bezeich:string = ""
    j:int = 0
    tot_prev:Decimal = to_decimal("0.0")
    tot_value:Decimal = to_decimal("0.0")
    tot_in:Decimal = to_decimal("0.0")
    tot_out:Decimal = to_decimal("0.0")
    total_in:Decimal = to_decimal("0.0")
    total_out:Decimal = to_decimal("0.0")
    total_prev:Decimal = to_decimal("0.0")
    total_value:Decimal = to_decimal("0.0")
    start_from_date:date = None
    loop:int = 0
    loop_date:date = None
    diff_month:int = 0
    long_digit:bool = False
    htparam = l_artikel = l_besthis = l_ophis = l_lager = l_untergrup = None

    stockoh_list = art_bestand = t_vkpreis = tot_t_vkpreis = None

    stockoh_list_data, Stockoh_list = create_model("Stockoh_list", {"artnr":string, "bezeich":string, "prevqty":string, "prevval":string, "incoming":string, "outgoing":string, "actqty":string, "actval":string, "avrg_pr":string, "incomingval":string, "outgoingval":string})
    art_bestand_data, Art_bestand = create_model("Art_bestand", {"lager":int, "artnr":int, "zwkum":int, "bezeich":string, "incoming":Decimal, "in_val":Decimal, "out_val":Decimal, "outgoing":Decimal, "prevqty":Decimal, "prevval":Decimal, "adjust":Decimal, "actqty":Decimal, "actval":Decimal, "avrg_pr":Decimal, "vk_preis":Decimal})
    t_vkpreis_data, T_vkpreis = create_model("T_vkpreis", {"lager":int, "artnr":int, "zwkum":int, "bezeich":string, "qty_end":Decimal, "val_end":Decimal, "vk_preis":Decimal})
    tot_t_vkpreis_data, Tot_t_vkpreis = create_model("Tot_t_vkpreis", {"lager":int, "artnr":int, "tot_val":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal stockoh_list_data, do_it, curr_art, curr_lager, out_bestand, zwkum, t_val, bezeich, j, tot_prev, tot_value, tot_in, tot_out, total_in, total_out, total_prev, total_value, start_from_date, loop, loop_date, diff_month, long_digit, htparam, l_artikel, l_besthis, l_ophis, l_lager, l_untergrup
        nonlocal from_lager, to_lager, from_art, to_art, to_date, move_art, end_notzero, global_oh, from_date


        nonlocal stockoh_list, art_bestand, t_vkpreis, tot_t_vkpreis
        nonlocal stockoh_list_data, art_bestand_data, t_vkpreis_data, tot_t_vkpreis_data

        return {"stockoh-list": stockoh_list_data}

    def calc_month_diff(from_date:date, to_date:date):

        nonlocal stockoh_list_data, do_it, curr_art, curr_lager, out_bestand, zwkum, t_val, bezeich, j, tot_prev, tot_value, tot_in, tot_out, total_in, total_out, total_prev, total_value, start_from_date, loop, loop_date, diff_month, long_digit, htparam, l_artikel, l_besthis, l_ophis, l_lager, l_untergrup
        nonlocal from_lager, to_lager, from_art, to_art, move_art, end_notzero, global_oh, stockoh_list, art_bestand, t_vkpreis, tot_t_vkpreis
        nonlocal stockoh_list_data, art_bestand_data, t_vkpreis_data, tot_t_vkpreis_data

        diff_month = 0
        year_from_date:int = 0
        year_to_date:int = 0
        month_from_date:int = 0
        month_to_date:int = 0
        diff_year:int = 0

        def generate_inner_output():
            return (diff_month)

        year_from_date = get_year(from_date)
        year_to_date = get_year(to_date)
        month_from_date = get_month(from_date)
        month_to_date = get_month(to_date)
        diff_year = year_to_date - year_from_date
        diff_month = (month_to_date + (12 * diff_year)) - month_from_date

        return generate_inner_output()


    def create_stock1():

        nonlocal stockoh_list_data, do_it, curr_art, curr_lager, out_bestand, zwkum, t_val, bezeich, j, tot_prev, tot_value, tot_in, tot_out, total_in, total_out, total_prev, total_value, start_from_date, loop, loop_date, diff_month, long_digit, htparam, l_artikel, l_besthis, l_ophis, l_lager, l_untergrup
        nonlocal from_lager, to_lager, from_art, to_art, to_date, move_art, end_notzero, global_oh, from_date


        nonlocal stockoh_list, art_bestand, t_vkpreis, tot_t_vkpreis
        nonlocal stockoh_list_data, art_bestand_data, t_vkpreis_data, tot_t_vkpreis_data


        t_vkpreis_data.clear()

        l_besthis_obj_list = {}
        l_besthis = L_besthis()
        l_artikel = L_artikel()
        for l_besthis.artnr, l_besthis.anz_anf_best, l_besthis.anz_eingang, l_besthis.anz_ausgang, l_besthis.val_anf_best, l_besthis.wert_eingang, l_besthis.wert_ausgang, l_besthis.lager_nr, l_besthis._recid, l_artikel.vk_preis, l_artikel.zwkum, l_artikel.bezeich, l_artikel._recid in db_session.query(L_besthis.artnr, L_besthis.anz_anf_best, L_besthis.anz_eingang, L_besthis.anz_ausgang, L_besthis.val_anf_best, L_besthis.wert_eingang, L_besthis.wert_ausgang, L_besthis.lager_nr, L_besthis._recid, L_artikel.vk_preis, L_artikel.zwkum, L_artikel.bezeich, L_artikel._recid).join(L_artikel,(L_artikel.artnr == L_besthis.artnr)).filter(
                 (L_besthis.lager_nr == 0) & (L_besthis.anf_best_dat >= date_mdy(get_month(from_date) , 1 , get_year(from_date))) & (L_besthis.anf_best_dat <= date_mdy(get_month(to_date) , 1 , get_year(to_date))) & (L_besthis.artnr >= from_art) & (L_besthis.artnr <= to_art)).order_by(L_artikel.zwkum, L_artikel.artnr).all():
            if l_besthis_obj_list.get(l_besthis._recid):
                continue
            else:
                l_besthis_obj_list[l_besthis._recid] = True

            t_vkpreis = query(t_vkpreis_data, filters=(lambda t_vkpreis: t_vkpreis.artnr == l_besthis.artnr), first=True)

            if t_vkpreis:
                t_vkpreis.qty_end =  to_decimal(t_vkpreis.qty_end) + to_decimal((l_besthis.anz_anf_best) + to_decimal(l_besthis.anz_eingang) - to_decimal(l_besthis.anz_ausgang))
                t_vkpreis.val_end =  to_decimal(t_vkpreis.val_end) + to_decimal((l_besthis.val_anf_best) + to_decimal(l_besthis.wert_eingang) - to_decimal(l_besthis.wert_ausgang))

                if t_vkpreis.val_end == 0 or t_vkpreis.qty_end == 0:
                    t_vkpreis.vk_preis =  to_decimal(t_vkpreis.vk_preis) + to_decimal(l_artikel.vk_preis)
                else:
                    t_vkpreis.vk_preis =  to_decimal(t_vkpreis.vk_preis) + to_decimal((t_vkpreis.val_end) / to_decimal((t_vkpreis.qty_end)))
            else:
                t_vkpreis = T_vkpreis()
                t_vkpreis_data.append(t_vkpreis)

                t_vkpreis.lager = l_besthis.lager_nr
                t_vkpreis.artnr = l_besthis.artnr
                t_vkpreis.zwkum = l_artikel.zwkum
                t_vkpreis.bezeich = l_artikel.bezeich
                t_vkpreis.qty_end =  to_decimal(l_besthis.anz_anf_best) + to_decimal(l_besthis.anz_eingang) - to_decimal(l_besthis.anz_ausgang)
                t_vkpreis.val_end =  to_decimal(l_besthis.val_anf_best) + to_decimal(l_besthis.wert_eingang) - to_decimal(l_besthis.wert_ausgang)

                if t_vkpreis.val_end == 0 or t_vkpreis.qty_end == 0:
                    t_vkpreis.vk_preis =  to_decimal(l_artikel.vk_preis)
                else:
                    t_vkpreis.vk_preis =  to_decimal(t_vkpreis.val_end) / to_decimal((t_vkpreis.qty_end))

        for l_besthis in db_session.query(L_besthis).filter(
                 (L_besthis.lager_nr >= from_lager) & (L_besthis.lager_nr <= to_lager) & (L_besthis.anf_best_dat == start_from_date) & (L_besthis.artnr >= from_art) & (L_besthis.artnr <= to_art)).order_by(L_besthis.artnr).all():

            t_vkpreis = query(t_vkpreis_data, filters=(lambda t_vkpreis: t_vkpreis.artnr == l_besthis.artnr), first=True)

            if t_vkpreis:
                do_it = True

                if do_it:

                    art_bestand = query(art_bestand_data, filters=(lambda art_bestand: art_bestand.artnr == l_besthis.artnr and art_bestand.lager == l_besthis.lager_nr), first=True)

                    if not art_bestand:
                        art_bestand = Art_bestand()
                        art_bestand_data.append(art_bestand)

                        art_bestand.bezeich = t_vkpreis.bezeich
                        art_bestand.zwkum = t_vkpreis.zwkum
                        art_bestand.artnr = l_besthis.artnr
                        art_bestand.lager = l_besthis.lager_nr
                        art_bestand.prevqty =  to_decimal(l_besthis.anz_anf_best)
                        art_bestand.prevval =  to_decimal(l_besthis.val_anf_best)
                        art_bestand.actqty =  to_decimal(l_besthis.anz_anf_best)
                        art_bestand.actval =  to_decimal(l_besthis.val_anf_best)
                        art_bestand.vk_preis =  to_decimal(t_vkpreis.vk_preis)
                        curr_art = l_besthis.artnr
                        curr_lager = l_besthis.lager_nr
                    out_bestand =  to_decimal("0")

        for l_ophis in db_session.query(L_ophis).filter(
                 (L_ophis.lager_nr >= from_lager) & (L_ophis.lager_nr <= to_lager) & (L_ophis.artnr >= from_art) & (L_ophis.artnr <= to_art) & (L_ophis.datum >= start_from_date) & (L_ophis.datum <= to_date) & (not_(matches(L_ophis.fibukonto,"*;CANCELLED*")))).order_by(L_ophis.datum).all():

            art_bestand = query(art_bestand_data, filters=(lambda art_bestand: art_bestand.artnr == l_ophis.artnr and art_bestand.lager == l_ophis.lager_nr), first=True)

            if art_bestand:

                if l_ophis.op_art == 1 or l_ophis.op_art == 2:
                    art_bestand.incoming =  to_decimal(art_bestand.incoming) + to_decimal(l_ophis.anzahl)
                    art_bestand.in_val =  to_decimal(art_bestand.in_val) + to_decimal(l_ophis.anzahl) * to_decimal((art_bestand.vk_preis) / to_decimal((diff_month) + to_decimal(1)))
                    art_bestand.actqty =  to_decimal(art_bestand.actqty) + to_decimal(l_ophis.anzahl)

                elif l_ophis.op_art == 3 or l_ophis.op_art == 4:
                    art_bestand.outgoing =  to_decimal(art_bestand.outgoing) + to_decimal(l_ophis.anzahl)
                    art_bestand.out_val =  to_decimal(art_bestand.out_val) + to_decimal(l_ophis.anzahl) * to_decimal((art_bestand.vk_preis) / to_decimal((diff_month) + to_decimal(1)))
                    art_bestand.actqty =  to_decimal(art_bestand.actqty) - to_decimal(l_ophis.anzahl)

        for art_bestand in query(art_bestand_data):
            art_bestand.prevval =  to_decimal(art_bestand.prevqty) * to_decimal((art_bestand.vk_preis) / to_decimal((diff_month) + to_decimal(1)))
            art_bestand.actval =  to_decimal(art_bestand.actqty) * to_decimal((art_bestand.vk_preis) / to_decimal((diff_month) + to_decimal(1)))

        for l_lager in db_session.query(L_lager).filter(
                 (L_lager.lager_nr >= from_lager) & (L_lager.lager_nr <= to_lager)).order_by(L_lager._recid).all():
            bezeich = ""
            stockoh_list = Stockoh_list()
            stockoh_list_data.append(stockoh_list)

            stockoh_list.bezeich = to_string(l_lager.lager_nr, "99") + " - " + to_string(l_lager.bezeich, "x(20)")
            tot_prev =  to_decimal("0")
            tot_in =  to_decimal("0")
            tot_out =  to_decimal("0")
            tot_value =  to_decimal("0")
            total_value =  to_decimal("0")
            zwkum = 0
            t_val =  to_decimal("0")

            for art_bestand in query(art_bestand_data, filters=(lambda art_bestand: art_bestand.lager == l_lager.lager_nr and art_bestand.artnr >= from_art and art_bestand.artnr <= to_art), sort_by=[("zwkum",False),("bezeich",False)]):

                if (move_art and end_notzero) and (art_bestand.incoming != 0 or art_bestand.outgoing != 0 or art_bestand.actqty != 0):

                    if zwkum == 0:
                        zwkum = art_bestand.zwkum

                        l_untergrup = get_cache (L_untergrup, {"zwkum": [(eq, zwkum)]})

                        if l_untergrup:
                            bezeich = l_untergrup.bezeich

                    if zwkum != art_bestand.zwkum:
                        stockoh_list = Stockoh_list()
                        stockoh_list_data.append(stockoh_list)


                        if not long_digit:
                            stockoh_list.bezeich = "Ttl " + to_string(substring(bezeich, 0, 9) , "x(9)") +\
                                    to_string(substring(bezeich, 9, 13) , "x(13)")
                            stockoh_list.actval = to_string(t_val, "->>,>>>,>>9.99")


                        else:
                            stockoh_list.bezeich = "Ttl " + to_string(substring(bezeich, 0, 9) , "x(9)") +\
                                    to_string(substring(bezeich, 9, 13) , "x(13)")
                            stockoh_list.actval = to_string(t_val, "->,>>>,>>>,>>9")


                        stockoh_list = Stockoh_list()
                        stockoh_list_data.append(stockoh_list)

                        t_val =  to_decimal("0")
                        zwkum = art_bestand.zwkum

                        l_untergrup = get_cache (L_untergrup, {"zwkum": [(eq, zwkum)]})

                        if l_untergrup:
                            bezeich = l_untergrup.bezeich

                    if art_bestand.avrg_pr == 0:

                        if art_bestand.actqty != 0:
                            art_bestand.avrg_pr =  to_decimal(art_bestand.actval) / to_decimal(art_bestand.actqty)
                        else:
                            art_bestand.actval =  to_decimal("0")

                            t_vkpreis = query(t_vkpreis_data, filters=(lambda t_vkpreis: t_vkpreis.artnr == art_bestand.artnr), first=True)

                            if t_vkpreis:
                                art_bestand.avrg_pr = ( to_decimal(t_vkpreis.vk_preis) / to_decimal((diff_month) + to_decimal(1)))
                    stockoh_list = Stockoh_list()
                    stockoh_list_data.append(stockoh_list)


                    if not long_digit:
                        stockoh_list.artnr = to_string(art_bestand.artnr, "9999999")
                        stockoh_list.bezeich = to_string(art_bestand.bezeich, "x(50)")
                        stockoh_list.prevqty = to_string(art_bestand.prevqty, "->,>>>,>>9.99")
                        stockoh_list.prevval = to_string(art_bestand.prevval, "->>,>>>,>>9.99")
                        stockoh_list.incoming = to_string(art_bestand.incoming, "->,>>>,>>9.99")
                        stockoh_list.outgoing = to_string(art_bestand.outgoing, "->,>>>,>>9.99")
                        stockoh_list.outgoingval = to_string(art_bestand.out_val, "->>>,>>>,>>9.99")
                        stockoh_list.incomingval = to_string(art_bestand.in_val, "->>>,>>>,>>9.99")
                        stockoh_list.actqty = to_string(art_bestand.actqty, "->,>>>,>>9.99")
                        stockoh_list.actval = to_string(art_bestand.actval, "->>,>>>,>>9.99")
                        stockoh_list.avrg_pr = to_string(art_bestand.avrg_pr, "->>,>>>,>>9.99")


                    else:
                        stockoh_list.artnr = to_string(art_bestand.artnr, "9999999")
                        stockoh_list.bezeich = to_string(art_bestand.bezeich, "x(50)")
                        stockoh_list.prevqty = to_string(art_bestand.prevqty, "->,>>>,>>9.99")
                        stockoh_list.prevval = to_string(art_bestand.prevval, "->,>>>,>>>,>>9")
                        stockoh_list.incoming = to_string(art_bestand.incoming, "->,>>>,>>9.99")
                        stockoh_list.outgoing = to_string(art_bestand.outgoing, "->,>>>,>>9.99")
                        stockoh_list.outgoingval = to_string(art_bestand.out_val, "->>>,>>>,>>9.99")
                        stockoh_list.incomingval = to_string(art_bestand.in_val, "->>>,>>>,>>9.99")
                        stockoh_list.actqty = to_string(art_bestand.actqty, "->,>>>,>>9.99")
                        stockoh_list.actval = to_string(art_bestand.actval, "->,>>>,>>>,>>9")
                        stockoh_list.avrg_pr = to_string(art_bestand.avrg_pr, ">>,>>>,>>>,>>9")


                    t_val =  to_decimal(t_val) + to_decimal(art_bestand.actval)
                    tot_in =  to_decimal(tot_in) + to_decimal(art_bestand.in_val)
                    tot_out =  to_decimal(tot_out) + to_decimal(art_bestand.out_val)
                    tot_prev =  to_decimal(tot_prev) + to_decimal(art_bestand.prevval)
                    tot_value =  to_decimal(tot_value) + to_decimal(art_bestand.actval)
                    total_in =  to_decimal(total_in) + to_decimal(art_bestand.in_val)
                    total_out =  to_decimal(total_out) + to_decimal(art_bestand.out_val)
                    total_prev =  to_decimal(total_prev) + to_decimal(art_bestand.prevval)
                    total_value =  to_decimal(total_value) + to_decimal(art_bestand.actval)

                elif (move_art and not end_notzero) and (art_bestand.incoming != 0 or art_bestand.outgoing != 0):

                    if zwkum == 0:
                        zwkum = art_bestand.zwkum

                        l_untergrup = get_cache (L_untergrup, {"zwkum": [(eq, zwkum)]})

                        if l_untergrup:
                            bezeich = l_untergrup.bezeich

                    if zwkum != art_bestand.zwkum:
                        stockoh_list = Stockoh_list()
                        stockoh_list_data.append(stockoh_list)


                        if not long_digit:
                            stockoh_list.bezeich = "Ttl " + to_string(substring(bezeich, 0, 9) , "x(9)") +\
                                    to_string(substring(bezeich, 9, 13) , "x(13)")
                            stockoh_list.actval = to_string(t_val, "->>,>>>,>>9.99")


                        else:
                            stockoh_list.bezeich = "Ttl " + to_string(substring(bezeich, 0, 9) , "x(9)") +\
                                    to_string(substring(bezeich, 9, 13) , "x(13)")
                            stockoh_list.actval = to_string(t_val, "->,>>>,>>>,>>9")


                        stockoh_list = Stockoh_list()
                        stockoh_list_data.append(stockoh_list)

                        t_val =  to_decimal("0")
                        zwkum = art_bestand.zwkum

                        l_untergrup = get_cache (L_untergrup, {"zwkum": [(eq, zwkum)]})

                        if l_untergrup:
                            bezeich = l_untergrup.bezeich

                    if art_bestand.avrg_pr == 0:

                        if art_bestand.actqty != 0:
                            art_bestand.avrg_pr =  to_decimal(art_bestand.actval) / to_decimal(art_bestand.actqty)
                        else:
                            art_bestand.actval =  to_decimal("0")

                            t_vkpreis = query(t_vkpreis_data, filters=(lambda t_vkpreis: t_vkpreis.artnr == art_bestand.artnr), first=True)

                            if t_vkpreis:
                                art_bestand.avrg_pr = ( to_decimal(t_vkpreis.vk_preis) / to_decimal((diff_month) + to_decimal(1)))
                    stockoh_list = Stockoh_list()
                    stockoh_list_data.append(stockoh_list)


                    if not long_digit:
                        stockoh_list.artnr = to_string(art_bestand.artnr, "9999999")
                        stockoh_list.bezeich = to_string(art_bestand.bezeich, "x(50)")
                        stockoh_list.prevqty = to_string(art_bestand.prevqty, "->,>>>,>>9.99")
                        stockoh_list.prevval = to_string(art_bestand.prevval, "->>,>>>,>>9.99")
                        stockoh_list.incoming = to_string(art_bestand.incoming, "->,>>>,>>9.99")
                        stockoh_list.outgoing = to_string(art_bestand.outgoing, "->,>>>,>>9.99")
                        stockoh_list.outgoingval = to_string(art_bestand.out_val, "->>>,>>>,>>9.99")
                        stockoh_list.incomingval = to_string(art_bestand.in_val, "->>>,>>>,>>9.99")
                        stockoh_list.actqty = to_string(art_bestand.actqty, "->,>>>,>>9.99")
                        stockoh_list.actval = to_string(art_bestand.actval, "->>,>>>,>>9.99")
                        stockoh_list.avrg_pr = to_string(art_bestand.avrg_pr, "->>,>>>,>>9.99")


                    else:
                        stockoh_list.artnr = to_string(art_bestand.artnr, "9999999")
                        stockoh_list.bezeich = to_string(art_bestand.bezeich, "x(50)")
                        stockoh_list.prevqty = to_string(art_bestand.prevqty, "->,>>>,>>9.99")
                        stockoh_list.prevval = to_string(art_bestand.prevval, "->,>>>,>>>,>>9")
                        stockoh_list.incoming = to_string(art_bestand.incoming, "->,>>>,>>9.99")
                        stockoh_list.outgoing = to_string(art_bestand.outgoing, "->,>>>,>>9.99")
                        stockoh_list.outgoingval = to_string(art_bestand.out_val, "->>>,>>>,>>9.99")
                        stockoh_list.incomingval = to_string(art_bestand.in_val, "->>>,>>>,>>9.99")
                        stockoh_list.actqty = to_string(art_bestand.actqty, "->,>>>,>>9.99")
                        stockoh_list.actval = to_string(art_bestand.actval, "->,>>>,>>>,>>9")
                        stockoh_list.avrg_pr = to_string(art_bestand.avrg_pr, ">>,>>>,>>>,>>9")


                    t_val =  to_decimal(t_val) + to_decimal(art_bestand.actval)
                    tot_in =  to_decimal(tot_in) + to_decimal(art_bestand.in_val)
                    tot_out =  to_decimal(tot_out) + to_decimal(art_bestand.out_val)
                    tot_prev =  to_decimal(tot_prev) + to_decimal(art_bestand.prevval)
                    tot_value =  to_decimal(tot_value) + to_decimal(art_bestand.actval)
                    total_in =  to_decimal(total_in) + to_decimal(art_bestand.in_val)
                    total_out =  to_decimal(total_out) + to_decimal(art_bestand.out_val)
                    total_prev =  to_decimal(total_prev) + to_decimal(art_bestand.prevval)
                    total_value =  to_decimal(total_value) + to_decimal(art_bestand.actval)

                elif (not move_art and end_notzero) and (art_bestand.actqty != 0):

                    if zwkum == 0:
                        zwkum = art_bestand.zwkum

                        l_untergrup = get_cache (L_untergrup, {"zwkum": [(eq, zwkum)]})

                        if l_untergrup:
                            bezeich = l_untergrup.bezeich

                    if zwkum != art_bestand.zwkum:
                        stockoh_list = Stockoh_list()
                        stockoh_list_data.append(stockoh_list)


                        if not long_digit:
                            stockoh_list.bezeich = "Ttl " + to_string(substring(bezeich, 0, 9) , "x(9)") +\
                                    to_string(substring(bezeich, 9, 13) , "x(13)")
                            stockoh_list.actval = to_string(t_val, "->>,>>>,>>9.99")


                        else:
                            stockoh_list.bezeich = "Ttl " + to_string(substring(bezeich, 0, 9) , "x(9)") +\
                                    to_string(substring(bezeich, 9, 13) , "x(13)")
                            stockoh_list.actval = to_string(t_val, "->,>>>,>>>,>>9")


                        stockoh_list = Stockoh_list()
                        stockoh_list_data.append(stockoh_list)

                        t_val =  to_decimal("0")
                        zwkum = art_bestand.zwkum

                        l_untergrup = get_cache (L_untergrup, {"zwkum": [(eq, zwkum)]})

                        if l_untergrup:
                            bezeich = l_untergrup.bezeich

                    if art_bestand.avrg_pr == 0:

                        if art_bestand.actqty != 0:
                            art_bestand.avrg_pr =  to_decimal(art_bestand.actval) / to_decimal(art_bestand.actqty)
                        else:
                            art_bestand.actval =  to_decimal("0")

                            t_vkpreis = query(t_vkpreis_data, filters=(lambda t_vkpreis: t_vkpreis.artnr == art_bestand.artnr), first=True)

                            if t_vkpreis:
                                art_bestand.avrg_pr = ( to_decimal(t_vkpreis.vk_preis) / to_decimal((diff_month) + to_decimal(1)))
                    stockoh_list = Stockoh_list()
                    stockoh_list_data.append(stockoh_list)


                    if not long_digit:
                        stockoh_list.artnr = to_string(art_bestand.artnr, "9999999")
                        stockoh_list.bezeich = to_string(art_bestand.bezeich, "x(50)")
                        stockoh_list.prevqty = to_string(art_bestand.prevqty, "->,>>>,>>9.99")
                        stockoh_list.prevval = to_string(art_bestand.prevval, "->>,>>>,>>9.99")
                        stockoh_list.incoming = to_string(art_bestand.incoming, "->,>>>,>>9.99")
                        stockoh_list.outgoing = to_string(art_bestand.outgoing, "->,>>>,>>9.99")
                        stockoh_list.outgoingval = to_string(art_bestand.out_val, "->>>,>>>,>>9.99")
                        stockoh_list.incomingval = to_string(art_bestand.in_val, "->>>,>>>,>>9.99")
                        stockoh_list.actqty = to_string(art_bestand.actqty, "->,>>>,>>9.99")
                        stockoh_list.actval = to_string(art_bestand.actval, "->>,>>>,>>9.99")
                        stockoh_list.avrg_pr = to_string(art_bestand.avrg_pr, "->>,>>>,>>9.99")


                    else:
                        stockoh_list.artnr = to_string(art_bestand.artnr, "9999999")
                        stockoh_list.bezeich = to_string(art_bestand.bezeich, "x(50)")
                        stockoh_list.prevqty = to_string(art_bestand.prevqty, "->,>>>,>>9.99")
                        stockoh_list.prevval = to_string(art_bestand.prevval, "->,>>>,>>>,>>9")
                        stockoh_list.incoming = to_string(art_bestand.incoming, "->,>>>,>>9.99")
                        stockoh_list.outgoing = to_string(art_bestand.outgoing, "->,>>>,>>9.99")
                        stockoh_list.outgoingval = to_string(art_bestand.out_val, "->>>,>>>,>>9.99")
                        stockoh_list.incomingval = to_string(art_bestand.in_val, "->>>,>>>,>>9.99")
                        stockoh_list.actqty = to_string(art_bestand.actqty, "->,>>>,>>9.99")
                        stockoh_list.actval = to_string(art_bestand.actval, "->,>>>,>>>,>>9")
                        stockoh_list.avrg_pr = to_string(art_bestand.avrg_pr, ">>,>>>,>>>,>>9")


                    t_val =  to_decimal(t_val) + to_decimal(art_bestand.actval)
                    tot_in =  to_decimal(tot_in) + to_decimal(art_bestand.in_val)
                    tot_out =  to_decimal(tot_out) + to_decimal(art_bestand.out_val)
                    tot_prev =  to_decimal(tot_prev) + to_decimal(art_bestand.prevval)
                    tot_value =  to_decimal(tot_value) + to_decimal(art_bestand.actval)
                    total_in =  to_decimal(total_in) + to_decimal(art_bestand.in_val)
                    total_out =  to_decimal(total_out) + to_decimal(art_bestand.out_val)
                    total_prev =  to_decimal(total_prev) + to_decimal(art_bestand.prevval)
                    total_value =  to_decimal(total_value) + to_decimal(art_bestand.actval)

                elif (not move_art and not end_notzero):

                    if zwkum == 0:
                        zwkum = art_bestand.zwkum

                        l_untergrup = get_cache (L_untergrup, {"zwkum": [(eq, zwkum)]})

                        if l_untergrup:
                            bezeich = l_untergrup.bezeich

                    if zwkum != art_bestand.zwkum:
                        stockoh_list = Stockoh_list()
                        stockoh_list_data.append(stockoh_list)


                        if not long_digit:
                            stockoh_list.bezeich = "Ttl " + to_string(substring(bezeich, 0, 9) , "x(9)") +\
                                    to_string(substring(bezeich, 9, 13) , "x(13)")
                            stockoh_list.actval = to_string(t_val, "->>,>>>,>>9.99")


                        else:
                            stockoh_list.bezeich = "Ttl " + to_string(substring(bezeich, 0, 9) , "x(9)") +\
                                    to_string(substring(bezeich, 9, 13) , "x(13)")
                            stockoh_list.actval = to_string(t_val, "->,>>>,>>>,>>9")


                        stockoh_list = Stockoh_list()
                        stockoh_list_data.append(stockoh_list)

                        t_val =  to_decimal("0")
                        zwkum = art_bestand.zwkum

                        l_untergrup = get_cache (L_untergrup, {"zwkum": [(eq, zwkum)]})

                        if l_untergrup:
                            bezeich = l_untergrup.bezeich

                    if art_bestand.avrg_pr == 0:

                        if art_bestand.actqty != 0:
                            art_bestand.avrg_pr =  to_decimal(art_bestand.actval) / to_decimal(art_bestand.actqty)
                        else:
                            art_bestand.actval =  to_decimal("0")

                            t_vkpreis = query(t_vkpreis_data, filters=(lambda t_vkpreis: t_vkpreis.artnr == art_bestand.artnr), first=True)

                            if t_vkpreis:
                                art_bestand.avrg_pr = ( to_decimal(t_vkpreis.vk_preis) / to_decimal((diff_month) + to_decimal(1)))
                    stockoh_list = Stockoh_list()
                    stockoh_list_data.append(stockoh_list)


                    if not long_digit:
                        stockoh_list.artnr = to_string(art_bestand.artnr, "9999999")
                        stockoh_list.bezeich = to_string(art_bestand.bezeich, "x(50)")
                        stockoh_list.prevqty = to_string(art_bestand.prevqty, "->,>>>,>>9.99")
                        stockoh_list.prevval = to_string(art_bestand.prevval, "->>,>>>,>>9.99")
                        stockoh_list.incoming = to_string(art_bestand.incoming, "->,>>>,>>9.99")
                        stockoh_list.outgoing = to_string(art_bestand.outgoing, "->,>>>,>>9.99")
                        stockoh_list.outgoingval = to_string(art_bestand.out_val, "->>>,>>>,>>9.99")
                        stockoh_list.incomingval = to_string(art_bestand.in_val, "->>>,>>>,>>9.99")
                        stockoh_list.actqty = to_string(art_bestand.actqty, "->,>>>,>>9.99")
                        stockoh_list.actval = to_string(art_bestand.actval, "->>,>>>,>>9.99")
                        stockoh_list.avrg_pr = to_string(art_bestand.avrg_pr, "->>,>>>,>>9.99")


                    else:
                        stockoh_list.artnr = to_string(art_bestand.artnr, "9999999")
                        stockoh_list.bezeich = to_string(art_bestand.bezeich, "x(50)")
                        stockoh_list.prevqty = to_string(art_bestand.prevqty, "->,>>>,>>9.99")
                        stockoh_list.prevval = to_string(art_bestand.prevval, "->,>>>,>>>,>>9")
                        stockoh_list.incoming = to_string(art_bestand.incoming, "->,>>>,>>9.99")
                        stockoh_list.outgoing = to_string(art_bestand.outgoing, "->,>>>,>>9.99")
                        stockoh_list.outgoingval = to_string(art_bestand.out_val, "->>>,>>>,>>9.99")
                        stockoh_list.incomingval = to_string(art_bestand.in_val, "->>>,>>>,>>9.99")
                        stockoh_list.actqty = to_string(art_bestand.actqty, "->,>>>,>>9.99")
                        stockoh_list.actval = to_string(art_bestand.actval, "->,>>>,>>>,>>9")
                        stockoh_list.avrg_pr = to_string(art_bestand.avrg_pr, ">>,>>>,>>>,>>9")


                    t_val =  to_decimal(t_val) + to_decimal(art_bestand.actval)
                    tot_in =  to_decimal(tot_in) + to_decimal(art_bestand.in_val)
                    tot_out =  to_decimal(tot_out) + to_decimal(art_bestand.out_val)
                    tot_prev =  to_decimal(tot_prev) + to_decimal(art_bestand.prevval)
                    tot_value =  to_decimal(tot_value) + to_decimal(art_bestand.actval)
                    total_in =  to_decimal(total_in) + to_decimal(art_bestand.in_val)
                    total_out =  to_decimal(total_out) + to_decimal(art_bestand.out_val)
                    total_prev =  to_decimal(total_prev) + to_decimal(art_bestand.prevval)
                    total_value =  to_decimal(total_value) + to_decimal(art_bestand.actval)

            if bezeich != "":
                stockoh_list = Stockoh_list()
                stockoh_list_data.append(stockoh_list)


                if not long_digit:
                    stockoh_list.bezeich = "Ttl " + to_string(substring(bezeich, 0, 9) , "x(9)") +\
                            to_string(substring(bezeich, 9, 13) , "x(13)")
                    stockoh_list.actval = to_string(t_val, "->>,>>>,>>9.99")


                else:
                    stockoh_list.bezeich = "Ttl " + to_string(substring(bezeich, 0, 9) , "x(9)") +\
                            to_string(substring(bezeich, 9, 13) , "x(13)")
                    stockoh_list.actval = to_string(t_val, "->,>>>,>>>,>>9")


                stockoh_list = Stockoh_list()
                stockoh_list_data.append(stockoh_list)

        art_bestand_data.clear()


    def create_stock2():

        nonlocal stockoh_list_data, do_it, curr_art, curr_lager, out_bestand, zwkum, t_val, bezeich, j, tot_prev, tot_value, tot_in, tot_out, total_in, total_out, total_prev, total_value, start_from_date, loop, loop_date, diff_month, long_digit, htparam, l_artikel, l_besthis, l_ophis, l_lager, l_untergrup
        nonlocal from_lager, to_lager, from_art, to_art, to_date, move_art, end_notzero, global_oh, from_date


        nonlocal stockoh_list, art_bestand, t_vkpreis, tot_t_vkpreis
        nonlocal stockoh_list_data, art_bestand_data, t_vkpreis_data, tot_t_vkpreis_data


        t_vkpreis_data.clear()

        l_besthis_obj_list = {}
        l_besthis = L_besthis()
        l_artikel = L_artikel()
        for l_besthis.artnr, l_besthis.anz_anf_best, l_besthis.anz_eingang, l_besthis.anz_ausgang, l_besthis.val_anf_best, l_besthis.wert_eingang, l_besthis.wert_ausgang, l_besthis.lager_nr, l_besthis._recid, l_artikel.vk_preis, l_artikel.zwkum, l_artikel.bezeich, l_artikel._recid in db_session.query(L_besthis.artnr, L_besthis.anz_anf_best, L_besthis.anz_eingang, L_besthis.anz_ausgang, L_besthis.val_anf_best, L_besthis.wert_eingang, L_besthis.wert_ausgang, L_besthis.lager_nr, L_besthis._recid, L_artikel.vk_preis, L_artikel.zwkum, L_artikel.bezeich, L_artikel._recid).join(L_artikel,(L_artikel.artnr == L_besthis.artnr)).filter(
                 (L_besthis.lager_nr == 0) & (L_besthis.anf_best_dat >= date_mdy(get_month(from_date) , 1 , get_year(from_date))) & (L_besthis.anf_best_dat <= date_mdy(get_month(to_date) , 1 , get_year(to_date))) & (L_besthis.artnr >= from_art) & (L_besthis.artnr <= to_art)).order_by(L_artikel.zwkum, L_artikel.artnr).all():
            if l_besthis_obj_list.get(l_besthis._recid):
                continue
            else:
                l_besthis_obj_list[l_besthis._recid] = True

            t_vkpreis = query(t_vkpreis_data, filters=(lambda t_vkpreis: t_vkpreis.artnr == l_besthis.artnr), first=True)

            if t_vkpreis:
                t_vkpreis.qty_end =  to_decimal(t_vkpreis.qty_end) + to_decimal((l_besthis.anz_anf_best) + to_decimal(l_besthis.anz_eingang) - to_decimal(l_besthis.anz_ausgang))
                t_vkpreis.val_end =  to_decimal(t_vkpreis.val_end) + to_decimal((l_besthis.val_anf_best) + to_decimal(l_besthis.wert_eingang) - to_decimal(l_besthis.wert_ausgang))

                if t_vkpreis.val_end == 0 or t_vkpreis.qty_end == 0:
                    t_vkpreis.vk_preis =  to_decimal(t_vkpreis.vk_preis) + to_decimal(l_artikel.vk_preis)
                else:
                    t_vkpreis.vk_preis =  to_decimal(t_vkpreis.vk_preis) + to_decimal((t_vkpreis.val_end) / to_decimal((t_vkpreis.qty_end)))
            else:
                t_vkpreis = T_vkpreis()
                t_vkpreis_data.append(t_vkpreis)

                t_vkpreis.lager = l_besthis.lager_nr
                t_vkpreis.artnr = l_besthis.artnr
                t_vkpreis.zwkum = l_artikel.zwkum
                t_vkpreis.bezeich = l_artikel.bezeich
                t_vkpreis.qty_end =  to_decimal(l_besthis.anz_anf_best) + to_decimal(l_besthis.anz_eingang) - to_decimal(l_besthis.anz_ausgang)
                t_vkpreis.val_end =  to_decimal(l_besthis.val_anf_best) + to_decimal(l_besthis.wert_eingang) - to_decimal(l_besthis.wert_ausgang)

                if t_vkpreis.val_end == 0 or t_vkpreis.qty_end == 0:
                    t_vkpreis.vk_preis =  to_decimal(l_artikel.vk_preis)
                else:
                    t_vkpreis.vk_preis =  to_decimal(t_vkpreis.val_end) / to_decimal((t_vkpreis.qty_end))

        for l_besthis in db_session.query(L_besthis).filter(
                 (L_besthis.anf_best_dat == from_date) & (L_besthis.lager_nr == 0) & (L_besthis.artnr >= from_art) & (L_besthis.artnr <= to_art)).order_by(L_besthis._recid).all():

            t_vkpreis = query(t_vkpreis_data, filters=(lambda t_vkpreis: t_vkpreis.artnr == l_besthis.artnr), first=True)

            if t_vkpreis:
                do_it = True

                if do_it:
                    art_bestand = Art_bestand()
                    art_bestand_data.append(art_bestand)

                    art_bestand.bezeich = t_vkpreis.bezeich
                    art_bestand.zwkum = t_vkpreis.zwkum
                    art_bestand.artnr = l_besthis.artnr
                    art_bestand.lager = l_besthis.lager_nr
                    art_bestand.prevqty =  to_decimal(l_besthis.anz_anf_best)
                    art_bestand.prevval =  to_decimal(l_besthis.val_anf_best)
                    art_bestand.actqty =  to_decimal(l_besthis.anz_anf_best)
                    art_bestand.actval =  to_decimal(l_besthis.val_anf_best)

        for art_bestand in query(art_bestand_data):

            t_vkpreis = query(t_vkpreis_data, filters=(lambda t_vkpreis: t_vkpreis.artnr == art_bestand.artnr), first=True)

            if t_vkpreis:

                for l_ophis in db_session.query(L_ophis).filter(
                         (L_ophis.artnr == art_bestand.artnr) & ((L_ophis.datum >= start_from_date) & (L_ophis.datum <= to_date)) & (not_(matches(L_ophis.fibukonto,"*;CANCELLED*")))).order_by(L_ophis.datum).all():

                    if l_ophis.op_art == 1 or l_ophis.op_art == 2:
                        art_bestand.incoming =  to_decimal(art_bestand.incoming) + to_decimal(l_ophis.anzahl)
                        art_bestand.in_val =  to_decimal(art_bestand.in_val) + to_decimal(l_ophis.anzahl) * to_decimal((t_vkpreis.vk_preis) / to_decimal((diff_month) + to_decimal(1)))
                        art_bestand.actqty =  to_decimal(art_bestand.actqty) + to_decimal(l_ophis.anzahl)

                    elif l_ophis.op_art == 3 or l_ophis.op_art == 4:
                        art_bestand.outgoing =  to_decimal(art_bestand.outgoing) + to_decimal(l_ophis.anzahl)
                        art_bestand.out_val =  to_decimal(art_bestand.out_val) + to_decimal(l_ophis.anzahl) * to_decimal((t_vkpreis.vk_preis) / to_decimal((diff_month) + to_decimal(1)))
                        art_bestand.actqty =  to_decimal(art_bestand.actqty) - to_decimal(l_ophis.anzahl)
                art_bestand.prevval =  to_decimal(art_bestand.prevqty) * to_decimal((t_vkpreis.vk_preis) / to_decimal((diff_month) + to_decimal(1)))
                art_bestand.actval =  to_decimal(art_bestand.actqty) * to_decimal((t_vkpreis.vk_preis) / to_decimal((diff_month) + to_decimal(1)))
        bezeich = ""
        stockoh_list = Stockoh_list()
        stockoh_list_data.append(stockoh_list)

        stockoh_list.bezeich = to_string("00") + " - " + to_string("ALL STORE")
        tot_prev =  to_decimal("0")
        tot_in =  to_decimal("0")
        tot_out =  to_decimal("0")
        tot_value =  to_decimal("0")
        total_value =  to_decimal("0")
        zwkum = 0
        t_val =  to_decimal("0")

        for art_bestand in query(art_bestand_data, filters=(lambda art_bestand: art_bestand.artnr >= from_art and art_bestand.artnr <= to_art), sort_by=[("zwkum",False),("bezeich",False)]):

            if (move_art and end_notzero) and (art_bestand.incoming != 0 or art_bestand.outgoing != 0 or art_bestand.actqty != 0):

                if zwkum == 0:
                    zwkum = art_bestand.zwkum

                    l_untergrup = get_cache (L_untergrup, {"zwkum": [(eq, zwkum)]})

                    if l_untergrup:
                        bezeich = l_untergrup.bezeich

                if zwkum != art_bestand.zwkum:
                    stockoh_list = Stockoh_list()
                    stockoh_list_data.append(stockoh_list)


                    if not long_digit:
                        stockoh_list.bezeich = "Ttl " + to_string(substring(bezeich, 0, 9) , "x(9)") +\
                                to_string(substring(bezeich, 9, 13) , "x(13)")
                        stockoh_list.actval = to_string(t_val, "->>,>>>,>>9.99")


                    else:
                        stockoh_list.bezeich = "Ttl " + to_string(substring(bezeich, 0, 9) , "x(9)") +\
                                to_string(substring(bezeich, 9, 13) , "x(13)")
                        stockoh_list.actval = to_string(t_val, "->,>>>,>>>,>>9")


                    stockoh_list = Stockoh_list()
                    stockoh_list_data.append(stockoh_list)

                    t_val =  to_decimal("0")
                    zwkum = art_bestand.zwkum

                    l_untergrup = get_cache (L_untergrup, {"zwkum": [(eq, zwkum)]})

                    if l_untergrup:
                        bezeich = l_untergrup.bezeich

                if art_bestand.avrg_pr == 0:

                    if art_bestand.actqty != 0:
                        art_bestand.avrg_pr =  to_decimal(art_bestand.actval) / to_decimal(art_bestand.actqty)
                    else:
                        art_bestand.actval =  to_decimal("0")

                        t_vkpreis = query(t_vkpreis_data, filters=(lambda t_vkpreis: t_vkpreis.artnr == art_bestand.artnr), first=True)

                        if t_vkpreis:
                            art_bestand.avrg_pr = ( to_decimal(t_vkpreis.vk_preis) / to_decimal((diff_month) + to_decimal(1)))
                stockoh_list = Stockoh_list()
                stockoh_list_data.append(stockoh_list)


                if not long_digit:
                    stockoh_list.artnr = to_string(art_bestand.artnr, "9999999")
                    stockoh_list.bezeich = to_string(art_bestand.bezeich, "x(50)")
                    stockoh_list.prevqty = to_string(art_bestand.prevqty, "->,>>>,>>9.99")
                    stockoh_list.prevval = to_string(art_bestand.prevval, "->>,>>>,>>9.99")
                    stockoh_list.incoming = to_string(art_bestand.incoming, "->,>>>,>>9.99")
                    stockoh_list.outgoing = to_string(art_bestand.outgoing, "->,>>>,>>9.99")
                    stockoh_list.outgoingval = to_string(art_bestand.out_val, "->>>,>>>,>>9.99")
                    stockoh_list.incomingval = to_string(art_bestand.in_val, "->>>,>>>,>>9.99")
                    stockoh_list.actqty = to_string(art_bestand.actqty, "->,>>>,>>9.99")
                    stockoh_list.actval = to_string(art_bestand.actval, "->>,>>>,>>9.99")
                    stockoh_list.avrg_pr = to_string(art_bestand.avrg_pr, "->>,>>>,>>9.99")


                else:
                    stockoh_list.artnr = to_string(art_bestand.artnr, "9999999")
                    stockoh_list.bezeich = to_string(art_bestand.bezeich, "x(50)")
                    stockoh_list.prevqty = to_string(art_bestand.prevqty, "->,>>>,>>9.99")
                    stockoh_list.prevval = to_string(art_bestand.prevval, "->,>>>,>>>,>>9")
                    stockoh_list.incoming = to_string(art_bestand.incoming, "->,>>>,>>9.99")
                    stockoh_list.outgoing = to_string(art_bestand.outgoing, "->,>>>,>>9.99")
                    stockoh_list.outgoingval = to_string(art_bestand.out_val, "->>>,>>>,>>9.99")
                    stockoh_list.incomingval = to_string(art_bestand.in_val, "->>>,>>>,>>9.99")
                    stockoh_list.actqty = to_string(art_bestand.actqty, "->,>>>,>>9.99")
                    stockoh_list.actval = to_string(art_bestand.actval, "->,>>>,>>>,>>9")
                    stockoh_list.avrg_pr = to_string(art_bestand.avrg_pr, ">>,>>>,>>>,>>9")


                t_val =  to_decimal(t_val) + to_decimal(art_bestand.actval)
                tot_in =  to_decimal(tot_in) + to_decimal(art_bestand.in_val)
                tot_out =  to_decimal(tot_out) + to_decimal(art_bestand.out_val)
                tot_prev =  to_decimal(tot_prev) + to_decimal(art_bestand.prevval)
                tot_value =  to_decimal(tot_value) + to_decimal(art_bestand.actval)
                total_in =  to_decimal(total_in) + to_decimal(art_bestand.in_val)
                total_out =  to_decimal(total_out) + to_decimal(art_bestand.out_val)
                total_prev =  to_decimal(total_prev) + to_decimal(art_bestand.prevval)
                total_value =  to_decimal(total_value) + to_decimal(art_bestand.actval)

            elif (move_art and not end_notzero) and (art_bestand.incoming != 0 or art_bestand.outgoing != 0):

                if zwkum == 0:
                    zwkum = art_bestand.zwkum

                    l_untergrup = get_cache (L_untergrup, {"zwkum": [(eq, zwkum)]})

                    if l_untergrup:
                        bezeich = l_untergrup.bezeich

                if zwkum != art_bestand.zwkum:
                    stockoh_list = Stockoh_list()
                    stockoh_list_data.append(stockoh_list)


                    if not long_digit:
                        stockoh_list.bezeich = "Ttl " + to_string(substring(bezeich, 0, 9) , "x(9)") +\
                                to_string(substring(bezeich, 9, 13) , "x(13)")
                        stockoh_list.actval = to_string(t_val, "->>,>>>,>>9.99")


                    else:
                        stockoh_list.bezeich = "Ttl " + to_string(substring(bezeich, 0, 9) , "x(9)") +\
                                to_string(substring(bezeich, 9, 13) , "x(13)")
                        stockoh_list.actval = to_string(t_val, "->,>>>,>>>,>>9")


                    stockoh_list = Stockoh_list()
                    stockoh_list_data.append(stockoh_list)

                    t_val =  to_decimal("0")
                    zwkum = art_bestand.zwkum

                    l_untergrup = get_cache (L_untergrup, {"zwkum": [(eq, zwkum)]})

                    if l_untergrup:
                        bezeich = l_untergrup.bezeich

                if art_bestand.avrg_pr == 0:

                    if art_bestand.actqty != 0:
                        art_bestand.avrg_pr =  to_decimal(art_bestand.actval) / to_decimal(art_bestand.actqty)
                    else:
                        art_bestand.actval =  to_decimal("0")

                        t_vkpreis = query(t_vkpreis_data, filters=(lambda t_vkpreis: t_vkpreis.artnr == art_bestand.artnr), first=True)

                        if t_vkpreis:
                            art_bestand.avrg_pr = ( to_decimal(t_vkpreis.vk_preis) / to_decimal((diff_month) + to_decimal(1)))
                stockoh_list = Stockoh_list()
                stockoh_list_data.append(stockoh_list)


                if not long_digit:
                    stockoh_list.artnr = to_string(art_bestand.artnr, "9999999")
                    stockoh_list.bezeich = to_string(art_bestand.bezeich, "x(50)")
                    stockoh_list.prevqty = to_string(art_bestand.prevqty, "->,>>>,>>9.99")
                    stockoh_list.prevval = to_string(art_bestand.prevval, "->>,>>>,>>9.99")
                    stockoh_list.incoming = to_string(art_bestand.incoming, "->,>>>,>>9.99")
                    stockoh_list.outgoing = to_string(art_bestand.outgoing, "->,>>>,>>9.99")
                    stockoh_list.outgoingval = to_string(art_bestand.out_val, "->>>,>>>,>>9.99")
                    stockoh_list.incomingval = to_string(art_bestand.in_val, "->>>,>>>,>>9.99")
                    stockoh_list.actqty = to_string(art_bestand.actqty, "->,>>>,>>9.99")
                    stockoh_list.actval = to_string(art_bestand.actval, "->>,>>>,>>9.99")
                    stockoh_list.avrg_pr = to_string(art_bestand.avrg_pr, "->>,>>>,>>9.99")


                else:
                    stockoh_list.artnr = to_string(art_bestand.artnr, "9999999")
                    stockoh_list.bezeich = to_string(art_bestand.bezeich, "x(50)")
                    stockoh_list.prevqty = to_string(art_bestand.prevqty, "->,>>>,>>9.99")
                    stockoh_list.prevval = to_string(art_bestand.prevval, "->,>>>,>>>,>>9")
                    stockoh_list.incoming = to_string(art_bestand.incoming, "->,>>>,>>9.99")
                    stockoh_list.outgoing = to_string(art_bestand.outgoing, "->,>>>,>>9.99")
                    stockoh_list.outgoingval = to_string(art_bestand.out_val, "->>>,>>>,>>9.99")
                    stockoh_list.incomingval = to_string(art_bestand.in_val, "->>>,>>>,>>9.99")
                    stockoh_list.actqty = to_string(art_bestand.actqty, "->,>>>,>>9.99")
                    stockoh_list.actval = to_string(art_bestand.actval, "->,>>>,>>>,>>9")
                    stockoh_list.avrg_pr = to_string(art_bestand.avrg_pr, ">>,>>>,>>>,>>9")


                t_val =  to_decimal(t_val) + to_decimal(art_bestand.actval)
                tot_in =  to_decimal(tot_in) + to_decimal(art_bestand.in_val)
                tot_out =  to_decimal(tot_out) + to_decimal(art_bestand.out_val)
                tot_prev =  to_decimal(tot_prev) + to_decimal(art_bestand.prevval)
                tot_value =  to_decimal(tot_value) + to_decimal(art_bestand.actval)
                total_in =  to_decimal(total_in) + to_decimal(art_bestand.in_val)
                total_out =  to_decimal(total_out) + to_decimal(art_bestand.out_val)
                total_prev =  to_decimal(total_prev) + to_decimal(art_bestand.prevval)
                total_value =  to_decimal(total_value) + to_decimal(art_bestand.actval)

            elif (not move_art and end_notzero) and (art_bestand.actqty != 0):

                if zwkum == 0:
                    zwkum = art_bestand.zwkum

                    l_untergrup = get_cache (L_untergrup, {"zwkum": [(eq, zwkum)]})

                    if l_untergrup:
                        bezeich = l_untergrup.bezeich

                if zwkum != art_bestand.zwkum:
                    stockoh_list = Stockoh_list()
                    stockoh_list_data.append(stockoh_list)


                    if not long_digit:
                        stockoh_list.bezeich = "Ttl " + to_string(substring(bezeich, 0, 9) , "x(9)") +\
                                to_string(substring(bezeich, 9, 13) , "x(13)")
                        stockoh_list.actval = to_string(t_val, "->>,>>>,>>9.99")


                    else:
                        stockoh_list.bezeich = "Ttl " + to_string(substring(bezeich, 0, 9) , "x(9)") +\
                                to_string(substring(bezeich, 9, 13) , "x(13)")
                        stockoh_list.actval = to_string(t_val, "->,>>>,>>>,>>9")


                    stockoh_list = Stockoh_list()
                    stockoh_list_data.append(stockoh_list)

                    t_val =  to_decimal("0")
                    zwkum = art_bestand.zwkum

                    l_untergrup = get_cache (L_untergrup, {"zwkum": [(eq, zwkum)]})

                    if l_untergrup:
                        bezeich = l_untergrup.bezeich

                if art_bestand.avrg_pr == 0:

                    if art_bestand.actqty != 0:
                        art_bestand.avrg_pr =  to_decimal(art_bestand.actval) / to_decimal(art_bestand.actqty)
                    else:
                        art_bestand.actval =  to_decimal("0")

                        t_vkpreis = query(t_vkpreis_data, filters=(lambda t_vkpreis: t_vkpreis.artnr == art_bestand.artnr), first=True)

                        if t_vkpreis:
                            art_bestand.avrg_pr = ( to_decimal(t_vkpreis.vk_preis) / to_decimal((diff_month) + to_decimal(1)))
                stockoh_list = Stockoh_list()
                stockoh_list_data.append(stockoh_list)


                if not long_digit:
                    stockoh_list.artnr = to_string(art_bestand.artnr, "9999999")
                    stockoh_list.bezeich = to_string(art_bestand.bezeich, "x(50)")
                    stockoh_list.prevqty = to_string(art_bestand.prevqty, "->,>>>,>>9.99")
                    stockoh_list.prevval = to_string(art_bestand.prevval, "->>,>>>,>>9.99")
                    stockoh_list.incoming = to_string(art_bestand.incoming, "->,>>>,>>9.99")
                    stockoh_list.outgoing = to_string(art_bestand.outgoing, "->,>>>,>>9.99")
                    stockoh_list.outgoingval = to_string(art_bestand.out_val, "->>>,>>>,>>9.99")
                    stockoh_list.incomingval = to_string(art_bestand.in_val, "->>>,>>>,>>9.99")
                    stockoh_list.actqty = to_string(art_bestand.actqty, "->,>>>,>>9.99")
                    stockoh_list.actval = to_string(art_bestand.actval, "->>,>>>,>>9.99")
                    stockoh_list.avrg_pr = to_string(art_bestand.avrg_pr, "->>,>>>,>>9.99")


                else:
                    stockoh_list.artnr = to_string(art_bestand.artnr, "9999999")
                    stockoh_list.bezeich = to_string(art_bestand.bezeich, "x(50)")
                    stockoh_list.prevqty = to_string(art_bestand.prevqty, "->,>>>,>>9.99")
                    stockoh_list.prevval = to_string(art_bestand.prevval, "->,>>>,>>>,>>9")
                    stockoh_list.incoming = to_string(art_bestand.incoming, "->,>>>,>>9.99")
                    stockoh_list.outgoing = to_string(art_bestand.outgoing, "->,>>>,>>9.99")
                    stockoh_list.outgoingval = to_string(art_bestand.out_val, "->>>,>>>,>>9.99")
                    stockoh_list.incomingval = to_string(art_bestand.in_val, "->>>,>>>,>>9.99")
                    stockoh_list.actqty = to_string(art_bestand.actqty, "->,>>>,>>9.99")
                    stockoh_list.actval = to_string(art_bestand.actval, "->,>>>,>>>,>>9")
                    stockoh_list.avrg_pr = to_string(art_bestand.avrg_pr, ">>,>>>,>>>,>>9")


                t_val =  to_decimal(t_val) + to_decimal(art_bestand.actval)
                tot_in =  to_decimal(tot_in) + to_decimal(art_bestand.in_val)
                tot_out =  to_decimal(tot_out) + to_decimal(art_bestand.out_val)
                tot_prev =  to_decimal(tot_prev) + to_decimal(art_bestand.prevval)
                tot_value =  to_decimal(tot_value) + to_decimal(art_bestand.actval)
                total_in =  to_decimal(total_in) + to_decimal(art_bestand.in_val)
                total_out =  to_decimal(total_out) + to_decimal(art_bestand.out_val)
                total_prev =  to_decimal(total_prev) + to_decimal(art_bestand.prevval)
                total_value =  to_decimal(total_value) + to_decimal(art_bestand.actval)

            elif (not move_art and not end_notzero):

                if zwkum == 0:
                    zwkum = art_bestand.zwkum

                    l_untergrup = get_cache (L_untergrup, {"zwkum": [(eq, zwkum)]})

                    if l_untergrup:
                        bezeich = l_untergrup.bezeich

                if zwkum != art_bestand.zwkum:
                    stockoh_list = Stockoh_list()
                    stockoh_list_data.append(stockoh_list)


                    if not long_digit:
                        stockoh_list.bezeich = "Ttl " + to_string(substring(bezeich, 0, 9) , "x(9)") +\
                                to_string(substring(bezeich, 9, 13) , "x(13)")
                        stockoh_list.actval = to_string(t_val, "->>,>>>,>>9.99")


                    else:
                        stockoh_list.bezeich = "Ttl " + to_string(substring(bezeich, 0, 9) , "x(9)") +\
                                to_string(substring(bezeich, 9, 13) , "x(13)")
                        stockoh_list.actval = to_string(t_val, "->,>>>,>>>,>>9")


                    stockoh_list = Stockoh_list()
                    stockoh_list_data.append(stockoh_list)

                    t_val =  to_decimal("0")
                    zwkum = art_bestand.zwkum

                    l_untergrup = get_cache (L_untergrup, {"zwkum": [(eq, zwkum)]})

                    if l_untergrup:
                        bezeich = l_untergrup.bezeich

                if art_bestand.avrg_pr == 0:

                    if art_bestand.actqty != 0:
                        art_bestand.avrg_pr =  to_decimal(art_bestand.actval) / to_decimal(art_bestand.actqty)
                    else:
                        art_bestand.actval =  to_decimal("0")

                        t_vkpreis = query(t_vkpreis_data, filters=(lambda t_vkpreis: t_vkpreis.artnr == art_bestand.artnr), first=True)

                        if t_vkpreis:
                            art_bestand.avrg_pr = ( to_decimal(t_vkpreis.vk_preis) / to_decimal((diff_month) + to_decimal(1)))
                stockoh_list = Stockoh_list()
                stockoh_list_data.append(stockoh_list)


                if not long_digit:
                    stockoh_list.artnr = to_string(art_bestand.artnr, "9999999")
                    stockoh_list.bezeich = to_string(art_bestand.bezeich, "x(50)")
                    stockoh_list.prevqty = to_string(art_bestand.prevqty, "->,>>>,>>9.99")
                    stockoh_list.prevval = to_string(art_bestand.prevval, "->>,>>>,>>9.99")
                    stockoh_list.incoming = to_string(art_bestand.incoming, "->,>>>,>>9.99")
                    stockoh_list.outgoing = to_string(art_bestand.outgoing, "->,>>>,>>9.99")
                    stockoh_list.outgoingval = to_string(art_bestand.out_val, "->>>,>>>,>>9.99")
                    stockoh_list.incomingval = to_string(art_bestand.in_val, "->>>,>>>,>>9.99")
                    stockoh_list.actqty = to_string(art_bestand.actqty, "->,>>>,>>9.99")
                    stockoh_list.actval = to_string(art_bestand.actval, "->>,>>>,>>9.99")
                    stockoh_list.avrg_pr = to_string(art_bestand.avrg_pr, "->>,>>>,>>9.99")


                else:
                    stockoh_list.artnr = to_string(art_bestand.artnr, "9999999")
                    stockoh_list.bezeich = to_string(art_bestand.bezeich, "x(50)")
                    stockoh_list.prevqty = to_string(art_bestand.prevqty, "->,>>>,>>9.99")
                    stockoh_list.prevval = to_string(art_bestand.prevval, "->,>>>,>>>,>>9")
                    stockoh_list.incoming = to_string(art_bestand.incoming, "->,>>>,>>9.99")
                    stockoh_list.outgoing = to_string(art_bestand.outgoing, "->,>>>,>>9.99")
                    stockoh_list.outgoingval = to_string(art_bestand.out_val, "->>>,>>>,>>9.99")
                    stockoh_list.incomingval = to_string(art_bestand.in_val, "->>>,>>>,>>9.99")
                    stockoh_list.actqty = to_string(art_bestand.actqty, "->,>>>,>>9.99")
                    stockoh_list.actval = to_string(art_bestand.actval, "->,>>>,>>>,>>9")
                    stockoh_list.avrg_pr = to_string(art_bestand.avrg_pr, ">>,>>>,>>>,>>9")


                t_val =  to_decimal(t_val) + to_decimal(art_bestand.actval)
                tot_in =  to_decimal(tot_in) + to_decimal(art_bestand.in_val)
                tot_out =  to_decimal(tot_out) + to_decimal(art_bestand.out_val)
                tot_prev =  to_decimal(tot_prev) + to_decimal(art_bestand.prevval)
                tot_value =  to_decimal(tot_value) + to_decimal(art_bestand.actval)
                total_in =  to_decimal(total_in) + to_decimal(art_bestand.in_val)
                total_out =  to_decimal(total_out) + to_decimal(art_bestand.out_val)
                total_prev =  to_decimal(total_prev) + to_decimal(art_bestand.prevval)
                total_value =  to_decimal(total_value) + to_decimal(art_bestand.actval)

        if bezeich != "":
            stockoh_list = Stockoh_list()
            stockoh_list_data.append(stockoh_list)


            if not long_digit:
                stockoh_list.bezeich = "Ttl " + to_string(substring(bezeich, 0, 9) , "x(9)") +\
                        to_string(substring(bezeich, 9, 13) , "x(13)")
                stockoh_list.actval = to_string(t_val, "->>,>>>,>>9.99")


            else:
                stockoh_list.bezeich = "Ttl " + to_string(substring(bezeich, 0, 9) , "x(9)") +\
                        to_string(substring(bezeich, 9, 13) , "x(13)")
                stockoh_list.actval = to_string(t_val, "->,>>>,>>>,>>9")


            stockoh_list = Stockoh_list()
            stockoh_list_data.append(stockoh_list)

        art_bestand_data.clear()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 246)]})

    if htparam:
        long_digit = htparam.flogical
    start_from_date = date_mdy(get_month(from_date) , 1 , get_year(from_date))
    diff_month = calc_month_diff(from_date, to_date)

    if global_oh == None:
        global_oh = False

    if end_notzero == None:
        end_notzero = False

    if not global_oh:
        create_stock1()
    else:
        create_stock2()

    return generate_output()