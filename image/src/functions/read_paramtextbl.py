from functions.additional_functions import *
import decimal
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


        nonlocal t_paramtext
        nonlocal t_paramtext_list
        return {"p_text": p_text, "t-paramtext": t_paramtext_list}

    if case_type == 1:

        paramtext = db_session.query(Paramtext).filter(
                (Paramtext.txtnr == p_txtno)).first()

        if paramtext:
            p_text = paramtext.ptexte


    elif case_type == 2:

        paramtext = db_session.query(Paramtext).filter(
                (Paramtext.txtnr == p_txtno)).first()

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
                (Paramtext.txtnr >= from_number) &  (Paramtext.txtnr <= to_number)).all():
            do_it = True

            if from_number == 9201:
                do_it = (paramtext.notes != "")

            if do_it:
                t_paramtext = T_paramtext()
                t_paramtext_list.append(t_paramtext)

                buffer_copy(paramtext, t_paramtext)
    elif case_type == 4:

        paramtext = db_session.query(Paramtext).filter(
                (Paramtext.txtnr == p_txtno)).first()

        if paramtext:
            p_text = paramtext.notes


    elif case_type == 5:

        for paramtext in db_session.query(Paramtext).filter(
                (Paramtext.txtnr == p_txtno)).all():
            t_paramtext = T_paramtext()
            t_paramtext_list.append(t_paramtext)

            buffer_copy(paramtext, t_paramtext)
    elif case_type == 6:

        for paramtext in db_session.query(Paramtext).filter(
                (Paramtext.txtnr >= 9201) &  (Paramtext.txtnr <= 9299)).all():
            t_paramtext = T_paramtext()
            t_paramtext_list.append(t_paramtext)

            buffer_copy(paramtext, t_paramtext)
    elif case_type == 7:

        for paramtext in db_session.query(Paramtext).filter(
                (Paramtext.txtnr == p_txtno) &  (Paramtext.ptexte != "")).all():
            t_paramtext = T_paramtext()
            t_paramtext_list.append(t_paramtext)

            buffer_copy(paramtext, t_paramtext)
    elif case_type == 8:

        paramtext = db_session.query(Paramtext).filter(
                (Paramtext.txtnr == 200)).first()

        if paramtext:
            t_paramtext = T_paramtext()
            t_paramtext_list.append(t_paramtext)

            buffer_copy(paramtext, t_paramtext)

        paramtext = db_session.query(Paramtext).filter(
                (Paramtext.txtnr == 201)).first()

        if paramtext:
            t_paramtext = T_paramtext()
            t_paramtext_list.append(t_paramtext)

            buffer_copy(paramtext, t_paramtext)

        paramtext = db_session.query(Paramtext).filter(
                (Paramtext.txtnr == 204)).first()

        if paramtext:
            t_paramtext = T_paramtext()
            t_paramtext_list.append(t_paramtext)

            buffer_copy(paramtext, t_paramtext)
    elif case_type == 9:
        do_it = False

        paramtext = db_session.query(Paramtext).filter(
                (Paramtext.txtnr == 711) &  (Paramtext.number == p_txtno)).first()

        if paramtext:
            do_it = True
            t_paramtext = T_paramtext()
            t_paramtext_list.append(t_paramtext)

            buffer_copy(paramtext, t_paramtext)

        paramtext = db_session.query(Paramtext).filter(
                (Paramtext.txtnr == 712) &  (Paramtext.number == p_txtno)).first()

        if paramtext:
            t_paramtext = T_paramtext()
            t_paramtext_list.append(t_paramtext)

            buffer_copy(paramtext, t_paramtext)

        if do_it:

            paramtext = db_session.query(Paramtext).filter(
                    (Paramtext.txtnr == 711) &  (Paramtext.number == 0)).first()

            if paramtext:
                db_session.delete(paramtext)


            paramtext = db_session.query(Paramtext).filter(
                    (Paramtext.txtnr == 712) &  (Paramtext.number == 0)).first()

            if paramtext:
                db_session.delete(paramtext)


    return generate_output()