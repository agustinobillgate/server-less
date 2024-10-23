
DEF INPUT PARAMETER case-type AS INT.
DEF INPUT PARAMETER user-init AS CHAR.
DEF INPUT PARAMETER acct-date AS DATE.

DEFINE BUFFER bparam FOR htparam.
DEFINE VARIABLE fdefault AS CHAR NO-UNDO.

IF case-type = 1 THEN
DO:
    DO transaction: 
        FIND FIRST htparam WHERE htparam.paramnr = 597 EXCLUSIVE-LOCK. 
        /* journal closing DATE */ 
        ASSIGN 
            htparam.fdate    = acct-date
            htparam.lupdate  = TODAY
            htparam.fdefault = user-init + " - " + STRING(TIME, "HH:MM:SS")
            fdefault         = htparam.fdefault. 
        FIND CURRENT htparam NO-LOCK. 
        RELEASE htparam.

        FIND FIRST bparam WHERE bparam.paramnr = 558 NO-LOCK NO-ERROR.
        IF AVAILABLE bparam THEN DO:
            FIND CURRENT bparam EXCLUSIVE-LOCK.
            ASSIGN bparam.fdefault = fdefault.
            FIND CURRENT bparam NO-LOCK.
            RELEASE bparam.
        END.
    END. 
END.
ELSE IF case-type = 2 THEN
DO:
    DEFINE VARIABLE curr-date       AS DATE. 
    FIND FIRST htparam WHERE htparam.paramnr = 597 no-lock.   /* journal closing DATE */ 
    curr-date = htparam.fdate. 

    FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK. 
    DO TRANSACTION:
      CREATE res-history.
      ASSIGN 
        res-history.nr = bediener.nr 
        res-history.datum = TODAY 
        res-history.zeit = TIME 
        res-history.aenderung = "Closing Month - " + STRING(curr-date)              
        res-history.action = "G/L". 
      FIND CURRENT res-history NO-LOCK. 
      RELEASE res-history. 
    END.
END.
