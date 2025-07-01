/*M 310512 -> add curr */
DEFINE TEMP-TABLE quote-list 
    FIELD artnr         LIKE l-quote.artnr         
    FIELD lief-nr       LIKE l-quote.lief-nr        
    FIELD supName       AS CHAR                     
    FIELD artName       LIKE l-artikel.bezeich      
    FIELD devUnit       LIKE l-artikel.traubensorte  
    FIELD content       LIKE l-artikel.lief-einheit 
    FIELD unitprice     LIKE l-quote.unitprice      
    FIELD curr          AS CHAR      
    FIELD from-date     LIKE l-quote.from-date      
    FIELD to-Date       LIKE l-quote.to-date        
    FIELD remark        LIKE l-quote.remark         
    FIELD filname       LIKE l-quote.filname        
    FIELD activeFlag    LIKE l-quote.activeflag     
    FIELD docu-nr       LIKE l-quote.docu-nr        
    FIELD minQty        AS DEC      INIT 0          
    FIELD delivDay      AS INT      INIT 0          
    FIELD disc          AS DEC      INIT 0          
    FIELD avl           AS LOGICAL  INIT YES
    FIELD quote-recid   AS INTEGER
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

    MESSAGE l-quote.docu-nr l-artikel.bezeich l-quote.unitprice
        VIEW-AS ALERT-BOX INFO BUTTONS OK.
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
        quote-list.quote-recid = RECID(l-quote) /*FDL Ticket EA3FF3*/
    .
END.
