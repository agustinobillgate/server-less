
DEF TEMP-TABLE t-bill          LIKE bill
    FIELD bl-recid      AS INTEGER.

DEF INPUT  PARAMETER case-type  AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER billNo     AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER resNo      AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER reslinNo   AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER actFlag    AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER roomNo     AS CHAR    NO-UNDO.
DEF INPUT  PARAMETER datum1     AS DATE    NO-UNDO.
DEF INPUT  PARAMETER datum2     AS DATE    NO-UNDO.
DEF INPUT  PARAMETER saldo1     AS DECIMAL NO-UNDO.
DEF INPUT  PARAMETER saldo2     AS DECIMAL NO-UNDO.
DEF OUTPUT PARAMETER TABLE FOR t-bill.

/* SY 04 June 2016 */
DEFINE BUFFER rline FOR res-line.

 /* SY 07 June 2016 */
DEFINE BUFFER bbuff FOR bill.

/*ITA 130616*/
DEF VARIABLE bl-saldo  AS DECIMAL NO-UNDO.
DEFINE BUFFER tbuff FOR bill.

CASE case-type:
  WHEN 1 THEN 
  DO:
    FIND FIRST bill WHERE bill.rechnr = billNo NO-LOCK NO-ERROR.
    IF AVAILABLE bill THEN RUN cr-bill.
  END.
  WHEN 2 THEN
  DO:
      FOR EACH bill WHERE bill.resnr = resNo AND bill.parent-nr = reslinNo
          AND bill.parent-nr NE 0 AND bill.flag = actFlag 
          AND bill.zinr = roomNo NO-LOCK: 
          RUN cr-bill.
      END.
  END.
  WHEN 3 THEN
  DO:
      FIND FIRST bill WHERE bill.resnr = resNo 
          AND bill.parent-nr = reslinNo AND bill.billnr = billNo 
          AND bill.flag = actFlag AND bill.zinr = roomNo NO-LOCK. 
      IF AVAILABLE bill THEN RUN cr-bill.
  END.
  WHEN 4 THEN
  DO:
      FOR EACH bill WHERE bill.resnr = resNo AND bill.parent-nr = reslinNo
          AND bill.flag = actFlag AND bill.zinr = roomNo NO-LOCK: 
          RUN cr-bill.
      END.
  END.
  WHEN 5 THEN
  DO:
      FIND FIRST bill WHERE RECID(bill) = billNo NO-LOCK NO-ERROR.
      IF AVAILABLE bill THEN RUN cr-bill.
  END.                                   
  WHEN 6 THEN 
  DO:
    FIND FIRST bill WHERE bill.flag = actFlag AND bill.datum GE datum1
        AND bill.datum LE datum2 AND bill.saldo NE 0
        USE-INDEX flagdat_ix NO-LOCK NO-ERROR.
    IF AVAILABLE bill THEN RUN cr-bill.
  END.
  WHEN 7 THEN
  DO:
      FIND FIRST bill WHERE bill.flag = actFlag
          AND (bill.saldo GE saldo1 OR bill.saldo LE - saldo2) NO-LOCK NO-ERROR.
      IF AVAILABLE bill THEN RUN cr-bill.
  END.
  WHEN 8 THEN
  DO:
      FIND FIRST bill WHERE bill.flag = actFlag AND bill.vesrdepot = roomNo 
          AND bill.billtyp = billNo USE-INDEX vesr2_ix NO-LOCK NO-ERROR. 
      IF AVAILABLE bill THEN RUN cr-bill.
  END.
  WHEN 9 THEN
  DO:
      FIND FIRST bill WHERE bill.flag = actFlag 
          AND bill.rechnr = reslinNo
          AND bill.resnr = resNo
          AND bill.reslinnr = 1
          AND bill.billtyp = billNo
          USE-INDEX vesr2_ix NO-LOCK NO-ERROR. 
      IF AVAILABLE bill THEN RUN cr-bill.
  END.
    /* SY 07 June 2016 */
    WHEN 10 OR WHEN 11 THEN
    DO:
      IF actflag = 0 THEN
      FOR EACH res-line WHERE res-line.active-flag = 1
            AND res-line.zinr = roomNo
            AND res-line.resstatus NE 12 
            AND res-line.l-zuordnung[3] = 0 NO-LOCK:

          FOR EACH bill WHERE bill.resnr = res-line.resnr
            AND bill.parent-nr = res-line.reslinnr
            AND bill.flag = 0 NO-LOCK:

            IF bill.zinr NE res-line.zinr THEN
            DO:
                FIND FIRST bbuff WHERE RECID(bbuff) = RECID(bill)
                    EXCLUSIVE-LOCK.
                ASSIGN bbuff.zinr = res-line.zinr.
                FIND CURRENT bbuff NO-LOCK.
              RELEASE bbuff.
            END.
            RUN cr-bill.
          END.
      END.      
      ELSE
      FOR EACH bill WHERE bill.zinr = roomNo
          AND bill.flag = actFlag NO-LOCK,
          FIRST res-line WHERE res-line.resnr = bill.resnr
          AND res-line.reslinnr = bill.reslinnr NO-LOCK:
          RUN cr-bill.
      END.
  END.
  
/* SY 07 June 2016 */
/*
/* SY 04 June 2016 */
  WHEN 11 THEN
  DO:
      IF actflag = 0 THEN
      FOR EACH bill WHERE bill.zinr = roomNo
          AND bill.flag = 0 NO-LOCK,
          FIRST rline WHERE rline.resnr = bill.resnr
          AND rline.reslinnr = bill.parent-nr 
          AND rline.active-flag = 1 NO-LOCK:
          RUN cr-bill.
      END.      
      ELSE
      FOR EACH bill WHERE bill.zinr = roomNo
          AND bill.flag = actFlag NO-LOCK:
          RUN cr-bill.
      END.
  END.
*/

  WHEN 12 THEN
  DO:
      FIND FIRST bill WHERE bill.resnr = resNo 
          AND bill.parent-nr = reslinNo 
          AND bill.parent-nr NE 0 AND bill.billnr = billNo 
          AND bill.flag = actFlag AND bill.zinr = roomNo NO-LOCK. 
      IF AVAILABLE bill THEN RUN cr-bill.
  END.

END CASE.

PROCEDURE cr-bill:
    ASSIGN bl-saldo = 0.
    FOR EACH bill-line WHERE bill-line.rechnr = bill.rechnr NO-LOCK:
          ASSIGN bl-saldo = bl-saldo + bill-line.betrag.
    END.

    IF bl-saldo NE bill.saldo THEN DO:
        FIND FIRST tbuff WHERE RECID(tbuff) = RECID(bill) EXCLUSIVE-LOCK.
        tbuff.saldo = bl-saldo.
        FIND CURRENT tbuff NO-LOCK.
        RELEASE tbuff.
    END.

    CREATE t-bill.
    FIND CURRENT bill NO-LOCK.
    BUFFER-COPY bill TO t-bill.
    t-bill.bl-recid = RECID(bill).
END.
