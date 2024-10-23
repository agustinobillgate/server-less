/*M 310512 -> add curr */
DEFINE TEMP-TABLE quote-list 
    FIELD artnr         LIKE l-quote.artnr          FORMAT "9999999"
    FIELD lief-nr       LIKE l-quote.lief-nr        FORMAT ">,>>>,>>9"
    FIELD supName       AS CHAR                     FORMAT "x(20)"
    FIELD artName       LIKE l-artikel.bezeich      FORMAT "x(20)"
    FIELD devUnit       LIKE l-artikel.traubensort  FORMAT "x(8)"
    FIELD content       LIKE l-artikel.lief-einheit FORMAT ">>9.99"
    FIELD unitprice     LIKE l-quote.unitprice      FORMAT ">>>,>>>,>>9.99"
    FIELD curr          LIKE l-quote.reserve-char[1]FORMAT "x(4)"     
    FIELD from-date     LIKE l-quote.from-date      FORMAT "99/99/99"     
    FIELD to-Date       LIKE l-quote.to-date        FORMAT "99/99/99"
    FIELD remark        LIKE l-quote.remark         FORMAT "x(20)"
    FIELD filname       LIKE l-quote.filname        FORMAT "x(20)"
    FIELD activeFlag    LIKE l-quote.activeflag     INIT YES
    FIELD docu-nr       LIKE l-quote.docu-nr        FORMAT "x(12)"
    FIELD minQty        AS DEC      INIT 0          FORMAT ">>9.99"
    FIELD delivDay      AS INT      INIT 0          FORMAT ">>9"
    FIELD disc          AS DEC      INIT 0          FORMAT ">>9.99"
    FIELD avl           AS LOGICAL  INIT YES
    .

DEFINE INPUT PARAMETER artNo        AS INT  NO-UNDO.
DEFINE INPUT PARAMETER supNo        AS INT  NO-UNDO.
DEFINE INPUT PARAMETER docuNo       AS CHAR NO-UNDO.
DEFINE OUTPUT PARAMETER prog-path   AS CHAR NO-UNDO INIT "".
DEFINE OUTPUT PARAMETER prog-name   AS CHAR NO-UNDO INIT "".
DEFINE OUTPUT PARAMETER bill-date   AS DATE NO-UNDO INIT ?.
DEFINE OUTPUT PARAMETER local-curr  AS CHAR NO-UNDO INIT "".
DEFINE OUTPUT PARAMETER TABLE FOR quote-list.


FIND FIRST htparam WHERE htparam.paramnr = 110 NO-LOCK.
IF AVAILABLE htparam THEN bill-date = htparam.fdate.
/*M program to open MS-Word */
FIND FIRST htparam WHERE htparam.paramnr = 400 NO-LOCK. 
IF htparam.fchar NE "" THEN prog-path = htparam.fchar. 
ELSE prog-path = "\""program files""\""microsoft office""\office\". 
FIND FIRST htparam WHERE htparam.paramnr = 405 NO-LOCK. 
IF htparam.fchar NE "" THEN prog-name = htparam.fchar. 
ELSE prog-name = "winword.exe". 

FIND FIRST htparam WHERE htparam.paramnr = 152 NO-LOCK. 
FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK NO-ERROR. 
IF NOT AVAILABLE waehrung THEN 
FIND FIRST waehrung NO-LOCK NO-ERROR.
IF AVAILABLE waehrung THEN local-curr = waehrung.wabkurz.

IF artNo NE 0 AND supNo EQ 0 AND docuNo EQ "" THEN /*based on artNo*/
FOR EACH l-quote WHERE l-quote.reserve-int[5] LE 1
    AND l-quote.artnr = artNo NO-LOCK,
    FIRST l-lieferant WHERE l-lieferant.lief-nr = l-quote.lief-nr NO-LOCK,
    FIRST l-artikel WHERE l-artikel.artnr = l-quote.artnr NO-LOCK :
    RUN cr-lquote.
END.
ELSE IF supNo NE 0 AND artNo EQ 0 AND docuNo EQ "" THEN /*based on supNo*/
FOR EACH l-quote WHERE l-quote.reserve-int[5] LE 1
    AND l-quote.lief-nr = supNo NO-LOCK,
    FIRST l-lieferant WHERE l-lieferant.lief-nr = l-quote.lief-nr NO-LOCK,
    FIRST l-artikel WHERE l-artikel.artnr = l-quote.artnr NO-LOCK :
    RUN cr-lquote.
END.
ELSE IF docuNo NE "" AND artNo EQ 0 AND supNo EQ 0 THEN /*based on docuNo*/
FOR EACH l-quote WHERE l-quote.reserve-int[5] LE 1
    AND l-quote.docu-nr = docuNo NO-LOCK,
    FIRST l-lieferant WHERE l-lieferant.lief-nr = l-quote.lief-nr NO-LOCK,
    FIRST l-artikel WHERE l-artikel.artnr = l-quote.artnr NO-LOCK :
    RUN cr-lquote.
END.
ELSE IF artNo NE 0 AND supNo NE 0 AND docuNo EQ "" THEN /*based on artNo & supNo*/
FOR EACH l-quote WHERE l-quote.reserve-int[5] LE 1
    AND l-quote.lief-nr = supNo 
    AND l-quote.artnr = artNo NO-LOCK,
    FIRST l-lieferant WHERE l-lieferant.lief-nr = l-quote.lief-nr NO-LOCK,
    FIRST l-artikel WHERE l-artikel.artnr = l-quote.artnr NO-LOCK :
    RUN cr-lquote.
END.
ELSE IF artNo NE 0 AND supNo EQ 0 AND docuNo NE "" THEN /*based on artNo & docuNo*/
FOR EACH l-quote WHERE l-quote.reserve-int[5] LE 1
    AND l-quote.artnr = artNo 
    AND l-quote.docu-nr EQ docuNo NO-LOCK,
    FIRST l-lieferant WHERE l-lieferant.lief-nr = l-quote.lief-nr NO-LOCK,
    FIRST l-artikel WHERE l-artikel.artnr = l-quote.artnr NO-LOCK :
    RUN cr-lquote.
END.
ELSE IF artNo EQ 0 AND supNo NE 0 AND docuNo NE "" THEN /*based on supNo & docuNo*/
FOR EACH l-quote WHERE l-quote.reserve-int[5] LE 1
    AND l-quote.lief-nr = supNo 
    AND l-quote.docu-nr = docuNo NO-LOCK,
    FIRST l-lieferant WHERE l-lieferant.lief-nr = l-quote.lief-nr NO-LOCK,
    FIRST l-artikel WHERE l-artikel.artnr = l-quote.artnr NO-LOCK :
    RUN cr-lquote.
END.

/************** PROCEDURES *****************/
PROCEDURE cr-lquote:
    CREATE quote-list.
        BUFFER-COPY l-quote TO quote-list.
    ASSIGN 
        quote-list.supName   = TRIM(l-lieferant.anredefirma + " " + firma)
        quote-list.artName   = l-artikel.bezeich
        quote-list.devUnit   = l-artikel.traubensort
        quote-list.content   = l-artikel.lief-einheit
        quote-list.curr      = l-quote.reserve-char[1]
        quote-list.minqty    = l-quote.reserve-deci[1]
        quote-list.disc      = l-quote.reserve-deci[2]
        quote-list.avl       = NOT l-quote.reserve-logic[1]
        quote-list.delivday  = l-quote.reserve-int[1]
    .
END.
