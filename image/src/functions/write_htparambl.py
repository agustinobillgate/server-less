from functions.additional_functions import *
import decimal
from models import Htparam, Nation

def write_htparambl(case_type:int, t_htparam:[T_htparam]):
    success_flag = False
    prev_natcode:int = 0
    new_natcode:int = 0
    htparam = nation = None

    t_htparam = htbuff = natbuff = None

    t_htparam_list, T_htparam = create_model_like(Htparam)

    Htbuff = Htparam
    Natbuff = Nation

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, prev_natcode, new_natcode, htparam, nation
        nonlocal htbuff, natbuff


        nonlocal t_htparam, htbuff, natbuff
        nonlocal t_htparam_list
        return {"success_flag": success_flag}

    t_htparam = query(t_htparam_list, first=True)

    if not t_htparam:

        return generate_output()

    if case_type == 1:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == t_Htparam.paramnr)).first()

        if htparam:

            htbuff = db_session.query(Htbuff).filter(
                    (Htbuff._recid == htparam._recid)).first()
            buffer_copy(t_htparam, htbuff)

            htbuff = db_session.query(Htbuff).first()

            success_flag = True
    elif case_type == 2:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == t_Htparam.paramnr)).first()

        if htparam:

            htbuff = db_session.query(Htbuff).filter(
                    (Htbuff._recid == htparam._recid)).first()
            htbuff.fdate = t_htparam.fdate

            htbuff = db_session.query(Htbuff).first()

            success_flag = True
    elif case_type == 3:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == t_Htparam.paramnr)).first()

        if htparam:

            if t_htparam.paramnr == 153 and t_htparam.fchar != None:

                if htparam.fchar != t_htparam.fchar:

                    nation = db_session.query(Nation).filter(
                            (Nation.kurzbez == htparam.fchar)).first()

                    if nation:
                        prev_natcode = nationnr

                    nation = db_session.query(Nation).filter(
                            (Nation.kurzbez == t_htparam.fchar)).first()
                    new_natcode = nationnr

                    if prev_natcode != 0:

                        nation = db_session.query(Nation).filter(
                                (Nation.natcode == prev_natcode)).first()
                        while None != nation:

                            natbuff = db_session.query(Natbuff).filter(
                                        (Natbuff._recid == nation._recid)).first()
                            natbuff.natcode = new_natcode

                            natbuff = db_session.query(Natbuff).first()

                            nation = db_session.query(Nation).filter(
                                    (Nation.natcode == prev_natcode)).first()

            htbuff = db_session.query(Htbuff).filter(
                        (Htbuff._recid == htparam._recid)).first()

            if t_htparam.finteger != None:
                htbuff.finteger = t_htparam.finteger

            if t_htparam.fdecimal != None:
                htbuff.fdecimal = t_htparam.fdecimal

            if t_htparam.fdate != None:
                htbuff.fdate = t_htparam.fdate

            if t_htparam.flogical != None:
                htbuff.flogical = t_htparam.flogical

            if t_htparam.fchar != None:
                htbuff.fchar = t_htparam.fchar

            htbuff = db_session.query(Htbuff).first()

            success_flag = True

    elif case_type == 4:

        for t_htparam in query(t_htparam_list):

            htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == t_Htparam.paramnr)).first()
            buffer_copy(t_htparam, htparam)

            htparam = db_session.query(Htparam).first()
        success_flag = True

    return generate_output()