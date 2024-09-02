from functions.additional_functions import *
import decimal
from models import Queasy

def selforder_articleadmin_change_active_soldoutbl(case_type:int, t_article:[T_article]):
    success_flag = False
    queasy = None

    t_article = None

    t_article_list, T_article = create_model("T_article", {"nr":int, "artnr":int, "dept":int, "bezeich":str, "img":str, "remark":str, "activ_art":bool, "sold_out":bool, "selected_art":bool})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, queasy


        nonlocal t_article
        nonlocal t_article_list
        return {"success_flag": success_flag}

    if case_type == 1:

        for t_article in query(t_article_list, filters=(lambda t_article :t_article.selected_art  and t_article.activ_art == False)):

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 222) &  (Queasy.number1 == 2) &  (Queasy.number2 == t_article.artnr) &  (Queasy.number3 == t_article.dept) &  (t_article.activ_art == Queasy.logi1)).first()

            if queasy:

                queasy = db_session.query(Queasy).first()
                queasy.logi1 = True

                queasy = db_session.query(Queasy).first()
            else:
                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 222
                queasy.number1 = 2
                queasy.number2 = t_article.artnr
                queasy.number3 = t_article.dept
                queasy.logi1 = True
                queasy.logi2 = False


        success_flag = True

    elif case_type == 2:

        for t_article in query(t_article_list, filters=(lambda t_article :t_article.selected_art  and t_article.activ_art)):

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 222) &  (Queasy.number1 == 2) &  (Queasy.number2 == t_article.artnr) &  (Queasy.number3 == t_article.dept) &  (t_article.activ_art == Queasy.logi1)).first()

            if queasy:

                queasy = db_session.query(Queasy).first()
                queasy.logi1 = False

                queasy = db_session.query(Queasy).first()
        success_flag = True

    elif case_type == 3:

        for t_article in query(t_article_list, filters=(lambda t_article :t_article.selected_art  and t_article.sold_out == False)):

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 222) &  (Queasy.number1 == 2) &  (Queasy.number2 == t_article.artnr) &  (Queasy.number3 == t_article.dept) &  (t_article.sold_out == Queasy.logi2)).first()

            if queasy:

                queasy = db_session.query(Queasy).first()
                queasy.logi2 = True

                queasy = db_session.query(Queasy).first()
            else:
                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 222
                queasy.number1 = 2
                queasy.number2 = t_article.artnr
                queasy.number3 = t_article.dept
                queasy.logi1 = False
                queasy.logi2 = True


        success_flag = True

    elif case_type == 4:

        for t_article in query(t_article_list, filters=(lambda t_article :t_article.selected_art  and t_article.sold_out)):

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 222) &  (Queasy.number1 == 2) &  (Queasy.number2 == t_article.artnr) &  (Queasy.number3 == t_article.dept) &  (t_article.sold_out == Queasy.logi2)).first()

            if queasy:

                queasy = db_session.query(Queasy).first()
                queasy.logi2 = False

                queasy = db_session.query(Queasy).first()
        success_flag = True

    return generate_output()