
DEFINE INPUT PARAMETER from-month   AS CHARACTER.
DEFINE INPUT PARAMETER ci-date      AS DATE.
DEFINE INPUT PARAMETER diff-one     AS INTEGER.
DEFINE OUTPUT PARAMETER msgLogi     AS LOGICAL INITIAL YES.

DEFINE VARIABLE mm1 AS INTEGER. 
DEFINE VARIABLE yy1 AS INTEGER. 

mm1 = INTEGER(SUBSTR(from-month,1,2)) + diff-one. 
yy1 = INTEGER(SUBSTR(from-month,3,4)). 
IF mm1 = 0 THEN 
DO: 
    mm1 = 12. 
    yy1 = yy1 - 1. 
END. 
IF (yy1 GT year(ci-date)) 
    OR ((year(ci-date) = yy1) AND (mm1 GT month(ci-date))) THEN msgLogi = NO. 
