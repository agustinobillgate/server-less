

DEF INPUT  PARAMETER pvILanguage    AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER billdate       AS DATE.
DEF INPUT  PARAMETER dept           AS INT.
DEF INPUT  PARAMETER curr-rechnr    AS INT.
DEF INPUT  PARAMETER kbuff-kellner-nr AS INT.

DEF OUTPUT PARAMETER otherKellner   AS CHAR.
DEF OUTPUT PARAMETER msg-str        AS CHAR.

{supertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "TS-hbline".

FIND FIRST vhp.h-journal WHERE vhp.h-journal.bill-datum = billdate
  AND vhp.h-journal.departement = dept
  AND vhp.h-journal.rechnr = curr-rechnr
  AND vhp.h-journal.kellner-nr NE kbuff-kellner-nr 
  AND vhp.h-journal.kellner-nr NE 0 NO-LOCK NO-ERROR.
IF AVAILABLE vhp.h-journal THEN
DO:
  FIND FIRST vhp.kellner WHERE vhp.kellner.kellner-nr = vhp.h-journal.kellner-nr
      AND vhp.kellner.departement = dept NO-LOCK NO-ERROR.
  IF AVAILABLE vhp.kellner THEN otherKellner = vhp.kellner.kellnername.
  msg-str = msg-str + CHR(2) + "&W"
          + translateExtended ("This table is being used by other user:",lvCAREA,"")
          + " " + otherKellner.
  /*MTanswer = NO.*/
END.
