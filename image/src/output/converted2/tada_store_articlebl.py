#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy, H_artikel

t_article_list, T_article = create_model("T_article", {"vhpdept":int, "vhpartnr":int, "vhpbezeich":string, "vhpflag":bool, "tadadept":int, "tadaartnr":int, "tadabezeich":string, "tadaflag":bool, "tadasku":string})

def tada_store_articlebl(case_type:int, vhp_artnr:int, deptno:int, article_flag:bool, t_article_list:[T_article]):

    prepare_cache ([Queasy, H_artikel])

    queasy = h_artikel = None

    t_article = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal queasy, h_artikel
        nonlocal case_type, vhp_artnr, deptno, article_flag


        nonlocal t_article

        return {}

    if case_type == 1:

        for t_article in query(t_article_list):

            queasy = get_cache (Queasy, {"key": [(eq, 270)],"number1": [(eq, 2)],"betriebsnr": [(eq, t_article.vhpdept)],"number2": [(eq, t_article.tadaartnr)]})

            if not queasy:
                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 270
                queasy.betriebsnr = t_article.vhpdept
                queasy.deci1 =  to_decimal(to_decimal(t_article.tadadept) )
                queasy.number1 = 2
                queasy.number2 = t_article.tadaartnr
                queasy.number3 = t_article.vhpartnr
                queasy.char1 = t_article.tadasku
                queasy.char2 = t_article.tadabezeich
                queasy.char3 = t_article.vhpbezeich
                queasy.logi2 = t_article.tadaflag
                queasy.logi3 = t_article.vhpflag

    elif case_type == 2:

        for t_article in query(t_article_list):

            queasy = get_cache (Queasy, {"key": [(eq, 270)],"number1": [(eq, 2)],"betriebsnr": [(eq, t_article.vhpdept)],"number2": [(eq, t_article.tadaartnr)]})

            if queasy:
                pass
                queasy.number2 = t_article.tadaartnr
                queasy.number3 = t_article.vhpartnr
                queasy.char1 = t_article.tadasku
                queasy.char2 = t_article.tadabezeich
                queasy.char3 = t_article.vhpbezeich
                queasy.logi2 = t_article.tadaflag
                queasy.logi3 = t_article.vhpflag


                pass
            else:
                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 270
                queasy.betriebsnr = t_article.vhpdept
                queasy.deci1 =  to_decimal(to_decimal(t_article.tadadept) )
                queasy.number1 = 2
                queasy.number2 = t_article.tadaartnr
                queasy.number3 = t_article.vhpartnr
                queasy.char1 = t_article.tadasku
                queasy.char2 = t_article.tadabezeich
                queasy.char3 = t_article.vhpbezeich
                queasy.logi2 = t_article.tadaflag
                queasy.logi3 = t_article.vhpflag

    elif case_type == 3:

        for t_article in query(t_article_list):

            queasy = get_cache (Queasy, {"key": [(eq, 270)],"number1": [(eq, 2)],"betriebsnr": [(eq, deptno)],"number3": [(eq, vhp_artnr)]})

            if queasy:
                pass
                queasy.logi3 = article_flag

                h_artikel = get_cache (H_artikel, {"departement": [(eq, deptno)],"artnr": [(eq, vhp_artnr)]})

                if h_artikel:
                    h_artikel.activeflag = article_flag
                pass
                pass

    return generate_output()