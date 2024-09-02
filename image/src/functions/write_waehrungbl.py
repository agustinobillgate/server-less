from functions.additional_functions import *
import decimal
from models import Waehrung, Res_line, Artikel, Htparam

def write_waehrungbl(case_type:int, t_waehrung:[T_waehrung]):
    successflag = False
    useflag:bool = False
    waehrung = res_line = artikel = htparam = None

    t_waehrung = None

    t_waehrung_list, T_waehrung = create_model_like(Waehrung)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal successflag, useflag, waehrung, res_line, artikel, htparam


        nonlocal t_waehrung
        nonlocal t_waehrung_list
        return {"successflag": successflag}

    t_waehrung = query(t_waehrung_list, first=True)

    if not t_waehrung:

        return generate_output()

    if case_type == 1:
        waehrung = Waehrung()
        db_session.add(waehrung)

        buffer_copy(t_waehrung, waehrung)

        successflag = True
    elif case_type == 2:

        waehrung = db_session.query(Waehrung).filter(
                (Waehrungsnr == t_Waehrungsnr)).first()

        if waehrung:
            buffer_copy(t_waehrung, waehrung)

            waehrung = db_session.query(Waehrung).first()
            successflag = True
    elif case_type == 3:

        waehrung = db_session.query(Waehrung).filter(
                (Waehrungsnr == t_Waehrungsnr)).first()

        if waehrung:

            res_line = db_session.query(Res_line).filter(
                    (Res_line.betriebsnr == waehrungsnr)).first()
            useflag = None != res_line

            if not useflag:

                artikel = db_session.query(Artikel).filter(
                        (Artikel.departement < 90) &  (Artikel.betriebsnr == waehrungsnr)).first()
                useflag = None != artikel

            if not useflag:

                htparam = db_session.query(Htparam).filter(
                        (Htparam.paramnr == 152)).first()

                if htparam.fchar == waehrung.wabkurz:

                    htparam = db_session.query(Htparam).first()
                    htparam.fchar = ""

                    htparam = db_session.query(Htparam).first()


                waehrung = db_session.query(Waehrung).first()
                db_session.delete(waehrung)

                successflag = True

    return generate_output()