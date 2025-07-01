DEFINE TEMP-TABLE apage-list
    FIELD docu-nr AS CHARACTER FORMAT "x(16)" 
    FIELD lschein AS CHARACTER FORMAT "x(14)" 
    FIELD rgdatum AS CHARACTER FORMAT "x(8)"
    FIELD STR AS CHARACTER.

DEFINE INPUT  PARAMETER pvILanguage  AS INTEGER              NO-UNDO.
DEFINE INPUT  PARAMETER to-date      AS DATE.
DEFINE INPUT  PARAMETER from-name    AS CHARACTER.
DEFINE INPUT  PARAMETER to-name      AS CHARACTER.           
DEFINE INPUT  PARAMETER detailed     AS LOGICAL.
DEFINE INPUT  PARAMETER mi-bill      AS LOGICAL.
DEFINE INPUT  PARAMETER segm         AS INTEGER.
DEFINE INPUT  PARAMETER curr-disp    AS INTEGER.
DEFINE OUTPUT PARAMETER TABLE        FOR apage-list.

DEFINE VARIABLE billdate     AS DATE    NO-UNDO. 
DEFINE VARIABLE curr-lief-nr AS INTEGER NO-UNDO. 
DEFINE VARIABLE curr-art     AS INTEGER NO-UNDO. 
DEFINE VARIABLE counter      AS INTEGER NO-UNDO FORMAT ">>>9". 
DEFINE VARIABLE i            AS INTEGER NO-UNDO. 
DEFINE VARIABLE curr-name    AS CHARACTER NO-UNDO FORMAT "x(24)". 
DEFINE VARIABLE firma        AS CHARACTER NO-UNDO FORMAT "x(34)". 
DEFINE VARIABLE curr-po      AS CHARACTER NO-UNDO.
DEFINE VARIABLE curr-lschein AS CHARACTER NO-UNDO.
DEFINE VARIABLE p-bal        AS DECIMAL NO-UNDO FORMAT "->>>,>>>,>>9". 
DEFINE VARIABLE debit        AS DECIMAL NO-UNDO FORMAT "->>>,>>>,>>9". 
DEFINE VARIABLE credit       AS DECIMAL NO-UNDO FORMAT "->>>,>>>,>>9". 
DEFINE VARIABLE debt0        AS DECIMAL NO-UNDO FORMAT "->>>,>>>,>>9". 
DEFINE VARIABLE debt1        AS DECIMAL NO-UNDO FORMAT "->>>,>>>,>>9". 
DEFINE VARIABLE debt2        AS DECIMAL NO-UNDO FORMAT "->>>,>>>,>>9". 
DEFINE VARIABLE debt3        AS DECIMAL NO-UNDO FORMAT "->>>,>>>,>>9". 

DEFINE VARIABLE tot-debt     AS DECIMAL NO-UNDO FORMAT "->,>>>,>>>,>>9.99" 
    LABEL "Total Debt" BGCOLOR 2  FGCOLOR 15. 

DEFINE VARIABLE t-comm       AS DECIMAL NO-UNDO FORMAT "->,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE t-adjust     AS DECIMAL NO-UNDO FORMAT "->,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE t-saldo      AS DECIMAL NO-UNDO FORMAT "->>,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE t-prev       AS DECIMAL NO-UNDO FORMAT "->>,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE t-debit      AS DECIMAL NO-UNDO FORMAT "->,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE t-credit     AS DECIMAL NO-UNDO FORMAT "->,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE t-debt0      AS DECIMAL NO-UNDO FORMAT "->,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE t-debt1      AS DECIMAL NO-UNDO FORMAT "->,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE t-debt2      AS DECIMAL NO-UNDO FORMAT "->,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE t-debt3      AS DECIMAL NO-UNDO FORMAT "->,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE tmp-saldo    AS DECIMAL NO-UNDO FORMAT "->>>>>>>>>>9" INITIAL 0. 
DEFINE VARIABLE curr-rgdatum AS CHARACTER NO-UNDO. 

DEFINE VARIABLE from-date    AS DATE    NO-UNDO.  
DEFINE VARIABLE guest-name   AS CHARACTER NO-UNDO FORMAT "x(27)". 
DEFINE VARIABLE curr-bezeich AS CHARACTER NO-UNDO FORMAT "x(27)". 
DEFINE VARIABLE outlist      AS CHARACTER NO-UNDO FORMAT "x(142)". 

DEFINE VARIABLE do-it        AS LOGICAL NO-UNDO.
DEFINE VARIABLE price-decimal AS INTEGER NO-UNDO.

DEFINE BUFFER debtrec   FOR l-kredit. 
DEFINE BUFFER debt      FOR l-kredit. 
 
DEFINE VARIABLE day1 AS INTEGER NO-UNDO INITIAL 30. 
DEFINE VARIABLE day2 AS INTEGER NO-UNDO INITIAL 30. 
DEFINE VARIABLE day3 AS INTEGER NO-UNDO INITIAL 30. 
DEFINE VARIABLE curr-saldo AS DECIMAL NO-UNDO.

DEFINE WORKFILE age-list 
    FIELD artnr           AS INTEGER 
    FIELD rechnr          AS CHARACTER 
    FIELD lschein         AS CHARACTER 
    FIELD counter         AS INTEGER 
    FIELD lief-nr         AS INTEGER 
    FIELD rgdatum         AS DATE 
    FIELD firma           AS CHARACTER FORMAT "x(34)" 
    FIELD p-bal           AS DECIMAL FORMAT "->>>,>>>,>>9" INITIAL 0 
    FIELD debit           AS DECIMAL FORMAT "->>>,>>>,>>9" INITIAL 0 
    FIELD credit          AS DECIMAL FORMAT "->>>,>>>,>>9" INITIAL 0 
    FIELD saldo           AS DECIMAL FORMAT "->>>,>>>,>>9" INITIAL 0 
    FIELD debt0           AS DECIMAL FORMAT "->>>,>>>,>>9" INITIAL 0 
    FIELD debt1           AS DECIMAL FORMAT "->>>,>>>,>>9" INITIAL 0 
    FIELD debt2           AS DECIMAL FORMAT "->>>,>>>,>>9" INITIAL 0 
    FIELD debt3           AS DECIMAL FORMAT "->>>,>>>,>>9" INITIAL 0 
    FIELD tot-debt        AS DECIMAL FORMAT "->>>,>>>,>>9" INITIAL 0.              

{supertransBL.i} 
DEFINE VARIABLE lvCAREA AS CHARACTER INITIAL "ap-age1". 

/*****************************************************************************/
ASSIGN  billdate = ?
        curr-lief-nr = 0
        curr-art = 0
        counter = 0
        i = 0
        curr-name = ""
        firma = ""
        curr-po = ""
        curr-lschein = ""
        p-bal = 0
        debit = 0
        credit = 0
        debt0 = 0
        debt1 = 0
        debt2 = 0
        debt3 = 0
        tot-debt = 0
        t-comm = 0
        t-adjust = 0
        t-saldo = 0
        t-prev = 0
        t-debit = 0
        t-credit = 0
        t-debt0 = 0
        t-debt1 = 0
        t-debt2 = 0
        t-debt3 = 0
        tmp-saldo = 0
        curr-rgdatum = ?.

FIND FIRST htparam WHERE paramnr = 330 NO-LOCK. 
IF finteger NE 0 THEN day1 = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
FIND FIRST htparam WHERE paramnr = 331 NO-LOCK. 
IF finteger NE 0 THEN day2 = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
FIND FIRST htparam WHERE paramnr = 332 NO-LOCK. 
IF finteger NE 0 THEN day3 = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
day2 = day2 + day1. 
day3 = day3 + day2. 

from-date = DATE(MONTH(to-date), 1, YEAR(to-date)). 

RUN htpint.p (491, OUTPUT price-decimal).

IF curr-disp = 1 THEN RUN age-list. /*ALL*/
ELSE IF curr-disp = 2 THEN RUN age-list1. /*Manual AP*/
ELSE IF curr-disp = 3 THEN RUN age-list2. /*Receiving AP*/
ELSE IF curr-disp = 4 THEN RUN age-list3. /*Receiving Invoice*/ /*Gerald*/
 

PROCEDURE age-list:
    /*M
    curr-bezeich = translateExtended ("Unpaid and partial paid A/P",lvCAREA,""). 
    DISP curr-bezeich WITH FRAME frame2. 
    */
    
    /* NOT paid OR partial paid */ 
    /*MTIF case-type = 1 THEN*/
    FOR EACH l-kredit WHERE l-kredit.rgdatum LE to-date AND 
        l-kredit.opart LE 1 AND l-kredit.counter GE 0 NO-LOCK USE-INDEX counter_ix, 
        FIRST l-lieferant WHERE l-lieferant.lief-nr = l-kredit.lief-nr 
        AND l-lieferant.firma GE from-name AND l-lieferant.firma LE to-name 
        BY l-lieferant.firma BY l-kredit.zahlkonto: 
        
        do-it = YES.
        IF segm NE 0 AND l-lieferant.segment1 NE segm THEN do-it = NO.
    
        IF do-it THEN
        DO:
            IF l-kredit.counter > 0 THEN FIND FIRST age-list WHERE 
                age-list.counter = l-kredit.counter NO-ERROR. 
            IF (l-kredit.counter = 0) OR (NOT AVAILABLE age-list) THEN 
            DO: 
                /* CREATE aging record FOR a specific guest, based ON A/P-debit record */ 
                CREATE age-list. 
                age-list.rgdatum = l-kredit.rgdatum. 
                age-list.counter = l-kredit.counter. 
                age-list.lief-nr = l-kredit.lief-nr. 
                age-list.tot-debt = 0. 
                age-list.firma = l-lieferant.firma. 
                age-list.rechnr = l-kredit.name.    /* po number */ 
    
                IF LENGTH(l-kredit.lscheinnr) LE 10 THEN 
                    age-list.lschein = l-kredit.lscheinnr. 
                ELSE 
                    age-list.lschein = SUBSTR(l-kredit.lscheinnr, 11, LENGTH(l-kredit.lscheinnr) - 10). 
    
                /*M
                guest-name = l-lieferant.firma. 
                DISP guest-name WITH FRAME frame2. 
                */
            END. 
            IF l-kredit.zahlkonto = 0 THEN 
                age-list.tot-debt = age-list.tot-debt + l-kredit.netto. 
            ELSE age-list.tot-debt = age-list.tot-debt + l-kredit.saldo. 
    
            /* previous balance  */ 
            IF l-kredit.rgdatum LT from-date AND l-kredit.zahlkonto = 0 THEN 
                age-list.p-bal = age-list.p-bal + /* l-kredit.saldo */ l-kredit.netto. 
            
            /* debit transaction */ 
            IF l-kredit.rgdatum GE from-date AND l-kredit.zahlkonto = 0 THEN 
                age-list.debit = age-list.debit + l-kredit.netto. 
    
            /* credit transaction */ 
            IF l-kredit.rgdatum LT from-date AND l-kredit.zahlkonto NE 0 THEN 
                age-list.p-bal = age-list.p-bal + l-kredit.saldo. 
            ELSE 
            DO: 
                IF l-kredit.rgdatum GE from-date AND l-kredit.zahlkonto NE 0 THEN 
                    age-list.credit = age-list.credit - l-kredit.saldo. 
            END.
        END.
    END. 
    /*MTELSE
    DO:*/
        counter = 0. 
        FOR EACH l-kredit WHERE l-kredit.lief-nr GT 0 AND l-kredit.rgdatum LE to-date 
            AND l-kredit.opart EQ 2 AND l-kredit.zahlkonto EQ 0 NO-LOCK USE-INDEX liefnr_ix, 
            FIRST l-lieferant WHERE l-lieferant.lief-nr = l-kredit.lief-nr 
            AND l-lieferant.firma GE from-name AND l-lieferant.firma LE to-name NO-LOCK 
            BY l-kredit.counter: 
    
            do-it = YES.
            IF segm NE 0 AND l-lieferant.segment1 NE segm THEN do-it = NO.
    
            IF do-it THEN
            DO:
                /* CREATE aging record FOR a specific guest */ 
                CREATE age-list. 
                ASSIGN  age-list.rgdatum  = l-kredit.rgdatum
                        age-list.counter  = l-kredit.counter 
                        age-list.lief-nr  = l-kredit.lief-nr 
                        age-list.tot-debt = l-kredit.netto 
                        age-list.firma    = l-lieferant.firma
                        age-list.rechnr   = l-kredit.NAME    /* po number */ 
                        guest-name        = l-lieferant.firma.
    
                IF LENGTH(l-kredit.lscheinnr) LE 10 THEN 
                    age-list.lschein = l-kredit.lscheinnr. 
                ELSE age-list.lschein = SUBSTR(l-kredit.lscheinnr, 11, 
                                               LENGTH(l-kredit.lscheinnr) - 10). 
    
                /*M
                DISP guest-name WITH FRAME frame2. 
                */
                IF l-kredit.rgdatum LT from-date THEN 
                    age-list.p-bal = age-list.p-bal + l-kredit.netto. 
                ELSE IF l-kredit.rgdatum GE from-date THEN 
                    age-list.debit = age-list.debit + l-kredit.netto. 
    
                FOR EACH debtrec WHERE debtrec.counter = l-kredit.counter 
                    AND debtrec.opart = 2 AND debtrec.zahlkonto GT 0 
                    AND debtrec.rgdatum LE to-date NO-LOCK: 
    
                    age-list.tot-debt = age-list.tot-debt + debtrec.saldo. 
                    IF debtrec.rgdatum LT from-date THEN 
                        age-list.p-bal = age-list.p-bal + debtrec.saldo. 
                    ELSE IF debtrec.rgdatum GE from-date THEN 
                        age-list.credit = age-list.credit - debtrec.saldo. 
                END.
            END.
        END. 
    /*MTEND.*/
    /*M
    curr-bezeich = "Full paid A/P records". 
    DISP curr-bezeich WITH FRAME frame2. 
    */
     
    /*  within period's full paid transaction */ 
     
    counter = 0. 
    curr-lief-nr = 0. 
    curr-name = "".
END.


PROCEDURE age-list1:
    /*M
    curr-bezeich = translateExtended ("Unpaid and partial paid A/P",lvCAREA,""). 
    DISP curr-bezeich WITH FRAME frame2. 
    */
    
    /* NOT paid OR partial paid */ 
    /*MTIF case-type = 1 THEN*/
    FOR EACH l-kredit WHERE l-kredit.rgdatum LE to-date AND 
        l-kredit.opart LE 1 AND l-kredit.counter GE 0 
        AND l-kredit.steuercode = 1 NO-LOCK USE-INDEX counter_ix, 
        FIRST l-lieferant WHERE l-lieferant.lief-nr = l-kredit.lief-nr 
        AND l-lieferant.firma GE from-name AND l-lieferant.firma LE to-name 
        BY l-lieferant.firma BY l-kredit.zahlkonto: 
        
        do-it = YES.
        IF segm NE 0 AND l-lieferant.segment1 NE segm THEN do-it = NO.
    
        IF do-it THEN
        DO:
            IF l-kredit.counter > 0 THEN FIND FIRST age-list WHERE 
                age-list.counter = l-kredit.counter NO-ERROR. 
            IF (l-kredit.counter = 0) OR (NOT AVAILABLE age-list) THEN 
            DO: 
                /* CREATE aging record FOR a specific guest, based ON A/P-debit record */ 
                CREATE age-list. 
                age-list.rgdatum = l-kredit.rgdatum. 
                age-list.counter = l-kredit.counter. 
                age-list.lief-nr = l-kredit.lief-nr. 
                age-list.tot-debt = 0. 
                age-list.firma = l-lieferant.firma. 
                age-list.rechnr = l-kredit.name.    /* po number */ 
    
                IF LENGTH(l-kredit.lscheinnr) LE 10 THEN 
                    age-list.lschein = l-kredit.lscheinnr. 
                ELSE 
                    age-list.lschein = SUBSTR(l-kredit.lscheinnr, 11, LENGTH(l-kredit.lscheinnr) - 10). 
    
                /*M
                guest-name = l-lieferant.firma. 
                DISP guest-name WITH FRAME frame2. 
                */
            END. 
            IF l-kredit.zahlkonto = 0 THEN 
                age-list.tot-debt = age-list.tot-debt + l-kredit.netto. 
            ELSE age-list.tot-debt = age-list.tot-debt + l-kredit.saldo. 
    
            /* previous balance  */ 
            IF l-kredit.rgdatum LT from-date AND l-kredit.zahlkonto = 0 THEN 
                age-list.p-bal = age-list.p-bal + /* l-kredit.saldo */ l-kredit.netto. 
            
            /* debit transaction */ 
            IF l-kredit.rgdatum GE from-date AND l-kredit.zahlkonto = 0 THEN 
                age-list.debit = age-list.debit + l-kredit.netto. 
    
            /* credit transaction */ 
            IF l-kredit.rgdatum LT from-date AND l-kredit.zahlkonto NE 0 THEN 
                age-list.p-bal = age-list.p-bal + l-kredit.saldo. 
            ELSE 
            DO: 
                IF l-kredit.rgdatum GE from-date AND l-kredit.zahlkonto NE 0 THEN 
                    age-list.credit = age-list.credit - l-kredit.saldo. 
            END.
        END.
    END. 
    /*MTELSE
    DO:*/
        counter = 0. 
        FOR EACH l-kredit WHERE l-kredit.lief-nr GT 0 AND l-kredit.rgdatum LE to-date 
            AND l-kredit.opart EQ 2 AND l-kredit.zahlkonto EQ 0 
            AND l-kredit.steuercode = 1 NO-LOCK USE-INDEX liefnr_ix, 
            FIRST l-lieferant WHERE l-lieferant.lief-nr = l-kredit.lief-nr 
            AND l-lieferant.firma GE from-name AND l-lieferant.firma LE to-name NO-LOCK 
            BY l-kredit.counter: 
    
            do-it = YES.
            IF segm NE 0 AND l-lieferant.segment1 NE segm THEN do-it = NO.
    
            IF do-it THEN
            DO:
                /* CREATE aging record FOR a specific guest */ 
                CREATE age-list. 
                ASSIGN  age-list.rgdatum  = l-kredit.rgdatum
                        age-list.counter  = l-kredit.counter 
                        age-list.lief-nr  = l-kredit.lief-nr 
                        age-list.tot-debt = l-kredit.netto 
                        age-list.firma    = l-lieferant.firma
                        age-list.rechnr   = l-kredit.NAME    /* po number */ 
                        guest-name        = l-lieferant.firma.
    
                IF LENGTH(l-kredit.lscheinnr) LE 10 THEN 
                    age-list.lschein = l-kredit.lscheinnr. 
                ELSE age-list.lschein = SUBSTR(l-kredit.lscheinnr, 11, 
                                               LENGTH(l-kredit.lscheinnr) - 10). 
    
                /*M
                DISP guest-name WITH FRAME frame2. 
                */
                IF l-kredit.rgdatum LT from-date THEN 
                    age-list.p-bal = age-list.p-bal + l-kredit.netto. 
                ELSE IF l-kredit.rgdatum GE from-date THEN 
                    age-list.debit = age-list.debit + l-kredit.netto. 
    
                FOR EACH debtrec WHERE debtrec.counter = l-kredit.counter 
                    AND debtrec.opart = 2 AND debtrec.zahlkonto GT 0 
                    AND debtrec.rgdatum LE to-date NO-LOCK: 
    
                    age-list.tot-debt = age-list.tot-debt + debtrec.saldo. 
                    IF debtrec.rgdatum LT from-date THEN 
                        age-list.p-bal = age-list.p-bal + debtrec.saldo. 
                    ELSE IF debtrec.rgdatum GE from-date THEN 
                        age-list.credit = age-list.credit - debtrec.saldo. 
                END.
            END.
        END. 
    /*MTEND.*/
    /*M
    curr-bezeich = "Full paid A/P records". 
    DISP curr-bezeich WITH FRAME frame2. 
    */
     
    /*  within period's full paid transaction */ 
     
    counter = 0. 
    curr-lief-nr = 0. 
    curr-name = "".
END.

PROCEDURE age-list2:
    /*M
    curr-bezeich = translateExtended ("Unpaid and partial paid A/P",lvCAREA,""). 
    DISP curr-bezeich WITH FRAME frame2. 
    */
    
    /* NOT paid OR partial paid */ 
    /*MTIF case-type = 1 THEN*/
    FOR EACH l-kredit WHERE l-kredit.rgdatum LE to-date AND 
        l-kredit.opart LE 1 AND l-kredit.counter GE 0 
        AND l-kredit.steuercode = 0 NO-LOCK USE-INDEX counter_ix, 
        FIRST l-lieferant WHERE l-lieferant.lief-nr = l-kredit.lief-nr 
        AND l-lieferant.firma GE from-name AND l-lieferant.firma LE to-name 
        BY l-lieferant.firma BY l-kredit.zahlkonto: 
        
        do-it = YES.
        IF segm NE 0 AND l-lieferant.segment1 NE segm THEN do-it = NO.
    
        IF do-it THEN
        DO:
            IF l-kredit.counter > 0 THEN FIND FIRST age-list WHERE 
                age-list.counter = l-kredit.counter NO-ERROR. 
            IF (l-kredit.counter = 0) OR (NOT AVAILABLE age-list) THEN 
            DO: 
                /* CREATE aging record FOR a specific guest, based ON A/P-debit record */ 
                CREATE age-list. 
                age-list.rgdatum = l-kredit.rgdatum. 
                age-list.counter = l-kredit.counter. 
                age-list.lief-nr = l-kredit.lief-nr. 
                age-list.tot-debt = 0. 
                age-list.firma = l-lieferant.firma. 
                age-list.rechnr = l-kredit.name.    /* po number */ 
    
                IF LENGTH(l-kredit.lscheinnr) LE 10 THEN 
                    age-list.lschein = l-kredit.lscheinnr. 
                ELSE 
                    age-list.lschein = SUBSTR(l-kredit.lscheinnr, 11, LENGTH(l-kredit.lscheinnr) - 10). 
    
                /*M
                guest-name = l-lieferant.firma. 
                DISP guest-name WITH FRAME frame2. 
                */
            END. 
            IF l-kredit.zahlkonto = 0 THEN 
                age-list.tot-debt = age-list.tot-debt + l-kredit.netto. 
            ELSE age-list.tot-debt = age-list.tot-debt + l-kredit.saldo. 
    
            /* previous balance  */ 
            IF l-kredit.rgdatum LT from-date AND l-kredit.zahlkonto = 0 THEN 
                age-list.p-bal = age-list.p-bal + /* l-kredit.saldo */ l-kredit.netto. 
            
            /* debit transaction */ 
            IF l-kredit.rgdatum GE from-date AND l-kredit.zahlkonto = 0 THEN 
                age-list.debit = age-list.debit + l-kredit.netto. 
    
            /* credit transaction */ 
            IF l-kredit.rgdatum LT from-date AND l-kredit.zahlkonto NE 0 THEN 
                age-list.p-bal = age-list.p-bal + l-kredit.saldo. 
            ELSE 
            DO: 
                IF l-kredit.rgdatum GE from-date AND l-kredit.zahlkonto NE 0 THEN 
                    age-list.credit = age-list.credit - l-kredit.saldo. 
            END.
        END.
    END. 
    /*MTELSE
    DO:*/
        counter = 0. 
        FOR EACH l-kredit WHERE l-kredit.lief-nr GT 0 AND l-kredit.rgdatum LE to-date 
            AND l-kredit.opart EQ 2 AND l-kredit.zahlkonto EQ 0 
            AND l-kredit.steuercode = 0 NO-LOCK USE-INDEX liefnr_ix, 
            FIRST l-lieferant WHERE l-lieferant.lief-nr = l-kredit.lief-nr 
            AND l-lieferant.firma GE from-name AND l-lieferant.firma LE to-name NO-LOCK 
            BY l-kredit.counter: 
    
            do-it = YES.
            IF segm NE 0 AND l-lieferant.segment1 NE segm THEN do-it = NO.
    
            IF do-it THEN
            DO:
                /* CREATE aging record FOR a specific guest */ 
                CREATE age-list. 
                ASSIGN  age-list.rgdatum  = l-kredit.rgdatum
                        age-list.counter  = l-kredit.counter 
                        age-list.lief-nr  = l-kredit.lief-nr 
                        age-list.tot-debt = l-kredit.netto 
                        age-list.firma    = l-lieferant.firma
                        age-list.rechnr   = l-kredit.NAME    /* po number */ 
                        guest-name        = l-lieferant.firma.
    
                IF LENGTH(l-kredit.lscheinnr) LE 10 THEN 
                    age-list.lschein = l-kredit.lscheinnr. 
                ELSE age-list.lschein = SUBSTR(l-kredit.lscheinnr, 11, 
                                               LENGTH(l-kredit.lscheinnr) - 10). 
    
                /*M
                DISP guest-name WITH FRAME frame2. 
                */
                IF l-kredit.rgdatum LT from-date THEN 
                    age-list.p-bal = age-list.p-bal + l-kredit.netto. 
                ELSE IF l-kredit.rgdatum GE from-date THEN 
                    age-list.debit = age-list.debit + l-kredit.netto. 
    
                FOR EACH debtrec WHERE debtrec.counter = l-kredit.counter 
                    AND debtrec.opart = 2 AND debtrec.zahlkonto GT 0 
                    AND debtrec.rgdatum LE to-date NO-LOCK: 
    
                    age-list.tot-debt = age-list.tot-debt + debtrec.saldo. 
                    IF debtrec.rgdatum LT from-date THEN 
                        age-list.p-bal = age-list.p-bal + debtrec.saldo. 
                    ELSE IF debtrec.rgdatum GE from-date THEN 
                        age-list.credit = age-list.credit - debtrec.saldo. 
                END.
            END.
        END. 
    /*MTEND.*/
    /*M
    curr-bezeich = "Full paid A/P records". 
    DISP curr-bezeich WITH FRAME frame2. 
    */
     
    /*  within period's full paid transaction */ 
     
    counter = 0. 
    curr-lief-nr = 0. 
    curr-name = "".
END.

PROCEDURE age-list3:
    FOR EACH l-kredit WHERE l-kredit.rgdatum LE to-date AND 
        l-kredit.opart LE 1 AND l-kredit.counter GE 0 NO-LOCK USE-INDEX counter_ix, 
        FIRST l-lieferant WHERE l-lieferant.lief-nr = l-kredit.lief-nr 
        AND l-lieferant.firma GE from-name AND l-lieferant.firma LE to-name 
        BY l-lieferant.firma BY l-kredit.zahlkonto: 
        
        do-it = YES.
        IF segm NE 0 AND l-lieferant.segment1 NE segm THEN do-it = NO.
    
        IF do-it THEN
        DO:
          FIND FIRST queasy WHERE queasy.KEY = 221 AND queasy.number1 = l-kredit.lief-nr
            AND queasy.char1 = l-kredit.lscheinnr /*l-kredit.NAME*/ NO-LOCK NO-ERROR.
          IF AVAILABLE queasy THEN
          DO:
             IF l-kredit.counter > 0 THEN FIND FIRST age-list WHERE 
                 age-list.counter = l-kredit.counter NO-ERROR. 
             IF (l-kredit.counter = 0) OR (NOT AVAILABLE age-list) THEN 
             DO: 
                 /* CREATE aging record FOR a specific guest, based ON A/P-debit record */ 
                 CREATE age-list. 
                 age-list.rgdatum = queasy.date1. 
                 age-list.counter = l-kredit.counter. 
                 age-list.lief-nr = l-kredit.lief-nr. 
                 age-list.tot-debt = 0. 
                 age-list.firma = l-lieferant.firma. 
                 age-list.rechnr = l-kredit.name.    /* po number */ 
             
                 IF LENGTH(l-kredit.lscheinnr) LE 10 THEN 
                     age-list.lschein = l-kredit.lscheinnr. 
                 ELSE 
                     age-list.lschein = SUBSTR(l-kredit.lscheinnr, 11, LENGTH(l-kredit.lscheinnr) - 10). 
             
                 /*M
                 guest-name = l-lieferant.firma. 
                 DISP guest-name WITH FRAME frame2. 
                 */
             END. 
             IF l-kredit.zahlkonto = 0 THEN 
                 age-list.tot-debt = age-list.tot-debt + l-kredit.netto. 
             ELSE age-list.tot-debt = age-list.tot-debt + l-kredit.saldo. 
             
             /* previous balance  */ 
             IF l-kredit.rgdatum LT from-date AND l-kredit.zahlkonto = 0 THEN 
                 age-list.p-bal = age-list.p-bal + /* l-kredit.saldo */ l-kredit.netto. 
             
             /* debit transaction */ 
             IF l-kredit.rgdatum GE from-date AND l-kredit.zahlkonto = 0 THEN 
                 age-list.debit = age-list.debit + l-kredit.netto. 
             
             /* credit transaction */ 
             IF l-kredit.rgdatum LT from-date AND l-kredit.zahlkonto NE 0 THEN 
                 age-list.p-bal = age-list.p-bal + l-kredit.saldo. 
             ELSE 
             DO: 
                 IF l-kredit.rgdatum GE from-date AND l-kredit.zahlkonto NE 0 THEN 
                     age-list.credit = age-list.credit - l-kredit.saldo. 
             END.
          END.
        END.
    END. 
    /*MTELSE
    DO:*/
        counter = 0. 
        FOR EACH l-kredit WHERE l-kredit.lief-nr GT 0 AND l-kredit.rgdatum LE to-date 
            AND l-kredit.opart EQ 2 AND l-kredit.zahlkonto EQ 0 NO-LOCK USE-INDEX liefnr_ix, 
            FIRST l-lieferant WHERE l-lieferant.lief-nr = l-kredit.lief-nr 
            AND l-lieferant.firma GE from-name AND l-lieferant.firma LE to-name NO-LOCK 
            BY l-kredit.counter: 
    
            do-it = YES.
            IF segm NE 0 AND l-lieferant.segment1 NE segm THEN do-it = NO.
    
            IF do-it THEN
            DO:
              FIND FIRST queasy WHERE queasy.KEY = 221 AND queasy.number1 = l-kredit.lief-nr
                AND queasy.char1 = l-kredit.lscheinnr /*l-kredit.NAME*/ NO-LOCK NO-ERROR.
              IF AVAILABLE queasy THEN
              DO:
                 /* CREATE aging record FOR a specific guest */ 
                 CREATE age-list. 
                 ASSIGN  age-list.rgdatum  = queasy.date1
                         age-list.counter  = l-kredit.counter 
                         age-list.lief-nr  = l-kredit.lief-nr 
                         age-list.tot-debt = l-kredit.netto 
                         age-list.firma    = l-lieferant.firma
                         age-list.rechnr   = l-kredit.NAME    /* po number */ 
                         guest-name        = l-lieferant.firma.
                 
                 IF LENGTH(l-kredit.lscheinnr) LE 10 THEN 
                     age-list.lschein = l-kredit.lscheinnr. 
                 ELSE age-list.lschein = SUBSTR(l-kredit.lscheinnr, 11, 
                                                LENGTH(l-kredit.lscheinnr) - 10). 
                 
                 /*M
                 DISP guest-name WITH FRAME frame2. 
                 */
                 IF l-kredit.rgdatum LT from-date THEN 
                     age-list.p-bal = age-list.p-bal + l-kredit.netto. 
                 ELSE IF l-kredit.rgdatum GE from-date THEN 
                     age-list.debit = age-list.debit + l-kredit.netto. 
                 
                 FOR EACH debtrec WHERE debtrec.counter = l-kredit.counter 
                     AND debtrec.opart = 2 AND debtrec.zahlkonto GT 0 
                     AND debtrec.rgdatum LE to-date NO-LOCK: 
                 
                     age-list.tot-debt = age-list.tot-debt + debtrec.saldo. 
                     IF debtrec.rgdatum LT from-date THEN 
                         age-list.p-bal = age-list.p-bal + debtrec.saldo. 
                     ELSE IF debtrec.rgdatum GE from-date THEN 
                         age-list.credit = age-list.credit - debtrec.saldo. 
                 END.
              END.
            END.
        END. 
    /*MTEND.*/
    /*M
    curr-bezeich = "Full paid A/P records". 
    DISP curr-bezeich WITH FRAME frame2. 
    */
     
    /*  within period's full paid transaction */ 
     
    counter = 0. 
    curr-lief-nr = 0. 
    curr-name = "".
END.

IF NOT detailed THEN 
DO: 
    FOR EACH age-list BY age-list.firma: 
        IF to-date - age-list.rgdatum GT day3 THEN 
            age-list.debt3 = age-list.tot-debt. 
        ELSE IF to-date - age-list.rgdatum GT day2 THEN 
            age-list.debt2 = age-list.tot-debt. 
        ELSE IF to-date - age-list.rgdatum GT day1 THEN 
            age-list.debt1 = age-list.tot-debt. 
        ELSE age-list.debt0 = age-list.tot-debt.

        t-saldo  = t-saldo  + ROUND(age-list.tot-debt, 0). 
        t-prev   = t-prev   + ROUND(age-list.p-bal   , 0). 
        t-debit  = t-debit  + ROUND(age-list.debit   , 0). 
        t-credit = t-credit + ROUND(age-list.credit  , 0). 
        t-debt0  = t-debt0  + ROUND(age-list.debt0   , 0). 
        t-debt1  = t-debt1  + ROUND(age-list.debt1   , 0). 
        t-debt2  = t-debt2  + ROUND(age-list.debt2   , 0). 
        t-debt3  = t-debt3  + ROUND(age-list.debt3   , 0). 
        
        IF curr-lief-nr = 0 THEN  
            ASSIGN  curr-po      = age-list.rechnr
                    curr-lschein = age-list.lschein
                    firma        = age-list.firma
                    tot-debt     = ROUND(age-list.tot-debt, 0)  
                    p-bal        = ROUND(age-list.p-bal   , 0)  
                    debit        = ROUND(age-list.debit   , 0)  
                    credit       = ROUND(age-list.credit  , 0)  
                    debt0        = ROUND(age-list.debt0   , 0)  
                    debt1        = ROUND(age-list.debt1   , 0)  
                    debt2        = ROUND(age-list.debt2   , 0)  
                    debt3        = ROUND(age-list.debt3   , 0)  
                    counter      = counter + 1 .  
        ELSE IF curr-name NE age-list.firma THEN 
        DO: 
            IF p-bal NE 0 OR debit NE 0 OR credit NE 0 THEN 
            DO: 
                IF price-decimal = 0 THEN
                  outlist = "  " + STRING(counter,">>>9 ") 
                          + STRING(firma, "x(30)") 
                          + STRING(tot-debt, "->,>>>,>>>,>>>,>>9") 
                          + STRING(p-bal, "->,>>>,>>>,>>>,>>9") 
                          + STRING(debit, "->,>>>,>>>,>>>,>>9") 
                          + STRING(credit, "->,>>>,>>>,>>>,>>9") 
                          + STRING(debt0, "->,>>>,>>>,>>>,>>9") 
                          + STRING(debt1, "->,>>>,>>>,>>>,>>9") 
                          + STRING(debt2, "->,>>>,>>>,>>>,>>9") 
                          + STRING(debt3, "->,>>>,>>>,>>>,>>9"). 
                ELSE
                outlist = "  " + STRING(counter,">>>9 ") 
                        + STRING(firma, "x(30)") 
                        + STRING(tot-debt, "->>,>>>,>>>,>>9.99") 
                        + STRING(p-bal, "->>,>>>,>>>,>>9.99") 
                        + STRING(debit, "->>,>>>,>>>,>>9.99") 
                        + STRING(credit, "->>,>>>,>>>,>>9.99") 
                        + STRING(debt0, "->>,>>>,>>>,>>9.99") 
                        + STRING(debt1, "->>,>>>,>>>,>>9.99") 
                        + STRING(debt2, "->>,>>>,>>>,>>9.99") 
                        + STRING(debt3, "->>,>>>,>>>,>>9.99"). 

                RUN fill-in-list(YES, curr-po, curr-lschein, curr-rgdatum). 
                ASSIGN  curr-po      = age-list.rechnr
                        curr-lschein = age-list.lschein.
            END. 
            ELSE counter = counter - 1. 

            firma    = age-list.firma. 
            tot-debt = ROUND(age-list.tot-debt, 0). 
            p-bal    = ROUND(age-list.p-bal   , 0). 
            debit    = ROUND(age-list.debit   , 0). 
            credit   = ROUND(age-list.credit  , 0). 
            debt0    = ROUND(age-list.debt0   , 0). 
            debt1    = ROUND(age-list.debt1   , 0). 
            debt2    = ROUND(age-list.debt2   , 0). 
            debt3    = ROUND(age-list.debt3   , 0). 
            counter  = counter + 1. 
        END. 
        ELSE 
        DO: 
            tot-debt = tot-debt + ROUND(age-list.tot-debt, 0).
            p-bal    = p-bal    + ROUND(age-list.p-bal   , 0).
            debit    = debit    + ROUND(age-list.debit   , 0).
            credit   = credit   + ROUND(age-list.credit  , 0).
            debt0    = debt0    + ROUND(age-list.debt0   , 0).
            debt1    = debt1    + ROUND(age-list.debt1   , 0).
            debt2    = debt2    + ROUND(age-list.debt2   , 0).
            debt3    = debt3    + ROUND(age-list.debt3   , 0).
        END.
        curr-lief-nr = age-list.lief-nr. 
        IF NOT detailed THEN curr-name = age-list.firma. 
        DELETE age-list. 
    END.
END. 
ELSE /* IF detailed */
DO:
    IF NOT mi-bill THEN
        FOR EACH age-list BY age-list.firma /*BY age-list.rgdatum BY age-list.rechnr*/ : 
            RUN add-detail-date.
        END.
    FOR EACH age-list BY age-list.firma /*BY age-list.rgdatum BY age-list.rechnr*/ : 
        RUN add-detail-date.
    END.
END.

IF counter GT 0 AND (p-bal NE 0 OR debit NE 0 OR credit NE 0) AND NOT detailed THEN 
DO: 
    IF price-decimal = 0 THEN
      outlist = "  " + STRING(counter,">>>9 ") 
              + STRING(firma, "x(30)") 
              + STRING(tot-debt, "->,>>>,>>>,>>>,>>9") 
              + STRING(p-bal, "->,>>>,>>>,>>>,>>9") 
              + STRING(debit, "->,>>>,>>>,>>>,>>9") 
              + STRING(credit, "->,>>>,>>>,>>>,>>9") 
              + STRING(debt0, "->,>>>,>>>,>>>,>>9") 
              + STRING(debt1, "->,>>>,>>>,>>>,>>9") 
              + STRING(debt2, "->,>>>,>>>,>>>,>>9") 
              + STRING(debt3, "->,>>>,>>>,>>>,>>9").
    ELSE
    outlist = "  " + STRING(counter,">>>9 ") 
            + STRING(firma, "x(30)") 
            + STRING(tot-debt, "->>,>>>,>>>,>>9.99") 
            + STRING(p-bal, "->>,>>>,>>>,>>9.99") 
            + STRING(debit, "->>,>>>,>>>,>>9.99") 
            + STRING(credit, "->>,>>>,>>>,>>9.99") 
            + STRING(debt0, "->>,>>>,>>>,>>9.99") 
            + STRING(debt1, "->>,>>>,>>>,>>9.99") 
            + STRING(debt2, "->>,>>>,>>>,>>9.99") 
            + STRING(debt3, "->>,>>>,>>>,>>9.99"). 
    RUN fill-in-list(YES, curr-po, curr-lschein, curr-rgdatum). 
END. 
ELSE counter = counter - 1. 

outlist = "-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------". 
RUN fill-in-list(NO, "", "", "--------"). 
IF price-decimal = 0 THEN
  outlist = "       " 
          + STRING(translateExtended ("T O T A L  A/P:",lvCAREA,""), "x(30)") 
          + STRING(t-saldo, "->,>>>,>>>,>>>,>>9") 
          + STRING(t-prev, "->,>>>,>>>,>>>,>>9") 
          + STRING(t-debit, "->,>>>,>>>,>>>,>>9") 
          + STRING(t-credit, "->,>>>,>>>,>>>,>>9") 
          + STRING(t-debt0, "->,>>>,>>>,>>>,>>9") 
          + STRING(t-debt1, "->,>>>,>>>,>>>,>>9") 
          + STRING(t-debt2, "->,>>>,>>>,>>>,>>9") 
          + STRING(t-debt3, "->,>>>,>>>,>>>,>>9").
ELSE
  outlist = "       " 
          + STRING(translateExtended ("T O T A L  A/P:",lvCAREA,""), "x(30)") 
          + STRING(t-saldo, "->>,>>>,>>>,>>9.99") 
          + STRING(t-prev, "->>,>>>,>>>,>>9.99") 
          + STRING(t-debit, "->>,>>>,>>>,>>9.99") 
          + STRING(t-credit, "->>,>>>,>>>,>>9.99") 
          + STRING(t-debt0, "->>,>>>,>>>,>>9.99") 
          + STRING(t-debt1, "->>,>>>,>>>,>>9.99") 
          + STRING(t-debt2, "->>,>>>,>>>,>>9.99") 
          + STRING(t-debt3, "->>,>>>,>>>,>>9.99"). 
RUN fill-in-list(NO, "", "", ""). 
 
outlist = "-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------". 
RUN fill-in-list(NO, "", "", "--------"). 

outlist = "       " 
        + STRING(translateExtended ("Statistic Percentage (%) :",lvCAREA,""), "x(30)") 
        + "            100.00". 

DO i = 1 TO 54: 
    outlist = outlist + " ". 
END. 

outlist = outlist + STRING((t-debt0 / t-saldo * 100), "           ->>9.99") 
        + STRING((t-debt1 / t-saldo * 100), "           ->>9.99") 
        + STRING((t-debt2 / t-saldo * 100), "           ->>9.99") 
        + STRING((t-debt3 / t-saldo * 100), "           ->>9.99"). 
RUN fill-in-list(NO, "", "", ""). 

outlist = "". 
RUN fill-in-list(NO, "", "", ""). 
/*M 
HIDE FRAME frame2 NO-PAUSE. 
*/


/****************************************************************************/


PROCEDURE fill-in-list: 
    DEFINE INPUT PARAMETER fill-billno  AS LOGICAL.
    DEFINE INPUT PARAMETER curr-po      AS CHAR.
    DEFINE INPUT PARAMETER curr-lschein AS CHAR.
    DEFINE INPUT PARAMETER curr-rgdatum AS CHAR.
  
    CREATE apage-list. 
    IF fill-billno THEN 
    ASSIGN  apage-list.docu-nr = curr-po
            apage-list.lschein = curr-lschein
            apage-list.rgdatum = curr-rgdatum. 
    
    apage-list.str = outlist. 
    IF SUBSTR(outlist,1,5) = "-----" THEN 
    DO:
        apage-list.docu-nr = "----------------". 
        apage-list.lschein = "--------------". 
        apage-list.rgdatum = "--------".
    END.
END. 


PROCEDURE add-detail-date:
    IF to-date - age-list.rgdatum GT day3 THEN 
        age-list.debt3 = age-list.tot-debt. 
    ELSE IF to-date - age-list.rgdatum GT day2 THEN 
        age-list.debt2 = age-list.tot-debt. 
    ELSE IF to-date - age-list.rgdatum GT day1 THEN 
        age-list.debt1 = age-list.tot-debt. 
    ELSE age-list.debt0 = age-list.tot-debt. 
    
    t-saldo  = t-saldo  + age-list.tot-debt. 
    t-prev   = t-prev   + age-list.p-bal. 
    t-debit  = t-debit  + age-list.debit. 
    t-credit = t-credit + age-list.credit. 
    t-debt0  = t-debt0 + age-list.debt0. 
    t-debt1  = t-debt1 + age-list.debt1. 
    t-debt2  = t-debt2 + age-list.debt2. 
    t-debt3  = t-debt3 + age-list.debt3. 
    
    ASSIGN  curr-po      = age-list.rechnr
            curr-lschein = age-list.lschein
            curr-rgdatum = STRING(age-list.rgdatum, "99/99/99")
            firma        = age-list.firma
            tot-debt     = ROUND(age-list.tot-debt, 0)
            p-bal        = ROUND(age-list.p-bal   , 0)
            debit        = ROUND(age-list.debit   , 0)
            credit       = ROUND(age-list.credit  , 0)
            debt0        = ROUND(age-list.debt0   , 0)
            debt1        = ROUND(age-list.debt1   , 0)
            debt2        = ROUND(age-list.debt2   , 0)
            debt3        = ROUND(age-list.debt3   , 0)
            counter      = counter + 1.  

    IF p-bal NE 0 OR debit NE 0 OR credit NE 0 THEN 
    DO: 
        IF price-decimal = 0 THEN
          outlist = "  " + STRING(counter,">>>9 ") 
                + STRING(firma, "x(30)") 
                + STRING(tot-debt, "->,>>>,>>>,>>>,>>9") 
                + STRING(p-bal, "->,>>>,>>>,>>>,>>9") 
                + STRING(debit, "->,>>>,>>>,>>>,>>9") 
                + STRING(credit, "->,>>>,>>>,>>>,>>9") 
                + STRING(debt0, "->,>>>,>>>,>>>,>>9") 
                + STRING(debt1, "->,>>>,>>>,>>>,>>9") 
                + STRING(debt2, "->,>>>,>>>,>>>,>>9") 
                + STRING(debt3, "->,>>>,>>>,>>>,>>9").
        ELSE
        outlist = "  " + STRING(counter,">>>9 ") 
                + STRING(firma, "x(30)") 
                + STRING(tot-debt, "->>,>>>,>>>,>>9.99") 
                + STRING(p-bal, "->>,>>>,>>>,>>9.99") 
                + STRING(debit, "->>,>>>,>>>,>>9.99") 
                + STRING(credit, "->>,>>>,>>>,>>9.99") 
                + STRING(debt0, "->>,>>>,>>>,>>9.99") 
                + STRING(debt1, "->>,>>>,>>>,>>9.99") 
                + STRING(debt2, "->>,>>>,>>>,>>9.99") 
                + STRING(debt3, "->>,>>>,>>>,>>9.99"). 
        RUN fill-in-list(YES, curr-po, curr-lschein, curr-rgdatum). 
        ASSIGN  curr-po      = age-list.rechnr
                curr-lschein = age-list.lschein.
    END. 
    ELSE counter = counter - 1. 
    DELETE age-list.
END.
