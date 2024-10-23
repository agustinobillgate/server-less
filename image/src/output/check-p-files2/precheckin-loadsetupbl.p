DEFINE TEMP-TABLE pci-setup
    FIELD number1         AS INT FORMAT ">>"         LABEL "GRP"
    FIELD number2         AS INT FORMAT ">>"         LABEL "SGRP"
    FIELD descr           AS CHAR    FORMAT "x(35)"  LABEL "DESCRIPTION"
    FIELD setupvalue      AS CHAR    FORMAT "x(84)"  LABEL "SETUP VALUE"
    FIELD setupflag       AS LOGICAL                 LABEL "FLAG"
    FIELD price           AS DECIMAL                 LABEL "DECIMAL VALUE"
    FIELD remarks         AS CHAR
    .

DEFINE TEMP-TABLE t-queasy LIKE queasy.
DEF TEMP-TABLE t-nation1 LIKE nation.
DEF TEMP-TABLE t-nation  LIKE nation
    FIELD marksegm AS CHAR
    FIELD rec-id AS INT.
DEF TEMP-TABLE t-subnation  LIKE nation.
DEFINE INPUT PARAMETER icase AS INT.
DEFINE OUTPUT PARAMETER TABLE FOR pci-setup.

DEFINE VARIABLE htl-name      AS CHAR.
/* DEFINE VARIABLE icase AS INT INIT 2. */

IF icase EQ 1 THEN
DO:
    FOR EACH queasy WHERE queasy.KEY = 216 NO-LOCK:
        CREATE pci-setup.
        ASSIGN 
          pci-setup.number1         = queasy.number1  
          pci-setup.number2         = queasy.number2  
          pci-setup.descr           = queasy.char1
          pci-setup.setupflag       = queasy.logi1
          pci-setup.setupvalue      = queasy.char3
          pci-setup.price           = queasy.deci1
          pci-setup.remarks         = queasy.char2
        .
    END.
END.
ELSE IF icase EQ 2 THEN
DO:
    FOR EACH queasy WHERE queasy.KEY = 216 AND queasy.logi1 EQ YES NO-LOCK:
        CREATE pci-setup.
        ASSIGN 
          pci-setup.number1         = queasy.number1  
          pci-setup.number2         = queasy.number2  
          pci-setup.descr           = queasy.char1
          pci-setup.setupflag       = queasy.logi1
          pci-setup.setupvalue      = queasy.char3
          pci-setup.price           = queasy.deci1
          pci-setup.remarks         = queasy.char2
        .
    END.
END.

/*LOAD TYPE OF DOCUMENT*/
RUN read-queasybl.p (3, 27, ?, "", OUTPUT TABLE t-queasy).
FOR EACH t-queasy:
    CREATE pci-setup.
    ASSIGN 
        pci-setup.number1         = 9  
        pci-setup.number2         = 0 
        pci-setup.descr           = "TYPE OF DOCUMENT"
        pci-setup.setupflag       = YES
        pci-setup.setupvalue      = t-queasy.char1
        .
END.

/*LOAD DEFAULT COUNTRY CODE*/
DEF VAR country AS CHAR.
FIND FIRST htparam WHERE htparam.paramnr EQ 153 NO-LOCK NO-ERROR.
IF htparam.fchar NE "" THEN
DO:
    /*IF htparam.fchar MATCHES "*INA*" THEN country = "IDN".
    ELSE country = htparam.fchar.*/
    country = htparam.fchar.
    CREATE pci-setup.
    ASSIGN 
      pci-setup.number1    = 9  
      pci-setup.number2    = 1  
      pci-setup.descr      = "DEFAULT COUNTRY CODE"
      pci-setup.setupflag  = YES
      pci-setup.setupvalue = country
      .
END.

/*HOTEL NAME*/
FIND FIRST paramtext WHERE txtnr = 240 NO-LOCK NO-ERROR. 
IF AVAILABLE paramtext AND ptexte NE "" THEN 
DO:
    RUN decode-string(ptexte, OUTPUT htl-name).
    CREATE pci-setup.
    ASSIGN 
      pci-setup.number1    = 99  
      pci-setup.number2    = 1  
      pci-setup.descr      = "HOTEL NAME"
      pci-setup.setupflag  = YES
      pci-setup.setupvalue = htl-name
    .
END.

/*NATIONALITY LIST*/
RUN nation-adminbl.p (0, OUTPUT TABLE t-nation, OUTPUT TABLE t-nation1).
FOR EACH t-nation BY ENTRY(1, t-nation.bezeich, ";") :
    CREATE pci-setup.
    ASSIGN 
      pci-setup.number1    = 9  
      pci-setup.number2    = 2  
      pci-setup.descr      = t-nation.kurzbez
      pci-setup.setupflag  = YES
      pci-setup.setupvalue = ENTRY(1, t-nation.bezeich, ";")
    .
END.

/*REGION LIST*/
EMPTY TEMP-TABLE t-nation1.
EMPTY TEMP-TABLE t-nation.
DEF VAR f-char     AS CHAR.
DEF VAR def-nation AS INTEGER NO-UNDO. 
RUN htpchar.p (153, OUTPUT f-char).
RUN read-nationbl.p (0, f-char, "", OUTPUT TABLE t-nation1).
FIND FIRST t-nation1 NO-ERROR.
def-nation = t-nation1.nationnr. 
RUN read-nation1bl.p (2, def-nation, ?,?, "","", ?, OUTPUT TABLE t-subnation).
FOR EACH t-subnation BY t-subnation.bezeich:
    CREATE pci-setup.
    ASSIGN 
      pci-setup.number1    = 9  
      pci-setup.number2    = 3 
      pci-setup.descr      = t-subnation.kurzbez
      pci-setup.setupflag  = YES
      pci-setup.setupvalue = t-subnation.bezeich
    .
END.

/*SYSTEM DATE*/
FIND FIRST htparam WHERE htparam.paramnr EQ 110 NO-LOCK NO-ERROR.
CREATE pci-setup.
ASSIGN 
    pci-setup.number1    = 9  
    pci-setup.number2    = 4 
    pci-setup.descr      = "SYSTEM DATE"
    pci-setup.setupflag  = YES
    pci-setup.setupvalue = STRING(htparam.fdate,"99/99/9999")
.

/*LICENSE WA/SMS GATEWAY*/
/*FIND FIRST htparam WHERE htparam.paramnr EQ 110 NO-LOCK NO-ERROR.*/
CREATE pci-setup.
ASSIGN 
    pci-setup.number1    = 9  
    pci-setup.number2    = 5 
    pci-setup.descr      = "LICENSE WA/SMS GATEWAY"
    pci-setup.setupflag  = YES
    pci-setup.setupvalue = ""
.

/*CHECK OCCUPANCY TODAY*/
DEFINE VARIABLE do-it    AS LOGICAL NO-UNDO.
DEFINE VARIABLE ci-date  AS DATE.
DEFINE VARIABLE tot-room AS INTEGER NO-UNDO INIT 0.
DEFINE VARIABLE occ-room AS INTEGER NO-UNDO.
DEFINE VARIABLE occ%     AS DECIMAL NO-UNDO.
DEFINE VARIABLE occ1     AS DECIMAL NO-UNDO INIT ?.
DEFINE VARIABLE occ2     AS DECIMAL NO-UNDO.
DEFINE BUFFER bresline FOR res-line.

FIND FIRST htparam WHERE htparam.paramnr EQ 110 NO-LOCK NO-ERROR.
ci-date = htparam.fdate.

FIND FIRST zimmer WHERE zimmer.sleeping NO-LOCK NO-ERROR.
DO WHILE AVAILABLE zimmer:
   DO:
       ASSIGN tot-room = tot-room + 1.
   END.
   FIND NEXT zimmer WHERE zimmer.sleeping NO-LOCK NO-ERROR.
END.
FOR EACH bresline WHERE bresline.active-flag LE 1 
    AND bresline.resstatus LE 6 AND bresline.resstatus NE 3
    AND bresline.resstatus NE 4 AND bresline.resstatus NE 12
    AND bresline.resstatus NE 11 AND bresline.resstatus NE 13 
    AND bresline.ankunft EQ ci-date
    AND bresline.l-zuordnung[3] = 0 NO-LOCK: 
    
    do-it = YES. 
    IF bresline.zinr NE "" THEN 
    DO: 
        FIND FIRST zimmer WHERE zimmer.zinr = bresline.zinr NO-LOCK. 
        do-it = zimmer.sleeping. 
    END.
    
    IF do-it THEN occ-room = occ-room + bresline.zimmeranz.        
END.
ASSIGN occ1 = occ-room / tot-room * 100.

CREATE pci-setup.
ASSIGN 
    pci-setup.number1    = 9  
    pci-setup.number2    = 6 
    pci-setup.descr      = "OCCUPANCY TODAY"
    pci-setup.setupflag  = YES
    pci-setup.setupvalue = ""
    pci-setup.price      = occ1.
.


/*TIME SERVER*/
CREATE pci-setup.
ASSIGN 
    pci-setup.number1    = 9  
    pci-setup.number2    = 7  
    pci-setup.descr      = "SERVER TIME"
    pci-setup.setupflag  = YES
    pci-setup.setupvalue = STRING(TIME,"HH:MM:SS")
.

/*LICENSE MEMBERSHIP*/
DEF VAR p-223 AS LOGICAL.
FIND FIRST htparam WHERE htparam.paramnr = 223 NO-LOCK. 
p-223 = htparam.flogical.

CREATE pci-setup.
ASSIGN 
    pci-setup.number1    = 9  
    pci-setup.number2    = 8
    pci-setup.descr      = "LICENSE MEMBERSHIP"
    pci-setup.setupflag  = p-223
    pci-setup.setupvalue = ""
    .

CREATE pci-setup.
ASSIGN 
    pci-setup.number1    = 9  
    pci-setup.number2    = 9
    pci-setup.descr      = "SERVER DATE"
    pci-setup.setupflag  = YES
    pci-setup.setupvalue = STRING(TODAY)
    .
PROCEDURE decode-string: 
    DEFINE INPUT PARAMETER in-str   AS CHAR. 
    DEFINE OUTPUT PARAMETER out-str AS CHAR INITIAL "". 
    DEFINE VARIABLE s   AS CHAR. 
    DEFINE VARIABLE j   AS INTEGER. 
    DEFINE VARIABLE len AS INTEGER. 
    s   = in-str. 
    j   = ASC(SUBSTR(s, 1, 1)) - 70. 
    len = LENGTH(in-str) - 1. 
    s   = SUBSTR(in-str, 2, len). 
    DO len = 1 TO LENGTH(s): 
       out-str = out-str + chr(asc(SUBSTR(s,len,1)) - j). 
    END. 
END. 

