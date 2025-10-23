#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import H_bill_line, H_artikel, Umsatz, Htparam, Hoteldpt, Queasy, H_bill, Artikel

def nt_kngfbrev():

    prepare_cache ([H_bill_line, H_artikel, Umsatz, Htparam, Queasy, H_bill, Artikel])

    disc_art1:int = 0
    disc_art2:int = 0
    disc_art3:int = 0
    ci_date:date = None
    tot_amt:Decimal = to_decimal("0.0")
    shift:int = 0
    shift_art:int = 0
    sum_compliment:Decimal = to_decimal("0.0")
    do_it:bool = False
    f_pax:int = 0
    b_pax:int = 0
    dept_minibar:int = 0
    dept_laundry:int = 0
    str_par:string = ""
    sep1:string = ","
    sep2:string = ";"
    i:int = 0
    j:int = 0
    k:int = 0
    c1:string = ""
    c2:string = ""
    d:int = 0
    art:List[int] = create_empty_list(4,0)
    h_bill_line = h_artikel = umsatz = htparam = hoteldpt = queasy = h_bill = artikel = None

    s_list = map_list = hb_buff = hb_buff1 = hart_buff = sbuff = ubuff = h_art1 = None

    s_list_data, S_list = create_model("S_list", {"shift":int, "ftime":int, "ttime":int})
    map_list_data, Map_list = create_model("Map_list", {"deptnr":int, "food":[int,4], "bev":[int,4]})

    Hb_buff = create_buffer("Hb_buff",H_bill_line)
    Hb_buff1 = create_buffer("Hb_buff1",H_bill_line)
    Hart_buff = create_buffer("Hart_buff",H_artikel)
    Sbuff = S_list
    sbuff_data = s_list_data

    Ubuff = create_buffer("Ubuff",Umsatz)
    H_art1 = create_buffer("H_art1",H_artikel)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal disc_art1, disc_art2, disc_art3, ci_date, tot_amt, shift, shift_art, sum_compliment, do_it, f_pax, b_pax, dept_minibar, dept_laundry, str_par, sep1, sep2, i, j, k, c1, c2, d, art, h_bill_line, h_artikel, umsatz, htparam, hoteldpt, queasy, h_bill, artikel
        nonlocal hb_buff, hb_buff1, hart_buff, sbuff, ubuff, h_art1


        nonlocal s_list, map_list, hb_buff, hb_buff1, hart_buff, sbuff, ubuff, h_art1
        nonlocal s_list_data, map_list_data

        return {}

    def get_anzahl():

        nonlocal disc_art1, disc_art2, disc_art3, ci_date, tot_amt, shift, shift_art, sum_compliment, do_it, f_pax, b_pax, dept_minibar, dept_laundry, str_par, sep1, sep2, i, j, k, c1, c2, d, art, h_bill_line, h_artikel, umsatz, htparam, hoteldpt, queasy, h_bill, artikel
        nonlocal hb_buff, hb_buff1, hart_buff, sbuff, ubuff, h_art1


        nonlocal s_list, map_list, hb_buff, hb_buff1, hart_buff, sbuff, ubuff, h_art1
        nonlocal s_list_data, map_list_data

        hb_buff_obj_list = {}
        hb_buff = H_bill_line()
        h_art1 = H_artikel()
        artikel = Artikel()
        for hb_buff.anzahl, hb_buff.betrag, hb_buff.betriebsnr, hb_buff.zeit, hb_buff.bill_datum, hb_buff._recid, h_art1.artnrfront, h_art1.departement, h_art1._recid, artikel.umsatzart, artikel._recid in db_session.query(Hb_buff.anzahl, Hb_buff.betrag, Hb_buff.betriebsnr, Hb_buff.zeit, Hb_buff.bill_datum, Hb_buff._recid, H_art1.artnrfront, H_art1.departement, H_art1._recid, Artikel.umsatzart, Artikel._recid).join(H_art1,(H_art1.artnr == Hb_buff.artnr) & (H_art1.departement == Hb_buff.departement) & (H_art1.artart == 0)).join(Artikel,(Artikel.artnr == H_art1.artnrfront) & (Artikel.departement == H_art1.departement)).filter(
                 (Hb_buff.rechnr == h_bill.rechnr) & (Hb_buff.departement == h_bill.departement) & (Hb_buff.artnr != disc_art1) & (Hb_buff.artnr != disc_art2) & (Hb_buff.artnr != disc_art3)).order_by(Hb_buff._recid).all():
            if hb_buff_obj_list.get(hb_buff._recid):
                continue
            else:
                hb_buff_obj_list[hb_buff._recid] = True

            if artikel.umsatzart == 3 or artikel.umsatzart == 5:
                f_pax = f_pax + hb_buff.anzahl

            elif artikel.umsatzart == 6:
                b_pax = b_pax + hb_buff.anzahl

    htparam = get_cache (Htparam, {"paramnr": [(eq, 557)]})
    disc_art1 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 596)]})
    disc_art2 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 556)]})
    disc_art3 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 849)]})
    dept_minibar = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1081)]})
    dept_laundry = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    ci_date = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 369)]})

    if htparam.feldtyp != 5 or htparam.fchar == "":

        return generate_output()
    str_par = htparam.fchar
    for i in range(1,num_entries(str_par, sep2) - 1 + 1) :
        c1 = entry(i - 1, str_par, sep2)
        map_list = Map_list()
        map_list_data.append(map_list)

        map_list.deptnr = to_int(substring(entry(0, c1, sep1) , 1, length(entry(0, c1, sep1)) - 1))


        for j in range(1,4 + 1) :
            map_list.food[j - 1] = to_int(entry(j + 1 - 1, c1 , sep1))
        k = 0
        for j in range(6,9 + 1) :
            k = k + 1
            map_list.bev[k - 1] = to_int(entry(j - 1, c1, sep1))

    for map_list in query(map_list_data):

        hoteldpt = get_cache (Hoteldpt, {"num": [(eq, map_list.deptnr)]})

        if not hoteldpt:

            return generate_output()

        umsatz = db_session.query(Umsatz).filter(
                 (Umsatz.departement == map_list.deptnr) & (Umsatz.datum == ci_date) & ((Umsatz.artnr == map_list.food[0]) | (Umsatz.artnr == map_list.food[1]) | (Umsatz.artnr == map_list.food[2]) | (Umsatz.artnr == map_list.food[3]) | (Umsatz.artnr == map_list.bev[0]) | (Umsatz.artnr == map_list.bev[1]) | (Umsatz.artnr == map_list.bev[2]) | (Umsatz.artnr == map_list.bev[3]))).first()

        if umsatz:

            return generate_output()

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 5) & (Queasy.number3 >= 1) & (Queasy.number3 <= 4)).order_by(Queasy._recid).all():
        s_list = S_list()
        s_list_data.append(s_list)

        s_list.shift = queasy.number3
        s_list.ftime = to_int(substring(to_string(queasy.number1, "9999") , 0, 2)) * 3600 +\
                to_int(substring(to_string(queasy.number1, "9999") , 2, 2)) * 60
        s_list.ttime = to_int(substring(to_string(queasy.number2, "9999") , 0, 2)) * 3600 +\
                to_int(substring(to_string(queasy.number2, "9999") , 2, 2)) * 60

        if s_list.ftime > s_list.ttime:
            sbuff = Sbuff()
            sbuff_data.append(sbuff)

            sbuff.shift = s_list.shift
            sbuff.ftime = 0
            sbuff.ttime = s_list.ttime
            s_list.ttime = 24 * 3600

    h_bill_obj_list = {}
    h_bill = H_bill()
    h_bill_line = H_bill_line()
    for h_bill.rechnr, h_bill.departement, h_bill.belegung, h_bill._recid, h_bill_line.anzahl, h_bill_line.betrag, h_bill_line.betriebsnr, h_bill_line.zeit, h_bill_line.bill_datum, h_bill_line._recid in db_session.query(H_bill.rechnr, H_bill.departement, H_bill.belegung, H_bill._recid, H_bill_line.anzahl, H_bill_line.betrag, H_bill_line.betriebsnr, H_bill_line.zeit, H_bill_line.bill_datum, H_bill_line._recid).join(H_bill_line,(H_bill_line.rechnr == H_bill.rechnr) & (H_bill_line.bill_datum == ci_date) & (H_bill_line.departement == H_bill.departement)).filter(
             (H_bill.saldo == 0) & (H_bill.flag == 1) & (H_bill.departement != dept_minibar) & (H_bill.departement != dept_laundry)).order_by(H_bill._recid).all():
        if h_bill_obj_list.get(h_bill._recid):
            continue
        else:
            h_bill_obj_list[h_bill._recid] = True


        sum_compliment =  to_decimal("0")

        hb_buff_obj_list = {}
        hb_buff = H_bill_line()
        hart_buff = H_artikel()
        for hb_buff.anzahl, hb_buff.betrag, hb_buff.betriebsnr, hb_buff.zeit, hb_buff.bill_datum, hb_buff._recid, hart_buff.artnrfront, hart_buff.departement, hart_buff._recid in db_session.query(Hb_buff.anzahl, Hb_buff.betrag, Hb_buff.betriebsnr, Hb_buff.zeit, Hb_buff.bill_datum, Hb_buff._recid, Hart_buff.artnrfront, Hart_buff.departement, Hart_buff._recid).join(Hart_buff,(Hart_buff.artnr == Hb_buff.artnr) & (Hart_buff.departement == Hb_buff.departement) & ((Hart_buff.artart == 11) | (Hart_buff.artart == 12))).filter(
                 (Hb_buff.rechnr == h_bill.rechnr) & (Hb_buff.departement == h_bill.departement) & (Hb_buff.bill_datum == ci_date)).order_by(Hb_buff._recid).all():
            if hb_buff_obj_list.get(hb_buff._recid):
                continue
            else:
                hb_buff_obj_list[hb_buff._recid] = True


            sum_compliment =  to_decimal(sum_compliment) + to_decimal(hb_buff.betrag)
        do_it = (sum_compliment == 0)

        if do_it:
            f_pax = 0 
            b_pax == 0

            if h_bill.belegung != 0:
                get_anzahl()

            if h_bill.belegung > 0:

                if f_pax > h_bill.belegung:
                    f_pax = h_bill.belegung

                if b_pax > h_bill.belegung:
                    b_pax = h_bill.belegung

            elif h_bill.belegung < 0:

                if f_pax < h_bill.belegung:
                    f_pax = h_bill.belegung

                if b_pax < h_bill.belegung:
                    b_pax = h_bill.belegung
            tot_amt =  to_decimal("0")

            hb_buff_obj_list = {}
            hb_buff = H_bill_line()
            hart_buff = H_artikel()
            for hb_buff.anzahl, hb_buff.betrag, hb_buff.betriebsnr, hb_buff.zeit, hb_buff.bill_datum, hb_buff._recid, hart_buff.artnrfront, hart_buff.departement, hart_buff._recid in db_session.query(Hb_buff.anzahl, Hb_buff.betrag, Hb_buff.betriebsnr, Hb_buff.zeit, Hb_buff.bill_datum, Hb_buff._recid, Hart_buff.artnrfront, Hart_buff.departement, Hart_buff._recid).join(Hart_buff,(Hart_buff.artnr == Hb_buff.artnr) & (Hart_buff.departement == Hb_buff.departement) & (Hart_buff.artart == 0)).filter(
                     (Hb_buff.rechnr == h_bill.rechnr) & (Hb_buff.departement == h_bill.departement) & (Hb_buff.bill_datum == ci_date)).order_by(Hb_buff._recid).all():
                if hb_buff_obj_list.get(hb_buff._recid):
                    continue
                else:
                    hb_buff_obj_list[hb_buff._recid] = True


                shift = 0 
                shift_art = 0
                shift = hb_buff.betriebsnr

                if shift == 0:

                    s_list = query(s_list_data, filters=(lambda s_list: s_list.hb_buff.zeit >= s_list.ftime and hb_buff.zeit <= s_list.ttime), first=True)

                    if s_list and s_list.shift <= 4:
                        shift = s_list.shift
                    else:
                        shift = 3
                shift_art = 0

                map_list = query(map_list_data, filters=(lambda map_list: map_list.deptnr == h_bill.departement), first=True)

                if map_list:

                    if hart_buff.artnrfront == 10:
                        shift_art = map_list.food[shift - 1]
                    elif hart_buff.artnrfront == 11:
                        shift_art = map_list.bev[shift - 1]

                if shift_art != 0:

                    umsatz = get_cache (Umsatz, {"artnr": [(eq, hart_buff.artnrfront)],"departement": [(eq, hart_buff.departement)],"datum": [(eq, hb_buff.bill_datum)]})

                    if umsatz:
                        umsatz.anzahl = umsatz.anzahl - hb_buff.anzahl
                        umsatz.betrag =  to_decimal(umsatz.betrag) - to_decimal(hb_buff.betrag)


                        pass

                        ubuff = get_cache (Umsatz, {"artnr": [(eq, shift_art)],"departement": [(eq, hart_buff.departement)],"datum": [(eq, hb_buff.bill_datum)]})

                        if not ubuff:
                            ubuff = Umsatz()
                            db_session.add(ubuff)

                            ubuff.artnr = shift_art
                            ubuff.departement = hart_buff.departement
                            ubuff.datum = hb_buff.bill_datum


                        ubuff.betrag =  to_decimal(ubuff.betrag) + to_decimal(hb_buff.betrag)

                        if hart_buff.artnrfront == 10:
                            ubuff.anzahl = ubuff.anzahl + hb_buff.anzahl

                        elif hart_buff.artnrfront == 11:
                            ubuff.anzahl = ubuff.anzahl + hb_buff.anzahl
                        pass

    return generate_output()