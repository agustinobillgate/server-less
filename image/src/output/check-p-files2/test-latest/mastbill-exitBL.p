DEF INPUT PARAMETER resnr           AS INTEGER  NO-UNDO.
DEF INPUT PARAMETER gastnrpay       AS INTEGER  NO-UNDO.
DEF INPUT PARAMETER rechnrstart     AS INTEGER  NO-UNDO.
DEF INPUT PARAMETER rechnrend       AS INTEGER  NO-UNDO.
DEF INPUT PARAMETER curr-segm       AS INTEGER  NO-UNDO.
DEF INPUT PARAMETER master-active   AS LOGICAL  NO-UNDO.
DEF INPUT PARAMETER umsatz1         AS LOGICAL  NO-UNDO.
DEF INPUT PARAMETER umsatz3         AS LOGICAL  NO-UNDO.
DEF INPUT PARAMETER umsatz4         AS LOGICAL  NO-UNDO.
DEF INPUT PARAMETER bill-receiver   AS CHAR     NO-UNDO.

    FIND FIRST master WHERE master.resnr = resnr EXCLUSIVE-LOCK. 
    ASSIGN 
        master.ACTIVE       = master-active 
        master.rechnrstart  = rechnrstart 
        master.rechnrend    = rechnrend 
        master.umsatzart[1] = umsatz1
        master.umsatzart[2] = master.umsatzart[1] 
        master.umsatzart[3] = umsatz3
        master.umsatzart[4] = umsatz4 
        master.gastnrpay    = gastnrpay 
        master.name         = bill-receiver
    . 
    FIND CURRENT master NO-LOCK. 
 
    IF NOT master.active THEN 
    DO: 
      FIND FIRST reservation WHERE reservation.resnr = resnr EXCLUSIVE-LOCK. 
      reservation.verstat = 0. 
      FIND CURRENT reservation NO-LOCK. 
    END. 
    ELSE DO: 
      FIND FIRST reservation WHERE reservation.resnr = resnr EXCLUSIVE-LOCK. 
      reservation.verstat = 1. 
      FIND CURRENT reservation NO-LOCK. 
    END. 
 
    FIND FIRST bill WHERE bill.resnr = resnr AND bill.reslinnr = 0 
      EXCLUSIVE-LOCK NO-ERROR. 
    IF NOT AVAILABLE bill THEN 
    DO: 
      CREATE bill. 
      ASSIGN
        bill.resnr    = resnr
        bill.reslinnr = 0
        bill.rgdruck  = 1 
        bill.billtyp  = 2
      . 
      FIND FIRST counters WHERE counters.counter-no = 3 EXCLUSIVE-LOCK. 
      counters.counter = counters.counter + 1. 
      bill.rechnr = counters.counter. 
      FIND CURRENT counter NO-LOCK. 
      FIND CURRENT master EXCLUSIVE-LOCK. 
      master.rechnr = bill.rechnr. 
      FIND CURRENT master NO-LOCK. 
    END.
    ASSIGN
      bill.gastnr       = gastnrpay 
      bill.name         = bill-receiver 
      bill.segmentcode  = curr-segm
    . 
    FIND CURRENT bill NO-LOCK. 
