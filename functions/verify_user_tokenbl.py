#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.get_user_tokenbl import get_user_tokenbl
from models import Guest_queasy, Bediener

def verify_user_tokenbl(user_init:string, license_nr:string, user_token:string):

    prepare_cache ([Bediener])

    new_user_token = ""
    i_result = 0
    errmess = ""
    headerstring:string = ""
    payloadstring:string = ""
    tokenstring:string = ""
    calctoken:string = ""
    i:int = 0
    secret:string = ""
    master_key:string = ""
    system_token:string = ""
    l_match:bool = False
    curr_i:int = 0
    max_counter:int = 0
    tot_counter:int = 0
    last_date:date = None
    last_time:int = 0
    delta_time:int = 0
    username:string = ""
    tokenlen:int = 0
    secret_str:string = ""
    guest_queasy = bediener = None

    gqbuff = gqbuff1 = None

    Gqbuff = create_buffer("Gqbuff",Guest_queasy)
    Gqbuff1 = create_buffer("Gqbuff1",Guest_queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal new_user_token, i_result, errmess, headerstring, payloadstring, tokenstring, calctoken, i, secret, master_key, system_token, l_match, curr_i, max_counter, tot_counter, last_date, last_time, delta_time, username, tokenlen, secret_str, guest_queasy, bediener
        nonlocal user_init, license_nr, user_token
        nonlocal gqbuff, gqbuff1


        nonlocal gqbuff, gqbuff1

        return {"new_user_token": new_user_token, "i_result": i_result, "errmess": errmess}

    def update_master_key():

        nonlocal new_user_token, i_result, errmess, headerstring, payloadstring, tokenstring, calctoken, i, secret, master_key, system_token, l_match, curr_i, max_counter, tot_counter, last_date, last_time, delta_time, username, tokenlen, secret_str, guest_queasy, bediener
        nonlocal user_init, license_nr, user_token
        nonlocal gqbuff, gqbuff1


        nonlocal gqbuff, gqbuff1

        new_key = ""
        user_pswd:string = ""

        def generate_inner_output():
            return (new_key)

        user_pswd = decode_string1(bediener.usercode)
        new_key = license_nr + bediener.username.upper() + user_pswd.upper() + "|" + to_string(get_current_date()) + to_string(get_current_time_in_seconds())

        return generate_inner_output()


    def decode_string1(in_str:string):

        nonlocal new_user_token, i_result, errmess, headerstring, payloadstring, tokenstring, calctoken, i, secret, master_key, system_token, l_match, curr_i, max_counter, tot_counter, last_date, last_time, delta_time, username, tokenlen, secret_str, guest_queasy, bediener
        nonlocal user_init, license_nr, user_token
        nonlocal gqbuff, gqbuff1


        nonlocal gqbuff, gqbuff1

        out_str = ""
        s:string = ""
        j:int = 0
        len_:int = 0

        def generate_inner_output():
            return (out_str)

        s = in_str
        j = asc(substring(s, 0, 1)) - 71
        len_ = length(in_str) - 1
        s = substring(in_str, 1, len_)


        for len_ in range(1,length(s)  + 1) :
            out_str = out_str + chr_unicode(asc(substring(s, len_ - 1, 1)) - j)
        out_str = substring(out_str, 4, (length(out_str) - 4))

        return generate_inner_output()


    new_user_token = user_token
    tokenlen = length(user_token) - 39
    tokenstring = substring(user_token, tokenlen - 1, 40)

    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})
    username = bediener.username

    for guest_queasy in db_session.query(Guest_queasy).filter(
             (Guest_queasy.key == ("userToken").lower()) & (Guest_queasy.char1 == (user_init).lower())).order_by(Guest_queasy.number3.desc()).all():
        tot_counter = tot_counter + 1
        curr_i = guest_queasy.number3
        master_key = entry(0, guest_queasy.char3, "|")

        if max_counter == 0:
            last_date = guest_queasy.date1
            last_time = guest_queasy.number1
            max_counter = guest_queasy.number3

        if not l_match:
            secret = master_key
            for i in range(1,length(secret)  + 1) :
                secret_str = secret_str + "#" + substring(secret, i - 1, 1)
            secret_str = secret_str + "#"
            calctoken = sha1(secret_str).hexdigest()
            l_match = (tokenstring == calctoken)

            if l_match:
                break

    if not l_match:
        i_result = 2
        errmess = "Invalid Token"

        return generate_output()

    if curr_i < max_counter:
        i_result = 1
    else:
        delta_time = get_current_time_in_seconds() + ((get_current_date() - last_date).days) * 86400 - last_time

        if delta_time <= 1800:

            return generate_output()
        else:
            i_result = 1

    if i_result == 1:

        if tot_counter >= 4:

            gqbuff = db_session.query(Gqbuff).filter(
                     (Gqbuff.key == ("userToken").lower()) & (Gqbuff.char1 == (user_init).lower()) & (Gqbuff.number3 <= 1)).first()
            while None != gqbuff:

                gqbuff1 = db_session.query(Gqbuff1).filter(
                             (Gqbuff1._recid == gqbuff._recid)).first()
                db_session.delete(gqbuff1)
                pass

                curr_recid = gqbuff._recid
                gqbuff = db_session.query(Gqbuff).filter(
                         (Gqbuff.key == ("userToken").lower()) & (Gqbuff.char1 == (user_init).lower()) & (Gqbuff.number3 <= 1) & (Gqbuff._recid > curr_recid)).first()

            guest_queasy = get_cache (Guest_queasy, {"key": [(eq, "usertoken")],"char1": [(eq, user_init)]})

            if guest_queasy:

                gqbuff = db_session.query(Gqbuff).filter(
                         (Gqbuff.key == ("userToken").lower()) & (Gqbuff.char1 == (user_init).lower()) & (Gqbuff.number3 == 1)).first()
                while not gqbuff:
                    max_counter = max_counter - 1

                    for guest_queasy in db_session.query(Guest_queasy).filter(
                             (Guest_queasy.key == ("userToken").lower()) & (Guest_queasy.char1 == (user_init).lower())).order_by(Guest_queasy._recid).all():

                        gqbuff1 = db_session.query(Gqbuff1).filter(
                                     (Gqbuff1._recid == guest_queasy._recid)).first()
                        gqbuff1.number3 = gqbuff1.number3 - 1
                        pass

                    curr_recid = gqbuff._recid
                    gqbuff = db_session.query(Gqbuff).filter(
                             (Gqbuff.key == ("userToken").lower()) & (Gqbuff.char1 == (user_init).lower()) & (Gqbuff.number3 == 1) & (Gqbuff._recid > curr_recid)).first()
            else:
                max_counter = 0
        master_key = update_master_key()
        guest_queasy = Guest_queasy()
        db_session.add(guest_queasy)

        guest_queasy.key = "userToken"
        guest_queasy.date1 = get_current_date()
        guest_queasy.number1 = get_current_time_in_seconds()
        guest_queasy.number3 = max_counter + 1
        guest_queasy.char3 = master_key
        guest_queasy.char1 = user_init


        pass
        new_user_token = get_output(get_user_tokenbl(user_init, "", license_nr, master_key))

    return generate_output()