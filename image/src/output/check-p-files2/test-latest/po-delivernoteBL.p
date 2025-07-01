DEFINE TEMP-TABLE delivernote-list
    FIELD datum     LIKE l-ophdr.datum 
    FIELD lager-nr  LIKE l-ophdr.lager-nr 
    FIELD docu-nr   LIKE l-ophdr.docu-nr 
    FIELD lscheinnr LIKE l-ophdr.lscheinnr.

DEFINE INPUT PARAMETER docu-nr  AS CHAR NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR delivernote-list.


FOR EACH l-ophdr WHERE l-ophdr.op-typ = "STI" AND l-ophdr.docu-nr = docu-nr 
    NO-LOCK BY l-ophdr.lager-nr. 
    CREATE delivernote-list.
    BUFFER-COPY l-ophdr TO delivernote-list.
END.
