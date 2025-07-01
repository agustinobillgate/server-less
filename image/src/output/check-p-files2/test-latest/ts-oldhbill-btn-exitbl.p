
DEF INPUT  PARAMETER pvILanguage    AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER rechnr         AS INT.
DEF INPUT  PARAMETER curr-dept      AS INT.
DEF INPUT  PARAMETER supervise      AS LOGICAL.
DEF INPUT  PARAMETER bill-date      AS DATE.
DEF INPUT  PARAMETER knr            AS INT.
DEF OUTPUT PARAMETER tischnr        AS INT.
DEF OUTPUT PARAMETER flag-code      AS INT INIT 0.
DEF OUTPUT PARAMETER msg-str        AS CHAR INIT "".

{supertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "TS-oldhbill".

FIND FIRST vhp.hoteldpt WHERE vhp.hoteldpt.num = curr-dept NO-LOCK.

FIND FIRST vhp.h-bill WHERE vhp.h-bill.rechnr = rechnr 
  AND vhp.h-bill.departement = curr-dept 
  AND vhp.h-bill.flag = 1 NO-LOCK USE-INDEX rechnr_ix NO-ERROR. 
IF NOT AVAILABLE vhp.h-bill THEN 
DO: 
  msg-str = msg-str + CHR(2)
          + translateExtended ("No such closed bill number for POS department",lvCAREA,"")
          + CHR(10)
          + STRING(curr-dept) + " - " + vhp.hoteldpt.depart.
  flag-code = 1.
  RETURN NO-APPLY. 
END. 
IF NOT supervise THEN 
DO: 
  FIND FIRST vhp.h-journal WHERE vhp.h-journal.rechnr = rechnr 
    AND vhp.h-journal.departement = curr-dept 
    AND vhp.h-journal.bill-datum EQ bill-date NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE vhp.h-journal THEN 
  DO: 
    msg-str = msg-str + CHR(2)
            + translateExtended ("The closed bill is older than today",lvCAREA,"").
    flag-code = 2.
    RETURN NO-APPLY. 
  END. 
  IF vhp.h-bill.kellner-nr NE knr THEN 
  DO: 
    FIND FIRST vhp.kellner WHERE vhp.kellner.kellner-nr 
      = vhp.h-bill.kellner-nr NO-LOCK. 
    msg-str = msg-str + CHR(2)
            + translateExtended ("The bill belongs to other user:",lvCAREA,"") + " " 
            + vhp.kellner.kellnername.
    flag-code = 3.
    RETURN NO-APPLY. 
  END. 
END. 
tischnr = vhp.h-bill.tischnr. 
FIND FIRST vhp.tisch WHERE vhp.tisch.tischnr = tischnr NO-LOCK. 
