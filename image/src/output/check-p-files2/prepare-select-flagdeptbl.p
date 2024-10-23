DEF TEMP-TABLE dept-list
    FIELD deptnr      AS INTEGER FORMAT ">>9"   LABEL "No"
    FIELD bezeich     AS CHAR    FORMAT "x(26)" LABEL "Department"
    FIELD select-flag AS LOGICAL INIT NO        LABEL "Select"
.

DEF INPUT  PARAMETER inp-dept AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR dept-list.

RUN create-list.

PROCEDURE create-list:
DEF VAR curr-i   AS INTEGER NO-UNDO.
DEF VAR mesValue AS CHAR    NO-UNDO.

  FOR EACH queasy WHERE queasy.KEY = 19 NO-LOCK BY queasy.number1:
      CREATE dept-list.
      ASSIGN
          dept-list.deptnr  = queasy.number1
          dept-list.bezeich = queasy.char3
      .
  END.
  
  DO curr-i = 1 TO NUM-ENTRIES(inp-dept, ","):
     mesValue = ENTRY(curr-i, inp-dept, ",").
     IF mesValue NE "" THEN
     DO:
       FIND FIRST dept-list WHERE dept-list.deptnr = INTEGER(mesValue)
           NO-ERROR.
       IF AVAILABLE dept-list THEN dept-list.select-flag = YES.
     END.
  END.
END.
