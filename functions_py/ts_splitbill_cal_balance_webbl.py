#using conversion tools version: 1.0.0.119
# =========================================
# Rulita, 06/01/2026
# - Recompile program update fitur sub menu
# =========================================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htplogic import htplogic
from models import H_bill_line, H_artikel, Htparam, Hoteldpt, H_mjourn, Artikel

def ts_splitbill_cal_balance_webbl(curr_dept:int, curr_select:int, t_rechnr:int):

    prepare_cache ([H_artikel, Htparam, Hoteldpt, H_mjourn, Artikel])

    balance = to_decimal("0.0")
    t_h_bill_line_data = []
    summary_bill_data = []
    t_h_artikel_data = []
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
    netto_bet:Decimal = to_decimal("0.0")
    cashless_flag:bool = False
    cashless_artnr:int = None
    h_bill_line = h_artikel = htparam = hoteldpt = h_mjourn = artikel = None

    t_h_bill_line = ordered_item = summary_bill = t_h_artikel = h_artikel_buff = None

    t_h_bill_line_data, T_h_bill_line = create_model_like(H_bill_line, {"rec_id":int, "menu_flag":int, "sub_menu_bezeich":string, "sub_menu_betriebsnr":int, "sub_menu_qty":int})
    ordered_item_data, Ordered_item = create_model("Ordered_item", {"dept":int, "artnr":int, "rec_id":int, "qty":int, "epreis":Decimal, "net_bet":Decimal, "tax":Decimal, "service":Decimal, "bill_date":date, "betrag":Decimal})
    summary_bill_data, Summary_bill = create_model("Summary_bill", {"subtotal":Decimal, "total_service":Decimal, "total_tax":Decimal, "grand_total":Decimal})
    t_h_artikel_data, T_h_artikel = create_model_like(H_artikel, {"rec_id":int})

    H_artikel_buff = create_buffer("H_artikel_buff",H_artikel)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal balance, t_h_bill_line_data, summary_bill_data, t_h_artikel_data, t_serv_perc, t_mwst_perc, t_fact, t_service, t_mwst1, t_mwst, h_service, h_mwst, h_mwst2, t_h_service, t_h_mwst, t_h_mwst2, incl_service, incl_mwst, gst_logic, serv_disc, vat_disc, f_discart, amount, f_dec, serv_code, vat_code, servtax_use_foart, serv_vat, tax_vat, ct, l_deci, fact_scvat, service, vat, vat2, mwst, mwst1, sub_tot, tot_serv, tot_tax, grand_tot, netto_bet, cashless_flag, cashless_artnr, h_bill_line, h_artikel, htparam, hoteldpt, h_mjourn, artikel
        nonlocal curr_dept, curr_select, t_rechnr
        nonlocal h_artikel_buff


        nonlocal t_h_bill_line, ordered_item, summary_bill, t_h_artikel, h_artikel_buff
        nonlocal t_h_bill_line_data, ordered_item_data, summary_bill_data, t_h_artikel_data

        return {"balance": balance, "t-h-bill-line": t_h_bill_line_data, "summary-bill": summary_bill_data, "t-h-artikel": t_h_artikel_data}


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
        t_h_artikel_data.append(t_h_artikel)

        buffer_copy(h_artikel, t_h_artikel)
        t_h_artikel.rec_id = to_int(h_artikel._recid)

        if t_h_artikel.artnr == cashless_artnr:
            t_h_artikel.bezeich = replace_str(t_h_artikel.bezeich, " ", "")

    if curr_select > 0:

        for h_bill_line in db_session.query(H_bill_line).filter(
                 (H_bill_line.rechnr == t_rechnr) & (H_bill_line.departement == curr_dept) & (H_bill_line.waehrungsnr == curr_select)).order_by(H_bill_line._recid).all():
            t_h_bill_line = T_h_bill_line()
            t_h_bill_line_data.append(t_h_bill_line)

            buffer_copy(h_bill_line, t_h_bill_line)
            t_h_bill_line.rec_id = h_bill_line._recid

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

            t_h_bill_line.menu_flag = 1

            h_artikel = get_cache (H_artikel, {"artnr": [(eq, h_bill_line.artnr)],"departement": [(eq, curr_dept)]})

            if h_artikel:
                t_h_bill_line.sub_menu_betriebsnr = h_artikel.betriebsnr

                h_mjourn_obj_list = {}
                h_mjourn = H_mjourn()
                h_artikel_buff = H_artikel()
                for h_mjourn.nr, h_mjourn.anzahl, h_mjourn.request, h_mjourn._recid, h_artikel_buff.bezeich, h_artikel_buff.artnr, h_artikel_buff._recid in db_session.query(H_mjourn.nr, H_mjourn.anzahl, H_mjourn.request, H_mjourn._recid, H_artikel_buff.bezeich, H_artikel_buff.artnr, H_artikel_buff._recid).join(H_artikel_buff,(H_artikel_buff.artnr == H_mjourn.artnr) & (H_artikel_buff.departement == H_mjourn.departement)).filter(
                         (H_mjourn.nr == h_artikel.betriebsnr) & (H_mjourn.departement == h_bill_line.departement) & (H_mjourn.rechnr == h_bill_line.rechnr)).order_by(H_mjourn._recid).all():
                    if h_mjourn_obj_list.get(h_mjourn._recid):
                        continue
                    else:
                        h_mjourn_obj_list[h_mjourn._recid] = True

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

    else:

        for h_bill_line in db_session.query(H_bill_line).filter(
                 (H_bill_line.rechnr == t_rechnr) & (H_bill_line.departement == curr_dept)).order_by(H_bill_line._recid).all():
            t_h_bill_line = T_h_bill_line()
            t_h_bill_line_data.append(t_h_bill_line)

            buffer_copy(h_bill_line, t_h_bill_line)
            t_h_bill_line.rec_id = h_bill_line._recid


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

            t_h_bill_line.menu_flag = 1

            h_artikel = get_cache (H_artikel, {"artnr": [(eq, h_bill_line.artnr)],"departement": [(eq, curr_dept)]})

            if h_artikel:
                t_h_bill_line.sub_menu_betriebsnr = h_artikel.betriebsnr

                h_mjourn_obj_list = {}
                h_mjourn = H_mjourn()
                h_artikel_buff = H_artikel()
                for h_mjourn.nr, h_mjourn.anzahl, h_mjourn.request, h_mjourn._recid, h_artikel_buff.bezeich, h_artikel_buff.artnr, h_artikel_buff._recid in db_session.query(H_mjourn.nr, H_mjourn.anzahl, H_mjourn.request, H_mjourn._recid, H_artikel_buff.bezeich, H_artikel_buff.artnr, H_artikel_buff._recid).join(H_artikel_buff,(H_artikel_buff.artnr == H_mjourn.artnr) & (H_artikel_buff.departement == h_bill_line.departement)).filter(
                         (H_mjourn.nr == h_artikel.betriebsnr) & (H_mjourn.departement == h_bill_line.departement) & (H_mjourn.rechnr == h_bill_line.rechnr)).order_by(H_mjourn._recid).all():
                    if h_mjourn_obj_list.get(h_mjourn._recid):
                        continue
                    else:
                        h_mjourn_obj_list[h_mjourn._recid] = True

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

    for ordered_item in query(ordered_item_data):
        t_h_service =  to_decimal("0")
        t_h_mwst =  to_decimal("0")
        t_h_mwst2 =  to_decimal("0")
        h_service =  to_decimal("0")
        h_mwst =  to_decimal("0")
        service =  to_decimal("0")
        mwst =  to_decimal("0")

        h_artikel = get_cache (H_artikel, {"departement": [(eq, ordered_item.dept)],"artnr": [(eq, ordered_item.artnr)],"artart": [(eq, 0)]})

        if h_artikel:
            netto_bet = to_decimal(netto_bet) + to_decimal((ordered_item.epreis) * to_decimal(ordered_item.qty))

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
        sub_tot =  to_decimal(netto_bet)
        tot_serv =  to_decimal(tot_serv) + to_decimal(ordered_item.service)
        tot_tax =  to_decimal(tot_tax) + to_decimal(ordered_item.tax)
        
    grand_tot =  to_decimal(sub_tot) + to_decimal(tot_serv) + to_decimal(tot_tax)
    summary_bill = Summary_bill()
    summary_bill_data.append(summary_bill)

    summary_bill.subtotal =  to_decimal(sub_tot)
    summary_bill.total_service =  to_decimal(tot_serv)
    summary_bill.total_tax =  to_decimal(tot_tax)
    summary_bill.grand_total = to_decimal(round(grand_tot , 0))

    return generate_output()