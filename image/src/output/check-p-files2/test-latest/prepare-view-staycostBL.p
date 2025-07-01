DEFINE TEMP-TABLE output-list   
  FIELD flag AS INTEGER INITIAL 0   
  FIELD STR AS CHAR FORMAT "x(68)"   
  FIELD str1 AS CHAR.  
  
DEFINE TEMP-TABLE t-res-line  
    FIELD name    LIKE res-line.name  
    FIELD zinr    LIKE res-line.zinr  
    FIELD ankunft LIKE res-line.ankunft  
    FIELD abreise LIKE res-line.abreise.  
  
DEFINE INPUT  PARAMETER pvILanguage     AS INTEGER  NO-UNDO.  
DEFINE INPUT  PARAMETER resnr           AS INTEGER.   
DEFINE INPUT PARAMETER reslinnr         AS INTEGER.  
  
DEFINE OUTPUT PARAMETER ci-date         AS DATE.  
DEFINE OUTPUT PARAMETER contcode        AS CHAR.  
DEFINE OUTPUT PARAMETER ct              AS CHAR.  
DEFINE OUTPUT PARAMETER curr-rmcat      AS CHAR.  
DEFINE OUTPUT PARAMETER t-str           AS CHAR.  
DEFINE OUTPUT PARAMETER str-arrangement AS CHAR.  
DEFINE OUTPUT PARAMETER kurzbez         AS CHAR.  
DEFINE OUTPUT PARAMETER TABLE FOR t-res-line.  
DEFINE OUTPUT PARAMETER TABLE FOR output-list.  
  
DEFINE VARIABLE new-contrate        AS LOGICAL INITIAL NO.   
{supertransBL.i}   
DEFINE VARIABLE lvCAREA AS CHARACTER INITIAL "view-staycost".   
  
DEFINE VARIABLE bonus-array         AS LOGICAL EXTENT 999 INITIAL NO.   
DEFINE VARIABLE wd-array AS INTEGER EXTENT 8   
  INITIAL [7, 1, 2, 3, 4, 5, 6, 7].   
  
FIND FIRST htparam WHERE htparam.paramnr = 550 NO-LOCK.  
IF htparam.feldtyp = 4 THEN new-contrate = htparam.flogical.  
  
FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK.   
ci-date = htparam.fdate.   
   
FIND FIRST res-line WHERE res-line.resnr = resnr AND   
  res-line.reslinnr = reslinnr NO-LOCK NO-ERROR. /*FT serverless*/
IF NOT AVAILABLE res-line THEN RETURN.
CREATE t-res-line.  
ASSIGN t-res-line.name    = res-line.name  
       t-res-line.zinr    = res-line.zinr  
       t-res-line.ankunft = res-line.ankunft  
       t-res-line.abreise = res-line.abreise.  
  
contcode = "".  
FIND FIRST guest-pr WHERE guest-pr.gastnr = res-line.gastnr NO-LOCK NO-ERROR.   
IF AVAILABLE guest-pr THEN   
DO:  
  contcode = guest-pr.CODE.  
  ct = res-line.zimmer-wunsch.  
  IF ct MATCHES("*$CODE$*") THEN  
  DO:  
    ct = SUBSTR(ct,INDEX(ct,"$CODE$") + 6).  
    contcode = SUBSTR(ct, 1, INDEX(ct,";") - 1).  
  END.  
END.  
  
IF res-line.l-zuordnung[1] NE 0 THEN   
DO:   
  FIND FIRST zimkateg WHERE zimkateg.zikatnr = res-line.l-zuordnung[1]   
    NO-LOCK NO-ERROR. 
  IF AVAILABLE zimkateg THEN
    curr-rmcat = zimkateg.kurzbez.   
END.   
   
FIND FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK NO-ERROR.   
FIND FIRST arrangement WHERE arrangement.arrangement   
  = res-line.arrangement NO-LOCK NO-ERROR.  
IF AVAILABLE arrangement THEN
  str-arrangement = arrangement.arrangement. 

IF str-arrangement NE "" THEN
  t-str = translateExtended ("Forecast RoomRev",lvCAREA,"")   
    + " " + TRIM(STRING(res-line.name,"x(30)"))   
    + " " + zimkateg.kurzbez + "/" + arrangement.arrangement.   
ELSE
  t-str = translateExtended ("Forecast RoomRev",lvCAREA,"")   
    + " " + TRIM(STRING(res-line.name,"x(30)"))   
    + " " + zimkateg.kurzbez.   
   
/* IF res-line.adrflag THEN t-str = t-str + " (Local Currency)". */   
IF res-line.betriebsnr NE 0 THEN   
DO:   
  FIND FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr NO-LOCK NO-ERROR.   
  IF AVAILABLE waehrung THEN
    t-str = t-str + "/" + waehrung.wabkurz.   
END.   
   
/* IF room type FOR rate setup is different */   
IF curr-rmcat NE "" THEN t-str = t-str   
    + translateExtended (" (Rate Rmcat =",lvCAREA,"")   
    + " " + curr-rmcat + ")".   
  
IF AVAILABLE zimkateg THEN kurzbez = zimkateg.kurzbez.   
  
RUN view-staycostbl.p  
    (pvILanguage, resnr, reslinnr, contcode, OUTPUT TABLE output-list).
