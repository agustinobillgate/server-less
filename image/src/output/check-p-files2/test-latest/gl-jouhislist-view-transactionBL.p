DEFINE TEMP-TABLE detail-trans 
    FIELD fibukonto AS CHAR
    FIELD debit     AS DECIMAL
    FIELD credit    AS DECIMAL
    FIELD bemerk    AS CHAR
    FIELD userinit  AS CHAR
    FIELD sysdate   AS DATE
    FIELD chginit   AS CHAR
    FIELD chgdate   AS DATE
    FIELD bezeich   AS CHAR.

DEFINE INPUT PARAMETER jnr AS INTEGER NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR detail-trans.

DEFINE BUFFER gl-jou FOR gl-jourhis. 
DEFINE BUFFER gl-acct1 FOR gl-acct. 


FUNCTION get-bemerk RETURNS CHAR(bemerk AS CHAR): 
DEF VAR n AS INTEGER. 
DEF VAR s1 AS CHAR. 
  bemerk = REPLACE(bemerk, CHR(10), " ").
  n = INDEX(bemerk, ";&&"). 
  IF n > 0 THEN s1 = SUBSTR(bemerk, 1, n - 1). 
  ELSE s1 = bemerk.
  RETURN s1. 
END. 

FOR EACH gl-jou WHERE gl-jou.jnr = jnr NO-LOCK, 
    FIRST gl-acct1 WHERE gl-acct1.fibukonto = gl-jou.fibukonto NO-LOCK 
    BY gl-acct1.fibukonto:
    
    CREATE detail-trans.
    ASSIGN 
        detail-trans.fibukonto = gl-acct1.fibukonto
        detail-trans.debit     = gl-jou.debit
        detail-trans.credit    = gl-jou.credit
        detail-trans.bemerk    = STRING(get-bemerk(gl-jou.bemerk), "x(50)")
        detail-trans.userinit  = gl-jou.userinit
        detail-trans.sysdate   = gl-jou.sysdate 
        detail-trans.chginit   = gl-jou.chginit
        detail-trans.chgdate   = gl-jou.chgdate
        detail-trans.bezeich   = gl-acct1.bezeich.

END.
