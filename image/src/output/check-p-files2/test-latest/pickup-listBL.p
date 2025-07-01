/****************************  DEFINE TEMP TABLE *********************************/   
DEF TEMP-TABLE pickup-list  
    FIELD gastnr            LIKE res-line.gastnr  
    FIELD gastnrmember      LIKE res-line.gastnrmember  
    FIELD resnr             LIKE res-line.resnr  
    FIELD reslinnr          LIKE res-line.reslinnr  
    FIELD zinr              LIKE res-line.zinr  
    FIELD NAME              LIKE res-line.NAME  
    FIELD vip               AS CHAR FORMAT "x(5)"       LABEL "VIP"  
    FIELD segmentcode       LIKE guestseg.segmentcode  
    FIELD ankunft           LIKE res-line.ankunft  
    FIELD arrTime           AS CHAR FORMAT "x(8)"       LABEL "ArrTime"  
    FIELD flight1           AS CHAR FORMAT "x(6)"       LABEL "FlightNo"  
    FIELD eta               AS CHAR FORMAT "x(5)"       LABEL "ETA"  
    FIELD abreise           LIKE res-line.abreise  
    FIELD flight2           AS CHAR FORMAT "x(6)"       LABEL "FlightNo"  
    FIELD etd               AS CHAR FORMAT "x(5)"       LABEL "ETD"  
    FIELD zimmeranz         LIKE res-line.zimmeranz  
    FIELD kurzbez           LIKE zimkateg.kurzbez  
    FIELD erwachs           LIKE res-line.erwachs       FORMAT ">9"  
    FIELD kind1             LIKE res-line.kind1         FORMAT ">9"  
    FIELD gratis            LIKE res-line.gratis        FORMAT ">9"  
    FIELD statStr           AS CHAR FORMAT "x(9)"       LABEL "ResStatus"  
    FIELD arrangemment      LIKE arrangement.arrangement  
    FIELD zipreis           LIKE res-line.zipreis  
    FIELD bemerk            LIKE res-line.bemerk        FORMAT "x(80)"  
    FIELD resname           AS CHAR  
    FIELD adresse           AS CHAR  
    FIELD wohnort           AS CHAR  
    FIELD nat1              AS CHAR  
    FIELD groupname         AS CHAR  
    FIELD betrieb-gastmem   AS INTEGER  
.  
  
/*************** DEFINE INPUT PARAMETER ***************/  
DEFINE INPUT  PARAMETER pvILanguage  AS INTEGER NO-UNDO.  
DEFINE INPUT  PARAMETER disp-pickup  AS LOGICAL NO-UNDO.
DEFINE INPUT  PARAMETER check-ftd    AS LOGICAL NO-UNDO.  
DEFINE INPUT  PARAMETER fdate        AS DATE    NO-UNDO.
DEFINE INPUT  PARAMETER frdate       AS DATE    NO-UNDO.  
DEFINE INPUT  PARAMETER tdate        AS DATE    NO-UNDO.  
  
DEFINE OUTPUT PARAMETER ci-date      AS DATE    NO-UNDO.  
DEFINE OUTPUT PARAMETER TABLE FOR pickup-list.  
  
DEFINE VARIABLE vipnr1   AS INTEGER  NO-UNDO.  
DEFINE VARIABLE vipnr2   AS INTEGER  NO-UNDO.  
DEFINE VARIABLE vipnr3   AS INTEGER  NO-UNDO.  
DEFINE VARIABLE vipnr4   AS INTEGER  NO-UNDO.  
DEFINE VARIABLE vipnr5   AS INTEGER  NO-UNDO.  
DEFINE VARIABLE vipnr6   AS INTEGER  NO-UNDO.  
DEFINE VARIABLE vipnr7   AS INTEGER  NO-UNDO.  
DEFINE VARIABLE vipnr8   AS INTEGER  NO-UNDO.  
DEFINE VARIABLE vipnr9   AS INTEGER  NO-UNDO.  
DEFINE VARIABLE vip-code AS CHAR     NO-UNDO.  
DEFINE VARIABLE nat-str  AS CHAR     NO-UNDO.  
  
DEFINE BUFFER gmember FOR guest.  
DEFINE BUFFER gsegbuff FOR guestseg.  
  
{supertransBL.i}   
DEF VAR lvCAREA AS CHAR INITIAL "availability".   
  
DEFINE VARIABLE stat-list AS CHAR EXTENT 13 FORMAT "x(9)" NO-UNDO.   
    stat-list[1]  = translateExtended ("Guaranted",lvCAREA,"").   
    stat-list[2]  = translateExtended ("6 PM",lvCAREA,"").   
    stat-list[3]  = translateExtended ("Tentative",lvCAREA,"").   
    stat-list[4]  = translateExtended ("WaitList",lvCAREA,"").   
    stat-list[5]  = translateExtended ("OralConfirm",lvCAREA,"").   
    stat-list[6]  = translateExtended ("Inhouse",lvCAREA,"").   
    stat-list[7]  = "".   
    stat-list[8]  = translateExtended ("Departed",lvCAREA,"").   
    stat-list[9]  = translateExtended ("Cancelled",lvCAREA,"").   
    stat-list[10] = translateExtended ("NoShow",lvCAREA,"").   
    stat-list[11] = translateExtended ("ShareRes",lvCAREA,"").   
    stat-list[12] = "".   
    stat-list[13] = translateExtended ("RmSharer",lvCAREA,"").   
  
  
/************************* MAIN LOGIC *****************************/  
  
RUN get-vipnrbl.p (OUTPUT vipnr1, OUTPUT vipnr2, OUTPUT vipnr3, OUTPUT vipnr4,  
                   OUTPUT vipnr5, OUTPUT vipnr6, OUTPUT vipnr7, OUTPUT vipnr8,  
                   OUTPUT vipnr9).  
  
FIND FIRST htparam WHERE htparam.paramnr = 297 NO-LOCK.  
IF htparam.finteger NE 0 THEN stat-list[2] = STRING(htparam.finteger)   
  + " " + translateExtended ("PM",lvCAREA,"").   
  
IF check-ftd = NO THEN DO:
    IF disp-pickup THEN RUN disp-pickup.  
    ELSE IF NOT disp-pickup THEN RUN disp-drop.  
END.
ELSE IF check-ftd = YES THEN DO:
    IF disp-pickup THEN RUN disp-pickup1.  
    ELSE IF NOT disp-pickup THEN RUN disp-drop1. 
END.
  
/************************ PROCEDURE ************************/  
PROCEDURE disp-pickup:   
  FOR EACH res-line WHERE   
     (res-line.resstatus LE 5 OR res-line.resstatus = 11)   
     AND res-line.ankunft = fdate   
     AND res-line.zimmer-wunsch MATCHES ("*pickup*") NO-LOCK,   
     FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK BY res-line.resnr BY res-line.NAME:  
       
     FIND FIRST guestseg WHERE guestseg.gastnr = res-line.gastnrmember AND   
     guestseg.reihenfolge = 1 NO-LOCK. 
     FIND FIRST reservation WHERE reservation.resnr = res-line.resnr  
         NO-LOCK.  
     FIND FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK.  
     FIND FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember  
         NO-LOCK.  
  
     vip-code = "".   
     FIND FIRST gsegbuff WHERE gsegbuff.gastnr = res-line.gastnrmember   
        AND (gsegbuff.segmentcode = vipnr1 OR   
        gsegbuff.segmentcode = vipnr2 OR   
        gsegbuff.segmentcode = vipnr3 OR   
        gsegbuff.segmentcode = vipnr4 OR   
        gsegbuff.segmentcode = vipnr5 OR   
        gsegbuff.segmentcode = vipnr6 OR   
        gsegbuff.segmentcode = vipnr7 OR   
        gsegbuff.segmentcode = vipnr8 OR   
        gsegbuff.segmentcode = vipnr9) NO-LOCK NO-ERROR.   
     IF AVAILABLE gsegbuff THEN   
     DO:   
       FIND FIRST segment  WHERE segment.segmentcode  
         = gsegbuff.segmentcode NO-LOCK.  
       vip-code = segment.bezeich.   
     END.  
       
     nat-str = "".  
     FIND FIRST nation WHERE nation.kurzbez = gmember.nation1   
       NO-LOCK NO-ERROR.  
     IF AVAILABLE nation THEN nat-str = nation.bezeich.  
  
     CREATE pickup-list.  
     BUFFER-COPY res-line TO pickup-list.  
     ASSIGN  
        pickup-list.vip = vip-code  
        pickup-list.segmentcode = guestseg.segmentcode  
        pickup-list.arrtime = STRING(res-line.ankzeit,"HH:MM:SS")  
        pickup-list.flight1 = SUBSTR(res-line.flight-nr, 1, 6)  
        pickup-list.eta = SUBSTR(res-line.flight-nr, 7, 5)  
        pickup-list.flight2 = SUBSTR(res-line.flight-nr, 12, 6)  
        pickup-list.etd = SUBSTR(res-line.flight-nr, 18, 5)   
        pickup-list.kurzbez = zimkateg.kurzbez  
        pickup-list.statStr = stat-list[res-line.resstatus] 
        pickup-list.arrangemment = res-line.arrangement
        pickup-list.resname = guest.NAME  
        pickup-list.adresse = gmember.adresse1 + ", " + gmember.adresse2  
        pickup-list.wohnort = gmember.wohnort + " " + gmember.plz  
        pickup-list.nat1    = nat-str  
        pickup-list.groupname = reservation.groupname  
     .  
  END.  
END.  
  
  
PROCEDURE disp-drop:   
  FOR EACH res-line WHERE res-line.active-flag LE 1  
     AND res-line.abreise = fdate   
     AND res-line.zimmer-wunsch MATCHES ("*drop-passanger*") NO-LOCK,   
     FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK BY res-line.resnr BY res-line.NAME:  
       
     FIND FIRST guestseg WHERE guestseg.gastnr = res-line.gastnrmember AND   
     guestseg.reihenfolge = 1 NO-LOCK. 
      FIND FIRST reservation WHERE reservation.resnr = res-line.resnr  
          NO-LOCK.  
     FIND FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK.  
     FIND FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember  
         NO-LOCK.  
  
     vip-code = "".   
     FIND FIRST gsegbuff WHERE gsegbuff.gastnr = res-line.gastnrmember   
        AND (gsegbuff.segmentcode = vipnr1 OR   
        gsegbuff.segmentcode = vipnr2 OR   
        gsegbuff.segmentcode = vipnr3 OR   
        gsegbuff.segmentcode = vipnr4 OR   
        gsegbuff.segmentcode = vipnr5 OR   
        gsegbuff.segmentcode = vipnr6 OR   
        gsegbuff.segmentcode = vipnr7 OR   
        gsegbuff.segmentcode = vipnr8 OR   
        gsegbuff.segmentcode = vipnr9) NO-LOCK NO-ERROR.   
     IF AVAILABLE gsegbuff THEN   
     DO:   
       FIND FIRST segment  WHERE segment.segmentcode  
         = gsegbuff.segmentcode NO-LOCK.  
       vip-code = segment.bezeich.   
     END.  
      
     nat-str = "".  
     FIND FIRST nation WHERE nation.kurzbez = gmember.nation1   
       NO-LOCK NO-ERROR.  
     IF AVAILABLE nation THEN nat-str = nation.bezeich.  
      
     CREATE pickup-list.  
     BUFFER-COPY res-line TO pickup-list.  
     ASSIGN  
        pickup-list.vip = vip-code  
        pickup-list.segmentcode = guestseg.segmentcode  
        pickup-list.arrtime = STRING(res-line.ankzeit,"HH:MM:SS")  
        pickup-list.flight1 = SUBSTR(res-line.flight-nr, 1, 6)  
        pickup-list.eta = SUBSTR(res-line.flight-nr, 7, 5)  
        pickup-list.flight2 = SUBSTR(res-line.flight-nr, 12, 6)  
        pickup-list.etd = SUBSTR(res-line.flight-nr, 18, 5)   
        pickup-list.kurzbez = zimkateg.kurzbez  
        pickup-list.statStr = stat-list[res-line.resstatus]
        pickup-list.arrangemment = res-line.arrangement
        pickup-list.resname = guest.NAME  
        pickup-list.adresse = gmember.adresse1 + ", " + gmember.adresse2  
        pickup-list.wohnort = gmember.wohnort + " " + gmember.plz  
        pickup-list.nat1    = nat-str  
        pickup-list.groupname = reservation.groupname  
    .  
  END.  
END.  


PROCEDURE disp-pickup1:   
  FOR EACH res-line WHERE   
     (res-line.resstatus LE 5 OR res-line.resstatus = 11)   
     AND res-line.ankunft GE frdate
     AND res-line.ankunft LE tdate
     AND res-line.zimmer-wunsch MATCHES ("*pickup*") NO-LOCK,   
     FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK BY res-line.resnr BY res-line.NAME:  
       
     FIND FIRST guestseg WHERE guestseg.gastnr = res-line.gastnrmember AND   
     guestseg.reihenfolge = 1 NO-LOCK. 
     FIND FIRST reservation WHERE reservation.resnr = res-line.resnr  
         NO-LOCK.  
     FIND FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK.  
     FIND FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember  
         NO-LOCK.  
  
     vip-code = "".   
     FIND FIRST gsegbuff WHERE gsegbuff.gastnr = res-line.gastnrmember   
        AND (gsegbuff.segmentcode = vipnr1 OR   
        gsegbuff.segmentcode = vipnr2 OR   
        gsegbuff.segmentcode = vipnr3 OR   
        gsegbuff.segmentcode = vipnr4 OR   
        gsegbuff.segmentcode = vipnr5 OR   
        gsegbuff.segmentcode = vipnr6 OR   
        gsegbuff.segmentcode = vipnr7 OR   
        gsegbuff.segmentcode = vipnr8 OR   
        gsegbuff.segmentcode = vipnr9) NO-LOCK NO-ERROR.   
     IF AVAILABLE gsegbuff THEN   
     DO:   
       FIND FIRST segment  WHERE segment.segmentcode  
         = gsegbuff.segmentcode NO-LOCK.  
       vip-code = segment.bezeich.   
     END.  
       
     nat-str = "".  
     FIND FIRST nation WHERE nation.kurzbez = gmember.nation1   
       NO-LOCK NO-ERROR.  
     IF AVAILABLE nation THEN nat-str = nation.bezeich.  
  
     CREATE pickup-list.  
     BUFFER-COPY res-line TO pickup-list.  
     ASSIGN  
        pickup-list.vip = vip-code  
        pickup-list.segmentcode = guestseg.segmentcode  
        pickup-list.arrtime = STRING(res-line.ankzeit,"HH:MM:SS")  
        pickup-list.flight1 = SUBSTR(res-line.flight-nr, 1, 6)  
        pickup-list.eta = SUBSTR(res-line.flight-nr, 7, 5)  
        pickup-list.flight2 = SUBSTR(res-line.flight-nr, 12, 6)  
        pickup-list.etd = SUBSTR(res-line.flight-nr, 18, 5)   
        pickup-list.kurzbez = zimkateg.kurzbez  
        pickup-list.statStr = stat-list[res-line.resstatus]
        pickup-list.arrangemment = res-line.arrangement
        pickup-list.resname = guest.NAME  
        pickup-list.adresse = gmember.adresse1 + ", " + gmember.adresse2  
        pickup-list.wohnort = gmember.wohnort + " " + gmember.plz  
        pickup-list.nat1    = nat-str  
        pickup-list.groupname = reservation.groupname  
     .  
  END.  
END.  
  
  
PROCEDURE disp-drop1:   
  FOR EACH res-line WHERE res-line.active-flag LE 1  
     AND res-line.abreise GE frdate
     AND res-line.abreise LE tdate
     AND res-line.zimmer-wunsch MATCHES ("*drop-passanger*") NO-LOCK,   
     FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK BY res-line.resnr BY res-line.NAME:  
       
      FIND FIRST guestseg WHERE guestseg.gastnr = res-line.gastnrmember AND   
     guestseg.reihenfolge = 1 NO-LOCK. 

      FIND FIRST reservation WHERE reservation.resnr = res-line.resnr  
          NO-LOCK.  
     FIND FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK.  
     FIND FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember  
         NO-LOCK.  
  
     vip-code = "".   
     FIND FIRST gsegbuff WHERE gsegbuff.gastnr = res-line.gastnrmember   
        AND (gsegbuff.segmentcode = vipnr1 OR   
        gsegbuff.segmentcode = vipnr2 OR   
        gsegbuff.segmentcode = vipnr3 OR   
        gsegbuff.segmentcode = vipnr4 OR   
        gsegbuff.segmentcode = vipnr5 OR   
        gsegbuff.segmentcode = vipnr6 OR   
        gsegbuff.segmentcode = vipnr7 OR   
        gsegbuff.segmentcode = vipnr8 OR   
        gsegbuff.segmentcode = vipnr9) NO-LOCK NO-ERROR.   
     IF AVAILABLE gsegbuff THEN   
     DO:   
       FIND FIRST segment  WHERE segment.segmentcode  
         = gsegbuff.segmentcode NO-LOCK.  
       vip-code = segment.bezeich.   
     END.  
      
     nat-str = "".  
     FIND FIRST nation WHERE nation.kurzbez = gmember.nation1   
       NO-LOCK NO-ERROR.  
     IF AVAILABLE nation THEN nat-str = nation.bezeich.  
      
     CREATE pickup-list.  
     BUFFER-COPY res-line TO pickup-list.  
     ASSIGN  
        pickup-list.vip = vip-code  
        pickup-list.segmentcode = guestseg.segmentcode  
        pickup-list.arrtime = STRING(res-line.ankzeit,"HH:MM:SS")  
        pickup-list.flight1 = SUBSTR(res-line.flight-nr, 1, 6)  
        pickup-list.eta = SUBSTR(res-line.flight-nr, 7, 5)  
        pickup-list.flight2 = SUBSTR(res-line.flight-nr, 12, 6)  
        pickup-list.etd = SUBSTR(res-line.flight-nr, 18, 5)   
        pickup-list.kurzbez = zimkateg.kurzbez  
        pickup-list.statStr = stat-list[res-line.resstatus]
        pickup-list.arrangemment = res-line.arrangement
        pickup-list.resname = guest.NAME  
        pickup-list.adresse = gmember.adresse1 + ", " + gmember.adresse2  
        pickup-list.wohnort = gmember.wohnort + " " + gmember.plz  
        pickup-list.nat1    = nat-str  
        pickup-list.groupname = reservation.groupname  
    .  
  END.  
END.  


