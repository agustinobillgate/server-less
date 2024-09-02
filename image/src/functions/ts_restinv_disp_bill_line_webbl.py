from functions.additional_functions import *
import decimal
from datetime import date
from functions.htplogic import htplogic
from functions.ts_restinv_disp_requestbl import ts_restinv_disp_requestbl
from models import H_bill_line, H_artikel, Htparam, Hoteldpt, Artikel

def ts_restinv_disp_bill_line_webbl(double_currency:bool, rechnr:int, curr_dept:int, avail_t_h_bill:bool):
    t_h_bill_line_list = []
    summary_bill_list = []
    t_h_artikel_list = []
    amount_bill = 0
    t_serv_perc:decimal = 0
    t_mwst_perc:decimal = 0
    t_fact:decimal = 1
    t_service:decimal = 0
    t_mwst1:decimal = 0
    t_mwst:decimal = 0
    h_service:decimal = 0
    h_mwst:decimal = 0
    h_mwst2:decimal = 0
    t_h_service:decimal = 0
    t_h_mwst:decimal = 0
    t_h_mwst2:decimal = 0
    incl_service:bool = False
    incl_mwst:bool = False
    gst_logic:bool = False
    serv_disc:bool = True
    vat_disc:bool = True
    f_discart:int = -1
    amount:decimal = 0
    f_dec:decimal = 0
    serv_code:int = 0
    vat_code:int = 0
    servtax_use_foart:bool = False
    serv_vat:bool = False
    tax_vat:bool = False
    ct:str = ""
    l_deci:int = 2
    fact_scvat:decimal = 1
    service:decimal = 0
    vat:decimal = 0
    vat2:decimal = 0
    mwst:decimal = 0
    mwst1:decimal = 0
    sub_tot:decimal = 0
    tot_serv:decimal = 0
    tot_tax:decimal = 0
    grand_tot:decimal = 0
    cashless_flag:bool = False
    cashless_artnr:int = None
    h_bill_line = h_artikel = htparam = hoteldpt = artikel = None

    t_h_bill_line = ordered_item = summary_bill = t_h_artikel = h_art2 = None

    t_h_bill_line_list, T_h_bill_line = create_model_like(H_bill_line, {"rec_id":int, "request_str":str, "flag_code":int})
    ordered_item_list, Ordered_item = create_model("Ordered_item", {"dept":int, "artnr":int, "rec_id":int, "qty":int, "epreis":decimal, "net_bet":decimal, "tax":decimal, "service":decimal, "bill_date":date, "betrag":decimal})
    summary_bill_list, Summary_bill = create_model("Summary_bill", {"subtotal":decimal, "total_service":decimal, "total_tax":decimal, "grand_total":decimal, "gt_not_round":decimal})
    t_h_artikel_list, T_h_artikel = create_model_like(H_artikel, {"rec_id":int})

    H_art2 = H_artikel

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_h_bill_line_list, summary_bill_list, t_h_artikel_list, amount_bill, t_serv_perc, t_mwst_perc, t_fact, t_service, t_mwst1, t_mwst, h_service, h_mwst, h_mwst2, t_h_service, t_h_mwst, t_h_mwst2, incl_service, incl_mwst, gst_logic, serv_disc, vat_disc, f_discart, amount, f_dec, serv_code, vat_code, servtax_use_foart, serv_vat, tax_vat, ct, l_deci, fact_scvat, service, vat, vat2, mwst, mwst1, sub_tot, tot_serv, tot_tax, grand_tot, cashless_flag, cashless_artnr, h_bill_line, h_artikel, htparam, hoteldpt, artikel
        nonlocal h_art2


        nonlocal t_h_bill_line, ordered_item, summary_bill, t_h_artikel, h_art2
        nonlocal t_h_bill_line_list, ordered_item_list, summary_bill_list, t_h_artikel_list
        return {"t-h-bill-line": t_h_bill_line_list, "summary-bill": summary_bill_list, "t-h-artikel": t_h_artikel_list, "amount_bill": amount_bill}

    def show_submenu():

        nonlocal t_h_bill_line_list, summary_bill_list, t_h_artikel_list, amount_bill, t_serv_perc, t_mwst_perc, t_fact, t_service, t_mwst1, t_mwst, h_service, h_mwst, h_mwst2, t_h_service, t_h_mwst, t_h_mwst2, incl_service, incl_mwst, gst_logic, serv_disc, vat_disc, f_discart, amount, f_dec, serv_code, vat_code, servtax_use_foart, serv_vat, tax_vat, ct, l_deci, fact_scvat, service, vat, vat2, mwst, mwst1, sub_tot, tot_serv, tot_tax, grand_tot, cashless_flag, cashless_artnr, h_bill_line, h_artikel, htparam, hoteldpt, artikel
        nonlocal h_art2


        nonlocal t_h_bill_line, ordered_item, summary_bill, t_h_artikel, h_art2
        nonlocal t_h_bill_line_list, ordered_item_list, summary_bill_list, t_h_artikel_list


        H_art2 = H_artikel

        h_art2 = db_session.query(H_art2).filter(
                (H_art2.departement == h_bill_line.departement) &  (H_art2.artnr == h_bill_line.artnr)).first()

        if not h_art2 or not avail_t_h_bill:
            t_h_bill_line.flag_code = 0

        elif h_art2.artart == 0 and h_art2.betriebsnr > 0:
            t_h_bill_line.flag_code = 1


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 468)).first()

    if htparam:
        serv_disc = htparam.flogic

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 469)).first()

    if htparam:
        vat_disc = htparam.flogic

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 557)).first()

    if htparam.finteger != 0:
        f_discart = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 376)).first()

    if htparam:

        if not htparam.flogic and entry(0, htparam.fchar, ";") == "GST(MA)":
            gst_logic = True

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 135)).first()
    incl_service = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 134)).first()
    incl_mwst = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 834)).first()
    cashless_flag = htparam.flogical

    if cashless_flag:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 569)).first()

        if htparam.paramnr != 0:
            cashless_artnr = htparam.finteger

    hoteldpt = db_session.query(Hoteldpt).filter(
            (Hoteldpt.num == curr_dept)).first()

    if hoteldpt:
        servtax_use_foart = hoteldpt.defult
    serv_vat = get_output(htplogic(479))
    tax_vat = get_output(htplogic(483))

    for h_artikel in db_session.query(H_artikel).filter(
            (H_artikel.departement == curr_dept) &  ((H_artikel.artart == 2) |  (H_artikel.artart == 6) |  (H_artikel.artart == 7) |  (H_artikel.artart == 11) |  (H_artikel.artart == 12))).all():
        t_h_artikel = T_h_artikel()
        t_h_artikel_list.append(t_h_artikel)

        buffer_copy(h_artikel, t_h_artikel)
        t_h_artikel.rec_id = to_int(h_artikel._recid)

        if t_h_artikel.artnr == cashless_artnr:
            t_h_artikel.bezeich = replace_str(t_h_artikel.bezeich, " ", "")

    if double_currency:

        for h_bill_line in db_session.query(H_bill_line).filter(
                (H_bill_line.rechnr == rechnr) &  (H_bill_line.departement == curr_dept)).all():
            t_h_bill_line = T_h_bill_line()
            t_h_bill_line_list.append(t_h_bill_line)

            buffer_copy(h_bill_line, t_h_bill_line)
            t_h_bill_line.rec_id = h_bill_line._recid


            show_submenu()
            request_str = get_output(ts_restinv_disp_requestbl(h_bill_line._recid))
            t_h_bill_line.request_str = request_str
            amount_bill = amount_bill + h_bill_line.betrag


            ordered_item = Ordered_item()
            ordered_item_list.append(ordered_item)

            ordered_item.dept = t_h_bill_line.departement
            ordered_item.artnr = t_h_bill_line.artnr
            ordered_item.rec_id = t_h_bill_line.rec_id
            ordered_item.qty = t_h_bill_line.anzahl
            ordered_item.epreis = t_h_bill_line.epreis
            ordered_item.net_bet = t_h_bill_line.nettobetrag
            ordered_item.bill_date = t_h_bill_line.bill_datum
            ordered_item.betrag = t_h_bill_line.betrag

    else:

        for h_bill_line in db_session.query(H_bill_line).filter(
                (H_bill_line.rechnr == rechnr) &  (H_bill_line.departement == curr_dept)).all():
            t_h_bill_line = T_h_bill_line()
            t_h_bill_line_list.append(t_h_bill_line)

            buffer_copy(h_bill_line, t_h_bill_line)
            t_h_bill_line.rec_id = h_bill_line._recid


            show_submenu()
            request_str = get_output(ts_restinv_disp_requestbl(h_bill_line._recid))
            t_h_bill_line.request_str = request_str
            amount_bill = amount_bill + h_bill_line.betrag


            ordered_item = Ordered_item()
            ordered_item_list.append(ordered_item)

            ordered_item.dept = t_h_bill_line.departement
            ordered_item.artnr = t_h_bill_line.artnr
            ordered_item.rec_id = t_h_bill_line.rec_id
            ordered_item.qty = t_h_bill_line.anzahl
            ordered_item.epreis = t_h_bill_line.epreis
            ordered_item.net_bet = t_h_bill_line.nettobetrag
            ordered_item.bill_date = t_h_bill_line.bill_datum
            ordered_item.betrag = t_h_bill_line.betrag


    for ordered_item in query(ordered_item_list):
        t_h_service = 0
        t_h_mwst = 0
        t_h_mwst2 = 0
        h_service = 0
        h_mwst = 0
        service = 0
        mwst = 0

        h_artikel = db_session.query(H_artikel).filter(
                (H_artikel.departement == dept) &  (H_artikel.artnr == ordered_item.artnr) &  (H_artikel.artart == 0)).first()

        if h_artikel:

            if not servtax_use_foart:
                serv_code = h_artikel.service_code
                vat_code = h_artikel.mwst_code


            else:

                artikel = db_session.query(Artikel).filter(
                        (Artikel.artnr == h_Artikel.artnrfront) &  (Artikel.departement == h_Artikel.departement)).first()

                if artikel:
                    serv_code = artikel.service_code
                    vat_code = artikel.mwst_code

        if h_artikel:

            if ordered_item.artnr != f_discart:

                if serv_code != 0 and not incl_service:

                    htparam = db_session.query(Htparam).filter(
                            (Htparam.paramnr == serv_code)).first()

                    if htparam and htparam.fdecimal != 0:

                        if num_entries(htparam.fchar, chr(2)) >= 2:
                            t_h_service = decimal.Decimal(entry(1, htparam.fchar, chr(2))) / 10000


                        else:
                            t_h_service = htparam.fdecimal

                if vat_code != 0 and not incl_mwst:

                    htparam = db_session.query(Htparam).filter(
                            (Htparam.paramnr == vat_code)).first()

                    if htparam and htparam.fdecimal != 0:

                        if num_entries(htparam.fchar, chr(2)) >= 2:
                            t_h_mwst = decimal.Decimal(entry(1, htparam.fchar, chr(2))) / 10000


                        else:
                            t_h_mwst = htparam.fdecimal

                        if serv_vat and not tax_vat:
                            t_h_mwst = t_h_mwst + t_h_mwst * t_h_service / 100

                        elif serv_vat and tax_vat:
                            t_h_mwst = t_h_mwst + t_h_mwst * (t_h_service + t_h_mwst2) / 100

                        elif not serv_vat and tax_vat:
                            t_h_mwst = t_h_mwst + t_h_mwst * t_h_mwst2 / 100
                        ct = replace_str(to_string(t_h_mwst) , ".", ",")
                        l_deci = len(entry(1, ct, ","))

                        if l_deci <= 2:
                            t_h_mwst = round(t_h_mwst, 2)

                        elif l_deci == 3:
                            t_h_mwst = round(t_h_mwst, 3)
                        else:
                            t_h_mwst = round(t_h_mwst, 4)

                if t_h_service != 0 or t_h_mwst != 0:
                    t_h_service = t_h_service / 100
                    t_h_mwst = t_h_mwst / 100
                    t_h_mwst2 = t_h_mwst2 / 100


                    fact_scvat = 1 + t_h_service + t_h_mwst + t_h_mwst2
                    h_service = ordered_item.betrag / fact_scvat * t_h_service
                    h_service = round(h_service, 2)
                    h_mwst = ordered_item.betrag / fact_scvat * t_h_mwst
                    h_mwst = round(h_mwst, 2)

                    if not incl_service:
                        service = service + h_service

                    if not incl_mwst:
                        mwst = mwst + h_mwst
                        mwst1 = mwst1 + h_mwst
            else:

                if serv_code != 0 and not incl_service and serv_disc:

                    htparam = db_session.query(Htparam).filter(
                            (Htparam.paramnr == serv_code)).first()

                    if htparam and htparam.fdecimal != 0:

                        if num_entries(htparam.fchar, chr(2)) >= 2:
                            t_h_service = decimal.Decimal(entry(1, htparam.fchar, chr(2))) / 10000


                        else:
                            t_h_service = htparam.fdecimal

                if vat_code != 0 and not incl_mwst and vat_disc:

                    htparam = db_session.query(Htparam).filter(
                            (Htparam.paramnr == vat_code)).first()

                    if htparam and htparam.fdecimal != 0:

                        if num_entries(htparam.fchar, chr(2)) >= 2:
                            t_h_mwst = decimal.Decimal(entry(1, htparam.fchar, chr(2))) / 10000


                        else:
                            t_h_mwst = htparam.fdecimal

                        if serv_vat and not tax_vat:
                            t_h_mwst = t_h_mwst + t_h_mwst * t_h_service / 100

                        elif serv_vat and tax_vat:
                            t_h_mwst = t_h_mwst + t_h_mwst * (t_h_service + t_h_mwst2) / 100

                        elif not serv_vat and tax_vat:
                            t_h_mwst = t_h_mwst + t_h_mwst * t_h_mwst2 / 100
                        ct = replace_str(to_string(t_h_mwst) , ".", ",")
                        l_deci = len(entry(1, ct, ","))

                        if l_deci <= 2:
                            t_h_mwst = round(t_h_mwst, 2)

                        elif l_deci == 3:
                            t_h_mwst = round(t_h_mwst, 3)
                        else:
                            t_h_mwst = round(t_h_mwst, 4)

                if ordered_item.epreis != ordered_item.betrag:

                    if t_h_service != 0 or t_h_mwst != 0:
                        t_h_service = t_h_service / 100
                        t_h_mwst = t_h_mwst / 100
                        t_h_mwst2 = t_h_mwst2 / 100


                        fact_scvat = 1 + t_h_service + t_h_mwst + t_h_mwst2
                        h_service = ordered_item.betrag / fact_scvat * t_h_service
                        h_service = round(h_service, 2)
                        h_mwst = ordered_item.betrag / fact_scvat * t_h_mwst
                        h_mwst = round(h_mwst, 2)

                        if not incl_service:
                            service = service + h_service

                        if not incl_mwst:
                            mwst = mwst + h_mwst
                            mwst1 = mwst1 + h_mwst
            ordered_item.service = service
            ordered_item.tax = mwst

    for ordered_item in query(ordered_item_list):
        sub_tot = sub_tot + (ordered_item.epreis * ordered_item.qty)
        tot_serv = tot_serv + ordered_item.service
        tot_tax = tot_tax + ordered_item.tax
    grand_tot = sub_tot + tot_serv + tot_tax
    summary_bill = Summary_bill()
    summary_bill_list.append(summary_bill)

    summary_bill.subtotal = sub_tot
    summary_bill.total_service = tot_serv
    summary_bill.total_tax = tot_tax
    summary_bill.grand_total = round(grand_tot, 0)
    summary_bill.gt_not_round = grand_tot

    return generate_output()