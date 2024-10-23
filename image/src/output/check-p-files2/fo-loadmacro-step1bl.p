DEFINE TEMP-TABLE brief-list 
  FIELD b-text AS CHAR. 

DEFINE TEMP-TABLE art-list 
  FIELD str-art AS CHAR
  FIELD anzahl  AS INT INIT 0.

DEFINE INPUT PARAMETER briefnr AS INT.
DEFINE OUTPUT PARAMETER TABLE FOR art-list.

DEFINE VARIABLE n           AS INTEGER. 
DEFINE VARIABLE l           AS INTEGER. 
DEFINE VARIABLE continued   AS LOGICAL INITIAL NO. 
DEFINE VARIABLE c           AS CHAR. 
DEFINE VARIABLE ct          AS CHAR.
DEFINE VARIABLE i           AS INTEGER. 
DEFINE VARIABLE j           AS INTEGER. 

DEFINE BUFFER parambuff FOR parameters.

FOR EACH briefzei WHERE briefzei.briefnr = briefnr 
    NO-LOCK BY briefzei.briefzeilnr: 
    j = 1. 
    DO i = 1 TO LENGTH(briefzei.texte): 
       IF ASC(SUBSTR(briefzei.texte, i , 1)) EQ 10 THEN 
       DO: 
         n = i - j. 
         c = SUBSTR(briefzei.texte, j,  n). 
         l = LENGTH(c). 
         IF NOT continued THEN CREATE brief-list. 
         brief-list.b-text = brief-list.b-text + c. 
         j = i + 1. 
       END. 
    END. 
    n = LENGTH(briefzei.texte) - j + 1. 
    c = SUBSTR(briefzei.texte, j,  n). 
    IF NOT continued THEN CREATE brief-list. 
    b-text = b-text + c. 
END.

FIND FIRST art-list NO-ERROR.
IF NOT AVAILABLE art-list THEN
  FOR EACH brief-list NO-LOCK:
    IF b-text = "" OR SUBSTR(b-text,1,1) = "#" THEN.
    ELSE
    DO:
      CREATE art-list.
      DO i = 1 TO NUM-ENTRIES(b-text," "):
        IF SUBSTR(ENTRY(i,b-text," "),1,1) = "^" THEN
          ASSIGN
            art-list.str-art = ENTRY(i,b-text," ")
            art-list.anzahl = 0.
      END.
    END.
  END.
ELSE
FOR EACH art-list WHERE art-list.anzahl NE 0:
  art-list.anzahl = 0.
END.

FIND FIRST parameters WHERE
  parameters.progname            = "FO-Macro"      AND
  parameters.SECTION             = STRING(briefnr) 
  NO-LOCK NO-ERROR.
DO WHILE AVAILABLE parameters:
  DO TRANSACTION:
    FIND FIRST parambuff WHERE RECID(parambuff) = RECID(parameters).
    DELETE parambuff.
  END.
  FIND NEXT parameters WHERE
    parameters.progname   = "FO-Macro"      AND
    parameters.SECTION    = STRING(briefnr)
    NO-LOCK NO-ERROR.
END.
