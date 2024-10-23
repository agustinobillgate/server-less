
DEF INPUT  PARAMETER pvILanguage    AS INTEGER          NO-UNDO.
DEF INPUT  PARAMETER pay-acctNo     AS CHAR.
DEF OUTPUT PARAMETER gc-PIacct-bezeich AS CHAR.
DEF OUTPUT PARAMETER p-558          AS DATE.
DEF OUTPUT PARAMETER msg-str        AS CHAR.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "mk-gcPI".

IF pay-acctNo NE "" THEN
DO:
    FIND FIRST gc-PIacct WHERE gc-PIacct.fibukonto = pay-acctNo NO-LOCK NO-ERROR.
    IF NOT AVAILABLE gc-PIacct THEN
    DO:
        msg-str = msg-str + CHR(2)
                + translateExtended ("PI Payment Account Number not found.", lvCAREA,"").
        RETURN.
    END.
    FIND FIRST gl-acct WHERE gl-acct.fibukonto = pay-acctNo NO-LOCK NO-ERROR.
    IF NOT AVAILABLE gl-acct THEN
    DO:
        msg-str = msg-str + CHR(2)
                + translateExtended ("GL Account Number not found.", lvCAREA,"").
        RETURN.
    END.
END.

FIND FIRST htparam WHERE htparam.paramnr = 558 NO-LOCK.
p-558 = htparam.fdate.

gc-PIacct-bezeich = gc-PIacct.bezeich.
