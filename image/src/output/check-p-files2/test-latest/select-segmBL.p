/**********  DEFINE TEMP TABLE **********/ 
DEFINE TEMP-TABLE segm-list 
  FIELD code    AS INTEGER LABEL "No" 
  FIELD name    AS CHAR FORMAT "x(10)" LABEL "Code"
  FIELD remark  AS CHAR FORMAT "x(24)" LABEL "Remark".

 
DEFINE OUTPUT PARAMETER TABLE FOR segm-list.

/**********  MAIN LOGIC  **********/ 
FOR EACH segment WHERE segment.betriebsnr LE 2 
  AND segment.vip-level = 0 AND NUM-ENTRIES(segment.bezeich, "$$0") = 1
  NO-LOCK BY segment.segmentcode: 
  CREATE segm-list. 
  ASSIGN
    segm-list.code   = segment.segmentcode
    segm-list.name   = segment.bezeich
    segm-list.remark = segment.bemerkung
  . 
END. 
