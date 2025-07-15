from functions.additional_functions import *
import decimal
from datetime import date
from functions.htplogic import htplogic
from models import H_artikel, Artikel, Waehrung, Exrate, Htparam, Hoteldpt

def ts_closeinv_calculate_amountbl(case_type:int, rec_id:int, double_currency:bool, price:decimal, qty:int, exchg_rate:decimal, price_decimal:int, transdate:date, cancel_flag:bool, foreign_rate:bool, curr_dept:int):
    amount_foreign = to_decimal("0.0")
    amount = to_decimal("0.0")
    fl_code = 0
    fl_code1 = 0
    h_artikel = artikel = waehrung = exrate = htparam = hoteldpt = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal amount_foreign, amount, fl_code, fl_code1, h_artikel, artikel, waehrung, exrate, htparam, hoteldpt
        nonlocal case_type, rec_id, double_currency, price, qty, exchg_rate, price_decimal, transdate, cancel_flag, foreign_rate, curr_dept


        return {"price": price, "amount_foreign": amount_foreign, "amount": amount, "fl_code": fl_code, "fl_code1": fl_code1}

    def calculate_amount():

        nonlocal amount_foreign, amount, fl_code, fl_code1, h_artikel, artikel, waehrung, exrate, htparam, hoteldpt
        nonlocal case_type, rec_id, double_currency, price, qty, exchg_rate, price_decimal, transdate, cancel_flag, foreign_rate, curr_dept

        avrg_kurs:decimal = 1
        rate_defined:bool = False
        answer:bool = False
        artikel1 = None
        w1 = None
        Artikel1 =  create_buffer("Artikel1",Artikel)
        W1 =  create_buffer("W1",Waehrung)

        if double_currency:
            amount_foreign =  to_decimal(price) * to_decimal(qty)
            amount =  to_decimal(price) * to_decimal(exchg_rate) * to_decimal(qty)
            amount = to_decimal(round(amount , price_decimal))


        else:

            if h_artikel.artart == 0:

                artikel1 = db_session.query(Artikel1).filter(
                         (Artikel1.artnr == h_artikel.artnrfront) & (Artikel1.departement == h_artikel.departement)).first()

                if artikel1 and artikel1.pricetab and artikel1.betriebsnr != 0:

                    if transdate != None:

                        exrate = db_session.query(Exrate).filter(
                                 (Exrate.artnr == artikel1.betriebsnr) & (Exrate.datum == transdate)).first()

                        if exrate:
                            rate_defined = True
                            avrg_kurs =  to_decimal(exrate.betrag)

                    if not rate_defined:

                        w1 = db_session.query(W1).filter(
                                 (W1.waehrungsnr == artikel1.betriebsnr) & (W1.ankauf != 0)).first()

                        if w1:
                            avrg_kurs =  to_decimal(w1.ankauf) / to_decimal(w1.einheit)
                        else:
                            avrg_kurs =  to_decimal(exchg_rate)
                    else:
                        avrg_kurs =  to_decimal(exchg_rate)
                else:
                    avrg_kurs =  to_decimal(exchg_rate)

                if artikel1.pricetab and not cancel_flag:
                    amount_foreign =  to_decimal(price) * to_decimal(qty)
                    price =  to_decimal(price) * to_decimal(avrg_kurs)
                    amount =  to_decimal(price) * to_decimal(qty)
                    amount = to_decimal(round(amount , price_decimal))
                else:
                    amount =  to_decimal(price) * to_decimal(qty)

                    if foreign_rate:
                        amount_foreign = to_decimal(round(amount / exchg_rate , 2))
                    amount = to_decimal(round(amount , price_decimal))
            else:
                amount =  to_decimal(price) * to_decimal(qty)
                amount = to_decimal(round(amount , price_decimal))

        if (amount > 99999999) or (amount < -99999999):
            fl_code = 1

        if amount < 0 and h_artikel.artart == 0:

            htparam = db_session.query(Htparam).filter(
                     (Htparam.paramnr == 261)).first()

            if htparam.flogical:
                fl_code1 = 1


    def calculate_amount2():

        nonlocal amount_foreign, amount, fl_code, fl_code1, h_artikel, artikel, waehrung, exrate, htparam, hoteldpt
        nonlocal case_type, rec_id, double_currency, price, qty, exchg_rate, price_decimal, transdate, cancel_flag, foreign_rate, curr_dept

        service:decimal = to_decimal("0.0")
        service_foreign:decimal = to_decimal("0.0")
        serv_code:int = 0
        vat_code:int = 0
        servtax_use_foart:bool = False
        serv_vat:bool = False
        ct:str = ""
        l_deci:int = 2
        vat:decimal = to_decimal("0.0")
        vat2:decimal = to_decimal("0.0")
        tax_vat:bool = False
        fact_scvat:decimal = 1
        unit_price:decimal = to_decimal("0.0")
        tax:decimal = to_decimal("0.0")
        serv:decimal = to_decimal("0.0")
        h_service:decimal = to_decimal("0.0")
        h_mwst:decimal = to_decimal("0.0")
        mwst:decimal = to_decimal("0.0")
        mwst_foreign:decimal = to_decimal("0.0")
        h_mwst_foreign:decimal = to_decimal("0.0")
        h_service_foreign:decimal = to_decimal("0.0")

        hoteldpt = db_session.query(Hoteldpt).filter(
                 (Hoteldpt.num == curr_dept)).first()

        if hoteldpt:
            servtax_use_foart = hoteldpt.defult

        if h_artikel:

            if servtax_use_foart:

                artikel = db_session.query(Artikel).filter(
                         (Artikel.artnr == h_artikel.artnrfront) & (Artikel.departement == h_artikel.departement)).first()

                if artikel:
                    serv_code = artikel.service_code
                    vat_code = artikel.mwst_code


            else:
                serv_code = h_artikel.service_code
                vat_code = h_artikel.mwst_code

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 135)).first()

        if not htparam.flogical and h_artikel.artart == 0 and h_artikel and serv_code != 0:

            htparam = db_session.query(Htparam).filter(
                     (Htparam.paramnr == serv_code)).first()

            if htparam and htparam.fdecimal != 0:

                if num_entries(htparam.fchar, chr(2)) >= 2:
                    service =  to_decimal(to_decimal(entry(1 , htparam.fchar , chr(2)))) / to_decimal("10000")


                else:
                    service =  to_decimal(htparam.fdecimal)
        serv_vat = get_output(htplogic(479))
        tax_vat = get_output(htplogic(483))

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 134)).first()

        if not htparam.flogical and h_artikel.artart == 0 and vat_code != 0:

            htparam = db_session.query(Htparam).filter(
                     (Htparam.paramnr == vat_code)).first()

            if htparam and htparam.fdecimal != 0:

                if num_entries(htparam.fchar, chr(2)) >= 2:
                    vat =  to_decimal(to_decimal(entry(1 , htparam.fchar , chr(2)))) / to_decimal("10000")


                else:
                    vat =  to_decimal(htparam.fdecimal)

                if serv_vat and not tax_vat:
                    vat =  to_decimal(vat) + to_decimal(vat) * to_decimal(service) / to_decimal("100")

                elif serv_vat and tax_vat:
                    vat =  to_decimal(vat) + to_decimal(vat) * to_decimal((service) + to_decimal(vat2)) / to_decimal("100")

                elif not serv_vat and tax_vat:
                    vat =  to_decimal(vat) + to_decimal(vat) * to_decimal(vat2) / to_decimal("100")
                ct = replace_str(to_string(vat) , ".", ",")
                l_deci = len(entry(1, ct, ","))

                if l_deci <= 2:
                    vat = to_decimal(round(vat , 2))

                elif l_deci == 3:
                    vat = to_decimal(round(vat , 3))
                else:
                    vat = to_decimal(round(vat , 4))

        if h_artikel.artart == 0:
            service =  to_decimal(service) / to_decimal("100")
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


            tax =  to_decimal(vat) + to_decimal(vat2)

            htparam = db_session.query(Htparam).filter(
                     (Htparam.paramnr == 135)).first()

            if htparam.flogical:
                service =  to_decimal("0")

            htparam = db_session.query(Htparam).filter(
                     (Htparam.paramnr == 134)).first()

            if htparam.flogical:
                tax =  to_decimal("0")
            h_service =  to_decimal(unit_price) * to_decimal(service)

            if double_currency:
                h_service_foreign = to_decimal(round(h_service , 4))
                h_service = to_decimal(round(h_service * exchg_rate , 4))
                service_foreign =  to_decimal(service_foreign) + to_decimal(h_service_foreign) * to_decimal(qty)


            h_service = to_decimal(round(h_service , 4))
            service =  to_decimal(service) + to_decimal(h_service) * to_decimal(qty)


            h_mwst =  to_decimal(unit_price) * to_decimal(tax)

            if double_currency:
                h_mwst_foreign = to_decimal(round(h_mwst , 4))
                h_mwst =  to_decimal(tax) * to_decimal(unit_price) * to_decimal(exchg_rate)
                h_mwst = to_decimal(round(h_mwst , 4))


            else:
                h_mwst_foreign = to_decimal(round(h_mwst / exchg_rate , 4))
                h_mwst = to_decimal(round(h_mwst , 4))


            mwst =  to_decimal(mwst) + to_decimal(h_mwst) * to_decimal(qty)
            mwst_foreign =  to_decimal(mwst_foreign) + to_decimal(h_mwst_foreign) * to_decimal(qty)


        unit_price =  to_decimal(price) * to_decimal(fact_scvat)
        amount =  to_decimal(unit_price) * to_decimal(qty)
        amount = to_decimal(round(amount , price_decimal))

    h_artikel = db_session.query(H_artikel).filter(
             (H_artikel._recid == rec_id)).first()

    if case_type == 1:
        calculate_amount()

    elif case_type == 2:
        calculate_amount2()

    return generate_output()