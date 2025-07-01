
DEFINE INPUT PARAMETER diff-one AS INTEGER.
DEFINE INPUT-OUTPUT PARAMETER from-month AS CHARACTER.

DEFINE VARIABLE mm AS INTEGER. 
DEFINE VARIABLE yy AS INTEGER. 
DEFINE VARIABLE curr-date AS DATE. 

mm = INTEGER(SUBSTR(from-month,1,2)) + diff-one. 
yy = INTEGER(SUBSTR(from-month,3,4)). 

IF diff-one = 1 AND mm = 13 THEN 
DO: 
    mm = 1. 
    yy = yy + 1. 
END. 
ELSE IF diff-one = -1 AND mm = 0 THEN 
DO: 
    mm = 12. 
    yy = yy - 1. 
END. 
curr-date = DATE(mm, 1, yy). 
from-month = STRING(month(curr-date),"99") + STRING(year(curr-date),"9999").

