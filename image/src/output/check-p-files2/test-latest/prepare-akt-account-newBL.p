
DEFINE TEMP-TABLE mainres-list 
  FIELD resname         AS CHAR    FORMAT "x(24)"           LABEL "Reserve Name"
  FIELD gastnr          AS INTEGER
  FIELD resnr           AS INTEGER FORMAT ">>>>>>9"         LABEL "ResNo" 
  FIELD actflag         AS INTEGER INITIAL 0 
  FIELD zimanz          AS INTEGER FORMAT ">>9"             LABEL "Qty" 
  FIELD ankunft         AS DATE    INITIAL 01/01/2099       LABEL "Arrival" 
  FIELD abreise         AS DATE    INITIAL 01/01/1998       LABEL "Depart" 
  FIELD segm            AS INTEGER FORMAT ">>9"             LABEL "Seg" 
  FIELD deposit         AS DECIMAL FORMAT "->>,>>>,>>9.99"  LABEL "Deposit" 
  FIELD until           AS DATE                             LABEL "DueDate" 
  FIELD paid            AS DECIMAL FORMAT "->>,>>>,>>9.99"  LABEL "Paid Amount" 
  FIELD vesrcode        AS CHAR    FORMAT "x(2)"            LABEL "Sales" 
  FIELD id1             AS CHAR    FORMAT "x(3)"            LABEL "ID" 
  FIELD id2             AS CHAR    FORMAT "x(3)"            LABEL "ID" 
  FIELD id2-date        AS DATE                             LABEL "ChgDate" 
  FIELD groupname       AS CHAR    FORMAT "x(33)"           LABEL "Group Name" 
  FIELD grpflag         AS LOGICAL 
  FIELD bemerk          AS CHAR    FORMAT "x(64)"           LABEL "Remark"
  FIELD arrival         AS LOGICAL INITIAL NO 
  FIELD resident        AS LOGICAL INITIAL NO 
  FIELD arr-today       AS LOGICAL INITIAL NO
  FIELD gname           AS CHAR
  FIELD address         AS CHAR
  FIELD city            AS CHAR. 

DEFINE TEMP-TABLE resline LIKE res-line
    FIELD kurzbez AS CHAR.

DEFINE TEMP-TABLE usr
    FIELD userinit AS CHAR
    FIELD username AS CHAR.


DEFINE INPUT PARAMETER userinit     AS CHAR NO-UNDO.
DEFINE OUTPUT PARAMETER ci-date     AS DATE NO-UNDO.
DEFINE OUTPUT PARAMETER other-time  AS INTEGER NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR mainres-list.
DEFINE OUTPUT PARAMETER TABLE FOR resline.
DEFINE OUTPUT PARAMETER TABLE FOR usr.

DEFINE BUFFER gmember FOR guest.

FIND FIRST htparam WHERE paramnr = 87 NO-LOCK NO-ERROR. 
ci-date = htparam.fdate. 

FIND FIRST htparam WHERE htparam.paramnr = 297 NO-LOCK NO-ERROR.
other-time = htparam.finteger.

RUN fill-mainres(1).     /* inital create mainres-list */ 

FOR EACH mainres-list NO-LOCK:
    FOR EACH res-line WHERE res-line.resnr = mainres-list.resnr NO-LOCK,
        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr 
        NO-LOCK BY res-line.reslinnr :
        CREATE resline.
        BUFFER-COPY res-line TO resline.
        ASSIGN resline.kurzbez = zimkateg.kurzbez.
    END.
END.


FOR EACH bediener NO-LOCK:
    CREATE usr.
    ASSIGN 
        usr.userinit = bediener.userinit
        usr.username = bediener.username.
END.


PROCEDURE fill-mainres: 
  DEFINE INPUT PARAMETER fill-code AS INTEGER. 

  FOR EACH mainres-list: 
    DELETE mainres-list. 
  END. 
 
  FOR EACH guest WHERE guest.gastnr GT 0 
    AND guest.phonetik3 = userinit NO-LOCK BY guest.karteityp
    BY guest.NAME:
    
    FOR EACH reservation WHERE reservation.gastnr = guest.gastnr 
      AND reservation.activeflag = 0 NO-LOCK BY reservation.resnr: 

      CREATE mainres-list. 
      ASSIGN
        mainres-list.resname      = guest.NAME
        mainres-list.gastnr       = guest.gastnr
        mainres-list.resnr        = reservation.resnr
        mainres-list.deposit      = reservation.depositgef 
        mainres-list.until        = reservation.limitdate 
        mainres-list.paid         = reservation.depositbez + reservation.depositbez2 
        mainres-list.segm         = reservation.segmentcode 
        mainres-list.groupname    = reservation.groupname
        mainres-list.bemerk       = reservation.bemerk
        mainres-list.vesrcode     = guest.phonetik3
        mainres-list.id1          = reservation.useridanlage 
        mainres-list.id2          = reservation.useridmutat 
        mainres-list.id2-date     = reservation.mutdat 
        mainres-list.grpflag      = reservation.grpflag
        mainres-list.gname        = guest.name + ", " + guest.vorname1 + guest.anredefirma 
                                      + " " + guest.anrede1
        mainres-list.address      = guest.adresse1 + " " + guest.adresse2 
        mainres-list.city         = guest.land + " " + guest.wohnort + " " + guest.plz. 

        RUN update-mainres. 
    END.
  END.
END. 


PROCEDURE update-mainres: 
DEF VAR resline-exist AS LOGICAL INIT NO NO-UNDO.
  ASSIGN
    mainres-list.ankunft   = 01/01/2099 
    mainres-list.abreise   = 01/01/1998 
    mainres-list.zimanz    = 0
    mainres-list.arrival   = NO 
    mainres-list.arr-today = NO 
    mainres-list.resident  = NO.


  FOR EACH res-line WHERE res-line.resnr = mainres-list.resnr 
    AND res-line.active-flag LE 1 AND res-line.resstatus NE 12 
    AND res-line.l-zuordnung[3] = 0 NO-LOCK: 
    resline-exist = YES.
    IF res-line.resstatus NE 11 AND res-line.resstatus NE 13 THEN
      mainres-list.zimanz = mainres-list.zimanz + res-line.zimmeranz. 
    IF mainres-list.ankunft > res-line.ankunft THEN 
       mainres-list.ankunft = res-line.ankunft. 
    IF mainres-list.abreise < res-line.abreise THEN 
       mainres-list.abreise = res-line.abreise. 
    IF (resstatus LE 5 OR resstatus = 11) THEN 
       mainres-list.arrival = YES. 
    IF mainres-list.arrival = YES AND res-line.ankunft = ci-date THEN 
       mainres-list.arr-today = YES. 
    IF res-line.resstatus = 6 OR res-line.resstatus = 13 THEN 
       mainres-list.resident = YES. 
  END. 
  IF NOT resline-exist THEN DELETE mainres-list.
END. 

