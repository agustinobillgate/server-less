from functions.additional_functions import *
import decimal
from datetime import date
from functions.htpdate import htpdate
from models import Zimmer, Res_line, Guestseg

def hk_rmboy_rmlistbl(loc_combo:str, stat1:str, stat2:str, stat3:str, stat4:str):
    credit = 0
    rmlist_list = []
    ci_date:date = None
    stat_list:List[str] = create_empty_list(4,"")
    zimmer = res_line = guestseg = None

    rmlist = None

    rmlist_list, Rmlist = create_model("Rmlist", {"flag":int, "code":str, "zinr":str, "credit":int, "floor":int, "gname":str, "pic":str, "bemerk":str, "rstat":str, "ankunft":date, "abreise":date, "kbezeich":str, "nation":str, "paxnr":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal credit, rmlist_list, ci_date, stat_list, zimmer, res_line, guestseg
        nonlocal loc_combo, stat1, stat2, stat3, stat4


        nonlocal rmlist
        nonlocal rmlist_list
        return {"credit": credit, "rmlist": rmlist_list}

    def create_rmlist():

        nonlocal credit, rmlist_list, ci_date, stat_list, zimmer, res_line, guestseg
        nonlocal loc_combo, stat1, stat2, stat3, stat4


        nonlocal rmlist
        nonlocal rmlist_list

        last_code:str = "1"
        do_it:bool = False
        room = None
        Room =  create_buffer("Room",Zimmer)
        rmlist_list.clear()
        credit = 0

        for room in db_session.query(Room).filter(
                (Room.zistatus >= 2) &  (Room.zistatus <= 4)).order_by(Room._recid).all():

            if loc_combo.lower()  == ("ALL").lower() :
                do_it = True
            else:
                do_it = room.code == loc_combo

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

                if room.zistatus == 3 or room.zistatus == 4:

                    # if not res_line or not(res_line.active_flag == 1 and res_line.zinr == room.zinr):
                    res_line = db_session.query(Res_line).filter(
                            (Res_line.active_flag == 1) &  (Res_line.zinr == room.zinr)).first()  

                    if res_line:
                        rmlist.bemerk = res_line.bemerk
                        rmlist.ankunft = res_line.ankunft
                        rmlist.abreise = res_line.abreise

                        if not guestseg or not(guestseg.gastnr == res_line.gastnrmember):
                            guestseg = db_session.query(Guestseg).filter(
                                (Guestseg.gastnr == res_line.gastnrmember)).first()

                        if guestseg:
                            rmlist.gname = guestseg.name + ", " + guestseg.vorname1 +\
                                    " " + guestseg.anrede1
                            rmlist.nation = guestseg.nation1

                if room.reihenfolge == 0:
                    credit = credit + 1
                else:
                    credit = credit + room.reihenfolge

        for res_line in db_session.query(Res_line).filter(
                (Res_line.resstatus == 6) &  (Res_line.abreise == ci_date)).order_by(Res_line.zinr).all():

            # if not room or not(room.zinr == res_line.zinr):
            room = db_session.query(Room).filter(
                (Room.zinr == res_line.zinr)).first()

            if loc_combo.lower()  == ("ALL").lower() :
                do_it = True
            else:
                do_it = room.code == loc_combo

            if do_it:

                # if not rmlist or not(rmlist.zinr == res_line.zinr):
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

                    # if not guestseg or not(guestseg.gastnr == res_line.gastnrmember):
                    guestseg = db_session.query(Guestseg).filter(
                        (Guestseg.gastnr == res_line.gastnrmember)).first()

                    if guestseg:
                        rmlist.gname = guestseg.name + ", " + guestseg.vorname1 +\
                                " " + guestseg.anrede1
                        rmlist.nation = guestseg.nation1

                    if room.reihenfolge == 0:
                        credit = credit + 1
                    else:
                        credit = credit + room.reihenfolge

    stat_list[0] = stat1
    stat_list[1] = stat2
    stat_list[2] = stat3
    stat_list[3] = stat4


    ci_date = get_output(htpdate(87))
    create_rmlist()

    return generate_output()