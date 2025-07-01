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
DEFINE OUTPUT PARAMETER error-flag  AS LOGICAL NO-UNDO INIT NO.
DEFINE OUTPUT PARAMETER child-error AS LOGICAL NO-UNDO INIT NO.
DEFINE OUTPUT PARAMETER error-msg   AS CHAR    NO-UNDO INIT "".

DEFINE BUFFER qbuff FOR queasy.
DEFINE BUFFER buf-rcode FOR ratecode.
/*****************************************************************************/
IF NUM-ENTRIES(prcode,";") GE 1 THEN
DO:
    prcode = ENTRY(1,prcode,";").
END.

CASE case-type :
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
        IF AVAILABLE ratecode THEN error-flag = YES.
    END.
    WHEN 4 THEN
    DO:
    /* check Parent Child Start End Period */
        FIND FIRST queasy WHERE queasy.KEY = 2 
            AND queasy.char1 = prcode NO-LOCK NO-ERROR.
        IF AVAILABLE queasy THEN DO:
            IF NOT queasy.logi2 THEN
            DO:     
              IF NUM-ENTRIES(queasy.char3, ";") GT 2 THEN
              DO: /* investigate Child code */ 
                FIND FIRST ratecode WHERE ratecode.marknr = markNo 
                    AND ratecode.code = ENTRY(2, queasy.char3, ";") 
                    AND ratecode.argtnr = argtNo 
                    AND ratecode.zikatnr = zikatNo
                    AND ratecode.erwachs = adult
                    AND ratecode.kind1 = child1 
                    AND ratecode.kind2 = child2 
                    AND ratecode.wday  = w-day
                    AND (ratecode.startperiod LE startDate)
                    AND (ratecode.endperiod GE endDate) NO-LOCK NO-ERROR.
                IF NOT AVAILABLE ratecode THEN
                DO:
                  ASSIGN
                      error-flag  = YES
                      child-error = YES                      
                  .
                  /*FDL Oct 11, 2024: Ticket EA982C*/
                  FIND FIRST buf-rcode WHERE buf-rcode.marknr EQ markNo 
                    AND buf-rcode.code EQ ENTRY(2, queasy.char3, ";") NO-LOCK NO-ERROR.
                  IF AVAILABLE buf-rcode THEN
                  DO:
                    error-msg   = buf-rcode.CODE + "   "
                                  + STRING(buf-rcode.startperiode)
                                  + " - "
                                  + STRING(buf-rcode.endperiode).
                  END.
                  RETURN.
                END.
              END.
              /* FDL Comment EA982C
              ELSE                  
              /* investigate Parent code */
              FOR EACH qbuff WHERE qbuff.KEY = 2 
                AND NUM-ENTRIES(qbuff.char3, ";") GT 2
                AND ENTRY(2, qbuff.char3, ";") = queasy.char1 NO-LOCK:
                FIND FIRST ratecode WHERE ratecode.marknr = markNo 
                    AND ratecode.code = qbuff.char1 
                    AND ratecode.argtnr = argtNo 
                    AND ratecode.zikatnr = zikatNo
                    AND ratecode.erwachs = adult
                    AND ratecode.kind1 = child1 
                    AND ratecode.kind2 = child2 
                    AND ratecode.wday  = w-day
                    AND (ratecode.startperiod GE startDate)
                    AND (ratecode.endperiod GT endDate) NO-LOCK NO-ERROR.
                IF AVAILABLE ratecode THEN
                DO:
                  ASSIGN
                      error-flag  = YES
                      child-error = YES
                      error-msg   = ratecode.CODE + "   "
                                  + STRING(ratecode.startperiode)
                                  + " - "
                                  + STRING(ratecode.endperiode)
                  .
                  RETURN.
                END.
                FIND FIRST ratecode WHERE ratecode.marknr = markNo 
                    AND ratecode.code = qbuff.char1 
                    AND ratecode.argtnr = argtNo 
                    AND ratecode.zikatnr = zikatNo
                    AND ratecode.erwachs = adult
                    AND ratecode.kind1 = child1 
                    AND ratecode.kind2 = child2 
                    AND ratecode.wday  = w-day
                    AND (ratecode.startperiod LT startDate)
                    AND (ratecode.endperiod LE endDate) NO-LOCK NO-ERROR.
                IF AVAILABLE ratecode THEN
                DO:
                  ASSIGN
                      error-flag  = YES
                      child-error = YES
                      error-msg   = ratecode.CODE + "   "
                                  + STRING(ratecode.startperiode)
                                  + " - "
                                  + STRING(ratecode.endperiode)
                  .
                  RETURN.
                END.
              END.
              */
            END.
        END.        
        
        IF s-recid EQ ? THEN
        FIND FIRST ratecode WHERE ratecode.marknr = markNo 
            AND ratecode.code = prcode 
            AND ratecode.argtnr = argtNo 
            AND ratecode.zikatnr = zikatNo
            AND ratecode.erwachs = adult
            AND ratecode.kind1 = child1 
            AND ratecode.kind2 = child2 
            AND ratecode.wday  = w-day 
            AND NOT (ratecode.startperiod GT endDate) 
            AND NOT (ratecode.endperiod LT startDate) NO-LOCK NO-ERROR. 
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
            AND NOT (ratecode.startperiod GT endDate) 
            AND NOT (ratecode.endperiod LT startDate) NO-LOCK NO-ERROR. 
        
        IF AVAILABLE ratecode THEN error-flag = YES.
    END.
END CASE.
