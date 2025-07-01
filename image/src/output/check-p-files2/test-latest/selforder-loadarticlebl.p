
DEFINE TEMP-TABLE article-list
  FIELD art-department  AS INTEGER
  FIELD art-recid       AS INTEGER
  FIELD art-number      AS INTEGER
  FIELD art-name        AS CHARACTER
  FIELD art-group       AS INTEGER
  FIELD art-subgrp      AS INTEGER
  FIELD art-group-str   AS CHARACTER
  FIELD art-subgrp-str  AS CHARACTER
  FIELD art-desc        AS CHARACTER
  FIELD art-price       AS DECIMAL
  FIELD art-orig-price  AS DECIMAL
  FIELD art-image       AS CHARACTER
  FIELD art-active-flag AS LOGICAL
  FIELD art-sold-out    AS LOGICAL  
.

DEFINE TEMP-TABLE maingroup-list
    FIELD maingrp-no            AS INT
    FIELD maingrp-description   AS CHAR
    FIELD maingrp-image         AS CHAR
    .

DEFINE TEMP-TABLE subgroup-list
    FIELD subgrp-no          AS INT
    FIELD subgrp-description AS CHAR.

DEFINE INPUT PARAMETER outlet-no    AS INTEGER.
DEFINE OUTPUT PARAMETER mess-result AS CHARACTER.
DEFINE OUTPUT PARAMETER TABLE FOR article-list.
DEFINE OUTPUT PARAMETER TABLE FOR maingroup-list.
DEFINE OUTPUT PARAMETER TABLE FOR subgroup-list.
/*
DEFINE VARIABLE outlet-no AS INTEGER INIT 6.
DEFINE VARIABLE mess-result AS CHARACTER.
*/
DEFINE VARIABLE ct                  AS CHARACTER NO-UNDO.
DEFINE VARIABLE l-deci              AS INTEGER NO-UNDO INIT 2.
DEFINE VARIABLE serv-vat            AS LOGICAL NO-UNDO. 
DEFINE VARIABLE tax-vat             AS LOGICAL NO-UNDO.
                                    
DEFINE VARIABLE tax                 AS DECIMAL NO-UNDO. 
DEFINE VARIABLE serv                AS DECIMAL NO-UNDO.
DEFINE VARIABLE service             AS DECIMAL NO-UNDO.
DEFINE VARIABLE vat                 AS DECIMAL NO-UNDO INIT 0.
DEFINE VARIABLE vat2                AS DECIMAL NO-UNDO INIT 0.
DEFINE VARIABLE fact-scvat          AS DECIMAL NO-UNDO INIT 1.
DEFINE VARIABLE servtax-use-foart   AS LOGICAL.         
DEFINE VARIABLE service-foreign     AS DECIMAL NO-UNDO INIT 0.  
DEFINE VARIABLE serv-code           AS INTEGER. 
DEFINE VARIABLE vat-code            AS INTEGER. 

/*********************************************************************************************/
EMPTY TEMP-TABLE article-list.
EMPTY TEMP-TABLE maingroup-list.
EMPTY TEMP-TABLE subgroup-list.

FIND FIRST hoteldpt WHERE hoteldpt.num EQ outlet-no NO-LOCK NO-ERROR.
IF AVAILABLE hoteldpt THEN
DO:
    servtax-use-foart = hoteldpt.defult. /*FD July 14, 2022*/
END. 

FIND FIRST queasy WHERE queasy.KEY EQ 228 NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN
DO:
    FOR EACH queasy WHERE queasy.KEY EQ 228
        AND queasy.number2 EQ outlet-no NO-LOCK:
        CREATE maingroup-list.
        ASSIGN
            maingroup-list.maingrp-no          = queasy.number1
            maingroup-list.maingrp-description = queasy.char1
            maingroup-list.maingrp-image       = queasy.char2
            .
    END.
END.
ELSE
DO:
    mess-result = "MainGroup not configured yet!".
    RETURN.
END.

FIND FIRST queasy WHERE queasy.KEY EQ 229 NO-LOCK NO-ERROR.
IF NOT AVAILABLE queasy THEN
DO:
    mess-result = "There is no mapping for subgroup, please mapping it first!".
    RETURN.
END.

DEFINE BUFFER bqsy FOR queasy.

FOR EACH h-artikel WHERE h-artikel.departement EQ outlet-no 
    AND h-artikel.artart EQ 0 AND h-artikel.activeflag 
    AND h-artikel.epreis1 NE 0 NO-LOCK BY h-artikel.bezeich:
    FIND FIRST queasy WHERE queasy.KEY EQ 229 AND queasy.number1 EQ h-artikel.zwkum
        AND queasy.number2 EQ h-artikel.departement NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN
    DO:
        service = 0.
        vat     = 0.
        vat2    = 0.

        IF servtax-use-foart THEN
        DO:
            FIND FIRST artikel WHERE artikel.artnr EQ h-artikel.artnrfront
                AND artikel.departement EQ h-artikel.departement NO-LOCK NO-ERROR.
            IF AVAILABLE artikel THEN
            DO:
                ASSIGN
                    serv-code = artikel.service-code
                    vat-code = artikel.mwst-code
                .
            END.
        END.  
        ELSE
        DO:
            ASSIGN
                serv-code = h-artikel.service-code
                vat-code = h-artikel.mwst-code
            .
        END.

        FIND FIRST bqsy WHERE bqsy.KEY EQ 228 AND bqsy.number1 EQ queasy.number3
            AND bqsy.number2 EQ queasy.number2 NO-LOCK NO-ERROR.

        FIND FIRST htparam WHERE htparam.paramnr = 135 NO-LOCK. 
        IF NOT htparam.flogical AND h-artikel.artart = 0 
            AND /*h-artikel.service-code*/ serv-code NE 0 THEN 
        DO: 
            FIND FIRST htparam WHERE htparam.paramnr = /*h-artikel.service-code*/ serv-code NO-LOCK NO-ERROR. 
            IF AVAILABLE htparam AND htparam.fdecimal NE 0 THEN 
            DO:
                IF NUM-ENTRIES(htparam.fchar, CHR(2)) GE 2 THEN
                ASSIGN service = DECIMAL(ENTRY(2, htparam.fchar, CHR(2))) / 10000.
                ELSE service = htparam.fdecimal.
            END.
        END.
        
        RUN htplogic.p(479, OUTPUT serv-vat).
        RUN htplogic.p(483, OUTPUT tax-vat).
                         
        FIND FIRST htparam WHERE paramnr = 134 NO-LOCK. 
        IF NOT vhp.htparam.flogical AND h-artikel.artart = 0 
            AND /*h-artikel.mwst-code*/ vat-code NE 0 THEN 
        DO: 
            FIND FIRST htparam WHERE htparam.paramnr = /*h-artikel.mwst-code*/ vat-code NO-LOCK NO-ERROR. 
            IF AVAILABLE htparam AND htparam.fdecimal NE 0 THEN 
            DO: 
                IF NUM-ENTRIES(htparam.fchar, CHR(2)) GE 2 THEN 
                ASSIGN vat = DECIMAL(ENTRY(2, htparam.fchar, CHR(2))) / 10000.
                ELSE vat = htparam.fdecimal.
                
                IF serv-vat AND NOT tax-vat THEN vat = vat + vat * service / 100.
                ELSE IF serv-vat AND tax-vat THEN vat = vat + vat * (service + vat2) / 100.
                ELSE IF NOT serv-vat AND tax-vat THEN vat = vat + vat * vat2 / 100.
                ASSIGN 
                  ct     = REPLACE(STRING(vat), ".", ",")
                  l-deci = LENGTH(ENTRY(2, ct, ",")) NO-ERROR
                .
                
                IF l-deci LE 2 THEN vat = ROUND(vat, 2).
                ELSE IF l-deci = 3 THEN vat = ROUND(vat, 3).
                ELSE vat = ROUND(vat, 4).
            END. 
        END.

        IF h-artikel.artart = 0 THEN 
        DO:                
            IF serv-code NE 0 THEN service = service / 100.
            IF vat-code NE 0 THEN
            DO:
                ASSIGN
                    vat     = vat / 100
                    vat2    = vat2 / 100
                .   
            END.                        
            
            ASSIGN fact-scvat = 1 + service + vat + vat2.
            
            IF vat = 1 THEN 
            ASSIGN
            fact-scvat  = 1
            service     = 0
            vat2        = 0
            .   
            ELSE IF vat2 = 1 THEN 
            ASSIGN
            fact-scvat = 1
            service    = 0
            vat        = 0
            .   
            ELSE IF service = 1 THEN 
            ASSIGN
            fact-scvat = 1
            vat        = 0
            vat2       = 0
            .   
        END.             
        
        CREATE article-list.
        ASSIGN
        article-list.art-department = h-artikel.departement
        article-list.art-recid      = RECID(h-artikel)
        article-list.art-number     = h-artikel.artnr
        article-list.art-name       = h-artikel.bezeich
        
        article-list.art-subgrp     = h-artikel.zwkum
        
        article-list.art-subgrp-str = queasy.char1
        article-list.art-price      = h-artikel.epreis1 * fact-scvat 
        article-list.art-price      = ROUND(article-list.art-price,0)
        article-list.art-orig-price = h-artikel.epreis1
        .
          
        IF AVAILABLE bqsy THEN
        DO:
            article-list.art-group      = bqsy.number1.
            article-list.art-group-str  = bqsy.char1.
        END.
            
        /*Get Description and Image From Queasy Key 222*/
        FIND FIRST queasy WHERE queasy.key EQ 222 AND queasy.number1 EQ 2
            AND queasy.number2 EQ h-artikel.artnr
            AND queasy.number3 EQ h-artikel.departement NO-LOCK NO-ERROR.
        IF AVAILABLE queasy THEN
        DO:
            ASSIGN
            article-list.art-image       = queasy.char2
            article-list.art-desc        = queasy.char3
            article-list.art-active-flag = queasy.logi1
            article-list.art-sold-out    = queasy.logi2  
            .   
        END.
    END.
END.

FOR EACH article-list WHERE article-list.art-active-flag EQ NO:
    DELETE article-list.
END.
mess-result = "Success load data ya".
