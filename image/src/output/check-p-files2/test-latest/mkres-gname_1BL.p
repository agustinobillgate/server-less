
DEFINE TEMP-TABLE resline-list
       FIELD ankunft     LIKE res-line.ankunft 
       FIELD abreise     LIKE res-line.abreise 
       FIELD kurzbez     LIKE zimkateg.kurzbez 
       FIELD zimmeranz   LIKE res-line.zimmeranz 
       FIELD zipreis     LIKE res-line.zipreis
       FIELD arrangement LIKE res-line.arrangement
       FIELD resnr       LIKE res-line.resnr
       FIELD reslinnr    LIKE res-line.reslinnr
       FIELD resstatus   LIKE res-line.resstatus 
       FIELD groupname   LIKE reservation.groupname 
       FIELD bemerk      LIKE res-line.bemerk 
       FIELD active-flag LIKE res-line.active-flag
.
DEFINE TEMP-TABLE guest-list
        FIELD firmen-nr  LIKE guest.firmen-nr
        FIELD steuernr   LIKE guest.steuernr
        FIELD full-name  AS CHAR
        FIELD nation1    LIKE guest.nation1
        FIELD wohnort    LIKE guest.wohnort
        FIELD land       LIKE guest.land
        FIELD gastnr     LIKE guest.gastnr
        FIELD karteityp  LIKE guest.karteityp
        FIELD telefon    LIKE guest.telefon
        FIELD overcredit AS LOGICAL INIT NO
.

/**/
DEFINE INPUT PARAMETER case-type        AS INT      NO-UNDO.
DEFINE INPUT PARAMETER temp-flag        AS INT      NO-UNDO.
DEFINE INPUT PARAMETER create-guestseg  AS LOGICAL  NO-UNDO.
DEF INPUT PARAMETER gastno              AS INTEGER  NO-UNDO.
DEF INPUT PARAMETER sorttype            AS INTEGER  NO-UNDO.   /**/
DEF INPUT PARAMETER famname             AS CHAR     NO-UNDO.   
DEF INPUT PARAMETER inp-compNo          AS INTEGER  NO-UNDO.   
DEF INPUT PARAMETER wiguestFlag         AS LOGICAL  NO-UNDO.
DEF INPUT-OUTPUT PARAMETER adult        AS INTEGER  NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR guest-list.
DEFINE OUTPUT PARAMETER TABLE FOR resline-list.

/*
DEF VAR case-type AS INT INIT 2.
DEF VAR gastno AS INT INIT 0.
DEF VAR sorttype AS INT INIT 0.
DEF VAR temp-flag AS INT INIT 2.
DEF VAR famname AS CHAR INIT "".
DEF VAR adult        AS INT  NO-UNDO.
DEF VAR create-guestseg  AS LOGICAL INIT NO NO-UNDO.
DEF VAR wiguestFlag         AS LOGICAL INIT NO NO-UNDO.
DEF VAR inp-compNo AS INT INIT 0. */

DEF VARIABLE fit-gastnr AS INTEGER NO-UNDO INIT 0.

/*************** MAIN LOGIC ***************/

FIND FIRST htparam WHERE htparam.paramnr = 262 NO-LOCK.
IF htparam.finteger GT 0 THEN adult = htparam.finteger.

IF create-guestseg THEN RUN create-guestseg-proc.
ELSE
CASE case-type:
    WHEN 1 THEN RUN create-res-list.
    WHEN 2 THEN RUN create-guest-list.
    WHEN 3 THEN RUN create-res-record.
END CASE.

RETURN.

/*************** PROCEDURE ***************/
PROCEDURE create-guest-list:
    
    IF sorttype = 11 THEN
    DO:
      FIND FIRST htparam WHERE htparam.paramnr = 123 NO-LOCK.
      ASSIGN
          fit-gastnr = htparam.finteger
          sorttype = 1
      .
    END.

    IF temp-flag LE 2 THEN
    DO:                                       
      IF famname = "" THEN
      DO:
        IF wiguestFlag THEN
        FIND FIRST htparam WHERE htparam.paramnr = 109 NO-LOCK.
        ELSE /* individual guest */
        FIND FIRST htparam WHERE htparam.paramnr = 123 NO-LOCK.
        IF htparam.finteger NE 0 THEN 
        DO:
          FIND FIRST guest WHERE guest.gastnr = htparam.finteger NO-LOCK NO-ERROR.
          IF AVAILABLE guest THEN RUN assign-it.
        END.
      END.
      ELSE
      DO:
        IF SUBSTR(famname,1,1) NE "*" THEN famname = "*" + famname.
        IF SUBSTR(famname, LENGTH(famname)) NE "*" THEN
          famname = famname + "*".
        FOR EACH guest WHERE guest.name MATCHES famname 
          AND guest.gastnr GT 0 
          AND guest.karteityp = sorttype 
          AND guest.gastnr NE fit-gastnr NO-LOCK
          USE-INDEX typenam_ix BY guest.NAME:
          RUN assign-it.
        END.
      END.
    END.
/* SY 10/07/2015
    ELSE IF temp-flag = 2 THEN
    DO:
      IF famname = "" THEN
      DO:
        IF wiguestFlag THEN
        FIND FIRST htparam WHERE htparam.paramnr = 109 NO-LOCK.
        ELSE /* individual guest */
        FIND FIRST htparam WHERE htparam.paramnr = 123 NO-LOCK.
        IF htparam.finteger NE 0 THEN 
        DO:
          FIND FIRST guest WHERE guest.gastnr = htparam.finteger NO-LOCK NO-ERROR.
          IF AVAILABLE guest THEN famname = guest.NAME.
        END.
      END.
      FOR EACH guest WHERE guest.name GE famname /*gname*/
        AND guest.gastnr GT 0 AND guest.karteityp = sorttype NO-LOCK
        USE-INDEX typenam_ix BY guest.NAME :
        RUN assign-it.
      END.
    END.
*/
    ELSE IF temp-flag = 3 THEN
    FOR EACH guest WHERE guest.gastnr > 0 
        AND guest.karteityp = sorttype AND guest.firmen-nr GE inp-compNo NO-LOCK
        USE-INDEX typevorname_ix BY guest.firmen-nr BY guest.NAME:
        RUN assign-it.
    END.

    ELSE IF temp-flag = 4 THEN
    FOR EACH guest WHERE guest.gastnr > 0 
        AND guest.karteityp = sorttype AND guest.steuernr GE famname NO-LOCK
        USE-INDEX typevorname_ix BY guest.steuernr BY guest.NAME:
        RUN assign-it.
    END.

    ELSE IF temp-flag = 5 THEN
    FOR EACH guest WHERE guest.gastnr = gastno NO-LOCK USE-INDEX gastnr_index:
        RUN assign-it.
    END.

END.

PROCEDURE assign-it:
    CREATE guest-list.
    ASSIGN 
        guest-list.firmen-nr = guest.firmen-nr
        guest-list.steuernr  = guest.steuernr
        guest-list.full-name = TRIM(guest.name + "," + guest.vorname1 + ", " + guest.anrede1)
        guest-list.nation1   = guest.nation1
        guest-list.wohnort   = guest.wohnort
        guest-list.land      = guest.land
        guest-list.gastnr    = guest.gastnr
        guest-list.karteityp = guest.karteityp
        guest-list.telefon   = guest.telefon. 

END.

PROCEDURE create-res-list: 
    FOR EACH res-line WHERE res-line.gastnr = gastno 
        AND res-line.active-flag LE 1 AND res-line.resstatus NE 12 
        USE-INDEX gnrank_ix , 
        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK
        USE-INDEX resnr_index , 
        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr 
        USE-INDEX zikatnr_ix NO-LOCK BY res-line.ankunft 
        BY res-line.resnr BY res-line.resstatus:
        CREATE resline-list.
        ASSIGN 
            resline-list.ankunft        = res-line.ankunft 
            resline-list.abreise        = res-line.abreise 
            resline-list.kurzbez        = zimkateg.kurzbez 
            resline-list.zimmeranz      = res-line.zimmeranz 
            resline-list.zipreis        = res-line.zipreis
            resline-list.arrangement    = res-line.arrangement
            resline-list.resnr          = res-line.resnr
            resline-list.reslinnr       = res-line.reslinnr
            resline-list.resstatus      = res-line.resstatus 
            resline-list.groupname      = reservation.groupname 
            resline-list.bemerk         = res-line.bemerk 
            resline-list.active-flag    = res-line.active-flag
        .
    END.
END.

PROCEDURE create-res-record: 
DEF VARIABLE inp-resnr    AS INTEGER NO-UNDO.
DEF VARIABLE inp-reslinnr AS INTEGER NO-UNDO.

    ASSIGN
        inp-resnr    = INTEGER(ENTRY(1, famname, ","))
        inp-reslinnr = INTEGER(ENTRY(2, famname, ","))
    .
    FIND FIRST res-line WHERE res-line.resnr = inp-resnr
         AND res-line.reslinnr = inp-reslinnr NO-LOCK.
    FIND FIRST reservation WHERE reservation.resnr = res-line.resnr 
        NO-LOCK.
    FIND FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr 
        NO-LOCK.
    CREATE resline-list.
    ASSIGN 
        resline-list.ankunft        = res-line.ankunft 
        resline-list.abreise        = res-line.abreise 
        resline-list.kurzbez        = zimkateg.kurzbez 
        resline-list.zimmeranz      = res-line.zimmeranz 
        resline-list.zipreis        = res-line.zipreis
        resline-list.arrangement    = res-line.arrangement
        resline-list.resnr          = res-line.resnr
        resline-list.reslinnr       = res-line.reslinnr
        resline-list.resstatus      = res-line.resstatus 
        resline-list.groupname      = reservation.groupname 
        resline-list.bemerk         = res-line.bemerk 
        resline-list.active-flag    = res-line.active-flag
    .
END.

PROCEDURE create-guestseg-proc:
  FIND FIRST segment WHERE segment.betriebsnr = 0 NO-LOCK. 
  FIND FIRST guestseg WHERE guestseg.gastnr = gastno
    AND guestseg.reihenfolge = 1 AND guestseg.segmentcode = segment.segmentcode
    EXCLUSIVE-LOCK NO-ERROR.
  IF NOT AVAILABLE guestseg THEN
  DO:
    CREATE guestseg. 
    ASSIGN 
      guestseg.gastnr       = gastno
      guestseg.reihenfolge  = 1 
      guestseg.segmentcode  = segment.segmentcode
    . 
    FIND CURRENT guestseg NO-LOCK.
    RELEASE guestseg. 
  END.
END.
