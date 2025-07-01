DEFINE TEMP-TABLE s-list 
  FIELD s-recid     AS INTEGER 
  FIELD datum       AS DATE LABEL "Date" 
  FIELD artnr       AS INTEGER FORMAT "9999999" LABEL "ArtNo" 
  FIELD bezeich     AS CHAR FORMAT "x(30)" LABEL "Description" 
  FIELD einzelpreis AS DECIMAL FORMAT ">,>>>,>>>,>>9.999" LABEL "Unit Price" 
  FIELD price0      AS DECIMAL INITIAL ? 
  FIELD anzahl      AS DECIMAL FORMAT "->>,>>9.999" LABEL "Qty" 
  FIELD anz0        AS DECIMAL FORMAT "->,>>>9.999" INITIAL ? 
  FIELD brutto      AS DECIMAL FORMAT "->>,>>>,>>9.99" LABEL "      Amount" 
  FIELD val0        AS DECIMAL 
  FIELD disc        AS DECIMAL FORMAT ">9.99" LABEL "Disc" 
  FIELD disc0       AS DECIMAL 
  FIELD disc2       AS DECIMAL FORMAT ">9.99" LABEL "Disc2" 
  FIELD disc20      AS DECIMAL 
  FIELD disc-amt    AS DECIMAL FORMAT "->,>>>,>>9.99" LABEL "Disc-Amount" 
  FIELD disc2-amt   AS DECIMAL FORMAT "->,>>>,>>9.99" LABEL "Disc2-Amount" 
  FIELD vat         AS DECIMAL FORMAT ">9.99" LABEL "VAT%" 
  FIELD warenwert   AS DECIMAL FORMAT "->>,>>>,>>9.99" LABEL "Net-Amount" 
  FIELD vat0        AS DECIMAL 
  FIELD vat-amt     AS DECIMAL FORMAT "->,>>>,>>9.99" LABEL "VAT-Amount" 
  FIELD betriebsnr  AS INTEGER. 

DEF INPUT-OUTPUT PARAMETER TABLE FOR s-list.

DEFINE buffer s-list1 FOR s-list. 
    
FOR EACH s-list1 WHERE s-list1.betriebsnr = 0 OR 
    s-list1.betriebsnr = 10: 
    FIND FIRST l-op WHERE RECID(l-op) = s-list1.s-recid EXCLUSIVE-LOCK. 
    IF l-op.betriebsnr = 0 OR l-op.betriebsnr = 10 THEN 
    ASSIGN
      l-op.betriebsnr    = l-op.betriebsnr + 1 
      s-list1.betriebsnr = s-list1.betriebsnr + 1
    . 
    FIND CURRENT l-op NO-LOCK. 
END.
