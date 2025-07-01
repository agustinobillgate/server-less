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

DEFINE TEMP-TABLE sub-list 
  FIELD zwkum       AS INTEGER FORMAT ">>9"
  FIELD bezeich     AS CHAR FORMAT "x(30)" 
  FIELD amt         AS DECIMAL  FORMAT "->>,>>>,>>>,>>9.99" 
  FIELD disc        AS DECIMAL FORMAT "->,>>>,>>>,>>9.99" 
  FIELD disc2       AS DECIMAL FORMAT "->,>>>,>>>,>>9.99" 
  FIELD vat         AS DECIMAL  FORMAT "->,>>>,>>>,>>9.99".

DEF INPUT  PARAMETER TABLE FOR s-list.
DEF OUTPUT PARAMETER TABLE FOR sub-list.

FOR EACH s-list BY s-list.bezeich BY s-list.betriebsnr:
    FIND FIRST l-artikel WHERE l-artikel.artnr = s-list.artnr NO-LOCK. 
    FIND FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum NO-LOCK. 
    FIND FIRST sub-list WHERE sub-list.zwkum = l-untergrup.zwkum NO-ERROR.

    IF NOT AVAILABLE sub-list THEN 
    DO: 
        create sub-list. 
        sub-list.zwkum = l-untergrup.zwkum. 
        sub-list.bezeich = l-untergrup.bezeich. 
    END. 
    sub-list.amt = sub-list.amt + s-list.brutto. 
    sub-list.disc = sub-list.disc + s-list.disc-amt. 
    sub-list.disc2 = sub-list.disc2 + s-list.disc2-amt. 
    sub-list.vat = sub-list.vat + s-list.vat-amt. 
END.
