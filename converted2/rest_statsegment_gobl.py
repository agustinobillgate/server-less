#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, H_journal, H_bill, H_artikel, Artikel, Guest, Guestseg, Segment

def rest_statsegment_gobl(pvilanguage:int, from_date:date, to_date:date, sorttype:int):

    prepare_cache ([Htparam, H_bill, H_artikel, Guest, Guestseg, Segment])

    output_list_data = []
    price_decimal:int = 0
    black_list:int = 0
    start_month:date = None
    start_year:date = None
    long_digit:bool = False
    f_endkum:int = 0
    m_endkum:int = 0
    b_endkum:int = 0
    lvcarea:string = "rest-statsegment"
    htparam = h_journal = h_bill = h_artikel = artikel = guest = guestseg = segment = None

    output_list = t_list = segm_list = None

    output_list_data, Output_list = create_model("Output_list", {"flag":string, "segm_no":string, "g_segm":string, "pax":string, "proz_pax":string, "t_rev":string, "proz_trev":string, "m_pax":string, "proz_mpax":string, "m_rev":string, "proz_mrev":string, "y_pax":string, "proz_ypax":string, "y_rev":string, "proz_yrev":string})
    t_list_data, T_list = create_model("T_list", {"flag":string, "segm_no":int, "g_segm":string, "dept":int, "pax":int, "proz_pax":Decimal, "t_rev":Decimal, "proz_trev":Decimal, "m_pax":int, "proz_mpax":Decimal, "m_rev":Decimal, "proz_mrev":Decimal, "y_pax":int, "proz_ypax":Decimal, "y_rev":Decimal, "proz_yrev":Decimal})
    segm_list_data, Segm_list = create_model("Segm_list", {"segmnr":int, "bezeich":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_data, price_decimal, black_list, start_month, start_year, long_digit, f_endkum, m_endkum, b_endkum, lvcarea, htparam, h_journal, h_bill, h_artikel, artikel, guest, guestseg, segment
        nonlocal pvilanguage, from_date, to_date, sorttype


        nonlocal output_list, t_list, segm_list
        nonlocal output_list_data, t_list_data, segm_list_data

        return {"output-list": output_list_data}

    def create_list():

        nonlocal output_list_data, price_decimal, black_list, start_month, start_year, long_digit, f_endkum, m_endkum, b_endkum, lvcarea, htparam, h_journal, h_bill, h_artikel, artikel, guest, guestseg, segment
        nonlocal pvilanguage, from_date, to_date, sorttype


        nonlocal output_list, t_list, segm_list
        nonlocal output_list_data, t_list_data, segm_list_data

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
        tot_pax = 0
        tot_rev =  to_decimal("0")
        tot_mpax = 0
        tot_mrev =  to_decimal("0")
        tot_ypax = 0
        tot_yrev =  to_decimal("0")
        t_list_data.clear()
        output_list_data.clear()
        curr_zeit = get_current_time_in_seconds()

        h_journal = get_cache (H_journal, {"bill_datum": [(ge, start_year),(le, to_date)]})
        while None != h_journal:

            h_bill = get_cache (H_bill, {"rechnr": [(eq, h_journal.rechnr)],"bilname": [(ne, "")],"departement": [(eq, h_journal.departement)]})

            if h_bill:

                h_artikel = get_cache (H_artikel, {"artnr": [(eq, h_journal.artnr)],"departement": [(eq, h_journal.departement)],"artart": [(eq, 0)]})

                if h_artikel:

                    if sorttype == 1:

                        artikel = db_session.query(Artikel).filter(
                                 (Artikel.artnr == h_artikel.artnrfront) & (Artikel.departement == h_artikel.departement) & ((Artikel.endkum == f_endkum) | (Artikel.endkum == m_endkum) | (Artikel.umsatzart == 3) | (Artikel.umsatzart == 5))).first()

                    elif sorttype == 2:

                        artikel = db_session.query(Artikel).filter(
                                 (Artikel.artnr == h_artikel.artnrfront) & (Artikel.departement == h_artikel.departement) & ((Artikel.endkum == b_endkum) | (Artikel.umsatzart == 6))).first()

                    elif sorttype == 3:

                        artikel = get_cache (Artikel, {"artnr": [(eq, h_artikel.artnrfront)],"departement": [(eq, h_artikel.departement)],"umsatzart": [(eq, 4)]})

                    elif sorttype == 4:

                        artikel = db_session.query(Artikel).filter(
                                 (Artikel.artnr == h_artikel.artnrfront) & (Artikel.departement == h_artikel.departement) & ((Artikel.endkum == f_endkum) | (Artikel.endkum == m_endkum) | (Artikel.umsatzart == 3) | (Artikel.umsatzart == 5)) | ((Artikel.endkum == b_endkum) | (Artikel.umsatzart == 6)) | ((Artikel.umsatzart == 4))).first()

                    if artikel:

                        guest = db_session.query(Guest).filter(
                                 (trim(Guest.name + "," + Guest.vorname1) == trim(h_bill.bilname))).first()

                        if guest:

                            guestseg = get_cache (Guestseg, {"gastnr": [(eq, guest.gastnr)],"reihenfolge": [(eq, 1)]})

                            if guestseg:

                                t_list = query(t_list_data, filters=(lambda t_list: t_list.segm_no == guestseg.segmentcode), first=True)

                                if not t_list:
                                    t_list = T_list()
                                    t_list_data.append(t_list)

                                    t_list.segm_no = guestseg.segmentcode

                                    segment = get_cache (Segment, {"segmentcode": [(eq, guestseg.segmentcode)]})

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

            curr_recid = h_journal._recid
            h_journal = db_session.query(H_journal).filter(
                     (H_journal.bill_datum >= start_year) & (H_journal.bill_datum <= to_date) & (H_journal._recid > curr_recid)).first()

        for t_list in query(t_list_data, sort_by=[("segm_no",False)]):

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
            output_list_data.append(output_list)

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

        output_list = query(output_list_data, first=True)

        if output_list:
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list = Output_list()
            output_list_data.append(output_list)

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