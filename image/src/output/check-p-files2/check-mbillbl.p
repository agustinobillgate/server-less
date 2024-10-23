
DEFINE TEMP-TABLE c-list 
  FIELD name    AS CHAR FORMAT "x(36)" 
  FIELD rechnr  AS INTEGER FORMAT ">>,>>>,>>9" 
  FIELD saldo   AS DECIMAL FORMAT "->>>,>>>,>>9.99" 
  FIELD zinr    LIKE zimmer.zinr
  FIELD abreise AS DATE. 

DEF OUTPUT PARAMETER TABLE FOR c-list.

FOR EACH bill WHERE resnr GT 0 AND reslinnr = 0 AND flag = 0 NO-LOCK 
  BY bill.saldo descending  BY bill.name: 
  FIND FIRST res-line WHERE res-line.resnr = bill.resnr 
    AND res-line.active-flag LE 1 NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE res-line THEN 
  DO: 
    FIND FIRST res-line WHERE res-line.resnr = bill.resnr 
      AND res-line.resstatus = 8 NO-LOCK NO-ERROR. 
    DISP bill.rechnr bill.name FORMAT "x(24)" bill.saldo. 
    IF AVAILABLE res-line THEN DISP res-line.abreise res-line.zinr. 
    create c-list. 
    c-list.rechnr = bill.rechnr. 
    c-list.name = bill.name. 
    c-list.saldo = bill.saldo. 
    IF AVAILABLE res-line THEN 
    DO: 
      c-list.abreise = res-line.abreise. 
      c-list.zinr = res-line.zinr. 
    END. 
  END. 
END. 
