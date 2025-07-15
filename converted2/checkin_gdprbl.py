#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from sqlalchemy import func
from models import Queasy, Nation, Guest, Mc_guest

def checkin_gdprbl(gastnr:int):

    prepare_cache ([Nation, Guest])

    err_flag = 0
    curr_nat:string = ""
    queasy = nation = guest = mc_guest = None

    nation_list = None

    nation_list_data, Nation_list = create_model("Nation_list", {"nr":int, "kurzbez":string, "bezeich":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_flag, curr_nat, queasy, nation, guest, mc_guest
        nonlocal gastnr


        nonlocal nation_list
        nonlocal nation_list_data

        return {"err_flag": err_flag}

    nation_obj_list = {}
    for nation, queasy in db_session.query(Nation, Queasy).join(Queasy,(Queasy.key == 6) & (Queasy.number1 == Nation.untergruppe) & (matches(Queasy.char1,"*europe*"))).filter(
             (Nation.natcode == 0)).order_by(Nation.kurzbez).all():
        if nation_obj_list.get(nation._recid):
            continue
        else:
            nation_obj_list[nation._recid] = True


        nation_list = Nation_list()
        nation_list_data.append(nation_list)

        nation_list.nr = nation.nationnr
        nation_list.kurzbez = nation.kurzbez
        nation_list.bezeich = entry(0, nation.bezeich, ";")

    guest = get_cache (Guest, {"gastnr": [(eq, gastnr)]})

    if guest:

        if guest.land != " ":
            curr_nat = guest.land

        elif guest.nation1 != " ":
            curr_nat = guest.nation1

        nation_list = query(nation_list_data, filters=(lambda nation_list: nation_list.kurzbez.lower()  == (curr_nat).lower()), first=True)

        if nation_list:
            err_flag = 1

        mc_guest = get_cache (Mc_guest, {"gastnr": [(eq, guest.gastnr)]})

        if mc_guest:
            err_flag = 2

    return generate_output()