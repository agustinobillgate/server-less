DEFINE TEMP-TABLE param-list LIKE parameters
    FIELD recid-param AS INTEGER
.

DEFINE INPUT PARAMETER curr-select AS CHAR NO-UNDO.
DEFINE INPUT PARAMETER zone        AS CHAR NO-UNDO.
DEFINE INPUT PARAMETER bezeich     AS CHAR NO-UNDO.
DEFINE INPUT PARAMETER recid-param AS INTEGER NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR param-list.

FOR EACH param-list:
    DELETE param-list.
END.

IF curr-select = "add" THEN DO:
    create parameters.
    RUN fill-new-parameters.
END.
ELSE IF curr-select = "chg" THEN DO:
    FIND FIRST parameters WHERE RECID(parameters) = recid-param.
    parameters.vstring = bezeich.
END.

FOR EACH parameters WHERE 
        parameters.progname = "interface" AND 
        parameters.section = "prefix" AND 
        parameters.varname = zone NO-LOCK BY parameters.vstring:

        CREATE param-list.
        BUFFER-COPY parameters TO param-list.
        ASSIGN param-list.recid-param = RECID(parameters).
END.


PROCEDURE fill-new-parameters: 
  ASSIGN 
    parameters.progname = "interface" 
    parameters.section = "prefix" 
    parameters.varname = zone 
    parameters.vstring = bezeich. 
END. 
