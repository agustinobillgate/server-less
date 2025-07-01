#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Paramtext

def read_paramtextbl(case_type:int, p_txtno:int):
    p_text = ""
    t_paramtext_list = []
    from_number:int = 0
    to_number:int = 0
    do_it:bool = False
    paramtext = None

    t_paramtext = None

    t_paramtext_list, T_paramtext = create_model_like(Paramtext)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal p_text, t_paramtext_list, from_number, to_number, do_it, paramtext
        nonlocal case_type, p_txtno


        nonlocal t_paramtext
        nonlocal t_paramtext_list

        return {"p_text": p_text, "t-paramtext": t_paramtext_list}

    if case_type == 1:

        paramtext = get_cache (Paramtext, {"txtnr": [(eq, p_txtno)]})

        if paramtext:
            p_text = paramtext.ptexte


    elif case_type == 2:

        paramtext = get_cache (Paramtext, {"txtnr": [(eq, p_txtno)]})

        if paramtext:
            p_text = paramtext.ptexte


            t_paramtext = T_paramtext()
            t_paramtext_list.append(t_paramtext)

            buffer_copy(paramtext, t_paramtext)
    elif case_type == 3:
        from_number = p_txtno
        to_number = p_txtno

        if from_number == 9201:
            to_number = 9299

        for paramtext in db_session.query(Paramtext).filter(
                 (Paramtext.txtnr >= from_number) & (Paramtext.txtnr <= to_number)).order_by(Paramtext.txtnr).all():
            do_it = True

            if from_number == 9201:
                do_it = (paramtext.notes != "")

            if do_it:
                t_paramtext = T_paramtext()
                t_paramtext_list.append(t_paramtext)

                buffer_copy(paramtext, t_paramtext)
    elif case_type == 4:

        paramtext = get_cache (Paramtext, {"txtnr": [(eq, p_txtno)]})

        if paramtext:
            p_text = paramtext.notes


    elif case_type == 5:

        for paramtext in db_session.query(Paramtext).filter(
                 (Paramtext.txtnr == p_txtno)).order_by(Paramtext._recid).all():
            t_paramtext = T_paramtext()
            t_paramtext_list.append(t_paramtext)

            buffer_copy(paramtext, t_paramtext)
    elif case_type == 6:

        for paramtext in db_session.query(Paramtext).filter(
                 (Paramtext.txtnr >= 9201) & (Paramtext.txtnr <= 9299)).order_by(Paramtext._recid).all():
            t_paramtext = T_paramtext()
            t_paramtext_list.append(t_paramtext)

            buffer_copy(paramtext, t_paramtext)
    elif case_type == 7:

        for paramtext in db_session.query(Paramtext).filter(
                 (Paramtext.txtnr == p_txtno) & (Paramtext.ptexte != "")).order_by(Paramtext._recid).all():
            t_paramtext = T_paramtext()
            t_paramtext_list.append(t_paramtext)

            buffer_copy(paramtext, t_paramtext)
    elif case_type == 8:

        paramtext = get_cache (Paramtext, {"txtnr": [(eq, 200)]})

        if paramtext:
            t_paramtext = T_paramtext()
            t_paramtext_list.append(t_paramtext)

            buffer_copy(paramtext, t_paramtext)

        paramtext = get_cache (Paramtext, {"txtnr": [(eq, 201)]})

        if paramtext:
            t_paramtext = T_paramtext()
            t_paramtext_list.append(t_paramtext)

            buffer_copy(paramtext, t_paramtext)

        paramtext = get_cache (Paramtext, {"txtnr": [(eq, 204)]})

        if paramtext:
            t_paramtext = T_paramtext()
            t_paramtext_list.append(t_paramtext)

            buffer_copy(paramtext, t_paramtext)
    elif case_type == 9:
        do_it = False

        paramtext = get_cache (Paramtext, {"txtnr": [(eq, 711)],"number": [(eq, p_txtno)]})

        if paramtext:
            do_it = True
            t_paramtext = T_paramtext()
            t_paramtext_list.append(t_paramtext)

            buffer_copy(paramtext, t_paramtext)

        paramtext = get_cache (Paramtext, {"txtnr": [(eq, 712)],"number": [(eq, p_txtno)]})

        if paramtext:
            t_paramtext = T_paramtext()
            t_paramtext_list.append(t_paramtext)

            buffer_copy(paramtext, t_paramtext)

        if do_it:

            paramtext = get_cache (Paramtext, {"txtnr": [(eq, 711)],"number": [(eq, 0)]})

            if paramtext:
                db_session.delete(paramtext)
                pass

            paramtext = get_cache (Paramtext, {"txtnr": [(eq, 712)],"number": [(eq, 0)]})

            if paramtext:
                db_session.delete(paramtext)
                pass

    return generate_output()