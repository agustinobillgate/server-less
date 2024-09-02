from functions.additional_functions import *
import decimal
from models import Paramtext

def write_paramtextbl(case_type:int, t_paramtext:[T_paramtext]):
    success_flag = False
    paramtext = None

    t_paramtext = None

    t_paramtext_list, T_paramtext = create_model_like(Paramtext)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, paramtext


        nonlocal t_paramtext
        nonlocal t_paramtext_list
        return {"success_flag": success_flag}

    t_paramtext = query(t_paramtext_list, first=True)

    if not t_paramtext:

        return generate_output()

    if case_type == 1:

        paramtext = db_session.query(Paramtext).filter(
                (Paramtext.txtnr == t_Paramtext.txtnr) &  (Paramtext.number == t_Paramtext.number) &  (Paramtext.sprachcode == t_Paramtext.sprachcode)).first()

        if paramtext:
            buffer_copy(t_paramtext, paramtext)

            paramtext = db_session.query(Paramtext).first()
            success_flag = True
    elif case_type == 2:
        paramtext = Paramtext()
        db_session.add(paramtext)

        buffer_copy(t_paramtext, paramtext)
        success_flag = True

        paramtext = db_session.query(Paramtext).first()
    elif case_type == 3:

        for t_paramtext in query(t_paramtext_list):

            paramtext = db_session.query(Paramtext).filter(
                    (Paramtext.txtnr == t_Paramtext.txtnr) &  (Paramtext.number == t_Paramtext.number) &  (Paramtext.sprachcode == t_Paramtext.sprachcode)).first()

            if not paramtext:

                paramtext = db_session.query(Paramtext).filter(
                        (Paramtext.txtnr == t_Paramtext.betriebsnr) &  (Paramtext.number == t_Paramtext.number) &  (Paramtext.sprachcode == t_Paramtext.sprachcode)).first()

            if paramtext:

                paramtext = db_session.query(Paramtext).first()
                buffer_copy(t_paramtext, paramtext)

                paramtext = db_session.query(Paramtext).first()

                success_flag = True
            else:
                paramtext = Paramtext()
                db_session.add(paramtext)

                buffer_copy(t_paramtext, paramtext)
                success_flag = True

                paramtext = db_session.query(Paramtext).first()
    elif case_type == 4:

        paramtext = db_session.query(Paramtext).filter(
                (Paramtext.txtnr == t_Paramtext.txtnr)).first()

        if not paramtext:
            paramtext = Paramtext()
        db_session.add(paramtext)

        buffer_copy(t_paramtext, paramtext)

        paramtext = db_session.query(Paramtext).first()
        success_flag = True

    return generate_output()