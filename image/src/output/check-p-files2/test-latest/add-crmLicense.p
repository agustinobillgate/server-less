FIND FIRST htparam WHERE htparam.paramnr = 1459 NO-LOCK.
IF htparam.paramgr NE 99 THEN
DO :
    FIND CURRENT htparam EXCLUSIVE-LOCK.
    ASSIGN
        htparam.paramgr     = 99
        htparam.bezeich     = "License FOR CRM Module"
        htparam.feldtyp     = 4
        htparam.flogical    = NO
        htparam.fchar       = ""
        htparam.reihenfolge = 1073
    .
END.
