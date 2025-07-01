
DEF INPUT PARAMETER case-type AS CHAR.

DEF INPUT PARAMETER int1  AS INT.
DEF OUTPUT PARAMETER char1 AS CHAR.

IF case-type EQ "btn-insert" THEN
DO :
    FIND FIRST briefzei WHERE briefzei.briefnr = int1 
      AND briefzei.briefzeilnr = 1 NO-LOCK NO-ERROR. 
    IF AVAILABLE briefzei THEN char1 = briefzei.texte.
END.
ELSE IF case-type EQ "btn-glmain" THEN
DO:
    FIND FIRST gl-main WHERE gl-main.nr = int1 NO-LOCK.
    char1 = STRING(gl-main.code).
END.
