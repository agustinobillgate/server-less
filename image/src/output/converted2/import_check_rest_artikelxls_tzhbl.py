#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import H_rezept, H_artikel

rest_article_list_list, Rest_article_list = create_model("Rest_article_list", {"dept_no":int, "dept_name":string, "artnr":int, "art_desc":string, "main_group":int, "sub_group":int, "main_group_desc":string, "sub_group_desc":string, "art_type":int, "price":Decimal, "cost_perc":Decimal, "fo_artnr":int, "foart_desc":string, "recipe_no":int, "recipe_desc":string, "kp_no":int, "kp_desc":string, "active_art":bool})
rest_maingroup_list_list, Rest_maingroup_list = create_model("Rest_maingroup_list", {"maingroup_no":int, "maingroup_desc":string, "new_maingroup_no":int, "new_maingroup_desc":string, "fibukonto":string, "betriebsnr":int})
rest_subgroup_list_list, Rest_subgroup_list = create_model("Rest_subgroup_list", {"dept_no":int, "dept_name":string, "subgroup_no":int, "subgroup_desc":string, "subgroup_prior":int, "subgroup_bgcol":int, "new_subgroup_no":int, "new_subgroup_desc":string, "fibukonto":string, "betriebsnr":int})

def import_check_rest_artikelxls_tzhbl(rest_article_list_list:[Rest_article_list], rest_maingroup_list_list:[Rest_maingroup_list], rest_subgroup_list_list:[Rest_subgroup_list]):
    output_list_list = []
    h_rezept = h_artikel = None

    rest_article_list = rest_maingroup_list = rest_subgroup_list = output_list = b_article_list = b_maingroup_list = b_subgroup_list = None

    output_list_list, Output_list = create_model("Output_list", {"dept_no":int, "dept_name":string, "artnr":int, "art_desc":string, "maingroup":int, "subgroup":int, "str":string, "key":string, "flag":int})

    B_article_list = Rest_article_list
    b_article_list_list = rest_article_list_list

    B_maingroup_list = Rest_maingroup_list
    b_maingroup_list_list = rest_maingroup_list_list

    B_subgroup_list = Rest_subgroup_list
    b_subgroup_list_list = rest_subgroup_list_list

    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_list, h_rezept, h_artikel
        nonlocal b_article_list, b_maingroup_list, b_subgroup_list


        nonlocal rest_article_list, rest_maingroup_list, rest_subgroup_list, output_list, b_article_list, b_maingroup_list, b_subgroup_list
        nonlocal output_list_list

        return {"output-list": output_list_list}

    output_list_list.clear()

    for rest_maingroup_list in query(rest_maingroup_list_list):

        if rest_maingroup_list.new_maingroup_no != None and rest_maingroup_list.new_maingroup_desc == None:
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.str = "There is a new main group but no description " + "(" + to_string(rest_maingroup_list.new_maingroup_no) + ")"
            output_list.key = "maingroup"

        if rest_maingroup_list.new_maingroup_no == None and rest_maingroup_list.new_maingroup_desc != None:
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.str = "There is a new main group but has not number " + "(" + rest_maingroup_list.new_maingroup_desc + ")"
            output_list.key = "maingroup"

    for rest_subgroup_list in query(rest_subgroup_list_list):

        if rest_subgroup_list.new_subgroup_no != None and rest_subgroup_list.new_subgroup_desc == None:
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.str = "There is a new sub group but no description " + "(" + to_string(rest_subgroup_list.new_subgroup_no) + ")"
            output_list.key = "subgroup"

        if rest_subgroup_list.new_subgroup_no == None and rest_subgroup_list.new_subgroup_desc != None:
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.str = "There is a new sub group but has not number " + "(" + rest_subgroup_list.new_subgroup_desc + ")"
            output_list.key = "subgroup"

        if rest_subgroup_list.new_subgroup_no != None or rest_subgroup_list.new_subgroup_desc != None:

            if rest_subgroup_list.dept_no == None:
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.str = "There is a new sub group but has not departement number " + "(" + to_string(rest_subgroup_list.new_subgroup_no) + ")"
                output_list.key = "subgroup"

            if rest_subgroup_list.dept_name == None:
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.str = "There is a new sub group but has not departement description " + "(" + to_string(rest_subgroup_list.new_subgroup_no) + ")"
                output_list.key = "subgroup"

    for rest_article_list in query(rest_article_list_list):

        if rest_article_list.dept_no == None:
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.str = "There is an article has not departement number at article " + "(" + to_string(rest_article_list.artnr) + ")"
            output_list.key = "article"

        if rest_article_list.art_desc == None:
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.str = "There is an article has not description at article " + "(" + to_string(rest_article_list.artnr) + ")"
            output_list.key = "article"

        if rest_article_list.price == None:
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.str = "Please fill the Price column at article " + "(" + to_string(rest_article_list.artnr) + ")"
            output_list.key = "article"

        if rest_article_list.cost_perc == None:
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.str = "Please fill Cost% column at article " + "(" + to_string(rest_article_list.artnr) + ")"
            output_list.key = "article"

        if rest_article_list.kp_no == None:
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.str = "Please fill KP NO column at article " + "(" + to_string(rest_article_list.artnr) + ")"
            output_list.key = "article"

        if rest_article_list.fo_artnr == None:
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.str = "Please fill FO Art column at article " + "(" + to_string(rest_article_list.artnr) + ")"
            output_list.key = "article"

        if rest_article_list.recipe_no == None:
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.str = "Please fill Recipe column at article " + "(" + to_string(rest_article_list.artnr) + ")"
            output_list.key = "article"

        b_maingroup_list = query(b_maingroup_list_list, filters=(lambda b_maingroup_list:(b_maingroup_list.maingroup_desc == rest_article_list.main_group_desc) or (b_maingroup_list.new_maingroup_desc == rest_article_list.main_group_desc)), first=True)

        if not b_maingroup_list:
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.str = "There is an invalid maingroup description at article " + "(" + to_string(rest_article_list.artnr) + ")" + " Department " +\
                    rest_article_list.dept_name
            output_list.key = "article"

        b_subgroup_list = query(b_subgroup_list_list, filters=(lambda b_subgroup_list:(b_subgroup_list.subgroup_desc == rest_article_list.sub_group_desc) or (b_subgroup_list.new_subgroup_desc == rest_article_list.sub_group_desc)), first=True)

        if not b_subgroup_list:
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.str = "There is an invalid subgroup description at article " + "(" + to_string(rest_article_list.artnr) + ")" + " Department " +\
                    rest_article_list.dept_name
            output_list.key = "article"

        b_article_list = query(b_article_list_list, filters=(lambda b_article_list: b_article_list.dept_no == rest_article_list.dept_no and b_article_list.artnr == rest_article_list.artnr), first=True)

        if b_article_list:

            if b_article_list.art_desc != rest_article_list.art_desc:
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.str = "Article " + b_article_list.art_desc + " has the same article number with " + rest_article_list.art_desc


                output_list.key = "article"

        if length(to_string(rest_article_list.artnr)) > 8:

            rest_maingroup_list = query(rest_maingroup_list_list, filters=(lambda rest_maingroup_list: rest_maingroup_list.new_maingroup_no == to_int(substring(to_string(rest_article_list.artnr) , 0, 1))), first=True)

            if not rest_maingroup_list:
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.str = "New Article " + rest_article_list.art_desc + " has invalid main group number in article number"


                output_list.key = "article"

            rest_subgroup_list = query(rest_subgroup_list_list, filters=(lambda rest_subgroup_list: rest_subgroup_list.new_subgroup_no == to_int(substring(to_string(rest_article_list.artnr) , 3, 2)) and rest_subgroup_list.dept_no == rest_article_list.dept_no), first=True)

            if not rest_subgroup_list:
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.str = "New Article " + rest_article_list.art_desc + " has invalid sub group number in article number"


                output_list.key = "article"

        if rest_article_list.recipe_no != 0:

            h_rezept = get_cache (H_rezept, {"artnrrezept": [(eq, rest_article_list.recipe_no)]})

            if not h_rezept:
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.str = "Article " + rest_article_list.art_desc + "(" + to_string(rest_article_list.artnr) + ")" + " has invalid recipe number (not found)"


                output_list.key = "article"

        h_artikel = get_cache (H_artikel, {"artnr": [(eq, rest_article_list.artnr)],"departement": [(eq, rest_article_list.dept_no)],"activeflag": [(ne, rest_article_list.active_art)]})

        if h_artikel:
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.str = "Article " + rest_article_list.art_desc + " ( " + to_string(rest_article_list.artnr) + " )" + " at departement " + rest_article_list.dept_name + " is exist but flag is not same."
            output_list.key = "completed"
            output_list.flag = 1

    output_list = query(output_list_list, filters=(lambda output_list: output_list.key.lower()  != ("completed").lower()), first=True)

    if not output_list:
        output_list = Output_list()
        output_list_list.append(output_list)

        output_list.str = "EXCEL COMPLETED"
        output_list.key = "completed"
        output_list.flag = 2

    return generate_output()