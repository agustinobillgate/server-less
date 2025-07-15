from functions.additional_functions import *
import decimal
from datetime import date
from functions.prepare_view_staycostbl import prepare_view_staycostbl
from models import Htparam, Paramtext, Reservation, Res_line, Zimkateg, Guest, Sourccod, Segment

def nt_guestlist_csv():
    variable = None
    htl_name:str = ""
    output_loc:str = ""
    to_day:date = None
    restatus:str = ""
    rate_code:str = ""
    ci_date:date = None
    contcode:str = ""
    ct:str = ""
    curr_rmcat:str = ""
    t_str:str = ""
    str_arrangement:str = ""
    kurzbez:str = ""
    htparam = paramtext = reservation = res_line = zimkateg = guest = sourccod = segment = None

    output_list = t_res_line = None

    output_list_list, Output_list = create_model("Output_list", {"flag":int, "str":str, "str1":str})
    t_res_line_list, T_res_line = create_model("T_res_line", {"name":str, "zinr":str, "ankunft":date, "abreise":date})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal variable, htl_name, output_loc, to_day, restatus, rate_code, ci_date, contcode, ct, curr_rmcat, t_str, str_arrangement, kurzbez, htparam, paramtext, reservation, res_line, zimkateg, guest, sourccod, segment


        nonlocal output_list, t_res_line
        nonlocal output_list_list, t_res_line_list

        return {}


    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 418)).first()
    output_loc = htparam.fchar

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 87)).first()
    to_day = htparam.fdate - timedelta(days=1)

    paramtext = db_session.query(Paramtext).filter(
             (Paramtext.txtnr == 200)).first()
    htl_name = paramtext.ptexte


    OUTPUT STREAM s1 TO VALUE (output_loc + "guest-list.csv") UNBUFFERED

    for reservation in db_session.query(Reservation).filter(
             (Reservation.resdat == to_day) & (Reservation.activeflag <= 1)).order_by(Reservation.resdat, func.substring(Reservation.name, 0, 32)).all():

        res_line = db_session.query(Res_line).filter(
                 (Res_line.resnr == reservation.resnr) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 12) & (Res_line.resstatus != 99)).first()

        zimkateg = db_session.query(Zimkateg).filter(
                 (Zimkateg.zikatnr == res_line.zikatnr)).first()

        guest = db_session.query(Guest).filter(
                 (Guest.gastnr == reservation.gastnr)).first()

        sourccod = db_session.query(Sourccod).filter(
                 (Sourccod.source_code == reservation.resart)).first()

        segment = db_session.query(Segment).filter(
                 (Segment.segmentcode == reservation.segmentcode)).first()

        if res_line:
            ci_date, contcode, ct, curr_rmcat, t_str, str_arrangement, kurzbez, t_res_line_list, output_list_list = get_output(prepare_view_staycostbl(language_code, res_line.resnr, res_line.reslinnr))

            t_res_line = query(t_res_line_list, first=True)

            output_list = query(output_list_list, first=True)
            rate_code = entry(1, output_list.str, "-")

            if res_line.resstatus == 1:
                restatus = "Guaranted"

            elif res_line.resstatus == 2:
                restatus = "6 PM"

            elif res_line.resstatus == 3:
                restatus = "Tentative"

            elif res_line.resstatus == 4:
                restatus = "Waitlist"

            elif res_line.resstatus == 5:
                restatus = "Oral Confirm"

            elif res_line.resstatus == 6:
                restatus = "In House"

            elif res_line.resstatus == 8:
                restatus = "C/O"

            elif res_line.resstatus == 11:
                restatus = "Room Sharer"

            elif res_line.resstatus == 13:
                restatus = "Accompanying Guest"


    OUTPUT STREAM s1 CLOSE

    return generate_output()