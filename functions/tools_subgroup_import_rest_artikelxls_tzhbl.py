#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Wgrpgen, Wgrpdep, H_artikel

rest_article_list_data, Rest_article_list = create_model("Rest_article_list", {"dept_no":int, "dept_name":string, "artnr":int, "art_desc":string, "main_group":int, "sub_group":int, "main_group_desc":string, "sub_group_desc":string, "art_type":int, "price":Decimal, "cost_perc":Decimal, "fo_artnr":int, "foart_desc":string, "recipe_no":int, "recipe_desc":string, "kp_no":int, "kp_desc":string, "active_art":bool})
rest_maingroup_list_data, Rest_maingroup_list = create_model("Rest_maingroup_list", {"maingroup_no":int, "maingroup_desc":string, "new_maingroup_no":int, "new_maingroup_desc":string, "fibukonto":string, "betriebsnr":int})
rest_subgroup_list_data, Rest_subgroup_list = create_model("Rest_subgroup_list", {"dept_no":int, "dept_name":string, "subgroup_no":int, "subgroup_desc":string, "subgroup_prior":int, "subgroup_bgcol":int, "new_subgroup_no":int, "new_subgroup_desc":string, "fibukonto":string, "betriebsnr":int})

def tools_subgroup_import_rest_artikelxls_tzhbl(rest_article_list_data:[Rest_article_list], rest_maingroup_list_data:[Rest_maingroup_list], rest_subgroup_list_data:[Rest_subgroup_list]):

    prepare_cache ([H_artikel])

    artnr = 0
    dept = ""
    art_desc1 = ""
    art_desc2 = ""
    maingroup = 0
    subgroup = 0
    fl_flag = 0
    wgrpgen = wgrpdep = h_artikel = None

    rest_article_list = rest_maingroup_list = rest_subgroup_list = b_article_list = b_maingroup_list = b_subgroup_list = b_wgrpgen = b_wgrpdep = b_artikel = None

    B_article_list = Rest_article_list
    b_article_list_data = rest_article_list_data

    B_maingroup_list = Rest_maingroup_list
    b_maingroup_list_data = rest_maingroup_list_data

    B_subgroup_list = Rest_subgroup_list
    b_subgroup_list_data = rest_subgroup_list_data

    B_wgrpgen = create_buffer("B_wgrpgen",Wgrpgen)
    B_wgrpdep = create_buffer("B_wgrpdep",Wgrpdep)
    B_artikel = create_buffer("B_artikel",H_artikel)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal artnr, dept, art_desc1, art_desc2, maingroup, subgroup, fl_flag, wgrpgen, wgrpdep, h_artikel
        nonlocal b_article_list, b_maingroup_list, b_subgroup_list, b_wgrpgen, b_wgrpdep, b_artikel


        nonlocal rest_article_list, rest_maingroup_list, rest_subgroup_list, b_article_list, b_maingroup_list, b_subgroup_list, b_wgrpgen, b_wgrpdep, b_artikel

        return {"artnr": artnr, "dept": dept, "art_desc1": art_desc1, "art_desc2": art_desc2, "maingroup": maingroup, "subgroup": subgroup, "fl_flag": fl_flag}

    def fix_subgroup():

        nonlocal artnr, dept, art_desc1, art_desc2, maingroup, subgroup, fl_flag, wgrpgen, wgrpdep, h_artikel
        nonlocal b_article_list, b_maingroup_list, b_subgroup_list, b_wgrpgen, b_wgrpdep, b_artikel


        nonlocal rest_article_list, rest_maingroup_list, rest_subgroup_list, b_article_list, b_maingroup_list, b_subgroup_list, b_wgrpgen, b_wgrpdep, b_artikel

        rest_subgroup_list = query(rest_subgroup_list_data, filters=(lambda rest_subgroup_list: rest_subgroup_list.dept_no == rest_article_list.dept_no and ((rest_subgroup_list.subgroup_desc == rest_article_list.sub_group_desc) or (rest_subgroup_list.new_subgroup_desc == rest_article_list.sub_group_desc))), first=True)

        if rest_subgroup_list:

            if trim(rest_subgroup_list.subgroup_desc) == trim(rest_article_list.sub_group_desc):
                rest_article_list.sub_group = rest_subgroup_list.new_subgroup_no

            elif trim (rest_subgroup_list.new_subgroup_desc) == (rest_article_list.sub_group_desc):
                rest_article_list.sub_group = rest_subgroup_list.new_subgroup_no

        for h_artikel in db_session.query(H_artikel).order_by(H_artikel._recid).all():

            b_article_list = query(b_article_list_data, filters=(lambda b_article_list: b_article_list.artnr == h_artikel.artnr and b_article_list.dept_no == h_artikel.departement and b_article_list.sub_group != h_artikel.zwkum), first=True)

            if b_article_list:
                h_artikel.zwkum = b_article_list.sub_group

    fix_subgroup()

    return generate_output()