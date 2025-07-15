#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Guest, Genstat, Res_line, Queasy

def guest_purposestatbl(f_date:date, t_date:date, pur_stay:string, mi_ch:string):

    prepare_cache ([Guest, Genstat, Res_line, Queasy])

    gmember_data = []
    s:string = ""
    num:int = 0
    number:int = 0
    pur_nr:int = 0
    p_nr:int = 0
    guest = genstat = res_line = queasy = None

    gmember = None

    gmember_data, Gmember = create_model("Gmember", {"nr":int, "name":string, "adresse1":string, "email_adr":string, "ankunft":date, "abreise":date})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal gmember_data, s, num, number, pur_nr, p_nr, guest, genstat, res_line, queasy
        nonlocal f_date, t_date, pur_stay, mi_ch


        nonlocal gmember
        nonlocal gmember_data

        return {"gmember": gmember_data}

    def disp_arlist():

        nonlocal gmember_data, s, num, number, pur_nr, p_nr, guest, genstat, res_line, queasy
        nonlocal f_date, t_date, pur_stay, mi_ch


        nonlocal gmember
        nonlocal gmember_data

        genstat_obj_list = {}
        genstat = Genstat()
        guest = Guest()
        for genstat.gastnrmember, genstat.res_char, genstat._recid, guest.name, guest.anrede1, guest.adresse1, guest.email_adr, guest._recid in db_session.query(Genstat.gastnrmember, Genstat.res_char, Genstat._recid, Guest.name, Guest.anrede1, Guest.adresse1, Guest.email_adr, Guest._recid).join(Guest,(Guest.gastnr == Genstat.gastnrmember)).filter(
                 (Genstat.datum >= f_date) & (Genstat.datum <= t_date) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)])).order_by(Guest.name).all():
            if genstat_obj_list.get(genstat._recid):
                continue
            else:
                genstat_obj_list[genstat._recid] = True

            res_line = get_cache (Res_line, {"gastnrmember": [(eq, genstat.gastnrmember)]})

            if res_line:
                p_nr = 0
                for num in range(1,num_entries(genstat.res_char[1], ";")  + 1) :
                    s = entry(num - 1, genstat.res_char[1], ";")

                    if matches(s,r"SEGM_PUR*"):
                        p_nr = to_int(substring(s, get_index(s, "SEGM_PUR") + 8 - 1))

                queasy = get_cache (Queasy, {"key": [(eq, 143)],"char3": [(eq, pur_stay)]})

                if queasy:
                    pur_nr = queasy.number1

                if pur_stay.lower()  == ("UNKNOWN").lower() :
                    pur_nr = 0

                if pur_nr == p_nr:
                    gmember = Gmember()
                    gmember_data.append(gmember)

                    gmember.name = guest.name + guest.anrede1
                    gmember.adresse1 = guest.adresse1
                    gmember.email_adr = guest.email_adr
                    gmember.ankunft = res_line.ankunft
                    gmember.abreise = res_line.abreise

    disp_arlist()

    return generate_output()