
DEF INPUT  PARAMETER pvILanguage    AS INTEGER NO-UNDO.
DEF INPUT PARAMETER curr-waiter AS INT.
DEF INPUT PARAMETER new-dept AS INT.
DEF INPUT PARAMETER zugriff AS LOGICAL.
DEF INPUT PARAMETER exchg-rate AS DECIMAL.

DEF OUTPUT PARAMETER deptname AS CHAR.
DEF OUTPUT PARAMETER b-title AS CHAR.
DEF OUTPUT PARAMETER msg-str AS CHAR.
DEF OUTPUT PARAMETER fl-code AS INT INIT 0.

{supertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "TS-restinv".

DEFINE BUFFER waiter     FOR vhp.kellner.

FIND FIRST waiter WHERE waiter.kellner-nr = curr-waiter 
  AND waiter.departement = new-dept NO-LOCK NO-ERROR. 
IF AVAILABLE waiter THEN 
DO: 
  IF zugriff THEN 
  DO: 
    FIND FIRST vhp.kellner WHERE RECID(kellner) = RECID(waiter) NO-LOCK. 
    /*MTRUN clear-bill-display. */
    FIND FIRST vhp.hoteldpt WHERE vhp.hoteldpt.num = new-dept NO-LOCK. 
    deptname = vhp.hoteldpt.depart. 
    b-title = vhp.hoteldpt.depart + " " 
        + translateExtended ("Bills",lvCAREA,""). 
    IF AVAILABLE vhp.waehrung THEN 
      b-title = b-title + " / " 
        + translateExtended ("Today's Exchange Rate",lvCAREA,"") 
        + " = " + STRING(exchg-rate). 
    fl-code = 1.
    RETURN NO-APPLY. 
  END. 
END. 
ELSE DO: 
  fl-code = 2.
  msg-str = msg-str + CHR(2)
          + translateExtended ("Waiter-account not defined in the selected department",lvCAREA,"").
END. 
