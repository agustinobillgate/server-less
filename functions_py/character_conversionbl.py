#using conversion tools version: 1.0.0.117
"""_yusufwijasena_28/10/2025

    Returns:
        _type_: _description_
"""

from functions.additional_functions import *
from decimal import Decimal

def character_conversionbl(inp_val:str, longinput:str):
    body = ""
    longbody = ""
    str = ""
    longstr = ""

    db_session = local_storage.db_session

    def generate_output():
        nonlocal body, longbody, str, longstr
        nonlocal inp_val, longinput
        return {"body": body, "longbody": longbody}


    if inp_val != "" and longinput == "":
        str = inp_val
        str = replace_str(str, chr_unicode(173) , "")
        str = replace_str(str, chr_unicode(176) , "")
        str = replace_str(str, chr_unicode(186) , "")
        str = replace_str(str, chr_unicode(212) , chr_unicode(111))
        str = replace_str(str, chr_unicode(221) , chr_unicode(121))
        str = replace_str(str, chr_unicode(222) , chr_unicode(84) + chr_unicode(72))
        str = replace_str(str, chr_unicode(223) , chr_unicode(115) + chr_unicode(115))
        str = replace_str(str, chr_unicode(224) , chr_unicode(97))
        str = replace_str(str, chr_unicode(225) , chr_unicode(97))
        str = replace_str(str, chr_unicode(226) , chr_unicode(97))
        str = replace_str(str, chr_unicode(195) , chr_unicode(97))
        str = replace_str(str, chr_unicode(220) , chr_unicode(117))
        str = replace_str(str, chr_unicode(227) , chr_unicode(97))
        str = replace_str(str, chr_unicode(228) , chr_unicode(97))
        str = replace_str(str, chr_unicode(229) , chr_unicode(97))
        str = replace_str(str, chr_unicode(230) , chr_unicode(97) + chr_unicode(101))
        str = replace_str(str, chr_unicode(231) , chr_unicode(99))
        str = replace_str(str, chr_unicode(232) , chr_unicode(101))
        str = replace_str(str, chr_unicode(233) , chr_unicode(101))
        str = replace_str(str, chr_unicode(234) , chr_unicode(101))
        str = replace_str(str, chr_unicode(235) , chr_unicode(101))
        str = replace_str(str, chr_unicode(236) , chr_unicode(105))
        str = replace_str(str, chr_unicode(237) , chr_unicode(105))
        str = replace_str(str, chr_unicode(238) , chr_unicode(105))
        str = replace_str(str, chr_unicode(239) , chr_unicode(105))
        str = replace_str(str, chr_unicode(240) , chr_unicode(100))
        str = replace_str(str, chr_unicode(241) , chr_unicode(110))
        str = replace_str(str, chr_unicode(242) , chr_unicode(111))
        str = replace_str(str, chr_unicode(243) , chr_unicode(111))
        str = replace_str(str, chr_unicode(244) , chr_unicode(111))
        str = replace_str(str, chr_unicode(245) , chr_unicode(111))
        str = replace_str(str, chr_unicode(214) , chr_unicode(111))
        str = replace_str(str, chr_unicode(246) , chr_unicode(111))
        str = replace_str(str, chr_unicode(248) , chr_unicode(111))
        str = replace_str(str, chr_unicode(249) , chr_unicode(117))
        str = replace_str(str, chr_unicode(250) , chr_unicode(117))
        str = replace_str(str, chr_unicode(251) , chr_unicode(117))
        str = replace_str(str, chr_unicode(252) , chr_unicode(117))
        str = replace_str(str, chr_unicode(254) , chr_unicode(116) + chr_unicode(104))
        str = replace_str(str, chr_unicode(34) , "")
        str = replace_str(str, chr_unicode(247) , "")
        str = replace_str(str, chr_unicode(189) , "")
        str = replace_str(str, chr_unicode(177) , "")
        str = replace_str(str, chr_unicode(160) , chr_unicode(32))
        str = replace_str(str, chr_unicode(178) , chr_unicode(50))
        str = replace_str(str, chr_unicode(191) , chr_unicode(63))
        str = replace_str(str, chr_unicode(215) , chr_unicode(120))
        str = replace_str(str, chr_unicode(183) , chr_unicode(46))
        body = str

    elif inp_val == "" and longinput != "":
        longstr = longinput
        longstr = replace_str(longstr, chr_unicode(173) , "")
        longstr = replace_str(longstr, chr_unicode(176) , "")
        longstr = replace_str(longstr, chr_unicode(186) , "")
        longstr = replace_str(longstr, chr_unicode(212) , chr_unicode(111))
        longstr = replace_str(longstr, chr_unicode(220) , chr_unicode(117))
        longstr = replace_str(longstr, chr_unicode(221) , chr_unicode(121))
        longstr = replace_str(longstr, chr_unicode(222) , chr_unicode(84) + chr_unicode(72))
        longstr = replace_str(longstr, chr_unicode(223) , chr_unicode(115) + chr_unicode(115))
        longstr = replace_str(longstr, chr_unicode(224) , chr_unicode(97))
        longstr = replace_str(longstr, chr_unicode(225) , chr_unicode(97))
        longstr = replace_str(longstr, chr_unicode(226) , chr_unicode(97))
        longstr = replace_str(longstr, chr_unicode(195) , chr_unicode(97))
        longstr = replace_str(longstr, chr_unicode(227) , chr_unicode(97))
        longstr = replace_str(longstr, chr_unicode(228) , chr_unicode(97))
        longstr = replace_str(longstr, chr_unicode(229) , chr_unicode(97))
        longstr = replace_str(longstr, chr_unicode(230) , chr_unicode(97) + chr_unicode(101))
        longstr = replace_str(longstr, chr_unicode(231) , chr_unicode(99))
        longstr = replace_str(longstr, chr_unicode(232) , chr_unicode(101))
        longstr = replace_str(longstr, chr_unicode(233) , chr_unicode(101))
        longstr = replace_str(longstr, chr_unicode(234) , chr_unicode(101))
        longstr = replace_str(longstr, chr_unicode(235) , chr_unicode(101))
        longstr = replace_str(longstr, chr_unicode(236) , chr_unicode(105))
        longstr = replace_str(longstr, chr_unicode(237) , chr_unicode(105))
        longstr = replace_str(longstr, chr_unicode(238) , chr_unicode(105))
        longstr = replace_str(longstr, chr_unicode(239) , chr_unicode(105))
        longstr = replace_str(longstr, chr_unicode(240) , chr_unicode(100))
        longstr = replace_str(longstr, chr_unicode(241) , chr_unicode(110))
        longstr = replace_str(longstr, chr_unicode(242) , chr_unicode(111))
        longstr = replace_str(longstr, chr_unicode(243) , chr_unicode(111))
        longstr = replace_str(longstr, chr_unicode(244) , chr_unicode(111))
        longstr = replace_str(longstr, chr_unicode(245) , chr_unicode(111))
        longstr = replace_str(longstr, chr_unicode(214) , chr_unicode(111))
        longstr = replace_str(longstr, chr_unicode(246) , chr_unicode(111))
        longstr = replace_str(longstr, chr_unicode(248) , chr_unicode(111))
        longstr = replace_str(longstr, chr_unicode(249) , chr_unicode(117))
        longstr = replace_str(longstr, chr_unicode(250) , chr_unicode(117))
        longstr = replace_str(longstr, chr_unicode(251) , chr_unicode(117))
        longstr = replace_str(longstr, chr_unicode(252) , chr_unicode(117))
        longstr = replace_str(longstr, chr_unicode(254) , chr_unicode(116) + chr_unicode(104))
        longstr = replace_str(longstr, chr_unicode(247) , "")
        longstr = replace_str(longstr, chr_unicode(189) , "")
        longstr = replace_str(longstr, chr_unicode(177) , "")
        longstr = replace_str(longstr, chr_unicode(160) , chr_unicode(32))
        longstr = replace_str(longstr, chr_unicode(178) , chr_unicode(50))
        longstr = replace_str(longstr, chr_unicode(191) , chr_unicode(63))
        longstr = replace_str(longstr, chr_unicode(215) , chr_unicode(120))
        longstr = replace_str(longstr, chr_unicode(183) , chr_unicode(46))
        longbody = longstr

    return generate_output()