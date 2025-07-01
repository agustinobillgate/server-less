
DEF TEMP-TABLE t-history    LIKE history.
DEF TEMP-TABLE bline-list   LIKE blinehis
  FIELD transflag AS LOGICAL INITIAL NO.

DEF INPUT  PARAMETER rechnr AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER TABLE FOR t-history.
DEF OUTPUT PARAMETER TABLE FOR bline-list.

  FIND FIRST t-history.

  FOR EACH bill-line WHERE bill-line.rechnr = rechnr NO-LOCK 
    BY bill-line.sysdate DESCENDING BY bill-line.zeit DESCENDING: 
    CREATE bline-list. 
    BUFFER-COPY bill-line TO bline-list. 
  END. 

  FOR EACH bill-line WHERE bill-line.rechnr NE rechnr
    AND bill-line.bill-datum GE t-history.ankunft
    AND bill-line.bill-datum LE t-history.abreise
    AND bill-line.massnr = t-history.resnr
    AND bill-line.billin-nr = t-history.reslinnr NO-LOCK:
    CREATE bline-list.
    BUFFER-COPY bill-line TO bline-list. 
    ASSIGN bline-list.transflag = YES.
  END.
  
  IF NOT AVAILABLE bline-list THEN 
  FOR EACH blinehis WHERE blinehis.rechnr = rechnr NO-LOCK 
    BY blinehis.sysdate DESCENDING BY blinehis.zeit DESCENDING: 
    CREATE bline-list. 
    BUFFER-COPY blinehis TO bline-list. 
  END. 
