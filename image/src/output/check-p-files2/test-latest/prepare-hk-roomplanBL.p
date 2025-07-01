DEFINE TEMP-TABLE room-list   
  FIELD zistatus    AS INTEGER   
  FIELD ststr       AS CHAR FORMAT "x(2)" LABEL "St"   
  FIELD build       AS CHAR FORMAT "x(40)"   
  FIELD build-flag  AS CHAR FORMAT "x(1)"  LABEL "P"   
  FIELD recid1      AS INTEGER EXTENT 17   
  FIELD etage       AS INTEGER FORMAT "99 " LABEL "FL "   
  FIELD zinr        AS CHAR FORMAT "x(5)" LABEL "RmNo"   
  FIELD c-char      AS CHAR FORMAT "x(2)" LABEL " C"   
  FIELD i-char      AS CHAR FORMAT "x(2)" LABEL " I"   
  FIELD zikatnr     AS INTEGER   
  FIELD rmcat       AS CHAR FORMAT "x(5)" LABEL "RmCat"   
  FIELD connec      AS CHAR FORMAT "x(5)" LABEL "Cnec"   
  FIELD avtoday     AS CHAR FORMAT "x(2)" LABEL ""   
  FIELD gstatus     AS INTEGER EXTENT 17   
  FIELD bcol        AS INTEGER EXTENT 17 INITIAL 0   
  FIELD fcol        AS INTEGER EXTENT 17 INITIAL 0   
  FIELD room        AS CHAR EXTENT 17 FORMAT "x(5)"  
  INDEX zinr_ix zinr.  
  
DEF INPUT  PARAMETER from-room AS CHAR.  
DEF OUTPUT PARAMETER curr-date AS DATE.  
DEF OUTPUT PARAMETER TABLE FOR room-list.  
  
FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK.   
curr-date  = htparam.fdate.  
  
RUN hk-roomplan-create-browsebl.p(NO, from-room, curr-date, curr-date, OUTPUT TABLE room-list).  
