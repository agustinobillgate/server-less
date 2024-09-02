from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam, Ratecode, Zimkateg, Arrangement

def prepare_select_ratecode_1bl(gastnr:int):
    t_ratecode_list = []
    i:int = 0
    rcode:str = ""
    rmtype:str = ""
    htparam = ratecode = zimkateg = arrangement = None

    t_ratecode = None

    t_ratecode_list, T_ratecode = create_model("T_ratecode", {"code":str, "bez":str, "startdate":date, "enddate":date, "zikatnr":int, "roomtype":str, "argt":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_ratecode_list, i, rcode, rmtype, htparam, ratecode, zimkateg, arrangement


        nonlocal t_ratecode
        nonlocal t_ratecode_list
        return {"t-ratecode": t_ratecode_list}

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1020)).first()

    if htparam:

        if num_entries(htparam.fchar, ";") > 1:
            for i in range(1,num_entries(htparam.fchar, ";")  + 1) :
                rcode = entry(i - 1, htparam.fchar, ";")

                ratecode = db_session.query(Ratecode).filter(
                        (Ratecode.code == rcode)).first()

                if ratecode:
                    t_ratecode = T_ratecode()
                    t_ratecode_list.append(t_ratecode)

                    t_ratecode.code = rcode
                    t_ratecode.bez = ratecode.bezeichnung
                    t_ratecode.startDate = ratecode.startperiod
                    t_ratecode.endDate = ratecode.endperiod
                    t_ratecode.zikatnr = ratecode.zikatnr

                    zimkateg = db_session.query(Zimkateg).filter(
                            (to_int(Zimkateg.zikatnr) == ratecode.zikatnr)).first()

                    if zimkateg:
                        t_ratecode.roomType = zimkateg.kurzbez

                    arrangement = db_session.query(Arrangement).filter(
                            (Arrangement.argtnr == ratecode.argtnr)).first()

                    if arrangement:
                        t_ratecode.argt = arrangement

    return generate_output()