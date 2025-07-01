DEFINE TEMP-TABLE trans-dept
    FIELD nr AS INTEGER.

DEFINE INPUT  PARAMETER pvILanguage    AS INTEGER      NO-UNDO.
DEFINE OUTPUT PARAMETER f-int          AS INTEGER.
DEFINE OUTPUT PARAMETER last-acctdate  AS DATE.
DEFINE OUTPUT PARAMETER acct-date      AS DATE.
DEFINE OUTPUT PARAMETER close-year     AS DATE.
DEFINE OUTPUT PARAMETER price-decimal  AS INTEGER.
DEFINE OUTPUT PARAMETER cash-fibu      AS CHAR.
DEFINE OUTPUT PARAMETER msg-str        AS CHAR.
DEFINE INPUT-OUTPUT PARAMETER combo-pf-file1 AS CHAR    NO-UNDO.
DEFINE INPUT-OUTPUT PARAMETER combo-pf-file2 AS CHAR    NO-UNDO.
DEFINE INPUT-OUTPUT PARAMETER combo-gastnr   AS INTEGER NO-UNDO.
DEFINE INPUT-OUTPUT PARAMETER combo-ledger   AS INTEGER NO-UNDO.
DEFINE INPUT-OUTPUT PARAMETER combo-gl-link  AS LOGICAL NO-UNDO.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "gl-linkfo". 

DEFINE VARIABLE last-acct-period AS DATE.
DEFINE VARIABLE tmpDate AS DATE.

DEFINE BUFFER art2              FOR artikel.

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

RUN check-dept.

FIND FIRST htparam WHERE paramnr = 1003 no-lock.  /* LAST FO Transfer DATE */ 
last-acctdate = htparam.fdate. 
FIND FIRST htparam WHERE paramnr = 597 no-lock.   /* CURRENT Accounting Period */ 
acct-date = htparam.fdate. 
FIND FIRST htparam WHERE paramnr = 558 no-lock.   /* LAST Accounting Period */ 
last-acct-period = htparam.fdate. 

FIND FIRST htparam WHERE paramnr = 795 NO-LOCK. 
close-year = htparam.fdate. 

FIND FIRST htparam WHERE htparam.paramnr = 491 NO-LOCK. 
price-decimal = htparam.finteger.   /* non-digit OR digit version */ 


FIND FIRST htparam WHERE htparam.paramnr = 112 NO-LOCK. 
FIND FIRST art2 WHERE art2.artnr = htparam.finteger 
  AND art2.departement = 0 AND art2.artart = 6 
  AND NOT art2.pricetab NO-LOCK NO-ERROR. 
IF NOT AVAILABLE art2 THEN 
DO: 
  msg-str = msg-str + CHR(2)
          + translateExtended ("Local Cash Article not defined! (Param 112 / Grp 5).",lvCAREA,"").
  RETURN. 
END. 
FIND FIRST gl-acct WHERE gl-acct.fibukonto = art2.fibukonto 
  NO-LOCK NO-ERROR. 
IF NOT AVAILABLE gl-acct THEN 
DO: 
  msg-str = msg-str + CHR(2)
          + translateExtended ("AcctNo of Cash Article",lvCAREA,"") + " " + STRING(art2.artnr) + " " + translateExtended ("not defined.",lvCAREA,"").
  RETURN. 
END. 

ASSIGN
    cash-fibu = gl-acct.fibukonto
    tmpDate = last-acctdate + 1.

/*FDL Dec 22, 2023 => Ticket 221A85*/
IF tmpDate LE last-acct-period THEN
DO:
    msg-str = msg-str + CHR(2)
        + translateExtended ("Last FO transfer to GL (Param 1003) lower then last accounting closing period (Param 558).",lvCAREA,"")
        + CHR(10)    
        + translateExtended ("Transfer to GL not possible.",lvCAREA,"")
        .
    RETURN.
END.

PROCEDURE check-dept:
    DEF VAR i AS INTEGER NO-UNDO.

    FOR EACH trans-dept:
        DELETE trans-dept.
    END.

    FIND FIRST htparam WHERE paramnr = 793 NO-LOCK.
    IF htparam.fchar NE "" THEN
    DO:
        DO i = 1 TO NUM-ENTRIES(htparam.fchar, ","):
            FIND FIRST trans-dept WHERE trans-dept.nr = INTEGER(ENTRY(i, htparam.fchar, ",")) 
                NO-ERROR.
            IF NOT AVAILABLE trans-dept THEN
            DO:
                CREATE trans-dept.
                ASSIGN nr = INTEGER(ENTRY(i, htparam.fchar, ",")) .
            END.
        END.
    END.
    ELSE
    DO:
        FOR EACH hoteldpt NO-LOCK:
            CREATE trans-dept.
            ASSIGN nr = hoteldpt.num.
        END.
    END.
END.
