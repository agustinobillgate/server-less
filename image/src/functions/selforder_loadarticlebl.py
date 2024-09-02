from functions.additional_functions import *
import decimal
from functions.htplogic import htplogic
from models import Hoteldpt, Queasy, H_artikel, Artikel, Htparam

def selforder_loadarticlebl(outlet_no:int):
    mess_result = ""
    article_list_list = []
    maingroup_list_list = []
    subgroup_list_list = []
    ct:str = ""
    l_deci:int = 2
    serv_vat:bool = False
    tax_vat:bool = False
    tax:decimal = 0
    serv:decimal = 0
    service:decimal = 0
    vat:decimal = 0
    vat2:decimal = 0
    fact_scvat:decimal = 1
    servtax_use_foart:bool = False
    service_foreign:decimal = 0
    serv_code:int = 0
    vat_code:int = 0
    hoteldpt = queasy = h_artikel = artikel = htparam = None

    article_list = maingroup_list = subgroup_list = bqsy = None

    article_list_list, Article_list = create_model("Article_list", {"art_department":int, "art_recid":int, "art_number":int, "art_name":str, "art_group":int, "art_subgrp":int, "art_group_str":str, "art_subgrp_str":str, "art_desc":str, "art_price":decimal, "art_orig_price":decimal, "art_image":str, "art_active_flag":bool, "art_sold_out":bool})
    maingroup_list_list, Maingroup_list = create_model("Maingroup_list", {"maingrp_no":int, "maingrp_description":str, "maingrp_image":str})
    subgroup_list_list, Subgroup_list = create_model("Subgroup_list", {"subgrp_no":int, "subgrp_description":str})

    Bqsy = Queasy

    db_session = local_storage.db_session

    def generate_output():
        nonlocal mess_result, article_list_list, maingroup_list_list, subgroup_list_list, ct, l_deci, serv_vat, tax_vat, tax, serv, service, vat, vat2, fact_scvat, servtax_use_foart, service_foreign, serv_code, vat_code, hoteldpt, queasy, h_artikel, artikel, htparam
        nonlocal bqsy


        nonlocal article_list, maingroup_list, subgroup_list, bqsy
        nonlocal article_list_list, maingroup_list_list, subgroup_list_list
        return {"mess_result": mess_result, "article-list": article_list_list, "maingroup-list": maingroup_list_list, "subgroup-list": subgroup_list_list}


    article_list._list.clear()
    maingroup_list._list.clear()
    subgroup_list._list.clear()

    hoteldpt = db_session.query(Hoteldpt).filter(
            (Hoteldpt.num == outlet_no)).first()

    if hoteldpt:
        servtax_use_foart = hoteldpt.defult

    queasy = db_session.query(Queasy).filter(
            (Queasy.key == 228)).first()

    if queasy:

        for queasy in db_session.query(Queasy).filter(
                (Queasy.key == 228) &  (Queasy.number2 == outlet_no)).all():
            maingroup_list = Maingroup_list()
            maingroup_list_list.append(maingroup_list)

            maingroup_list.maingrp_no = queasy.number1
            maingroup_list.maingrp_description = queasy.char1
            maingroup_list.maingrp_image = queasy.char2


    else:
        mess_result = "MainGroup not configured yet!"

        return generate_output()

    queasy = db_session.query(Queasy).filter(
            (Queasy.key == 229)).first()

    if not queasy:
        mess_result = "There is no mapping for subgroup, please mapping it first!"

        return generate_output()

    for h_artikel in db_session.query(H_artikel).filter(
            (H_artikel.departement == outlet_no) &  (H_artikel.artart == 0) &  (H_artikel.activeflag) &  (H_artikel.epreis1 != 0)).all():

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 229) &  (Queasy.number1 == h_artikel.zwkum) &  (Queasy.number2 == h_artikel.departement)).first()

        if queasy:
            service = 0
            vat = 0
            vat2 = 0

            if servtax_use_foart:

                artikel = db_session.query(Artikel).filter(
                        (Artikel.artnr == h_Artikel.artnrfront) &  (Artikel.departement == h_Artikel.departement)).first()

                if artikel:
                    serv_code = artikel.service_code
                    vat_code = artikel.mwst_code


            else:
                serv_code = h_artikel.service_code
                vat_code = h_artikel.mwst_code

            bqsy = db_session.query(Bqsy).filter(
                    (Bqsy.key == 228) &  (Bqsy.number1 == queasy.number3) &  (Bqsy.number2 == queasy.number2)).first()

            htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == 135)).first()

            if not htparam.flogical and h_artikel.artart == 0 and serv_code != 0:

                htparam = db_session.query(Htparam).filter(
                        (Htparam.paramnr == serv_code)).first()

                if htparam and htparam.fdecimal != 0:

                    if num_entries(htparam.fchar, chr(2)) >= 2:
                        service = decimal.Decimal(entry(1, htparam.fchar, chr(2))) / 10000


                    else:
                        service = htparam.fdecimal
            serv_vat = get_output(htplogic(479))
            tax_vat = get_output(htplogic(483))

            htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == 134)).first()

            if not htparam.flogical and h_artikel.artart == 0 and vat_code != 0:

                htparam = db_session.query(Htparam).filter(
                        (Htparam.paramnr == vat_code)).first()

                if htparam and htparam.fdecimal != 0:

                    if num_entries(htparam.fchar, chr(2)) >= 2:
                        vat = decimal.Decimal(entry(1, htparam.fchar, chr(2))) / 10000


                    else:
                        vat = htparam.fdecimal

                    if serv_vat and not tax_vat:
                        vat = vat + vat * service / 100

                    elif serv_vat and tax_vat:
                        vat = vat + vat * (service + vat2) / 100

                    elif not serv_vat and tax_vat:
                        vat = vat + vat * vat2 / 100
                    ct = replace_str(to_string(vat) , ".", ",")
                    l_deci = len(entry(1, ct, ","))

                    if l_deci <= 2:
                        vat = round(vat, 2)

                    elif l_deci == 3:
                        vat = round(vat, 3)
                    else:
                        vat = round(vat, 4)

            if h_artikel.artart == 0:

                if serv_code != 0:
                    service = service / 100

                if vat_code != 0:
                    vat = vat / 100
                    vat2 = vat2 / 100


                fact_scvat = 1 + service + vat + vat2

                if vat == 1:
                    fact_scvat = 1
                    service = 0
                    vat2 = 0

                elif vat2 == 1:
                    fact_scvat = 1
                    service = 0
                    vat = 0

                elif service == 1:
                    fact_scvat = 1
                    vat = 0
                    vat2 = 0


            article_list = Article_list()
            article_list_list.append(article_list)

            article_list.art_department = h_artikel.departement
            article_list.art_recid = h_artikel._recid
            article_list.art_number = h_artikel.artnr
            article_list.art_name = h_artikel.bezeich
            article_list.art_subgrp = h_artikel.zwkum
            article_list.art_subgrp_str = queasy.char1
            article_list.art_price = h_artikel.epreis1 * fact_scvat
            article_list.art_price = round(article_list.art_price, 0)
            article_list.art_orig_price = h_artikel.epreis1

            if bqsy:
                article_list.art_group = bqsy.number1
                article_list.art_group_str = bqsy.char1

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 222) &  (Queasy.number1 == 2) &  (Queasy.number2 == h_artikel.artnr) &  (Queasy.number3 == h_artikel.departement)).first()

            if queasy:
                article_list.art_image = queasy.char2
                article_list.art_desc = queasy.char3
                article_list.art_active_flag = queasy.logi1
                article_list.art_sold_out = queasy.logi2

    for article_list in query(article_list_list, filters=(lambda article_list :article_list.art_active_flag == False)):
        article_list_list.remove(article_list)
    mess_result = "Success load data ya"

    return generate_output()