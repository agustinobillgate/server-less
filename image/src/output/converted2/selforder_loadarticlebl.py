#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from functions.htplogic import htplogic
from models import Hoteldpt, Queasy, H_artikel, Artikel, Htparam

def selforder_loadarticlebl(outlet_no:int):

    prepare_cache ([Hoteldpt, Queasy, H_artikel, Artikel, Htparam])

    mess_result = ""
    article_list_list = []
    maingroup_list_list = []
    subgroup_list_list = []
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
    hoteldpt = queasy = h_artikel = artikel = htparam = None

    article_list = maingroup_list = subgroup_list = bqsy = None

    article_list_list, Article_list = create_model("Article_list", {"art_department":int, "art_recid":int, "art_number":int, "art_name":string, "art_group":int, "art_subgrp":int, "art_group_str":string, "art_subgrp_str":string, "art_desc":string, "art_price":Decimal, "art_orig_price":Decimal, "art_image":string, "art_active_flag":bool, "art_sold_out":bool})
    maingroup_list_list, Maingroup_list = create_model("Maingroup_list", {"maingrp_no":int, "maingrp_description":string, "maingrp_image":string})
    subgroup_list_list, Subgroup_list = create_model("Subgroup_list", {"subgrp_no":int, "subgrp_description":string})

    Bqsy = create_buffer("Bqsy",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal mess_result, article_list_list, maingroup_list_list, subgroup_list_list, ct, l_deci, serv_vat, tax_vat, tax, serv, service, vat, vat2, fact_scvat, servtax_use_foart, service_foreign, serv_code, vat_code, hoteldpt, queasy, h_artikel, artikel, htparam
        nonlocal outlet_no
        nonlocal bqsy


        nonlocal article_list, maingroup_list, subgroup_list, bqsy
        nonlocal article_list_list, maingroup_list_list, subgroup_list_list

        return {"mess_result": mess_result, "article-list": article_list_list, "maingroup-list": maingroup_list_list, "subgroup-list": subgroup_list_list}


    article_list_list.clear()
    maingroup_list_list.clear()
    subgroup_list_list.clear()

    hoteldpt = get_cache (Hoteldpt, {"num": [(eq, outlet_no)]})

    if hoteldpt:
        servtax_use_foart = hoteldpt.defult

    queasy = get_cache (Queasy, {"key": [(eq, 228)]})

    if queasy:

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 228) & (Queasy.number2 == outlet_no)).order_by(Queasy._recid).all():
            maingroup_list = Maingroup_list()
            maingroup_list_list.append(maingroup_list)

            maingroup_list.maingrp_no = queasy.number1
            maingroup_list.maingrp_description = queasy.char1
            maingroup_list.maingrp_image = queasy.char2


    else:
        mess_result = "MainGroup not configured yet!"

        return generate_output()

    queasy = get_cache (Queasy, {"key": [(eq, 229)]})

    if not queasy:
        mess_result = "There is no mapping for subgroup, please mapping it first!"

        return generate_output()

    for h_artikel in db_session.query(H_artikel).filter(
             (H_artikel.departement == outlet_no) & (H_artikel.artart == 0) & (H_artikel.activeflag) & (H_artikel.epreis1 != 0)).order_by(H_artikel.bezeich).all():

        queasy = get_cache (Queasy, {"key": [(eq, 229)],"number1": [(eq, h_artikel.zwkum)],"number2": [(eq, h_artikel.departement)]})

        if queasy:
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

            bqsy = get_cache (Queasy, {"key": [(eq, 228)],"number1": [(eq, queasy.number3)],"number2": [(eq, queasy.number2)]})

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


            article_list = Article_list()
            article_list_list.append(article_list)

            article_list.art_department = h_artikel.departement
            article_list.art_recid = h_artikel._recid
            article_list.art_number = h_artikel.artnr
            article_list.art_name = h_artikel.bezeich
            article_list.art_subgrp = h_artikel.zwkum
            article_list.art_subgrp_str = queasy.char1
            article_list.art_price =  to_decimal(h_artikel.epreis1) * to_decimal(fact_scvat)
            article_list.art_price = to_decimal(round(article_list.art_price , 0))
            article_list.art_orig_price =  to_decimal(h_artikel.epreis1)

            if bqsy:
                article_list.art_group = bqsy.number1
                article_list.art_group_str = bqsy.char1

            queasy = get_cache (Queasy, {"key": [(eq, 222)],"number1": [(eq, 2)],"number2": [(eq, h_artikel.artnr)],"number3": [(eq, h_artikel.departement)]})

            if queasy:
                article_list.art_image = queasy.char2
                article_list.art_desc = queasy.char3
                article_list.art_active_flag = queasy.logi1
                article_list.art_sold_out = queasy.logi2

    for article_list in query(article_list_list, filters=(lambda article_list: article_list.art_active_flag == False)):
        article_list_list.remove(article_list)
    mess_result = "Success load data ya"

    return generate_output()