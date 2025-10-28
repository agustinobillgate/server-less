#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import datetime, date
from models import Queasy

import time

input_list_data, Input_list = create_model("Input_list", {"pvilanguage":int, "from_date":date, "to_date":date, "sorttype":int, "excl_tax":bool, "from_outlet":int, "to_outlet":int, "id_flag":string})

def rest_statsegment_go2_outlist_webbl(input_list_data:[Input_list]):
    out_param_list_data = []
    output_list_data = []
    counter:int = 0
    queasy = None

    output_list = input_list = out_param_list = bqueasy = pqueasy = tqueasy = None

    output_list_data, Output_list = create_model("Output_list", {"flag":string, "segm_no":string, "g_segm":string, "segm_gr":string, "pax":string, "proz_pax":string, "t_rev":string, "proz_trev":string, "m_pax":string, "proz_mpax":string, "m_rev":string, "proz_mrev":string, "y_pax":string, "proz_ypax":string, "y_rev":string, "proz_yrev":string})
    out_param_list_data, Out_param_list = create_model("Out_param_list", {"done_flag":bool, "msg_result":string})

    Bqueasy = create_buffer("Bqueasy",Queasy)
    Pqueasy = create_buffer("Pqueasy",Queasy)
    Tqueasy = create_buffer("Tqueasy",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal out_param_list_data, output_list_data, counter, queasy
        nonlocal bqueasy, pqueasy, tqueasy


        nonlocal output_list, input_list, out_param_list, bqueasy, pqueasy, tqueasy
        nonlocal output_list_data, out_param_list_data

        return {"out-param-list": out_param_list_data, "output-list": output_list_data}

    input_list_data_tmp = [Input_list
        (
            pvilanguage=item.pvilanguage,
            from_date=item.from_date,
            to_date=item.to_date,
            sorttype=item.sorttype,
            excl_tax=item.excl_tax,
            from_outlet=item.from_outlet,
            to_outlet=item.to_outlet,
            id_flag=item.id_flag,
        )

        for item in input_list_data
    ]

    input_list_data = input_list_data_tmp

    input_list = query(input_list_data, first=True)

    if not input_list:
        out_param_list = Out_param_list()
        out_param_list_data.append(out_param_list)

        out_param_list.done_flag = True
        out_param_list.msg_result = "No Input List Available."

        return generate_output()

    tmp_count = 0
    retry = 0

    while True:
        count = db_session.query(Queasy).filter(
            (Queasy.key == 280) &
            (Queasy.char1 == "rest stat guest segment")
        ).count()

        if count >= 50:
            break

        if tmp_count == 0 and retry > 60:
            break

        if tmp_count > 0 and tmp_count == count:
            break

        tmp_count = count
        retry += 1

        time.sleep(0.5)

    # queasy = get_cache (Queasy, {"key": [(eq, 280)],"char1": [(eq, "rest stat guest segment")]})
    # while None != queasy:

    queasy = Queasy()

    for queasy in db_session.query(Queasy).filter((Queasy.key == 280) & (Queasy.char1 == "rest stat guest segment")):

        if queasy.char3 == input_list.id_flag:
            counter = counter + 1

            if counter > 50:
                break

            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.segm_no = entry(0, queasy.char2, "|")
            output_list.g_segm = entry(1, queasy.char2, "|")
            output_list.segm_gr = entry(2, queasy.char2, "|")
            output_list.pax = entry(3, queasy.char2, "|")
            output_list.t_rev = entry(4, queasy.char2, "|")
            output_list.m_pax = entry(5, queasy.char2, "|")
            output_list.m_rev = entry(6, queasy.char2, "|")
            output_list.y_pax = entry(7, queasy.char2, "|")
            output_list.y_rev = entry(8, queasy.char2, "|")
            output_list.proz_pax = entry(9, queasy.char2, "|")
            output_list.proz_trev = entry(10, queasy.char2, "|")
            output_list.proz_mpax = entry(11, queasy.char2, "|")
            output_list.proz_mrev = entry(12, queasy.char2, "|")
            output_list.proz_ypax = entry(13, queasy.char2, "|")
            output_list.proz_yrev = entry(14, queasy.char2, "|")

            pass
            db_session.delete(queasy)

        curr_recid = queasy._recid
        # queasy = db_session.query(Queasy).filter((Queasy.key == 280) & (Queasy.char1 == ("Rest Stat Guest Segment").lower()) & (Queasy._recid > curr_recid)).first()

    out_param_list = Out_param_list()
    out_param_list_data.append(out_param_list)


    pqueasy = db_session.query(Pqueasy).filter(
             (Pqueasy.key == 280) & (Pqueasy.char1 == "rest stat guest segment") & (Pqueasy.char3 == input_list.id_flag)).first()

    if pqueasy:
        out_param_list.done_flag = False
    else:

        tqueasy = db_session.query(Tqueasy).filter(
                 (Tqueasy.key == 285) & (Tqueasy.char1 == "rest stat guest segment") & (Tqueasy.number1 == 1) & (Tqueasy.char2 == input_list.id_flag)).first()

        if tqueasy:
            out_param_list.done_flag = False
        else:
            out_param_list.done_flag = True

    output_list = query(output_list_data, first=True)

    if not output_list:
        out_param_list.done_flag = False
    else:
        out_param_list.done_flag = True

        for tqueasy in db_session.query(Tqueasy).filter(
                 (Tqueasy.key == 285) & (Tqueasy.char1 == "rest stat guest segment") & (Tqueasy.char2 == input_list.id_flag)).order_by(Tqueasy._recid).all():
            db_session.delete(tqueasy)
            pass

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 280) & (Queasy.char1 == "rest stat guest segment")).order_by(Queasy._recid).all():

            if queasy.char3 == input_list.id_flag:

                tqueasy = db_session.query(Tqueasy).filter(
                         (Tqueasy._recid == queasy._recid)).first()

                if tqueasy:
                    db_session.delete(tqueasy)
                    pass

    return generate_output()