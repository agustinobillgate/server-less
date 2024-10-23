
DEFINE TEMP-TABLE tb1 LIKE queasy
    FIELD waehrungsnr   LIKE waehrung.waehrungsnr  
    FIELD wabkurz       LIKE waehrung.wabkurz  
.
/*
    FIELD KEY       LIKE queasy.KEY
    FIELD number1   LIKE queasy.number1
    FIELD number2   LIKE queasy.number2
    FIELD char1     LIKE queasy.char1
    FIELD char2     LIKE queasy.char2
    FIELD char3     LIKE queasy.char3
    FIELD logi1     LIKE queasy.logi1
    FIELD logi2     LIKE queasy.logi2
    FIELD deci1     LIKE queasy.deci1
    FIELD date1     LIKE queasy.date1
    FIELD betriebsnr    LIKE queasy.betriebsnr
    FIELD waehrungsnr   LIKE waehrung.waehrungsnr
    FIELD wabkurz   LIKE waehrung.wabkurz.
*/

DEFINE INPUT PARAMETER case-type        AS INTEGER.
DEFINE INPUT PARAMETER int1             AS INTEGER.
DEFINE INPUT PARAMETER int2             AS INTEGER.
DEFINE INPUT PARAMETER inp-char1        AS CHARACTER.
DEFINE OUTPUT PARAMETER TABLE FOR tb1.


/*****************************************************************************/
CASE case-type :
    WHEN 1 THEN
    DO:
        FOR EACH queasy WHERE queasy.key = int1 NO-LOCK, 
            FIRST waehrung WHERE waehrung.waehrungsnr = queasy.number1 NO-LOCK 
            BY queasy.logi2 DESC BY queasy.char2 :
            RUN cr-tb1.
        END.
    END.
    WHEN 2 THEN
    DO:
        FOR EACH queasy WHERE queasy.key = int1 
            AND queasy.char1 GE inp-char1 NO-LOCK, 
            FIRST waehrung WHERE waehrung.waehrungsnr = queasy.number1 NO-LOCK 
            BY queasy.logi2 DESC BY queasy.char1:
            RUN cr-tb1.
        END.
    END.
END CASE.


/******************************* PROCEDURES **********************************/
PROCEDURE cr-tb1 :
    CREATE tb1.
    BUFFER-COPY waehrung TO tb1.
    BUFFER-COPY queasy TO tb1.
/*
    ASSIGN
        tb1.KEY       = queasy.KEY
        tb1.number1   = queasy.number1
        tb1.char1     = queasy.char1
        tb1.char2     = queasy.char2
        tb1.char3     = queasy.char3
        tb1.logi2     = queasy.logi2
        tb1.deci1     = queasy.deci1
        tb1.date1     = queasy.date1
        tb1.betriebsnr    = queasy.betriebsnr
        tb1.waehrungsnr   = waehrung.waehrungsnr
        tb1.wabkurz   = waehrung.wabkurz.
    .
*/
END.
