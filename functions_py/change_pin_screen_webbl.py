#using conversion tools version: 1.0.0.118
#-------------------------------------------
# Rd, 26/11/2025, with_for_update
#-------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Queasy, Bediener, Res_history, Paramtext

t_payload_list_data, T_payload_list = create_model("T_payload_list", {"hotel_code":string, "user_init":string, "case_type":int, "old_pin":string, "new_pin":string})

def change_pin_screen_webbl(t_payload_list_data:[T_payload_list]):

    prepare_cache ([Queasy, Bediener, Res_history, Paramtext])

    signature_list_data = []
    t_output_list_data = []
    epoch_signature = 0
    c_pin:string = ""
    c_hashed_pin:string = ""
    c_pin_new:string = ""
    c_hashed_pin_new:string = ""
    queasy = bediener = res_history = paramtext = None

    t_payload_list = t_output_list = value_list = signature_list = buf_queasy = None

    t_output_list_data, T_output_list = create_model("T_output_list", {"msg":string, "flag":bool})
    value_list_data, Value_list = create_model("Value_list", {"var_name":string, "value_str":string})
    signature_list_data, Signature_list = create_model("Signature_list", {"var_name":string, "signature":string})

    Buf_queasy = create_buffer("Buf_queasy",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal signature_list_data, t_output_list_data, epoch_signature, c_pin, c_hashed_pin, c_pin_new, c_hashed_pin_new, queasy, bediener, res_history, paramtext
        nonlocal buf_queasy


        nonlocal t_payload_list, t_output_list, value_list, signature_list, buf_queasy
        nonlocal t_output_list_data, value_list_data, signature_list_data

        return {"signature-list": signature_list_data, "t-output-list": t_output_list_data, "epoch_signature": epoch_signature}

    def isvalidpin(c_hashed_pin:string):

        nonlocal signature_list_data, t_output_list_data, epoch_signature, c_pin, c_pin_new, c_hashed_pin_new, queasy, bediener, res_history, paramtext
        nonlocal buf_queasy


        nonlocal t_payload_list, t_output_list, value_list, signature_list, buf_queasy
        nonlocal t_output_list_data, value_list_data, signature_list_data

        cline:string = ""
        lisvalid:bool = False
        cinvalidhashedpin:string = ""

        queasy = get_cache (Queasy, {"key": [(eq, 362)]})

        if queasy:

            buf_queasy = get_cache (Queasy, {"key": [(eq, 362)],"char1": [(eq, c_hashed_pin)]})

            if buf_queasy:
                lisvalid = True
            else:
                lisvalid = True
        else:
            lisvalid = True
        return lisvalid


    def create_signature(user_name:string, value_list_data:[Value_list]):

        nonlocal signature_list_data, t_output_list_data, epoch_signature, c_pin, c_hashed_pin, c_pin_new, c_hashed_pin_new, queasy, bediener, res_history, paramtext
        nonlocal buf_queasy


        nonlocal t_payload_list, t_output_list, value_list, signature_list, buf_queasy
        nonlocal t_output_list_data, signature_list_data

        epoch = 0
        dtz1 = None
        dtz2 = None
        lic_nr:string = ""
        data:string = ""
        value_str:string = ""

        def generate_inner_output():
            return (epoch, signature_list_data)


        paramtext = get_cache(Paramtext, {"txtnr": [(eq, 243)]})

        if paramtext and paramtext.ptexte != "":
            lic_nr = decode_string(paramtext.ptexte)
        dtz1 = get_current_datetime()
        dtz2 = parse("1970-01-01T00:00:00.000+0:00")
        epoch = get_interval(dtz1, dtz2, "milliseconds")

        for value_list in query(value_list_data):
            value_str = value_list.value_str.lower()

            if value_str == "yes":
                value_str = "true"
            elif value_str == "no":
                value_str = "false"
            data = value_str + "-" + to_string(epoch) + "-" + to_string(lic_nr) + "-" + user_name.lower()
            signature_list = Signature_list()
            signature_list_data.append(signature_list)

            signature_list.var_name = value_list.var_name
            signature_list.signature = sha1(data).hexdigest()

        return generate_inner_output()


    def decode_string(in_str:string):

        nonlocal signature_list_data, t_output_list_data, epoch_signature, c_pin, c_hashed_pin, c_pin_new, c_hashed_pin_new, queasy, bediener, res_history, paramtext
        nonlocal buf_queasy


        nonlocal t_payload_list, t_output_list, value_list, signature_list, buf_queasy
        nonlocal t_output_list_data, value_list_data, signature_list_data

        out_str = ""
        s:string = ""
        j:int = 0
        len_:int = 0

        def generate_inner_output():
            return (out_str)

        s = in_str
        j = asc(substring(s, 0, 1)) - 70
        len_ = length(in_str) - 1
        s = substring(in_str, 1, len_)
        for len_ in range(1,length(s)  + 1) :
            out_str = out_str + chr_unicode(asc(substring(s, len_ - 1, 1)) - j)

        return generate_inner_output()


    def change_pin():

        nonlocal signature_list_data, t_output_list_data, epoch_signature, c_pin, c_hashed_pin, c_pin_new, c_hashed_pin_new, queasy, bediener, res_history, paramtext
        nonlocal buf_queasy


        nonlocal t_payload_list, t_output_list, value_list, signature_list, buf_queasy
        nonlocal t_output_list_data, value_list_data, signature_list_data


        c_pin_new = t_payload_list.new_pin + bediener.userinit
        c_hashed_pin_new = sha1(c_pin_new).hexdigest()
        pass
        db_session.delete(queasy)
        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 360
        queasy.number1 = bediener.nr
        queasy.char1 = c_hashed_pin_new
        queasy.char2 = c_hashed_pin
        queasy.date1 = get_current_date()


        t_output_list.flag = True
        t_output_list.msg = "PIN is succesfully updated"
        value_list = Value_list()
        value_list_data.append(value_list)

        value_list.var_name = "flag"
        value_list.value_str = to_string(t_output_list.flag)


        epoch_signature, signature_list_data = create_signature(bediener.username, value_list_data)
        res_history = Res_history()
        db_session.add(res_history)

        res_history.nr = bediener.nr
        res_history.datum = get_current_date()
        res_history.zeit = get_current_time_in_seconds()
        res_history.action = "Manage PIN"


        res_history.aenderung = "Change PIN for username: " + bediener.username

    t_payload_list = query(t_payload_list_data, first=True)
    t_output_list = T_output_list()
    t_output_list_data.append(t_output_list)


    if t_payload_list.case_type == 1:

        bediener = get_cache(Bediener, {"userinit": [(eq, t_payload_list.user_init)]})

        if bediener:
            queasy = get_cache(Queasy, {"key": [(eq, 360)],"number1": [(eq, bediener.nr)]})

            if queasy:
                c_pin = t_payload_list.old_pin + bediener.userinit
                c_hashed_pin = sha1(c_pin).hexdigest()

                if queasy.char1.lower()  == (c_hashed_pin).lower() :

                    if not isvalidpin(t_payload_list.new_pin):
                        t_output_list.flag = False
                        t_output_list.msg = "PIN is weak"
                        value_list = Value_list()
                        value_list_data.append(value_list)

                        value_list.var_name = "flag"
                        value_list.value_str = to_string(t_output_list.flag)

                        epoch_signature, signature_list_data = create_signature(bediener.username, value_list_data)

                        return generate_output()
                    else:
                        c_pin_new = t_payload_list.new_pin + bediener.userinit
                        c_hashed_pin_new = sha1(c_pin_new).hexdigest()

                        # buf_queasy = get_cache (Queasy, {"key": [(eq, 360)],"number1": [(eq, bediener.nr)]})
                        buf_queasy = db_session.query(Queasy).filter(Queasy.key == 360, 
                                                             Queasy.number1 == bediener.nr).with_for_update().first()
                        buf_queasy.char1 = c_hashed_pin_new
                        buf_queasy.char2 = c_hashed_pin
                        buf_queasy.date2 = get_current_date()
                        buf_queasy.number3 = 21

                        t_output_list.flag = True
                        t_output_list.msg = "PIN is succesfully updated"
                        value_list = Value_list()
                        value_list_data.append(value_list)

                        value_list.var_name = "flag"
                        value_list.value_str = to_string(t_output_list.flag)


                        epoch_signature, signature_list_data = create_signature(bediener.username, value_list_data)
                        res_history = Res_history()
                        db_session.add(res_history)

                        res_history.nr = bediener.nr
                        res_history.datum = get_current_date()
                        res_history.zeit = get_current_time_in_seconds()
                        res_history.action = "Manage PIN"


                        res_history.aenderung = "Change PIN for username: " + bediener.username
                else:
                    t_output_list.flag = False
                    t_output_list.msg = "PIN is wrong, please try again"
                    value_list = Value_list()
                    value_list_data.append(value_list)

                    value_list.var_name = "flag"
                    value_list.value_str = to_string(t_output_list.flag)


                    epoch_signature, signature_list_data = create_signature(bediener.username, value_list_data)

                return generate_output()

    return generate_output()