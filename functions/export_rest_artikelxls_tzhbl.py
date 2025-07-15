#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Htparam, Wgrpgen, Hoteldpt, Wgrpdep, H_artikel, Artikel, H_rezept, Printer

def export_rest_artikelxls_tzhbl():

    prepare_cache ([Htparam, Hoteldpt, Artikel, H_rezept, Printer])

    rest_article_list_data = []
    rest_maingroup_list_data = []
    rest_subgroup_list_data = []
    disc_art1:int = 0
    disc_art2:int = 0
    disc_art3:int = 0
    htparam = wgrpgen = hoteldpt = wgrpdep = h_artikel = artikel = h_rezept = printer = None

    rest_article_list = rest_maingroup_list = rest_subgroup_list = None

    rest_article_list_data, Rest_article_list = create_model("Rest_article_list", {"dept_no":int, "dept_name":string, "artnr":int, "art_desc":string, "main_group":int, "sub_group":int, "main_group_desc":string, "sub_group_desc":string, "art_type":int, "price":Decimal, "cost_perc":Decimal, "fo_artnr":int, "foart_desc":string, "recipe_no":int, "recipe_desc":string, "kp_no":int, "kp_desc":string, "active_art":bool})
    rest_maingroup_list_data, Rest_maingroup_list = create_model("Rest_maingroup_list", {"maingroup_no":int, "maingroup_desc":string})
    rest_subgroup_list_data, Rest_subgroup_list = create_model("Rest_subgroup_list", {"dept_no":int, "dept_name":string, "subgroup_no":int, "subgroup_desc":string, "subgroup_prior":int, "subgroup_bgcol":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal rest_article_list_data, rest_maingroup_list_data, rest_subgroup_list_data, disc_art1, disc_art2, disc_art3, htparam, wgrpgen, hoteldpt, wgrpdep, h_artikel, artikel, h_rezept, printer


        nonlocal rest_article_list, rest_maingroup_list, rest_subgroup_list
        nonlocal rest_article_list_data, rest_maingroup_list_data, rest_subgroup_list_data

        return {"rest-article-list": rest_article_list_data, "rest-maingroup-list": rest_maingroup_list_data, "rest-subgroup-list": rest_subgroup_list_data}

    def create_rest_maingroup():

        nonlocal rest_article_list_data, rest_maingroup_list_data, rest_subgroup_list_data, disc_art1, disc_art2, disc_art3, htparam, wgrpgen, hoteldpt, wgrpdep, h_artikel, artikel, h_rezept, printer


        nonlocal rest_article_list, rest_maingroup_list, rest_subgroup_list
        nonlocal rest_article_list_data, rest_maingroup_list_data, rest_subgroup_list_data


        rest_maingroup_list_data.clear()

        wgrpgen = db_session.query(Wgrpgen).first()
        while None != wgrpgen:
            rest_maingroup_list = Rest_maingroup_list()
            rest_maingroup_list_data.append(rest_maingroup_list)

            rest_maingroup_list.maingroup_no = wgrpgen.eknr
            rest_maingroup_list.maingroup_desc = wgrpgen.bezeich

            curr_recid = wgrpgen._recid
            wgrpgen = db_session.query(Wgrpgen).filter(Wgrpgen._recid > curr_recid).first()


    def create_rest_subgroup():

        nonlocal rest_article_list_data, rest_maingroup_list_data, rest_subgroup_list_data, disc_art1, disc_art2, disc_art3, htparam, wgrpgen, hoteldpt, wgrpdep, h_artikel, artikel, h_rezept, printer


        nonlocal rest_article_list, rest_maingroup_list, rest_subgroup_list
        nonlocal rest_article_list_data, rest_maingroup_list_data, rest_subgroup_list_data


        rest_subgroup_list_data.clear()

        for hoteldpt in db_session.query(Hoteldpt).filter(
                 (Hoteldpt.num > 0)).order_by(Hoteldpt.num).all():

            wgrpdep = get_cache (Wgrpdep, {"departement": [(eq, hoteldpt.num)]})
            while None != wgrpdep:
                rest_subgroup_list = Rest_subgroup_list()
                rest_subgroup_list_data.append(rest_subgroup_list)

                rest_subgroup_list.dept_no = hoteldpt.num
                rest_subgroup_list.dept_name = hoteldpt.depart
                rest_subgroup_list.subgroup_no = wgrpdep.zknr
                rest_subgroup_list.subgroup_desc = wgrpdep.bezeich
                rest_subgroup_list.subgroup_prior = wgrpdep.betriebsnr
                rest_subgroup_list.subgroup_bgcol = to_int(entry(0, wgrpdep.fibukonto, ";"))

                curr_recid = wgrpdep._recid
                wgrpdep = db_session.query(Wgrpdep).filter(
                         (Wgrpdep.departement == hoteldpt.num) & (Wgrpdep._recid > curr_recid)).first()


    def create_rest_art():

        nonlocal rest_article_list_data, rest_maingroup_list_data, rest_subgroup_list_data, disc_art1, disc_art2, disc_art3, htparam, wgrpgen, hoteldpt, wgrpdep, h_artikel, artikel, h_rezept, printer


        nonlocal rest_article_list, rest_maingroup_list, rest_subgroup_list
        nonlocal rest_article_list_data, rest_maingroup_list_data, rest_subgroup_list_data


        rest_article_list_data.clear()

        for hoteldpt in db_session.query(Hoteldpt).filter(
                 (Hoteldpt.num > 0)).order_by(Hoteldpt.num).all():

            h_artikel = get_cache (H_artikel, {"departement": [(eq, hoteldpt.num)],"artart": [(eq, 0)],"artnr": [(ne, disc_art1),(ne, disc_art2),(ne, disc_art3)]})
            while None != h_artikel:
                rest_article_list = Rest_article_list()
                rest_article_list_data.append(rest_article_list)

                rest_article_list.dept_no = h_artikel.departement
                rest_article_list.dept_name = hoteldpt.depart
                rest_article_list.artnr = h_artikel.artnr
                rest_article_list.art_desc = h_artikel.bezeich
                rest_article_list.main_group = h_artikel.endkum
                rest_article_list.sub_group = h_artikel.zwkum
                rest_article_list.art_type = h_artikel.artart
                rest_article_list.price =  to_decimal(h_artikel.epreis1)
                rest_article_list.cost_perc =  to_decimal(h_artikel.prozent)
                rest_article_list.fo_artnr = h_artikel.artnrfront
                rest_article_list.recipe_no = h_artikel.artnrrezept
                rest_article_list.kp_no = h_artikel.bondruckernr[0]
                rest_article_list.active_art = h_artikel.activeflag

                artikel = get_cache (Artikel, {"artnr": [(eq, h_artikel.artnrfront)],"departement": [(eq, h_artikel.departement)]})

                if artikel:
                    rest_article_list.foart_desc = artikel.bezeich

                h_rezept = get_cache (H_rezept, {"artnrrezept": [(eq, h_artikel.artnrrezept)]})

                if h_rezept:
                    rest_article_list.recipe_desc = substring(h_rezept.bezeich, 0, 24)

                wgrpgen = get_cache (Wgrpgen, {"eknr": [(eq, h_artikel.endkum)]})

                if wgrpgen:
                    rest_article_list.main_group_desc = wgrpgen.bezeich

                wgrpdep = get_cache (Wgrpdep, {"departement": [(eq, h_artikel.departement)],"zknr": [(eq, h_artikel.zwkum)]})

                if wgrpdep:
                    rest_article_list.sub_group_desc = wgrpdep.bezeich

                printer = get_cache (Printer, {"nr": [(eq, h_artikel.bondruckernr[0])]})

                if printer:
                    rest_article_list.kp_desc = printer.position

                curr_recid = h_artikel._recid
                h_artikel = db_session.query(H_artikel).filter(
                         (H_artikel.departement == hoteldpt.num) & (H_artikel.artart == 0) & (H_artikel.artnr != disc_art1) & (H_artikel.artnr != disc_art2) & (H_artikel.artnr != disc_art3) & (H_artikel._recid > curr_recid)).first()


    htparam = get_cache (Htparam, {"paramnr": [(eq, 557)]})

    if htparam:
        disc_art1 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 596)]})

    if htparam:
        disc_art2 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 556)]})

    if htparam:
        disc_art3 = htparam.finteger
    create_rest_maingroup()
    create_rest_subgroup()
    create_rest_art()

    return generate_output()