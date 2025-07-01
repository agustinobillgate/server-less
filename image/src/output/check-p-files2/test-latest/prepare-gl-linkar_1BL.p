
DEFINE OUTPUT PARAMETER f-int          AS INTEGER.
DEFINE OUTPUT PARAMETER last-acctdate  AS DATE.
DEFINE OUTPUT PARAMETER from-date      AS DATE.
DEFINE OUTPUT PARAMETER acct-date      AS DATE.
DEFINE OUTPUT PARAMETER close-year     AS DATE.
DEFINE OUTPUT PARAMETER msg-str        AS CHARACTER.
DEFINE INPUT-OUTPUT PARAMETER combo-pf-file1 AS CHAR    NO-UNDO.
DEFINE INPUT-OUTPUT PARAMETER combo-pf-file2 AS CHAR    NO-UNDO.
DEFINE INPUT-OUTPUT PARAMETER combo-gastnr   AS INTEGER NO-UNDO.
DEFINE INPUT-OUTPUT PARAMETER combo-ledger   AS INTEGER NO-UNDO.
DEFINE INPUT-OUTPUT PARAMETER combo-gl-link  AS LOGICAL NO-UNDO.

DEFINE VARIABLE last-acct-period AS DATE.

IF combo-gastnr = ? THEN
DO:
    FIND FIRST vhp.htparam WHERE vhp.htpara.paramnr = 155 NO-LOCK. 
    combo-gastnr = vhp.htparam.finteger.
    IF combo-gastnr GT 0 THEN
    DO:
        FIND FIRST guest WHERE guest.gastnr = combo-gastnr NO-LOCK NO-ERROR.
        IF NOT AVAILABLE guest THEN combo-gastnr = 0.
        ELSE ASSIGN combo-ledger = guest.zahlungsart.
        IF combo-ledger GT 0 THEN
        DO:
            FIND FIRST artikel WHERE artikel.artnr = combo-ledger
                AND artikel.departement = 0
                AND artikel.artart = 2 NO-LOCK NO-ERROR.
            IF NOT AVAILABLE artikel THEN
            ASSIGN
                combo-gastnr = 0
                combo-ledger = 0
            .
        END.
        ELSE combo-gastnr = 0.
    END.
    ELSE combo-gastnr = 0.
END.
IF combo-gastnr GT 0 THEN
DO:
    FIND FIRST vhp.htparam WHERE vhp.htpara.paramnr = 339 NO-LOCK. 
    combo-pf-file1 = vhp.htparam.fchar. 
    FIND FIRST vhp.htparam WHERE vhp.htpara.paramnr = 340 NO-LOCK. 
    combo-pf-file2 = vhp.htparam.fchar.
    FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 343 NO-LOCK.
    ASSIGN combo-gl-link = vhp.htparam.flogical.
END.

FIND FIRST htparam WHERE htparam.paramnr = 1012 NO-LOCK.
IF htparam.paramgr = 38 AND htparam.feldtyp = 1 AND htparam.finteger GT 0 THEN
    f-int = htparam.finteger.

FIND FIRST htparam WHERE paramnr = 1014 no-lock.    /* LAST A/R Transfer DATE */ 
ASSIGN
    last-acctdate = htparam.fdate
    from-date = last-acctdate + 1. 


FIND FIRST htparam WHERE paramnr = 597 no-lock.   /* CURRENT Accounting Period */ 
acct-date = htparam.fdate. 
 
FIND FIRST htparam WHERE paramnr = 795 NO-LOCK. 
close-year = htparam.fdate. 

FIND FIRST htparam WHERE paramnr = 558 no-lock.   /* LAST Accounting Period */ 
last-acct-period = htparam.fdate.

/*FDL Dec 22, 2023 => Ticket 221A85*/
/*IF (last-acctdate + 1) LE last-acct-period THEN FT serverless*/
IF from-date LE last-acct-period THEN
DO:
    msg-str = "Last AR transfer to GL (Param 1014) lower then last accounting closing period (Param 558)."
        + CHR(10)    
        + "Transfer to GL not possible."
        .
    RETURN.
END.
