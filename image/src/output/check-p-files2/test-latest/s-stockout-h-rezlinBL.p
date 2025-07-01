
DEF TEMP-TABLE t-l-bestand LIKE l-bestand.
DEF TEMP-TABLE t-h-rezlin LIKE h-rezlin.

DEF INPUT PARAMETER p-artnr AS INT.
DEF INPUT PARAMETER curr-lager AS INT.
DEF OUTPUT PARAMETER TABLE FOR t-l-bestand.
DEF OUTPUT PARAMETER TABLE FOR t-h-rezlin.

FOR EACH h-rezlin WHERE h-rezlin.artnrrezept = p-artnr NO-LOCK:
    CREATE t-h-rezlin.
    BUFFER-COPY h-rezlin TO t-h-rezlin.
    IF NOT h-rezlin.recipe-flag THEN
    DO:
        FIND FIRST l-bestand WHERE l-bestand.lager-nr = curr-lager 
            AND l-bestand.artnr = h-rezlin.artnrlager NO-LOCK NO-ERROR.
        IF AVAILABLE l-bestand THEN
        DO:
            CREATE t-l-bestand.
            BUFFER-COPY l-bestand TO t-l-bestand.
        END.
    END.
END.
