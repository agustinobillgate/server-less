#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from functions.calc_servtaxesbl import calc_servtaxesbl
from models import Htparam, H_bill, H_bill_line, H_artikel, Artikel

def odx_sum_billbl(rechnr:int, dept:int):

    prepare_cache ([Htparam, H_bill, H_bill_line, H_artikel, Artikel])

    summary_bill_list = []
    vat:Decimal = to_decimal("0.0")
    vat2:Decimal = to_decimal("0.0")
    service:Decimal = to_decimal("0.0")
    fact:Decimal = to_decimal("0.0")
    netto:Decimal = to_decimal("0.0")
    t_service:int = 0
    discfood_artnr:int = 0
    discoth_artnr:int = 0
    discbev_artnr:int = 0
    htparam = h_bill = h_bill_line = h_artikel = artikel = None

    summary_bill = None

    summary_bill_list, Summary_bill = create_model("Summary_bill", {"department":int, "tableno":int, "rechnr":int, "pax":int, "total_food":Decimal, "total_bev":Decimal, "total_other":Decimal, "total_service":Decimal, "total_tax":Decimal, "total_disc":Decimal, "total_tips":Decimal, "total_amount":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal summary_bill_list, vat, vat2, service, fact, netto, t_service, discfood_artnr, discoth_artnr, discbev_artnr, htparam, h_bill, h_bill_line, h_artikel, artikel
        nonlocal rechnr, dept


        nonlocal summary_bill
        nonlocal summary_bill_list

        return {"summary-bill": summary_bill_list}

    htparam = get_cache (Htparam, {"paramnr": [(eq, 556)]})
    discoth_artnr = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 557)]})
    discfood_artnr = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 559)]})
    discbev_artnr = htparam.finteger

    h_bill = get_cache (H_bill, {"departement": [(eq, dept)],"rechnr": [(eq, rechnr)]})

    if h_bill:
        summary_bill = Summary_bill()
        summary_bill_list.append(summary_bill)

        summary_bill.department = h_bill.departement
        summary_bill.tableno = h_bill.tischnr
        summary_bill.rechnr = h_bill.rechnr
        summary_bill.pax = h_bill.belegung

        for h_bill_line in db_session.query(H_bill_line).filter(
                 (H_bill_line.rechnr == rechnr) & (H_bill_line.departement == dept)).order_by(H_bill_line._recid).all():

            h_artikel = get_cache (H_artikel, {"departement": [(eq, dept)],"artnr": [(eq, h_bill_line.artnr)],"artart": [(eq, 0)]})

            if h_artikel:

                if h_artikel.artnr == discfood_artnr:
                    summary_bill.total_disc =  to_decimal(summary_bill.total_disc) + to_decimal((h_bill_line.epreis) * to_decimal(h_bill_line.anzahl))

                elif h_artikel.artnr == discbev_artnr:
                    summary_bill.total_disc =  to_decimal(summary_bill.total_disc) + to_decimal((h_bill_line.epreis) * to_decimal(h_bill_line.anzahl))

                elif h_artikel.artnr == discoth_artnr:
                    summary_bill.total_disc =  to_decimal(summary_bill.total_disc) + to_decimal((h_bill_line.epreis) * to_decimal(h_bill_line.anzahl))
                else:

                    if h_artikel.artnrfront == 10:
                        summary_bill.total_food =  to_decimal(summary_bill.total_food) + to_decimal((h_artikel.epreis1) * to_decimal(h_bill_line.anzahl))

                    elif h_artikel.artnrfront == 11:
                        summary_bill.total_bev =  to_decimal(summary_bill.total_bev) + to_decimal((h_artikel.epreis1) * to_decimal(h_bill_line.anzahl))
                    else:
                        summary_bill.total_other =  to_decimal(summary_bill.total_other) + to_decimal((h_artikel.epreis1) * to_decimal(h_bill_line.anzahl))

                artikel = get_cache (Artikel, {"departement": [(eq, h_artikel.departement)],"artnr": [(eq, h_artikel.artnrfront)]})

                if artikel:
                    service, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, h_bill_line.bill_datum))
                    netto =  to_decimal(h_bill_line.betrag) / to_decimal((1) + to_decimal(vat) + to_decimal(vat2) + to_decimal(service))
                    summary_bill.total_service =  to_decimal(summary_bill.total_service) + to_decimal((netto) * to_decimal(service))
                    summary_bill.total_tax =  to_decimal(summary_bill.total_tax) + to_decimal((netto) * to_decimal(vat))

                    if h_artikel.artnr == discfood_artnr:
                        pass

                    elif h_artikel.artnr == discbev_artnr:
                        pass

                    elif h_artikel.artnr == discoth_artnr:
                        pass

    for summary_bill in query(summary_bill_list):
        summary_bill.total_service = to_decimal(round(summary_bill.total_service , 0))
        summary_bill.total_other = to_decimal(round(summary_bill.total_other , 0))
        summary_bill.total_amount = to_decimal(round(summary_bill.total_food + summary_bill.total_bev + summary_bill.total_other + summary_bill.total_service + summary_bill.total_tax + summary_bill.total_disc , 0))

    return generate_output()