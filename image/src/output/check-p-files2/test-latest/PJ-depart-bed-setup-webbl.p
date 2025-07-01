
DEFINE TEMP-TABLE t-paramtext LIKE paramtext.    
DEFINE TEMP-TABLE setup-list 
  FIELD nr          AS INTEGER 
  FIELD CHAR        AS CHAR FORMAT "x(1)". 

DEFINE OUTPUT PARAMETER TABLE FOR setup-list.

DEFINE VARIABLE p-text AS CHAR INITIAL "" NO-UNDO.

CREATE setup-list. 
setup-list.nr = 1. 
setup-list.char = " ". 

RUN read-paramtextbl.p(3, 9201, OUTPUT p-text, OUTPUT TABLE t-paramtext).
FOR EACH t-paramtext : 
    CREATE setup-list. 
    ASSIGN
        setup-list.nr = t-paramtext.txtnr - 9199 
        setup-list.char = SUBSTR(t-paramtext.notes,1,1). 
END.

