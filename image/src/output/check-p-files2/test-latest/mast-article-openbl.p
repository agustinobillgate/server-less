DEFINE TEMP-TABLE bill1 LIKE bill.  

DEFINE INPUT PARAMETER resnr            AS INTEGER.
DEFINE INPUT PARAMETER gastnrpay        AS INTEGER.
DEFINE INPUT PARAMETER bill-receiver    AS CHARACTER.
DEFINE OUTPUT PARAMETER success         AS LOGICAL  NO-UNDO INITIAL NO.

RUN read-billbl.p(2, ?, resnr, 0, ?, OUTPUT TABLE bill1).  
FIND FIRST bill1 NO-ERROR.   
IF AVAILABLE bill1 AND bill1.gastnr NE gastnrpay THEN   
DO:   
  ASSIGN  
    bill1.gastnr = gastnrpay   
    bill1.name = bill-receiver  
  .   
  RUN write-bill2bl.p(INPUT TABLE bill1, OUTPUT success).  
END.   
