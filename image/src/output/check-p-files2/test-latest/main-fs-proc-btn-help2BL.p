
DEFINE buffer rsv2 FOR bk-reser. 
DEFINE buffer bk-reser1 FOR bk-reser. 
DEFINE buffer bkfc FOR bk-func. 

DEF INPUT PARAMETER room AS CHAR.
DEF INPUT PARAMETER bkf-veran-nr AS INT.
DEF INPUT PARAMETER bkf-veran-seite AS INT.
DEF INPUT PARAMETER bkf-raeume-1 AS CHAR.
DEF OUTPUT PARAMETER err AS INT INIT 0.
DEF OUTPUT PARAMETER t-raeume AS CHAR.

FIND FIRST bk-raum WHERE bk-raum.raum = room USE-INDEX raum-ix NO-LOCK NO-ERROR. 
IF AVAILABLE bk-raum THEN 
DO: 
  FIND FIRST bk-reser1 WHERE bk-reser1.veran-nr = bkf-veran-nr AND 
    bk-reser1.veran-resnr = bkf-veran-seite USE-INDEX vernr-ix 
    NO-LOCK NO-ERROR. 
  IF AVAILABLE bk-reser1 THEN 
  DO: 
    FIND FIRST rsv2 WHERE rsv2.datum = bk-reser1.datum 
      AND rsv2.raum = bkf-raeume-1 AND rsv2.resstatus = bk-reser1.resstatus 
    AND NOT rsv2.von-i GE bk-reser1.bis-i 
    AND NOT rsv2.bis-i LE bk-reser1.von-i 
    AND RECID(rsv2) NE RECID(bk-reser1) NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE rsv2 THEN 
    DO: 
        err = 1.
    END. 
    ELSE 
    DO: 
        FIND FIRST bkfc WHERE bkfc.veran-nr = bkf-veran-nr 
          AND bkfc.veran-seite = bkf-veran-seite NO-LOCK NO-ERROR. 
        t-raeume = bkfc.raeume[1]. 
        err = 2.
    END. 
  END. 
END.
