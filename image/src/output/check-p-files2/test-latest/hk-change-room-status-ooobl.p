
DEFINE TEMP-TABLE bline-list   
  FIELD zinr AS CHAR   
  FIELD selected AS LOGICAL INITIAL NO   
  FIELD bl-recid AS INTEGER.   

DEFINE TEMP-TABLE t-bline-list LIKE bline-list.

DEFINE TEMP-TABLE room-list
  FIELD nr AS CHAR.

DEF TEMP-TABLE z-list
    FIELD zinr              LIKE zimmer.zinr
    FIELD setup             LIKE zimmer.setup
    FIELD zikatnr           LIKE zimmer.zikatnr
    FIELD etage             LIKE zimmer.etage
    FIELD zistatus          LIKE zimmer.zistatus
    FIELD CODE              LIKE zimmer.CODE
    FIELD bediener-nr-stat  LIKE zimmer.bediener-nr-stat
    FIELD checkout          AS LOGICAL INITIAL NO
    FIELD str-reason        AS CHAR
.

DEFINE TEMP-TABLE om-list 
  FIELD zinr AS CHAR 
  FIELD ind AS INTEGER INITIAL 0. 

DEF TEMP-TABLE t-zimkateg LIKE zimkateg.  

DEFINE TEMP-TABLE setup-list   
  FIELD nr AS INTEGER   
  FIELD CHAR AS CHAR FORMAT "x(1)".   

DEFINE INPUT PARAMETER pvILanguage AS INT.
DEFINE INPUT PARAMETER user-init      AS CHAR FORMAT "x(2)".  
DEFINE INPUT PARAMETER from-date AS DATE.
DEFINE INPUT PARAMETER to-date AS DATE.
DEFINE INPUT PARAMETER dept AS INT.
DEFINE INPUT PARAMETER reason AS CHAR.
DEFINE INPUT PARAMETER service-flag AS LOGICAL.
DEFINE INPUT PARAMETER TABLE FOR room-list.

DEFINE OUTPUT PARAMETER rec-id AS INTEGER.
DEFINE OUTPUT PARAMETER msg-str AS CHAR.

DEF VAR lvCAREA AS CHAR INITIAL "hk-change-room-status". 
{supertransBL.i} 


DEFINE VARIABLE t-zinr AS CHAR.
DEFINE VARIABLE t-zistatus AS INT INIT 0.
DEFINE VARIABLE ci-date AS DATE.
DEFINE VARIABLE flag AS INT INIT 0.


FOR EACH room-list:
  CREATE bline-list.
  bline-list.SELECTED = YES.
  bline-list.zinr = room-list.nr.
END.

RUN hk-statadmin-start-chgstatbl.p(4, TABLE bline-list,
    OUTPUT flag, OUTPUT t-zinr, OUTPUT t-zistatus).

IF flag EQ 4 THEN
DO:
  flag = 6.
END.

IF flag EQ 6 THEN
DO:
  RUN prepare-hk-statadminbl.p ("", 0, 0, 0,  
     OUTPUT ci-date, OUTPUT TABLE z-list, OUTPUT TABLE om-list,  
     OUTPUT TABLE t-bline-list, OUTPUT TABLE setup-list,  
     OUTPUT TABLE t-zimkateg).  

  FIND FIRST bediener WHERE bediener.userinit EQ user-init NO-LOCK NO-ERROR.

  RUN hk-statadmin-activate-ooobl.p (INPUT-OUTPUT TABLE bline-list, 
      INPUT-OUTPUT TABLE om-list,  
      pvILanguage, from-date, to-date, ci-date, dept,  
      reason, service-flag, bediener.nr, OUTPUT flag, OUTPUT msg-str,  
      OUTPUT TABLE z-list).  

  IF flag EQ 1 THEN
  DO:
    msg-str = translateExtended ("Overlapping O-O-O or O-M record found!",lvCAREA,"") + " " + STRING(bline-list.zinr). 
  END.
  ELSE
  DO:
    FIND FIRST room-list NO-LOCK NO-ERROR.
    IF AVAILABLE room-list THEN
    DO:
      FIND FIRST outorder WHERE
          outorder.zinr EQ room-list.nr AND
          outorder.gespstart EQ from-date AND
          outorder.gespende EQ to-date
          NO-LOCK NO-ERROR.
      IF AVAILABLE outorder THEN
      DO:
        rec-id = RECID(outorder).
      END.
    END.
  END.
END.
ELSE
DO:
  IF flag = 1 THEN  
  DO:   
    msg-str = translateExtended ("To change room status select room(s) first.",lvCAREA,"").
  END.   
  ELSE IF flag = 5 THEN  
  DO:  
      msg-str = translateExtended ("Status Changes not possible.",lvCAREA,""). 
  END.  

END.
