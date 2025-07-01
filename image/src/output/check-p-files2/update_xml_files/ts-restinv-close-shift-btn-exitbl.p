DEFINE TEMP-TABLE shift-list
    FIELD rechnr     LIKE vhp.h-bill.rechnr FORMAT ">>>>>9"
    FIELD tischnr    LIKE vhp.h-bill.tischnr
    FIELD selectFlag AS LOGICAL COLUMN-LABEL "Selected" INITIAL YES
    FIELD bstr       AS CHAR LABEL ""
.

DEFINE TEMP-TABLE user-list
  FIELD kellner-nr   AS INTEGER.
  
DEF INPUT PARAMETER pvILanguage     AS INTEGER NO-UNDO.
DEF INPUT-OUTPUT PARAMETER TABLE FOR shift-list.
DEF INPUT PARAMETER all-user        AS LOGICAL.
DEF INPUT PARAMETER curr-dept       AS INT.
DEF INPUT PARAMETER billdate        AS DATE.
DEF INPUT PARAMETER kellner-kellner-nr AS INT.
DEF INPUT PARAMETER shift           AS INT.
DEF INPUT PARAMETER user-init       AS CHAR.
DEF OUTPUT PARAMETER flag           AS INT INIT 0.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "TS-restinv".

DEF VAR do-it AS LOGICAL.
DEF BUFFER sbuff FOR shift-list.
DEFINE BUFFER hbline FOR vhp.h-bill-line.

  FOR EACH user-list:
      DELETE user-list.
  END.
  IF all-user THEN
  DO:
    FOR EACH h-journal WHERE h-journal.departement = curr-dept
      AND h-journal.bill-datum = billdate NO-LOCK:
      FIND FIRST user-list WHERE user-list.kellner-nr = h-journal.kellner-nr
          NO-ERROR.
      IF NOT AVAILABLE user-list THEN
      DO:
          CREATE user-list.
          ASSIGN user-list.kellner-nr = h-journal.kellner-nr.
      END.
    END.
  END.
  ELSE
  DO:
    CREATE user-list.
    ASSIGN user-list.kellner-nr = kellner-kellner-nr.
  END.
 
  FOR EACH user-list:
    FOR EACH vhp.h-bill WHERE vhp.h-bill.flag EQ 1 AND vhp.h-bill.departement = curr-dept 
      AND vhp.h-bill.kellner-nr = user-list.kellner-nr NO-LOCK USE-INDEX dept1_ix: 
      IF all-user THEN do-it = YES.
      ELSE
      DO:
        FIND FIRST sbuff WHERE sbuff.rechnr = vhp.h-bill.rechnr
          AND sbuff.selectflag = YES NO-ERROR.
        do-it = AVAILABLE sbuff.
      END.
      IF do-it THEN
      DO:
        FIND FIRST vhp.h-bill-line WHERE vhp.h-bill-line.rechnr = vhp.h-bill.rechnr 
          AND vhp.h-bill-line.bill-datum = billdate 
          AND vhp.h-bill-line.departement = curr-dept 
          AND vhp.h-bill-line.zeit GE 0 AND vhp.h-bill-line.betriebsnr = 0 NO-LOCK 
          NO-ERROR. 
        DO TRANSACTION WHILE AVAILABLE vhp.h-bill-line: 
          FIND FIRST hbline WHERE RECID(hbline) = RECID(h-bill-line) 
              EXCLUSIVE-LOCK. 
          hbline.betriebsnr = shift. 
          FIND CURRENT hbline NO-LOCK. 
          RELEASE hbline. 
          FIND NEXT vhp.h-bill-line WHERE vhp.h-bill-line.rechnr = vhp.h-bill.rechnr 
            AND vhp.h-bill-line.bill-datum = billdate 
            AND vhp.h-bill-line.departement = curr-dept 
            AND vhp.h-bill-line.zeit GE 0 AND vhp.h-bill-line.betriebsnr = 0 
            NO-LOCK NO-ERROR. 
        END.
      END.
    END.
  END.

  IF all-user THEN
  DO:
      DO TRANSACTION :
          FIND FIRST vhp.bediener WHERE vhp.bediener.userinit = user-init NO-LOCK NO-ERROR.
          CREATE res-history.
          ASSIGN res-history.nr     = vhp.bediener.nr
              res-history.datum     = TODAY
              res-history.zeit      = TIME
              res-history.aenderung = "Close Shift(ALL)"
              res-history.action    = "POS Cashier".
          FIND CURRENT res-history NO-LOCK.
          RELEASE res-history.
      END.
      flag = 1.
  END.
  ELSE
  DO:
    FIND FIRST sbuff WHERE sbuff.selectflag = NO NO-ERROR.
    IF NOT AVAILABLE sbuff THEN
        flag = 2.
    ELSE
        flag = 3.
  END. 
