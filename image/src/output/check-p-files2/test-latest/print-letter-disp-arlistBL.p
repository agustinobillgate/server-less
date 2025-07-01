DEFINE TEMP-TABLE setup-list
    FIELD nr     AS INTEGER
    FIELD CHAR   AS CHAR FORMAT "x(1)"
    FIELD ptexte AS CHAR.

DEF TEMP-TABLE q1-list
    FIELD resnr          LIKE reservation.resnr
    FIELD grpflag        LIKE reservation.grpflag
    FIELD gastnr         LIKE reservation.gastnr
    FIELD name           LIKE guest.name
    FIELD vorname1       LIKE guest.vorname1
    FIELD anrede1        LIKE guest.anrede1
    FIELD anredefirma    LIKE guest.anredefirma
    FIELD briefnr        LIKE reservation.briefnr
    FIELD ankunft        LIKE res-line.ankunft
    FIELD anztage        LIKE res-line.anztage
    FIELD abreise        LIKE res-line.abreise
    FIELD kurzbez        LIKE zimkateg.kurzbez
    FIELD resstatus      LIKE res-line.resstatus
    FIELD groupname      LIKE reservation.groupname
    FIELD activeflag     LIKE reservation.activeflag
/*gerald 19BC08*/
    FIELD roomrate       AS DECIMAL FORMAT "->,>>>,>>>,>>>,>>9.99"
    FIELD room-night     AS INTEGER
    FIELD bedsetup       AS CHARACTER.

DEF INPUT PARAMETER last-sort AS INTEGER.
DEF INPUT PARAMETER fdate     AS DATE.
DEF INPUT PARAMETER lname     AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR q1-list.

/*CREATE setup-list.
setup-list.nr = 1.
setup-list.char = " ".*/

FOR EACH paramtext WHERE paramtext.txtnr GE 9201   
    AND paramtext.txtnr LE 9299 NO-LOCK:   
    CREATE setup-list.   
    setup-list.nr = paramtext.txtnr - 9199.   
    setup-list.char = SUBSTR(paramtext.notes,1,1). 
    setup-list.ptexte = paramtext.ptexte.
END.   

RUN disp-arlist.

PROCEDURE disp-arlist:

  DO: 
    IF last-sort = 1 THEN 
    DO: 
      IF fdate = ? THEN 
      FOR EACH reservation WHERE 
          reservation.activeflag = 0 AND reservation.name GE lname,
          FIRST res-line WHERE res-line.resnr = reservation.resnr
          AND res-line.active-flag = 0,
          FIRST guest WHERE guest.gastnr = reservation.gastnr, 
          FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr,
          FIRST setup-list WHERE setup-list.nr = res-line.setup + 1
          NO-LOCK BY reservation.name:
          RUN assign-it.
          IF reservation.resnr = 80 THEN
      END.
      ELSE
      FOR EACH reservation WHERE
          reservation.activeflag = 0 AND reservation.name GE lname,
          FIRST res-line WHERE res-line.resnr = reservation.resnr
          AND res-line.active-flag = 0 AND res-line.ankunft GE fdate,
          FIRST guest WHERE guest.gastnr = reservation.gastnr,
          FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr,
          FIRST setup-list WHERE setup-list.nr = res-line.setup + 1
          NO-LOCK BY reservation.name:
          RUN assign-it.
      END.
    END.
   ELSE IF last-sort = 2 THEN
   DO:
      IF fdate = ? THEN
      FOR EACH reservation WHERE
          reservation.activeflag = 0 AND reservation.name GE lname,
          FIRST res-line WHERE res-line.resnr = reservation.resnr
          AND res-line.active-flag = 0, 
          FIRST guest WHERE guest.gastnr = reservation.gastnr, 
          FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr,
          FIRST setup-list WHERE setup-list.nr = res-line.setup + 1
          NO-LOCK BY res-line.ankunft:
          RUN assign-it.
      END.
      ELSE
      FOR EACH reservation WHERE 
          reservation.activeflag = 0 AND reservation.name GE lname, 
          FIRST res-line WHERE res-line.resnr = reservation.resnr 
          AND res-line.active-flag = 0 AND res-line.ankunft GE fdate, 
          FIRST guest WHERE guest.gastnr = reservation.gastnr, 
          FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr,
          FIRST setup-list WHERE setup-list.nr = res-line.setup + 1
          NO-LOCK BY res-line.ankunft:
          RUN assign-it.
      END.
    END. 
    ELSE IF last-sort = 3 THEN 
    FOR EACH reservation WHERE 
        reservation.activeflag = 0 AND reservation.name GE lname, 
        FIRST res-line WHERE res-line.resnr = reservation.resnr 
        AND res-line.active-flag = 0, 
        FIRST guest WHERE guest.gastnr = reservation.gastnr, 
        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr,
        FIRST setup-list WHERE setup-list.nr = res-line.setup + 1
        NO-LOCK BY reservation.resnr:
        RUN assign-it.
    END.
  END. 
END.

PROCEDURE assign-it:
    CREATE q1-list.
    ASSIGN
      q1-list.resnr         = reservation.resnr
      q1-list.grpflag       = reservation.grpflag
      q1-list.gastnr        = reservation.gastnr
      q1-list.name          = guest.name
      q1-list.vorname1      = guest.vorname1
      q1-list.anrede1       = guest.anrede1
      q1-list.anredefirma   = guest.anredefirma
      q1-list.briefnr       = reservation.briefnr
      q1-list.ankunft       = res-line.ankunft
      q1-list.anztage       = res-line.anztage
      q1-list.abreise       = res-line.abreise
      q1-list.kurzbez       = zimkateg.kurzbez
      q1-list.resstatus     = res-line.resstatus
      q1-list.groupname     = reservation.groupname
      q1-list.activeflag    = reservation.activeflag
      q1-list.roomrate      = res-line.zipreis
      q1-list.room-night    = (res-line.abreise - res-line.ankunft) * res-line.zimmeranz
      q1-list.bedsetup      = setup-list.ptexte.

    /*/* Add by Gerald RoomRate untuk OTA jadi 0 */
    IF (guest.karteityp = 1) OR (guest.karteityp = 2) THEN
    DO:
        q1-list.roomrate = 0.
    END.*/
END.
