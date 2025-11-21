#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Paramtext

t_paramtext_data, T_paramtext = create_model("T_paramtext", {"betriebsnr":int, "notes":string, "number":int, "passwort":string, "ptexte":string, "sprachcode":int, "txtnr":int, "wert":bool})

def write_paramtextbl(case_type:int, t_paramtext_data:[T_paramtext]):
    success_flag: bool = False
    paramtext = None

    t_paramtext = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, paramtext
        nonlocal case_type

        nonlocal t_paramtext

        return {"success_flag": success_flag}

    t_paramtext = query(t_paramtext_data, first=True)

    if type(t_paramtext.betriebsnr) == str:
        t_paramtext.betriebsnr = to_int(t_paramtext.betriebsnr.strip())

    if not t_paramtext:

        return generate_output()

    if case_type == 1:

        paramtext = get_cache (Paramtext, {"txtnr": [(eq, t_paramtext.txtnr)],"number": [(eq, t_paramtext.number)],"sprachcode": [(eq, t_paramtext.sprachcode)]})

        if paramtext:
            buffer_copy(t_paramtext, paramtext)
            pass
            success_flag = True

    elif case_type == 2:
        paramtext = Paramtext()
        db_session.add(paramtext)

        buffer_copy(t_paramtext, paramtext)
        success_flag = True
        pass

    elif case_type == 3:

        for t_paramtext in query(t_paramtext_data):

            paramtext = get_cache (Paramtext, {"txtnr": [(eq, t_paramtext.txtnr)],"number": [(eq, t_paramtext.number)],"sprachcode": [(eq, t_paramtext.sprachcode)]})

            if not paramtext:

                paramtext = get_cache (Paramtext, {"txtnr": [(eq, t_paramtext.betriebsnr)],"number": [(eq, t_paramtext.number)],"sprachcode": [(eq, t_paramtext.sprachcode)]})

            if paramtext:
                pass
                buffer_copy(t_paramtext, paramtext)
                pass
                pass
                success_flag = True
            else:
                paramtext = Paramtext()
                db_session.add(paramtext)

                buffer_copy(t_paramtext, paramtext)
                success_flag = True
                pass

    elif case_type == 4:

        paramtext = get_cache (Paramtext, {"txtnr": [(eq, t_paramtext.txtnr)]})

        if not paramtext:
            paramtext = Paramtext()
            db_session.add(paramtext)

        buffer_copy(t_paramtext, paramtext)
        pass
        success_flag = True

    return generate_output()