
DEFINE INPUT PARAMETER pvILanguage  AS INTEGER  NO-UNDO.
DEF INPUT PARAMETER out-type AS INT.
DEF INPUT PARAMETER s-artnr  AS INT.
DEF INPUT PARAMETER transdate AS DATE.
DEF OUTPUT PARAMETER accepted AS LOGICAL INITIAL YES. 
DEF OUTPUT PARAMETER msg-str AS CHAR.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "s-stockout".

RUN check-artnr.

PROCEDURE check-artnr:
DEF BUFFER l-art FOR l-artikel. 
  IF out-type = 1 THEN RETURN. 
  FIND FIRST l-art WHERE l-art.artnr = s-artnr NO-LOCK. 
  FIND FIRST gl-acct WHERE gl-acct.fibukonto = l-art.fibukonto NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE gl-acct THEN 
  DO: 
    FIND FIRST l-untergrup WHERE l-untergrup.zwkum = l-art.zwkum NO-LOCK. 
    FIND FIRST gl-acct WHERE gl-acct.fibukonto = l-untergrup.fibukonto 
      NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE gl-acct THEN RETURN. 
  END. 
  FOR EACH gl-jouhdr WHERE gl-jouhdr.activeflag = 0 AND gl-jouhdr.BATCH 
    AND gl-jouhdr.jtype = 3 AND gl-jouhdr.datum GE transdate NO-LOCK: 
    FIND FIRST gl-journal WHERE gl-journal.jnr = gl-jouhdr.jnr 
      AND gl-journal.fibukonto = gl-acct.fibukonto 
      AND gl-journal.bemerk MATCHES("*;&&5;") NO-LOCK NO-ERROR. 
      IF AVAILABLE gl-journal THEN 
      DO: 
          msg-str = msg-str + CHR(2)
                  + translateExtended ("Journal Transfer to G/L found on",lvCAREA,"")
                  + " " + STRING(gl-jouhdr.datum).
          accepted = NO. 
          RETURN.
      END. 
  END. 
END. 
