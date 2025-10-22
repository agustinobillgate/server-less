#using conversion tools version: 1.0.0.117
#----------------------------------------
# Rd 3/8/2025
# dept -> ordered_item.dept

# Rulita, 22/08/2025
# Added : find first h_artikel
# ticketID : 1DA62E
#----------------------------------------

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htplogic import htplogic
from sqlalchemy import func
from functions.ts_restinv_disp_requestbl import ts_restinv_disp_requestbl
from models import H_bill_line, H_artikel, Htparam, Hoteldpt, H_journal, Wgrpgen, Artikel, H_mjourn

def ts_restinv_disp_bill_line_web_1bl(double_currency:bool, rechnr:int, curr_dept:int, avail_t_h_bill:bool, hbill_recid:int):

    prepare_cache ([H_artikel, Htparam, Hoteldpt, H_journal, Wgrpgen, Artikel, H_mjourn])

    t_h_bill_line_data = []
    summary_bill_data = []
    t_h_artikel_data = []
    amount_bill = to_decimal("0.0")
    depo_flag = False
    rsvtable_text = ""
    t_serv_perc:Decimal = to_decimal("0.0")
    t_mwst_perc:Decimal = to_decimal("0.0")
    t_fact:Decimal = 1
    t_service:Decimal = to_decimal("0.0")
    t_mwst1:Decimal = to_decimal("0.0")
    t_mwst:Decimal = to_decimal("0.0")
    h_service:Decimal = to_decimal("0.0")
    h_mwst:Decimal = to_decimal("0.0")
    h_mwst2:Decimal = to_decimal("0.0")
    t_h_service:Decimal = to_decimal("0.0")
    t_h_mwst:Decimal = to_decimal("0.0")
    t_h_mwst2:Decimal = to_decimal("0.0")
    incl_service:bool = False
    incl_mwst:bool = False
    gst_logic:bool = False
    serv_disc:bool = True
    vat_disc:bool = True
    f_discart:int = -1
    amount:Decimal = to_decimal("0.0")
    f_dec:Decimal = to_decimal("0.0")
    serv_code:int = 0
    vat_code:int = 0
    servtax_use_foart:bool = False
    serv_vat:bool = False
    tax_vat:bool = False
    ct:string = ""
    l_deci:int = 2
    fact_scvat:Decimal = 1
    service:Decimal = to_decimal("0.0")
    vat:Decimal = to_decimal("0.0")
    vat2:Decimal = to_decimal("0.0")
    mwst:Decimal = to_decimal("0.0")
    mwst1:Decimal = to_decimal("0.0")
    sub_tot:Decimal = to_decimal("0.0")
    tot_serv:Decimal = to_decimal("0.0")
    tot_tax:Decimal = to_decimal("0.0")
    grand_tot:Decimal = to_decimal("0.0")
    cashless_flag:bool = False
    cashless_artnr:int = None
    h_bill_line_recid_main:int = 0
    request_str:string = ""
    h_bill_line = h_artikel = htparam = hoteldpt = h_journal = wgrpgen = artikel = h_mjourn = None

    t_h_bill_line = ordered_item = summary_bill = t_h_artikel = h_artikel_buff = None

    t_h_bill_line_data, T_h_bill_line = create_model_like(H_bill_line, {"rec_id":int, "request_str":string, "flag_code":int, "kds_stat":int, "kds_stat_str":string, "posting_id":int, "t_time":string, "artart":int, "menu_flag":int, "sub_menu_bezeich":string, "sub_menu_betriebsnr":int, "sub_menu_qty":int}, {"kds_stat": -1})
    ordered_item_data, Ordered_item = create_model("Ordered_item", {"dept":int, "artnr":int, "rec_id":int, "qty":int, "epreis":Decimal, "net_bet":Decimal, "tax":Decimal, "service":Decimal, "bill_date":date, "betrag":Decimal})
    summary_bill_data, Summary_bill = create_model("Summary_bill", {"subtotal":Decimal, "total_service":Decimal, "total_tax":Decimal, "grand_total":Decimal, "gt_not_round":Decimal})
    t_h_artikel_data, T_h_artikel = create_model_like(H_artikel, {"rec_id":int})

    H_artikel_buff = create_buffer("H_artikel_buff",H_artikel)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_h_bill_line_data, summary_bill_data, t_h_artikel_data, amount_bill, depo_flag, rsvtable_text, t_serv_perc, t_mwst_perc, t_fact, t_service, t_mwst1, t_mwst, h_service, h_mwst, h_mwst2, t_h_service, t_h_mwst, t_h_mwst2, incl_service, incl_mwst, gst_logic, serv_disc, vat_disc, f_discart, amount, f_dec, serv_code, vat_code, servtax_use_foart, serv_vat, tax_vat, ct, l_deci, fact_scvat, service, vat, vat2, mwst, mwst1, sub_tot, tot_serv, tot_tax, grand_tot, cashless_flag, cashless_artnr, h_bill_line_recid_main, request_str, h_bill_line, h_artikel, htparam, hoteldpt, h_journal, wgrpgen, artikel, h_mjourn
        nonlocal double_currency, rechnr, curr_dept, avail_t_h_bill, hbill_recid
        nonlocal h_artikel_buff


        nonlocal t_h_bill_line, ordered_item, summary_bill, t_h_artikel, h_artikel_buff
        nonlocal t_h_bill_line_data, ordered_item_data, summary_bill_data, t_h_artikel_data

        return {"t-h-bill-line": t_h_bill_line_data, "summary-bill": summary_bill_data, "t-h-artikel": t_h_artikel_data, "amount_bill": amount_bill, "depo_flag": depo_flag, "rsvtable_text": rsvtable_text}

    def show_submenu():

        nonlocal t_h_bill_line_data, summary_bill_data, t_h_artikel_data, amount_bill, depo_flag, rsvtable_text, t_serv_perc, t_mwst_perc, t_fact, t_service, t_mwst1, t_mwst, h_service, h_mwst, h_mwst2, t_h_service, t_h_mwst, t_h_mwst2, incl_service, incl_mwst, gst_logic, serv_disc, vat_disc, f_discart, amount, f_dec, serv_code, vat_code, servtax_use_foart, serv_vat, tax_vat, ct, l_deci, fact_scvat, service, vat, vat2, mwst, mwst1, sub_tot, tot_serv, tot_tax, grand_tot, cashless_flag, cashless_artnr, h_bill_line_recid_main, request_str, h_bill_line, h_artikel, htparam, hoteldpt, h_journal, wgrpgen, artikel, h_mjourn
        nonlocal double_currency, rechnr, curr_dept, avail_t_h_bill, hbill_recid
        nonlocal h_artikel_buff


        nonlocal t_h_bill_line, ordered_item, summary_bill, t_h_artikel, h_artikel_buff
        nonlocal t_h_bill_line_data, ordered_item_data, summary_bill_data, t_h_artikel_data

        h_art2 = None
        rqst_sub_menu:string = ""
        list_reqst:List[string] = create_empty_list(15,"")
        list_rec_id:List[int] = create_empty_list(15,0)
        counter:int = 0
        nr:int = 0
        h_bill_line_recid:int = 0
        H_art2 =  create_buffer("H_art2",H_artikel)

        h_art2 = get_cache (H_artikel, {"departement": [(eq, h_bill_line.departement)],"artnr": [(eq, h_bill_line.artnr)]})

        if not h_art2 or not avail_t_h_bill:
            t_h_bill_line.flag_code = 0

        elif h_art2.artart == 0 and h_art2.betriebsnr > 0:
            t_h_bill_line.flag_code = 1
            t_h_bill_line.sub_menu_betriebsnr = h_art2.betriebsnr

            h_mjourn_obj_list = {}
            h_mjourn = H_mjourn()
            h_artikel_buff = H_artikel()
            for h_mjourn.nr, h_mjourn.anzahl, h_mjourn.request, h_mjourn._recid, h_artikel_buff.betriebsnr, h_artikel_buff.departement, h_artikel_buff.artart, h_artikel_buff._recid, h_artikel_buff.bezeich, h_artikel_buff.artnr in db_session.query(H_mjourn.nr, H_mjourn.anzahl, H_mjourn.request, H_mjourn._recid, H_artikel_buff.betriebsnr, H_artikel_buff.departement, H_artikel_buff.artart, H_artikel_buff._recid, H_artikel_buff.bezeich, H_artikel_buff.artnr).join(H_artikel_buff,(H_artikel_buff.artnr == H_mjourn.artnr) & (H_artikel_buff.departement == H_mjourn.departement)).filter(
                     (H_mjourn.nr == h_art2.betriebsnr) & (H_mjourn.departement == h_art2.departement) & (H_mjourn.rechnr == h_bill_line.rechnr)).order_by(H_mjourn._recid).all():
                if h_mjourn_obj_list.get(h_mjourn._recid):
                    continue
                else:
                    h_mjourn_obj_list[h_mjourn._recid] = True


                counter = counter + 1

                if num_entries(h_mjourn.request, "|") > 1:

                    if entry(0, h_mjourn.request, "|") == to_string(h_bill_line._recid):
                        t_h_bill_line = T_h_bill_line()
                        t_h_bill_line_data.append(t_h_bill_line)

                        t_h_bill_line.menu_flag = 2
                        t_h_bill_line.sub_menu_bezeich = h_artikel_buff.bezeich
                        t_h_bill_line.sub_menu_betriebsnr = h_mjourn.nr
                        t_h_bill_line.sub_menu_qty = h_mjourn.anzahl
                        t_h_bill_line.rec_id = h_bill_line._recid
                        t_h_bill_line.artnr = h_artikel_buff.artnr
                        t_h_bill_line.request_str = entry(1, h_mjourn.request, "|")
                        t_h_bill_line.rechnr = None
                        t_h_bill_line.bill_datum = None
                        t_h_bill_line.anzahl = None
                        t_h_bill_line.epreis =  to_decimal(None)
                        t_h_bill_line.betrag =  to_decimal(None)
                        t_h_bill_line.steuercode = None
                        t_h_bill_line.bezeich = None
                        t_h_bill_line.fremdwbetrag =  to_decimal(None)
                        t_h_bill_line.zeit = None
                        t_h_bill_line.waehrungsnr = None
                        t_h_bill_line.sysdate = None
                        t_h_bill_line.departement = None
                        t_h_bill_line.prtflag = None
                        t_h_bill_line.tischnr = None
                        t_h_bill_line.kellner_nr = None
                        t_h_bill_line.nettobetrag =  to_decimal(None)
                        t_h_bill_line.paid_flag = None
                        t_h_bill_line.betriebsnr = None
                        t_h_bill_line.segmentcode = None
                        t_h_bill_line.transferred = None
                        t_h_bill_line.flag_code = None
                        t_h_bill_line.kds_stat = None
                        t_h_bill_line.kds_stat_st = None
                        t_h_bill_line.posting_id = None
                        t_h_bill_line.t_time = None
                        t_h_bill_line.artart = None

    htparam = get_cache (Htparam, {"paramnr": [(eq, 468)]})

    if htparam:
        serv_disc = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 469)]})

    if htparam:
        vat_disc = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 557)]})

    if htparam.finteger != 0:
        f_discart = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 376)]})

    if htparam:

        if not htparam.flogical and entry(0, htparam.fchar, ";") == ("GST(MA)").lower() :
            gst_logic = True

    htparam = get_cache (Htparam, {"paramnr": [(eq, 135)]})
    incl_service = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 134)]})
    incl_mwst = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 834)]})
    cashless_flag = htparam.flogical

    if cashless_flag:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 569)]})

        if htparam.paramnr != 0:
            cashless_artnr = htparam.finteger

    hoteldpt = get_cache (Hoteldpt, {"num": [(eq, curr_dept)]})

    if hoteldpt:
        servtax_use_foart = hoteldpt.defult
    serv_vat = get_output(htplogic(479))
    tax_vat = get_output(htplogic(483))

    for h_artikel in db_session.query(H_artikel).filter(
             (H_artikel.departement == curr_dept) & ((H_artikel.artart == 2) | (H_artikel.artart == 6) | (H_artikel.artart == 7) | (H_artikel.artart == 11) | (H_artikel.artart == 12) | (H_artikel.artart == 5))).order_by(H_artikel._recid).all():
        t_h_artikel = T_h_artikel()
        t_h_artikel_data.append(t_h_artikel)

        buffer_copy(h_artikel, t_h_artikel)
        t_h_artikel.rec_id = to_int(h_artikel._recid)

        if t_h_artikel.artnr == cashless_artnr:
            t_h_artikel.bezeich = replace_str(t_h_artikel.bezeich, " ", "")

    if double_currency:

        for h_bill_line in db_session.query(H_bill_line).filter(
                 (H_bill_line.rechnr == rechnr) & (H_bill_line.departement == curr_dept)).order_by(H_bill_line.bill_datum.desc(), H_bill_line.zeit.desc()).yield_per(100):
            t_h_bill_line = T_h_bill_line()
            t_h_bill_line_data.append(t_h_bill_line)

            buffer_copy(h_bill_line, t_h_bill_line)
            t_h_bill_line.rec_id = h_bill_line._recid
            t_h_bill_line.t_time = to_string(h_bill_line.zeit, "HH:MM:SS")

            h_journal = get_cache (H_journal, {"rechnr": [(eq, h_bill_line.rechnr)],"zeit": [(eq, h_bill_line.zeit)],"schankbuch": [(eq, to_int(h_bill_line._recid))]})

            if h_journal:
                t_h_bill_line.posting_id = h_journal.kellner_nr


            else:

                h_journal = db_session.query(H_journal).filter(
                         (H_journal.rechnr == h_bill_line.rechnr) & (H_journal.zeit == h_bill_line.zeit) & (matches(H_journal.bezeich,"*Discount*")) | (matches(H_journal.bezeich,"*Disc*"))).first()

                if h_journal:
                    t_h_bill_line.posting_id = h_journal.kellner_nr

            h_artikel = get_cache (H_artikel, {"artnr": [(eq, h_bill_line.artnr)],"departement": [(eq, h_bill_line.departement)]})

            if h_artikel:
                t_h_bill_line.artart = h_artikel.artart
            request_str = get_output(ts_restinv_disp_requestbl(h_bill_line._recid))
            t_h_bill_line.request_str = request_str
            amount_bill =  to_decimal(amount_bill) + to_decimal(h_bill_line.betrag)


            ordered_item = Ordered_item()
            ordered_item_data.append(ordered_item)

            ordered_item.dept = t_h_bill_line.departement
            ordered_item.artnr = t_h_bill_line.artnr
            ordered_item.rec_id = t_h_bill_line.rec_id
            ordered_item.qty = t_h_bill_line.anzahl
            ordered_item.epreis =  to_decimal(t_h_bill_line.epreis)
            ordered_item.net_bet =  to_decimal(t_h_bill_line.nettobetrag)
            ordered_item.bill_date = t_h_bill_line.bill_datum
            ordered_item.betrag =  to_decimal(t_h_bill_line.betrag)


            show_submenu()

    else:

        for h_bill_line in db_session.query(H_bill_line).filter(
                 (H_bill_line.rechnr == rechnr) & (H_bill_line.departement == curr_dept)).order_by(H_bill_line.bill_datum.desc(), H_bill_line.zeit.desc()).yield_per(100):
            h_bill_line_recid_main = h_bill_line._recid
            t_h_bill_line = T_h_bill_line()
            t_h_bill_line_data.append(t_h_bill_line)

            buffer_copy(h_bill_line, t_h_bill_line)
            t_h_bill_line.rec_id = h_bill_line._recid
            t_h_bill_line.t_time = to_string(h_bill_line.zeit, "HH:MM:SS")
            t_h_bill_line.menu_flag = 1

            h_journal = get_cache (H_journal, {"rechnr": [(eq, h_bill_line.rechnr)],"zeit": [(eq, h_bill_line.zeit)],"schankbuch": [(eq, to_int(h_bill_line._recid))]})

            if h_journal:
                t_h_bill_line.posting_id = h_journal.kellner_nr


            else:

                h_journal = db_session.query(H_journal).filter(
                         (H_journal.rechnr == h_bill_line.rechnr) & (H_journal.zeit == h_bill_line.zeit) & (matches(H_journal.bezeich,"*Discount*")) | (matches(H_journal.bezeich,"*Disc*"))).first()

                if h_journal:
                    t_h_bill_line.posting_id = h_journal.kellner_nr

            h_artikel = get_cache (H_artikel, {"artnr": [(eq, h_bill_line.artnr)],"departement": [(eq, h_bill_line.departement)]})

            if h_artikel:
                t_h_bill_line.artart = h_artikel.artart
            request_str = get_output(ts_restinv_disp_requestbl(h_bill_line._recid))
            t_h_bill_line.request_str = request_str
            amount_bill =  to_decimal(amount_bill) + to_decimal(h_bill_line.betrag)


            ordered_item = Ordered_item()
            ordered_item_data.append(ordered_item)

            ordered_item.dept = t_h_bill_line.departement
            ordered_item.artnr = t_h_bill_line.artnr
            ordered_item.rec_id = t_h_bill_line.rec_id
            ordered_item.qty = t_h_bill_line.anzahl
            ordered_item.epreis =  to_decimal(t_h_bill_line.epreis)
            ordered_item.net_bet =  to_decimal(t_h_bill_line.nettobetrag)
            ordered_item.bill_date = t_h_bill_line.bill_datum
            ordered_item.betrag =  to_decimal(t_h_bill_line.betrag)


            show_submenu()


    wgrpgen = db_session.query(Wgrpgen).filter(
             (matches(Wgrpgen.bezeich,"*deposit*"))).first()

    if wgrpgen:

        h_bill_line_obj_list = {}
        for h_bill_line, h_artikel in db_session.query(H_bill_line, H_artikel).join(H_artikel,(H_artikel.artnr == H_bill_line.artnr) & (H_artikel.departement == H_bill_line.departement) & (H_artikel.activeflag)).filter(
                 (H_bill_line.rechnr == rechnr) & (H_bill_line.departement == curr_dept)).order_by(H_bill_line.bill_datum.desc(), H_bill_line.zeit.desc()).yield_per(100):
            if h_bill_line_obj_list.get(h_bill_line._recid):
                continue
            else:
                h_bill_line_obj_list[h_bill_line._recid] = True

            if h_artikel.endkum == wgrpgen.eknr:
                depo_flag = True
                break

    for ordered_item in query(ordered_item_data):
        t_h_service =  to_decimal("0")
        t_h_mwst =  to_decimal("0")
        t_h_mwst2 =  to_decimal("0")
        h_service =  to_decimal("0")
        h_mwst =  to_decimal("0")
        service =  to_decimal("0")
        mwst =  to_decimal("0")

        # Rd, 3/8/2025
        # h_artikel = get_cache (H_artikel, {"departement": [(eq, dept)],"artnr": [(eq, ordered_item.artnr)],"artart": [(eq, 0)]})
        h_artikel = get_cache (H_artikel, {"departement": [(eq, ordered_item.dept)],"artnr": [(eq, ordered_item.artnr)],"artart": [(eq, 0)]})

        if h_artikel:

            if not servtax_use_foart:
                serv_code = h_artikel.service_code
                vat_code = h_artikel.mwst_code


            else:

                artikel = get_cache (Artikel, {"artnr": [(eq, h_artikel.artnrfront)],"departement": [(eq, h_artikel.departement)]})

                if artikel:
                    serv_code = artikel.service_code
                    vat_code = artikel.mwst_code

        if h_artikel:

            if ordered_item.artnr != f_discart:

                if serv_code != 0 and not incl_service:

                    htparam = get_cache (Htparam, {"paramnr": [(eq, serv_code)]})

                    if htparam and htparam.fdecimal != 0:

                        if num_entries(htparam.fchar, chr_unicode(2)) >= 2:
                            t_h_service =  to_decimal(to_decimal(entry(1 , htparam.fchar , chr_unicode(2)))) / to_decimal("10000")


                        else:
                            t_h_service =  to_decimal(htparam.fdecimal)

                if vat_code != 0 and not incl_mwst:

                    htparam = get_cache (Htparam, {"paramnr": [(eq, vat_code)]})

                    if htparam and htparam.fdecimal != 0:

                        if num_entries(htparam.fchar, chr_unicode(2)) >= 2:
                            t_h_mwst =  to_decimal(to_decimal(entry(1 , htparam.fchar , chr_unicode(2)))) / to_decimal("10000")


                        else:
                            t_h_mwst =  to_decimal(htparam.fdecimal)

                        if serv_vat and not tax_vat:
                            t_h_mwst =  to_decimal(t_h_mwst) + to_decimal(t_h_mwst) * to_decimal(t_h_service) / to_decimal("100")

                        elif serv_vat and tax_vat:
                            t_h_mwst =  to_decimal(t_h_mwst) + to_decimal(t_h_mwst) * to_decimal((t_h_service) + to_decimal(t_h_mwst2)) / to_decimal("100")

                        elif not serv_vat and tax_vat:
                            t_h_mwst =  to_decimal(t_h_mwst) + to_decimal(t_h_mwst) * to_decimal(t_h_mwst2) / to_decimal("100")
                        ct = replace_str(to_string(t_h_mwst) , ".", ",")
                        l_deci = length(entry(1, ct, ","))

                        if l_deci <= 2:
                            t_h_mwst = to_decimal(round(t_h_mwst , 2))

                        elif l_deci == 3:
                            t_h_mwst = to_decimal(round(t_h_mwst , 3))
                        else:
                            t_h_mwst = to_decimal(round(t_h_mwst , 4))

                if t_h_service != 0 or t_h_mwst != 0:
                    t_h_service =  to_decimal(t_h_service) / to_decimal("100")
                    t_h_mwst =  to_decimal(t_h_mwst) / to_decimal("100")
                    t_h_mwst2 =  to_decimal(t_h_mwst2) / to_decimal("100")


                    fact_scvat =  to_decimal("1") + to_decimal(t_h_service) + to_decimal(t_h_mwst) + to_decimal(t_h_mwst2)
                    h_service =  to_decimal(ordered_item.betrag) / to_decimal(fact_scvat) * to_decimal(t_h_service)
                    h_service = to_decimal(round(h_service , 2))
                    h_mwst =  to_decimal(ordered_item.betrag) / to_decimal(fact_scvat) * to_decimal(t_h_mwst)
                    h_mwst = to_decimal(round(h_mwst , 2))

                    if not incl_service:
                        service =  to_decimal(service) + to_decimal(h_service)

                    if not incl_mwst:
                        mwst =  to_decimal(mwst) + to_decimal(h_mwst)
                        mwst1 =  to_decimal(mwst1) + to_decimal(h_mwst)
            else:

                if serv_code != 0 and not incl_service and serv_disc:

                    htparam = get_cache (Htparam, {"paramnr": [(eq, serv_code)]})

                    if htparam and htparam.fdecimal != 0:

                        if num_entries(htparam.fchar, chr_unicode(2)) >= 2:
                            t_h_service =  to_decimal(to_decimal(entry(1 , htparam.fchar , chr_unicode(2)))) / to_decimal("10000")


                        else:
                            t_h_service =  to_decimal(htparam.fdecimal)

                if vat_code != 0 and not incl_mwst and vat_disc:

                    htparam = get_cache (Htparam, {"paramnr": [(eq, vat_code)]})

                    if htparam and htparam.fdecimal != 0:

                        if num_entries(htparam.fchar, chr_unicode(2)) >= 2:
                            t_h_mwst =  to_decimal(to_decimal(entry(1 , htparam.fchar , chr_unicode(2)))) / to_decimal("10000")


                        else:
                            t_h_mwst =  to_decimal(htparam.fdecimal)

                        if serv_vat and not tax_vat:
                            t_h_mwst =  to_decimal(t_h_mwst) + to_decimal(t_h_mwst) * to_decimal(t_h_service) / to_decimal("100")

                        elif serv_vat and tax_vat:
                            t_h_mwst =  to_decimal(t_h_mwst) + to_decimal(t_h_mwst) * to_decimal((t_h_service) + to_decimal(t_h_mwst2)) / to_decimal("100")

                        elif not serv_vat and tax_vat:
                            t_h_mwst =  to_decimal(t_h_mwst) + to_decimal(t_h_mwst) * to_decimal(t_h_mwst2) / to_decimal("100")
                        ct = replace_str(to_string(t_h_mwst) , ".", ",")
                        l_deci = length(entry(1, ct, ","))

                        if l_deci <= 2:
                            t_h_mwst = to_decimal(round(t_h_mwst , 2))

                        elif l_deci == 3:
                            t_h_mwst = to_decimal(round(t_h_mwst , 3))
                        else:
                            t_h_mwst = to_decimal(round(t_h_mwst , 4))

                if ordered_item.epreis != ordered_item.betrag:

                    if t_h_service != 0 or t_h_mwst != 0:
                        t_h_service =  to_decimal(t_h_service) / to_decimal("100")
                        t_h_mwst =  to_decimal(t_h_mwst) / to_decimal("100")
                        t_h_mwst2 =  to_decimal(t_h_mwst2) / to_decimal("100")


                        fact_scvat =  to_decimal("1") + to_decimal(t_h_service) + to_decimal(t_h_mwst) + to_decimal(t_h_mwst2)
                        h_service =  to_decimal(ordered_item.betrag) / to_decimal(fact_scvat) * to_decimal(t_h_service)
                        h_service = to_decimal(round(h_service , 2))
                        h_mwst =  to_decimal(ordered_item.betrag) / to_decimal(fact_scvat) * to_decimal(t_h_mwst)
                        h_mwst = to_decimal(round(h_mwst , 2))

                        if not incl_service:
                            service =  to_decimal(service) + to_decimal(h_service)

                        if not incl_mwst:
                            mwst =  to_decimal(mwst) + to_decimal(h_mwst)
                            mwst1 =  to_decimal(mwst1) + to_decimal(h_mwst)
            ordered_item.service =  to_decimal(service)
            ordered_item.tax =  to_decimal(mwst)

    for ordered_item in query(ordered_item_data):
        sub_tot =  to_decimal(sub_tot) + to_decimal((ordered_item.epreis) * to_decimal(ordered_item.qty))
        tot_serv =  to_decimal(tot_serv) + to_decimal(ordered_item.service)
        tot_tax =  to_decimal(tot_tax) + to_decimal(ordered_item.tax)
    grand_tot =  to_decimal(sub_tot) + to_decimal(tot_serv) + to_decimal(tot_tax)
    summary_bill = Summary_bill()
    summary_bill_data.append(summary_bill)

    summary_bill.subtotal =  to_decimal(sub_tot)
    summary_bill.total_service =  to_decimal(tot_serv)
    summary_bill.total_tax =  to_decimal(tot_tax)
    summary_bill.grand_total = to_decimal(round(grand_tot , 0))
    summary_bill.gt_not_round =  to_decimal(grand_tot)

    return generate_output()