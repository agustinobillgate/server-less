DEFINE TEMP-TABLE apage-list
    FIELD docu-nr  AS CHARACTER FORMAT "x(16)" 
    FIELD lschein  AS CHARACTER FORMAT "x(14)" 
    FIELD rgdatum  AS CHARACTER FORMAT "x(8)"
    FIELD rechnr   AS CHARACTER
    FIELD ag-datum AS CHARACTER FORMAT "x(6)"
    FIELD overdue  AS CHARACTER FORMAT "x(8)"             
    FIELD term-pay AS CHARACTER FORMAT "x(8)"
    field t-no     as character format "x(7)" 
    field t-supp   as character format "x(30)"
    field t-saldo  as character format "x(18)" 
    field t-prev   as character format "x(18)"
    field t-debit  as character format "x(18)"
    field t-credit as character format "x(18)"
    field t-debt0  as character format "x(18)"
    field t-debt1  as character format "x(18)"
    field t-debt2  as character format "x(18)"
    field t-debt3  as character format "x(18)".
/**/
DEFINE INPUT  PARAMETER pvILanguage  AS INTEGER NO-UNDO.
DEFINE INPUT  PARAMETER to-date      AS DATE.
DEFINE INPUT  PARAMETER from-name    AS CHARACTER.
DEFINE INPUT  PARAMETER to-name      AS CHARACTER.           
DEFINE INPUT  PARAMETER mi-bill      AS LOGICAL.
DEFINE INPUT  PARAMETER segm         AS INTEGER.
DEFINE INPUT  PARAMETER curr-disp    AS INTEGER.
DEFINE INPUT  PARAMETER round-zero   AS LOGICAL.
DEFINE OUTPUT PARAMETER TABLE        FOR apage-list.
                                                      
define variable tt-no     as character format "x(7)"  no-undo. 
define variable tt-supp   as character format "x(30)" no-undo. 
define variable tt-saldo  as character format "x(18)" no-undo. 
define variable tt-prev   as character format "x(18)" no-undo. 
define variable tt-debit  as character format "x(18)" no-undo. 
define variable tt-credit as character format "x(18)" no-undo. 
define variable tt-debt0  as character format "x(18)" no-undo. 
define variable tt-debt1  as character format "x(18)" no-undo. 
define variable tt-debt2  as character format "x(18)" no-undo. 
define variable tt-debt3  as character format "x(18)" no-undo.



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
DEFINE VARIABLE agdatum      AS INTEGER NO-UNDO.
DEFINE VARIABLE overdatum    AS DATE NO-UNDO.
DEFINE VARIABLE termof-pay   AS INT NO-UNDO.

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
DEFINE VARIABLE voucher-no   AS CHARACTER NO-UNDO FORMAT "x(11)".

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
    FIELD voucher-no      AS INTEGER FORMAT ">>>,>>>,>>>"
    FIELD p-bal           AS DECIMAL FORMAT "->>>,>>>,>>9" INITIAL 0 
    FIELD debit           AS DECIMAL FORMAT "->>>,>>>,>>9" INITIAL 0 
    FIELD credit          AS DECIMAL FORMAT "->>>,>>>,>>9" INITIAL 0 
    FIELD saldo           AS DECIMAL FORMAT "->>>,>>>,>>9" INITIAL 0 
    FIELD debt0           AS DECIMAL FORMAT "->>>,>>>,>>9" INITIAL 0 
    FIELD debt1           AS DECIMAL FORMAT "->>>,>>>,>>9" INITIAL 0 
    FIELD debt2           AS DECIMAL FORMAT "->>>,>>>,>>9" INITIAL 0 
    FIELD debt3           AS DECIMAL FORMAT "->>>,>>>,>>9" INITIAL 0 
    FIELD tot-debt        AS DECIMAL FORMAT "->>>,>>>,>>9" INITIAL 0
    FIELD ap-term         AS INTEGER.
     

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


IF NOT mi-bill THEN
    FOR EACH age-list WHERE age-list.tot-debt NE 0 BY age-list.firma /*BY age-list.rgdatum BY age-list.rechnr*/ :        
        RUN add-detail-date.
    END.
ELSE DO:
    FOR EACH age-list BY age-list.rgdatum /*BY age-list.rgdatum BY age-list.rechnr*/ : 
        RUN add-detail-date.

    END.
END.    

counter = counter - 1. 

tt-no     = "-------".
tt-supp   = "------------------------------".
tt-saldo  = "------------------".
tt-prev   = "------------------".
tt-debit  = "------------------".
tt-credit = "------------------".
tt-debt0  = "------------------".
tt-debt1  = "------------------".
tt-debt2  = "------------------".
tt-debt3  = "------------------".

RUN fill-in-list(NO, "", "", "--------", "", "", "", ""). 
IF price-decimal = 0 THEN
DO:
  tt-no     = "       ".
  tt-supp   = STRING(translateExtended ("T O T A L  A/P:",lvCAREA,""), "x(30)"). 
  tt-saldo  = STRING(t-saldo, "->,>>>,>>>,>>>,>>9").
  tt-prev   = STRING(t-prev, "->,>>>,>>>,>>>,>>9"). 
  tt-debit  = STRING(t-debit, "->,>>>,>>>,>>>,>>9").
  tt-credit = STRING(t-credit, "->,>>>,>>>,>>>,>>9").
  tt-debt0  = STRING(t-debt0, "->,>>>,>>>,>>>,>>9"). 
  tt-debt1  = STRING(t-debt1, "->,>>>,>>>,>>>,>>9"). 
  tt-debt2  = STRING(t-debt2, "->,>>>,>>>,>>>,>>9").
  tt-debt3  = STRING(t-debt3, "->,>>>,>>>,>>>,>>9").
END.
ELSE
DO:
  tt-no     = "       ". 
  tt-supp   = STRING(translateExtended ("T O T A L  A/P:",lvCAREA,""), "x(30)"). 
  tt-saldo  = STRING(t-saldo, "->>,>>>,>>>,>>9.99"). 
  tt-prev   = STRING(t-prev, "->>,>>>,>>>,>>9.99"). 
  tt-debit  = STRING(t-debit, "->>,>>>,>>>,>>9.99"). 
  tt-credit = STRING(t-credit, "->>,>>>,>>>,>>9.99"). 
  tt-debt0  = STRING(t-debt0, "->>,>>>,>>>,>>9.99"). 
  tt-debt1  = STRING(t-debt1, "->>,>>>,>>>,>>9.99"). 
  tt-debt2  = STRING(t-debt2, "->>,>>>,>>>,>>9.99"). 
  tt-debt3  = STRING(t-debt3, "->>,>>>,>>>,>>9.99"). 
END.

RUN fill-in-list(NO, "", "", "", "", "", "", ""). 
 
tt-no     = "-------".
tt-supp   = "------------------------------".
tt-saldo  = "------------------".
tt-prev   = "------------------".
tt-debit  = "------------------".
tt-credit = "------------------".
tt-debt0  = "------------------".
tt-debt1  = "------------------".
tt-debt2  = "------------------".
tt-debt3  = "------------------".

RUN fill-in-list(NO, "", "", "--------", "", "", "", ""). 

 tt-no     = "       ". 
 tt-supp   = STRING(translateExtended ("Statistic Percentage (%) :",lvCAREA,""), "x(30)"). 
 tt-saldo  = "            100.00".
 tt-prev   = "".
 tt-debit  = "".
 tt-credit = "".
 tt-debt0  = STRING((t-debt0 / t-saldo * 100), "           ->>9.99").
 tt-debt1  = STRING((t-debt1 / t-saldo * 100), "           ->>9.99").
 tt-debt2  = STRING((t-debt2 / t-saldo * 100), "           ->>9.99").
 tt-debt3  = STRING((t-debt3 / t-saldo * 100), "           ->>9.99").

RUN fill-in-list(NO, "", "", "", "", "", "", ""). 

 tt-no     = "" .
 tt-supp   = "" . 
 tt-saldo  = "" .
 tt-prev   = "" .
 tt-debit  = "" .
 tt-credit = "" .
 tt-debt0  = "" .
 tt-debt1  = "" .
 tt-debt2  = "" .
 tt-debt3  = "" .

RUN fill-in-list(NO, "", "", "", "", "", "", ""). 

PROCEDURE age-list:
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
                age-list.rechnr = l-kredit.name.     /* po number */ 
                age-list.voucher-no = l-kredit.rechnr.                  
                
                /*FD Nov 02, 2022 => Ticket BB0BD0 - to be the same as the AP List report*/
                age-list.lschein = l-kredit.lscheinnr.

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
            age-list.ap-term = l-kredit.ziel.
        END.
    END. 

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
                    guest-name        = l-lieferant.firma
                    age-list.voucher-no = l-kredit.rechnr.

            /*FD Nov 02, 2022 => Ticket BB0BD0 - to be the same as the AP List report*/
            age-list.lschein = l-kredit.lscheinnr.

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
            age-list.ap-term = l-kredit.ziel.
        END.
    END. 
     
    /*  within period's full paid transaction */ 
     
    counter = 0. 
    curr-lief-nr = 0. 
    curr-name = "".
END.


PROCEDURE age-list1:

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
                age-list.voucher-no = l-kredit.rechnr.

                /*FD Nov 02, 2022 => Ticket BB0BD0 - to be the same as the AP List report*/
                age-list.lschein = l-kredit.lscheinnr.

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
            age-list.ap-term = l-kredit.ziel.
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
                        guest-name        = l-lieferant.firma
                        age-list.voucher-no = l-kredit.rechnr
                    .

                /*FD Nov 02, 2022 => Ticket BB0BD0 - to be the same as the AP List report*/
                age-list.lschein = l-kredit.lscheinnr.

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
            age-list.ap-term = l-kredit.ziel.
        END. 

    /*  within period's full paid transaction */ 
     
    counter = 0. 
    curr-lief-nr = 0. 
    curr-name = "".
END.

PROCEDURE age-list2:

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
                age-list.voucher-no = l-kredit.rechnr.

                /*FD Nov 02, 2022 => Ticket BB0BD0 - to be the same as the AP List report*/
                age-list.lschein = l-kredit.lscheinnr.

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
            age-list.ap-term = l-kredit.ziel.
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
                        guest-name        = l-lieferant.firma
                        age-list.voucher-no = l-kredit.rechnr.

                /*FD Nov 02, 2022 => Ticket BB0BD0 - to be the same as the AP List report*/
                age-list.lschein = l-kredit.lscheinnr.

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
                age-list.ap-term = l-kredit.ziel.
                
            END.           
        END. 
     
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
          FIND FIRST queasy WHERE queasy.KEY = 221 AND queasy.number1 EQ l-kredit.lief-nr
            AND queasy.char1 EQ l-kredit.lscheinnr /*l-kredit.NAME*/ NO-LOCK NO-ERROR.
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

                 /*FD Nov 02, 2022 => Ticket BB0BD0 - to be the same as the AP List report*/
                 age-list.lschein = l-kredit.lscheinnr.

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
             FIND FIRST l-orderhdr WHERE l-orderhdr.docu-nr EQ l-kredit.NAME NO-LOCK NO-ERROR.
             IF AVAILABLE l-orderhdr THEN
             DO:
                 age-list.ap-term = l-orderhdr.angebot-lief[2].
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
                         guest-name        = l-lieferant.firma
                         age-list.voucher-no = l-kredit.rechnr.

                 /*FD Nov 02, 2022 => Ticket BB0BD0 - to be the same as the AP List report*/
                 age-list.lschein = l-kredit.lscheinnr.

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
                 FIND FIRST l-orderhdr WHERE l-orderhdr.docu-nr EQ l-kredit.NAME NO-LOCK NO-ERROR.
                 IF AVAILABLE l-orderhdr THEN
                 DO:
                     age-list.ap-term = l-orderhdr.angebot-lief[2].
                 END.
              END.
            END.
        END. 
     
    /*  within period's full paid transaction */ 
     
    counter = 0. 
    curr-lief-nr = 0. 
    curr-name = "".
END.

/****************************************************************************/

PROCEDURE fill-in-list: 
    DEFINE INPUT PARAMETER fill-billno  AS LOGICAL.
    DEFINE INPUT PARAMETER curr-po      AS CHAR.
    DEFINE INPUT PARAMETER curr-lschein AS CHAR.
    DEFINE INPUT PARAMETER curr-rgdatum AS CHAR.
    DEFINE INPUT PARAMETER voucher-no   AS CHAR.
    DEFINE INPUT PARAMETER agdatum      AS CHAR.
    DEFINE INPUT PARAMETER overdatum    AS CHAR.
    DEFINE INPUT PARAMETER termof-pay   AS CHAR.

    CREATE apage-list. 
    IF fill-billno THEN 
    ASSIGN  apage-list.docu-nr   = curr-po
            apage-list.lschein   = curr-lschein
            apage-list.rgdatum   = curr-rgdatum 
            apage-list.rechnr    = voucher-no
            apage-list.ag-datum  = agdatum
            apage-list.overdue   = overdatum
            apage-list.term-pay  = termof-pay
            .

    IF tt-no = "-------" THEN 
    DO:
        apage-list.docu-nr = "----------------". 
        apage-list.lschein = "-------------------". 
        apage-list.rgdatum = "--------".
        apage-list.rechnr  = "----------".
        apage-list.rechnr  = "----------".
        apage-list.rechnr  = "----------".
        apage-list.ag-datum = "------".
        apage-list.overdue = "--------".
    END. 
        apage-list.t-no     = tt-no     .
        apage-list.t-supp   = tt-supp   .
        apage-list.t-saldo  = tt-saldo  .
        apage-list.t-prev   = tt-prev   .
        apage-list.t-debit  = tt-debit  .
        apage-list.t-credit = tt-credit .
        apage-list.t-debt0  = tt-debt0  .
        apage-list.t-debt1  = tt-debt1  .
        apage-list.t-debt2  = tt-debt2  .
        apage-list.t-debt3  = tt-debt3  .
END. 

PROCEDURE add-detail-date:
     IF to-date - age-list.rgdatum /*(age-list.rgdatum + age-list.ap-term)*/ LE 30 THEN 
        age-list.debt0 = age-list.tot-debt.
    ELSE IF to-date - age-list.rgdatum /* (age-list.rgdatum + age-list.ap-term)*/ GE 30
        AND to-date - age-list.rgdatum /* (age-list.rgdatum + age-list.ap-term)*/ LT 60 THEN
        age-list.debt1 = age-list.tot-debt.
    ELSE IF to-date - age-list.rgdatum /* (age-list.rgdatum + age-list.ap-term)*/ GE 60
        AND to-date - age-list.rgdatum /* (age-list.rgdatum + age-list.ap-term)*/ LT 90 THEN
        age-list.debt2 = age-list.tot-debt.
    ELSE IF to-date - age-list.rgdatum /* (age-list.rgdatum + age-list.ap-term)*/ GE 90 THEN
        age-list.debt3 = age-list.tot-debt.

    IF round-zero THEN
    DO:
        t-saldo  = t-saldo  + ROUND(age-list.tot-debt, 0). 
        t-prev   = t-prev   + ROUND(age-list.p-bal   , 0).
        t-debit  = t-debit  + ROUND(age-list.debit   , 0).
        t-credit = t-credit + ROUND(age-list.credit  , 0).
        t-debt0  = t-debt0  + ROUND(age-list.debt0   , 0).
        t-debt1  = t-debt1  + ROUND(age-list.debt1   , 0).
        t-debt2  = t-debt2  + ROUND(age-list.debt2   , 0).
        t-debt3  = t-debt3  + ROUND(age-list.debt3   , 0).

        ASSIGN  
            curr-po      = age-list.rechnr
            curr-lschein = age-list.lschein
            curr-rgdatum = STRING(age-list.rgdatum, "99/99/99")
            firma        = age-list.firma
            voucher-no   = STRING(age-list.voucher-no)
            tot-debt     = ROUND(age-list.tot-debt, 0)
            p-bal        = ROUND(age-list.p-bal   , 0)
            debit        = ROUND(age-list.debit   , 0)
            credit       = ROUND(age-list.credit  , 0)
            debt0        = ROUND(age-list.debt0   , 0)
            debt1        = ROUND(age-list.debt1   , 0)
            debt2        = ROUND(age-list.debt2   , 0)
            debt3        = ROUND(age-list.debt3   , 0)
            agdatum      = to-date - age-list.rgdatum
            overdatum    = age-list.rgdatum + ap-term
            termof-pay   = age-list.ap-term
        .
        counter = counter + 1. 
    END.
    ELSE
    DO:    
        t-saldo  = t-saldo  + age-list.tot-debt. 
        t-prev   = t-prev   + age-list.p-bal.
        t-debit  = t-debit  + age-list.debit.
        t-credit = t-credit + age-list.credit.
        t-debt0  = t-debt0  + age-list.debt0.
        t-debt1  = t-debt1  + age-list.debt1.
        t-debt2  = t-debt2  + age-list.debt2.
        t-debt3  = t-debt3  + age-list.debt3.

        ASSIGN  
            curr-po       = age-list.rechnr
            curr-lschein  = age-list.lschein
            curr-rgdatum  = STRING(age-list.rgdatum, "99/99/99")
            firma         = age-list.firma
            voucher-no    = STRING(age-list.voucher-no)
            tot-debt      = age-list.tot-debt
            p-bal         = age-list.p-bal   
            debit         = age-list.debit   
            credit        = age-list.credit  
            debt0         = age-list.debt0   
            debt1         = age-list.debt1   
            debt2         = age-list.debt2   
            debt3         = age-list.debt3 
            counter       = counter + 1
            agdatum       = to-date - age-list.rgdatum
            overdatum     = age-list.rgdatum + ap-term
            termof-pay    = age-list.ap-term.
    END. 

    IF p-bal NE 0 OR debit NE 0 OR credit NE 0 THEN 
    DO: 
        IF price-decimal = 0 THEN
        ASSIGN
          tt-no     = "  " + STRING(counter,">>>9 ") 
          tt-supp   = STRING(firma, "x(30)") 
          tt-saldo  = STRING(tot-debt, "->,>>>,>>>,>>>,>>9") 
          tt-prev   = STRING(p-bal, "->,>>>,>>>,>>>,>>9") 
          tt-debit  = STRING(debit, "->,>>>,>>>,>>>,>>9") 
          tt-credit = STRING(credit, "->,>>>,>>>,>>>,>>9") 
          tt-debt0  = STRING(debt0, "->,>>>,>>>,>>>,>>9") 
          tt-debt1  = STRING(debt1, "->,>>>,>>>,>>>,>>9") 
          tt-debt2  = STRING(debt2, "->,>>>,>>>,>>>,>>9") 
          tt-debt3  = STRING(debt3, "->,>>>,>>>,>>>,>>9").
        ELSE
        ASSIGN
          tt-no     = "  " + STRING(counter,">>>9 ") 
          tt-supp   = STRING(firma, "x(30)") 
          tt-saldo  = STRING(tot-debt, "->>,>>>,>>>,>>9.99") 
          tt-prev   = STRING(p-bal, "->>,>>>,>>>,>>9.99") 
          tt-debit  = STRING(debit, "->>,>>>,>>>,>>9.99") 
          tt-credit = STRING(credit, "->>,>>>,>>>,>>9.99") 
          tt-debt0  = STRING(debt0, "->>,>>>,>>>,>>9.99") 
          tt-debt1  = STRING(debt1, "->>,>>>,>>>,>>9.99") 
          tt-debt2  = STRING(debt2, "->>,>>>,>>>,>>9.99") 
          tt-debt3  = STRING(debt3, "->>,>>>,>>>,>>9.99"). 

        RUN fill-in-list(YES, curr-po, curr-lschein, curr-rgdatum, voucher-no, agdatum, overdatum, termof-pay). 
        ASSIGN  curr-po      = age-list.rechnr
                curr-lschein = age-list.lschein
                voucher-no   = STRING(age-list.voucher-no).
    END. 
    ELSE counter = counter - 1. 
    DELETE age-list.
END.

