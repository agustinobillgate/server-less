#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, H_bill, H_artikel, H_journal, Artikel, Res_line, Guest, Segment

def rest_statsegment_go_webbl(pvilanguage:int, from_date:date, to_date:date, sorttype:int):

    prepare_cache ([Htparam, H_bill, H_artikel, H_journal, Res_line, Segment])

    output_list_list = []
    price_decimal:int = 0
    black_list:int = 0
    start_month:date = None
    start_year:date = None
    long_digit:bool = False
    f_endkum:int = 0
    m_endkum:int = 0
    b_endkum:int = 0
    lvcarea:string = "rest-statsegment"
    htparam = h_bill = h_artikel = h_journal = artikel = res_line = guest = segment = None

    output_list = t_list = segm_list = None

    output_list_list, Output_list = create_model("Output_list", {"flag":string, "segm_no":string, "g_segm":string, "pax":string, "proz_pax":string, "t_rev":string, "proz_trev":string, "m_pax":string, "proz_mpax":string, "m_rev":string, "proz_mrev":string, "y_pax":string, "proz_ypax":string, "y_rev":string, "proz_yrev":string})
    t_list_list, T_list = create_model("T_list", {"flag":string, "segm_no":int, "g_segm":string, "dept":int, "pax":int, "proz_pax":Decimal, "t_rev":Decimal, "proz_trev":Decimal, "m_pax":int, "proz_mpax":Decimal, "m_rev":Decimal, "proz_mrev":Decimal, "y_pax":int, "proz_ypax":Decimal, "y_rev":Decimal, "proz_yrev":Decimal})
    segm_list_list, Segm_list = create_model("Segm_list", {"segmnr":int, "bezeich":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_list, price_decimal, black_list, start_month, start_year, long_digit, f_endkum, m_endkum, b_endkum, lvcarea, htparam, h_bill, h_artikel, h_journal, artikel, res_line, guest, segment
        nonlocal pvilanguage, from_date, to_date, sorttype


        nonlocal output_list, t_list, segm_list
        nonlocal output_list_list, t_list_list, segm_list_list

        return {"output-list": output_list_list}

    def create_list():

        nonlocal output_list_list, price_decimal, black_list, start_month, start_year, long_digit, f_endkum, m_endkum, b_endkum, lvcarea, htparam, h_bill, h_artikel, h_journal, artikel, res_line, guest, segment
        nonlocal pvilanguage, from_date, to_date, sorttype


        nonlocal output_list, t_list, segm_list
        nonlocal output_list_list, t_list_list, segm_list_list

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
        tot_pax = 0
        tot_rev =  to_decimal("0")
        tot_mpax = 0
        tot_mrev =  to_decimal("0")
        tot_ypax = 0
        tot_yrev =  to_decimal("0")
        t_list_list.clear()
        output_list_list.clear()
        curr_zeit = get_current_time_in_seconds()

        h_journal_obj_list = {}
        h_journal = H_journal()
        h_bill = H_bill()
        h_artikel = H_artikel()
        for h_journal.betrag, h_journal.bill_datum, h_journal._recid, h_bill.resnr, h_bill.reslinnr, h_bill.segmentcode, h_bill.rechnr, h_bill.departement, h_bill.belegung, h_bill._recid, h_artikel.artnrfront, h_artikel.departement, h_artikel._recid in db_session.query(H_journal.betrag, H_journal.bill_datum, H_journal._recid, H_bill.resnr, H_bill.reslinnr, H_bill.segmentcode, H_bill.rechnr, H_bill.departement, H_bill.belegung, H_bill._recid, H_artikel.artnrfront, H_artikel.departement, H_artikel._recid).join(H_bill,(H_bill.rechnr == H_journal.rechnr) & (H_bill.departement == H_journal.departement) & (H_bill.bilname != "")).join(H_artikel,(H_artikel.artnr == H_journal.artnr) & (H_artikel.departement == H_journal.departement) & (H_artikel.artart == 0)).filter(
                 (H_journal.bill_datum >= start_year) & (H_journal.bill_datum <= to_date)).order_by(H_journal._recid).all():
            if h_journal_obj_list.get(h_journal._recid):
                continue
            else:
                h_journal_obj_list[h_journal._recid] = True


            guest_no = 0

            if sorttype == 1:

                artikel = db_session.query(Artikel).filter(
                             (Artikel.artnr == h_artikel.artnrfront) & (Artikel.departement == h_artikel.departement) & ((Artikel.umsatzart == 3) | (Artikel.umsatzart == 5))).first()

            elif sorttype == 2:

                artikel = get_cache (Artikel, {"artnr": [(eq, h_artikel.artnrfront)],"departement": [(eq, h_artikel.departement)],"umsatzart": [(eq, 6)]})

            elif sorttype == 3:

                artikel = get_cache (Artikel, {"artnr": [(eq, h_artikel.artnrfront)],"departement": [(eq, h_artikel.departement)],"umsatzart": [(eq, 4)]})

            elif sorttype == 4:

                artikel = get_cache (Artikel, {"artnr": [(eq, h_artikel.artnrfront)],"departement": [(eq, h_artikel.departement)],"umsatzart": [(ge, 3),(le, 6)]})

            if artikel:

                if h_bill.resnr > 0 and h_bill.reslinnr > 0:

                    res_line = get_cache (Res_line, {"resnr": [(eq, h_bill.resnr)],"reslinnr": [(eq, h_bill.reslinnr)]})

                    if res_line:
                        guest_no = res_line.gastnrmember

                elif h_bill.resnr > 0:
                    guest_no = h_bill.resnr

                if guest_no != 0 and h_bill.segmentcode != 0:

                    guest = get_cache (Guest, {"gastnr": [(eq, guest_no)]})

                    if guest:

                        t_list = query(t_list_list, filters=(lambda t_list: t_list.segm_no == h_bill.segmentcode), first=True)

                        if not t_list:
                            t_list = T_list()
                            t_list_list.append(t_list)

                            t_list.segm_no = h_bill.segmentcode

                            segment = get_cache (Segment, {"segmentcode": [(eq, h_bill.segmentcode)]})

                            if segment:
                                t_list.g_segm = entry(0, segment.bezeich, "$$0")

                        if h_journal.bill_datum == to_date:

                            if curr_billno != (to_string(h_bill.rechnr) + "-" + to_string(h_bill.departement)):
                                t_list.pax = t_list.pax + h_bill.belegung
                                tot_pax = tot_pax + h_bill.belegung


                            t_list.t_rev =  to_decimal(t_list.t_rev) + to_decimal(h_journal.betrag)
                            tot_rev =  to_decimal(tot_rev) + to_decimal(h_journal.betrag)

                        if get_month(h_journal.bill_datum) == get_month(to_date):

                            if curr_billno != (to_string(h_bill.rechnr) + "-" + to_string(h_bill.departement)):
                                t_list.m_pax = t_list.m_pax + h_bill.belegung
                                tot_mpax = tot_mpax + h_bill.belegung


                            t_list.m_rev =  to_decimal(t_list.m_rev) + to_decimal(h_journal.betrag)
                            tot_mrev =  to_decimal(tot_mrev) + to_decimal(h_journal.betrag)

                        if curr_billno != (to_string(h_bill.rechnr) + "-" + to_string(h_bill.departement)):
                            t_list.y_pax = t_list.y_pax + h_bill.belegung
                            tot_ypax = tot_ypax + h_bill.belegung


                        t_list.y_rev =  to_decimal(t_list.y_rev) + to_decimal(h_journal.betrag)
                        tot_yrev =  to_decimal(tot_yrev) + to_decimal(h_journal.betrag)
                        curr_billno = to_string(h_bill.rechnr) + "-" + to_string(h_bill.departement)
                else:

                    t_list = query(t_list_list, filters=(lambda t_list: t_list.segm_no == 9999), first=True)

                    if not t_list:
                        t_list = T_list()
                        t_list_list.append(t_list)

                        t_list.segm_no = 9999
                        t_list.g_segm = "UNKNOWN"

                    if h_journal.bill_datum == to_date:

                        if curr_billno != (to_string(h_bill.rechnr) + "-" + to_string(h_bill.departement)):
                            t_list.pax = t_list.pax + h_bill.belegung
                            tot_pax = tot_pax + h_bill.belegung


                        t_list.t_rev =  to_decimal(t_list.t_rev) + to_decimal(h_journal.betrag)
                        tot_rev =  to_decimal(tot_rev) + to_decimal(h_journal.betrag)

                    if get_month(h_journal.bill_datum) == get_month(to_date):

                        if curr_billno != (to_string(h_bill.rechnr) + "-" + to_string(h_bill.departement)):
                            t_list.m_pax = t_list.m_pax + h_bill.belegung
                            tot_mpax = tot_mpax + h_bill.belegung


                        t_list.m_rev =  to_decimal(t_list.m_rev) + to_decimal(h_journal.betrag)
                        tot_mrev =  to_decimal(tot_mrev) + to_decimal(h_journal.betrag)

                    if curr_billno != (to_string(h_bill.rechnr) + "-" + to_string(h_bill.departement)):
                        t_list.y_pax = t_list.y_pax + h_bill.belegung
                        tot_ypax = tot_ypax + h_bill.belegung


                    t_list.y_rev =  to_decimal(t_list.y_rev) + to_decimal(h_journal.betrag)
                    tot_yrev =  to_decimal(tot_yrev) + to_decimal(h_journal.betrag)
                    curr_billno = to_string(h_bill.rechnr) + "-" + to_string(h_bill.departement)

        for t_list in query(t_list_list, sort_by=[("segm_no",False)]):

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
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.segm_no = to_string(t_list.segm_no, ">>>>>>>")


            output_list.g_segm = t_list.g_segm

            if long_digit:
                output_list.pax = to_string(t_list.pax, ">>>>>>9")
                output_list.t_rev = to_string(t_list.t_rev, "->>>,>>>,>>>,>>>,>>9")
                output_list.m_pax = to_string(t_list.m_pax, ">>>>>>9")
                output_list.m_rev = to_string(t_list.m_rev, "->>>,>>>,>>>,>>>,>>9")
                output_list.y_pax = to_string(t_list.y_pax, ">>>>>>9")
                output_list.y_rev = to_string(t_list.y_rev, "->>>,>>>,>>>,>>>,>>9")
                output_list.proz_pax = to_string(t_list.proz_pax, ">>9.99")
                output_list.proz_trev = to_string(t_list.proz_trev, ">>9.99")
                output_list.proz_mpax = to_string(t_list.proz_mpax, ">>9.99")
                output_list.proz_mrev = to_string(t_list.proz_mrev, ">>9.99")
                output_list.proz_ypax = to_string(t_list.proz_ypax, ">>9.99")
                output_list.proz_yrev = to_string(t_list.proz_yrev, ">>9.99")


            else:
                output_list.pax = to_string(t_list.pax, " >>>>9")
                output_list.t_rev = to_string(t_list.t_rev, ">,>>>,>>>,>>>,>>9.99")
                output_list.m_pax = to_string(t_list.m_pax, " >>>>>9")
                output_list.m_rev = to_string(t_list.m_rev, ">,>>>,>>>,>>>,>>9.99")
                output_list.y_pax = to_string(t_list.y_pax, " >>>>>9")
                output_list.y_rev = to_string(t_list.y_rev, ">,>>>,>>>,>>>,>>9.99")
                output_list.proz_pax = to_string(t_list.proz_pax, ">>9.99")
                output_list.proz_trev = to_string(t_list.proz_trev, ">>9.99")
                output_list.proz_mpax = to_string(t_list.proz_mpax, ">>9.99")
                output_list.proz_mrev = to_string(t_list.proz_mrev, ">>9.99")
                output_list.proz_ypax = to_string(t_list.proz_ypax, ">>9.99")
                output_list.proz_yrev = to_string(t_list.proz_yrev, ">>9.99")

        output_list = query(output_list_list, first=True)

        if output_list:
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.g_segm = translateExtended ("Total Revenue", lvcarea, "")
            output_list.pax = to_string(tot_pax, ">>>>>>9")
            output_list.t_rev = to_string(tot_rev, ">,>>>,>>>,>>>,>>9.99")
            output_list.m_pax = to_string(tot_mpax, ">>>>>>9")
            output_list.m_rev = to_string(tot_mrev, ">,>>>,>>>,>>>,>>9.99")
            output_list.y_pax = to_string(tot_ypax, ">>>>>>9")
            output_list.y_rev = to_string(tot_yrev, ">,>>>,>>>,>>>,>>9.99")
            output_list.proz_pax = to_string(100, ">>9.99")
            output_list.proz_trev = to_string(100, ">>9.99")
            output_list.proz_mpax = to_string(100, ">>9.99")
            output_list.proz_mrev = to_string(100, ">>9.99")
            output_list.proz_ypax = to_string(100, ">>9.99")
            output_list.proz_yrev = to_string(100, ">>9.99")

    start_month = date_mdy(get_month(to_date) , 1, get_year(to_date))
    start_year = date_mdy(1, 1, get_year(to_date))

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
    create_list()

    return generate_output()