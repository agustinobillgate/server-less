#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Wgrpgen, Wgrpdep, H_artikel

rest_article_list_data, Rest_article_list = create_model("Rest_article_list", {"dept_no":int, "dept_name":string, "artnr":int, "art_desc":string, "main_group":int, "sub_group":int, "main_group_desc":string, "sub_group_desc":string, "art_type":int, "price":Decimal, "cost_perc":Decimal, "fo_artnr":int, "foart_desc":string, "recipe_no":int, "recipe_desc":string, "kp_no":int, "kp_desc":string, "active_art":bool})
rest_maingroup_list_data, Rest_maingroup_list = create_model("Rest_maingroup_list", {"maingroup_no":int, "maingroup_desc":string, "new_maingroup_no":int, "new_maingroup_desc":string, "fibukonto":string, "betriebsnr":int})
rest_subgroup_list_data, Rest_subgroup_list = create_model("Rest_subgroup_list", {"dept_no":int, "dept_name":string, "subgroup_no":int, "subgroup_desc":string, "subgroup_prior":int, "subgroup_bgcol":int, "new_subgroup_no":int, "new_subgroup_desc":string, "fibukonto":string, "betriebsnr":int})

def import_rest_artikelxls_tzhbl(rest_article_list_data:[Rest_article_list], rest_maingroup_list_data:[Rest_maingroup_list], rest_subgroup_list_data:[Rest_subgroup_list]):

    prepare_cache ([Wgrpgen, Wgrpdep, H_artikel])

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

    def cek_artikel():

        nonlocal artnr, dept, art_desc1, art_desc2, maingroup, subgroup, fl_flag, wgrpgen, wgrpdep, h_artikel
        nonlocal b_article_list, b_maingroup_list, b_subgroup_list, b_wgrpgen, b_wgrpdep, b_artikel


        nonlocal rest_article_list, rest_maingroup_list, rest_subgroup_list, b_article_list, b_maingroup_list, b_subgroup_list, b_wgrpgen, b_wgrpdep, b_artikel

        for b_article_list in query(b_article_list_data):

            b_maingroup_list = query(b_maingroup_list_data, filters=(lambda b_maingroup_list:(b_maingroup_list.maingroup_desc == b_article_list.main_group_desc) or (b_maingroup_list.new_maingroup_desc == b_article_list.main_group_desc)), first=True)

            if not b_maingroup_list:
                artnr = b_article_list.artnr
                dept = b_article_list.dept_name
                fl_flag = 1

                return

            b_subgroup_list = query(b_subgroup_list_data, filters=(lambda b_subgroup_list:(b_subgroup_list.subgroup_desc == b_article_list.sub_group_desc) or (b_subgroup_list.new_subgroup_desc == b_article_list.sub_group_desc)), first=True)

            if not b_subgroup_list:
                artnr = b_article_list.artnr
                dept = b_article_list.dept_name
                fl_flag = 2

                return

            rest_article_list = query(rest_article_list_data, filters=(lambda rest_article_list: rest_article_list.dept_no == b_article_list.dept_no and rest_article_list.artnr == b_article_list.artnr), first=True)

            if rest_article_list:

                if rest_article_list.art_desc != b_article_list.art_desc:
                    art_desc1 = b_article_list.art_desc
                    art_desc2 = rest_article_list.art_desc
                    dept = b_article_list.dept_name
                    fl_flag = 3

                    return


    def import_artikel():

        nonlocal artnr, dept, art_desc1, art_desc2, maingroup, subgroup, fl_flag, wgrpgen, wgrpdep, h_artikel
        nonlocal b_article_list, b_maingroup_list, b_subgroup_list, b_wgrpgen, b_wgrpdep, b_artikel


        nonlocal rest_article_list, rest_maingroup_list, rest_subgroup_list, b_article_list, b_maingroup_list, b_subgroup_list, b_wgrpgen, b_wgrpdep, b_artikel

        for h_artikel in db_session.query(H_artikel).order_by(H_artikel._recid).all():

            rest_article_list = query(rest_article_list_data, filters=(lambda rest_article_list: rest_article_list.artnr == h_artikel.artnr and rest_article_list.dept_no == h_artikel.departement), first=True)

            if rest_article_list:
                h_artikel.activeflag = rest_article_list.active_art

            rest_maingroup_list = query(rest_maingroup_list_data, filters=(lambda rest_maingroup_list: rest_maingroup_list.maingroup_no == h_artikel.endkum), first=True)

            if rest_maingroup_list:
                h_artikel.endkum = rest_maingroup_list.new_maingroup_no

            rest_subgroup_list = query(rest_subgroup_list_data, filters=(lambda rest_subgroup_list: rest_subgroup_list.subgroup_no == h_artikel.zwkum and rest_subgroup_list.dept_no == h_artikel.departement), first=True)

            if rest_subgroup_list:
                h_artikel.zwkum = rest_subgroup_list.new_subgroup_no

        for rest_maingroup_list in query(rest_maingroup_list_data):

            wgrpgen = get_cache (Wgrpgen, {"eknr": [(eq, rest_maingroup_list.maingroup_no)]})

            if wgrpgen:
                rest_maingroup_list.fibukonto = wgrpgen.fibukonto
                rest_maingroup_list.betriebsnr = wgrpgen.betriebsnr


                db_session.delete(wgrpgen)

            if not wgrpgen:
                rest_maingroup_list.fibukonto = ""
                rest_maingroup_list.betriebsnr = 0

            b_wgrpgen = get_cache (Wgrpgen, {"eknr": [(eq, rest_maingroup_list.new_maingroup_no)]})

            if not b_wgrpgen:
                b_wgrpgen = Wgrpgen()
                db_session.add(b_wgrpgen)

                b_wgrpgen.eknr = rest_maingroup_list.new_maingroup_no
                b_wgrpgen.bezeich = rest_maingroup_list.new_maingroup_desc
                b_wgrpgen.fibukonto = rest_maingroup_list.fibukonto
                b_wgrpgen.betriebsnr = rest_maingroup_list.betriebsnr

            if b_wgrpgen:
                b_wgrpgen.bezeich = rest_maingroup_list.new_maingroup_desc

        for rest_subgroup_list in query(rest_subgroup_list_data):

            wgrpdep = get_cache (Wgrpdep, {"zknr": [(eq, rest_subgroup_list.subgroup_no)],"departement": [(eq, rest_subgroup_list.dept_no)]})

            if wgrpdep:
                rest_subgroup_list.fibukonto = wgrpdep.fibukonto
                rest_subgroup_list.betriebsnr = wgrpdep.betriebsnr


                db_session.delete(wgrpdep)

            if not wgrpdep:
                rest_subgroup_list.fibukonto = ""
                rest_subgroup_list.betriebsnr = 0

            b_wgrpdep = get_cache (Wgrpdep, {"zknr": [(eq, rest_subgroup_list.new_subgroup_no)],"departement": [(eq, rest_subgroup_list.dept_no)]})

            if not b_wgrpdep:
                b_wgrpdep = Wgrpdep()
                db_session.add(b_wgrpdep)

                b_wgrpdep.zknr = rest_subgroup_list.new_subgroup_no
                b_wgrpdep.bezeich = rest_subgroup_list.new_subgroup_desc
                b_wgrpdep.departement = rest_subgroup_list.dept_no
                b_wgrpdep.fibukonto = rest_subgroup_list.fibukonto
                b_wgrpdep.betriebsnr = rest_subgroup_list.betriebsnr

            if b_wgrpdep:
                b_wgrpdep.bezeich = rest_subgroup_list.new_subgroup_desc

        for rest_article_list in query(rest_article_list_data):

            h_artikel = get_cache (H_artikel, {"artnr": [(eq, rest_article_list.artnr)],"departement": [(eq, rest_article_list.dept_no)]})

            if not h_artikel:
                h_artikel = H_artikel()
                db_session.add(h_artikel)

                h_artikel.departement = rest_article_list.dept_no
                h_artikel.artnr = rest_article_list.artnr
                h_artikel.bezeich = rest_article_list.art_desc
                h_artikel.epreis1 =  to_decimal(rest_article_list.price)
                h_artikel.autosaldo = False
                h_artikel.bezaendern = False
                h_artikel.prozent =  to_decimal(rest_article_list.cost_perc)
                h_artikel.bondruckernr = rest_article_list.kp_no
                h_artikel.aenderwunsch = False
                h_artikel.artnrfront = rest_article_list.fo_artnr
                h_artikel.artnrrezept = rest_article_list.recipe_no
                h_artikel.activeflag = rest_article_list.active_art
                h_artikel.betriebsnr = 0


                wgrpgen = get_cache (Wgrpgen, {"bezeich": [(eq, rest_article_list.main_group_desc)]})

                if wgrpgen:
                    h_artikel.endkum = wgrpgen.eknr

                    b_artikel = get_cache (H_artikel, {"endkum": [(eq, wgrpgen.eknr)],"mwst_code": [(ne, 0)],"service_code": [(ne, 0)]})

                    if b_artikel:
                        h_artikel.mwst_code = b_artikel.mwst_code
                        h_artikel.service_code = b_artikel.service_code

                wgrpdep = get_cache (Wgrpdep, {"bezeich": [(eq, rest_article_list.sub_group_desc)],"departement": [(eq, rest_article_list.dept_no)]})

                if wgrpdep:
                    h_artikel.zwkum = wgrpdep.zknr

            elif h_artikel:

                if length(to_string(rest_article_list.artnr)) > 6:
                    h_artikel.epreis1 =  to_decimal(rest_article_list.price)
                    h_artikel.activeflag = rest_article_list.active_art
                    h_artikel.bezeich = rest_article_list.art_desc

                    if h_artikel.mwst_code == 0 and h_artikel.service_code == 0:

                        b_artikel = get_cache (H_artikel, {"endkum": [(eq, h_artikel.endkum)],"mwst_code": [(ne, 0)],"service_code": [(ne, 0)]})

                        if b_artikel:
                            h_artikel.mwst_code = b_artikel.mwst_code
                            h_artikel.service_code = b_artikel.service_code

    cek_artikel()

    if fl_flag == 1 or fl_flag == 2 or fl_flag == 3:

        return generate_output()
    import_artikel()

    return generate_output()