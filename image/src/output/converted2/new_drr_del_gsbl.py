from functions.additional_functions import *
import decimal
from models import Paramtext

def new_drr_del_gsbl(gsheet_link:str):
    file_path:str = ""
    ch:str = ""
    counter:int = 0
    htl_no:str = ""
    crow:int = 0
    ccol:int = 0
    cval:str = ""
    paramtext = None

    stream_list = None

    stream_list_list, Stream_list = create_model("Stream_list", {"crow":int, "ccol":int, "cval":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal file_path, ch, counter, htl_no, crow, ccol, cval, paramtext
        nonlocal gsheet_link


        nonlocal stream_list
        nonlocal stream_list_list

        return {}

    def decode_string(in_str:str):

        nonlocal file_path, ch, counter, htl_no, crow, ccol, cval, paramtext
        nonlocal gsheet_link


        nonlocal stream_list
        nonlocal stream_list_list

        out_str = ""
        s:str = ""
        j:int = 0
        len_:int = 0

        def generate_inner_output():
            return (out_str)

        s = in_str
        j = asc(substring(s, 0, 1)) - 70
        len_ = len(in_str) - 1
        s = substring(in_str, 1, len_)
        for len_ in range(1,len(s)  + 1) :
            out_str = out_str + chr (asc(substring(s, len_ - 1, 1)) - j)

        return generate_inner_output()


    paramtext = db_session.query(Paramtext).filter(
             (Paramtext.txtnr == 243)).first()

    if paramtext and paramtext.ptexte != "":
        htl_no = decode_string(paramtext.ptexte)
    file_path = "usr1/vhp/tmp/outputFO_" + htl_no + ".txt "

    if SEARCH (file_path) == None:

        return generate_output()
    INPUT STREAM s1 FROM VALUE (file_path)
    counter = 0
    while True:
        IMPORT STREAM s1 UNFORMATTED ch
        ch = trim(ch)

        if ch == "":
            pass

        elif counter == 0:
            pass
        else:
            crow = to_int(entry(0, ch, ";"))
            ccol = to_int(entry(1, ch, ";"))
            cval = trim(entry(2, ch, ";"))
            stream_list = Stream_list()
            stream_list_list.append(stream_list)

            stream_list.crow = crow
            stream_list.ccol = ccol
            stream_list.cval = cval


        counter = counter + 1
    INPUT STREAM s1 CLOSE
    OS_DELETE VALUE ("/usr1/vhp/tmp/outputFO_" + htl_no + ".txt")
    OUTPUT STREAM s1 TO VALUE ("/usr1/vhp/tmp/outputFO_" + htl_no + ".txt") APPEND UNBUFFERED

    for stream_list in query(stream_list_list, sort_by=[("crow",False),("ccol",False)]):

        if stream_list.cval != "":
            pass
    OUTPUT STREAM s1 CLOSE
    OS_COMMAND SILENT VALUE ("php /usr1/vhp/php-script/write-sheet.php /usr1/vhp/tmp/outputFO_" + htl_no + ".txt " + gsheet_link)

    return generate_output()