
DEF TEMP-TABLE bill-list    LIKE billhis. 

DEF INPUT  PARAMETER resnr    AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER reslinnr AS INTEGER NO-UNDO.
DEF OUTPUT PARAMETER TABLE FOR bill-list.

FOR EACH bill WHERE bill.resnr = resnr 
  AND bill.parent-nr = reslinnr NO-LOCK BY bill.billnr: 
  CREATE bill-list. 
  BUFFER-COPY bill TO bill-list. 
END. 
  
IF NOT AVAILABLE bill-list THEN 
DO: 
  FOR EACH billhis WHERE billhis.resnr = resnr 
    AND billhis.parent-nr = reslinnr NO-LOCK BY billhis.billnr: 
    CREATE bill-list. 
    BUFFER-COPY billhis TO bill-list. 
  END. 
END. 
