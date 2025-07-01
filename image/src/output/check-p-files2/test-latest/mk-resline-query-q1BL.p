DEF TEMP-TABLE rline-list       LIKE res-line
  FIELD res-char                AS CHAR FORMAT "x(1)" INITIAL " "
  FIELD rsvname                 LIKE reservation.NAME
  FIELD kurzbez                 LIKE zimkateg.kurzbez
  FIELD status-str              AS CHAR FORMAT "x(10)"
.

DEF TEMP-TABLE reschanged-list
    FIELD reslinnr AS INTEGER.

DEF INPUT  PARAMETER pvILanguage    AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER newFlag        AS LOGICAL NO-UNDO.
DEF INPUT  PARAMETER chgNameFlag    AS LOGICAL NO-UNDO.
DEF INPUT  PARAMETER inp-resNo      AS INT     NO-UNDO.
DEF INPUT-OUTPUT PARAMETER TABLE FOR rline-list.
DEF INPUT-OUTPUT PARAMETER TABLE FOR reschanged-list.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "mk-resline". 

DEFINE VARIABLE rstat-list AS CHAR EXTENT 13 FORMAT "x(9)" NO-UNDO.
rstat-list[1]  = translateExtended ("Guaranted",lvCAREA,"").
rstat-list[2]  = translateExtended ("6 PM",lvCAREA,"").
rstat-list[3]  = translateExtended ("Tentative",lvCAREA,"").
rstat-list[4]  = translateExtended ("WaitList",lvCAREA,"").
rstat-list[5]  = "".
rstat-list[6]  = translateExtended ("Inhouse",lvCAREA,"").
rstat-list[7]  = "".
rstat-list[8]  = translateExtended ("Departed",lvCAREA,"").
rstat-list[9]  = translateExtended ("Cancelled",lvCAREA,"").
rstat-list[10] = translateExtended ("NoShow",lvCAREA,"").
rstat-list[11] = translateExtended ("ShareRes",lvCAREA,"").
rstat-list[12] = "".
rstat-list[13] = translateExtended ("RmSharer",lvCAREA,"").

DEF BUFFER rline FOR res-line.
IF newFlag THEN
DO:
    FIND FIRST reservation WHERE reservation.resnr = inp-resNo NO-LOCK NO-ERROR.
    FOR EACH rline WHERE rline.resnr = inp-resNo
        AND rline.active-flag    LE 1 
        AND rline.resstatus      NE 12 
        AND rline.l-zuordnung[3] EQ 0 NO-LOCK: 

        FIND FIRST zimkateg WHERE zimkateg.zikatnr = rline.zikatnr NO-LOCK NO-ERROR.
        
        FIND FIRST rline-list WHERE rline-list.resnr = rline.resnr
            AND rline-list.reslinnr = rline.reslinnr NO-LOCK NO-ERROR.
        IF NOT AVAILABLE rline-list THEN CREATE rline-list.
        BUFFER-COPY rline TO rline-list.
        ASSIGN 
            rline-list.rsvname     = reservation.NAME
            rline-list.status-str  = rstat-list[rline.resstatus]
        .   
        IF AVAILABLE zimkateg THEN rline-list.kurzbez = zimkateg.kurzbez. /*Fix failed find on log appserver eko@12apr2016*/
        FIND FIRST reschanged-list WHERE reschanged-list.reslinnr = rline-list.reslinnr
            NO-ERROR.
        IF AVAILABLE reschanged-list THEN ASSIGN rline-list.res-char = "*".
    END.
END.

IF chgNameFlag THEN
FOR EACH rline-list:
    FIND FIRST rline WHERE rline.resnr = inp-resNo
        AND rline.reslinnr = rline-list.reslinnr NO-LOCK NO-ERROR.
    ASSIGN rline-list.NAME = rline.NAME.
END.
