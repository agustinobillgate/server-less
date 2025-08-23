#using conversion tools version: 1.0.0.117

#------------------------------------------------
# Rulita, 22/08/2025
# Recompile 
# ticket: 5BE11A
#------------------------------------------------

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.calc_servtaxesbl import calc_servtaxesbl
from models import Htparam, H_journal, H_bill, H_artikel, Artikel, Res_line, Guestseg, Guest

input_list_data, Input_list = create_model("Input_list", {"sorttype":int, "segmcode":int, "start_jan":date, "from_date":date, "to_date":date, "excl_tax":bool})

def rest_stat2_webbl(input_list_data:[Input_list]):

    prepare_cache ([Htparam, H_journal, H_bill, H_artikel, Artikel, Res_line, Guestseg, Guest])

    detail_list_data = []
    price_decimal:int = 0
    black_list:int = 0
    long_digit:bool = False
    f_endkum:int = 0
    m_endkum:int = 0
    b_endkum:int = 0
    tot_pax:int = 0
    tot_rev:Decimal = to_decimal("0.0")
    tot_mpax:int = 0
    tot_mrev:Decimal = to_decimal("0.0")
    tot_ypax:int = 0
    tot_yrev:Decimal = to_decimal("0.0")
    detail_pax:int = 0
    detail_rev:Decimal = to_decimal("0.0")
    curr_segm:int = 0
    gname:string = ""
    curr_billno:string = ""
    curr_dept:int = 0
    command_str:string = ""
    curr_zeit:int = 0
    guest_no:int = 0
    segm_no:int = 0
    vat:Decimal = to_decimal("0.0")
    vat2:Decimal = to_decimal("0.0")
    service:Decimal = to_decimal("0.0")
    fact:Decimal = to_decimal("0.0")
    htparam = h_journal = h_bill = h_artikel = artikel = res_line = guestseg = guest = None

    detail_list = t_list = input_list = None

    detail_list_data, Detail_list = create_model("Detail_list", {"flag":string, "segm_no":int, "guest_name":string, "descipt":string, "bill_no":string, "dept":int, "pax":string, "proz_pax":string, "t_rev":string, "proz_trev":string, "m_pax":string, "proz_mpax":string, "m_rev":string, "proz_mrev":string, "y_pax":string, "proz_ypax":string, "y_rev":string, "proz_yrev":string})
    t_list_data, T_list = create_model("T_list", {"flag":string, "segm_no":int, "guest_name":string, "bill_no":int, "dept":int, "pax":int, "proz_pax":Decimal, "t_rev":Decimal, "proz_trev":Decimal, "m_pax":int, "proz_mpax":Decimal, "m_rev":Decimal, "proz_mrev":Decimal, "y_pax":int, "proz_ypax":Decimal, "y_rev":Decimal, "proz_yrev":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal detail_list_data, price_decimal, black_list, long_digit, f_endkum, m_endkum, b_endkum, tot_pax, tot_rev, tot_mpax, tot_mrev, tot_ypax, tot_yrev, detail_pax, detail_rev, curr_segm, gname, curr_billno, curr_dept, command_str, curr_zeit, guest_no, segm_no, vat, vat2, service, fact, htparam, h_journal, h_bill, h_artikel, artikel, res_line, guestseg, guest


        nonlocal detail_list, t_list, input_list
        nonlocal detail_list_data, t_list_data

        return {"detail-list": detail_list_data}

    def calculate_betrag(inp_deci:Decimal):

        nonlocal detail_list_data, price_decimal, black_list, long_digit, f_endkum, m_endkum, b_endkum, tot_pax, tot_rev, tot_mpax, tot_mrev, tot_ypax, tot_yrev, detail_pax, detail_rev, curr_segm, gname, curr_billno, curr_dept, command_str, curr_zeit, guest_no, segm_no, vat, vat2, service, fact, htparam, h_journal, h_bill, h_artikel, artikel, res_line, guestseg, guest


        nonlocal detail_list, t_list, input_list
        nonlocal detail_list_data, t_list_data

        if input_list.excl_tax  and inp_deci != 0:
            service =  to_decimal("0")
            vat =  to_decimal("0")
            vat2 =  to_decimal("0")
            service, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, h_journal.bill_datum))
            inp_deci =  to_decimal(inp_deci) / to_decimal((1) + to_decimal(vat) + to_decimal(vat2) + to_decimal(service))
        return inp_deci


    def create_detail():

        nonlocal detail_list_data, price_decimal, black_list, long_digit, f_endkum, m_endkum, b_endkum, tot_pax, tot_rev, tot_mpax, tot_mrev, tot_ypax, tot_yrev, detail_pax, detail_rev, curr_segm, gname, curr_billno, curr_dept, command_str, curr_zeit, guest_no, segm_no, vat, vat2, service, fact, htparam, h_journal, h_bill, h_artikel, artikel, res_line, guestseg, guest


        nonlocal detail_list, t_list, input_list
        nonlocal detail_list_data, t_list_data


        tot_pax = 0
        tot_rev =  to_decimal("0")
        tot_mpax = 0
        tot_mrev =  to_decimal("0")
        tot_ypax = 0
        tot_yrev =  to_decimal("0")
        t_list_data.clear()
        detail_list_data.clear()
        curr_zeit = get_current_time_in_seconds()

        for h_journal in db_session.query(H_journal).filter(
                 (H_journal.bill_datum >= input_list.start_jan) & (H_journal.bill_datum <= input_list.to_date)).order_by(H_journal.rechnr).all():

            if input_list.segmcode != 9999:

                h_bill = get_cache (H_bill, {"rechnr": [(eq, h_journal.rechnr)],"departement": [(eq, h_journal.departement)]})

            if h_bill:

                h_artikel = get_cache (H_artikel, {"artnr": [(eq, h_journal.artnr)],"departement": [(eq, h_journal.departement)],"artart": [(eq, 0)]})

                if h_artikel:

                    if input_list.sorttype == 1:

                        artikel = db_session.query(Artikel).filter(
                                 (Artikel.artnr == h_artikel.artnrfront) & (Artikel.departement == h_artikel.departement) & ((Artikel.umsatzart == 3) | (Artikel.umsatzart == 5))).first()

                    elif input_list.sorttype == 2:

                        artikel = get_cache (Artikel, {"artnr": [(eq, h_artikel.artnrfront)],"departement": [(eq, h_artikel.departement)],"umsatzart": [(eq, 6)]})

                    elif input_list.sorttype == 3:

                        artikel = get_cache (Artikel, {"artnr": [(eq, h_artikel.artnrfront)],"departement": [(eq, h_artikel.departement)],"umsatzart": [(eq, 4)]})

                    elif input_list.sorttype == 4:

                        artikel = get_cache (Artikel, {"artnr": [(eq, h_artikel.artnrfront)],"departement": [(eq, h_artikel.departement)],"umsatzart": [(ge, 3),(le, 6)]})

                    if artikel:
                        segm_no = 0
                        guest_no = 0

                        if h_bill.resnr > 0 and h_bill.reslinnr > 0:

                            res_line = get_cache (Res_line, {"resnr": [(eq, h_bill.resnr)],"reslinnr": [(eq, h_bill.reslinnr)]})

                            if res_line:
                                guest_no = res_line.gastnrmember

                        elif h_bill.resnr > 0:
                            guest_no = h_bill.resnr

                        if h_bill.segmentcode == 0:

                            guestseg = get_cache (Guestseg, {"gastnr": [(eq, guest_no)],"reihenfolge": [(eq, 1)]})

                            if guestseg:
                                segm_no = guestseg.segmentcode
                        else:
                            segm_no = h_bill.segmentcode

                        if input_list.segmcode == segm_no:

                            t_list = query(t_list_data, filters=(lambda t_list: t_list.bill_no == h_bill.rechnr and t_list.dept == h_bill.departement), first=True)

                            if not t_list:
                                t_list = T_list()
                                t_list_data.append(t_list)

                                t_list.bill_no = h_bill.rechnr
                                t_list.dept = h_bill.departement
                                t_list.segm_no = input_list.segmcode

                                if guest_no != 0:

                                    guest = get_cache (Guest, {"gastnr": [(eq, guest_no)]})

                                    if guest:
                                        t_list.guest_name = guest.name + ", " + guest.vorname1 + " " + guest.anrede1


                                    else:
                                        t_list.guest_name = h_bill.bilname

                            if h_journal.bill_datum == input_list.to_date:

                                if curr_billno != (to_string(h_bill.rechnr) + "-" + to_string(h_bill.departement)):
                                    t_list.pax = h_bill.belegung
                                    tot_pax = tot_pax + h_bill.belegung


                                t_list.t_rev =  to_decimal(t_list.t_rev) + to_decimal(calculate_betrag (h_journal.betrag) )
                                tot_rev =  to_decimal(tot_rev) + to_decimal(calculate_betrag (h_journal.betrag) )

                            if h_journal.bill_datum >= input_list.from_date and h_journal.bill_datum <= input_list.to_date:

                                if curr_billno != (to_string(h_bill.rechnr) + "-" + to_string(h_bill.departement)):
                                    t_list.m_pax = h_bill.belegung
                                    tot_mpax = tot_mpax + h_bill.belegung


                                t_list.m_rev =  to_decimal(t_list.m_rev) + to_decimal(calculate_betrag (h_journal.betrag) )
                                tot_mrev =  to_decimal(tot_mrev) + to_decimal(calculate_betrag (h_journal.betrag) )

                            if curr_billno != (to_string(h_bill.rechnr) + "-" + to_string(h_bill.departement)):
                                t_list.y_pax = h_bill.belegung
                                tot_ypax = tot_ypax + h_bill.belegung


                            t_list.y_rev =  to_decimal(t_list.y_rev) + to_decimal(calculate_betrag (h_journal.betrag) )
                            tot_yrev =  to_decimal(tot_yrev) + to_decimal(calculate_betrag (h_journal.betrag) )


                            curr_billno = to_string(h_bill.rechnr) + "-" + to_string(h_bill.departement)

        for t_list in query(t_list_data, filters=(lambda t_list: t_list.pax == 0 and t_list.t_rev == 0 and t_list.m_pax == 0 and t_list.m_rev == 0 and t_list.y_pax == 0 and t_list.y_rev == 0)):
            t_list_data.remove(t_list)

        for t_list in query(t_list_data, sort_by=[("bill_no",False)]):

            if t_list.pax != 0:
                t_list.proz_pax =  to_decimal(t_list.pax) / to_decimal(tot_pax) * to_decimal("100")

            if t_list.t_rev != 0:
                t_list.proz_trev =  to_decimal(t_list.t_rev) / to_decimal(tot_rev) * to_decimal("100")

            if t_list.m_pax != 0:
                t_list.proz_mpax =  to_decimal(t_list.m_pax) / to_decimal(tot_mpax) * to_decimal("100")

            if t_list.m_rev != 0:
                t_list.proz_mrev =  to_decimal(t_list.m_rev) / to_decimal(tot_mrev) * to_decimal("100")

            if t_list.y_pax != 0:
                t_list.proz_ypax =  to_decimal(t_list.y_pax) / to_decimal(tot_ypax) * to_decimal("100")

            if t_list.y_rev != 0:
                t_list.proz_yrev =  to_decimal(t_list.y_rev) / to_decimal(tot_yrev) * to_decimal("100")
            detail_list = Detail_list()
            detail_list_data.append(detail_list)

            detail_list.descipt = to_string(t_list.bill_no) + " - " + to_string(t_list.dept, "99")
            detail_list.guest_name = t_list.guest_name
            detail_list.segm_no = t_list.segm_no

            if long_digit:
                detail_list.pax = to_string(t_list.pax, "->>>>>>9")
                detail_list.t_rev = to_string(t_list.t_rev, "->>>,>>>,>>>,>>>,>>9")
                detail_list.m_pax = to_string(t_list.m_pax, "->>>>>>9")
                detail_list.m_rev = to_string(t_list.m_rev, "->>>,>>>,>>>,>>>,>>9")
                detail_list.y_pax = to_string(t_list.y_pax, "->>>>>>9")
                detail_list.y_rev = to_string(t_list.y_rev, "->>>,>>>,>>>,>>>,>>9")
                detail_list.proz_pax = to_string(t_list.proz_pax, "->>9.99")
                detail_list.proz_trev = to_string(t_list.proz_trev, "->>9.99")
                detail_list.proz_mpax = to_string(t_list.proz_mpax, "->>9.99")
                detail_list.proz_mrev = to_string(t_list.proz_mrev, "->>9.99")
                detail_list.proz_ypax = to_string(t_list.proz_ypax, "->>9.99")
                detail_list.proz_yrev = to_string(t_list.proz_yrev, "->>9.99")


            else:
                detail_list.pax = to_string(t_list.pax, " ->>>>9")
                detail_list.t_rev = to_string(t_list.t_rev, "->,>>>,>>>,>>>,>>9.99")
                detail_list.m_pax = to_string(t_list.m_pax, " ->>>>>9")
                detail_list.m_rev = to_string(t_list.m_rev, "->,>>>,>>>,>>>,>>9.99")
                detail_list.y_pax = to_string(t_list.y_pax, " ->>>>>9")
                detail_list.y_rev = to_string(t_list.y_rev, "->,>>>,>>>,>>>,>>9.99")
                detail_list.proz_pax = to_string(t_list.proz_pax, "->>9.99")
                detail_list.proz_trev = to_string(t_list.proz_trev, "->>9.99")
                detail_list.proz_mpax = to_string(t_list.proz_mpax, "->>9.99")
                detail_list.proz_mrev = to_string(t_list.proz_mrev, "->>9.99")
                detail_list.proz_ypax = to_string(t_list.proz_ypax, "->>9.99")
                detail_list.proz_yrev = to_string(t_list.proz_yrev, "->>9.99")

        detail_list = query(detail_list_data, first=True)

        if detail_list:
            detail_list = Detail_list()
            detail_list_data.append(detail_list)

            detail_list.flag = "*"
            detail_list.descipt = "T O T A L"
            detail_list.pax = to_string(tot_pax, "->>>>>>9")
            detail_list.t_rev = to_string(tot_rev, "->,>>>,>>>,>>>,>>9.99")
            detail_list.m_pax = to_string(tot_mpax, "->>>>>>9")
            detail_list.m_rev = to_string(tot_mrev, "->,>>>,>>>,>>>,>>9.99")
            detail_list.y_pax = to_string(tot_ypax, "->>>>>>9")
            detail_list.y_rev = to_string(tot_yrev, "->,>>>,>>>,>>>,>>9.99")
            detail_list.proz_pax = to_string(100, ">>9.99")
            detail_list.proz_trev = to_string(100, ">>9.99")
            detail_list.proz_mpax = to_string(100, ">>9.99")
            detail_list.proz_mrev = to_string(100, ">>9.99")
            detail_list.proz_ypax = to_string(100, ">>9.99")
            detail_list.proz_yrev = to_string(100, ">>9.99")


    def create_detail_unknown():

        nonlocal detail_list_data, price_decimal, black_list, long_digit, f_endkum, m_endkum, b_endkum, tot_pax, tot_rev, tot_mpax, tot_mrev, tot_ypax, tot_yrev, detail_pax, detail_rev, curr_segm, gname, curr_billno, curr_dept, command_str, curr_zeit, guest_no, segm_no, vat, vat2, service, fact, htparam, h_journal, h_bill, h_artikel, artikel, res_line, guestseg, guest


        nonlocal detail_list, t_list, input_list
        nonlocal detail_list_data, t_list_data


        tot_pax = 0
        tot_rev =  to_decimal("0")
        tot_mpax = 0
        tot_mrev =  to_decimal("0")
        tot_ypax = 0
        tot_yrev =  to_decimal("0")
        t_list_data.clear()
        detail_list_data.clear()
        curr_zeit = get_current_time_in_seconds()

        for h_journal in db_session.query(H_journal).filter(
                 (H_journal.bill_datum >= input_list.start_jan) & (H_journal.bill_datum <= input_list.to_date)).order_by(H_journal.departement, H_journal.rechnr).all():

            h_bill = get_cache (H_bill, {"rechnr": [(eq, h_journal.rechnr)],"departement": [(eq, h_journal.departement)],"segmentcode": [(eq, 0)]})

            if h_bill:

                h_artikel = get_cache (H_artikel, {"artnr": [(eq, h_journal.artnr)],"departement": [(eq, h_journal.departement)],"artart": [(eq, 0)]})

                if h_artikel:

                    if input_list.sorttype == 1:

                        artikel = db_session.query(Artikel).filter(
                                 (Artikel.artnr == h_artikel.artnrfront) & (Artikel.departement == h_artikel.departement) & ((Artikel.umsatzart == 3) | (Artikel.umsatzart == 5))).first()

                    elif input_list.sorttype == 2:

                        artikel = get_cache (Artikel, {"artnr": [(eq, h_artikel.artnrfront)],"departement": [(eq, h_artikel.departement)],"umsatzart": [(eq, 6)]})

                    elif input_list.sorttype == 3:

                        artikel = get_cache (Artikel, {"artnr": [(eq, h_artikel.artnrfront)],"departement": [(eq, h_artikel.departement)],"umsatzart": [(eq, 4)]})

                    elif input_list.sorttype == 4:

                        artikel = get_cache (Artikel, {"artnr": [(eq, h_artikel.artnrfront)],"departement": [(eq, h_artikel.departement)],"umsatzart": [(ge, 3),(le, 6)]})

                    if artikel:
                        segm_no = 0
                        guest_no = 0

                        if h_bill.resnr > 0 and h_bill.reslinnr > 0:

                            res_line = get_cache (Res_line, {"resnr": [(eq, h_bill.resnr)],"reslinnr": [(eq, h_bill.reslinnr)]})

                            if res_line:
                                guest_no = res_line.gastnrmember

                        elif h_bill.resnr > 0:
                            guest_no = h_bill.resnr

                        if h_bill.segmentcode == 0:

                            guestseg = get_cache (Guestseg, {"gastnr": [(eq, guest_no)],"reihenfolge": [(eq, 1)]})

                            if guestseg:
                                segm_no = guestseg.segmentcode
                        else:
                            segm_no = h_bill.segmentcode

                        if segm_no == 0:

                            t_list = query(t_list_data, filters=(lambda t_list: t_list.bill_no == h_bill.rechnr and t_list.dept == h_bill.departement), first=True)

                            if not t_list:
                                t_list = T_list()
                                t_list_data.append(t_list)

                                t_list.bill_no = h_bill.rechnr
                                t_list.dept = h_bill.departement
                                t_list.guest_name = h_bill.bilname
                                t_list.segm_no = 9999

                            if h_journal.bill_datum == input_list.to_date:

                                if curr_billno != (to_string(h_bill.rechnr) + "-" + to_string(h_bill.departement)):
                                    t_list.pax = h_bill.belegung
                                    tot_pax = tot_pax + h_bill.belegung
                                t_list.t_rev =  to_decimal(t_list.t_rev) + to_decimal(calculate_betrag (h_journal.betrag) )
                                tot_rev =  to_decimal(tot_rev) + to_decimal(calculate_betrag (h_journal.betrag) )

                            if h_journal.bill_datum >= input_list.from_date and h_journal.bill_datum <= input_list.to_date:

                                if curr_billno != (to_string(h_bill.rechnr) + "-" + to_string(h_bill.departement)):
                                    t_list.m_pax = h_bill.belegung
                                    tot_mpax = tot_mpax + h_bill.belegung
                                t_list.m_rev =  to_decimal(t_list.m_rev) + to_decimal(calculate_betrag (h_journal.betrag) )
                                tot_mrev =  to_decimal(tot_mrev) + to_decimal(calculate_betrag (h_journal.betrag) )

                            if curr_billno != (to_string(h_bill.rechnr) + "-" + to_string(h_bill.departement)):
                                t_list.y_pax = h_bill.belegung
                                tot_ypax = tot_ypax + h_bill.belegung


                            t_list.y_rev =  to_decimal(t_list.y_rev) + to_decimal(calculate_betrag (h_journal.betrag) )
                            tot_yrev =  to_decimal(tot_yrev) + to_decimal(calculate_betrag (h_journal.betrag) )


                            curr_billno = to_string(h_bill.rechnr) + "-" + to_string(h_bill.departement)

        for t_list in query(t_list_data, filters=(lambda t_list: t_list.pax == 0 and t_list.t_rev == 0 and t_list.m_pax == 0 and t_list.m_rev == 0 and t_list.y_pax == 0 and t_list.y_rev == 0)):
            t_list_data.remove(t_list)

        for t_list in query(t_list_data, sort_by=[("bill_no",False)]):

            if t_list.pax != 0:
                t_list.proz_pax =  to_decimal(t_list.pax) / to_decimal(tot_pax) * to_decimal("100")

            if t_list.t_rev != 0:
                t_list.proz_trev =  to_decimal(t_list.t_rev) / to_decimal(tot_rev) * to_decimal("100")

            if t_list.m_pax != 0:
                t_list.proz_mpax =  to_decimal(t_list.m_pax) / to_decimal(tot_mpax) * to_decimal("100")

            if t_list.m_rev != 0:
                t_list.proz_mrev =  to_decimal(t_list.m_rev) / to_decimal(tot_mrev) * to_decimal("100")

            if t_list.y_pax != 0:
                t_list.proz_ypax =  to_decimal(t_list.y_pax) / to_decimal(tot_ypax) * to_decimal("100")

            if t_list.y_rev != 0:
                t_list.proz_yrev =  to_decimal(t_list.y_rev) / to_decimal(tot_yrev) * to_decimal("100")
            detail_list = Detail_list()
            detail_list_data.append(detail_list)

            detail_list.descipt = to_string(t_list.bill_no) + " - " + to_string(t_list.dept, "99")
            detail_list.guest_name = t_list.guest_name
            detail_list.segm_no = t_list.segm_no

            if long_digit:
                detail_list.pax = to_string(t_list.pax, "->>>>>>9")
                detail_list.t_rev = to_string(t_list.t_rev, "->>>,>>>,>>>,>>>,>>9")
                detail_list.m_pax = to_string(t_list.m_pax, "->>>>>>9")
                detail_list.m_rev = to_string(t_list.m_rev, "->>>,>>>,>>>,>>>,>>9")
                detail_list.y_pax = to_string(t_list.y_pax, "->>>>>>9")
                detail_list.y_rev = to_string(t_list.y_rev, "->>>,>>>,>>>,>>>,>>9")
                detail_list.proz_pax = to_string(t_list.proz_pax, "->>9.99")
                detail_list.proz_trev = to_string(t_list.proz_trev, "->>9.99")
                detail_list.proz_mpax = to_string(t_list.proz_mpax, "->>9.99")
                detail_list.proz_mrev = to_string(t_list.proz_mrev, "->>9.99")
                detail_list.proz_ypax = to_string(t_list.proz_ypax, "->>9.99")
                detail_list.proz_yrev = to_string(t_list.proz_yrev, "->>9.99")


            else:
                detail_list.pax = to_string(t_list.pax, " ->>>>9")
                detail_list.t_rev = to_string(t_list.t_rev, "->,>>>,>>>,>>>,>>9.99")
                detail_list.m_pax = to_string(t_list.m_pax, " ->>>>>9")
                detail_list.m_rev = to_string(t_list.m_rev, "->,>>>,>>>,>>>,>>9.99")
                detail_list.y_pax = to_string(t_list.y_pax, " ->>>>>9")
                detail_list.y_rev = to_string(t_list.y_rev, "->,>>>,>>>,>>>,>>9.99")
                detail_list.proz_pax = to_string(t_list.proz_pax, "->>9.99")
                detail_list.proz_trev = to_string(t_list.proz_trev, "->>9.99")
                detail_list.proz_mpax = to_string(t_list.proz_mpax, "->>9.99")
                detail_list.proz_mrev = to_string(t_list.proz_mrev, "->>9.99")
                detail_list.proz_ypax = to_string(t_list.proz_ypax, "->>9.99")
                detail_list.proz_yrev = to_string(t_list.proz_yrev, "->>9.99")

        detail_list = query(detail_list_data, first=True)

        if detail_list:
            detail_list = Detail_list()
            detail_list_data.append(detail_list)

            detail_list.flag = "*"
            detail_list.descipt = "T O T A L"
            detail_list.pax = to_string(tot_pax, "->>>>>>9")
            detail_list.t_rev = to_string(tot_rev, "->,>>>,>>>,>>>,>>9.99")
            detail_list.m_pax = to_string(tot_mpax, "->>>>>>9")
            detail_list.m_rev = to_string(tot_mrev, "->,>>>,>>>,>>>,>>9.99")
            detail_list.y_pax = to_string(tot_ypax, "->>>>>>9")
            detail_list.y_rev = to_string(tot_yrev, "->,>>>,>>>,>>>,>>9.99")
            detail_list.proz_pax = to_string(100, ">>9.99")
            detail_list.proz_trev = to_string(100, ">>9.99")
            detail_list.proz_mpax = to_string(100, ">>9.99")
            detail_list.proz_mrev = to_string(100, ">>9.99")
            detail_list.proz_ypax = to_string(100, ">>9.99")
            detail_list.proz_yrev = to_string(100, ">>9.99")


    input_list = query(input_list_data, first=True)

    if not input_list:

        return generate_output()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
    price_decimal = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 709)]})
    black_list = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 246)]})
    long_digit = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 862)]})
    f_endkum = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 273)]})
    m_endkum = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 892)]})
    b_endkum = htparam.finteger

    if input_list.segmcode != 9999:
        create_detail()
    else:
        create_detail_unknown()

    return generate_output()