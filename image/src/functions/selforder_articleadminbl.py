from functions.additional_functions import *
import decimal
from models import Queasy, H_artikel

def selforder_articleadminbl(case_type:int, art_dept:int, art_nr:int, art_name:str, art_desc:str, art_img:str, art_flag:bool, soldout:bool):
    t_article_list = []
    nr:int = 0
    queasy = h_artikel = None

    t_article = None

    t_article_list, T_article = create_model("T_article", {"nr":int, "artnr":int, "dept":int, "bezeich":str, "img":str, "remark":str, "activ_art":bool, "sold_out":bool, "selected_art":bool})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_article_list, nr, queasy, h_artikel


        nonlocal t_article
        nonlocal t_article_list
        return {"t-article": t_article_list}

    if case_type == 1:

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 222) &  (Queasy.number1 == 2) &  (Queasy.number2 == art_nr) &  (Queasy.number3 == art_dept)).first()

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

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 222) &  (Queasy.number1 == 2) &  (Queasy.number2 == art_nr) &  (Queasy.number3 == art_dept)).first()

        if queasy:
            queasy.char2 = ""

    for h_artikel in db_session.query(H_artikel).filter(
            (H_artikel.departement == art_dept) &  (H_artikel.activeflag) &  (H_artikel.artart == 0) &  (H_artikel.epreis1 != 0)).all():

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 222) &  (Queasy.number1 == 2) &  (Queasy.number2 == h_artikel.artnr) &  (Queasy.number3 == h_artikel.departement)).first()

        if queasy:
            t_article = T_article()
            t_article_list.append(t_article)

            t_article.artnr = queasy.number2
            t_article.dept = queasy.number3
            t_article.bezeich = h_artikel.bezeich
            t_article.img = queasy.char2
            t_article.remark = queasy.char3
            t_article.activ_art = queasy.logi1
            t_article.sold_out = queasy.logi2


        else:
            t_article = T_article()
            t_article_list.append(t_article)

            t_article.artnr = h_artikel.artnr
            t_article.dept = h_artikel.departement
            t_article.bezeich = h_artikel.bezeich


    nr = 0

    for t_article in query(t_article_list):
        nr = nr + 1
        t_article.nr = nr

    return generate_output()