


DEF INPUT  PARAMETER pvILanguage   AS INTEGER      NO-UNDO.
DEF INPUT  PARAMETER curr-mode     AS CHAR.
DEF INPUT  PARAMETER elim-journal  AS LOGICAL.
DEF INPUT  PARAMETER fibukonto     AS CHAR.

DEF OUTPUT PARAMETER acct-bez      AS CHAR.
DEF OUTPUT PARAMETER flag-code     AS INTEGER INIT 0.
DEF OUTPUT PARAMETER msg-str       AS CHAR.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "gl-postjourn".

FIND FIRST gl-acct WHERE gl-acct.fibukonto = fibukonto
  AND gl-acct.activeflag = YES AND gl-acct.bezeich NE "" NO-LOCK NO-ERROR.
IF NOT AVAILABLE gl-acct THEN
DO:
  msg-str = msg-str + CHR(2)
          + translateExtended ("No such account found.",lvCAREA,"").
  RETURN NO-APPLY.
END.

IF elim-journal THEN 
DO: 
  FIND FIRST queasy WHERE queasy.key = 108 AND queasy.char1 = fibukonto 
    NO-LOCK NO-ERROR. 
  IF AVAILABLE queasy THEN 
    FIND FIRST gl-acct WHERE gl-acct.fibukonto = queasy.char2 NO-LOCK. 
  fibukonto = gl-acct.fibukonto. 
END. 
acct-bez = gl-acct.bezeich.

IF gl-acct.acc-type = 2 OR gl-acct.acc-type = 3 OR gl-acct.acc-type = 5 THEN
DO:
  flag-code = 1.
  RETURN NO-APPLY.
END.
ELSE IF gl-acct.acc-type = 1 OR gl-acct.acc-type = 4 THEN
DO:
  flag-code = 2.
  RETURN NO-APPLY.
END.
