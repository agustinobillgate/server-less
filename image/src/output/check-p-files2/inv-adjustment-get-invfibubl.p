DEF INPUT PARAMETER artnr AS INT.
DEF OUTPUT PARAMETER fibukonto AS CHAR.
DEF OUTPUT PARAMETER cost-alloc AS CHAR.
DEF OUTPUT PARAMETER flag AS LOGICAL INITIAL NO.

FIND FIRST l-artikel WHERE l-artikel.artnr EQ artnr NO-LOCK NO-ERROR.
IF AVAILABLE l-artikel THEN 
DO:
    IF l-artikel.fibukonto NE "00000000" 
        AND l-artikel.fibukonto NE "0000000000"
        AND l-artikel.fibukonto NE ""
        AND NOT l-artikel.fibukonto MATCHES "* *"
        THEN
    DO:    
        fibukonto = l-artikel.fibukonto.
        
        FIND FIRST gl-acct WHERE gl-acct.fibukonto EQ l-artikel.fibukonto NO-LOCK NO-ERROR.
        IF AVAILABLE gl-acct THEN
        DO:
            cost-alloc = gl-acct.bezeich.
        END.

        flag = YES.
    END. /* Frans: 15/12/2023 #881BFB */
    ELSE IF l-artikel.fibukonto EQ ""
        OR l-artikel.fibukonto EQ " " THEN
        DO: 
        fibukonto = "00000000".
        /*1112002 artno cek di db */

        FIND FIRST gl-acct WHERE gl-acct.fibukonto EQ l-artikel.fibukonto NO-LOCK NO-ERROR.
        IF AVAILABLE gl-acct THEN
        DO:
            cost-alloc = gl-acct.bezeich.
        END.

        flag = YES.
    END.
END.
     
     


