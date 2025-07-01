DEFINE TEMP-TABLE t-outorder  LIKE outorder.  
DEFINE TEMP-TABLE t-res-line  LIKE res-line.

DEFINE INPUT PARAMETER roomnumber AS CHAR.
DEFINE INPUT PARAMETER resnumber  AS INTEGER.
DEFINE INPUT PARAMETER fromdate   AS DATE.
DEFINE INPUT PARAMETER todate     AS DATE.

DEFINE OUTPUT PARAMETER roomno    AS CHARACTER.
DEFINE OUTPUT PARAMETER resno     AS INTEGER.
DEFINE OUTPUT PARAMETER resname   AS CHARACTER.
DEFINE OUTPUT PARAMETER from-date AS DATE.
DEFINE OUTPUT PARAMETER to-date   AS DATE.
DEFINE OUTPUT PARAMETER reason    AS CHARACTER.

RUN read-outorderbl.p (99, roomnumber, resnumber, fromdate, todate, OUTPUT TABLE t-outorder).  
RUN read-res-linebl.p (24, resnumber, ?,?,?, roomnumber, ?,?,?,?, "", OUTPUT TABLE t-res-line). 

FIND FIRST t-outorder.  
  roomno      = t-outorder.zinr.   
  from-date   = t-outorder.gespstart.   
  to-date     = t-outorder.gespende.   
  resno       = t-outorder.betriebsnr.
  IF t-outorder.gespgrund MATCHES "*$*" THEN reason = ENTRY(1,t-outorder.gespgrund,"$").
  ELSE reason  = t-outorder.gespgrund.

FIND FIRST t-res-line NO-ERROR.  
IF AVAILABLE t-res-line THEN resname = t-res-line.name.  

