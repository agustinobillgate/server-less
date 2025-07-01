#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Artikel, Hoteldpt, Zwkum, Ekum

def load_artikelbl(case_type:int, deptno:int):

    prepare_cache ([Artikel, Hoteldpt, Zwkum, Ekum])

    artikel_list_list = []
    t_artikel_list = []
    artikel = hoteldpt = zwkum = ekum = None

    t_artikel = artikel_list = None

    t_artikel_list, T_artikel = create_model_like(Artikel)
    artikel_list_list, Artikel_list = create_model("Artikel_list", {"artnr":int, "departement":int, "bezeich":string, "artart":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal artikel_list_list, t_artikel_list, artikel, hoteldpt, zwkum, ekum
        nonlocal case_type, deptno


        nonlocal t_artikel, artikel_list
        nonlocal t_artikel_list, artikel_list_list

        return {"artikel-list": artikel_list_list, "t-artikel": t_artikel_list}

    def create_abuff(inp_dept:int):

        nonlocal artikel_list_list, t_artikel_list, artikel, hoteldpt, zwkum, ekum
        nonlocal case_type, deptno


        nonlocal t_artikel, artikel_list
        nonlocal t_artikel_list, artikel_list_list

        abuff = None
        zbuff = None
        Abuff =  create_buffer("Abuff",Artikel)
        Zbuff =  create_buffer("Zbuff",Zwkum)

        for artikel in db_session.query(Artikel).filter(
                 (Artikel.departement == inp_dept)).order_by(Artikel._recid).all():
            abuff = Artikel()
            db_session.add(abuff)

            buffer_copy(artikel, abuff,except_fields=["departement","eigentuemer"])
            abuff.eigentuemer = False
            abuff.departement = deptno
            abuff.endkum = 100 + deptno

            if substring(abuff.bezeich, length(abuff.bezeich) - 1 - 1) == ("01").lower() :
                abuff.bezeich = substring(abuff.bezeich, 0, length(abuff.bezeich) - 2) + to_string(deptno, "99")
            pass
            pass

        for zwkum in db_session.query(Zwkum).filter(
                 (Zwkum.departement == inp_dept)).order_by(Zwkum._recid).all():
            zbuff = Zwkum()
            db_session.add(zbuff)

            buffer_copy(zwkum, zbuff,except_fields=["departement"])
            zbuff.departement = deptno


            pass
            pass

        ekum = get_cache (Ekum, {"eknr": [(eq, 100 + hoteldpt.num)]})

        if not ekum:
            ekum = Ekum()
            db_session.add(ekum)

            ekum.eknr = 100 + hoteldpt.num
            ekum.bezeich = hoteldpt.depart


            pass
            pass

    if case_type == 1:

        for artikel in db_session.query(Artikel).filter(
                 (Artikel.departement == deptno) & (Artikel.activeflag)).order_by(Artikel._recid).all():
            artikel_list = Artikel_list()
            artikel_list_list.append(artikel_list)

            buffer_copy(artikel, artikel_list)

    elif case_type == 2:

        for artikel in db_session.query(Artikel).filter(
                 (Artikel.departement == deptno) & (Artikel.activeFLag)).order_by(Artikel._recid).all():
            t_artikel = T_artikel()
            t_artikel_list.append(t_artikel)

            buffer_copy(artikel, t_artikel)

    elif case_type == 3:

        for artikel in db_session.query(Artikel).filter(
                 (Artikel.departement == 0) & ((Artikel.artart == 2) | (Artikel.artart == 7)) & (Artikel.activeflag)).order_by(Artikel._recid).all():
            t_artikel = T_artikel()
            t_artikel_list.append(t_artikel)

            buffer_copy(artikel, t_artikel)

    elif case_type == 4:

        for artikel in db_session.query(Artikel).filter(
                 (Artikel.departement == 0) & ((Artikel.artart == 2) | (Artikel.artart == 7)) & (Artikel.activeflag)).order_by(Artikel._recid).all():
            artikel_list = Artikel_list()
            artikel_list_list.append(artikel_list)

            buffer_copy(artikel, artikel_list)

    elif case_type == 5:

        for artikel in db_session.query(Artikel).filter(
                 (Artikel.departement == 0) & (Artikel.artart == 2) & (Artikel.activeflag)).order_by(Artikel._recid).all():
            artikel_list = Artikel_list()
            artikel_list_list.append(artikel_list)

            buffer_copy(artikel, artikel_list)

    elif case_type == 6:

        for artikel in db_session.query(Artikel).filter(
                 (Artikel.departement == deptno)).order_by(Artikel._recid).all():
            t_artikel = T_artikel()
            t_artikel_list.append(t_artikel)

            buffer_copy(artikel, t_artikel)

    elif case_type == 7:

        for artikel in db_session.query(Artikel).filter(
                 (Artikel.departement == 0) & (Artikel.artart == 7) & (Artikel.activeflag)).order_by(Artikel._recid).all():
            artikel_list = Artikel_list()
            artikel_list_list.append(artikel_list)

            buffer_copy(artikel, artikel_list)

    elif case_type == 8:

        for artikel in db_session.query(Artikel).filter(
                 (Artikel.departement == deptno)).order_by(Artikel._recid).all():
            artikel_list = Artikel_list()
            artikel_list_list.append(artikel_list)

            buffer_copy(artikel, artikel_list)

    elif case_type == 9:

        for artikel in db_session.query(Artikel).filter(
                 (Artikel.departement == 0) & (Artikel.artart == 10) & (Artikel.activeflag)).order_by(Artikel.artnr).all():
            artikel_list = Artikel_list()
            artikel_list_list.append(artikel_list)

            buffer_copy(artikel, artikel_list)

    elif case_type == 10:

        for artikel in db_session.query(Artikel).filter(
                 (Artikel.departement == 0) & (Artikel.artart == 4) & (Artikel.activeflag)).order_by(Artikel.artnr).all():
            artikel_list = Artikel_list()
            artikel_list_list.append(artikel_list)

            buffer_copy(artikel, artikel_list)

    elif case_type == 11:

        hoteldpt = get_cache (Hoteldpt, {"num": [(eq, deptno)]})

        if not hoteldpt:

            return generate_output()

        artikel = get_cache (Artikel, {"departement": [(eq, deptno)]})

        if artikel:

            for artikel in db_session.query(Artikel).filter(
                     (Artikel.departement == deptno)).order_by(Artikel._recid).all():
                t_artikel = T_artikel()
                t_artikel_list.append(t_artikel)

                buffer_copy(artikel, t_artikel)

            return generate_output()
        else:

            if hoteldpt.departtyp == 0:
                pass
            elif hoteldpt.departtyp == 1:
                create_abuff(91)
            elif hoteldpt.departtyp == 2:
                create_abuff(93)
            elif hoteldpt.departtyp == 3:
                create_abuff(94)
            elif hoteldpt.departtyp == 4:
                create_abuff(92)
            elif hoteldpt.departtyp == 5:
                create_abuff(93)
            elif hoteldpt.departtyp == 6:
                create_abuff(93)

            for artikel in db_session.query(Artikel).filter(
                     (Artikel.departement == deptno)).order_by(Artikel._recid).all():
                t_artikel = T_artikel()
                t_artikel_list.append(t_artikel)

                buffer_copy(artikel, t_artikel)

    return generate_output()