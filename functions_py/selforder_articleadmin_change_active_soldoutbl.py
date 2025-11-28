#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 28/11/2025, with_for_update added, remark area
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

t_article_data, T_article = create_model("T_article", {"nr":int, "artnr":int, "dept":int, "bezeich":string, "img":string, "remark":string, "activ_art":bool, "sold_out":bool, "selected_art":bool})

def selforder_articleadmin_change_active_soldoutbl(case_type:int, t_article_data:[T_article]):

    prepare_cache ([Queasy])

    success_flag = False
    queasy = None

    t_article = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, queasy
        nonlocal case_type


        nonlocal t_article

        return {"success_flag": success_flag}

    if case_type == 1:

        for t_article in query(t_article_data, filters=(lambda t_article: t_article.selected_art  and t_article.activ_art == False)):

            # queasy = get_cache (Queasy, {"key": [(eq, 222)],"number1": [(eq, 2)],"number2": [(eq, t_article.artnr)],
            #                              "number3": [(eq, t_article.dept)],"logi1": [(eq, t_article.activ_art)]})
            queasy = db_session.query(Queasy).filter(
                        (Queasy.key == 222) &
                        (Queasy.number1 == 2) &
                        (Queasy.number2 == t_article.artnr) &
                        (Queasy.number3 == t_article.dept) &
                        (Queasy.logi1 == t_article.activ_art)
                    ).with_for_update().first()

            if queasy:
                pass
                queasy.logi1 = True
                pass
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

        for t_article in query(t_article_data, filters=(lambda t_article: t_article.selected_art  and t_article.activ_art)):

            # queasy = get_cache (Queasy, {"key": [(eq, 222)],"number1": [(eq, 2)],"number2": [(eq, t_article.artnr)],
            #                              "number3": [(eq, t_article.dept)],"logi1": [(eq, t_article.activ_art)]})
            queasy = db_session.query(Queasy).filter(
                            (Queasy.key == 222) &
                            (Queasy.number1 == 2) &
                            (Queasy.number2 == t_article.artnr) &
                            (Queasy.number3 == t_article.dept) &
                            (Queasy.logi1 == t_article.activ_art)
                        ).with_for_update().first()

            if queasy:
                queasy.logi1 = False
        success_flag = True

    elif case_type == 3:

        for t_article in query(t_article_data, filters=(lambda t_article: t_article.selected_art  and t_article.sold_out == False)):

            # queasy = get_cache (Queasy, {"key": [(eq, 222)],"number1": [(eq, 2)],"number2": [(eq, t_article.artnr)],
            #                              "number3": [(eq, t_article.dept)],"logi2": [(eq, t_article.sold_out)]})
            queasy = db_session.query(Queasy).filter(
                            (Queasy.key == 222) &
                            (Queasy.number1 == 2) &
                            (Queasy.number2 == t_article.artnr) &
                            (Queasy.number3 == t_article.dept) &
                            (Queasy.logi2 == t_article.sold_out)
                        ).with_for_update().first()

            if queasy:
                queasy.logi2 = True
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

        for t_article in query(t_article_data, filters=(lambda t_article: t_article.selected_art  and t_article.sold_out)):

            # queasy = get_cache (Queasy, {"key": [(eq, 222)],"number1": [(eq, 2)],"number2": [(eq, t_article.artnr)],
            #                              "number3": [(eq, t_article.dept)],"logi2": [(eq, t_article.sold_out)]})
            queasy = db_session.query(Queasy).filter(
                                    (Queasy.key == 222) &
                                    (Queasy.number1 == 2) &
                                    (Queasy.number2 == t_article.artnr) &
                                    (Queasy.number3 == t_article.dept) &
                                    (Queasy.logi2 == t_article.sold_out)
                                ).with_for_update().first()

            if queasy:
                queasy.logi2 = False
        success_flag = True

    return generate_output()