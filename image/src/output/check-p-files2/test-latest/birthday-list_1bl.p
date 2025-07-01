DEFINE TEMP-TABLE s-list 
  FIELD gastnr  AS INTEGER 
  FIELD NAME    AS CHAR FORMAT "x(32)" LABEL "Name" 
  FIELD zinr    LIKE zimmer.zinr COLUMN-LABEL "RmNo" 
  FIELD bdate   AS DATE LABEL "Birthday Date" FORMAT "99/99/9999"
  FIELD resstat AS CHAR FORMAT "x(12)" LABEL "Status" 
  FIELD abreise AS DATE LABEL "Departure". 

DEFINE INPUT PARAMETER pvILanguage      AS INTEGER         NO-UNDO.
DEFINE OUTPUT PARAMETER bday-available  AS LOGICAL INIT NO.
DEFINE OUTPUT PARAMETER TABLE FOR s-list.

{supertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "birthday-list". 

RUN create-list.

PROCEDURE create-list: 
DEF BUFFER sbuff FOR s-list.  
  FOR EACH res-line WHERE res-line.active-flag = 0 AND 
      (res-line.resstatus LE 5 OR res-line.resstatus = 11) 
      AND res-line.ankunft = TODAY NO-LOCK, 
      FIRST guest WHERE guest.gastnr = res-line.gastnrmember 
      /*MTAND MONTH(guest.geburtdatum1) = MONTH(TODAY) 
      AND DAY(guest.geburtdatum1) = DAY(TODAY) 
      */
      AND 
      (
          (MONTH(guest.geburtdatum1) = MONTH(TODAY) AND DAY(guest.geburtdatum1) = DAY(TODAY))
          OR
          (MONTH(guest.geburtdatum1) = MONTH(TODAY) AND DAY(guest.geburtdatum1) = (DAY(TODAY)) + 1)
      )
      NO-LOCK BY guest.NAME 
      BY res-line.zinr: 
      FIND FIRST sbuff WHERE sbuff.gastnr = guest.gastnr NO-ERROR. 
      IF NOT AVAILABLE sbuff THEN 
      DO: 
        CREATE s-list. 
        ASSIGN 
          s-list.gastnr  = guest.gastnr 
          s-list.NAME    = res-line.NAME 
          s-list.zinr    = res-line.zinr 
          s-list.bdate   = DATE(MONTH(guest.geburtdatum1), DAY(guest.geburtdatum1), YEAR(guest.geburtdatum1))
          s-list.resstat = translateExtended ("Arrival",lvCAREA,"") 
          s-list.abreise = res-line.abreise. 
        bday-available = YES.
      END. 
  END. 
  FOR EACH res-line WHERE res-line.active-flag = 1 AND 
      (res-line.resstatus EQ 6 OR res-line.resstatus = 13) NO-LOCK, 
      FIRST guest WHERE guest.gastnr = res-line.gastnrmember 
      /*MTAND MONTH(guest.geburtdatum1) = MONTH(TODAY) 
      AND DAY(guest.geburtdatum1) = DAY(TODAY) 
      */
      AND 
      (
          (MONTH(guest.geburtdatum1) = MONTH(TODAY) AND DAY(guest.geburtdatum1) = DAY(TODAY))
          OR
          (MONTH(guest.geburtdatum1) = MONTH(TODAY) AND DAY(guest.geburtdatum1) = (DAY(TODAY)) + 1)
      )
      
      NO-LOCK BY guest.NAME 
      BY res-line.zinr: 
      FIND FIRST sbuff WHERE sbuff.gastnr = guest.gastnr 
          AND sbuff.resstat = "Inhouse" NO-ERROR. 
      IF NOT AVAILABLE sbuff THEN 
      DO: 
        CREATE s-list. 
        ASSIGN 
          s-list.gastnr  = guest.gastnr 
          s-list.NAME    = res-line.NAME 
          s-list.zinr    = res-line.zinr 
          s-list.bdate   = DATE(MONTH(guest.geburtdatum1), DAY(guest.geburtdatum1), YEAR(guest.geburtdatum1))
          s-list.resstat = translateExtended ("Inhouse",lvCAREA,"") 
          s-list.abreise = res-line.abreise. 
        bday-available = YES.

      END. 
  END. 
END. 
