
DEF TEMP-TABLE t-arrangement LIKE arrangement
    FIELD waehrungsnr AS CHAR.

DEF OUTPUT PARAMETER TABLE FOR t-arrangement.

DEFINE BUFFER waehrung1    FOR waehrung. 

FOR EACH arrangement WHERE arrangement.segmentcode = 0
     NO-LOCK BY arrangement.argtnr:
     CREATE t-arrangement.
     BUFFER-COPY arrangement TO t-arrangement.

     FIND FIRST waehrung1 WHERE waehrung1.waehrungsnr = arrangement.betriebsnr 
         NO-LOCK.
     ASSIGN t-arrangement.waehrungsnr = waehrung1.bezeich.
END.
