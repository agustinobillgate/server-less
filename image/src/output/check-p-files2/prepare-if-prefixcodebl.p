DEFINE TEMP-TABLE param-list LIKE parameters 
    FIELD recid-param AS INTEGER.
.

DEFINE INPUT PARAMETER zone AS CHAR NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR param-list.

FOR EACH parameters WHERE 
    parameters.progname = "interface" AND 
    parameters.section = "prefix" AND 
    parameters.varname = zone NO-LOCK BY parameters.vstring:

    CREATE param-list.
    BUFFER-COPY parameters TO param-list.
    ASSIGN param-list.recid-param = RECID(parameters).
END.
