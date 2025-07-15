#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from functions.read_reservationbl import read_reservationbl
from functions.res_vouchernobl import res_vouchernobl
from functions.read_guestbl import read_guestbl
from models import Guest, Reservation

def res_voucherno1bl(voucher_no:string, fname:string):
    t_res_voucherno_data = []
    t_part_resline_data = []
    r_list_data = []
    tname:string = ""
    i:int = 0
    str:string = ""
    guest = reservation = None

    t_res_voucherno = t_part_resline = r_list = t_guest = t_reservation = t_voucherno = None

    t_res_voucherno_data, T_res_voucherno = create_model("T_res_voucherno", {"name":string, "vesrdepot":string, "resnr":int, "activeflag":int})
    t_part_resline_data, T_part_resline = create_model("T_part_resline", {"zimmer_wunsch":string, "gastnr":int, "name":string, "resnr":int})
    r_list_data, R_list = create_model("R_list", {"ta_name":string, "gname":string, "resnr":int, "voucher":string})
    t_guest_data, T_guest = create_model_like(Guest)
    t_reservation_data, T_reservation = create_model_like(Reservation)
    t_voucherno_data, T_voucherno = create_model_like(T_res_voucherno)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_res_voucherno_data, t_part_resline_data, r_list_data, tname, i, str, guest, reservation
        nonlocal voucher_no, fname


        nonlocal t_res_voucherno, t_part_resline, r_list, t_guest, t_reservation, t_voucherno
        nonlocal t_res_voucherno_data, t_part_resline_data, r_list_data, t_guest_data, t_reservation_data, t_voucherno_data

        return {"t-res-voucherNo": t_res_voucherno_data, "t-part-resline": t_part_resline_data, "r-list": r_list_data}

    t_reservation_data = get_output(read_reservationbl(3, 0, 0, voucher_no))

    t_reservation = query(t_reservation_data, first=True)

    if t_reservation:
        t_res_voucherNo_data, t_part_resline_data = get_output(res_vouchernobl(1, voucher_no, "", ""))
    else:

        if fname != "":
            tname = substring(fname, 0, 1) + "ZZZ"
            t_res_voucherNo_data, t_part_resline_data = get_output(res_vouchernobl(2, voucher_no, fname, tname))
        else:
            t_res_voucherNo_data, t_part_resline_data = get_output(res_vouchernobl(3, voucher_no, "", ""))
    r_list_data.clear()
    t_voucherNo_data, t_part_resline_data = get_output(res_vouchernobl(4, "", "", ""))

    for t_part_resline in query(t_part_resline_data):
        for i in range(1,num_entries(t_part_resline.zimmer_wunsch, ";") - 1 + 1) :
            str = entry(i - 1, t_part_resline.zimmer_wunsch, ";")

            if substring(str, 0, 7) == ("voucher").lower()  and matches(substring(str, 7),r"*" + voucher_no + r"*"):
                i = 999
                t_guest_data = get_output(read_guestbl(1, t_part_resline.gastnr, "", ""))

                t_guest = query(t_guest_data, first=True)
                r_list = R_list()
                r_list_data.append(r_list)

                r_list.ta_name = t_guest.name
                r_list.gname = t_part_resline.name
                r_list.resnr = t_part_resline.resnr
                r_list.voucher = substring(str, 7)

    return generate_output()