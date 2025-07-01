DEF TEMP-TABLE queasy-list
    FIELD number1 LIKE vhp.queasy.number1
    FIELD char1   LIKE vhp.queasy.char1   FORMAT "x(4)"
    FIELD char2   LIKE vhp.queasy.char2.

DEF OUTPUT PARAMETER TABLE FOR queasy-list.

FOR EACH vhp.queasy WHERE vhp.queasy.key = 10 NO-LOCK BY vhp.queasy.char2:
    CREATE queasy-list.
    ASSIGN
    queasy-list.number1 = vhp.queasy.number1
    queasy-list.char1   = vhp.queasy.char1
    queasy-list.char2   = vhp.queasy.char2.
END.
