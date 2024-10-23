DEF TEMP-TABLE t-h-bill LIKE h-bill
    FIELD rec-id AS INT.

DEF INPUT  PARAMETER pvILanguage     AS INTEGER NO-UNDO.
DEF INPUT PARAMETER tableno AS INT.
DEF INPUT PARAMETER curr-dept AS INT.
DEF OUTPUT PARAMETER err-code AS INT INIT 0.
DEF OUTPUT PARAMETER msg-str AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR t-h-bill.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "TS-transtisch".

  FIND FIRST vhp.tisch WHERE vhp.tisch.tischnr = tableno AND 
    vhp.tisch.departement = curr-dept NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE vhp.tisch THEN 
  DO:
    err-code = 1.
    RETURN NO-APPLY. 
  END. 
  ELSE 
  DO: 
    FIND FIRST vhp.h-bill WHERE vhp.h-bill.tischnr = tableno 
      AND vhp.h-bill.departement = curr-dept AND vhp.h-bill.flag = 0 
      NO-LOCK NO-ERROR.
    IF AVAILABLE h-bill THEN
    DO:
        CREATE t-h-bill.
        BUFFER-COPY h-bill TO t-h-bill.
        ASSIGN t-h-bill.rec-id = RECID(h-bill).

        FIND FIRST vhp.kellner WHERE vhp.kellner.kellner-nr = vhp.h-bill.kellner-nr 
            AND vhp.kellner.departement = curr-dept NO-LOCK NO-ERROR.
        IF AVAILABLE vhp.kellner THEN
        DO:
          msg-str = msg-str + CHR(2) + "&Q"
                  + translateExtended ("Transfer to table served by other waiter",lvCAREA,"")
                  + CHR(10)
                  + STRING(kellner.kellner-nr) + " - " + vhp.kellner.kellnername + "?".
        END.
    END.
    ELSE
    /*MT
    IF NOT AVAILABLE vhp.h-bill THEN 
    DO: 
      tischnr = tableno. 
    END. 
    ELSE 
    DO: 
      IF vhp.h-bill.rechnr GT 0 THEN 
      DO: 
        answer = YES. 
        hide MESSAGE NO-PAUSE. 
        MESSAGE translateExtended ("The selected table is already occupied.",lvCAREA,"") 
          SKIP 
          translateExtended ("Are you sure you want to move to this table?",lvCAREA,"") 
          VIEW-AS ALERT-BOX BUTTONS YES-NO UPDATE answer. 
        IF NOT answer THEN 
        DO: 
          tableno = 0. 
          DISP tableno WITH FRAME frame1. 
          APPLY "entry" TO tableno. 
          RETURN NO-APPLY. 
        END. 
      END. 
      IF vhp.h-bill.kellner-nr NE curr-waiter THEN 
      DO: 
        FIND FIRST vhp.kellner WHERE vhp.kellner.kellner-nr 
          = vhp.h-bill.kellner-nr 
          AND vhp.kellner.departement = curr-dept NO-LOCK NO-ERROR. 
        answer = YES. 
        IF AVAILABLE vhp.kellner THEN 
        DO: 
          hide MESSAGE NO-PAUSE. 
          MESSAGE translateExtended ("Transfer to table served by other waiter",lvCAREA,"") 
            SKIP 
            STRING(kellner.kellner-nr) + " - " + vhp.kellner.kellnername + "?" 
            VIEW-AS ALERT-BOX BUTTONS YES-NO UPDATE answer. 
          IF NOT answer THEN 
          DO: 
            tableno = 0. 
            APPLY "entry" TO tableno. 
            RETURN NO-APPLY. 
          END. 
          ELSE 
          DO: 
            tischnr = tableno. 
            bilrecid = RECID(h-bill). 
            new-waiter = vhp.kellner.kellner-nr. 
          END. 
        END. 
        ELSE 
        DO: 
          tischnr = tableno. 
          bilrecid = RECID(h-bill). 
        END. 
      END. 
      ELSE 
      DO: 
        tischnr = tableno. 
        bilrecid = RECID(h-bill). 
      END. 
    END. 
    */
  END. 
