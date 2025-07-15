from functions.additional_functions import *
import decimal
from models import L_untergrup, Queasy, Gl_acct

def inv_checking_create_gl_cldbl():
    artikel3_list = []
    l_untergrup = queasy = gl_acct = None

    artikel3 = None

    artikel3_list, Artikel3 = create_model("Artikel3", {"kum":int, "zeich2":str, "numb":int, "fibu":str, "zeich3":str})


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

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 29) &  (Queasy.number2 == l_untergrup.zwkum)).first()

            if queasy:

                gl_acct = db_session.query(Gl_acct).filter(
                        (Gl_acct.fibukonto == l_untergrup.fibukonto)).first()
                artikel3 = Artikel3()
                artikel3_list.append(artikel3)

                artikel3.kum = l_untergrup.zwkum
                artikel3.zeich2 = l_untergrup.bezeich
                artikel3.numb = queasy.number1
                artikel3.fibu = gl_acct.fibukonto
                artikel3.zeich3 = gl_acct.bezeich

    create_gl()

    return generate_output()