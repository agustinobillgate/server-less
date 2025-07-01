#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Artikel, Queasy

def prepare_bookengine_mapping_sales_articlebl(bookengid:int):

    prepare_cache ([Artikel, Queasy])

    t_mapping_sales_list = []
    artikel = queasy = None

    t_mapping_sales = None

    t_mapping_sales_list, T_mapping_sales = create_model("T_mapping_sales", {"articlevhp":string, "articlebe":string, "descr":string, "nr":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_mapping_sales_list, artikel, queasy
        nonlocal bookengid


        nonlocal t_mapping_sales
        nonlocal t_mapping_sales_list

        return {"t-mapping-sales": t_mapping_sales_list}

    for artikel in db_session.query(Artikel).filter(
             (Artikel.departement == 0) & (Artikel.artart == 0)).order_by(Artikel.bezeich).all():
        t_mapping_sales = T_mapping_sales()
        t_mapping_sales_list.append(t_mapping_sales)

        t_mapping_sales.articlevhp = to_string(artikel.artnr)
        t_mapping_sales.descr = artikel.bezeich
        t_mapping_sales.nr = artikel.artnr

        queasy = get_cache (Queasy, {"key": [(eq, 323)],"number1": [(eq, bookengid)],"number2": [(eq, artikel.artnr)]})

        if queasy:
            t_mapping_sales.articlebe = queasy.char2


        else:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 323
            queasy.number1 = bookengid
            queasy.number2 = artikel.artnr
            queasy.char1 = to_string(artikel.artnr)

    return generate_output()