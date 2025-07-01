DEF TEMP-TABLE t-zimkateg LIKE zimkateg.

DEF TEMP-TABLE t-z-list
    FIELD zinr              LIKE zimmer.zinr
    FIELD setup             LIKE zimmer.setup
    FIELD zikatnr           LIKE zimmer.zikatnr
    FIELD etage             LIKE zimmer.etage
    FIELD zistatus          LIKE zimmer.zistatus
    FIELD CODE              LIKE zimmer.CODE
    FIELD bediener-nr-stat  LIKE zimmer.bediener-nr-stat
    FIELD checkout          AS LOGICAL INITIAL NO
    FIELD str-reason        AS CHAR.

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
    FIELD id AS CHAR
    FIELD pic AS CHAR
.

DEFINE TEMP-TABLE om-list 
  FIELD zinr AS CHAR 
  FIELD ind AS INTEGER INITIAL 0. 

DEFINE TEMP-TABLE bline-list 
  FIELD zinr AS CHAR 
  FIELD selected AS LOGICAL INITIAL NO 
  FIELD bl-recid AS INTEGER. 

DEFINE TEMP-TABLE setup-list 
  FIELD nr AS INTEGER 
  FIELD CHAR AS CHAR FORMAT "x(1)". 

DEF OUTPUT PARAMETER ci-date AS DATE.
DEF OUTPUT PARAMETER TABLE FOR z-list.
DEF OUTPUT PARAMETER TABLE FOR om-list.
DEF OUTPUT PARAMETER TABLE FOR bline-list.
DEF OUTPUT PARAMETER TABLE FOR setup-list.
DEF OUTPUT PARAMETER TABLE FOR t-zimkateg.

RUN mobile-prepare-hk-statadminbl.p ("", 0, 0, 0,  
               OUTPUT ci-date, OUTPUT TABLE t-z-list, OUTPUT TABLE om-list,  
               OUTPUT TABLE bline-list, OUTPUT TABLE setup-list,  
               OUTPUT TABLE t-zimkateg).  

FOR EACH t-z-list:
  CREATE z-list.
  BUFFER-COPY t-z-list TO z-list.
  
  FIND FIRST queasy WHERE queasy.KEY EQ 196 AND
    queasy.date1 EQ ci-date AND
    entry(1,queasy.char1,";") EQ z-list.zinr NO-LOCK NO-ERROR.

  IF AVAILABLE queasy THEN
  DO:
    z-list.id = ENTRY(2,queasy.char1,";").
    FIND FIRST bediener WHERE bediener.userinit EQ z-list.id NO-LOCK NO-ERROR.
    IF AVAILABLE bediener THEN
    DO:
      z-list.pic = bediener.username.
    END.
  END.
END.
