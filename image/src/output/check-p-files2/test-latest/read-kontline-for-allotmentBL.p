DEFINE TEMP-TABLE t-kontline LIKE kontline.

DEFINE INPUT PARAMETER case-type AS INTEGER NO-UNDO.
DEF INPUT PARAMETER gastNo       AS INTEGER NO-UNDO.
DEF INPUT PARAMETER kontigNr     AS INTEGER NO-UNDO.
DEF INPUT PARAMETER kontcode     AS CHAR    NO-UNDO.
DEF INPUT PARAMETER katnr        AS INTEGER NO-UNDO.
DEF INPUT PARAMETER argt         AS CHAR    NO-UNDO.
DEF INPUT PARAMETER erwachs      AS INTEGER NO-UNDO.
DEF INPUT PARAMETER abreise      AS DATE    NO-UNDO.
DEF INPUT PARAMETER ankunft      AS DATE    NO-UNDO.
DEF OUTPUT PARAMETER TABLE FOR t-kontline.


CASE case-type:
    WHEN 1 THEN
    DO:
        FIND FIRST kontline WHERE kontline.gastnr = gastNo AND 
        kontline.kontignr NE kontigNr 
        AND kontline.kontcode = kontcode 
        AND kontline.kontstat = 1 
        AND ((kontline.zikatnr NE katnr) OR (kontline.arrangement NE argt) OR 
        (kontline.erwachs NE erwachs)) 
        NO-LOCK NO-ERROR. 
        IF AVAILABLE kontline THEN
        DO:
            CREATE t-kontline.
            BUFFER-COPY kontline TO t-kontline.
        END.
    END.

    WHEN 2 THEN
    DO:
        FIND FIRST kontline WHERE kontline.gastnr = gastNo AND 
        kontline.kontignr NE kontigNr 
        AND kontline.kontcode EQ kontcode 
        AND kontline.kontstat = 1 
        AND NOT kontline.ankunft GE abreise 
        AND NOT kontline.abreise LE ankunft 
        NO-LOCK NO-ERROR. 
        IF AVAILABLE kontline THEN
        DO:
            CREATE t-kontline.
            BUFFER-COPY kontline TO t-kontline.
        END.
    END.
END CASE.
