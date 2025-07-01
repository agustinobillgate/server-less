#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htplogic import htplogic
from functions.ts_restinv_disp_requestbl import ts_restinv_disp_requestbl
from models import H_bill_line, H_artikel, Htparam, Hoteldpt, Artikel

def ts_restinv_disp_bill_line_webbl(double_currency:bool, rechnr:int, curr_dept:int, avail_t_h_bill:bool):

    prepare_cache ([H_artikel, Htparam, Hoteldpt, Artikel])

    t_h_bill_line_list = []
    summary_bill_list = []
    t_h_artikel_list = []
    amount_bill = to_decimal("0.0")
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
    h_bill_line = h_artikel = htparam = hoteldpt = artikel = None

    t_h_bill_line = ordered_item = summary_bill = t_h_artikel = None

    t_h_bill_line_list, T_h_bill_line = create_model_like(H_bill_line, {"rec_id":int, "request_str":string, "flag_code":int})
    ordered_item_list, Ordered_item = create_model("Ordered_item", {"dept":int, "artnr":int, "rec_id":int, "qty":int, "epreis":Decimal, "net_bet":Decimal, "tax":Decimal, "service":Decimal, "bill_date":date, "betrag":Decimal})
    summary_bill_list, Summary_bill = create_model("Summary_bill", {"subtotal":Decimal, "total_service":Decimal, "total_tax":Decimal, "grand_total":Decimal, "gt_not_round":Decimal})
    t_h_artikel_list, T_h_artikel = create_model_like(H_artikel, {"rec_id":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_h_bill_line_list, summary_bill_list, t_h_artikel_list, amount_bill, t_serv_perc, t_mwst_perc, t_fact, t_service, t_mwst1, t_mwst, h_service, h_mwst, h_mwst2, t_h_service, t_h_mwst, t_h_mwst2, incl_service, incl_mwst, gst_logic, serv_disc, vat_disc, f_discart, amount, f_dec, serv_code, vat_code, servtax_use_foart, serv_vat, tax_vat, ct, l_deci, fact_scvat, service, vat, vat2, mwst, mwst1, sub_tot, tot_serv, tot_tax, grand_tot, cashless_flag, cashless_artnr, h_bill_line, h_artikel, htparam, hoteldpt, artikel
        nonlocal double_currency, rechnr, curr_dept, avail_t_h_bill


        nonlocal t_h_bill_line, ordered_item, summary_bill, t_h_artikel
        nonlocal t_h_bill_line_list, ordered_item_list, summary_bill_list, t_h_artikel_list

        return {"t-h-bill-line": t_h_bill_line_list, "summary-bill": summary_bill_list, "t-h-artikel": t_h_artikel_list, "amount_bill": amount_bill}

    def show_submenu():

        nonlocal t_h_bill_line_list, summary_bill_list, t_h_artikel_list, amount_bill, t_serv_perc, t_mwst_perc, t_fact, t_service, t_mwst1, t_mwst, h_service, h_mwst, h_mwst2, t_h_service, t_h_mwst, t_h_mwst2, incl_service, incl_mwst, gst_logic, serv_disc, vat_disc, f_discart, amount, f_dec, serv_code, vat_code, servtax_use_foart, serv_vat, tax_vat, ct, l_deci, fact_scvat, service, vat, vat2, mwst, mwst1, sub_tot, tot_serv, tot_tax, grand_tot, cashless_flag, cashless_artnr, h_bill_line, h_artikel, htparam, hoteldpt, artikel
        nonlocal double_currency, rechnr, curr_dept, avail_t_h_bill


        nonlocal t_h_bill_line, ordered_item, summary_bill, t_h_artikel
        nonlocal t_h_bill_line_list, ordered_item_list, summary_bill_list, t_h_artikel_list

        h_art2 = None
        H_art2 =  create_buffer("H_art2",H_artikel)

        h_art2 = get_cache (H_artikel, {"departement": [(eq, h_bill_line.departement)],"artnr": [(eq, h_bill_line.artnr)]})

        if not h_art2 or not avail_t_h_bill:
            t_h_bill_line.flag_code = 0

        elif h_art2.artart == 0 and h_art2.betriebsnr > 0:
            t_h_bill_line.flag_code = 1

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
             (H_artikel.departement == curr_dept) & ((H_artikel.artart == 2) | (H_artikel.artart == 6) | (H_artikel.artart == 7) | (H_artikel.artart == 11) | (H_artikel.artart == 12))).order_by(H_artikel._recid).all():
        t_h_artikel = T_h_artikel()
        t_h_artikel_list.append(t_h_artikel)

        buffer_copy(h_artikel, t_h_artikel)
        t_h_artikel.rec_id = to_int(h_artikel._recid)

        if t_h_artikel.artnr == cashless_artnr:
            t_h_artikel.bezeich = replace_str(t_h_artikel.bezeich, " ", "")

    if double_currency:

        for h_bill_line in db_session.query(H_bill_line).filter(
                 (H_bill_line.rechnr == rechnr) & (H_bill_line.departement == curr_dept)).order_by(H_bill_line.bill_datum.desc(), H_bill_line.zeit.desc()).all():
            t_h_bill_line = T_h_bill_line()
            t_h_bill_line_list.append(t_h_bill_line)

            buffer_copy(h_bill_line, t_h_bill_line)
            t_h_bill_line.rec_id = h_bill_line._recid


            show_submenu()
            request_str = get_output(ts_restinv_disp_requestbl(h_bill_line._recid))
            t_h_bill_line.request_str = request_str
            amount_bill =  to_decimal(amount_bill) + to_decimal(h_bill_line.betrag)


            ordered_item = Ordered_item()
            ordered_item_list.append(ordered_item)

            ordered_item.dept = t_h_bill_line.departement
            ordered_item.artnr = t_h_bill_line.artnr
            ordered_item.rec_id = t_h_bill_line.rec_id
            ordered_item.qty = t_h_bill_line.anzahl
            ordered_item.epreis =  to_decimal(t_h_bill_line.epreis)
            ordered_item.net_bet =  to_decimal(t_h_bill_line.nettobetrag)
            ordered_item.bill_date = t_h_bill_line.bill_datum
            ordered_item.betrag =  to_decimal(t_h_bill_line.betrag)

    else:

        for h_bill_line in db_session.query(H_bill_line).filter(
                 (H_bill_line.rechnr == rechnr) & (H_bill_line.departement == curr_dept)).order_by(H_bill_line.bill_datum.desc(), H_bill_line.zeit.desc()).all():
            t_h_bill_line = T_h_bill_line()
            t_h_bill_line_list.append(t_h_bill_line)

            buffer_copy(h_bill_line, t_h_bill_line)
            t_h_bill_line.rec_id = h_bill_line._recid


            show_submenu()
            request_str = get_output(ts_restinv_disp_requestbl(h_bill_line._recid))
            t_h_bill_line.request_str = request_str
            amount_bill =  to_decimal(amount_bill) + to_decimal(h_bill_line.betrag)


            ordered_item = Ordered_item()
            ordered_item_list.append(ordered_item)

            ordered_item.dept = t_h_bill_line.departement
            ordered_item.artnr = t_h_bill_line.artnr
            ordered_item.rec_id = t_h_bill_line.rec_id
            ordered_item.qty = t_h_bill_line.anzahl
            ordered_item.epreis =  to_decimal(t_h_bill_line.epreis)
            ordered_item.net_bet =  to_decimal(t_h_bill_line.nettobetrag)
            ordered_item.bill_date = t_h_bill_line.bill_datum
            ordered_item.betrag =  to_decimal(t_h_bill_line.betrag)


    for ordered_item in query(ordered_item_list):
        t_h_service =  to_decimal("0")
        t_h_mwst =  to_decimal("0")
        t_h_mwst2 =  to_decimal("0")
        h_service =  to_decimal("0")
        h_mwst =  to_decimal("0")
        service =  to_decimal("0")
        mwst =  to_decimal("0")

        h_artikel = get_cache (H_artikel, {"departement": [(eq, dept)],"artnr": [(eq, ordered_item.artnr)],"artart": [(eq, 0)]})

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

    for ordered_item in query(ordered_item_list):
        sub_tot =  to_decimal(sub_tot) + to_decimal((ordered_item.epreis) * to_decimal(ordered_item.qty))
        tot_serv =  to_decimal(tot_serv) + to_decimal(ordered_item.service)
        tot_tax =  to_decimal(tot_tax) + to_decimal(ordered_item.tax)
    grand_tot =  to_decimal(sub_tot) + to_decimal(tot_serv) + to_decimal(tot_tax)
    summary_bill = Summary_bill()
    summary_bill_list.append(summary_bill)

    summary_bill.subtotal =  to_decimal(sub_tot)
    summary_bill.total_service =  to_decimal(tot_serv)
    summary_bill.total_tax =  to_decimal(tot_tax)
    summary_bill.grand_total = to_decimal(round(grand_tot , 0))
    summary_bill.gt_not_round =  to_decimal(grand_tot)

    return generate_output()