
DEF TEMP-TABLE t-fixleist      LIKE fixleist
    FIELD depart  AS CHAR
    FIELD rec-id  AS INTEGER.

DEFINE INPUT  PARAMETER pvILanguage     AS INTEGER  NO-UNDO.
DEFINE INPUT  PARAMETER resnr           AS INTEGER.
DEFINE INPUT  PARAMETER reslinnr        AS INTEGER.

DEFINE OUTPUT PARAMETER f-tittle        AS CHAR.
DEFINE OUTPUT PARAMETER contcode        AS CHAR.
DEFINE OUTPUT PARAMETER billdate        AS DATE.
DEFINE OUTPUT PARAMETER foreign-rate    AS LOGICAL.
DEFINE OUTPUT PARAMETER double-currency AS LOGICAL.
DEFINE OUTPUT PARAMETER price-decimal   AS INTEGER.
DEFINE OUTPUT PARAMETER exchg-rate      AS DECIMAL INITIAL 1.
DEFINE OUTPUT PARAMETER curr-local      AS CHAR.
DEFINE OUTPUT PARAMETER curr-foreign    AS CHAR.
DEFINE OUTPUT PARAMETER flag            AS LOGICAL INIT NO.
DEFINE OUTPUT PARAMETER TABLE FOR t-fixleist.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "res-fixart".

DEFINE VARIABLE ct  AS CHAR.

FIND FIRST res-line WHERE res-line.resnr = resnr 
  AND res-line.reslinnr = reslinnr NO-LOCK. 
 
f-tittle = res-line.name + " - " + translateExtended ("Check-In",lvCAREA,"") 
         + " " + STRING(res-line.ankunft) 
         + "; " + translateExtended ("Check-Out",lvCAREA,"") 
         + " " + STRING(res-line.abreise). 
 
contcode = "".
FIND FIRST guest-pr WHERE guest-pr.gastnr = res-line.gastnr NO-LOCK NO-ERROR. 
IF AVAILABLE guest-pr THEN 
DO:
  contcode = guest-pr.code.
  ct = res-line.zimmer-wunsch.
  IF ct MATCHES("*$CODE$*") THEN
  DO:
    ct = SUBSTR(ct,INDEX(ct,"$CODE$") + 6).
    contcode = SUBSTR(ct, 1, INDEX(ct,";") - 1).
  END.
END.

 
FIND FIRST htparam WHERE paramnr = 110 NO-LOCK. 
billdate = htparam.fdate. 
 
FOR EACH fixleist WHERE fixleist.resnr = resnr 
    AND fixleist.reslinnr = reslinnr NO-LOCK 
    BY fixleist.departement BY fixleist.artnr:
    CREATE t-fixleist.
    BUFFER-COPY fixleist TO t-fixleist.
    t-fixleist.rec-id = RECID(fixleist).
    FIND FIRST hoteldpt WHERE hoteldpt.num = fixleist.departement NO-LOCK. 
    t-fixleist.depart = hoteldpt.depart. 
END.

/*MTIF AVAILABLE fixleist THEN 
DO: 
  selected = YES. 
  RUN fill-fixleist-list. 
  DISPLAY fixleist-list.departement deptname fixleist-list.artnr 
          fixleist-list.bezeich fixleist-list.number 
          fixleist-list.sequenz fixleist-list.dekade fixleist-list.lfakt 
          fixleist-list.betrag WITH FRAME frame1. 
END. 

ENABLE b1 btn-exit btn-cancel WITH FRAME frame1. 
IF NOT view-only THEN 
  ENABLE btn-addart btn-chgart btn-delart WITH FRAME frame1. 
*/

FIND FIRST htparam WHERE htparam.paramnr = 143 NO-LOCK. 
foreign-rate = htparam.flogical. 
FIND FIRST htparam WHERE paramnr = 240 NO-LOCK. 
double-currency = htparam.flogical. 
FIND FIRST htparam WHERE htparam.paramnr = 491 NO-LOCK. 
price-decimal = htparam.finteger. 

/* 
FIND FIRST htparam WHERE htparam.paramnr = 144 NO-LOCK. 
FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK NO-ERROR. 
*/

FIND FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr NO-LOCK
    NO-ERROR.
IF AVAILABLE waehrung THEN exchg-rate = waehrung.ankauf / waehrung.einheit. 

FIND FIRST htparam WHERE paramnr = 152 NO-LOCK. 
curr-local = htparam.fchar. 
FIND FIRST htparam WHERE paramnr = 144 NO-LOCK. 
curr-foreign = htparam.fchar. 
 
IF res-line.adrflag THEN 
DO: 
  flag = YES.
END. 
