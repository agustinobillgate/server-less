DEFINE TEMP-TABLE shift-list
    FIELD rechnr     LIKE vhp.h-bill.rechnr FORMAT ">>>>>9"
    FIELD tischnr    LIKE vhp.h-bill.tischnr
    FIELD selectFlag AS LOGICAL COLUMN-LABEL "Selected" INITIAL YES
    FIELD bstr       AS CHAR LABEL ""
.

DEF INPUT PARAMETER pvILanguage     AS INTEGER NO-UNDO.
DEF INPUT PARAMETER curr-dept AS INT.
DEF INPUT PARAMETER curr-waiter AS INT.
DEF OUTPUT PARAMETER billdate AS DATE.
DEF OUTPUT PARAMETER msg-str AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR shift-list.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "TS-restinv".

DEFINE buffer hbill FOR vhp.h-bill.
DEFINE BUFFER hbline FOR vhp.h-bill-line.

FIND FIRST vhp.h-bill WHERE vhp.h-bill.departement = curr-dept 
    AND vhp.h-bill.flag = 0 AND vhp.h-bill.kellner-nr = curr-waiter NO-LOCK NO-ERROR. 
IF AVAILABLE vhp.h-bill THEN 
DO: 
  msg-str = msg-str + CHR(2)
          + translateExtended ("Opened bill found:",lvCAREA,"") + " " 
          + translateExtended ("Table No:", lvCAREA, "") + " " 
          + STRING(h-bill.tischnr) 
          + CHR(10)
          + translateExtended ("Close Shift not possible.",lvCAREA,"").
  RETURN. 
END. 
 
FIND FIRST htparam WHERE htparam.paramnr = 110 NO-LOCK. 
billdate = htparam.fdate.



FOR EACH shift-list:
    DELETE shift-list.
END.
FOR EACH hbill WHERE hbill.flag EQ 1 AND hbill.departement = curr-dept 
    AND hbill.kellner-nr = curr-waiter  NO-LOCK USE-INDEX dept1_ix,
    FIRST hbline WHERE hbline.rechnr = hbill.rechnr 
    AND hbline.bill-datum = billdate 
    AND hbline.departement = curr-dept 
    AND hbline.zeit GE 0 AND hbline.betriebsnr = 0 NO-LOCK
    BY hbill.tischnr:
    CREATE shift-list.
    ASSIGN
        shift-list.rechnr  = hbill.rechnr
        shift-list.tischnr = hbill.tischnr
    .
END.
