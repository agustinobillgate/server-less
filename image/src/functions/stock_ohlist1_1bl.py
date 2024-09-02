from functions.additional_functions import *
import decimal
from datetime import date
from functions.htpdate import htpdate
from sqlalchemy import func
from models import L_bestand, L_besthis, Htparam, L_lager, L_artikel, L_op, L_ophis, L_untergrup, Printcod

def stock_ohlist1_1bl(from_lager:int, to_lager:int, from_art:int, to_art:int, from_date:date, to_date:date, move_art:bool):
    stockoh_list_list = []
    do_it:bool = False
    curr_art:int = 0
    curr_lager:int = 0
    out_bestand:decimal = 0
    zwkum:int = 0
    t_val:decimal = 0
    bezeich:str = ""
    j:int = 0
    tot_prev:decimal = 0
    tot_value:decimal = 0
    tot_in:decimal = 0
    tot_out:decimal = 0
    total_in:decimal = 0
    total_out:decimal = 0
    total_prev:decimal = 0
    total_value:decimal = 0
    tdate:date = None
    qty:decimal = 0
    wert:decimal = 0
    long_digit:bool = False
    l_bestand = l_besthis = htparam = l_lager = l_artikel = l_op = l_ophis = l_untergrup = printcod = None

    stockoh_list = art_bestand = l_oh = l_ohis = None

    stockoh_list_list, Stockoh_list = create_model("Stockoh_list", {"artnr":str, "bezeich":str, "prevqty":str, "prevval":str, "incoming":str, "incomingval":str, "outgoing":str, "outgoingval":str, "actqty":str, "actval":str, "avrg_pr":str})
    art_bestand_list, Art_bestand = create_model("Art_bestand", {"lager":int, "artnr":int, "zwkum":int, "bezeich":str, "incoming":decimal, "in_val":decimal, "out_val":decimal, "outgoing":decimal, "prevqty":decimal, "prevval":decimal, "adjust":decimal, "actqty":decimal, "actval":decimal, "avrg_pr":decimal})

    L_oh = L_bestand
    L_ohis = L_besthis

    db_session = local_storage.db_session

    def generate_output():
        nonlocal stockoh_list_list, do_it, curr_art, curr_lager, out_bestand, zwkum, t_val, bezeich, j, tot_prev, tot_value, tot_in, tot_out, total_in, total_out, total_prev, total_value, tdate, qty, wert, long_digit, l_bestand, l_besthis, htparam, l_lager, l_artikel, l_op, l_ophis, l_untergrup, printcod
        nonlocal l_oh, l_ohis


        nonlocal stockoh_list, art_bestand, l_oh, l_ohis
        nonlocal stockoh_list_list, art_bestand_list
        return {"stockoh-list": stockoh_list_list}


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 246)).first()
    long_digit = htparam.flogical
    tdate = get_output(htpdate(87))

    if get_month(to_date) <= get_month(tdate) and get_month(from_date) <= get_month(tdate):

        for l_lager in db_session.query(L_lager).filter(
                (L_lager.lager_nr >= from_lager) &  (L_lager.lager_nr <= to_lager)).all():
            zwkum = 0
            t_val = 0

            l_bestand_obj_list = []
            for l_bestand, l_artikel in db_session.query(L_bestand, L_artikel).join(L_artikel,(L_artikel.artnr == L_bestand.artnr)).filter(
                    (L_bestand.lager_nr == l_lager.lager_nr) &  (L_bestand.artnr >= from_art) &  (L_bestand.artnr <= to_art)).all():
                if l_bestand._recid in l_bestand_obj_list:
                    continue
                else:
                    l_bestand_obj_list.append(l_bestand._recid)


                do_it = True

                if do_it:

                    art_bestand = query(art_bestand_list, filters=(lambda art_bestand :art_bestand.artnr == l_bestand.artnr and art_bestand.lager == l_lager.lager_nr), first=True)

                    if not art_bestand:
                        art_bestand = Art_bestand()
                        art_bestand_list.append(art_bestand)

                        art_bestand.bezeich = l_artikel.bezeich
                        art_bestand.zwkum = l_artikel.zwkum
                        art_bestand.artnr = l_bestand.artnr
                        art_bestand.lager = l_lager.lager_nr
                        art_bestand.prevqty = l_bestand.anz_anf_best
                        art_bestand.prevval = l_bestand.val_anf_best
                        art_bestand.actqty = l_bestand.anz_anf_best
                        art_bestand.actval = l_bestand.val_anf_best
                        curr_art = l_bestand.artnr
                        curr_lager = l_lager.lager_nr
                    out_bestand = 0

                    for l_op in db_session.query(L_op).filter(
                            (L_op.lager_nr == l_lager.lager_nr) &  (L_op.artnr == l_bestand.artnr) &  ((L_op.datum >= from_date) &  (L_op.datum <= to_date)) &  (L_op.loeschflag <= 1)).all():

                        if l_op.op_art == 1 or l_op.op_art == 2:
                            art_bestand.incoming = art_bestand.incoming + l_op.anzahl
                            art_bestand.in_val = art_bestand.in_val + l_op.anzahl * l_artikel.vk_preis
                            art_bestand.actqty = art_bestand.actqty + l_op.anzahl
                            art_bestand.actval = art_bestand.actval + l_op.anzahl * l_artikel.vk_preis

                        elif l_op.op_art == 3 or l_op.op_art == 4:
                            art_bestand.outgoing = art_bestand.outgoing + l_op.anzahl
                            art_bestand.out_val = art_bestand.out_val + l_op.anzahl * l_artikel.vk_preis
                            art_bestand.actqty = art_bestand.actqty - l_op.anzahl
                            art_bestand.actval = art_bestand.actval - l_op.anzahl * l_artikel.vk_preis

    if to_date < tdate and from_date < tdate:

        for l_lager in db_session.query(L_lager).filter(
                (L_lager.lager_nr >= from_lager) &  (L_lager.lager_nr <= to_lager)).all():
            zwkum = 0
            t_val = 0

            l_besthis_obj_list = []
            for l_besthis, l_artikel in db_session.query(L_besthis, L_artikel).join(L_artikel,(L_artikel.artnr == L_besthis.artnr)).filter(
                    (L_besthis.lager_nr == l_lager.lager_nr) &  (L_besthis.artnr >= from_art) &  (L_besthis.artnr <= to_art) &  (L_besthis.anf_best_dat >= from_date) &  (L_besthis.anf_best_dat <= to_date)).all():
                if l_besthis._recid in l_besthis_obj_list:
                    continue
                else:
                    l_besthis_obj_list.append(l_besthis._recid)


                do_it = True

                if do_it:

                    art_bestand = query(art_bestand_list, filters=(lambda art_bestand :art_bestand.artnr == l_besthis.artnr and art_bestand.lager == l_lager.lager_nr), first=True)

                    if not art_bestand:
                        art_bestand = Art_bestand()
                        art_bestand_list.append(art_bestand)

                        art_bestand.bezeich = l_artikel.bezeich
                        art_bestand.zwkum = l_artikel.zwkum
                        art_bestand.artnr = l_besthis.artnr
                        art_bestand.lager = l_lager.lager_nr
                        art_bestand.prevqty = l_besthis.anz_anf_best
                        art_bestand.prevval = l_besthis.val_anf_best
                        art_bestand.actqty = l_besthis.anz_anf_best
                        art_bestand.actval = l_besthis.val_anf_best
                        curr_art = l_besthis.artnr
                        curr_lager = l_lager.lager_nr
                    out_bestand = 0

                    for l_ophis in db_session.query(L_ophis).filter(
                            (L_ophis.lager_nr == l_lager.lager_nr) &  (L_ophis.artnr == l_besthis.artnr) &  ((L_ophis.datum >= from_date) &  (L_ophis.datum <= to_date))).all():

                        if l_ophis.op_art == 1 or l_ophis.op_art == 2:
                            art_bestand.incoming = art_bestand.incoming + l_ophis.anzahl
                            art_bestand.in_val = art_bestand.in_val + l_ophis.anzahl * l_artikel.vk_preis
                            art_bestand.actqty = art_bestand.actqty + l_ophis.anzahl
                            art_bestand.actval = art_bestand.actval + l_ophis.anzahl * l_artikel.vk_preis

                        elif l_ophis.op_art == 3 or l_ophis.op_art == 4:
                            art_bestand.outgoing = art_bestand.outgoing + l_ophis.anzahl
                            art_bestand.out_val = art_bestand.out_val + l_ophis.anzahl * l_artikel.vk_preis
                            art_bestand.actqty = art_bestand.actqty - l_ophis.anzahl
                            art_bestand.actval = art_bestand.actval - l_ophis.anzahl * l_artikel.vk_preis

    for l_lager in db_session.query(L_lager).filter(
            (L_lager.lager_nr >= from_lager) &  (L_lager.lager_nr <= to_lager)).all():
        bezeich = ""
        stockoh_list = Stockoh_list()
        stockoh_list_list.append(stockoh_list)

        stockoh_list.bezeich = to_string(l_lager.lager_nr, "99") + " - " + to_string(l_lager.bezeich, "x(25)")
        tot_prev = 0
        tot_in = 0
        tot_out = 0
        tot_value = 0
        zwkum = 0
        t_val = 0

        for art_bestand in query(art_bestand_list, filters=(lambda art_bestand :art_bestand.lager == l_lager.lager_nr and art_bestand.artnr >= from_art and art_bestand.artnr <= to_art)):

            if (not move_art) or art_bestand.incoming != 0 or art_bestand.outgoing != 0:

                if zwkum == 0:
                    zwkum = art_bestand.zwkum

                    l_untergrup = db_session.query(L_untergrup).filter(
                            (L_untergrup.zwkum == zwkum)).first()
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


                    t_val = 0
                    zwkum = art_bestand.zwkum

                    l_untergrup = db_session.query(L_untergrup).filter(
                            (L_untergrup.zwkum == zwkum)).first()
                    bezeich = l_untergrup.bezeich

                l_artikel = db_session.query(L_artikel).filter(
                        (L_artikel.artnr == art_bestand.artnr)).first()

                if art_bestand.avrg_pr == 0:

                    if art_bestand.actqty != 0:
                        art_bestand.avrg_pr = art_bestand.actval / art_bestand.actqty
                else:
                    art_bestand.avrg_pr = l_artikel.vk_preis
                    art_bestand.actval = 0


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


                t_val = t_val + art_bestand.actval
                tot_in = tot_in + art_bestand.in_val
                tot_out = tot_out + art_bestand.out_val
                tot_prev = tot_prev + art_bestand.prevval
                tot_value = tot_value + art_bestand.actval
                total_in = total_in + art_bestand.in_val
                total_out = total_out + art_bestand.out_val
                total_prev = total_prev + art_bestand.prevval
                total_value = total_value + art_bestand.actval

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
        stockoh_list.bezeich = "G R A N D  T O T A L"
        stockoh_list.actval = to_string(total_value, "->,>>>,>>>,>>9.99")


    else:
        stockoh_list.bezeich = "G R A N D  T O T A L"
        stockoh_list.actval = to_string(total_value, "->>,>>>,>>>,>>9")

    printcod = db_session.query(Printcod).filter(
            (func.lower(Printcod.emu) == "Epson") &  (func.lower(Printcod.code) == "rs")).first()

    if printcod:
        art_bestand_list.clear()

    return generate_output()