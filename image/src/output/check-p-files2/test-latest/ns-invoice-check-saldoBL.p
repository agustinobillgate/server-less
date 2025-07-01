DEFINE TEMP-TABLE t-bill-line       LIKE bill-line
    FIELD bl-recid  AS INTEGER
    FIELD artart    AS INTEGER
    FIELD tool-tip  AS CHAR
.

DEFINE TEMP-TABLE t-bill        LIKE bill
    FIELD bl-recid          AS INTEGER.

DEF BUFFER bibuff FOR bill.
DEF BUFFER rlbuff FOR res-line.

DEFINE INPUT  PARAMETER pvILanguage AS INTEGER NO-UNDO.
DEFINE INPUT  PARAMETER t-rechnr    AS INT.
DEFINE OUTPUT PARAMETER TABLE FOR t-bill.
DEFINE OUTPUT PARAMETER TABLE FOR t-bill-line.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "ns-invoice".

FIND FIRST bill WHERE bill.rechnr EQ t-rechnr NO-LOCK NO-ERROR.                 /* Rulita 281124 | Fixing serverless issue 235 */
IF AVAILABLE bill THEN
DO :
    CREATE t-bill.
    BUFFER-COPY bill TO t-bill.
    ASSIGN t-bill.bl-recid = RECID(bill).

    FOR EACH bill-line WHERE rechnr = t-rechnr NO-LOCK:
        CREATE t-bill-line.
        BUFFER-COPY bill-line TO t-bill-line.
        t-bill-line.bl-recid = RECID(bill-line).

        FIND FIRST artikel WHERE artikel.artnr = t-bill-line.artnr
            AND artikel.departement = t-bill-line.departement
            NO-LOCK NO-ERROR.
        IF AVAILABLE artikel THEN 
            ASSIGN t-bill-line.artart = artikel.artart.
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
END.
