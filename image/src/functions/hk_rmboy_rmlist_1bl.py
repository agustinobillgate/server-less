from functions.additional_functions import *
import decimal
from datetime import date
from functions.htpdate import htpdate
from models import Zimmer, Res_line, Guest

def hk_rmboy_rmlist_1bl(loc_combo:str, stat8:str, stat2:str, stat3:str, stat4:str, fr_floor:int, to_floor:int):
    credit = 0
    rmlist_list = []
    ci_date:date = None
    stat_list:List[str] = create_empty_list(8,"")
    zimmer = res_line = guest = None

    rmlist = None

    rmlist_list, Rmlist = create_model("Rmlist", {"flag":int, "code":str, "zinr":str, "credit":int, "floor":int, "gname":str, "pic":str, "bemerk":str, "rstat":str, "ankunft":date, "abreise":date, "kbezeich":str, "nation":str, "paxnr":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal credit, rmlist_list, ci_date, stat_list, zimmer, res_line, guest
        nonlocal loc_combo, stat8, stat2, stat3, stat4, fr_floor, to_floor


        nonlocal rmlist
        nonlocal rmlist_list
        return {"credit": credit, "rmlist": rmlist_list}

    def create_rmlist():

        nonlocal credit, rmlist_list, ci_date, stat_list, zimmer, res_line, guest
        nonlocal loc_combo, stat8, stat2, stat3, stat4, fr_floor, to_floor


        nonlocal rmlist
        nonlocal rmlist_list

        last_code:str = "1"
        do_it:bool = False
        room = None
        Room =  create_buffer("Room",Zimmer)
        rmlist_list.clear()
        credit = 0

        for room in db_session.query(Room).filter(
                ((Room.zistatus >= 2) &  (Room.zistatus <= 4)) |  (Room.zistatus == 8)).order_by(Room._recid).all():

            if loc_combo.lower()  == ("ALL").lower() :
                do_it = True
            else:
                do_it = room.code == loc_combo

            if do_it:

                if fr_floor != 0 or to_floor != 0:
                    do_it = room.etage >= fr_floor and room.etage <= to_floor

            if do_it:
                rmlist = Rmlist()
                rmlist_list.append(rmlist)

                rmlist.code = room.code
                rmlist.zinr = room.zinr
                rmlist.credit = room.reihenfolge
                rmlist.floor = room.etage
                rmlist.rstat = stat_list[room.zistatus - 1]
                rmlist.kbezeich = room.kbezeich

                if rmlist.credit == 0:
                    rmlist.credit = 1

                if (room.zistatus == 3 or room.zistatus == 4) or room.zistatus == 8:

                    if not res_line or not(res_line.active_flag == 1 and res_line.zinr == room.zinr):
                        res_line = db_session.query(Res_line).filter(
                            (Res_line.active_flag == 1) &  (Res_line.zinr == room.zinr)).first()

                    if res_line:
                        rmlist.bemerk = res_line.bemerk
                        rmlist.ankunft = res_line.ankunft
                        rmlist.abreise = res_line.abreise

                        if not guest or not(guest.gastnr == res_line.gastnrmember):
                            guest = db_session.query(Guest).filter(
                                (Guest.gastnr == res_line.gastnrmember)).first()

                        if guest:
                            rmlist.gname = guest.name + ", " + guest.vorname1 +\
                                    " " + guest.anrede1
                            rmlist.nation = guest.nation1

                if room.reihenfolge == 0:
                    credit = credit + 1
                else:
                    credit = credit + room.reihenfolge

        for res_line in db_session.query(Res_line).filter(
                (Res_line.resstatus == 6) &  (Res_line.abreise == ci_date)).order_by(Res_line.zinr).all():

            if not room or not(room.zinr == res_line.zinr):
                room = db_session.query(Room).filter(
                    (Room.zinr == res_line.zinr)).first()

            if loc_combo.lower()  == ("ALL").lower() :
                do_it = True
            else:
                do_it = room.code == loc_combo

            if do_it:

                if fr_floor != 0 or to_floor != 0:
                    do_it = room.etage >= fr_floor and room.etage <= to_floor

            if do_it:

                if not rmlist or not(rmlist.zinr == res_line.zinr):
                    rmlist = query(rmlist_list, filters=(lambda rmlist: rmlist.zinr == res_line.zinr), first=True)

                if not rmlist:
                    rmlist = Rmlist()
                    rmlist_list.append(rmlist)

                    rmlist.code = room.code
                    rmlist.zinr = room.zinr
                    rmlist.credit = room.reihenfolge
                    rmlist.floor = room.etage
                    rmlist.rstat = stat_list[2]
                    rmlist.kbezeich = room.kbezeich

                    if rmlist.credit == 0:
                        rmlist.credit = 1
                    rmlist.bemerk = res_line.bemerk
                    rmlist.ankunft = res_line.ankunft
                    rmlist.abreise = res_line.abreise

                    if not guest or not(guest.gastnr == res_line.gastnrmember):
                        guest = db_session.query(Guest).filter(
                            (Guest.gastnr == res_line.gastnrmember)).first()

                    if guest:
                        rmlist.gname = guest.name + ", " + guest.vorname1 +\
                                " " + guest.anrede1
                        rmlist.nation = guest.nation1

                    if room.reihenfolge == 0:
                        credit = credit + 1
                    else:
                        credit = credit + room.reihenfolge

    stat_list[7] = stat8
    stat_list[1] = stat2
    stat_list[2] = stat3
    stat_list[3] = stat4


    ci_date = get_output(htpdate(87))
    create_rmlist()

    return generate_output()