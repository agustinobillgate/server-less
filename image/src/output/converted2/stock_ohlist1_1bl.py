#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpdate import htpdate
from models import L_bestand, L_besthis, Htparam, L_lager, L_artikel, L_op, L_ophis, L_untergrup, Printcod

def stock_ohlist1_1bl(from_lager:int, to_lager:int, from_art:int, to_art:int, from_date:date, to_date:date, move_art:bool):

    prepare_cache ([L_bestand, L_besthis, Htparam, L_lager, L_artikel, L_op, L_ophis, L_untergrup])

    stockoh_list_list = []
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
    tdate:date = None
    qty:Decimal = to_decimal("0.0")
    wert:Decimal = to_decimal("0.0")
    long_digit:bool = False
    l_bestand = l_besthis = htparam = l_lager = l_artikel = l_op = l_ophis = l_untergrup = printcod = None

    stockoh_list = art_bestand = l_oh = l_ohis = None

    stockoh_list_list, Stockoh_list = create_model("Stockoh_list", {"artnr":string, "bezeich":string, "prevqty":string, "prevval":string, "incoming":string, "incomingval":string, "outgoing":string, "outgoingval":string, "actqty":string, "actval":string, "avrg_pr":string})
    art_bestand_list, Art_bestand = create_model("Art_bestand", {"lager":int, "artnr":int, "zwkum":int, "bezeich":string, "incoming":Decimal, "in_val":Decimal, "out_val":Decimal, "outgoing":Decimal, "prevqty":Decimal, "prevval":Decimal, "adjust":Decimal, "actqty":Decimal, "actval":Decimal, "avrg_pr":Decimal})

    L_oh = create_buffer("L_oh",L_bestand)
    L_ohis = create_buffer("L_ohis",L_besthis)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal stockoh_list_list, do_it, curr_art, curr_lager, out_bestand, zwkum, t_val, bezeich, j, tot_prev, tot_value, tot_in, tot_out, total_in, total_out, total_prev, total_value, tdate, qty, wert, long_digit, l_bestand, l_besthis, htparam, l_lager, l_artikel, l_op, l_ophis, l_untergrup, printcod
        nonlocal from_lager, to_lager, from_art, to_art, from_date, to_date, move_art
        nonlocal l_oh, l_ohis


        nonlocal stockoh_list, art_bestand, l_oh, l_ohis
        nonlocal stockoh_list_list, art_bestand_list

        return {"stockoh-list": stockoh_list_list}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 246)]})
    long_digit = htparam.flogical
    tdate = get_output(htpdate(87))

    if get_month(to_date) <= get_month(tdate) and get_month(from_date) <= get_month(tdate):

        for l_lager in db_session.query(L_lager).filter(
                 (L_lager.lager_nr >= from_lager) & (L_lager.lager_nr <= to_lager)).order_by(L_lager._recid).all():
            zwkum = 0
            t_val =  to_decimal("0")

            l_bestand_obj_list = {}
            l_bestand = L_bestand()
            l_artikel = L_artikel()
            for l_bestand.artnr, l_bestand.anz_anf_best, l_bestand.val_anf_best, l_bestand._recid, l_artikel.bezeich, l_artikel.zwkum, l_artikel.vk_preis, l_artikel._recid in db_session.query(L_bestand.artnr, L_bestand.anz_anf_best, L_bestand.val_anf_best, L_bestand._recid, L_artikel.bezeich, L_artikel.zwkum, L_artikel.vk_preis, L_artikel._recid).join(L_artikel,(L_artikel.artnr == L_bestand.artnr)).filter(
                     (L_bestand.lager_nr == l_lager.lager_nr) & (L_bestand.artnr >= from_art) & (L_bestand.artnr <= to_art)).order_by(L_artikel.zwkum, L_artikel.artnr).all():
                if l_bestand_obj_list.get(l_bestand._recid):
                    continue
                else:
                    l_bestand_obj_list[l_bestand._recid] = True


                do_it = True

                if do_it:

                    art_bestand = query(art_bestand_list, filters=(lambda art_bestand: art_bestand.artnr == l_bestand.artnr and art_bestand.lager == l_lager.lager_nr), first=True)

                    if not art_bestand:
                        art_bestand = Art_bestand()
                        art_bestand_list.append(art_bestand)

                        art_bestand.bezeich = l_artikel.bezeich
                        art_bestand.zwkum = l_artikel.zwkum
                        art_bestand.artnr = l_bestand.artnr
                        art_bestand.lager = l_lager.lager_nr
                        art_bestand.prevqty =  to_decimal(l_bestand.anz_anf_best)
                        art_bestand.prevval =  to_decimal(l_bestand.val_anf_best)
                        art_bestand.actqty =  to_decimal(l_bestand.anz_anf_best)
                        art_bestand.actval =  to_decimal(l_bestand.val_anf_best)
                        curr_art = l_bestand.artnr
                        curr_lager = l_lager.lager_nr
                    out_bestand =  to_decimal("0")

                    for l_op in db_session.query(L_op).filter(
                             (L_op.lager_nr == l_lager.lager_nr) & (L_op.artnr == l_bestand.artnr) & ((L_op.datum >= from_date) & (L_op.datum <= to_date)) & (L_op.loeschflag <= 1)).order_by(L_op.datum).all():

                        if l_op.op_art == 1 or l_op.op_art == 2:
                            art_bestand.incoming =  to_decimal(art_bestand.incoming) + to_decimal(l_op.anzahl)
                            art_bestand.in_val =  to_decimal(art_bestand.in_val) + to_decimal(l_op.anzahl) * to_decimal(l_artikel.vk_preis)
                            art_bestand.actqty =  to_decimal(art_bestand.actqty) + to_decimal(l_op.anzahl)
                            art_bestand.actval =  to_decimal(art_bestand.actval) + to_decimal(l_op.anzahl) * to_decimal(l_artikel.vk_preis)

                        elif l_op.op_art == 3 or l_op.op_art == 4:
                            art_bestand.outgoing =  to_decimal(art_bestand.outgoing) + to_decimal(l_op.anzahl)
                            art_bestand.out_val =  to_decimal(art_bestand.out_val) + to_decimal(l_op.anzahl) * to_decimal(l_artikel.vk_preis)
                            art_bestand.actqty =  to_decimal(art_bestand.actqty) - to_decimal(l_op.anzahl)
                            art_bestand.actval =  to_decimal(art_bestand.actval) - to_decimal(l_op.anzahl) * to_decimal(l_artikel.vk_preis)

    if to_date < tdate and from_date < tdate:

        for l_lager in db_session.query(L_lager).filter(
                 (L_lager.lager_nr >= from_lager) & (L_lager.lager_nr <= to_lager)).order_by(L_lager._recid).all():
            zwkum = 0
            t_val =  to_decimal("0")

            l_besthis_obj_list = {}
            l_besthis = L_besthis()
            l_artikel = L_artikel()
            for l_besthis.artnr, l_besthis.anz_anf_best, l_besthis.val_anf_best, l_besthis._recid, l_artikel.bezeich, l_artikel.zwkum, l_artikel.vk_preis, l_artikel._recid in db_session.query(L_besthis.artnr, L_besthis.anz_anf_best, L_besthis.val_anf_best, L_besthis._recid, L_artikel.bezeich, L_artikel.zwkum, L_artikel.vk_preis, L_artikel._recid).join(L_artikel,(L_artikel.artnr == L_besthis.artnr)).filter(
                     (L_besthis.lager_nr == l_lager.lager_nr) & (L_besthis.artnr >= from_art) & (L_besthis.artnr <= to_art) & (L_besthis.anf_best_dat >= from_date) & (L_besthis.anf_best_dat <= to_date)).order_by(L_artikel.zwkum, L_artikel.artnr).all():
                if l_besthis_obj_list.get(l_besthis._recid):
                    continue
                else:
                    l_besthis_obj_list[l_besthis._recid] = True


                do_it = True

                if do_it:

                    art_bestand = query(art_bestand_list, filters=(lambda art_bestand: art_bestand.artnr == l_besthis.artnr and art_bestand.lager == l_lager.lager_nr), first=True)

                    if not art_bestand:
                        art_bestand = Art_bestand()
                        art_bestand_list.append(art_bestand)

                        art_bestand.bezeich = l_artikel.bezeich
                        art_bestand.zwkum = l_artikel.zwkum
                        art_bestand.artnr = l_besthis.artnr
                        art_bestand.lager = l_lager.lager_nr
                        art_bestand.prevqty =  to_decimal(l_besthis.anz_anf_best)
                        art_bestand.prevval =  to_decimal(l_besthis.val_anf_best)
                        art_bestand.actqty =  to_decimal(l_besthis.anz_anf_best)
                        art_bestand.actval =  to_decimal(l_besthis.val_anf_best)
                        curr_art = l_besthis.artnr
                        curr_lager = l_lager.lager_nr
                    out_bestand =  to_decimal("0")

                    for l_ophis in db_session.query(L_ophis).filter(
                             (L_ophis.lager_nr == l_lager.lager_nr) & (L_ophis.artnr == l_besthis.artnr) & ((L_ophis.datum >= from_date) & (L_ophis.datum <= to_date))).order_by(L_ophis.datum).all():

                        if l_ophis.op_art == 1 or l_ophis.op_art == 2:
                            art_bestand.incoming =  to_decimal(art_bestand.incoming) + to_decimal(l_ophis.anzahl)
                            art_bestand.in_val =  to_decimal(art_bestand.in_val) + to_decimal(l_ophis.anzahl) * to_decimal(l_artikel.vk_preis)
                            art_bestand.actqty =  to_decimal(art_bestand.actqty) + to_decimal(l_ophis.anzahl)
                            art_bestand.actval =  to_decimal(art_bestand.actval) + to_decimal(l_ophis.anzahl) * to_decimal(l_artikel.vk_preis)

                        elif l_ophis.op_art == 3 or l_ophis.op_art == 4:
                            art_bestand.outgoing =  to_decimal(art_bestand.outgoing) + to_decimal(l_ophis.anzahl)
                            art_bestand.out_val =  to_decimal(art_bestand.out_val) + to_decimal(l_ophis.anzahl) * to_decimal(l_artikel.vk_preis)
                            art_bestand.actqty =  to_decimal(art_bestand.actqty) - to_decimal(l_ophis.anzahl)
                            art_bestand.actval =  to_decimal(art_bestand.actval) - to_decimal(l_ophis.anzahl) * to_decimal(l_artikel.vk_preis)

    for l_lager in db_session.query(L_lager).filter(
             (L_lager.lager_nr >= from_lager) & (L_lager.lager_nr <= to_lager)).order_by(L_lager._recid).all():
        bezeich = ""
        stockoh_list = Stockoh_list()
        stockoh_list_list.append(stockoh_list)

        stockoh_list.bezeich = to_string(l_lager.lager_nr, "99") + " - " + to_string(l_lager.bezeich, "x(25)")
        tot_prev =  to_decimal("0")
        tot_in =  to_decimal("0")
        tot_out =  to_decimal("0")
        tot_value =  to_decimal("0")
        zwkum = 0
        t_val =  to_decimal("0")

        for art_bestand in query(art_bestand_list, filters=(lambda art_bestand: art_bestand.lager == l_lager.lager_nr and art_bestand.artnr >= from_art and art_bestand.artnr <= to_art), sort_by=[("zwkum",False),("bezeich",False)]):

            if (not move_art) or art_bestand.incoming != 0 or art_bestand.outgoing != 0:

                if zwkum == 0:
                    zwkum = art_bestand.zwkum

                    l_untergrup = get_cache (L_untergrup, {"zwkum": [(eq, zwkum)]})
                    bezeich = l_untergrup.bezeich

                if zwkum != art_bestand.zwkum:
                    stockoh_list = Stockoh_list()
                    stockoh_list_list.append(stockoh_list)


                    if not long_digit:
                        stockoh_list.bezeich = "Ttl " + to_string(substring(bezeich, 0, 9) , "x(9)") +\
                                to_string(substring(bezeich, 9, 13) , "x(13)")
                        stockoh_list.actval = to_string(t_val, "->,>>>,>>>,>>9.99")


                    else:
                        stockoh_list.bezeich = "Ttl " + to_string(substring(bezeich, 0, 9) , "x(9)") +\
                                to_string(substring(bezeich, 9, 13) , "x(13)")
                        stockoh_list.actval = to_string(t_val, "->>,>>>,>>>,>>9")


                    t_val =  to_decimal("0")
                    zwkum = art_bestand.zwkum

                    l_untergrup = get_cache (L_untergrup, {"zwkum": [(eq, zwkum)]})
                    bezeich = l_untergrup.bezeich

                l_artikel = get_cache (L_artikel, {"artnr": [(eq, art_bestand.artnr)]})

                if art_bestand.avrg_pr == 0:

                    if art_bestand.actqty != 0:
                        art_bestand.avrg_pr =  to_decimal(art_bestand.actval) / to_decimal(art_bestand.actqty)
                else:
                    art_bestand.avrg_pr =  to_decimal(l_artikel.vk_preis)
                    art_bestand.actval =  to_decimal("0")


                stockoh_list = Stockoh_list()
                stockoh_list_list.append(stockoh_list)


                if not long_digit:
                    stockoh_list.artnr = to_string(art_bestand.artnr, "9999999")
                    stockoh_list.bezeich = to_string(art_bestand.bezeich, "x(30)")
                    stockoh_list.prevqty = to_string(art_bestand.prevqty, "->,>>>,>>9.99")
                    stockoh_list.prevval = to_string(art_bestand.prevval, "->>,>>>,>>9.99")
                    stockoh_list.incoming = to_string(art_bestand.incoming, "->,>>>,>>9.99")
                    stockoh_list.outgoing = to_string(art_bestand.outgoing, "->,>>>,>>9.99")
                    stockoh_list.outgoingval = to_string(art_bestand.out_val, "->>>,>>>,>>9.99")
                    stockoh_list.incomingval = to_string(art_bestand.in_val, "->>>,>>>,>>9.99")
                    stockoh_list.actqty = to_string(art_bestand.actqty, "->,>>>,>>9.99")
                    stockoh_list.actval = to_string(art_bestand.actval, "->,>>>,>>>,>>9.99")
                    stockoh_list.avrg_pr = to_string(art_bestand.avrg_pr, "->>>,>>>,>>>,>>9.99")


                else:
                    stockoh_list.artnr = to_string(art_bestand.artnr, "9999999")
                    stockoh_list.bezeich = to_string(art_bestand.bezeich, "x(30)")
                    stockoh_list.prevqty = to_string(art_bestand.prevqty, "->,>>>,>>9.99")
                    stockoh_list.prevval = to_string(art_bestand.prevval, "->,>>>,>>>,>>9")
                    stockoh_list.incoming = to_string(art_bestand.incoming, "->,>>>,>>9.99")
                    stockoh_list.outgoing = to_string(art_bestand.outgoing, "->,>>>,>>9.99")
                    stockoh_list.outgoingval = to_string(art_bestand.out_val, "->>>,>>>,>>9.99")
                    stockoh_list.incomingval = to_string(art_bestand.in_val, "->>>,>>>,>>9.99")
                    stockoh_list.actqty = to_string(art_bestand.actqty, "->,>>>,>>9.99")
                    stockoh_list.actval = to_string(art_bestand.actval, "->>,>>>,>>>,>>9")
                    stockoh_list.avrg_pr = to_string(art_bestand.avrg_pr, "->>,>>>,>>>,>>>,>>9")


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
            stockoh_list_list.append(stockoh_list)


            if not long_digit:
                stockoh_list.bezeich = "Ttl " + to_string(substring(bezeich, 0, 9) , "x(9)") +\
                        to_string(substring(bezeich, 9, 13) , "x(13)")
                stockoh_list.actval = to_string(t_val, "->,>>>,>>>,>>9.99")


            else:
                stockoh_list.bezeich = "Ttl " + to_string(substring(bezeich, 0, 9) , "x(9)") +\
                        to_string(substring(bezeich, 9, 13) , "x(13)")
                stockoh_list.actval = to_string(t_val, "->>,>>>,>>>,>>9")


            stockoh_list = Stockoh_list()
            stockoh_list_list.append(stockoh_list)


            if not long_digit:
                stockoh_list.bezeich = "Ttl " + to_string(l_lager.bezeich, "x(25)")
                stockoh_list.actval = to_string(tot_value, "->,>>>,>>>,>>9.99")


            else:
                stockoh_list.bezeich = "Ttl " + to_string(l_lager.bezeich, "x(25)")
                stockoh_list.actval = to_string(tot_value, "->>,>>>,>>>,>>9")


            stockoh_list = Stockoh_list()
            stockoh_list_list.append(stockoh_list)


    if not long_digit:
        stockoh_list.bezeich = "G R A N D T O T A L"
        stockoh_list.actval = to_string(total_value, "->,>>>,>>>,>>9.99")


    else:
        stockoh_list.bezeich = "G R A N D T O T A L"
        stockoh_list.actval = to_string(total_value, "->>,>>>,>>>,>>9")

    printcod = db_session.query(Printcod).filter(
             (Printcod.emu == ("Epson").lower()) & (Printcod.code == ("rs").lower())).first()

    if printcod:
        art_bestand_list.clear()

    return generate_output()