DEF INPUT PARAMETER docu-nr AS CHAR.
DEF INPUT PARAMETER flag AS INT.

FIND FIRST gc-pi WHERE gc-pi.docu-nr = docu-nr NO-LOCK NO-ERROR. /* Malik Serverless 711 change EXCLUSIVE-LOCK -> NO-LOCK NO-ERROR */
IF AVAILABLE gc-pi THEN
DO:
    FIND CURRENT gc-pi EXCLUSIVE-LOCK.
    IF flag = 1 THEN
        ASSIGN gc-pi.printed1 = YES.
    ELSE IF flag = 2 THEN
        ASSIGN gc-pi.printed1A = YES.
    FIND CURRENT gc-pi NO-LOCK.
    RELEASE gc-pi.
END.
