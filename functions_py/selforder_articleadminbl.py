#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 28/11/2025, with_for_update added, remark area
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Queasy, H_artikel

def selforder_articleadminbl(case_type:int, art_dept:int, art_nr:int, art_name:string, art_desc:string, art_img:string, art_flag:bool, soldout:bool):

    prepare_cache ([Queasy, H_artikel])

    t_article_data = []
    nr:int = 0
    queasy = h_artikel = None

    t_article = None

    t_article_data, T_article = create_model("T_article", {"nr":int, "artnr":int, "dept":int, "bezeich":string, "img":string, "remark":string, "activ_art":bool, "sold_out":bool, "selected_art":bool})

    db_session = local_storage.db_session
    art_name = art_name.strip()
    art_desc = art_desc.strip()
    art_img = art_img.strip()   

    def generate_output():
        nonlocal t_article_data, nr, queasy, h_artikel
        nonlocal case_type, art_dept, art_nr, art_name, art_desc, art_img, art_flag, soldout


        nonlocal t_article
        nonlocal t_article_data

        return {"t-article": t_article_data}

    if art_name == None:
        art_name = ""

    if art_desc == None:
        art_desc = ""

    if art_img == None:
        art_img = ""

    if case_type == 1:

        # queasy = get_cache (Queasy, {"key": [(eq, 222)],"number1": [(eq, 2)],"number2": [(eq, art_nr)],"number3": [(eq, art_dept)]})
        queasy = db_session.query(Queasy).filter(
            (Queasy.key == 222) &
            (Queasy.number1 == 2) &
            (Queasy.number2 == art_nr) &
            (Queasy.number3 == art_dept)).with_for_update().first()

        if queasy:
            queasy.char2 = art_img
            queasy.char3 = art_desc
            queasy.logi1 = art_flag
            queasy.logi2 = soldout


        else:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 222
            queasy.number1 = 2
            queasy.number2 = art_nr
            queasy.number3 = art_dept
            queasy.char2 = art_img
            queasy.char3 = art_desc
            queasy.logi1 = art_flag
            queasy.logi2 = soldout

    elif case_type == 2:

        # queasy = get_cache (Queasy, {"key": [(eq, 222)],"number1": [(eq, 2)],"number2": [(eq, art_nr)],"number3": [(eq, art_dept)]})
        queasy = db_session.query(Queasy).filter(
                            (Queasy.key == 222) &
                            (Queasy.number1 == 2) &
                            (Queasy.number2 == art_nr) &
                            (Queasy.number3 == art_dept)).with_for_update().first() 

        if queasy:
            queasy.char2 = ""

    for h_artikel in db_session.query(H_artikel).filter(
             (H_artikel.departement == art_dept) & (H_artikel.activeflag) & (H_artikel.artart == 0) & (H_artikel.epreis1 != 0)).order_by(H_artikel._recid).all():

        # queasy = get_cache (Queasy, {"key": [(eq, 222)],"number1": [(eq, 2)],
        #                              "number2": [(eq, h_artikel.artnr)],"number3": [(eq, h_artikel.departement)]})
        queasy = db_session.query(Queasy).filter(
                                (Queasy.key == 222) &
                                (Queasy.number1 == 2) &
                                (Queasy.number2 == h_artikel.artnr) &
                                (Queasy.number3 == h_artikel.departement)).with_for_update().first()

        if queasy:
            t_article = T_article()
            t_article_data.append(t_article)

            t_article.artnr = queasy.number2
            t_article.dept = queasy.number3
            t_article.bezeich = h_artikel.bezeich
            t_article.img = queasy.char2
            t_article.remark = queasy.char3
            t_article.activ_art = queasy.logi1
            t_article.sold_out = queasy.logi2


        else:
            t_article = T_article()
            t_article_data.append(t_article)

            t_article.artnr = h_artikel.artnr
            t_article.dept = h_artikel.departement
            t_article.bezeich = h_artikel.bezeich


    nr = 0

    for t_article in query(t_article_data, sort_by=[("activ_art",True),("bezeich",False)]):
        nr = nr + 1
        t_article.nr = nr

    return generate_output()