
DEFINE TEMP-TABLE t-bill-line   LIKE bill-line
    FIELD bl-recid  AS INTEGER
    FIELD artart    AS INTEGER
    FIELD tool-tip  AS CHAR
.


DEFINE INPUT PARAMETER case-type    AS INTEGER.
DEFINE INPUT PARAMETER pvILanguage  AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER rechNo       AS INTEGER.
DEFINE INPUT PARAMETER artNo        AS INTEGER.
DEFINE INPUT PARAMETER deptNo       AS INTEGER.
DEFINE INPUT PARAMETER anzahl       AS INTEGER.
DEFINE INPUT PARAMETER epreis       AS DECIMAL.
DEFINE INPUT PARAMETER betrag       AS DECIMAL.
DEFINE OUTPUT PARAMETER TABLE FOR t-bill-line.
                                               
DEF BUFFER rlbuff FOR res-line. 
DEF BUFFER bibuff FOR bill.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "fo-invoice". 

CASE case-type :
    WHEN 1 THEN
    DO:
        FOR EACH bill-line WHERE bill-line.artnr = artNo
            AND bill-line.departement = deptNo
            AND bill-line.rechnr = rechNo NO-LOCK: 
            CREATE t-bill-line.
            BUFFER-COPY bill-line TO t-bill-line.
            t-bill-line.bl-recid = RECID(bill-line).
        END.
    END.
    WHEN 2 THEN
    DO: 
        FIND FIRST bill-line WHERE bill-line.artnr = artNo
            AND bill-line.departement = deptNo
            AND bill-line.rechnr = rechNo
            AND bill-line.anzahl = - anzahl
            AND bill-line.epreis = epreis
            AND bill-line.betrag = - betrag NO-LOCK NO-ERROR.
        IF AVAILABLE bill-line THEN
        DO:
            CREATE t-bill-line.
            BUFFER-COPY bill-line TO t-bill-line.
            t-bill-line.bl-recid = RECID(bill-line).
        END.
    END.
    WHEN 3 THEN
    DO:
        FOR EACH bill-line WHERE bill-line.rechnr = rechNo NO-LOCK :
            CREATE t-bill-line.
            BUFFER-COPY bill-line TO t-bill-line.
            t-bill-line.bl-recid = RECID(bill-line).
        END.
    END.
    WHEN 4 THEN
    DO:
        FOR EACH bill-line WHERE bill-line.rechnr = rechNo 
            AND bill-line.artnr = artNo NO-LOCK:
            CREATE t-bill-line.
            BUFFER-COPY bill-line TO t-bill-line.
            t-bill-line.bl-recid = RECID(bill-line).
        END.
    END.
    WHEN 5 THEN
    DO:
        FIND FIRST bill-line WHERE RECID(bill-line) = anzahl
            AND bill-line.rechnr = rechNo NO-LOCK NO-ERROR. 
        IF AVAILABLE bill-line THEN
        DO:
            CREATE t-bill-line.
            BUFFER-COPY bill-line TO t-bill-line.
            t-bill-line.bl-recid = RECID(bill-line).
        END.
    END.
END CASE.

IF NOT AVAILABLE t-bill-line THEN RETURN.
FIND FIRST bill WHERE bill.rechnr = rechNo NO-LOCK.

FOR EACH t-bill-line:
  
  FIND FIRST artikel WHERE artikel.artnr = t-bill-line.artnr
    AND artikel.departement = t-bill-line.departement
    NO-LOCK NO-ERROR.
  IF AVAILABLE artikel THEN 
      ASSIGN t-bill-line.artart = artikel.artart.
  
  FIND FIRST bill-line WHERE RECID(bill-line) = t-bill-line.bl-recid
     NO-LOCK.
   IF bill-line.massnr NE 0 AND bill-line.billin-nr NE 0
      AND (bill-line.massnr NE bill.resnr
        OR bill-line.billin-nr NE bill.reslinnr) THEN
   DO:
     FIND FIRST bibuff WHERE bibuff.resnr = bill-line.massnr
         AND bibuff.reslinnr = bill-line.billin-nr NO-LOCK NO-ERROR.
     IF AVAILABLE bibuff THEN
     DO:
         FIND FIRST rlbuff WHERE rlbuff.resnr = bibuff.resnr
             AND rlbuff.reslinnr = bibuff.parent-nr NO-LOCK NO-ERROR.
         IF AVAILABLE rlbuff THEN ASSIGN t-bill-line.tool-tip =
             translateExtended ("RmNo",lvCAREA,"") + " "
             + rlbuff.zinr + " " + rlbuff.NAME + "  " + STRING(rlbuff.ankunft)
             + "-" + STRING(rlbuff.abreise) + " " 
             + translateExtended ("BillNo",lvCAREA,"") + " "
             + STRING(bibuff.rechnr).
         ELSE t-bill-line.tool-tip = translateExtended ("RmNo",lvCAREA,"") + " "
             + bibuff.zinr + " " + bibuff.NAME + " " 
             + translateExtended ("BillNo",lvCAREA,"") + " "
             + STRING(bibuff.rechnr).
     END.
     ELSE t-bill-line.tool-tip = "".
   END.
END.

