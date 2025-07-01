#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import L_untergrup, Queasy, Gl_acct

def inv_checking_create_glbl():

    prepare_cache ([L_untergrup, Queasy, Gl_acct])

    artikel3_list = []
    l_untergrup = queasy = gl_acct = None

    artikel3 = None

    artikel3_list, Artikel3 = create_model("Artikel3", {"kum":int, "zeich2":string, "numb":int, "fibu":string, "zeich3":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal artikel3_list, l_untergrup, queasy, gl_acct


        nonlocal artikel3
        nonlocal artikel3_list

        return {"artikel3": artikel3_list}

    def create_gl():

        nonlocal artikel3_list, l_untergrup, queasy, gl_acct


        nonlocal artikel3
        nonlocal artikel3_list


        artikel3_list.clear()

        for l_untergrup in db_session.query(L_untergrup).order_by(L_untergrup._recid).all():

            queasy = get_cache (Queasy, {"key": [(eq, 29)],"number2": [(eq, l_untergrup.zwkum)]})

            if queasy:

                gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, l_untergrup.fibukonto)]})
                artikel3 = Artikel3()
                artikel3_list.append(artikel3)

                artikel3.kum = l_untergrup.zwkum
                artikel3.zeich2 = l_untergrup.bezeich
                artikel3.numb = queasy.number1
                artikel3.fibu = gl_acct.fibukonto
                artikel3.zeich3 = gl_acct.bezeich

    create_gl()

    return generate_output()