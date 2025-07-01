#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

t_mapping_sales_list, T_mapping_sales = create_model("T_mapping_sales", {"articlevhp":string, "articlebe":string, "descr":string, "nr":int})

def bookengine_mapping_sales_article_btn_exitbl(t_mapping_sales_list:[T_mapping_sales], bookengid:int):

    prepare_cache ([Queasy])

    queasy = None

    t_mapping_sales = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal queasy
        nonlocal bookengid


        nonlocal t_mapping_sales

        return {}

    for t_mapping_sales in query(t_mapping_sales_list):

        queasy = get_cache (Queasy, {"key": [(eq, 323)],"number1": [(eq, bookengid)],"number2": [(eq, t_mapping_sales.nr)]})

        if queasy:
            queasy.char2 = t_mapping_sales.articleBE


        else:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 323
            queasy.number1 = bookengid
            queasy.number2 = t_mapping_sales.nr
            queasy.char1 = t_mapping_sales.articleVHP

    return generate_output()