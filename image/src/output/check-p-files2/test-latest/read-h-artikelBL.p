DEF TEMP-TABLE t-artikel LIKE h-artikel.

DEF INPUT  PARAMETER case-type  AS INTEGER  NO-UNDO.
DEF INPUT  PARAMETER artNo      AS INTEGER  NO-UNDO.
DEF INPUT  PARAMETER dept       AS INTEGER  NO-UNDO.
DEF INPUT  PARAMETER aName      AS CHAR     NO-UNDO.
DEF INPUT  PARAMETER artart     AS INTEGER  NO-UNDO.
DEF INPUT  PARAMETER betriebsNo AS INTEGER  NO-UNDO.
DEF INPUT  PARAMETER actFlag    AS LOGICAL  NO-UNDO.
DEF OUTPUT PARAMETER TABLE FOR t-artikel.

CASE case-type :
    WHEN 1 THEN DO:
        IF artNo NE 0 THEN
            FIND FIRST h-artikel WHERE h-artikel.artnr = artNo 
            AND h-artikel.departement = dept NO-LOCK NO-ERROR.
        ELSE IF aName NE "" THEN
            FIND FIRST h-artikel WHERE h-artikel.bezeich = aName 
            AND h-artikel.departement = dept NO-LOCK NO-ERROR.
        IF AVAILABLE h-artikel THEN RUN cr-artikel.
    END.
    WHEN 2 THEN
    DO:
        FIND FIRST h-artikel WHERE h-artikel.departement = dept 
            AND h-artikel.bezeich = aName 
            AND h-artikel.artnr NE artNo NO-LOCK NO-ERROR.
        IF AVAILABLE h-artikel THEN RUN cr-artikel.
    END.
    
END CASE.

PROCEDURE cr-artikel :
    CREATE t-artikel.
    BUFFER-COPY h-artikel TO t-artikel.
END.
