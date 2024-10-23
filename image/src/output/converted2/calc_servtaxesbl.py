from functions.additional_functions import *
import decimal
from datetime import date
from functions.htpdate import htpdate
from functions.htplogic import htplogic
from models import Artikel, Htparam, Kontplan

def calc_servtaxesbl(i_case:int, inp_artno:int, inp_deptno:int, inp_date:date):
    service = to_decimal("0.0")
    vat = to_decimal("0.0")
    vat2 = to_decimal("0.0")
    fact_scvat = 1
    service_code:int = 0
    tax_code:int = 0
    vat_code:int = 0
    bill_date:date = None
    serv_vat:bool = False
    tax_vat:bool = False
    ct:str = ""
    l_deci:int = 2
    rm_serv:bool = False
    rm_vat:bool = False
    incl_service:bool = False
    incl_mwst:bool = False
    returnflag:bool = False
    artikel = htparam = kontplan = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal service, vat, vat2, fact_scvat, service_code, tax_code, vat_code, bill_date, serv_vat, tax_vat, ct, l_deci, rm_serv, rm_vat, incl_service, incl_mwst, returnflag, artikel, htparam, kontplan
        nonlocal i_case, inp_artno, inp_deptno, inp_date


        return {"service": service, "vat": vat, "vat2": vat2, "fact_scvat": fact_scvat}

    def calculate_it2():

        nonlocal service, vat, vat2, fact_scvat, service_code, tax_code, vat_code, bill_date, serv_vat, tax_vat, ct, l_deci, rm_serv, rm_vat, incl_service, incl_mwst, returnflag, artikel, htparam, kontplan
        nonlocal i_case, inp_artno, inp_deptno, inp_date

        kontplan = db_session.query(Kontplan).filter(
                 (Kontplan.betriebsnr == inp_deptno) & (Kontplan.kontignr == inp_artno) & (Kontplan.datum == inp_date)).first()

        if not kontplan:

            return

        if kontplan.anzkont >= 100000:
            service =  to_decimal(kontplan.anzkont) / to_decimal("10000000")
            vat =  to_decimal(kontplan.anzconf) / to_decimal("10000000")


        else:
            service =  to_decimal(kontplan.anzkont) / to_decimal("10000")
            vat =  to_decimal(kontplan.anzconf) / to_decimal("10000")

        kontplan = db_session.query(Kontplan).filter(
                 (Kontplan.betriebsnr == inp_deptno + 100) & (Kontplan.kontignr == inp_artno) & (Kontplan.datum == inp_date)).first()

        if kontplan:
            vat2 =  to_decimal(kontplan.anzconf) / to_decimal("10000000")

        if i_case == 2:

            if not rm_vat:
                vat =  to_decimal("0")
                vat2 =  to_decimal("0")

            if not rm_serv:
                service =  to_decimal("0")

        if i_case == 3:

            if not incl_mwst:
                vat =  to_decimal("0")
                vat2 =  to_decimal("0")

            if not incl_service:
                service =  to_decimal("0")


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


        returnflag = True

    artikel = db_session.query(Artikel).filter(
             (Artikel.artnr == inp_artno) & (Artikel.departement == inp_deptno)).first()

    if not artikel:

        return generate_output()
    service_code = artikel.service_code
    tax_code = artikel.prov_code
    vat_code = artikel.mwst_code


    bill_date = get_output(htpdate(110))
    serv_vat = get_output(htplogic(479))
    tax_vat = get_output(htplogic(483))
    rm_vat = get_output(htplogic(127))
    rm_serv = get_output(htplogic(128))
    incl_service = get_output(htplogic(135))
    incl_mwst = get_output(htplogic(134))

    if inp_date != None and inp_date < bill_date:
        calculate_it2()

        if returnflag:

            return generate_output()

    if service_code != 0:

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == service_code)).first()

        if htparam and htparam.fdecimal != 0:

            if num_entries(htparam.fchar, chr(2)) >= 2:
                service =  to_decimal(to_decimal(entry(1 , htparam.fchar , chr(2)))) / to_decimal("10000")


            else:
                service =  to_decimal(htparam.fdecimal)

    if tax_code != 0:

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == tax_code)).first()

        if htparam and htparam.fdecimal != 0:

            if num_entries(htparam.fchar, chr(2)) >= 2:
                vat2 =  to_decimal(to_decimal(entry(1 , htparam.fchar , chr(2)))) / to_decimal("10000")


            else:
                vat2 =  to_decimal(htparam.fdecimal)

            if serv_vat:
                vat2 =  to_decimal(vat2) + (to_decimal(vat2) * to_decimal(service)) / to_decimal("100")
            ct = replace_str(to_string(vat) , ".", ",")
            l_deci = len(entry(1, ct, ","))

            if l_deci <= 2:
                vat2 = to_decimal(round(vat2 , 2))

            elif l_deci == 3:
                vat2 = to_decimal(round(vat2 , 3))
            else:
                vat2 = to_decimal(round(vat2 , 4))

    if vat_code != 0:

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
    service =  to_decimal(service) / to_decimal("100")
    vat =  to_decimal(vat) / to_decimal("100")
    vat2 =  to_decimal(vat2) / to_decimal("100")

    if i_case == 2:

        if not rm_vat:
            vat =  to_decimal("0")
            vat2 =  to_decimal("0")

        if not rm_serv:
            service =  to_decimal("0")

    if i_case == 3:

        if not incl_mwst:
            vat =  to_decimal("0")
            vat2 =  to_decimal("0")

        if not incl_service:
            service =  to_decimal("0")


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