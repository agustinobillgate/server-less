#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htplogic import htplogic
from models import H_bill, H_artikel, Hoteldpt, Htparam, Queasy, Artikel, H_journal

def ts_restinv_run_help_webbl(kpr_time:int, kpr_recid:int, bill_date:date, tischnr:int, curr_dept:int, amount:Decimal):

    prepare_cache ([Hoteldpt, Htparam, Queasy, Artikel, H_journal])

    fl_code = 0
    t_h_artikel1_data = []
    t_h_bill_data = []
    ct:string = ""
    l_deci:int = 2
    serv_vat:bool = False
    tax_vat:bool = False
    tax:Decimal = to_decimal("0.0")
    serv:Decimal = to_decimal("0.0")
    service:Decimal = to_decimal("0.0")
    vat:Decimal = to_decimal("0.0")
    vat2:Decimal = to_decimal("0.0")
    fact_scvat:Decimal = 1
    servtax_use_foart:bool = False
    service_foreign:Decimal = to_decimal("0.0")
    serv_code:int = 0
    vat_code:int = 0
    f_disc:int = 0
    b_disc:int = 0
    o_disc:int = 0
    price_decimal:int = 0
    curr_qty_posted:int = 0
    h_bill = h_artikel = hoteldpt = htparam = queasy = artikel = h_journal = None

    t_h_bill = t_h_artikel1 = None

    t_h_bill_data, T_h_bill = create_model_like(H_bill, {"rec_id":int})
    t_h_artikel1_data, T_h_artikel1 = create_model_like(H_artikel, {"rec_id":int, "amount_taxserv":Decimal, "max_soldout_qty":int, "soldout_flag":bool, "posted_qty":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal fl_code, t_h_artikel1_data, t_h_bill_data, ct, l_deci, serv_vat, tax_vat, tax, serv, service, vat, vat2, fact_scvat, servtax_use_foart, service_foreign, serv_code, vat_code, f_disc, b_disc, o_disc, price_decimal, curr_qty_posted, h_bill, h_artikel, hoteldpt, htparam, queasy, artikel, h_journal
        nonlocal kpr_time, kpr_recid, bill_date, tischnr, curr_dept, amount


        nonlocal t_h_bill, t_h_artikel1
        nonlocal t_h_bill_data, t_h_artikel1_data

        return {"kpr_time": kpr_time, "kpr_recid": kpr_recid, "fl_code": fl_code, "t-h-artikel1": t_h_artikel1_data, "t-h-bill": t_h_bill_data}


    hoteldpt = get_cache (Hoteldpt, {"num": [(eq, curr_dept)]})

    if hoteldpt:
        servtax_use_foart = hoteldpt.defult

    htparam = get_cache (Htparam, {"paramnr": [(eq, 557)]})

    if htparam and htparam.finteger != 0:
        f_disc = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 556)]})

    if htparam and htparam.finteger != 0:
        o_disc = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 596)]})

    if htparam and htparam.finteger != 0:
        b_disc = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})

    if htparam:
        price_decimal = htparam.finteger

    if (kpr_time - get_current_time_in_seconds()) >= 300:
        kpr_time = get_current_time_in_seconds()

    if kpr_recid == 0:

        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 3) & (Queasy.number1 != 0) & ((Queasy.char1 != "") | (Queasy.char3 != "")) & ((Queasy.date1 == bill_date))).first()

        if queasy:
            kpr_recid = to_int(queasy._recid)


        kpr_time = get_current_time_in_seconds()

    elif kpr_recid != 0 and (get_current_time_in_seconds() > (kpr_time + 30)):

        queasy = get_cache (Queasy, {"_recid": [(eq, kpr_recid)]})

        if queasy and queasy.number1 != 0:
            fl_code = 1
        kpr_recid = 0
        kpr_time = get_current_time_in_seconds()

    h_bill = get_cache (H_bill, {"tischnr": [(eq, tischnr)],"departement": [(eq, curr_dept)],"flag": [(eq, 0)]})

    if h_bill:
        t_h_bill = T_h_bill()
        t_h_bill_data.append(t_h_bill)

        buffer_copy(h_bill, t_h_bill)
        t_h_bill.rec_id = h_bill._recid

    for h_artikel in db_session.query(H_artikel).filter(
             (H_artikel.departement == curr_dept) & (H_artikel.activeflag)).order_by(H_artikel._recid).all():
        t_h_artikel1 = T_h_artikel1()
        t_h_artikel1_data.append(t_h_artikel1)

        buffer_copy(h_artikel, t_h_artikel1)
        t_h_artikel1.rec_id = h_artikel._recid


        fact_scvat =  to_decimal("1")
        service =  to_decimal("0")
        vat =  to_decimal("0")
        vat2 =  to_decimal("0")

        if servtax_use_foart:

            artikel = get_cache (Artikel, {"artnr": [(eq, h_artikel.artnrfront)],"departement": [(eq, h_artikel.departement)]})

            if artikel:
                serv_code = artikel.service_code
                vat_code = artikel.mwst_code


        else:
            serv_code = h_artikel.service_code
            vat_code = h_artikel.mwst_code

        htparam = get_cache (Htparam, {"paramnr": [(eq, 135)]})

        if not htparam.flogical and h_artikel.artart == 0 and serv_code != 0:

            htparam = get_cache (Htparam, {"paramnr": [(eq, serv_code)]})

            if htparam and htparam.fdecimal != 0:

                if num_entries(htparam.fchar, chr_unicode(2)) >= 2:
                    service =  to_decimal(to_decimal(entry(1 , htparam.fchar , chr_unicode(2)))) / to_decimal("10000")


                else:
                    service =  to_decimal(htparam.fdecimal)
        serv_vat = get_output(htplogic(479))
        tax_vat = get_output(htplogic(483))

        htparam = get_cache (Htparam, {"paramnr": [(eq, 134)]})

        if not htparam.flogical and h_artikel.artart == 0 and vat_code != 0:

            htparam = get_cache (Htparam, {"paramnr": [(eq, vat_code)]})

            if htparam and htparam.fdecimal != 0:

                if num_entries(htparam.fchar, chr_unicode(2)) >= 2:
                    vat =  to_decimal(to_decimal(entry(1 , htparam.fchar , chr_unicode(2)))) / to_decimal("10000")


                else:
                    vat =  to_decimal(htparam.fdecimal)

                if serv_vat and not tax_vat:
                    vat =  to_decimal(vat) + to_decimal(vat) * to_decimal(service) / to_decimal("100")

                elif serv_vat and tax_vat:
                    vat =  to_decimal(vat) + to_decimal(vat) * to_decimal((service) + to_decimal(vat2)) / to_decimal("100")

                elif not serv_vat and tax_vat:
                    vat =  to_decimal(vat) + to_decimal(vat) * to_decimal(vat2) / to_decimal("100")
                ct = replace_str(to_string(vat) , ".", ",")
                l_deci = length(entry(1, ct, ","))

                if l_deci <= 2:
                    vat = to_decimal(round(vat , 2))

                elif l_deci == 3:
                    vat = to_decimal(round(vat , 3))
                else:
                    vat = to_decimal(round(vat , 4))

        if h_artikel.artart == 0 and (h_artikel.artnr != f_disc or h_artikel.artnr != b_disc or h_artikel.artnr != o_disc):

            if serv_code != 0:
                service =  to_decimal(service) / to_decimal("100")

            if vat_code != 0:
                vat =  to_decimal(vat) / to_decimal("100")
                vat2 =  to_decimal(vat2) / to_decimal("100")


            fact_scvat =  to_decimal("1") + to_decimal(service) + to_decimal(vat) + to_decimal(vat2)

            if vat == 1:
                fact_scvat =  to_decimal("1")
                service =  to_decimal("0")
                vat2 =  to_decimal("0")

            elif vat2 == 1:
                fact_scvat =  to_decimal("1")
                service =  to_decimal("0")
                vat =  to_decimal("0")

            elif service == 1:
                fact_scvat =  to_decimal("1")
                vat =  to_decimal("0")
                vat2 =  to_decimal("0")


        t_h_artikel1.amount_taxserv =  to_decimal(h_artikel.epreis1) * to_decimal(fact_scvat)

        if price_decimal == 0:
            t_h_artikel1.amount_taxserv = to_decimal(round(t_h_artikel1.amount_taxserv , 0))
        else:
            t_h_artikel1.amount_taxserv = to_decimal(round(t_h_artikel1.amount_taxserv , 2))

        queasy = get_cache (Queasy, {"key": [(eq, 222)],"number1": [(eq, 2)],"number2": [(eq, h_artikel.artnr)],"number3": [(eq, h_artikel.departement)]})

        if queasy:
            t_h_artikel1.max_soldout_qty = to_int(queasy.deci1)
            t_h_artikel1.soldout_flag = queasy.logi2

        if t_h_artikel1.max_soldout_qty > 0:
            curr_qty_posted = 0

            for h_journal in db_session.query(H_journal).filter(
                     (H_journal.artnr == h_artikel.artnr) & (H_journal.departement == h_artikel.departement) & (H_journal.bill_datum == bill_date)).order_by(H_journal._recid).all():
                curr_qty_posted = curr_qty_posted + h_journal.anzahl
            t_h_artikel1.posted_qty = curr_qty_posted

    return generate_output()