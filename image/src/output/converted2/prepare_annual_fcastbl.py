#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Nation, Htparam, Zimkateg, Zimmer

def prepare_annual_fcastbl():

    prepare_cache ([Nation, Htparam, Zimkateg])

    ci_date = None
    from_month = ""
    rm_serv = False
    foreign_rate = False
    ena_rmrev = False
    t_nation_list = []
    tot_room:int = 0
    inactive:int = 0
    nation = htparam = zimkateg = zimmer = None

    t_nation = None

    t_nation_list, T_nation = create_model("T_nation", {"bezeich":string, "kurzbez":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal ci_date, from_month, rm_serv, foreign_rate, ena_rmrev, t_nation_list, tot_room, inactive, nation, htparam, zimkateg, zimmer


        nonlocal t_nation
        nonlocal t_nation_list

        return {"ci_date": ci_date, "from_month": from_month, "rm_serv": rm_serv, "foreign_rate": foreign_rate, "ena_rmrev": ena_rmrev, "t-nation": t_nation_list}

    def sum_rooms():

        nonlocal ci_date, from_month, rm_serv, foreign_rate, ena_rmrev, t_nation_list, tot_room, inactive, nation, htparam, zimkateg, zimmer


        nonlocal t_nation
        nonlocal t_nation_list


        tot_room = 0
        inactive = 0

        for zimkateg in db_session.query(Zimkateg).filter(
                 (Zimkateg.verfuegbarkeit)).order_by(Zimkateg._recid).all():

            for zimmer in db_session.query(Zimmer).filter(
                     (Zimmer.zikatnr == zimkateg.zikatnr)).order_by(Zimmer._recid).all():

                if zimmer.sleeping:
                    tot_room = tot_room + 1
                else:
                    inactive = inactive + 1


    for nation in db_session.query(Nation).order_by(Nation._recid).all():
        t_nation = T_nation()
        t_nation_list.append(t_nation)

        t_nation.bezeich = nation.bezeich
        t_nation.kurzbez = nation.kurzbez

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate
    from_month = to_string(get_month(ci_date) , "99") + to_string(get_year(ci_date) , "9999")

    htparam = get_cache (Htparam, {"paramnr": [(eq, 128)]})
    rm_serv = not htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 143)]})
    foreign_rate = htparam.flogical
    sum_rooms()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 550)]})

    if htparam.feldtyp == 4 and htparam.flogical:
        ena_rmrev = True

    return generate_output()