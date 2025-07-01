
DEF INPUT PARAMETER case-type AS INT.
DEF INPUT PARAMETER int1 AS INT.
DEF INPUT PARAMETER int2 AS INT.
DEF INPUT PARAMETER int3 AS INT.
DEF INPUT PARAMETER char1 AS CHAR.
DEF INPUT PARAMETER word-exist AS LOGICAL.
DEF OUTPUT PARAMETER success-flag AS LOGICAL INIT NO.


CASE case-type:
    WHEN 1 THEN
    DO:
        IF NOT word-exist THEN 
        DO:
            CREATE briefzei.
            briefzei.briefnr = int1.
            briefzei.briefzeilnr = int2.
            FIND CURRENT briefzei.
        END.
        ELSE FIND FIRST briefzei WHERE briefzei.briefnr = int1 EXCLUSIVE-LOCK.
        
        briefzei.texte = char1.
        RELEASE briefzei.
        ASSIGN success-flag = YES.
    END.
END CASE.
