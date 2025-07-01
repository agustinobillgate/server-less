
DEF INPUT  PARAMETER bkf-veran-nr       AS INT.
DEF INPUT  PARAMETER bkf-veran-seite    AS INT.
DEF INPUT  PARAMETER bkf-resstatus      AS INT.
DEF OUTPUT PARAMETER rsv2-resstatus     AS INT.
DEF OUTPUT PARAMETER avail-rsv2         AS LOGICAL INIT NO.

DEFINE buffer rsv2 FOR bk-reser. 
DEFINE buffer bk-reser1 FOR bk-reser. 

FIND FIRST bk-reser1 WHERE bk-reser1.veran-nr = bkf-veran-nr AND 
    bk-reser1.veran-resnr = bkf-veran-seite USE-INDEX vernr-ix 
    NO-LOCK NO-ERROR. 
FIND FIRST rsv2 WHERE rsv2.datum = bk-reser1.datum 
    AND rsv2.raum = bk-reser1.raum AND rsv2.resstatus = bkf-resstatus 
    AND NOT rsv2.von-i GE bk-reser1.bis-i 
    AND NOT rsv2.bis-i LE bk-reser1.von-i 
    AND RECID(rsv2) NE RECID(bk-reser1) NO-LOCK NO-ERROR. 
IF AVAILABLE rsv2 THEN 
DO:
    rsv2-resstatus = rsv2.resstatus.
    avail-rsv2 = YES.
END.


