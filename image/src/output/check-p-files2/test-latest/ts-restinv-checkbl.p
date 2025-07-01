DEF INPUT-OUTPUT PARAMETER exchg-rate AS DECIMAL.
DEF INPUT PARAMETER transdate AS DATE.
DEF INPUT PARAMETER double-currency AS LOGICAL.

FIND FIRST vhp.htparam WHERE paramnr = 110 NO-LOCK.
IF vhp.htparam.fdate NE transdate AND double-currency THEN 
DO:
  FIND FIRST vhp.exrate WHERE vhp.exrate.datum = transdate 
    NO-LOCK NO-ERROR.
  IF AVAILABLE vhp.exrate THEN exchg-rate = vhp.exrate.betrag.
END.
