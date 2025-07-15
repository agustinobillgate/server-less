from functions.additional_functions import *
import decimal
from functions.htplogic import htplogic
from models import Hoteldpt, H_artikel, Artikel, Htparam

def ts_hbline_get_taxservicebl(art_no:int, dept_no:int):
    fact_scvat = 1
    ct:str = ""
    l_deci:int = 2
    serv_vat:bool = False
    tax_vat:bool = False
    tax:decimal = to_decimal("0.0")
    serv:decimal = to_decimal("0.0")
    service:decimal = to_decimal("0.0")
    vat:decimal = to_decimal("0.0")
    vat2:decimal = to_decimal("0.0")
    servtax_use_foart:bool = False
    service_foreign:decimal = to_decimal("0.0")
    serv_code:int = 0
    vat_code:int = 0
    hoteldpt = h_artikel = artikel = htparam = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal fact_scvat, ct, l_deci, serv_vat, tax_vat, tax, serv, service, vat, vat2, servtax_use_foart, service_foreign, serv_code, vat_code, hoteldpt, h_artikel, artikel, htparam
        nonlocal art_no, dept_no


        return {"fact_scvat": fact_scvat}


    hoteldpt = db_session.query(Hoteldpt).filter(
             (Hoteldpt.num == dept_no)).first()

    if hoteldpt:
        servtax_use_foart = hoteldpt.defult

    h_artikel = db_session.query(H_artikel).filter(
             (H_artikel.departement == dept_no) & (H_artikel.artnr == art_no) & (H_artikel.artart == 0) & (H_artikel.activeflag)).first()

    if h_artikel:
        service =  to_decimal("0")
        vat =  to_decimal("0")
        vat2 =  to_decimal("0")

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

        if not htparam.flogical and h_artikel.artart == 0 and serv_code != 0:

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

    return generate_output()