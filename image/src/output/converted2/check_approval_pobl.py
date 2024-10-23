from functions.additional_functions import *
import decimal
from datetime import date
from functions.htplogic import htplogic
from sqlalchemy import func
from models import Messages, Htparam, L_orderhdr, Queasy, Bediener

def check_approval_pobl(user_init:str):
    nr:int = 0
    loop_init:int = 0
    do_alert:bool = False
    app_lvl:int = 0
    use_po_esignature:bool = False
    billdate:date = None
    a:str = ""
    b:str = ""
    c:str = ""
    d:str = ""
    messages = htparam = l_orderhdr = queasy = bediener = None

    po_list = q245 = mess_list = qsy_list = bmessage = None

    po_list_list, Po_list = create_model("Po_list", {"lief_nr":int, "docu_nr":str, "bestelldatum":date, "lieferdatum":date, "wabkurz":str, "bestellart":str, "gedruckt":date, "besteller":str, "lief_fax_3":str, "lief_fax_2":str, "rechnungswert":decimal, "rec_id":int, "approval_lvl":[bool,4], "approval_id":[str,4], "need_approval":str})
    q245_list, Q245 = create_model("Q245", {"key":int, "docu_nr":str, "user_init":str, "app_id":str, "app_no":int, "sign_id":int})
    mess_list_list, Mess_list = create_model("Mess_list", {"nr":int, "reslinnr":int, "betriebsnr":int, "mess_recid":int, "datum":date, "mess_str":str})
    qsy_list_list, Qsy_list = create_model("Qsy_list", {"docu_nr":str})

    Bmessage = create_buffer("Bmessage",Messages)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal nr, loop_init, do_alert, app_lvl, use_po_esignature, billdate, a, b, c, d, messages, htparam, l_orderhdr, queasy, bediener
        nonlocal user_init
        nonlocal bmessage


        nonlocal po_list, q245, mess_list, qsy_list, bmessage
        nonlocal po_list_list, q245_list, mess_list_list, qsy_list_list
        return {}

    use_po_esignature = get_output(htplogic(71))

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 110)).first()
    billdate = htparam.fdate
    a = to_string(get_current_time_in_seconds(), "HH:MM:SS")

    l_orderhdr = db_session.query(L_orderhdr).filter(
             (L_orderhdr.lieferdatum >= billdate) & (L_orderhdr.betriebsnr <= 1)).first()
    while None != l_orderhdr:

        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 245) & (Queasy.char1 == l_orderhdr.docu_nr) & (Queasy.number1 >= 1) & (Queasy.number1 < 4)).first()
        while None != queasy:

            qsy_list = query(qsy_list_list, filters=(lambda qsy_list: qsy_list.trim(qsy_list.docu_nr) == trim(queasy.char1)), first=True)

            if not qsy_list:
                qsy_list = Qsy_list()
                qsy_list_list.append(qsy_list)

                qsy_list.docu_nr = queasy.char1

                bediener = db_session.query(Bediener).filter(
                         (func.lower(Bediener.userinit) == (user_init).lower())).first()

                messages = db_session.query(Messages).filter(
                         (Messages.zinr == qsy_list.docu_nr) & (Messages.gastnr == bediener.nr)).first()

                if messages:
                    db_session.delete(messages)

            curr_recid = queasy._recid
            queasy = db_session.query(Queasy).filter(
                     (Queasy.key == 245) & (Queasy.char1 == l_orderhdr.docu_nr) & (Queasy.number1 >= 1) & (Queasy.number1 < 4)).filter(Queasy._recid > curr_recid).first()

        curr_recid = l_orderhdr._recid
        l_orderhdr = db_session.query(L_orderhdr).filter(
                 (L_orderhdr.lieferdatum >= billdate) & (L_orderhdr.betriebsnr <= 1)).filter(L_orderhdr._recid > curr_recid).first()
    b = to_string(get_current_time_in_seconds(), "HH:MM:SS")

    messages = db_session.query(Messages).first()
    while None != messages:
        db_session.delete(messages)

        curr_recid = messages._recid
        messages = db_session.query(Messages).filter(Messages._recid > curr_recid).first()
    c = to_string(get_current_time_in_seconds(), "HH:MM:SS")

    if use_po_esignature:

        qsy_list = query(qsy_list_list, first=True)
        while None != qsy_list:

            l_orderhdr = db_session.query(L_orderhdr).filter(
                     (L_orderhdr.docu_nr == qsy_list.docu_nr)).first()

            if l_orderhdr:
                po_list = Po_list()
                po_list_list.append(po_list)

                po_list.lief_nr = l_orderhdr.lief_nr
                po_list.docu_nr = l_orderhdr.docu_nr
                po_list.bestelldatum = l_orderhdr.bestelldatum
                po_list.lieferdatum = l_orderhdr.lieferdatum
                po_list.bestellart = l_orderhdr.bestellart
                po_list.gedruckt = l_orderhdr.gedruckt
                po_list.besteller = l_orderhdr.besteller
                po_list.lief_fax_3 = l_orderhdr.lief_fax[2]
                po_list.rec_id = l_orderhdr._recid

                for queasy in db_session.query(Queasy).filter(
                         (Queasy.key == 245) & (Queasy.char1 == po_list.docu_nr)).order_by(Queasy._recid).all():

                    if queasy.number1 == 1:
                        po_list.approval_lvl[0] = True

                    if queasy.number1 == 2:
                        po_list.approval_lvl[1] = True

                    if queasy.number1 == 3:
                        po_list.approval_lvl[2] = True

                    if queasy.number1 == 4:
                        po_list.approval_lvl[3] = True

                if po_list.approval_lvl[0] == False:
                    po_list_list.remove(po_list)
                else:

                    bediener = db_session.query(Bediener).filter(
                             (func.lower(Bediener.userinit) == (user_init).lower())).first()

                    if bediener:

                        if substring(bediener.permissions, 88, 2) >= '2':
                            po_list.approval_id[0] = bediener.userinit

                        if substring(bediener.permissions, 89, 2) >= '2':
                            po_list.approval_id[1] = bediener.userinit

                        if substring(bediener.permissions, 90, 2) >= '2':
                            po_list.approval_id[2] = bediener.userinit

                        if substring(bediener.permissions, 91, 2) >= '2':
                            po_list.approval_id[3] = bediener.userinit

                    if po_list.approval_lvl[0] :
                        app_lvl = 1
                        po_list.need_approval = "2nd Approval"

                    if po_list.approval_lvl[1] :
                        app_lvl = 2
                        po_list.need_approval = "3rd Approval"

                    if po_list.approval_lvl[2] :
                        app_lvl = 3
                        po_list.need_approval = "4th Approval"

                    if po_list.approval_lvl[0]  and po_list.approval_lvl[1]  and po_list.approval_lvl[2]  and po_list.approval_lvl[3] :
                        pass
                    else:
                        for loop_init in range(2,4 + 1) :

                            if po_list.approval_id[loop_init - 1] == (user_init).lower()  and po_list.approval_lvl[loop_init - 1] == False:

                                if po_list.approval_lvl[loop_init - 1 - 1] :

                                    bediener = db_session.query(Bediener).filter(
                                             (func.lower(Bediener.userinit) == (user_init).lower())).first()

                                    messages = db_session.query(Messages).filter(
                                             (Messages.zinr == po_list.docu_nr) & (Messages.gastnr == bediener.nr)).first()

                                    if not messages:
                                        messages = Messages()
                                        db_session.add(messages)

                                        messages.zeit = get_current_time_in_seconds()
                                        messages.gastnr = bediener.nr
                                        messages.zinr = po_list.docu_nr
                                        messages.messtext[9] = to_string(po_list.lief_nr)
                                        messages.name = to_string(get_year(get_current_date()) , "9999") + "/" + to_string(get_month(get_current_date()) , "99") + "/" + to_string(get_day(get_current_date()) , "99")
                                        messages.usre = user_init
                                        messages.messtext[6] = to_string(po_list.approval_id[0]) + "|" + to_string(po_list.approval_id[1]) + "|" + to_string(po_list.approval_id[2]) + "|" + to_string(po_list.approval_id[3])
                                        messages.messtext[7] = to_string(po_list.approval_lvl[0]) + "|" + to_string(po_list.approval_lvl[1]) + "|" + to_string(po_list.approval_lvl[2]) + "|" + to_string(po_list.approval_lvl[3])
                                        messages.messtext[8] = to_string(app_lvl)
                                        messages.messtext[0] = "PO Number " + po_list.docu_nr + " Need " + po_list.need_approval

            qsy_list = query(qsy_list_list, next=True)
    d = to_string(get_current_time_in_seconds(), "HH:MM:SS")

    return generate_output()