#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.ts_closeinv_cancel_orderbl import ts_closeinv_cancel_orderbl
from functions.htplogic import htplogic
from functions.ts_closeinv_calculate_amountbl import ts_closeinv_calculate_amountbl
from functions.ts_closeinv_updatebill_cldbl import ts_closeinv_updatebill_cldbl
from functions.ts_closeinv_create_logfilebl import ts_closeinv_create_logfilebl
from models import H_bill_line, H_artikel, Bediener, H_bill, Kellner, Htparam, Hoteldpt, Artikel

t_b_list_list, T_b_list = create_model_like(H_bill_line, {"rec_id":int})

def ts_closeinv_void_salesitembl(t_b_list_list:[T_b_list], language_code:int, v_type:int, bl_recid:int, rec_id:int, bill_no:int, curr_dept:int, tischnr:int, pax:int, price_decimal:int, curr_waiter:int, kreditlimit:Decimal, exchg_rate:Decimal, gname:string, user_init:string, cancel_str:string, double_currency:bool, foreign_rate:bool, balance:Decimal):

    prepare_cache ([H_artikel, Htparam, Hoteldpt, Artikel])

    mess_result = ""
    v_success = False
    t_void_list_list = []
    summary_bill_list = []
    vcorrect:bool = False
    cancel_flag:bool = False
    answer:bool = False
    zugriff:bool = False
    fl_code:int = 0
    fl_code1:int = 0
    fl_code2:int = 0
    fl_code3:int = 0
    sales_art:int = 0
    rec_id_h_art:int = 0
    anz:int = 0
    total_qty:int = 0
    hoga_resnr:int = 0
    hoga_reslinnr:int = 0
    qty:int = 0
    f_disc:int = 0
    b_disc:int = 0
    o_disc:int = 0
    rechnr:int = 0
    bcol:int = 0
    add_second:int = 0
    ci_date:date = None
    bill_date:date = None
    description:string = ""
    msg_str:string = ""
    printed:string = ""
    deptname:string = ""
    price:Decimal = to_decimal("0.0")
    do_it:bool = True
    s:string = ""
    f_log:bool = False
    p_88:bool = False
    closed:bool = False
    mwst_sales:Decimal = to_decimal("0.0")
    mwst_foreign_sales:Decimal = to_decimal("0.0")
    balance_sales:Decimal = to_decimal("0.0")
    balance_foreign_sales:Decimal = to_decimal("0.0")
    amount_foreign:Decimal = to_decimal("0.0")
    amount:Decimal = to_decimal("0.0")
    netto_betrag:Decimal = to_decimal("0.0")
    rec_id_artikel:int = 0
    service_code:int = 0
    h_bill_line = h_artikel = bediener = h_bill = kellner = htparam = hoteldpt = artikel = None

    t_b_list = ordered_item = t_void_list = t_h_artsales = b_list = tmp_hartikel = tp_bediener = submenu_list = t_h_bill = t_kellner1 = summary_bill = None

    ordered_item_list, Ordered_item = create_model_like(H_bill_line, {"rec_id":int, "tax":Decimal, "service":Decimal})
    t_void_list_list, T_void_list = create_model_like(H_bill_line, {"rec_id":int})
    t_h_artsales_list, T_h_artsales = create_model_like(H_artikel, {"rec_id":int})
    b_list_list, B_list = create_model_like(H_bill_line, {"rec_id":int})
    tmp_hartikel_list, Tmp_hartikel = create_model_like(H_artikel, {"rec_id":int})
    tp_bediener_list, Tp_bediener = create_model_like(Bediener)
    submenu_list_list, Submenu_list = create_model("Submenu_list", {"menurecid":int, "zeit":int, "nr":int, "artnr":int, "bezeich":string, "anzahl":int, "zknr":int, "request":string})
    t_h_bill_list, T_h_bill = create_model_like(H_bill, {"rec_id":int})
    t_kellner1_list, T_kellner1 = create_model_like(Kellner)
    summary_bill_list, Summary_bill = create_model("Summary_bill", {"subtotal":Decimal, "total_service":Decimal, "total_tax":Decimal, "grand_total":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal mess_result, v_success, t_void_list_list, summary_bill_list, vcorrect, cancel_flag, answer, zugriff, fl_code, fl_code1, fl_code2, fl_code3, sales_art, rec_id_h_art, anz, total_qty, hoga_resnr, hoga_reslinnr, qty, f_disc, b_disc, o_disc, rechnr, bcol, add_second, ci_date, bill_date, description, msg_str, printed, deptname, price, do_it, s, f_log, p_88, closed, mwst_sales, mwst_foreign_sales, balance_sales, balance_foreign_sales, amount_foreign, amount, netto_betrag, rec_id_artikel, service_code, h_bill_line, h_artikel, bediener, h_bill, kellner, htparam, hoteldpt, artikel
        nonlocal language_code, v_type, bl_recid, rec_id, bill_no, curr_dept, tischnr, pax, price_decimal, curr_waiter, kreditlimit, exchg_rate, gname, user_init, cancel_str, double_currency, foreign_rate, balance


        nonlocal t_b_list, ordered_item, t_void_list, t_h_artsales, b_list, tmp_hartikel, tp_bediener, submenu_list, t_h_bill, t_kellner1, summary_bill
        nonlocal ordered_item_list, t_void_list_list, t_h_artsales_list, b_list_list, tmp_hartikel_list, tp_bediener_list, submenu_list_list, t_h_bill_list, t_kellner1_list, summary_bill_list

        return {"balance": balance, "mess_result": mess_result, "v_success": v_success, "t-void-list": t_void_list_list, "summary-bill": summary_bill_list}

    def check_permission(user_init:string, array_nr:int, expected_nr:int):

        nonlocal mess_result, v_success, t_void_list_list, summary_bill_list, vcorrect, cancel_flag, answer, zugriff, fl_code, fl_code1, fl_code2, fl_code3, sales_art, rec_id_h_art, total_qty, hoga_resnr, hoga_reslinnr, qty, f_disc, b_disc, o_disc, rechnr, bcol, add_second, ci_date, bill_date, description, msg_str, printed, deptname, price, do_it, s, f_log, p_88, closed, mwst_sales, mwst_foreign_sales, balance_sales, balance_foreign_sales, amount_foreign, amount, netto_betrag, rec_id_artikel, service_code, h_bill_line, h_artikel, bediener, h_bill, kellner, htparam, hoteldpt, artikel
        nonlocal language_code, v_type, bl_recid, rec_id, bill_no, curr_dept, tischnr, pax, price_decimal, curr_waiter, kreditlimit, exchg_rate, gname, cancel_str, double_currency, foreign_rate, balance


        nonlocal t_b_list, ordered_item, t_void_list, t_h_artsales, b_list, tmp_hartikel, tp_bediener, submenu_list, t_h_bill, t_kellner1, summary_bill
        nonlocal ordered_item_list, t_void_list_list, t_h_artsales_list, b_list_list, tmp_hartikel_list, tp_bediener_list, submenu_list_list, t_h_bill_list, t_kellner1_list, summary_bill_list

        zugriff = True
        msg_str = ""
        mail_exist:bool = False
        logical_flag:bool = False
        n:int = 0
        perm:List[int] = create_empty_list(120,0)
        s1:string = ""
        s2:string = ""
        mn_date:date = None
        anz:int = 0

        def generate_inner_output():
            return (zugriff, msg_str)


        if user_init == "":
            zugriff = False
            msg_str = "User not defined."

            return generate_inner_output()
        else:
            tp_bediener_list.clear()

            bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

            if bediener:
                tp_bediener = Tp_bediener()
                tp_bediener_list.append(tp_bediener)

                buffer_copy(bediener, tp_bediener)
            else:
                zugriff = False
                msg_str = "User not found."

                return generate_inner_output()
            for n in range(1,length(tp_bediener.permissions)  + 1) :
                perm[n - 1] = to_int(substring(tp_bediener.permissions, n - 1, 1))

            if perm[array_nr - 1] < expected_nr:
                zugriff = False
                s1 = to_string(array_nr, "999")
                s2 = to_string(expected_nr)
                msg_str = "Sorry, No Access Right, Access Code = " + s1 + s2

        return generate_inner_output()


    def recalculate_summarybill():

        nonlocal mess_result, v_success, t_void_list_list, summary_bill_list, vcorrect, cancel_flag, answer, zugriff, fl_code, fl_code1, fl_code2, fl_code3, sales_art, rec_id_h_art, anz, total_qty, hoga_resnr, hoga_reslinnr, qty, f_disc, b_disc, o_disc, rechnr, bcol, add_second, ci_date, bill_date, description, msg_str, printed, deptname, price, do_it, s, f_log, p_88, closed, mwst_sales, mwst_foreign_sales, balance_sales, balance_foreign_sales, amount_foreign, netto_betrag, rec_id_artikel, service_code, h_bill_line, h_artikel, bediener, h_bill, kellner, htparam, hoteldpt, artikel
        nonlocal language_code, v_type, bl_recid, rec_id, bill_no, curr_dept, tischnr, pax, price_decimal, curr_waiter, kreditlimit, exchg_rate, gname, user_init, cancel_str, double_currency, foreign_rate, balance


        nonlocal t_b_list, ordered_item, t_void_list, t_h_artsales, b_list, tmp_hartikel, tp_bediener, submenu_list, t_h_bill, t_kellner1, summary_bill
        nonlocal ordered_item_list, t_void_list_list, t_h_artsales_list, b_list_list, tmp_hartikel_list, tp_bediener_list, submenu_list_list, t_h_bill_list, t_kellner1_list, summary_bill_list

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
        compli_flag:bool = False
        buff_hart = None
        Buff_hart =  create_buffer("Buff_hart",H_artikel)

        hoteldpt = get_cache (Hoteldpt, {"num": [(eq, curr_dept)]})

        if hoteldpt:
            servtax_use_foart = hoteldpt.defult

        htparam = get_cache (Htparam, {"paramnr": [(eq, 468)]})

        if htparam:
            serv_disc = htparam.flogical

        htparam = get_cache (Htparam, {"paramnr": [(eq, 469)]})

        if htparam:
            vat_disc = htparam.flogical

        htparam = get_cache (Htparam, {"paramnr": [(eq, 135)]})
        incl_service = htparam.flogical

        htparam = get_cache (Htparam, {"paramnr": [(eq, 134)]})
        incl_mwst = htparam.flogical
        serv_vat = get_output(htplogic(479))
        tax_vat = get_output(htplogic(483))

        for t_b_list in query(t_b_list_list):
            ordered_item = Ordered_item()
            ordered_item_list.append(ordered_item)

            buffer_copy(t_b_list, ordered_item)

        for ordered_item in query(ordered_item_list, filters=(lambda ordered_item: ordered_item.rec_id == bl_recid)):
            t_h_service =  to_decimal("0")
            t_h_mwst =  to_decimal("0")
            t_h_mwst2 =  to_decimal("0")
            h_service =  to_decimal("0")
            h_mwst =  to_decimal("0")
            service =  to_decimal("0")
            mwst =  to_decimal("0")

            h_artikel = get_cache (H_artikel, {"departement": [(eq, ordered_item.departement)],"artnr": [(eq, ordered_item.artnr)],"artart": [(eq, 0)]})

            if h_artikel:
                netto_bet =  to_decimal(netto_bet) + to_decimal((ordered_item.epreis) * to_decimal(ordered_item.anzahl))

                if not servtax_use_foart:
                    serv_code = h_artikel.service_code
                    vat_code = h_artikel.mwst_code


                else:

                    artikel = get_cache (Artikel, {"artnr": [(eq, h_artikel.artnrfront)],"departement": [(eq, h_artikel.departement)]})

                    if artikel:
                        serv_code = artikel.service_code
                        vat_code = artikel.mwst_code

            if h_artikel:

                if ordered_item.artnr != f_disc:

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

        buff_hart_obj_list = {}
        for buff_hart in db_session.query(Buff_hart).filter(
                 ((Buff_hart.artnr.in_(list(set([ordered_item.artnr for ordered_item in ordered_item_list])))) & (Buff_hart.departement == ordered_item.departement))).order_by(Buff_hart._recid).all():
            if buff_hart_obj_list.get(buff_hart._recid):
                continue
            else:
                buff_hart_obj_list[buff_hart._recid] = True


            sub_tot =  to_decimal(netto_bet)
            tot_serv =  to_decimal(tot_serv) + to_decimal(ordered_item.service)
            tot_tax =  to_decimal(tot_tax) + to_decimal(ordered_item.tax)

            if buff_hart.artart == 11 or buff_hart.artart == 12:
                compli_flag = True

        if compli_flag:
            tot_serv =  to_decimal("0")
            tot_tax =  to_decimal("0")
        grand_tot =  to_decimal(sub_tot) + to_decimal(tot_serv) + to_decimal(tot_tax)
        summary_bill = Summary_bill()
        summary_bill_list.append(summary_bill)

        summary_bill.subtotal =  to_decimal(sub_tot)
        summary_bill.total_service =  to_decimal(tot_serv)
        summary_bill.total_tax =  to_decimal(tot_tax)
        summary_bill.grand_total =  to_decimal(grand_tot)


    htparam = get_cache (Htparam, {"paramnr": [(eq, 557)]})
    f_disc = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 596)]})
    b_disc = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 556)]})
    o_disc = htparam.finteger

    for h_artikel in db_session.query(H_artikel).filter(
             (H_artikel.departement == curr_dept) & (H_artikel.artart == 0)).order_by(H_artikel._recid).all():
        t_h_artsales = T_h_artsales()
        t_h_artsales_list.append(t_h_artsales)

        buffer_copy(h_artikel, t_h_artsales)
        t_h_artsales.rec_id = to_int(h_artikel._recid)

    hoteldpt = get_cache (Hoteldpt, {"num": [(eq, curr_dept)]})

    if hoteldpt:
        deptname = hoteldpt.depart

    t_b_list = query(t_b_list_list, first=True)

    if not t_b_list:
        mess_result = "01-No Data Available."

        return generate_output()

    for t_b_list in query(t_b_list_list, filters=(lambda t_b_list: t_b_list.rec_id == bl_recid)):
        b_list = B_list()
        b_list_list.append(b_list)

        buffer_copy(t_b_list, b_list)

    if v_type == 1:

        b_list = query(b_list_list, first=True)

        t_h_artsales = query(t_h_artsales_list, filters=(lambda t_h_artsales: t_h_artsales.artnr == b_list.artnr and t_h_artsales.departement == b_list.departement and b_list.anzahl > 0), first=True)

        if t_h_artsales and balance != 0:

            t_b_list = query(t_b_list_list, filters=(lambda t_b_list: t_b_list.artnr == f_disc or t_b_list.artnr == b_disc or t_b_list.artnr == o_disc), first=True)

            if t_b_list:
                mess_result = "02-Bill have discount article, deleteing not possible."

                return generate_output()
        else:
            mess_result = "03-balance not zero or article sales not available."

            return generate_output()
        v_success = True

    elif v_type == 2:
        fl_code, fl_code1, fl_code2, qty, answer, cancel_flag, sales_art, description, price, rec_id_h_art, anz, tmp_hartikel_list = get_output(ts_closeinv_cancel_orderbl(bl_recid))

        tmp_hartikel = query(tmp_hartikel_list, first=True)

        if fl_code == 1:
            mess_result = "04-qty is zero. Cancel not possible."

            return generate_output()

        if qty < 0 and tmp_hartikel.artart == 0:
            f_log = get_output(htplogic(261))

            if f_log:
                zugriff, msg_str = check_permission(user_init, 52, 2)

                if not zugriff:
                    mess_result = "05-" + msg_str

                    return generate_output()

        if tmp_hartikel.artart != 0:
            do_it = False

        if qty == 0 or sales_art == 0:
            do_it = False

        if qty != 0:

            if price != 0:
                price, amount_foreign, amount, fl_code, fl_code1 = get_output(ts_closeinv_calculate_amountbl(1, tmp_hartikel.rec_id, double_currency, price, qty, exchg_rate, price_decimal, None, cancel_flag, foreign_rate, curr_dept))
                netto_betrag =  to_decimal(amount)

                if fl_code1 == 1:
                    zugriff, msg_str = check_permission(user_init, 52, 2)

                    if not zugriff:
                        mess_result = "05-" + msg_str

                        return generate_output()

                if price != 0 and amount == 0:
                    mess_result = "06-amount is zero. Posting not possible."

                if tmp_hartikel.artart == 0 and qty < 0:

                    if cancel_str == "":
                        cancel_flag = False
                        do_it = False

                if do_it:

                    if not tmp_hartikel.autosaldo:
                        printed = ""

                    if tmp_hartikel.artart == 0:
                        zugriff, msg_str = check_permission(user_init, 19, 2)

                        if not zugriff:
                            mess_result = "05-" + msg_str

                            return generate_output()
                    else:
                        zugriff, msg_str = check_permission(user_init, 20, 2)

                        if not zugriff:
                            mess_result = "05-" + msg_str

                            return generate_output()

                    if zugriff:

                        if not tmp_hartikel:
                            rec_id_artikel = 0
                            service_code = 0
                        else:
                            rec_id_artikel = tmp_hartikel.rec_id
                            service_code = tmp_hartikel.service_code
                        bill_date, cancel_flag, fl_code, mwst_sales, mwst_foreign_sales, rechnr, balance_sales, bcol, balance_foreign_sales, fl_code1, fl_code2, fl_code3, p_88, closed, t_h_bill_list, t_kellner1_list = get_output(ts_closeinv_updatebill_cldbl(language_code, rec_id, rec_id_artikel, deptname, None, tmp_hartikel.artart, False, service_code, amount, amount_foreign, price, double_currency, qty, exchg_rate, price_decimal, 0, tischnr, curr_dept, curr_waiter, gname, pax, kreditlimit, 1, sales_art, description, "", "", cancel_str, "", "", "", False, False, tmp_hartikel.artnrfront, 0, 0, "", False, foreign_rate, "", user_init, hoga_resnr, hoga_reslinnr, False, 0, "", submenu_list_list))

                        t_h_bill = query(t_h_bill_list, first=True)

                        t_kellner1 = query(t_kellner1_list, first=True)

                    if fl_code == 2:
                        mess_result = "08-Occupied Table. Posting not possible."

                        return generate_output()
                    price, amount_foreign, amount, fl_code, fl_code1 = get_output(ts_closeinv_calculate_amountbl(2, tmp_hartikel.rec_id, double_currency, price, qty, exchg_rate, price_decimal, None, cancel_flag, foreign_rate, curr_dept))
                    get_output(ts_closeinv_create_logfilebl(user_init, bl_recid))
                    t_void_list = T_void_list()
                    t_void_list_list.append(t_void_list)

                    add_second = add_second + 1
                    t_void_list.rechnr = t_h_bill.rechnr
                    t_void_list.artnr = sales_art
                    t_void_list.bezeich = description
                    t_void_list.anzahl = qty
                    t_void_list.nettobetrag =  to_decimal(netto_betrag)
                    t_void_list.fremdwbetrag =  to_decimal(amount_foreign)
                    t_void_list.betrag =  to_decimal(amount)
                    t_void_list.tischnr = tischnr
                    t_void_list.departement = curr_dept
                    t_void_list.epreis =  to_decimal(price)
                    t_void_list.zeit = get_current_time_in_seconds() + add_second
                    t_void_list.bill_datum = bill_date
                    t_void_list.sysdate = get_current_date()


                    balance =  to_decimal(balance) + to_decimal(amount)
                    recalculate_summarybill()
        v_success = True

    return generate_output()