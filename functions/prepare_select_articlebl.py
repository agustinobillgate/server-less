from functions.additional_functions import *
import decimal
from models import Htparam, Artikel, Hoteldpt

def prepare_select_articlebl(case_type:int, departement:int):
    c_862:int = 0
    c_892:int = 0
    str_list_list = []
    htparam = artikel = hoteldpt = None

    str_list = None

    str_list_list, Str_list = create_model("Str_list", {"nr":int, "bezeich":str, "used":bool})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal c_862, c_892, str_list_list, htparam, artikel, hoteldpt
        nonlocal case_type, departement


        nonlocal str_list
        nonlocal str_list_list
        return {"str-list": str_list_list}

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 862)).first()
    c_862 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 892)).first()
    c_892 = htparam.finteger

    if case_type == 1:

        for artikel in db_session.query(Artikel).filter(
                 (Artikel.artart == 7)).order_by(Artikel._recid).all():
            str_list = Str_list()
            str_list_list.append(str_list)

            str_list.nr = artikel.artnr
            str_list.bezeich = artikel.bezeich

    elif case_type == 2:

        for artikel in db_session.query(Artikel).filter(
                 (Artikel.artart == 2)).order_by(Artikel._recid).all():
            str_list = Str_list()
            str_list_list.append(str_list)

            str_list.nr = artikel.artnr
            str_list.bezeich = artikel.bezeich

    elif case_type == 3:

        for artikel in db_session.query(Artikel).filter(
                 (Artikel.artart == 6) & (Artikel.umsatzart == 0)).order_by(Artikel._recid).all():
            str_list = Str_list()
            str_list_list.append(str_list)

            str_list.nr = artikel.artnr
            str_list.bezeich = artikel.bezeich

    elif case_type == 4:

        for artikel in db_session.query(Artikel).filter(
                 (Artikel.artart == 6) & (Artikel.umsatzart == 4)).order_by(Artikel._recid).all():
            str_list = Str_list()
            str_list_list.append(str_list)

            str_list.nr = artikel.artnr
            str_list.bezeich = artikel.bezeich

    elif case_type == 5:

        for artikel in db_session.query(Artikel).filter(
                 (Artikel.artart == 5)).order_by(Artikel._recid).all():
            str_list = Str_list()
            str_list_list.append(str_list)

            str_list.nr = artikel.artnr
            str_list.bezeich = artikel.bezeich

    elif case_type == 6:

        for hoteldpt in db_session.query(Hoteldpt).order_by(Hoteldpt._recid).all():
            str_list = Str_list()
            str_list_list.append(str_list)

            str_list.nr = hoteldpt.num
            str_list.bezeich = hoteldpt.depart

    elif case_type == 7:

        for artikel in db_session.query(Artikel).filter(
                 (Artikel.departement == departement)).order_by(Artikel._recid).all():
            str_list = Str_list()
            str_list_list.append(str_list)

            str_list.nr = artikel.artnr
            str_list.bezeich = artikel.bezeich

    elif case_type == 8:

        for artikel in db_session.query(Artikel).filter(
                 (Artikel.endkum == c_862) & (Artikel.departement == departement)).order_by(Artikel._recid).all():
            str_list = Str_list()
            str_list_list.append(str_list)

            str_list.nr = artikel.artnr
            str_list.bezeich = artikel.bezeich

    elif case_type == 9:

        for artikel in db_session.query(Artikel).filter(
                 (Artikel.endkum == c_892) & (Artikel.departement == departement)).order_by(Artikel._recid).all():
            str_list = Str_list()
            str_list_list.append(str_list)

            str_list.nr = artikel.artnr
            str_list.bezeich = artikel.bezeich

    elif case_type == 10:

        for artikel in db_session.query(Artikel).filter(
                 ((Artikel.artart == 0) | (Artikel.artart == 8)) & (Artikel.umsatzart == 1) & (Artikel.departement == departement)).order_by(Artikel._recid).all():
            str_list = Str_list()
            str_list_list.append(str_list)

            str_list.nr = artikel.artnr
            str_list.bezeich = artikel.bezeich

    elif case_type == 11:

        for artikel in db_session.query(Artikel).filter(
                 ((Artikel.artart == 0) | (Artikel.artart == 8)) & (Artikel.umsatzart == 4) & (Artikel.departement == departement)).order_by(Artikel._recid).all():
            str_list = Str_list()
            str_list_list.append(str_list)

            str_list.nr = artikel.artnr
            str_list.bezeich = artikel.bezeich

    return generate_output()