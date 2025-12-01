#using conversion tools version: 1.0.0.118
#-------------------------------------------
# Rd, 26/11/2025, with_for_update
#-------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Bediener, Queasy, Res_history, Paramtext

t_payload_list_data, T_payload_list = create_model("T_payload_list", {"hotel_code":string, "user_init":string, "case_type":int, "pin":string})

def unlock_screen_webbl(t_payload_list_data:[T_payload_list]):

    prepare_cache ([Bediener, Res_history, Paramtext])

    signature_list_data = []
    t_output_list_data = []
    epoch_signature = 0
    c_pin:string = ""
    c_hashed_pin:string = ""
    decoded_passwd:string = ""
    bediener = queasy = res_history = paramtext = None

    t_payload_list = t_output_list = value_list = signature_list = buf_bediener = buf_queasy = None

    t_output_list_data, T_output_list = create_model("T_output_list", {"msg":string, "flag":bool, "statuspin":bool}, {"statuspin": None})
    value_list_data, Value_list = create_model("Value_list", {"var_name":string, "value_str":string})
    signature_list_data, Signature_list = create_model("Signature_list", {"var_name":string, "signature":string})

    Buf_bediener = create_buffer("Buf_bediener",Bediener)
    Buf_queasy = create_buffer("Buf_queasy",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal signature_list_data, t_output_list_data, epoch_signature, c_pin, c_hashed_pin, decoded_passwd, bediener, queasy, res_history, paramtext
        nonlocal buf_bediener, buf_queasy


        nonlocal t_payload_list, t_output_list, value_list, signature_list, buf_bediener, buf_queasy
        nonlocal t_output_list_data, value_list_data, signature_list_data

        return {"signature-list": signature_list_data, "t-output-list": t_output_list_data, "epoch_signature": epoch_signature}

    def isvalidpin(c_hashed_pin:string):

        nonlocal signature_list_data, t_output_list_data, epoch_signature, c_pin, decoded_passwd, bediener, queasy, res_history, paramtext
        nonlocal buf_bediener, buf_queasy


        nonlocal t_payload_list, t_output_list, value_list, signature_list, buf_bediener, buf_queasy
        nonlocal t_output_list_data, value_list_data, signature_list_data

        cline:string = ""
        lisvalid:bool = False
        cinvalidhashedpin:string = ""

        queasy = get_cache (Queasy, {"key": [(eq, 362)]})

        if queasy:

            buf_queasy = db_session.query(Buf_queasy).filter(
                     (Buf_queasy.key == 362) & (Buf_queasy.char1 == (c_hashed_pin).lower())).first()

            if buf_queasy:
                lisvalid = True
            else:
                lisvalid = True
        else:
            lisvalid = True
        return lisvalid


    def create_signature(user_name:string, value_list_data:[Value_list]):

        nonlocal signature_list_data, t_output_list_data, epoch_signature, c_pin, c_hashed_pin, decoded_passwd, bediener, queasy, res_history, paramtext
        nonlocal buf_bediener, buf_queasy


        nonlocal t_payload_list, t_output_list, value_list, signature_list, buf_bediener, buf_queasy
        nonlocal t_output_list_data, signature_list_data

        epoch = 0
        dtz1 = None
        dtz2 = None
        lic_nr:string = ""
        data:string = ""
        value_str:string = ""

        def generate_inner_output():
            return (epoch, signature_list_data)


        paramtext = get_cache (Paramtext, {"txtnr": [(eq, 243)]})

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

        nonlocal signature_list_data, t_output_list_data, epoch_signature, c_pin, c_hashed_pin, decoded_passwd, bediener, queasy, res_history, paramtext
        nonlocal buf_bediener, buf_queasy


        nonlocal t_payload_list, t_output_list, value_list, signature_list, buf_bediener, buf_queasy
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


    def decode_password(usercode:string):

        nonlocal signature_list_data, t_output_list_data, epoch_signature, c_pin, c_hashed_pin, decoded_passwd, bediener, queasy, res_history, paramtext
        nonlocal buf_bediener, buf_queasy


        nonlocal t_payload_list, t_output_list, value_list, signature_list, buf_bediener, buf_queasy
        nonlocal t_output_list_data, value_list_data, signature_list_data

        passwd = ""
        s:string = ""
        j:int = 0
        len_:int = 0

        def generate_inner_output():
            return (passwd)

        s = usercode
        j = asc(substring(s, 0, 1)) - 71
        len_ = length(usercode) - 1
        s = substring(usercode, 1, len_)
        for len_ in range(1,length(s)  + 1) :
            passwd = passwd + chr_unicode(asc(substring(s, len_ - 1, 1)) - j)
        passwd = substring(passwd, 4, (length(passwd) - 4))

        return generate_inner_output()
    

    def disable_pin_using_pin():

        nonlocal signature_list_data, t_output_list_data, epoch_signature, c_pin, c_hashed_pin, decoded_passwd, bediener, queasy, res_history, paramtext
        nonlocal buf_bediener, buf_queasy


        nonlocal t_payload_list, t_output_list, value_list, signature_list, buf_bediener, buf_queasy
        nonlocal t_output_list_data, value_list_data, signature_list_data


        pass
        db_session.delete(queasy)
        res_history = Res_history()
        db_session.add(res_history)

        res_history.nr = bediener.nr
        res_history.datum = get_current_date()
        res_history.zeit = get_current_time_in_seconds()
        res_history.action = "Manage PIN"


        res_history.aenderung = "Disable PIN using pin for username: " + bediener.username
        pass
        pass
        t_output_list.flag = True
        t_output_list.statuspin = False
        t_output_list.msg = "PIN is disabled"
        value_list = Value_list()
        value_list_data.append(value_list)

        value_list.var_name = "flag"
        value_list.value_str = to_string(t_output_list.flag)


        epoch_signature, signature_list_data = create_signature(bediener.username, value_list_data)


    def disable_pin_using_password():

        nonlocal signature_list_data, t_output_list_data, epoch_signature, c_pin, c_hashed_pin, decoded_passwd, bediener, queasy, res_history, paramtext
        nonlocal buf_bediener, buf_queasy


        nonlocal t_payload_list, t_output_list, value_list, signature_list, buf_bediener, buf_queasy
        nonlocal t_output_list_data, value_list_data, signature_list_data


        pass
        db_session.delete(queasy)
        res_history = Res_history()
        db_session.add(res_history)

        res_history.nr = bediener.nr
        res_history.datum = get_current_date()
        res_history.zeit = get_current_time_in_seconds()
        res_history.action = "Manage PIN"


        res_history.aenderung = "Disable PIN using password for username: " + bediener.username
        pass
        pass
        t_output_list.flag = True
        t_output_list.statuspin = False
        t_output_list.msg = "PIN is disabled"
        value_list = Value_list()
        value_list_data.append(value_list)

        value_list.var_name = "flag"
        value_list.value_str = to_string(t_output_list.flag)


        epoch_signature, signature_list_data = create_signature(bediener.username, value_list_data)

    t_payload_list = query(t_payload_list_data, first=True)
    t_output_list = T_output_list()
    t_output_list_data.append(t_output_list)


    if t_payload_list.case_type == 1:

        bediener = get_cache (Bediener, {"userinit": [(eq, t_payload_list.user_init)]})

        if bediener:

            queasy = get_cache (Queasy, {"key": [(eq, 360)],"number1": [(eq, bediener.nr)]})

            if queasy:
                t_output_list.flag = True
                t_output_list.statuspin = True
                t_output_list.msg = "PIN is already created and active"
                value_list = Value_list()
                value_list_data.append(value_list)

                value_list.var_name = "flag"
                value_list.value_str = to_string(t_output_list.flag)


                epoch_signature, signature_list_data = create_signature(bediener.username, value_list_data)
            else:
                t_output_list.flag = False
                t_output_list.statuspin = False
                t_output_list.msg = "PIN is unactive, please create new pin"
                value_list = Value_list()
                value_list_data.append(value_list)

                value_list.var_name = "flag"
                value_list.value_str = to_string(t_output_list.flag)


                epoch_signature, signature_list_data = create_signature(bediener.username, value_list_data)

            return generate_output()

    elif t_payload_list.case_type == 2:

        bediener = get_cache (Bediener, {"userinit": [(eq, t_payload_list.user_init)]})

        if bediener:

            if not isvalidpin(t_payload_list.pin):
                t_output_list.flag = False
                t_output_list.msg = "PIN is weak"
                value_list = Value_list()
                value_list_data.append(value_list)

                value_list.var_name = "flag"
                value_list.value_str = to_string(t_output_list.flag)


                epoch_signature, signature_list_data = create_signature(bediener.username, value_list_data)
            else:
                c_pin = t_payload_list.pin + bediener.userinit
                c_hashed_pin = sha1(c_pin).hexdigest()
                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 360
                queasy.number1 = bediener.nr
                queasy.char1 = c_hashed_pin
                queasy.char2 = c_hashed_pin
                queasy.date1 = get_current_date()


                t_output_list.flag = True
                t_output_list.msg = "Succesfully created PIN"
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


                res_history.aenderung = "Create PIN for username: " + bediener.username
                pass
                pass

            return generate_output()

    elif t_payload_list.case_type == 3:

        bediener = get_cache (Bediener, {"userinit": [(eq, t_payload_list.user_init)]})

        if bediener:

            # queasy = get_cache (Queasy, {"key": [(eq, 360)],"number1": [(eq, bediener.nr)]})
            queasy = db_session.query(Queasy).filter(Queasy.key == 360, 
                                                 Queasy.number1 == bediener.nr).with_for_update().with_for_update().first()

            if queasy:
                c_pin = t_payload_list.pin + bediener.userinit
                c_hashed_pin = sha1(c_pin).hexdigest()

                if queasy.char1.lower()  == (c_hashed_pin).lower() :
                    disable_pin_using_pin()
                else:
                    t_output_list.flag = False
                    t_output_list.statuspin = True
                    t_output_list.msg = "PIN is wrong"
                    value_list = Value_list()
                    value_list_data.append(value_list)

                    value_list.var_name = "flag"
                    value_list.value_str = to_string(t_output_list.flag)


                    epoch_signature, signature_list_data = create_signature(bediener.username, value_list_data)

                return generate_output()

    elif t_payload_list.case_type == 4:

        bediener = get_cache (Bediener, {"userinit": [(eq, t_payload_list.user_init)]})

        if bediener:
            decoded_passwd = decode_password(bediener.usercode)
            decoded_passwd = sha1(decoded_passwd).hexdigest()

            if decoded_passwd == t_payload_list.pin:

                # queasy = get_cache (Queasy, {"key": [(eq, 360)],"number1": [(eq, bediener.nr)]})
                queasy = db_session.query(Queasy).filter(Queasy.key == 360, 
                                                     Queasy.number1 == bediener.nr).with_for_update().first()

                if queasy:
                    disable_pin_using_password()
            else:
                t_output_list.flag = False
                t_output_list.statuspin = True
                t_output_list.msg = "password is wrong"
                value_list = Value_list()
                value_list_data.append(value_list)

                value_list.var_name = "flag"
                value_list.value_str = to_string(t_output_list.flag)


                epoch_signature, signature_list_data = create_signature(bediener.username, value_list_data)

            return generate_output()

    elif t_payload_list.case_type == 5:

        bediener = get_cache (Bediener, {"userinit": [(eq, t_payload_list.user_init)]})

        if bediener:

            queasy = get_cache (Queasy, {"key": [(eq, 360)],"number1": [(eq, bediener.nr)]})

            if queasy:
                c_pin = t_payload_list.pin + bediener.userinit
                c_hashed_pin = sha1(c_pin).hexdigest()

                if queasy.char1.lower()  == (c_hashed_pin).lower() :
                    t_output_list.flag = True
                    t_output_list.msg = "Succesfully unlock screen"
                    value_list = Value_list()
                    value_list_data.append(value_list)

                    value_list.var_name = "flag"
                    value_list.value_str = to_string(t_output_list.flag)


                    epoch_signature, signature_list_data = create_signature(bediener.username, value_list_data)
                else:
                    t_output_list.flag = False
                    t_output_list.msg = "PIN is wrong"
                    value_list = Value_list()
                    value_list_data.append(value_list)

                    value_list.var_name = "flag"
                    value_list.value_str = to_string(t_output_list.flag)


                    epoch_signature, signature_list_data = create_signature(bediener.username, value_list_data)

                return generate_output()

    elif t_payload_list.case_type == 6:

        bediener = get_cache (Bediener, {"userinit": [(eq, t_payload_list.user_init)]})

        if bediener:
            decoded_passwd = decode_password(bediener.usercode)
            decoded_passwd = sha1(decoded_passwd).hexdigest()

            if decoded_passwd == t_payload_list.pin:
                t_output_list.flag = True
                t_output_list.msg = "Succesfully unlock screen"
                value_list = Value_list()
                value_list_data.append(value_list)

                value_list.var_name = "flag"
                value_list.value_str = to_string(t_output_list.flag)


                epoch_signature, signature_list_data = create_signature(bediener.username, value_list_data)
            else:
                t_output_list.flag = False
                t_output_list.msg = "password is wrong"
                value_list = Value_list()
                value_list_data.append(value_list)

                value_list.var_name = "flag"
                value_list.value_str = to_string(t_output_list.flag)


                epoch_signature, signature_list_data = create_signature(bediener.username, value_list_data)

            return generate_output()

    return generate_output()