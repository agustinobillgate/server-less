
DEFINE TEMP-TABLE ci-list
  FIELD ResNo AS INTEGER FORMAT "->,>>>,>>9"
  FIELD resname AS CHAR FORMAT "x(30)"
  FIELD gname AS CHAR FORMAT "x(30)"
  FIELD arrive AS DATE
  FIELD depart AS DATE
  FIELD rmno LIKE zimmer.zinr
  FIELD roomcat AS CHAR FORMAT "x(6)"
  FIELD qty AS INTEGER FORMAT ">>9"
  FIELD resstate AS CHAR FORMAT "x(10)"
  FIELD usrid AS CHAR FORMAT "x(2)"
  FIELD cancel AS DATE.

DEFINE INPUT PARAMETER pvILanguage  AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER sortby       AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER date1        AS DATE NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR ci-list.

{supertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "arl-list".

DEFINE VARIABLE stat-list AS CHAR EXTENT 14 FORMAT "x(9)" NO-UNDO. 
stat-list[1] = translateExtended ("Guaranted",lvCAREA,""). 
stat-list[2] = translateExtended ("6 PM",lvCAREA,""). 
stat-list[3] = translateExtended ("Tentative",lvCAREA,""). 
stat-list[4] = translateExtended ("WaitList",lvCAREA,""). 
stat-list[5] = translateExtended ("OralConfirm",lvCAREA,""). 
stat-list[6] = translateExtended ("Inhouse",lvCAREA,""). 
stat-list[7] = "". 
stat-list[8] = translateExtended ("Departed",lvCAREA,""). 
stat-list[9] = translateExtended ("Cancelled",lvCAREA,""). 
stat-list[10] = translateExtended ("NoShow",lvCAREA,""). 
stat-list[11] = translateExtended ("ShareRes",lvCAREA,""). 
stat-list[12] = translateExtended ("AccGuest",lvCAREA,""). 
stat-list[13] = translateExtended ("RmSharer",lvCAREA,""). 
stat-list[14] = translateExtended ("AccGuest",lvCAREA,"").



RUN cancel-ci.

/******************** PROCEDURE ********************/
&ANALYZE-SUSPEND _UIB-CODE-BLOCK _PROCEDURE cancel-ci wWin 
PROCEDURE cancel-ci :
/*------------------------------------------------------------------------------
  Purpose:     
  Parameters:  <none>
  Notes:       
------------------------------------------------------------------------------*/

/*
res-history.aenderung   = "Cancel C/I Room " + res-line.zinr 
    res-history.action      = "Checkin". 
*/
IF sortby = 1 THEN
DO: 
    FOR EACH res-history WHERE res-history.datum = date1 AND res-history.action = "Cancel C/I"
      AND res-history.aenderung MATCHES ("Cancel C/I Room*") NO-LOCK,
      FIRST res-line WHERE res-line.resnr = res-history.resnr 
      AND res-line.reslinnr = res-history.reslinnr NO-LOCK,
      FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK,
      FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK,
      FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
      FIRST bediener WHERE bediener.nr = res-history.nr NO-LOCK:
        CREATE ci-list.
            ci-list.ResNo = res-line.resnr.
            ci-list.resname = reservation.NAME.
            ci-list.gname = guest.NAME + ", " + guest.vorname1 + ", " + guest.anrede1 + " " + guest.anredefirma.
            ci-list.arrive = res-line.ankunft.
            ci-list.depart = res-line.abreise.
            ci-list.rmno = res-line.zinr.
            ci-list.roomcat = zimkateg.kurzbez.
            ci-list.qty = res-line.zimmeranz.
            ci-list.resstate = stat-list[res-line.resstatus + res-line.l-zuordnung[3]].
            /*IF res-line.resstatus = 1 THEN
                ci-list.resstate = translateExtended ("Guaranted",lvCAREA,"").
            ELSE IF  res-line.resstatus = 2 THEN
                ci-list.resstate = translateExtended ("6 PM",lvCAREA,"").
            ELSE IF  res-line.resstatus = 3 THEN
                ci-list.resstate = translateExtended ("Tentative",lvCAREA,"").
            ELSE IF  res-line.resstatus = 4 THEN
                ci-list.resstate = translateExtended ("WaitList",lvCAREA,"").
            ELSE IF  res-line.resstatus = 5 THEN
                ci-list.resstate = translateExtended ("OralConfirm",lvCAREA,"").
            ELSE IF  res-line.resstatus = 6 THEN
                ci-list.resstate = translateExtended ("Inhouse",lvCAREA,"").
            ELSE IF  res-line.resstatus = 7 THEN
                ci-list.resstate = "".
            ELSE IF  res-line.resstatus = 8 THEN
                ci-list.resstate = translateExtended ("Departed",lvCAREA,"").
            ELSE IF  res-line.resstatus = 9 THEN
                ci-list.resstate = translateExtended ("Cancelled",lvCAREA,"").
            ELSE IF  res-line.resstatus = 10 THEN
                ci-list.resstate = translateExtended ("NoShow",lvCAREA,"").
            ELSE IF  res-line.resstatus = 11 THEN
                ci-list.resstate = translateExtended ("ShareRes",lvCAREA,"").
             ELSE IF  res-line.resstatus = 12 THEN
                ci-list.resstate = translateExtended ("AccGuest",lvCAREA,"").
            ELSE IF  res-line.resstatus = 13 THEN
                ci-list.resstate = translateExtended ("RmSharer",lvCAREA,"").
            ELSE IF  res-line.resstatus = 14 THEN
                ci-list.resstate = translateExtended ("AccGuest",lvCAREA,"").*/

            ci-list.usrid = bediener.userinit.
            ci-list.cancel = res-history.datum.
    END.
   
END.
ELSE IF sortby = 2 THEN
DO:
    FOR EACH res-history WHERE res-history.action = "Cancel C/I"
        AND res-history.aenderung MATCHES ("Cancel C/I Room*") NO-LOCK,
        FIRST res-line WHERE res-line.resnr = res-history.resnr AND
        res-line.ankunft = date1 AND
        res-line.reslinnr = res-history.reslinnr NO-LOCK,
        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK,
        FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK,
        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
        FIRST bediener WHERE bediener.nr = res-history.nr NO-LOCK:
          CREATE ci-list.
            ci-list.ResNo = res-line.resnr.
            ci-list.resname = reservation.NAME.
            ci-list.gname = guest.NAME + ", " + guest.vorname1 + ", " + guest.anrede1 + " " + guest.anredefirma.
            ci-list.arrive = res-line.ankunft.
            ci-list.depart = res-line.abreise.
            ci-list.rmno = res-line.zinr.
            ci-list.roomcat = zimkateg.kurzbez.
            ci-list.qty = res-line.zimmeranz.
            ci-list.resstate = stat-list[res-line.resstatus + res-line.l-zuordnung[3]].
            /*IF res-line.resstatus = 1 THEN
                ci-list.resstate = translateExtended ("Guaranted",lvCAREA,"").
            ELSE IF  res-line.resstatus = 2 THEN
                ci-list.resstate = translateExtended ("6 PM",lvCAREA,"").
            ELSE IF  res-line.resstatus = 3 THEN
                ci-list.resstate = translateExtended ("Tentative",lvCAREA,"").
            ELSE IF  res-line.resstatus = 4 THEN
                ci-list.resstate = translateExtended ("WaitList",lvCAREA,"").
            ELSE IF  res-line.resstatus = 5 THEN
                ci-list.resstate = translateExtended ("OralConfirm",lvCAREA,"").
            ELSE IF  res-line.resstatus = 6 THEN
                ci-list.resstate = translateExtended ("Inhouse",lvCAREA,"").
            ELSE IF  res-line.resstatus = 7 THEN
                ci-list.resstate = "".
            ELSE IF  res-line.resstatus = 8 THEN
                ci-list.resstate = translateExtended ("Departed",lvCAREA,"").
            ELSE IF  res-line.resstatus = 9 THEN
                ci-list.resstate = translateExtended ("Cancelled",lvCAREA,"").
            ELSE IF  res-line.resstatus = 10 THEN
                ci-list.resstate = translateExtended ("NoShow",lvCAREA,"").
            ELSE IF  res-line.resstatus = 11 THEN
                ci-list.resstate = translateExtended ("ShareRes",lvCAREA,"").
             ELSE IF  res-line.resstatus = 12 THEN
                ci-list.resstate = translateExtended ("AccGuest",lvCAREA,"").
            ELSE IF  res-line.resstatus = 13 THEN
                ci-list.resstate = translateExtended ("RmSharer",lvCAREA,"").
            ELSE IF  res-line.resstatus = 14 THEN
                ci-list.resstate = translateExtended ("AccGuest",lvCAREA,"").*/
            ci-list.usrid = bediener.userinit.
            ci-list.cancel = res-history.datum.
    END.
    
END.
ELSE IF sortby = 3 THEN
DO:
    FOR EACH res-history WHERE res-history.action = "Cancel C/I"
        AND res-history.aenderung MATCHES ("Cancel C/I Room*") NO-LOCK,
        FIRST res-line WHERE res-line.resnr = res-history.resnr AND 
        res-line.abreise = date1 AND res-line.reslinnr = res-history.reslinnr NO-LOCK,
        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK,
        FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK, 
        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
        FIRST bediener WHERE bediener.nr = res-history.nr NO-LOCK: 
        CREATE ci-list.
            ci-list.ResNo = res-line.resnr.
            ci-list.resname = reservation.NAME.
            ci-list.gname = guest.NAME + ", " + guest.vorname1 + ", " + guest.anrede1 + " " + guest.anredefirma.
            ci-list.arrive = res-line.ankunft.
            ci-list.depart = res-line.abreise.
            ci-list.rmno = res-line.zinr.
            ci-list.roomcat = zimkateg.kurzbez.
            ci-list.qty = res-line.zimmeranz.
            ci-list.resstate = stat-list[res-line.resstatus + res-line.l-zuordnung[3]].
            /*IF res-line.resstatus = 1 THEN
                ci-list.resstate = translateExtended ("Guaranted",lvCAREA,"").
            ELSE IF  res-line.resstatus = 2 THEN
                ci-list.resstate = translateExtended ("6 PM",lvCAREA,"").
            ELSE IF  res-line.resstatus = 3 THEN
                ci-list.resstate = translateExtended ("Tentative",lvCAREA,"").
            ELSE IF  res-line.resstatus = 4 THEN
                ci-list.resstate = translateExtended ("WaitList",lvCAREA,"").
            ELSE IF  res-line.resstatus = 5 THEN
                ci-list.resstate = translateExtended ("OralConfirm",lvCAREA,"").
            ELSE IF  res-line.resstatus = 6 THEN
                ci-list.resstate = translateExtended ("Inhouse",lvCAREA,"").
            ELSE IF  res-line.resstatus = 7 THEN
                ci-list.resstate = "".
            ELSE IF  res-line.resstatus = 8 THEN
                ci-list.resstate = translateExtended ("Departed",lvCAREA,"").
            ELSE IF  res-line.resstatus = 9 THEN
                ci-list.resstate = translateExtended ("Cancelled",lvCAREA,"").
            ELSE IF  res-line.resstatus = 10 THEN
                ci-list.resstate = translateExtended ("NoShow",lvCAREA,"").
            ELSE IF  res-line.resstatus = 11 THEN
                ci-list.resstate = translateExtended ("ShareRes",lvCAREA,"").
             ELSE IF  res-line.resstatus = 12 THEN
                ci-list.resstate = translateExtended ("AccGuest",lvCAREA,"").
            ELSE IF  res-line.resstatus = 13 THEN
                ci-list.resstate = translateExtended ("RmSharer",lvCAREA,"").
            ELSE IF  res-line.resstatus = 14 THEN
                ci-list.resstate = translateExtended ("AccGuest",lvCAREA,"").*/
            ci-list.usrid = bediener.userinit.
            ci-list.cancel = res-history.datum.
    END.
    
  
END.

END PROCEDURE.

/* _UIB-CODE-BLOCK-END */
&ANALYZE-RESUME
