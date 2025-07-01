
DEF INPUT PARAMETER wgrpgen-eknr    AS INT.
DEF OUTPUT PARAMETER flag           AS INT INIT 0.

FIND FIRST artikel WHERE artikel.endkum = wgrpgen-eknr NO-LOCK NO-ERROR. 
IF AVAILABLE artikel THEN 
DO: 
    ASSIGN flag = 1.
END. 
ELSE 
DO:
    /*Alder - Serverless - Issue 335 - Start*/
    
    /*
    FIND FIRST wgrpgen WHERE wgrpgen.eknr = wgrpgen-eknr.
    FIND CURRENT wgrpgen EXCLUSIVE-LOCK. 
    delete wgrpgen.
    */

    FIND FIRST wgrpgen WHERE wgrpgen.eknr EQ wgrpgen-eknr NO-LOCK NO-ERROR.
    IF AVAILABLE wgrpgen THEN
    DO:
        FIND CURRENT wgrpgen EXCLUSIVE-LOCK.
        DELETE wgrpgen.
        RELEASE wgrpgen.
    END.

    /*Alder - Serverless - Issue 335 - End*/
END.
