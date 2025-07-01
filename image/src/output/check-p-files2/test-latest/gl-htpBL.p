DEFINE TEMP-TABLE t-htparam LIKE htparam.

DEFINE TEMP-TABLE htgrp 
  FIELD number AS INTEGER FORMAT ">>9" LABEL "Group" 
  FIELD bezeich AS CHAR FORMAT "x(36)" LABEL "Description". 

DEF INPUT  PARAMETER grpnr AS INT.
DEF OUTPUT PARAMETER TABLE FOR t-htparam.
DEF OUTPUT PARAMETER TABLE FOR htgrp.

RUN create-htgrp.
FOR EACH htgrp:
    RUN create-htparam.
END.

PROCEDURE create-htgrp: 
  DEFINE VARIABLE arr AS INTEGER EXTENT 20 INITIAL 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
     0, 0, 0, 158, 0, 0, 0, 0, 0]. 
  DEFINE VARIABLE i AS INTEGER. 
 
  IF grpnr = 20 THEN 
  DO: 
    arr[15] = 143. 
    arr[16] = 0. 
  END. 
  ELSE IF grpnr = 21 THEN 
  DO: 
    arr[15] = 144. 
    arr[16] = 0. 
  END. 
 
  DO i = 1 TO 20: 
    IF arr[i] NE 0 THEN 
    DO: 
      FIND FIRST paramtext WHERE txtnr = arr[i] NO-LOCK. 
      create htgrp. 
      htgrp.number = paramtext.number. 
      htgrp.bezeich = paramtext.ptexte. 
    END. 
  END. 
END. 
 
PROCEDURE create-htparam:
    FOR EACH htparam WHERE paramgr = htgrp.number NO-LOCK:
        CREATE t-htparam.
        BUFFER-COPY htparam TO t-htparam.
    END.
END.
