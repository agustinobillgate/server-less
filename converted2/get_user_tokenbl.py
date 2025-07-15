#using conversion tools version: 1.0.0.29

from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Bediener, Guest_queasy, Paramtext

def get_user_tokenbl(user_init:str, user_code:str, license_nr:str, master_key:str):
    user_token = ""
    ojsonarray = None
    ojsonobjectheader = None
    ojsonobjectpayload = None
    tokensignature:str = ""
    secret:str = ""
    token:str = ""
    headerstring:str = ""
    payloadstring:str = ""
    rawheader:bytes = None
    rawpayload:bytes = None
    user_pswd:str = ""
    username:str = ""
    i:int = 0
    bediener = guest_queasy = paramtext = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal user_token, ojsonarray, ojsonobjectheader, ojsonobjectpayload, tokensignature, secret, token, headerstring, payloadstring, rawheader, rawpayload, user_pswd, username, i, bediener, guest_queasy, paramtext
        nonlocal user_init, user_code, license_nr, master_key

        return {"user_token": user_token}

    def BinaryXOR(intoperand1:int, intoperand2:int):

        nonlocal user_token, ojsonarray, ojsonobjectheader, ojsonobjectpayload, tokensignature, secret, token, headerstring, payloadstring, rawheader, rawpayload, user_pswd, username, i, bediener, guest_queasy, paramtext
        nonlocal user_init, user_code, license_nr, master_key

        ibyteloop:int = 0
        ixoresult:int = 0
        lfirstbit:bool = False
        lsecondbit:bool = False
        ixoresult = 0
        for ibyteloop in range(0,7 + 1) :
            lfirstbit = GET_BITS (intoperand1, ibyteloop + 1, 1) == 1
            lsecondbit = GET_BITS (intoperand2, ibyteloop + 1, 1) == 1

            if (lfirstbit and not lsecondbit) or (lsecondbit and not lfirstbit):
                ixoresult = ixoresult + EXP (2, ibyteloop)
        return ixoresult


    def HMAC_BASE64(pcsha:str, pckey:str, pcdata:str):

        nonlocal user_token, ojsonarray, ojsonobjectheader, ojsonobjectpayload, tokensignature, secret, token, headerstring, payloadstring, rawheader, rawpayload, user_pswd, username, i, bediener, guest_queasy, paramtext
        nonlocal user_init, user_code, license_nr, master_key

        mkeyopad:bytes = None
        mkeyipad:bytes = None
        mdata:bytes = None
        mkey:bytes = None
        minnercombined:bytes = None
        moutercombined:bytes = None
        ibytepos:int = 0
        iopad:int = 0
        iipad:int = 0
        ikey:int = 0
        itimetaken:int = 0
        rrawdatasha:bytes = None
        chmacsha:str = ""
        for ibytepos in range(1,{&xiBlockSize} + 1) :
            put_bytes (mkey, ibytepos) = HEX_DECODE ("00":U)
            put_bytes (mkeyopad, ibytepos) = HEX_DECODE ("5C":U)
            put_bytes (mkeyipad, ibytepos) = HEX_DECODE ("36":U)

        if length(pckey) > {&xiBlockSize}:
            mdata = pckey.encode('utf-8')
            rrawdatasha = sha1(mdata)
            put_bytes (mkey, 1) = rrawdatasha
        else:
            mkey = pckey.encode('utf-8')
        for ibytepos in range(1,{&xiBlockSize} + 1) :
            ikey = GET_BYTE (mkey, ibytepos)
            iopad = GET_BYTE (mkeyopad, ibytepos)
            iipad = GET_BYTE (mkeyipad, ibytepos)


            put_byte (mkeyipad, ibytepos) = BinaryXOR (INPUT ikey, INPUT iipad)
            put_byte (mkeyopad, ibytepos) = BinaryXOR (INPUT ikey, INPUT iopad)
        mdata = pcdata.encode('utf-8')
        put_bytes (minnercombined, 1) = mkeyipad
        put_bytes (minnercombined, {&xiblocksize} + 1) = mdata

        if pcsha == 'SHA1':
            rrawdatasha = sha1(minnercombined)


        elif pcsha == 'SHA-256':
            rrawdatasha = MESSAGE_DIGEST ('SHA-256', minnercombined)


        else:
            rrawdatasha = sha1(minnercombined)


        put_bytes (moutercombined, 1) = mkeyopad
        put_bytes (moutercombined, {&xiblocksize} + 1) = rrawdatasha

        if pcsha == 'SHA1':
            rrawdatasha = sha1(moutercombined)


        elif pcsha == 'SHA-256':
            rrawdatasha = MESSAGE_DIGEST ('SHA-256', moutercombined)


        else:
            rrawdatasha = sha1(moutercombined)


        chmacsha = base64_encode(rrawdatasha)
        &UNDEFINE xiBlockSize return chmacsha


    def decode_string1(in_str:str):

        nonlocal user_token, ojsonarray, ojsonobjectheader, ojsonobjectpayload, tokensignature, secret, token, headerstring, payloadstring, rawheader, rawpayload, user_pswd, username, i, bediener, guest_queasy, paramtext
        nonlocal user_init, user_code, license_nr, master_key

        out_str = ""
        s:str = ""
        j:int = 0
        len_:int = 0

        def generate_inner_output():
            return (out_str)

        s = in_str
        j = asc(substring(s, 0, 1)) - 71
        len_ = length(in_str) - 1
        s = substring(in_str, 1, len_)


        for len_ in range(1,length(s)  + 1) :
            out_str = out_str + chr (asc(substring(s, len_ - 1, 1)) - j)
        out_str = substring(out_str, 4, (length(out_str) - 4))

        return generate_inner_output()


    def decode_string(in_str:str):

        nonlocal user_token, ojsonarray, ojsonobjectheader, ojsonobjectpayload, tokensignature, secret, token, headerstring, payloadstring, rawheader, rawpayload, user_pswd, username, i, bediener, guest_queasy, paramtext
        nonlocal user_init, user_code, license_nr, master_key

        out_str = ""
        s:str = ""
        j:int = 0
        len_:int = 0

        def generate_inner_output():
            return (out_str)

        s = in_str
        j = asc(substring(s, 0, 1)) - 70
        len_ = length(in_str) - 1
        s = substring(in_str, 1, len_)
        for len_ in range(1,length(s)  + 1) :
            out_str = out_str + chr (asc(substring(s, len_ - 1, 1)) - j)

        return generate_inner_output()


    USING PROGRESS.Json.ObjectModel.JsonArray
    USING PROGRESS.Json.ObjectModel.JsonObject

    bediener = db_session.query(Bediener).filter(
             (func.lower(Bediener.userinit) == (user_init).lower())).first()
    username = bediener.username

    if master_key == "":

        for guest_queasy in db_session.query(Guest_queasy).filter(
                 (func.lower(Guest_queasy.key) == ("userToken").lower()) & (func.lower(Guest_queasy.char1) == (user_init).lower())).order_by(Guest_queasy.number3.desc()).all():
            master_key = entry(0, guest_queasy.char3, "|")


            break

    if license_nr == "":

        paramtext = db_session.query(Paramtext).filter(
                 (Paramtext.txtnr == 243)).first()

        if paramtext and paramtext.ptexte != "":
            license_nr = decode_string(paramtext.ptexte)
    secret = master_key
    ojsonobjectheader = NEW JsonObject()
    ojsonobjectheader:ADD ("alg", "HS256")
    ojsonobjectheader:ADD ("type", "JWT")
    headerstring = to_string(ojsonobjectheader:GetJsonText())
    rawheader = headerstring.encode('utf-8')
    headerstring = to_string(base64_encode(rawheader))
    headerstring = replace_str(headerstring, "/", "_")
    headerstring = replace_str(headerstring, "+", "-")
    headerstring = replace_str(headerstring, "=", "")
    headerstring = right_trim(headerstring, "A")
    ojsonobjectpayload = NEW JsonObject()
    ojsonobjectpayload:Add ("loggedInAs", "admin")
    ojsonobjectpayload:Add ("generated", get_current_datetime())
    ojsonobjectpayload:Add ("expired", get_current_datetime() + 3600 * 1000)
    payloadstring = to_string(ojsonobjectpayload:GetJsonText())
    rawpayload = payloadstring.encode('utf-8')
    payloadstring = to_string(base64_encode(rawpayload))
    payloadstring = replace_str(payloadstring, "/", "_")
    payloadstring = replace_str(payloadstring, "+", "-")
    payloadstring = replace_str(payloadstring, "=", "")
    payloadstring = right_trim(payloadstring, "A")
    for i in range(1,length(secret)  + 1) :
        tokensignature = tokensignature + "#" + substring(secret, i - 1, 1)
    tokensignature = tokensignature + "#"
    tokensignature = sha1(tokensignature).hexdigest()
    tokensignature = tokensignature.upper()
    token = headerstring + payloadstring + to_string(tokensignature)
    clipboard:value = token
    user_token = token.upper()

    return generate_output()