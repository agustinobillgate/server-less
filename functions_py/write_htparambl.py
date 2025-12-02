#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 27/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Htparam, Nation

t_htparam_data, T_htparam = create_model_like(Htparam)

def write_htparambl(case_type:int, t_htparam_data:[T_htparam]):

    prepare_cache ([Htparam, Nation])

    success_flag = False
    prev_natcode:int = 0
    new_natcode:int = 0
    htparam = nation = None

    t_htparam = htbuff = natbuff = None

    Htbuff = create_buffer("Htbuff",Htparam)
    Natbuff = create_buffer("Natbuff",Nation)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, prev_natcode, new_natcode, htparam, nation
        nonlocal case_type
        nonlocal htbuff, natbuff


        nonlocal t_htparam, htbuff, natbuff

        return {"success_flag": success_flag}

    t_htparam = query(t_htparam_data, first=True)

    if not t_htparam:

        return generate_output()

    if case_type == 1:

        htparam = get_cache (Htparam, {"paramnr": [(eq, t_htparam.paramnr)]})

        if htparam:

            # htbuff = get_cache (Htparam, {"_recid": [(eq, htparam._recid)]})
            htbuff = db_session.query(Htparam).filter(
                     (Htparam._recid == htparam._recid)).with_for_update().first
            buffer_copy(t_htparam, htbuff)
            pass
            pass
            success_flag = True
    elif case_type == 2:

        htparam = get_cache (Htparam, {"paramnr": [(eq, t_htparam.paramnr)]})

        if htparam:

            # htbuff = get_cache (Htparam, {"_recid": [(eq, htparam._recid)]})
            htbuff = db_session.query(Htparam).filter(
                     (Htparam._recid == htparam._recid)).with_for_update().first()
            htbuff.fdate = t_htparam.fdate


            pass
            pass
            success_flag = True
    elif case_type == 3:

        htparam = get_cache (Htparam, {"paramnr": [(eq, t_htparam.paramnr)]})

        if htparam:

            if t_htparam.paramnr == 153 and t_htparam.fchar != None:

                if htparam.fchar != t_htparam.fchar:

                    nation = get_cache (Nation, {"kurzbez": [(eq, htparam.fchar)]})

                    if nation:
                        prev_natcode = nation.nationnr

                    nation = get_cache (Nation, {"kurzbez": [(eq, t_htparam.fchar)]})
                    new_natcode = nation.nationnr

                    if prev_natcode != 0:

                        nation = get_cache (Nation, {"natcode": [(eq, prev_natcode)]})
                        while None != nation:

                            # natbuff = get_cache (Nation, {"_recid": [(eq, nation._recid)]})
                            natbuff = db_session.query(Nation).filter(
                                     (Nation._recid == nation._recid)).with_for_update().first()
                            natbuff.natcode = new_natcode


                            pass
                            pass

                            curr_recid = nation._recid
                            nation = db_session.query(Nation).filter(
                                     (Nation.natcode == prev_natcode) & (Nation._recid > curr_recid)).first()

            htbuff = get_cache (Htparam, {"_recid": [(eq, htparam._recid)]})

            if t_htparam.finteger != None:
                htbuff.finteger = t_htparam.finteger

            if t_htparam.fdecimal != None:
                htbuff.fdecimal =  to_decimal(t_htparam.fdecimal)

            if t_htparam.fdate != None:
                htbuff.fdate = t_htparam.fdate

            if t_htparam.flogical != None:
                htbuff.flogical = t_htparam.flogical

            if t_htparam.fchar != None:
                htbuff.fchar = t_htparam.fchar


            pass
            pass
            success_flag = True
    elif case_type == 4:

        for t_htparam in query(t_htparam_data):

            # htparam = get_cache (Htparam, {"paramnr": [(eq, t_htparam.paramnr)]})
            htparam = db_session.query(Htparam).filter(
                     (Htparam.paramnr == t_htparam.paramnr)).with_for_update().first()
            buffer_copy(t_htparam, htparam)
            pass
        success_flag = True

    return generate_output()