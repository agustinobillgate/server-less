
DEFINE TEMP-TABLE bline-list   
  FIELD zinr AS CHAR   
  FIELD selected AS LOGICAL INITIAL NO   
  FIELD bl-recid AS INTEGER.   

DEFINE TEMP-TABLE t-bline-list 
  FIELD zinr AS CHAR   
  FIELD selected AS LOGICAL INITIAL NO   
  FIELD bl-recid AS INTEGER.   

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
DEFINE INPUT PARAMETER chgsort AS INT.
DEFINE INPUT PARAMETER user-init      AS CHAR FORMAT "x(2)".  
DEFINE INPUT PARAMETER TABLE FOR room-list.

DEFINE OUTPUT PARAMETER msg-str AS CHAR.

DEF VAR lvCAREA AS CHAR INITIAL "hk-change-room-status". 
{supertransBL.i} 


DEFINE VARIABLE t-zinr AS CHAR.
DEFINE VARIABLE t-zistatus AS INT INIT 0.
DEFINE VARIABLE ci-date AS DATE.
DEFINE VARIABLE curr-zinr AS CHAR.
DEFINE VARIABLE curr-stat AS CHAR.
DEFINE VARIABLE flag AS INT INIT 0.


IF chgsort NE 4 AND chgsort NE 5 THEN
DO:
  FOR EACH room-list:
    CREATE bline-list.
    bline-list.SELECTED = YES.
    bline-list.zinr = room-list.nr.
  END.

  RUN hk-statadmin-start-chgstatbl.p(chgsort, TABLE bline-list,
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
    
    IF t-zistatus EQ 6 THEN
    DO:
      IF chgsort EQ 4 THEN
      DO:
        msg-str = translateExtended ("Status Changes not possible.",lvCAREA,"").
      END.
      ELSE
      DO:
        RUN hk-statadmin-deactivate-ooobl.p  (INPUT-OUTPUT TABLE bline-list,  
               INPUT-OUTPUT TABLE om-list, ci-date, bediener.nr, chgsort,  
               OUTPUT TABLE z-list).  

      END.
    END.
    ELSE
    DO:
      RUN hk-statadmin-chg-zistatusbl.p 
        (INPUT-OUTPUT TABLE bline-list, INPUT-OUTPUT TABLE om-list,  
          0, ci-date, chgsort, "", user-init, bediener.nr,  
          OUTPUT curr-zinr, OUTPUT curr-stat, OUTPUT TABLE z-list).  

    END.
  END.
  ELSE
  DO:
    IF flag = 1 THEN  
    DO:   
      msg-str = translateExtended ("To change room status select room(s) first.",lvCAREA,"").
    END.   
    ELSE IF flag = 2 THEN  
    DO:   
      msg-str = translateExtended ("Set back DO NOT DISTURB to status dirty.",lvCAREA,"").   
    END.   
    ELSE IF flag = 3 THEN  
    DO:   
      msg-str = translateExtended ("DO NOT DISTURB is for Occupied Dirty Rooms only.",lvCAREA,"").
    END.   
    ELSE IF flag = 5 THEN  
    DO:  
        msg-str = translateExtended ("Status Changes not possible.",lvCAREA,""). 
    END.  

  END.

END.
