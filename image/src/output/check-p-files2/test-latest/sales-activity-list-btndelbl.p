DEFINE TEMP-TABLE output-list 
  FIELD outnr AS INTEGER FORMAT ">9" 
  FIELD act-str AS CHAR FORMAT "x(78)". 

DEFINE INPUT PARAMETER resnr AS INTEGER.
DEFINE INPUT PARAMETER counter-reason AS INTEGER.
DEFINE INPUT PARAMETER outnr AS INTEGER.
DEFINE INPUT PARAMETER TABLE FOR output-list.
DEFINE OUTPUT PARAMETER TABLE FOR output-list.

RUN reorg-outlist.

PROCEDURE create-outlist: 
DEFINE VARIABLE i AS INTEGER. 
  counter-reason = 0. 
  FOR EACH output-list : 
    DELETE output-list. 
  END. 
  DO i = 1 TO 18: 
    IF b-storno.grund[i] NE "" THEN 
    DO: 
      CREATE output-list. 
      ASSIGN 
        outnr = i 
        act-str = b-storno.grund[i]. 
      counter-reason = i. 
    END. 
  END. 
END. 
 
PROCEDURE reorg-outlist: 
DEF VAR i AS INTEGER.
  FOR EACH output-list NO-LOCK:
  FIND FIRST b-storno WHERE b-storno.bankettnr = resnr AND output-list.outnr EQ outnr NO-LOCK NO-ERROR.
  FIND CURRENT b-storno EXCLUSIVE-LOCK. 
  IF output-list.outnr < 18 THEN 
  DO i = (output-list.outnr + 1) TO 18: 
      b-storno.grund[i - 1] = b-storno.grund[i]. 
  END. 
  b-storno.grund[counter-reason] = "". 
  RUN create-outlist.   
  END.
END.
