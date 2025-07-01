
DEF TEMP-TABLE t-nation
    FIELD bezeich LIKE nation.bezeich
    FIELD kurzbez LIKE nation.kurzbez.


DEF OUTPUT PARAMETER ci-date AS DATE.
DEF OUTPUT PARAMETER from-month AS CHAR.
DEF OUTPUT PARAMETER rm-serv AS LOGICAL.
DEF OUTPUT PARAMETER foreign-rate AS LOGICAL.
DEF OUTPUT PARAMETER ena-rmrev AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER TABLE FOR t-nation.

DEFINE VARIABLE tot-room     AS INTEGER. 
DEFINE VARIABLE inactive     AS INTEGER. 

for each nation  no-lock by nation.bezeich :    /*ozhan added */
    CREATE t-nation.
    ASSIGN t-nation.bezeich = nation.bezeich
           t-nation.kurzbez = nation.kurzbez.
end. 


FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK. 
ci-date = htparam.fdate. 
from-month = STRING(month(ci-date),"99") + STRING(year(ci-date),"9999"). 
 
FIND FIRST htparam WHERE htparam.paramnr = 128 NO-LOCK. 
rm-serv = NOT htparam.flogical. 

FIND FIRST htparam WHERE paramnr = 143 NO-LOCK. 
foreign-rate = htparam.flogical. 

RUN sum-rooms.

FIND FIRST htparam WHERE htparam.paramnr = 550 NO-LOCK.
IF htparam.feldtyp = 4 AND htparam.flogical THEN 
    /*MTENABLE show-rmrev WITH FRAME frame1.*/
    ena-rmrev = YES.

PROCEDURE sum-rooms: 
  tot-room = 0. 
  inactive = 0. 
  FOR EACH zimkateg WHERE zimkateg.verfuegbarkeit = YES NO-LOCK: 
    FOR EACH zimmer WHERE zimmer.zikatnr = zimkateg.zikatnr NO-LOCK: 
      IF sleeping THEN tot-room = tot-room + 1. 
      ELSE inactive = inactive + 1. 
    END. 
  END. 
END. 

