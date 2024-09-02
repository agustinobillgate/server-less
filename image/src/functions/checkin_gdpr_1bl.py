from functions.additional_functions import *
import decimal
from models import Htparam, Queasy, Nation, Guest, Mc_guest

def checkin_gdpr_1bl(gastnr:int):
    err_flag = 0
    save_day = 0
    curr_nat:str = ""
    do_it:bool = False
    list_region:str = ""
    list_nat:str = ""
    loopi:int = 0
    htparam = queasy = nation = guest = mc_guest = None

    nation_list = None

    nation_list_list, Nation_list = create_model("Nation_list", {"nr":int, "kurzbez":str, "bezeich":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_flag, save_day, curr_nat, do_it, list_region, list_nat, loopi, htparam, queasy, nation, guest, mc_guest


        nonlocal nation_list
        nonlocal nation_list_list
        return {"err_flag": err_flag, "save_day": save_day}

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 466)).first()

    if htparam:
        save_day = htparam.fint

    nation_obj_list = []
    for nation, queasy in db_session.query(Nation, Queasy).join(Queasy,(Queasy.key == 6) &  (Queasy.number1 == Nation.untergruppe) &  (Queasy.char1.op("~")(".*europe.*"))).filter(
            (Nation.natcode == 0)).all():
        if nation._recid in nation_obj_list:
            continue
        else:
            nation_obj_list.append(nation._recid)


        nation_list = Nation_list()
        nation_list_list.append(nation_list)

        nation_list.nr = nationnr
        nation_list.kurzbez = nation.kurzbez
        nation_list.bezeich = entry(0, nation.bezeich, ";")

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 448)).first()

    if htparam:
        list_region = htparam.fchar

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 449)).first()

    if htparam:
        list_nat = htparam.fchar

    if list_region != "":
        for loopi in range(1,num_entries(list_region, ";")  + 1) :

            for nation in db_session.query(Nation).filter(
                    (Nation.natcode == 0) &  (Nation.untergruppe == to_int(entry(loopi - 1, list_region, ";")))).all():

                nation_list = query(nation_list_list, filters=(lambda nation_list :nation_list.nr == nationnr), first=True)

                if not nation_list:
                    nation_list = Nation_list()
                    nation_list_list.append(nation_list)

                    nation_list.nr = nationnr
                    nation_list.kurzbez = nation.kurzbez
                    nation_list.bezeich = entry(0, nation.bezeich, ";")

    if list_nat != "":
        for loopi in range(1,num_entries(list_nat, ";")  + 1) :

            for nation in db_session.query(Nation).filter(
                    (Nation.natcode == 0) &  (Nationnr == to_int(entry(loopi - 1, list_nat, ";")))).all():

                nation_list = query(nation_list_list, filters=(lambda nation_list :nation_list.nr == nationnr), first=True)

                if not nation_list:
                    nation_list = Nation_list()
                    nation_list_list.append(nation_list)

                    nation_list.nr = nationnr
                    nation_list.kurzbez = nation.kurzbez
                    nation_list.bezeich = entry(0, nation.bezeich, ";")

    guest = db_session.query(Guest).filter(
            (Guest.gastnr == gastnr)).first()

    if guest:

        mc_guest = db_session.query(Mc_guest).filter(
                (Mc_guest.gastnr == guest.gastnr)).first()

        if mc_guest:
            err_flag = 2

            return generate_output()
        do_it = True

        if do_it:

            if guest.land != " ":
                curr_nat = guest.land

                nation_list = query(nation_list_list, filters=(lambda nation_list :nation_list.kurzbez.lower()  == (curr_nat).lower()), first=True)

                if nation_list:
                    do_it = True


                else:
                    do_it = False

            if do_it == False:

                if guest.nation1 != " ":
                    curr_nat = guest.nation1

                    nation_list = query(nation_list_list, filters=(lambda nation_list :nation_list.kurzbez.lower()  == (curr_nat).lower()), first=True)

                    if nation_list:
                        do_it = True


                    else:
                        do_it = False

        if do_it :
            err_flag = 1

            return generate_output()