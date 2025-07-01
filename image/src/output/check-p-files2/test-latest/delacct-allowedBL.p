
DEF INPUT  PARAMETER pvILanguage  AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER from-acct    AS CHAR.
DEF INPUT  PARAMETER mess-it      AS LOGICAL. 
DEF OUTPUT PARAMETER do-it        AS LOGICAL INITIAL NO.
DEF OUTPUT PARAMETER msg-str      AS CHAR.

{SupertransBL.i}
DEF VAR lvCAREA AS CHAR INITIAL "gl-export-import-journal".

FIND FIRST gl-acct WHERE gl-acct.fibukonto = from-acct 
    NO-LOCK NO-ERROR.
IF NOT AVAILABLE gl-acct THEN
DO:
    msg-str = translateExtended ("No such Account Number:",lvCAREA,"")
            + " " + from-acct.
    RETURN.
END.

RUN delacct-allowed.

PROCEDURE delacct-allowed: 
  FIND FIRST gl-journal WHERE gl-journal.fibukonto = gl-acct.fibukonto 
    NO-LOCK NO-ERROR. 
  IF AVAILABLE gl-journal THEN 
  DO: 
    IF mess-it THEN 
    DO: 
      msg-str = msg-str + CHR(2)
              + translateExtended ("G/L Journal entry exists, deleting not possible.",lvCAREA,"").
    END. 
    RETURN. 
  END. 
  FIND FIRST artikel WHERE artikel.fibukonto = gl-acct.fibukonto 
    NO-LOCK NO-ERROR. 
  IF AVAILABLE artikel THEN 
  DO: 
    IF mess-it THEN 
    DO: 
      msg-str = msg-str + CHR(2)
              + translateExtended ("Front-office Article exists, deleting not possible",lvCAREA,"") 
              + CHR(10)
              + STRING(artikel.artnr) + " - " + artikel.bezeich.
    END. 
    RETURN. 
  END. 
  FIND FIRST parameters WHERE parameters.progname = "CostCenter" 
    AND parameters.section = "Alloc" AND parameters.vtype = 1 
    AND parameters.vstring = gl-acct.fibukonto NO-LOCK NO-ERROR. 
  IF AVAILABLE parameters THEN 
  DO: 
    IF mess-it THEN 
    DO: 
      msg-str = msg-str + CHR(2)
              + translateExtended ("Cost Allocation exists, deleting not possible.",lvCAREA,"").
    END. 
    RETURN. 
  END. 
  do-it = YES. 
END. 
