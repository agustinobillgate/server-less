
DEFINE TEMP-TABLE t-ratecode   LIKE ratecode
    FIELD s-recid               AS INTEGER.

DEFINE INPUT PARAMETER case-type    AS INTEGER.
DEFINE INPUT PARAMETER markNo       AS INTEGER.
DEFINE INPUT PARAMETER prcode       AS CHAR.
DEFINE INPUT PARAMETER argtNo       AS INTEGER.
DEFINE INPUT PARAMETER zikatNo      AS INTEGER.
DEFINE INPUT PARAMETER adult        AS INTEGER.
DEFINE INPUT PARAMETER child1       AS INTEGER.
DEFINE INPUT PARAMETER child2       AS INTEGER.
DEFINE INPUT PARAMETER w-day        AS INTEGER.
DEFINE INPUT PARAMETER startDate    AS DATE.
DEFINE INPUT PARAMETER endDate      AS DATE.
DEFINE INPUT PARAMETER s-recid      AS INTEGER.
DEFINE OUTPUT PARAMETER TABLE FOR t-ratecode.
    
/*****************************************************************************/
CASE case-type :
    WHEN 1 THEN
    FOR EACH ratecode WHERE ratecode.marknr = markNo
        AND ratecode.code = prcode AND ratecode.argtnr = argtNo 
        AND ratecode.zikatnr = zikatNo NO-LOCK :
        RUN cr-t-ratecode.
    END.
    WHEN 2 THEN
    FOR EACH ratecode WHERE ratecode.code = prcode NO-LOCK: 
        RUN cr-t-ratecode.
    END.
    WHEN 3 THEN
    DO:
        FIND FIRST ratecode WHERE ratecode.marknr = markNo
            AND ratecode.code = prcode 
            AND ratecode.argtnr = argtNo 
            AND ratecode.zikatnr = zikatNo 
            AND RECID(ratecode) NE s-recid
            AND ratecode.erwachs = adult 
            AND ratecode.kind1 = child1 
            AND ratecode.kind2 = child2 
            AND ratecode.wday  = w-day
            AND NOT ratecode.startperiod GE endDate
            AND NOT ratecode.endperiod LE startDate NO-LOCK NO-ERROR. 
        IF AVAILABLE ratecode THEN RUN cr-t-ratecode.
    END.
    WHEN 4 THEN
    DO:
        IF s-recid EQ ? THEN
        FIND FIRST ratecode WHERE ratecode.marknr = markNo 
            AND ratecode.code = prcode 
            AND ratecode.argtnr = argtNo 
            AND ratecode.zikatnr = zikatNo
            AND ratecode.erwachs = adult
            AND ratecode.kind1 = child1 
            AND ratecode.kind2 = child2 
            AND ratecode.wday  = w-day
            AND NOT ratecode.startperiod GE endDate
            AND NOT ratecode.endperiod LE startDate NO-LOCK NO-ERROR. 
        ELSE
        FIND FIRST ratecode WHERE ratecode.marknr = markNo 
            AND ratecode.code = prcode 
            AND ratecode.argtnr = argtNo 
            AND ratecode.zikatnr = zikatNo 
            AND RECID(ratecode) NE s-recid
            AND ratecode.erwachs = adult 
            AND ratecode.kind1 = child1 
            AND ratecode.kind2 = child2 
            AND ratecode.wday  = w-day
            AND NOT ratecode.startperiod GE endDate
            AND NOT ratecode.endperiod LE startDate NO-LOCK NO-ERROR. 

        IF AVAILABLE ratecode THEN RUN cr-t-ratecode.
    END.
    WHEN 5 THEN
    DO:
        FIND FIRST ratecode WHERE ratecode.CODE = prcode
            AND ratecode.zikatnr = zikatNo NO-LOCK NO-ERROR.
        IF AVAILABLE ratecode THEN
            RUN cr-t-ratecode.
    END.
END CASE.


PROCEDURE cr-t-ratecode :
    CREATE t-ratecode.
    BUFFER-COPY ratecode TO t-ratecode.
    t-ratecode.s-recid = RECID(ratecode).
END.

