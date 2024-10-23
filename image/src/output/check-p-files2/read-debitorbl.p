DEF TEMP-TABLE t-debitor LIKE debitor
    FIELD tb-recid      AS INTEGER.

DEF INPUT PARAMETER case-type AS INTEGER NO-UNDO.
DEF INPUT PARAMETER artNo     AS INTEGER NO-UNDO.
DEF INPUT PARAMETER billNo    AS INTEGER NO-UNDO.
DEF INPUT PARAMETER billDate  AS DATE    NO-UNDO.
DEF INPUT PARAMETER saldo     AS DECIMAL NO-UNDO.
DEF INPUT PARAMETER inp-opart AS INTEGER NO-UNDO.
DEF INPUT PARAMETER inp-konto AS INTEGER NO-UNDO.
DEF OUTPUT PARAMETER TABLE FOR t-debitor.

CASE case-type:
  WHEN 1 THEN
  FIND FIRST debitor WHERE debitor.artnr = artNo 
    AND debitor.rechnr = billNo AND debitor.opart = inp-opart 
    AND debitor.zahlkonto = inp-konto NO-LOCK NO-ERROR. 

  WHEN 2 THEN
  FIND FIRST debitor WHERE debitor.artnr = artNo
    AND debitor.rechnr = billNo AND debitor.opart = inp-opart
    AND debitor.zahlkonto GT inp-konto NO-LOCK NO-ERROR. 

  WHEN 3 THEN
  FIND FIRST debitor WHERE debitor.artnr = artNo 
    AND debitor.rechnr = billNo AND debitor.opart = inp-opart 
    AND debitor.zahlkonto = inp-konto NO-LOCK NO-ERROR. 

  WHEN 4 THEN
  FIND FIRST debitor WHERE debitor.artnr = artNo 
    AND debitor.rechnr = billNo 
    AND debitor.rgdatum = billDate
    AND debitor.opart = inp-opart 
    AND debitor.zahlkonto = inp-konto NO-LOCK NO-ERROR. 

  WHEN 5 THEN
  FIND FIRST debitor WHERE debitor.artnr = artNo 
    AND debitor.rechnr = billNo 
    AND debitor.rgdatum = billDate
    AND debitor.saldo = saldo
    AND debitor.opart = inp-opart 
    AND debitor.zahlkonto = inp-konto NO-LOCK NO-ERROR. 
  WHEN 6 THEN
  FIND FIRST debitor WHERE debitor.artnr = artNo 
      AND debitor.rechnr = billNo 
      AND debitor.rgdatum = billDate
      AND debitor.saldo = - saldo
      AND debitor.counter = inp-opart NO-LOCK NO-ERROR. 
  WHEN 7 THEN
  FIND FIRST debitor WHERE RECID(debitor) = artNo NO-LOCK NO-ERROR.
  WHEN 8 THEN
  FIND FIRST debitor WHERE debitor.counter = inp-opart
      AND debitor.zahlkonto > 0 AND debitor.rgdatum LE billDate
      NO-LOCK NO-ERROR.
  WHEN 9 THEN
  FIND FIRST debitor WHERE debitor.rechnr = billNo
      AND debitor.artnr = artNo AND debitor.gastnr = inp-konto 
      AND debitor.gastnrmember = inp-konto 
      AND debitor.rgdatum = billDate AND debitor.saldo = - saldo 
      AND debitor.counter = 0 NO-LOCK NO-ERROR.

  WHEN 99 THEN
  FIND FIRST debitor WHERE RECID(debitor) = artNo EXCLUSIVE-LOCK.

END CASE.

IF AVAILABLE debitor THEN
DO:
  CREATE t-debitor.
  BUFFER-COPY debitor TO t-debitor.
  t-debitor.tb-recid = RECID(debitor).
END.
