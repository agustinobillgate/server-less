DEFINE TEMP-TABLE t-article
    FIELD nr            AS INTEGER   FORMAT ">>>9" LABEL "No"
    FIELD artnr         AS INTEGER   FORMAT ">>>>>>>9" LABEL "ArtNo"
    FIELD dept          AS INTEGER   FORMAT ">>9"
    FIELD bezeich       AS CHARACTER FORMAT "x(30)"  LABEL "Article Name"
    FIELD img           AS CHARACTER FORMAT "x(100)"
    FIELD remark        AS CHARACTER FORMAT "x(78)" LABEL "Description"
    FIELD activ-art     AS LOGICAL LABEL "Active" FORMAT "Yes/No"
    FIELD sold-out      AS LOGICAL LABEL "SoldOut" FORMAT "Yes/No"
    FIELD selected-art  AS LOGICAL INITIAL NO             
    .

DEFINE INPUT PARAMETER case-type AS INTEGER.
DEFINE INPUT PARAMETER TABLE FOR t-article.
DEFINE OUTPUT PARAMETER success-flag AS LOGICAL INITIAL NO.

IF case-type EQ 1 THEN /*Active Article*/
DO:
    FOR EACH t-article WHERE t-article.selected-art EQ YES AND t-article.activ-art EQ NO NO-LOCK:
        FIND FIRST queasy WHERE queasy.KEY EQ 222 
            AND queasy.number1 EQ 2
            AND queasy.number2 EQ t-article.artnr 
            AND queasy.number3 EQ t-article.dept
            AND t-article.activ-art EQ queasy.logi1 NO-LOCK NO-ERROR.
        IF AVAILABLE queasy THEN
        DO:
            FIND CURRENT queasy EXCLUSIVE-LOCK.
            queasy.logi1 = YES.
            FIND CURRENT queasy NO-LOCK.
        END.
        ELSE
        DO:
            CREATE queasy.
            ASSIGN
                queasy.KEY      = 222
                queasy.number1  = 2
                queasy.number2  = t-article.artnr
                queasy.number3  = t-article.dept
                queasy.logi1    = YES
                queasy.logi2    = NO
            .
        END.
    END.

    success-flag = YES.
END.
ELSE IF case-type EQ 2 THEN /*Deactive Article*/
DO:
    FOR EACH t-article WHERE t-article.selected-art EQ YES AND t-article.activ-art EQ YES NO-LOCK:
        FIND FIRST queasy WHERE queasy.KEY EQ 222 
            AND queasy.number1 EQ 2
            AND queasy.number2 EQ t-article.artnr 
            AND queasy.number3 EQ t-article.dept
            AND t-article.activ-art EQ queasy.logi1 NO-LOCK NO-ERROR.
        IF AVAILABLE queasy THEN
        DO:
            FIND CURRENT queasy EXCLUSIVE-LOCK.
            queasy.logi1 = NO.
            FIND CURRENT queasy NO-LOCK.
        END.        
    END.

    success-flag = YES.
END.
ELSE IF case-type EQ 3 THEN /*Active SoldOut Article*/
DO:
    FOR EACH t-article WHERE t-article.selected-art EQ YES AND t-article.sold-out EQ NO NO-LOCK:
        FIND FIRST queasy WHERE queasy.KEY EQ 222 
            AND queasy.number1 EQ 2
            AND queasy.number2 EQ t-article.artnr 
            AND queasy.number3 EQ t-article.dept
            AND t-article.sold-out EQ queasy.logi2 NO-LOCK NO-ERROR.
        IF AVAILABLE queasy THEN
        DO:
            FIND CURRENT queasy EXCLUSIVE-LOCK.
            queasy.logi2 = YES.
            FIND CURRENT queasy NO-LOCK.
        END.
        ELSE
        DO:
            CREATE queasy.
            ASSIGN
                queasy.KEY      = 222
                queasy.number1  = 2
                queasy.number2  = t-article.artnr
                queasy.number3  = t-article.dept
                queasy.logi1    = NO
                queasy.logi2    = YES
            .
        END.
    END.

    success-flag = YES.
END.
ELSE IF case-type EQ 4 THEN /*Deactive SoldOut Article*/
DO:
    FOR EACH t-article WHERE t-article.selected-art EQ YES AND t-article.sold-out EQ YES NO-LOCK:
        FIND FIRST queasy WHERE queasy.KEY EQ 222 
            AND queasy.number1 EQ 2
            AND queasy.number2 EQ t-article.artnr 
            AND queasy.number3 EQ t-article.dept
            AND t-article.sold-out EQ queasy.logi2 NO-LOCK NO-ERROR.
        IF AVAILABLE queasy THEN
        DO:
            FIND CURRENT queasy EXCLUSIVE-LOCK.
            queasy.logi2 = NO.
            FIND CURRENT queasy NO-LOCK.
        END.        
    END.

    success-flag = YES.
END.
