DEFINE TEMP-TABLE s-list 
  FIELD nr AS INTEGER.

DEFINE TEMP-TABLE htp-list  LIKE htparam.

DEFINE TEMP-TABLE htgrp 
  FIELD number AS INTEGER FORMAT ">>9" LABEL "Group" 
  FIELD bezeich AS CHAR FORMAT "x(36)" LABEL "Description". 


DEFINE TEMP-TABLE htp 
  FIELD reihenfolge AS INTEGER 
  FIELD number AS INTEGER FORMAT ">>>9" LABEL "No" 
  FIELD bezeich AS CHAR FORMAT "x(46)" LABEL "Description" 
  FIELD typ AS INTEGER 
  FIELD logv AS LOGICAL 
  FIELD lupdate AS DATE LABEL "Chg Date " 
  FIELD note AS CHAR FORMAT "x(14)" LABEL "Changed By" 
  FIELD wert AS CHAR FORMAT "x(32)" LABEL "Value". 

DEF OUTPUT PARAMETER rest-flag AS LOGICAL.
DEF OUTPUT PARAMETER TABLE FOR s-list.
DEF OUTPUT PARAMETER TABLE FOR htp.
DEF OUTPUT PARAMETER TABLE FOR htgrp.
DEF OUTPUT PARAMETER TABLE FOR htp-list.

DEFINE VARIABLE fl-assign AS LOGICAL INIT NO.
DEFINE VARIABLE gnr AS INTEGER INITIAL 31.
DEFINE VARIABLE anz-htp AS INTEGER INITIAL 70.
DEFINE VARIABLE arr AS INTEGER EXTENT 31 INITIAL 
    [124, 126, 128, 129, 130, 131, 132, 133, 136, 137, 
     138,   0, 140, 141, 142, 143, 144, 146, 147, 148, 
     149, 150, 151, 152, 153, 161, 158, 159, 125, 160, 162]. 

DEFINE VARIABLE htp-arr AS INTEGER EXTENT 70 INITIAL 
  [318,84,87,592,117,119,120,121,124,1001,47,97,137,139,146, 
   159,166,218,226,250,391,559,677,1108,48,125,130,131,145,149, 
   150,151,154,156,157,158,198,227,228,229,241,255,264,270,478, 
   295,162,233,260,265,302,113,114,115,76,434,435,440,441,442, 
   587,1116,2313,2315,273,143,144,377,0,0]. 

FIND FIRST htparam WHERE paramnr = 996 no-lock.   /* VHP Front multi user */ 
IF NOT htparam.flogical THEN 
DO: 
  FIND FIRST htparam WHERE paramnr = 1015 no-lock.   /* VHP Lite */ 
  IF NOT htparam.flogical THEN 
  DO: 
    FIND FIRST htparam WHERE paramnr = 990 no-lock.   /* Rest License */ 
    IF htparam.flogical THEN 
    DO:
      DEFINE VARIABLE i AS INTEGER. 
      rest-flag = YES. 
      arr[9]  = 0.  /* Interface */ 
      arr[14] = 0.  /* VIP AND Black List */ 
      arr[16] = 0.  /* Fix Asset */ 
      arr[18] = 0.  /* Banquet */ 
      arr[19] = 0.  /* Key Card */ 
      arr[20] = 0.  /* sales */ 
      DO i = 1 TO anz-htp: 
        IF htp-arr[i] NE 0 THEN 
        DO:
          CREATE s-list.
          s-list.nr = htp-arr[i].
        END. 
      END.
    END. 
  END. 
END. 


FIND FIRST htparam WHERE paramnr = 981 NO-LOCK. 
IF NOT htparam.flogical THEN arr[19] = 0.

RUN create-htgrp.

FIND FIRST htgrp NO-ERROR.
IF AVAILABLE htgrp AND htgrp.number NE 10 AND htgrp.number NE 99 
    AND htgrp.number NE 100 THEN RUN create-htp(htgrp.number).

RUN create-htplist.

PROCEDURE create-htplist:
  FOR EACH htparam WHERE htparam.paramgr = 40 NO-LOCK:
      CREATE htp-list.
      BUFFER-COPY htparam TO htp-list.
  END.
END.

PROCEDURE create-htgrp: 
  DEFINE VARIABLE i AS INTEGER. 

  FIND FIRST paramtext WHERE txtnr = 161 NO-LOCK NO-ERROR.
  IF NOT AVAILABLE paramtext THEN
  DO:
      CREATE paramtext.
      ASSIGN
          paramtext.txtnr   = 161
          paramtext.number  = 35
          paramtext.ptexte = "Centralized Mgmt Reporting System"
      .
  END.

  DO i = 1 TO gnr: 
    IF arr[i] NE 0 THEN 
    DO: 
      FIND FIRST paramtext WHERE paramtext.txtnr = arr[i] NO-LOCK NO-ERROR.
      IF AVAILABLE paramtext THEN
      DO:
        CREATE htgrp. 
        ASSIGN
          htgrp.number  = paramtext.number 
          htgrp.bezeich = paramtext.ptexte
        . 
      END.
    END. 
  END. 
END. 


PROCEDURE create-htp: 
  DEFINE INPUT PARAMETER i AS INTEGER. 
  DEFINE VARIABLE passwd-ok AS LOGICAL INITIAL YES. 
  DEFINE VARIABLE do-it AS LOGICAL. 
  FOR EACH htp: 
    DELETE htp. 
  END. 
  
  DO: 
    FOR EACH htparam WHERE htparam.paramgr = i NO-LOCK 
      BY htparam.paramnr: 
      do-it = YES. 
      IF rest-flag THEN 
      DO: 
        FIND FIRST s-list WHERE s-list.nr = htparam.paramnr NO-ERROR. 
        IF AVAILABLE s-list THEN do-it = NO. 
      END. 
      IF do-it THEN 
      DO: 
        CREATE htp. 
        ASSIGN
          htp.reihenfolge = htparam.reihenfolge
          htp.number      = htparam.paramnr
          htp.bezeich     = htparam.bezeich 
          htp.lupdate     = htparam.lupdate 
          htp.note        = htparam.fdefault
        . 
        IF feldtyp = 1 THEN htp.wert = STRING(htparam.finteger). 
        ELSE IF feldtyp = 2 THEN htp.wert = STRING(htparam.fdecimal). 
        ELSE IF feldtyp = 3 THEN htp.wert = STRING(htparam.fdate). 
        ELSE IF feldtyp = 4 THEN 
        DO: 
          htp.wert = STRING(htparam.flogical). 
          htp.logv = htparam.flogical. 
        END. 
        ELSE IF feldtyp = 5 THEN htp.wert = STRING(htparam.fchar). 
        htp.typ = htparam.feldtyp. 
      END. 
    END. 
  END.
  /*MTIF i = 8 OR i = 17 OR i = 30 OR i = 39 THEN 
  DO: 
      ASSIGN 
          intval:READ-ONLY IN FRAME frame1 = TRUE 
          decval:READ-ONLY IN FRAME frame1 = TRUE 
          dateval:READ-ONLY IN FRAME frame1 = TRUE 
          logval:READ-ONLY IN FRAME frame1 = TRUE 
          charval:READ-ONLY IN FRAME frame1 = TRUE 
      . 
  END. 
  ELSE DO: 
      ASSIGN 
          intval:READ-ONLY IN FRAME frame1 = FALSE 
          decval:READ-ONLY IN FRAME frame1 = FALSE 
          dateval:READ-ONLY IN FRAME frame1 = FALSE 
          logval:READ-ONLY IN FRAME frame1 = FALSE 
          charval:READ-ONLY IN FRAME frame1 = FALSE 
      . 
  END. */
END.

