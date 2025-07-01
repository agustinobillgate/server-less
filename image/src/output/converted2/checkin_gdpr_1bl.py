#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from sqlalchemy import func
from models import Htparam, Queasy, Nation, Guest, Mc_guest

def checkin_gdpr_1bl(gastnr:int):

    prepare_cache ([Htparam, Nation, Guest])

    err_flag = 0
    save_day = 0
    curr_nat:string = ""
    do_it:bool = False
    list_region:string = ""
    list_nat:string = ""
    loopi:int = 0
    htparam = queasy = nation = guest = mc_guest = None

    nation_list = None

    nation_list_list, Nation_list = create_model("Nation_list", {"nr":int, "kurzbez":string, "bezeich":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_flag, save_day, curr_nat, do_it, list_region, list_nat, loopi, htparam, queasy, nation, guest, mc_guest
        nonlocal gastnr


        nonlocal nation_list
        nonlocal nation_list_list

        return {"err_flag": err_flag, "save_day": save_day}

    htparam = get_cache (Htparam, {"paramnr": [(eq, 466)]})

    if htparam:
        save_day = htparam.finteger

    nation_obj_list = {}
    for nation, queasy in db_session.query(Nation, Queasy).join(Queasy,(Queasy.key == 6) & (Queasy.number1 == Nation.untergruppe) & (matches(Queasy.char1,"*europe*"))).filter(
             (Nation.natcode == 0)).order_by(Nation.kurzbez).all():
        if nation_obj_list.get(nation._recid):
            continue
        else:
            nation_obj_list[nation._recid] = True


        nation_list = Nation_list()
        nation_list_list.append(nation_list)

        nation_list.nr = nation.nationnr
        nation_list.kurzbez = nation.kurzbez
        nation_list.bezeich = entry(0, nation.bezeich, ";")

    htparam = get_cache (Htparam, {"paramnr": [(eq, 448)]})

    if htparam:
        list_region = htparam.fchar

    htparam = get_cache (Htparam, {"paramnr": [(eq, 449)]})

    if htparam:
        list_nat = htparam.fchar

    if list_region != "":
        for loopi in range(1,num_entries(list_region, ";")  + 1) :

            for nation in db_session.query(Nation).filter(
                     (Nation.natcode == 0) & (Nation.untergruppe == to_int(entry(loopi - 1, list_region, ";")))).order_by(Nation.kurzbez).all():

                nation_list = query(nation_list_list, filters=(lambda nation_list: nation_list.nr == nation.nationnr), first=True)

                if not nation_list:
                    nation_list = Nation_list()
                    nation_list_list.append(nation_list)

                    nation_list.nr = nation.nationnr
                    nation_list.kurzbez = nation.kurzbez
                    nation_list.bezeich = entry(0, nation.bezeich, ";")

    if list_nat != "":
        for loopi in range(1,num_entries(list_nat, ";")  + 1) :

            for nation in db_session.query(Nation).filter(
                     (Nation.natcode == 0) & (Nation.nationnr == to_int(entry(loopi - 1, list_nat, ";")))).order_by(Nation.kurzbez).all():

                nation_list = query(nation_list_list, filters=(lambda nation_list: nation_list.nr == nation.nationnr), first=True)

                if not nation_list:
                    nation_list = Nation_list()
                    nation_list_list.append(nation_list)

                    nation_list.nr = nation.nationnr
                    nation_list.kurzbez = nation.kurzbez
                    nation_list.bezeich = entry(0, nation.bezeich, ";")

    guest = get_cache (Guest, {"gastnr": [(eq, gastnr)]})

    if guest:

        mc_guest = get_cache (Mc_guest, {"gastnr": [(eq, guest.gastnr)]})

        if mc_guest:
            err_flag = 2

            return generate_output()
        do_it = True

        if do_it:

            if guest.land != " ":
                curr_nat = guest.land

                nation_list = query(nation_list_list, filters=(lambda nation_list: nation_list.kurzbez.lower()  == (curr_nat).lower()), first=True)

                if nation_list:
                    do_it = True


                else:
                    do_it = False

            if do_it == False:

                if guest.nation1 != " ":
                    curr_nat = guest.nation1

                    nation_list = query(nation_list_list, filters=(lambda nation_list: nation_list.kurzbez.lower()  == (curr_nat).lower()), first=True)

                    if nation_list:
                        do_it = True


                    else:
                        do_it = False

        if do_it :
            err_flag = 1

            return generate_output()

    return generate_output()