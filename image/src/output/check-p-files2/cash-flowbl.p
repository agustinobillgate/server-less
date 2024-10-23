
DEFINE TEMP-TABLE t-cflow  LIKE queasy.
DEFINE OUTPUT PARAMETER TABLE FOR t-cflow.
FOR EACH  queasy WHERE queasy.KEY = 177 NO-LOCK:
   /*DISP queasy.char1 FORMAT "x(20)".*/     
     CREATE t-cflow.    
    BUFFER-COPY queasy TO t-cflow.
    IF queasy.number1 NE 0 THEN ASSIGN t-cflow.deci1 = queasy.number1.
END.
