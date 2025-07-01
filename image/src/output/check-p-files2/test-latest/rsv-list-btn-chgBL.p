
DEF INPUT  PARAMETER output-list-resstatus AS INT.
DEF INPUT  PARAMETER output-list-resnr     AS INT.
DEF INPUT  PARAMETER output-list-reslinnr  AS INT.
DEF OUTPUT PARAMETER recid-bk-reser        AS INT.
DEF OUTPUT PARAMETER avail-bk-reser        AS LOGICAL INIT NO.

IF output-list-resstatus = 1 THEN 
DO: 
  FIND FIRST bk-veran WHERE bk-veran.veran-nr = output-list-resnr 
    USE-INDEX vernr-ix NO-LOCK NO-ERROR. 
  IF AVAILABLE bk-veran THEN /*FT serverless*/
  DO:
    IF (bk-veran.deposit-payment[1] + bk-veran.deposit-payment[2] 
      + bk-veran.deposit-payment[3] + bk-veran.deposit-payment[4] 
      + bk-veran.deposit-payment[5] + bk-veran.deposit-payment[6] 
      + bk-veran.deposit-payment[7] + bk-veran.deposit-payment[8] 
      + bk-veran.deposit-payment[9]) NE 0 THEN 
    DO: 
      FIND FIRST bk-reser WHERE bk-reser.veran-nr = bk-veran.veran-nr 
        AND bk-reser.veran-resnr NE output-list-reslinnr 
        AND bk-reser.resstatus = 1 NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE bk-reser THEN 
      DO: 
        avail-bk-reser = NO.
        /*MT
        HIDE MESSAGE NO-PAUSE. 
        MESSAGE translateExtended ("Deposit exists, status change not possible.",lvCAREA,"") 
            VIEW-AS ALERT-BOX INFORMATION. 
        APPLY "entry" TO from-date.
        */
        RETURN NO-APPLY. 
      END. 
      ELSE 
      DO:
        avail-bk-reser = YES.
        recid-bk-reser = RECID(bk-reser).
      END.
    END. 
    ELSE 
    DO: /*ITA 291015*/
      FIND FIRST bk-reser WHERE bk-reser.veran-nr = bk-veran.veran-nr 
        AND bk-reser.veran-resnr = output-list-reslinnr 
        AND bk-reser.resstatus = 1 NO-LOCK NO-ERROR. 
      IF AVAILABLE bk-reser THEN
      DO:
        avail-bk-reser = YES.
        recid-bk-reser = RECID(bk-reser).
      END.
    END.
  END.
END. 
ELSE 
DO:
  FIND FIRST bk-veran WHERE bk-veran.veran-nr = output-list-resnr 
    USE-INDEX vernr-ix NO-LOCK NO-ERROR. 
  IF AVAILABLE bk-veran THEN /*FT serverless*/
  DO:
    IF (bk-veran.deposit-payment[1] + bk-veran.deposit-payment[2] 
      + bk-veran.deposit-payment[3] + bk-veran.deposit-payment[4] 
      + bk-veran.deposit-payment[5] + bk-veran.deposit-payment[6] 
      + bk-veran.deposit-payment[7] + bk-veran.deposit-payment[8] 
      + bk-veran.deposit-payment[9]) NE 0 THEN 
    DO: 
      FIND FIRST bk-reser WHERE bk-reser.veran-nr = bk-veran.veran-nr 
        AND bk-reser.veran-resnr = output-list-reslinnr 
        AND bk-reser.resstatus = output-list-resstatus NO-LOCK NO-ERROR. 
      IF AVAILABLE bk-reser THEN 
      DO:
        avail-bk-reser = YES.
        recid-bk-reser = RECID(bk-reser).
      END.
      ELSE
      DO:
        avail-bk-reser = NO.
        RETURN NO-APPLY.
      END.
    END.
    ELSE 
    DO:
      FIND FIRST bk-reser WHERE bk-reser.veran-nr = bk-veran.veran-nr 
        AND bk-reser.veran-resnr = output-list-reslinnr 
        AND bk-reser.resstatus = output-list-resstatus NO-LOCK NO-ERROR. 
      IF AVAILABLE bk-reser THEN 
      DO:
        avail-bk-reser = YES.
        recid-bk-reser = RECID(bk-reser).
      END.
    END.
  END.
END.

/*MTFIND FIRST bk-reser WHERE bk-reser.veran-nr = output-list-resnr 
  AND bk-reser.veran-seite = output-list-reslinnr NO-LOCK. 

RUN chg-bastatus-line.p(RECID(bk-reser), OUTPUT r-status, OUTPUT c-status). 
IF r-status NE 0 AND r-status NE output-list.resstatus THEN 
DO: 
  RUN update-resstatus(r-status, c-status). 
  b1:REFRESH(). 
END. 
*/
