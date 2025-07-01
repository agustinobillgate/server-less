#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from functions.selforder_loadarticlebl import selforder_loadarticlebl
from models import Wgrpdep, Wgrpgen, Bediener, Hoteldpt, Paramtext, Queasy

def selforder_loadsetupbl(outlet_no:int):

    prepare_cache ([Wgrpdep, Wgrpgen, Bediener, Hoteldpt, Paramtext, Queasy])

    user_init = ""
    font_color = ""
    bg_color = ""
    outlet_name = ""
    hotel_name = ""
    image_logo = ""
    image_food = ""
    image_bev = ""
    image_other = ""
    mess_result = ""
    language_list_list = []
    article_list_list = []
    carousel_list_list = []
    subgroup_list_list = []
    maingroup_list_list = []
    wgrpdep = wgrpgen = bediener = hoteldpt = paramtext = queasy = None

    language_list = article_list = carousel_list = maingroup_list = subgroup_list = None

    language_list_list, Language_list = create_model("Language_list", {"lang_num":int, "lang_id":string, "lang_default":string, "lang_other":string})
    article_list_list, Article_list = create_model("Article_list", {"art_department":int, "art_recid":int, "art_number":int, "art_name":string, "art_group":int, "art_subgrp":int, "art_group_str":string, "art_subgrp_str":string, "art_desc":string, "art_price":Decimal, "art_image":string, "art_active_flag":bool})
    carousel_list_list, Carousel_list = create_model("Carousel_list", {"carousel_recid":int, "carousel_dept":int, "carousel_num":int, "carousel_title":string, "carousel_desc":string, "carousel_image":string})
    maingroup_list_list, Maingroup_list = create_model("Maingroup_list", {"maingrp_no":int, "maingrp_description":string})
    subgroup_list_list, Subgroup_list = create_model("Subgroup_list", {"subgrp_no":int, "subgrp_description":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal user_init, font_color, bg_color, outlet_name, hotel_name, image_logo, image_food, image_bev, image_other, mess_result, language_list_list, article_list_list, carousel_list_list, subgroup_list_list, maingroup_list_list, wgrpdep, wgrpgen, bediener, hoteldpt, paramtext, queasy
        nonlocal outlet_no


        nonlocal language_list, article_list, carousel_list, maingroup_list, subgroup_list
        nonlocal language_list_list, article_list_list, carousel_list_list, maingroup_list_list, subgroup_list_list

        return {"user_init": user_init, "font_color": font_color, "bg_color": bg_color, "outlet_name": outlet_name, "hotel_name": hotel_name, "image_logo": image_logo, "image_food": image_food, "image_bev": image_bev, "image_other": image_other, "mess_result": mess_result, "language-list": language_list_list, "article-list": article_list_list, "carousel-list": carousel_list_list, "subgroup-list": subgroup_list_list, "maingroup-list": maingroup_list_list}


    article_list_list.clear()
    maingroup_list_list.clear()
    subgroup_list_list.clear()

    for wgrpdep in db_session.query(Wgrpdep).filter(
             (Wgrpdep.departement == outlet_no)).order_by(Wgrpdep.betriebsnr.desc(), Wgrpdep.zknr).all():
        subgroup_list = Subgroup_list()
        subgroup_list_list.append(subgroup_list)

        subgroup_list.subgrp_no = wgrpdep.zknr
        subgroup_list.subgrp_description = wgrpdep.bezeich

    for wgrpgen in db_session.query(Wgrpgen).order_by(Wgrpgen.eknr).all():
        maingroup_list = Maingroup_list()
        maingroup_list_list.append(maingroup_list)

        maingroup_list.maingrp_no = wgrpgen.eknr
        maingroup_list.maingrp_description = wgrpgen.bezeich


    language_list_list.clear()
    carousel_list_list.clear()

    bediener = get_cache (Bediener, {"username": [(eq, input_username)]})

    if bediener:
        user_init = bediener.userinit

    hoteldpt = get_cache (Hoteldpt, {"num": [(eq, outlet_no)]})

    if hoteldpt:
        outlet_name = hoteldpt.depart

    paramtext = get_cache (Paramtext, {"txtnr": [(eq, 200)]})

    if paramtext:
        hotel_name = paramtext.ptexte
    mess_result, article_list_list = get_output(selforder_loadarticlebl(outlet_no))

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 222) & (Queasy.number1 == 1)).order_by(Queasy.number2).all():

        if queasy.number2 == 1:
            font_color = queasy.char2

        elif queasy.number2 == 2:
            bg_color = queasy.char2

        elif queasy.number2 == 3:
            image_logo = queasy.char2

    queasy = get_cache (Queasy, {"key": [(eq, 222)],"number1": [(eq, 4)]})

    if queasy:
        image_food = queasy.char1
        image_bev = queasy.char2
        image_other = queasy.char3

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 222) & (Queasy.number1 == 3) & (Queasy.number3 == outlet_no) & (Queasy.logi1)).order_by(Queasy._recid).all():
        carousel_list = Carousel_list()
        carousel_list_list.append(carousel_list)

        carousel_list.carousel_recid = queasy._recid
        carousel_list.carousel_dept = queasy.number3
        carousel_list.carousel_num = queasy.number2
        carousel_list.carousel_title = queasy.char1
        carousel_list.carousel_desc = queasy.char3
        carousel_list.carousel_image = queasy.char2


    mess_result = "Success load data"

    return generate_output()