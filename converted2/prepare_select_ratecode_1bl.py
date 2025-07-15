#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Ratecode, Zimkateg, Arrangement

def prepare_select_ratecode_1bl(gastnr:int):

    prepare_cache ([Htparam, Ratecode, Zimkateg, Arrangement])

    t_ratecode_data = []
    i:int = 0
    rcode:string = ""
    rmtype:string = ""
    htparam = ratecode = zimkateg = arrangement = None

    t_ratecode = None

    t_ratecode_data, T_ratecode = create_model("T_ratecode", {"code":string, "bez":string, "startdate":date, "enddate":date, "zikatnr":int, "roomtype":string, "argt":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_ratecode_data, i, rcode, rmtype, htparam, ratecode, zimkateg, arrangement
        nonlocal gastnr


        nonlocal t_ratecode
        nonlocal t_ratecode_data

        return {"t-ratecode": t_ratecode_data}

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1020)]})

    if htparam:

        if num_entries(htparam.fchar, ";") > 1:
            for i in range(1,num_entries(htparam.fchar, ";")  + 1) :
                rcode = entry(i - 1, htparam.fchar, ";")

                ratecode = get_cache (Ratecode, {"code": [(eq, rcode)]})

                if ratecode:
                    t_ratecode = T_ratecode()
                    t_ratecode_data.append(t_ratecode)

                    t_ratecode.code = rcode
                    t_ratecode.bez = ratecode.bezeichnung
                    t_ratecode.startdate = ratecode.startperiod
                    t_ratecode.enddate = ratecode.endperiod
                    t_ratecode.zikatnr = ratecode.zikatnr

                    zimkateg = db_session.query(Zimkateg).filter(
                             (to_int(Zimkateg.zikatnr) == ratecode.zikatnr)).first()

                    if zimkateg:
                        t_ratecode.roomtype = zimkateg.kurzbez

                    arrangement = get_cache (Arrangement, {"argtnr": [(eq, ratecode.argtnr)]})

                    if arrangement:
                        t_ratecode.argt = arrangement.arrangement

    return generate_output()