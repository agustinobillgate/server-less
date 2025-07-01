DEF TEMP-TABLE r-list LIKE res-line
    FIELD select-flag AS LOGICAL INITIAL NO
.

DEFINE INPUT PARAMETER case-type AS INTEGER.
DEFINE INPUT PARAMETER resNo    AS INTEGER.
DEFINE INPUT PARAMETER sortType AS INTEGER.
DEFINE INPUT PARAMETER newResNo AS INTEGER.
DEFINE INPUT PARAMETER TABLE FOR r-list.
DEFINE OUTPUT PARAMETER done    AS LOGICAL INITIAL NO. 
DEFINE OUTPUT PARAMETER TABLE FOR r-list.

DEFINE VARIABLE ci-date AS DATE NO-UNDO.

FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK.
ASSIGN ci-date = htparam.fdate. 

IF case-type = 1 THEN
DO:
    RUN mk-r-list.
END.
ELSE 
DO:
    RUN update-it.
END.


PROCEDURE mk-r-list:
    IF sorttype = 1 THEN  /* Reservation  */ 
    FOR EACH res-line WHERE res-line.resnr = resNo 
        AND res-line.resstatus LE 5 NO-LOCK:
        CREATE r-list.
        BUFFER-COPY res-line TO r-list.
    END.
    ELSE IF sorttype = 2 THEN  /* Reservation  */ 
    FOR EACH res-line WHERE res-line.resnr = resNo 
        AND res-line.resstatus = 6 NO-LOCK:
        CREATE r-list.
        BUFFER-COPY res-line TO r-list.
    END.
    ELSE IF sorttype = 3 THEN  /* Arrival Today  */ 
    FOR EACH res-line WHERE res-line.resnr = resNo 
        AND res-line.resstatus LE 5 
        AND res-line.ankunft = ci-date NO-LOCK:
        CREATE r-list.
        BUFFER-COPY res-line TO r-list.
    END.
    ELSE IF sorttype = 4 THEN  /* ALL  */ 
    FOR EACH res-line WHERE res-line.resnr = resNo 
        AND res-line.active-flag LE 1 AND res-line.resstatus NE 11
        AND res-line.resstatus NE 12 
        AND res-line.resstatus NE 13 NO-LOCK:
        CREATE r-list.
        BUFFER-COPY res-line TO r-list.
    END.
END.

PROCEDURE update-it:
DEF BUFFER rbuff  FOR r-list.
DEF BUFFER msbuff FOR master.
DEF BUFFER mbill  FOR bill.
DEF BUFFER mbuff  FOR reservation.
DEF BUFFER rline  FOR res-line.
DEF BUFFER mainres FOR reservation.    

  IF newResNo = 0 THEN
  DO:
      FIND FIRST mainres NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE mainres THEN newResNo = 1. 
      ELSE newResNo = mainres.resnr + 1. 
  END.

  FOR EACH rline NO-LOCK BY rline.resnr DESCENDING:
      IF newResNo LE rline.resnr THEN newResNo = rline.resnr + 1.
      LEAVE.
  END.

    FIND FIRST reservation WHERE reservation.resnr = resNo NO-LOCK.
    DO TRANSACTION:
    CREATE mbuff.
    BUFFER-COPY reservation EXCEPT resnr depositgef limitdate limitdate2
        depositbez depositbez2 zahldatum zahldatum2
        zahlkonto zahlkonto2 bestat-datum TO mbuff.
    ASSIGN mbuff.resnr = newResNo.
    FIND CURRENT mbuff NO-LOCK.

    FIND FIRST master WHERE master.resnr = resNo NO-LOCK NO-ERROR.
    IF AVAILABLE master THEN
    DO:
      FIND FIRST counters WHERE counters.counter-no = 3 EXCLUSIVE-LOCK. 
      counters.counter = counters.counter + 1. 
      FIND CURRENT counters NO-LOCK. 
      CREATE msbuff.
      BUFFER-COPY master EXCEPT resnr rechnr TO msbuff.
      ASSIGN 
          msbuff.rechnr = counters.counter
          msbuff.resnr  = newResNo
      .
      FIND CURRENT msbuff NO-LOCK.

      FIND FIRST bill WHERE bill.resnr = resNo 
        AND bill.reslinnr = 0 NO-LOCK NO-ERROR.
      IF AVAILABLE bill THEN
      DO:
        CREATE mbill.
        BUFFER-COPY bill EXCEPT resnr rechnr saldo TO mbill.
        ASSIGN 
            mbill.rechnr = counters.counter
            mbill.resnr  = newResNo
            mbill.saldo  = 0
        .
        FIND CURRENT mbill NO-LOCK.
      END.
    END.

    FOR EACH rbuff WHERE rbuff.select-flag = YES:
      FIND FIRST res-line WHERE res-line.resnr = rbuff.resnr
          AND res-line.reslinnr = rbuff.reslinnr EXCLUSIVE-LOCK.

      IF res-line.resstatus = 6 THEN
      DO:
          FOR EACH bill WHERE bill.resnr = res-line.resnr
              AND bill.parent-nr = res-line.reslinnr:
              FIND FIRST rline WHERE rline.resnr = bill.resnr
                  AND rline.reslinnr = bill.reslinnr
                  AND rline.resstatus = 12 NO-ERROR.
              IF AVAILABLE rline THEN ASSIGN rline.resnr = newResNo.
              bill.resnr = newResNo.
          END.
      END.
      
      FIND FIRST gentable WHERE gentable.key = "reservation" 
        AND gentable.number1 = res-line.resnr 
        AND gentable.number2 = res-line.reslinnr NO-ERROR.
      IF AVAILABLE gentable THEN ASSIGN gentable.number1 = newResNo.
      
      FOR EACH rline WHERE rline.resnr = rbuff.resnr
          AND (rline.resstatus = 11 OR rline.resstatus = 13)
          AND rline.kontakt-nr = res-line.reslinnr:
          rline.resnr = newResNo.
      END.
      
      FOR EACH reslin-queasy WHERE reslin-queasy.KEY = "arrangement"
          AND reslin-queasy.resnr = res-line.resnr
          AND reslin-queasy.reslinnr = res-line.reslinnr:
          reslin-queasy.resnr = newResNo.
      END.
      
      FOR EACH reslin-queasy WHERE reslin-queasy.KEY = "resChanges"
          AND reslin-queasy.resnr = res-line.resnr
          AND reslin-queasy.reslinnr = res-line.reslinnr:
          reslin-queasy.resnr = newResNo.
      END.
      
      FOR EACH reslin-queasy WHERE reslin-queasy.KEY = "flag"
          AND reslin-queasy.resnr = res-line.resnr
          AND reslin-queasy.reslinnr = res-line.reslinnr:
          reslin-queasy.resnr = newResNo.
      END.
      
      FOR EACH reslin-queasy WHERE reslin-queasy.KEY = "fargt-line"
          AND reslin-queasy.resnr = res-line.resnr
          AND reslin-queasy.reslinnr = res-line.reslinnr:
          reslin-queasy.resnr = newResNo.
      END.
      
      FOR EACH res-history WHERE res-history.action = "Remark"
          AND res-history.resnr = res-line.resnr
          AND res-history.reslinnr = res-line.reslinnr:
          res-history.resnr = newResNo.
      END.
      
      FOR EACH res-history WHERE res-history.action = "Pickup"
          AND res-history.resnr = res-line.resnr
          AND res-history.reslinnr = res-line.reslinnr:
          res-history.resnr = newResNo.
      END.

      FOR EACH res-history WHERE res-history.action = "Drop"
          AND res-history.resnr = res-line.resnr
          AND res-history.reslinnr = res-line.reslinnr:
          res-history.resnr = newResNo.
      END.

      FOR EACH fixleist WHERE fixleist.resnr = res-line.resnr
          AND fixleist.reslinnr = res-line.reslinnr:
          fixleist.resnr = newResNo.
      END.
      
      ASSIGN res-line.resnr = newResNo.
      FIND CURRENT res-line NO-LOCK.
    END.
    ASSIGN done = YES.
  END.
END.
