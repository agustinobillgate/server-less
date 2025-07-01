DEF INPUT  PARAM user-init       AS CHAR            NO-UNDO.

DEF OUTPUT PARAM sorttype-fchar0 AS CHAR INIT ""    NO-UNDO.
DEF OUTPUT PARAM sorttype-fchar1 AS CHAR INIT ""    NO-UNDO.
DEF OUTPUT PARAM sorttype-fchar2 AS CHAR INIT ""    NO-UNDO.
DEF OUTPUT PARAM ext-char        AS CHAR INIT ""    NO-UNDO.
DEF OUTPUT PARAM htl-city        AS CHAR INIT ""    NO-UNDO.
DEF OUTPUT PARAM curr-htl-city   AS CHAR INIT ""    NO-UNDO.

DEF OUTPUT PARAM vhp-lite        AS LOGICAL         NO-UNDO.
DEF OUTPUT PARAM vhp-multi       AS LOGICAL         NO-UNDO.
DEF OUTPUT PARAM rest-lic        AS LOGICAL         NO-UNDO.
DEF OUTPUT PARAM long-digit      AS LOGICAL         NO-UNDO.
DEF OUTPUT PARAM aktlist-flag    AS LOGICAL INIT NO NO-UNDO.

DEF OUTPUT PARAM ci-date         AS DATE            NO-UNDO.

DEF OUTPUT PARAM vipnr1          AS INTEGER INITIAL 999999999 NO-UNDO. 
DEF OUTPUT PARAM vipnr2          AS INTEGER INITIAL 999999999 NO-UNDO. 
DEF OUTPUT PARAM vipnr3          AS INTEGER INITIAL 999999999 NO-UNDO. 
DEF OUTPUT PARAM vipnr4          AS INTEGER INITIAL 999999999 NO-UNDO. 
DEF OUTPUT PARAM vipnr5          AS INTEGER INITIAL 999999999 NO-UNDO. 
DEF OUTPUT PARAM vipnr6          AS INTEGER INITIAL 999999999 NO-UNDO. 
DEF OUTPUT PARAM vipnr7          AS INTEGER INITIAL 999999999 NO-UNDO.
DEF OUTPUT PARAM vipnr8          AS INTEGER INITIAL 999999999 NO-UNDO.
DEF OUTPUT PARAM vipnr9          AS INTEGER INITIAL 999999999 NO-UNDO.

FIND FIRST paramtext WHERE txtnr = 203 NO-ERROR. 
curr-htl-city = paramtext.ptexte.
/* &Individual", 0, "&Company", 1, "&TravelAgent" */ 
FIND FIRST htparam WHERE paramnr = 796 NO-LOCK. 
IF htparam.fchar NE "" THEN sorttype-fchar0 = htparam.fchar.
 
FIND FIRST htparam WHERE paramnr = 797 NO-LOCK. 
IF htparam.fchar NE "" THEN sorttype-fchar1 = htparam.fchar.
 
FIND FIRST htparam WHERE paramnr = 798 NO-LOCK. 
IF htparam.fchar NE "" THEN sorttype-fchar2 = htparam.fchar.
   
FIND FIRST htparam WHERE paramnr = 1015 no-lock.  /* VHP Lite */ 
vhp-lite = htparam.flogical. 
FIND FIRST htparam WHERE paramnr = 996 NO-LOCK. 
vhp-multi = htparam.flogical.
FIND FIRST htparam WHERE paramnr = 990 no-lock.  /* Rest License */ 
rest-lic = htparam.flogical. 
FIND FIRST htparam WHERE paramnr = 246 no-lock.  /* Long Digit */ 
long-digit = htparam.flogical. 
FIND FIRST htparam WHERE paramnr = 148 no-lock.  /* Extended CHAR FOR GCF Prog */ 
ext-char = htparam.fchar. 
  
RUN get-vipnr. 
 
FIND FIRST htparam WHERE htparam.paramnr = 110 NO-LOCK. 
ci-date = htparam.fdate.

/*ITA 22/11/21 - Request HGU*/
FIND FIRST htparam WHERE htparam.paramnr = 1355 NO-LOCK.
IF htparam.flogical = YES THEN ASSIGN ci-date = TODAY.

FIND FIRST htparam WHERE htparam.paramnr = 1002 NO-LOCK. /* sales Lic */
IF htparam.flogical THEN
DO:
  FIND FIRST akt-line WHERE akt-line.userinit = user-init
    AND akt-line.datum GE (ci-date - 1) AND akt-line.datum LE ci-date
    NO-LOCK NO-ERROR.
  aktlist-flag = AVAILABLE akt-line. 
END. 

FIND FIRST paramtext WHERE paramtext.txtnr GE 203.
htl-city = paramtext.ptexte.

PROCEDURE get-vipnr: 
  FIND FIRST htparam WHERE paramnr = 700 NO-LOCK. 
  IF htparam.finteger NE 0 THEN vipnr1 = htparam.finteger. 
  FIND FIRST htparam WHERE paramnr = 701 NO-LOCK. 
  IF htparam.finteger NE 0 THEN vipnr2 = htparam.finteger. 
  FIND FIRST htparam WHERE paramnr = 702 NO-LOCK. 
  IF htparam.finteger NE 0 THEN vipnr3 = htparam.finteger. 
  FIND FIRST htparam WHERE paramnr = 703 NO-LOCK. 
  IF htparam.finteger NE 0 THEN vipnr4 = htparam.finteger. 
  FIND FIRST htparam WHERE paramnr = 704 NO-LOCK. 
  IF htparam.finteger NE 0 THEN vipnr5 = htparam.finteger. 
  FIND FIRST htparam WHERE paramnr = 705 NO-LOCK. 
  IF htparam.finteger NE 0 THEN vipnr6 = htparam.finteger. 
  FIND FIRST htparam WHERE paramnr = 706 NO-LOCK. 
  IF htparam.finteger NE 0 THEN vipnr7 = htparam.finteger. 
  FIND FIRST htparam WHERE paramnr = 707 NO-LOCK. 
  IF htparam.finteger NE 0 THEN vipnr8 = htparam.finteger. 
  FIND FIRST htparam WHERE paramnr = 708 NO-LOCK. 
  IF htparam.finteger NE 0 THEN vipnr9 = htparam.finteger. 
END.
