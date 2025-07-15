#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Bediener, Kellner

def ts_helpusr_check_passwdbl(passwd:string, knr:int, dept:int):

    prepare_cache ([Kellner])

    anzahl_falsch = 0
    its_ok = False
    bediener = kellner = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal anzahl_falsch, its_ok, bediener, kellner
        nonlocal passwd, knr, dept

        return {"anzahl_falsch": anzahl_falsch, "its_ok": its_ok}

    def check_passwd():

        nonlocal anzahl_falsch, its_ok, bediener, kellner
        nonlocal passwd, knr, dept

        passwd1:string = ""
        vhpusr = None
        Vhpusr =  create_buffer("Vhpusr",Bediener)

        kellner = get_cache (Kellner, {"kellner_nr": [(eq, knr)],"departement": [(eq, dept)]})

        vhpusr = db_session.query(Vhpusr).filter(
                 (Vhpusr.userinit == trim(to_string(kellner.kellner_nr, ">>99")))).first()
        passwd1 = decode_string1(vhpusr.usercode)
        its_ok = (passwd == passwd1)

        if not its_ok:
            anzahl_falsch = anzahl_falsch + 1


    def decode_string1(in_str:string):

        nonlocal anzahl_falsch, its_ok, bediener, kellner
        nonlocal passwd, knr, dept

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


    check_passwd()

    return generate_output()