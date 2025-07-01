
DEFINE INPUT PARAMETER res-mode AS CHAR.
DEFINE INPUT PARAMETER resNo    AS INTEGER.
DEFINE INPUT PARAMETER reslinNo AS INTEGER.
DEFINE INPUT PARAMETER new-zinr LIKE zimmer.zinr.

RUN release-zinr.

PROCEDURE release-zinr:
DEFINE VARIABLE res-recid1  AS INTEGER.
DEFINE VARIABLE beg-datum   AS DATE.
DEFINE VARIABLE answer      AS LOGICAL.
DEFINE VARIABLE parent-nr   AS INTEGER.
DEFINE BUFFER rline     FOR res-line.
DEFINE BUFFER res-line1 FOR res-line.
DEFINE BUFFER res-line2 FOR res-line.

  FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK.

  FIND FIRST rline WHERE rline.resnr = resNo 
      AND rline.reslinnr = reslinNo NO-LOCK.
  if rline.zinr NE "" THEN
  DO: 
    beg-datum = rline.ankunft. 
    res-recid1 = 0.

    if res-mode = "delete" OR res-mode = "cancel" 
      AND rline.resstatus = 1 THEN 
    DO TRANSACTION:
      FIND FIRST res-line1 WHERE res-line1.resnr = resNo
        AND res-line1.zinr = rline.zinr AND res-line1.resstatus = 11
        NO-LOCK NO-ERROR.
      if AVAILABLE res-line1 THEN 
      DO:
        FIND CURRENT res-line1 EXCLUSIVE-LOCK.
        res-line1.resstatus = 1.
        FIND CURRENT res-line1 NO-LOCK.
        res-recid1 = RECID(res-line1).
      END.
    END.    
    if res-mode = "inhouse" THEN 
    DO:
      answer = yes.
      beg-datum = htparam.fdate.

      if rline.resstatus = 6 AND (rline.zinr NE new-zinr) THEN
      DO TRANSACTION:
        FIND FIRST res-line1 WHERE res-line1.resnr = resNo
          AND res-line1.zinr = rline.zinr AND res-line1.resstatus = 13 
          NO-LOCK NO-ERROR.
        if AVAILABLE res-line1 THEN 
        DO:       
          FOR EACH res-line2 WHERE res-line2.resnr = resNo
              AND res-line2.zinr = rline.zinr AND res-line2.resstatus = 13 
              EXCLUSIVE-LOCK:
            FIND FIRST bill WHERE bill.resnr = resNo
              AND bill.reslinnr = res-line2.reslinnr AND bill.flag = 0 
              AND bill.zinr = res-line2.zinr EXCLUSIVE-LOCK.
            bill.zinr = new-zinr.
            parent-nr = bill.parent-nr.
            FIND CURRENT bill NO-LOCK.
            FOR EACH bill WHERE bill.resnr = resNo 
              AND bill.parent-nr = parent-nr AND bill.flag = 0
              AND bill.zinr = res-line2.zinr EXCLUSIVE-LOCK:
              bill.zinr = new-zinr.
              RELEASE bill.
            END.
            res-line2.zinr = new-zinr.
            RELEASE res-line2.
          END.
          FIND FIRST zimmer WHERE zimmer.zinr = rline.zinr EXCLUSIVE-LOCK.
          zimmer.zistatus = 2.
          FIND CURRENT zimmer NO-LOCK.
        END.
      END.
    END.
    DO:
      FOR EACH zimplan WHERE zimplan.zinr = rline.zinr 
          AND zimplan.datum GE beg-datum
          AND zimplan.datum LT rline.abreise EXCLUSIVE-LOCK:
        if res-recid1 NE 0 THEN zimplan.res-recid = res-recid1.
        ELSE delete zimplan.
      END.
    END.
  END.
END. 
 
