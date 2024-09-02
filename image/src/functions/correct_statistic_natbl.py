from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Nation

def correct_statistic_natbl(a_char:str):
    t_nationnr = 0
    t_bezeich = ""
    nation = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_nationnr, t_bezeich, nation


        return {"t_nationnr": t_nationnr, "t_bezeich": t_bezeich}


    nation = db_session.query(Nation).filter(
            (func.lower(Nation.kurzbez) == (a_char).lower())).first()
    t_nationnr = nationnr
    t_bezeich = nation.bezeich

    return generate_output()