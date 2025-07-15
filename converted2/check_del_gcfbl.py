#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Guest, Res_line, Debitor, Akt_cust, Bill, Billhis, Kontline, Zimmer, Bk_veran, Mc_guest, Cl_member, Akt_kont, Htparam, Queasy

def check_del_gcfbl(gastnr:int):

    prepare_cache ([Guest, Queasy])

    error_code = 0
    mname = ""
    answer:bool = False
    gastno:string = ""
    guest = res_line = debitor = akt_cust = bill = billhis = kontline = zimmer = bk_veran = mc_guest = cl_member = akt_kont = htparam = queasy = None

    guest1 = None

    Guest1 = create_buffer("Guest1",Guest)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal error_code, mname, answer, gastno, guest, res_line, debitor, akt_cust, bill, billhis, kontline, zimmer, bk_veran, mc_guest, cl_member, akt_kont, htparam, queasy
        nonlocal gastnr
        nonlocal guest1


        nonlocal guest1

        return {"error_code": error_code, "mname": mname}

    def check_global_allotment():

        nonlocal error_code, mname, answer, gastno, guest, res_line, debitor, akt_cust, bill, billhis, kontline, zimmer, bk_veran, mc_guest, cl_member, akt_kont, htparam, queasy
        nonlocal gastnr
        nonlocal guest1


        nonlocal guest1

        error_code = 0
        tokcounter:int = 0
        mesvalue:string = ""

        def generate_inner_output():
            return (error_code)


        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 147)).order_by(Queasy._recid).yield_per(100):
            for tokcounter in range(1,num_entries(queasy.char3, ",")  + 1) :
                mesvalue = entry(tokcounter - 1, queasy.char3, ",")

                if mesvalue != "" and to_int(mesvalue) == gastnr:
                    error_code = 66
                    break

        return generate_inner_output()

    res_line = get_cache (Res_line, {"gastnr": [(eq, gastnr)]})

    if res_line:
        error_code = 1

        return generate_output()

    res_line = get_cache (Res_line, {"gastnrmember": [(eq, gastnr)]})

    if res_line:
        error_code = 1

        return generate_output()

    res_line = get_cache (Res_line, {"gastnrpay": [(eq, gastnr)]})

    if res_line:
        error_code = 1

        return generate_output()

    debitor = get_cache (Debitor, {"gastnr": [(eq, gastnr)],"zahlkonto": [(eq, 0)]})

    if debitor:
        error_code = 2

        return generate_output()

    debitor = get_cache (Debitor, {"gastnrmember": [(eq, gastnr)],"zahlkonto": [(eq, 0)]})

    if debitor:
        error_code = 2

        return generate_output()

    guest1 = get_cache (Guest, {"master_gastnr": [(eq, gastnr)],"gastnr": [(gt, 0)]})

    if guest1:
        error_code = 3
        mname = guest1.name.upper() + ", " + guest1.vorname1.upper() + " " + guest1.anredefirma.upper() + guest1.anrede1.upper()

        return generate_output()

    akt_cust = get_cache (Akt_cust, {"gastnr": [(eq, gastnr)]})

    if akt_cust:
        error_code = 4

        return generate_output()

    bill = get_cache (Bill, {"gastnr": [(eq, gastnr)]})

    if bill:
        error_code = 5

        return generate_output()

    billhis = get_cache (Billhis, {"gastnr": [(eq, gastnr)]})

    if billhis:
        error_code = 5

        return generate_output()

    kontline = get_cache (Kontline, {"gastnr": [(eq, gastnr)]})

    if kontline:
        error_code = 6

        return generate_output()
    error_code = check_global_allotment()

    if error_code > 0:

        return generate_output()

    zimmer = get_cache (Zimmer, {"owner_nr": [(eq, gastnr)]})

    if zimmer:
        error_code = 7

        return generate_output()

    bk_veran = get_cache (Bk_veran, {"gastnr": [(eq, gastnr)]})

    if bk_veran:
        error_code = 8

        return generate_output()

    mc_guest = get_cache (Mc_guest, {"gastnr": [(eq, gastnr)]})

    if mc_guest:
        error_code = 9

        return generate_output()

    cl_member = get_cache (Cl_member, {"gastnr": [(eq, gastnr)]})

    if cl_member:
        error_code = 10

        return generate_output()

    akt_kont = get_cache (Akt_kont, {"betrieb_gast": [(eq, gastnr)]})

    if akt_kont:
        error_code = 11

        return generate_output()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 615)]})

    if htparam:
        gastno = "*" + to_string(gastnr) + "*"

        if matches(htparam.fchar,gastno):
            error_code = 12

            return generate_output()

    return generate_output()