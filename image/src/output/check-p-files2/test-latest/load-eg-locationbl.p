DEFINE TEMP-TABLE t-eg-location LIKE eg-location
    FIELD rec-id AS INTEGER.

DEFINE INPUT PARAMETER case-type AS INTEGER.
DEFINE OUTPUT PARAMETER TABLE FOR t-eg-location.

IF case-type = 1 THEN
DO:
    FOR EACH eg-location NO-LOCK:
        CREATE t-eg-location.
        BUFFER-COPY eg-location TO t-eg-location.
        ASSIGN t-eg-location.rec-id = RECID(eg-location).
    END.    
END.
