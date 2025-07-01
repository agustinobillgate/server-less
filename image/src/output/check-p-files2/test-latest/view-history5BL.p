.
DEF TEMP-TABLE hjou-list
  FIELD artnr       AS INTEGER  FORMAT ">>>>9"               COLUMN-LABEL "ArtNo" 
  FIELD anzahl      AS INTEGER  FORMAT "->>>9"               COLUMN-LABEL "Qty" 
  FIELD bezeich     AS CHAR     FORMAT "x(21)"               COLUMN-LABEL "Description"
  FIELD epreis      AS DECIMAL  FORMAT "->,>>>,>>>,>>9.99"   COLUMN-LABEL "Unit Price"
  FIELD betrag      AS DECIMAL  FORMAT "->,>>>,>>>,>>9"      COLUMN-LABEL "Amount" 
  FIELD waehrungsnr AS INTEGER  FORMAT ">9"                  COLUMN-LABEL "No"
  FIELD bill-datum  AS DATE                                  COLUMN-LABEL "BillDate"
  FIELD zeit        AS INTEGER
.
DEF INPUT  PARAMETER billNo   AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER deptNo   AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER billDate AS DATE    NO-UNDO.
DEF OUTPUT PARAMETER TABLE FOR hjou-list.

FOR EACH h-journal WHERE h-journal.rechnr = billNo
  AND h-journal.departement = deptNo
  AND h-journal.bill-datum  = billDate NO-LOCK 
  BY h-journal.sysdate BY h-journal.zeit:
  CREATE hjou-list.
  BUFFER-COPY h-journal TO hjou-list.
END.
