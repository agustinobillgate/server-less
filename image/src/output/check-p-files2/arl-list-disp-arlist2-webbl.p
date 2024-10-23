  
DEFINE WORKFILE setup-list   
  FIELD nr AS INTEGER   
  FIELD CHAR AS CHAR FORMAT "x(1)".   
  
DEFINE BUFFER gbuff FOR guest.  
  
DEFINE TEMP-TABLE arl-list  
    FIELD resnr             LIKE res-line.resnr  
    FIELD reslinnr          LIKE res-line.reslinnr  
    FIELD resline-wabkurz   LIKE res-line.wabkurz  
    FIELD voucher-nr        LIKE res-line.voucher-nr  
    FIELD grpflag           LIKE reservation.grpflag  
    FIELD verstat           LIKE reservation.verstat  
    FIELD l-zuordnung2      AS INTEGER  
    FIELD kontignr          LIKE res-line.kontignr  
    FIELD firmen-nr         AS INTEGER  
    FIELD steuernr          AS CHARACTER 
    FIELD rsv-name          AS CHARACTER FORMAT "x(120)"
    FIELD zinr              LIKE res-line.zinr  
    FIELD setup-list-char   AS CHARACTER  
    FIELD resline-name      LIKE res-line.name  
    FIELD waehrung-wabkurz  LIKE waehrung.wabkurz  
    FIELD segmentcode       LIKE reservation.segmentcode  
    FIELD ankunft           LIKE res-line.ankunft  
    FIELD abreise           LIKE res-line.abreise  
    FIELD zimmeranz         LIKE res-line.zimmeranz  
    FIELD kurzbez           LIKE zimkateg.kurzbez  
    FIELD arrangement       LIKE res-line.arrangement  
    FIELD zipreis           LIKE res-line.zipreis  
    FIELD anztage           LIKE res-line.anztage  
    FIELD erwachs           LIKE res-line.erwachs  
    FIELD kind1             LIKE res-line.kind1  
    FIELD kind2             LIKE res-line.kind2  
    FIELD gratis            LIKE res-line.gratis  
    FIELD l-zuordnung4      AS INTEGER  
    FIELD resstatus         LIKE res-line.resstatus  
    FIELD l-zuordnung3      AS INTEGER  
    FIELD flight-nr         LIKE res-line.flight-nr  
    FIELD ankzeit           LIKE res-line.ankzeit  
    FIELD abreisezeit       LIKE res-line.abreisezeit  
    FIELD betrieb-gast      LIKE res-line.betrieb-gast  
    FIELD resdat            LIKE reservation.resdat  
    FIELD useridanlage      LIKE reservation.useridanlage  
    FIELD reserve-dec       LIKE res-line.reserve-dec  
    FIELD cancelled-id      LIKE res-line.cancelled-id  
    FIELD changed-id        LIKE res-line.changed-id  
    FIELD groupname         LIKE reservation.groupname    
    FIELD active-flag       LIKE res-line.active-flag  
    FIELD gastnr            LIKE res-line.gastnr      
    FIELD gastnrmember      LIKE res-line.gastnrmember  
    FIELD karteityp         AS INTEGER    
    FIELD reserve-int       LIKE res-line.reserve-int
    FIELD zikatnr           LIKE res-line.zikatnr  
    FIELD betrieb-gastmem   LIKE res-line.betrieb-gastmem  
    FIELD pseudofix         LIKE res-line.pseudofix  
    FIELD reserve-char      LIKE res-line.reserve-char  
    FIELD bemerk            LIKE res-line.bemerk    
    FIELD depositbez        LIKE reservation.depositbez  
    FIELD depositbez2       LIKE reservation.depositbez2  
    FIELD bestat-dat        AS DATE  
    FIELD briefnr           LIKE reservation.briefnr  
    FIELD rsv-gastnr        LIKE reservation.gastnr  
    FIELD rsv-resnr         LIKE reservation.resnr  
    FIELD rsv-bemerk        LIKE reservation.bemerk  
    FIELD rsv-grpflag       LIKE reservation.grpflag 
    FIELD recid-resline     AS INT  
    FIELD address           AS CHARACTER 
    FIELD city              AS CHAR  
    FIELD comments          AS CHAR        
    FIELD resnr-fgcol       AS INT INIT -1  
    FIELD mc-str-fgcol      AS INT INIT -1  
    FIELD mc-str-bgcol      AS INT INIT -1  
    FIELD rsv-name-fgcol    AS INT INIT -1  
    FIELD rsv-name-bgcol    AS INT INIT -1  
    FIELD zinr-fgcol        AS INT INIT -1  
    FIELD reslin-name-fgcol AS INT INIT -1  
    FIELD ankunft-fgcol     AS INT INIT -1  
    FIELD anztage-fgcol     AS INT INIT -1  
    FIELD abreise-fgcol     AS INT INIT -1  
    FIELD segmentcode-fgcol AS INT INIT -1  
    FIELD reslin-name-bgcol AS INT INIT -1  
    FIELD segmentcode-bgcol AS INT INIT -1  
    FIELD zinr-bgcol        AS INT INIT -1
    FIELD webci             AS CHAR
    FIELD webci-flag        AS CHAR
    FIELD voucher-flag      AS CHAR
    FIELD kontignr-flag     AS CHAR
    FIELD birthday-flag     AS LOGICAL
    FIELD sharer-no         AS INTEGER.  

DEFINE TEMP-TABLE b-arl-list  
    FIELD resnr             LIKE res-line.resnr  
    FIELD reslinnr          LIKE res-line.reslinnr  
    FIELD resline-wabkurz   LIKE res-line.wabkurz  
    FIELD voucher-nr        LIKE res-line.voucher-nr  
    FIELD grpflag           LIKE reservation.grpflag  
    FIELD verstat           LIKE reservation.verstat  
    FIELD l-zuordnung2      AS INTEGER  
    FIELD kontignr          LIKE res-line.kontignr  
    FIELD firmen-nr         AS INTEGER  
    FIELD steuernr          AS CHARACTER 
    FIELD rsv-name          AS CHARACTER FORMAT "x(120)"
    FIELD zinr              LIKE res-line.zinr  
    FIELD setup-list-char   AS CHARACTER  
    FIELD resline-name      LIKE res-line.name  
    FIELD waehrung-wabkurz  LIKE waehrung.wabkurz  
    FIELD segmentcode       LIKE reservation.segmentcode  
    FIELD ankunft           LIKE res-line.ankunft  
    FIELD abreise           LIKE res-line.abreise  
    FIELD zimmeranz         LIKE res-line.zimmeranz  
    FIELD kurzbez           LIKE zimkateg.kurzbez  
    FIELD arrangement       LIKE res-line.arrangement  
    FIELD zipreis           LIKE res-line.zipreis  
    FIELD anztage           LIKE res-line.anztage  
    FIELD erwachs           LIKE res-line.erwachs  
    FIELD kind1             LIKE res-line.kind1  
    FIELD kind2             LIKE res-line.kind2  
    FIELD gratis            LIKE res-line.gratis  
    FIELD l-zuordnung4      AS INTEGER  
    FIELD resstatus         LIKE res-line.resstatus  
    FIELD l-zuordnung3      AS INTEGER  
    FIELD flight-nr         LIKE res-line.flight-nr  
    FIELD ankzeit           LIKE res-line.ankzeit  
    FIELD abreisezeit       LIKE res-line.abreisezeit  
    FIELD betrieb-gast      LIKE res-line.betrieb-gast  
    FIELD resdat            LIKE reservation.resdat  
    FIELD useridanlage      LIKE reservation.useridanlage  
    FIELD reserve-dec       LIKE res-line.reserve-dec  
    FIELD cancelled-id      LIKE res-line.cancelled-id  
    FIELD changed-id        LIKE res-line.changed-id  
    FIELD groupname         LIKE reservation.groupname    
    FIELD active-flag       LIKE res-line.active-flag  
    FIELD gastnr            LIKE res-line.gastnr      
    FIELD gastnrmember      LIKE res-line.gastnrmember  
    FIELD karteityp         AS INTEGER    
    FIELD reserve-int       LIKE res-line.reserve-int
    FIELD zikatnr           LIKE res-line.zikatnr  
    FIELD betrieb-gastmem   LIKE res-line.betrieb-gastmem  
    FIELD pseudofix         LIKE res-line.pseudofix  
    FIELD reserve-char      LIKE res-line.reserve-char  
    FIELD bemerk            LIKE res-line.bemerk    
    FIELD depositbez        LIKE reservation.depositbez  
    FIELD depositbez2       LIKE reservation.depositbez2  
    FIELD bestat-dat        AS DATE  
    FIELD briefnr           LIKE reservation.briefnr  
    FIELD rsv-gastnr        LIKE reservation.gastnr  
    FIELD rsv-resnr         LIKE reservation.resnr  
    FIELD rsv-bemerk        LIKE reservation.bemerk  
    FIELD rsv-grpflag       LIKE reservation.grpflag 
    FIELD recid-resline     AS INT  
    FIELD address           AS CHARACTER 
    FIELD city              AS CHAR  
    FIELD comments          AS CHAR        
    FIELD resnr-fgcol       AS INT INIT -1  
    FIELD mc-str-fgcol      AS INT INIT -1  
    FIELD mc-str-bgcol      AS INT INIT -1  
    FIELD rsv-name-fgcol    AS INT INIT -1  
    FIELD rsv-name-bgcol    AS INT INIT -1  
    FIELD zinr-fgcol        AS INT INIT -1  
    FIELD reslin-name-fgcol AS INT INIT -1  
    FIELD ankunft-fgcol     AS INT INIT -1  
    FIELD anztage-fgcol     AS INT INIT -1  
    FIELD abreise-fgcol     AS INT INIT -1  
    FIELD segmentcode-fgcol AS INT INIT -1  
    FIELD reslin-name-bgcol AS INT INIT -1  
    FIELD segmentcode-bgcol AS INT INIT -1  
    FIELD zinr-bgcol        AS INT INIT -1
    FIELD webci             AS CHAR
    FIELD webci-flag        AS CHAR
    FIELD voucher-flag      AS CHAR
    FIELD kontignr-flag     AS CHAR
    FIELD birthday-flag     AS LOGICAL
    FIELD sharer-no         AS INTEGER.  
  
CREATE setup-list.   
setup-list.nr = 1.   
setup-list.char = " ".   
   
FOR EACH paramtext WHERE paramtext.txtnr GE 9201   
    AND paramtext.txtnr LE 9299 NO-LOCK:   
    CREATE setup-list.   
    setup-list.nr = paramtext.txtnr - 9199.   
    setup-list.char = SUBSTR(paramtext.notes,1,1).  
END.   
  
DEFINE INPUT  PARAMETER show-rate    AS LOGICAL.  
DEFINE INPUT  PARAMETER last-sort    AS INT.  
DEFINE INPUT  PARAMETER lresnr       AS INT.  
DEFINE INPUT  PARAMETER long-stay    AS INT.  
  
DEFINE INPUT  PARAMETER ci-date      AS DATE.  
DEFINE INPUT  PARAMETER grpFlag      AS LOGICAL.  
DEFINE INPUT  PARAMETER room         AS CHAR.  
DEFINE INPUT  PARAMETER lname        AS CHAR.  
DEFINE INPUT  PARAMETER sorttype     AS INT.  
DEFINE INPUT-OUTPUT  PARAMETER fdate1       AS DATE.  
DEFINE INPUT-OUTPUT  PARAMETER fdate2       AS DATE.  
DEFINE INPUT  PARAMETER fdate        AS DATE.  
DEFINE INPUT  PARAMETER excl-rmshare AS LOGICAL.
  
DEFINE OUTPUT PARAMETER rmlen        AS INTEGER.  
DEFINE OUTPUT PARAMETER TABLE FOR arl-list.  

DEFINE VARIABLE vipnr1 AS INTEGER INITIAL 999999999.   
DEFINE VARIABLE vipnr2 AS INTEGER INITIAL 999999999.   
DEFINE VARIABLE vipnr3 AS INTEGER INITIAL 999999999.   
DEFINE VARIABLE vipnr4 AS INTEGER INITIAL 999999999.   
DEFINE VARIABLE vipnr5 AS INTEGER INITIAL 999999999.   
DEFINE VARIABLE vipnr6 AS INTEGER INITIAL 999999999.   
DEFINE VARIABLE vipnr7 AS INTEGER INITIAL 999999999.   
DEFINE VARIABLE vipnr8 AS INTEGER INITIAL 999999999.   
DEFINE VARIABLE vipnr9 AS INTEGER INITIAL 999999999.   
  
DEF VARIABLE done-flag    AS LOGICAL NO-UNDO.
DEF VARIABLE curr-resnr   AS INTEGER NO-UNDO INIT 0.
DEF VARIABLE curr-resline AS INTEGER NO-UNDO.
DEF VARIABLE today-str    AS CHAR    NO-UNDO.
DEF VARIABLE reserve-str  AS CHAR    NO-UNDO.
DEF VARIABLE created-time AS INTEGER NO-UNDO.
DEF VARIABLE do-it        AS LOGICAL NO-UNDO INIT YES.
DEF VARIABLE loop-i       AS INTEGER NO-UNDO INIT 0.
DEF VARIABLE comment-str  AS CHAR    NO-UNDO.

DEF VAR all-inclusive     AS CHAR    NO-UNDO.  
DEF VAR res-mode          AS CHAR    NO-UNDO.  
DEF VAR checkin-flag      AS LOGICAL NO-UNDO INIT NO.

DEFINE VARIABLE stay      AS INTEGER NO-UNDO.
DEFINE VARIABLE resbemerk AS CHAR    NO-UNDO.  
DEFINE VARIABLE rescomment AS CHAR    NO-UNDO.  

FUNCTION get-toname RETURNS CHAR (INPUT lname AS CHAR) :   
    RETURN CHR(ASC(SUBSTR(lname,1,1)) + 1).   
END FUNCTION.   
  
DEFINE BUFFER gmember FOR guest.

/* DODY - 09 AUG 2018 : REPEATER GUEST ARTOTEL*/
FIND FIRST htparam WHERE htparam.paramnr = 458 NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN
DO:
    stay = htparam.finteger.
END.

/* ST 09 AUG 2015: fixing all res-line.resname = "" */
RUN fixing-blank-resname.

PROCEDURE fixing-blank-resname:
DEF BUFFER rline FOR res-line.
    FIND FIRST res-line WHERE res-line.active-flag LE 1
        AND res-line.resstatus NE 12 
        AND res-line.resname = "" NO-LOCK NO-ERROR.
    DO WHILE AVAILABLE res-line:
        FIND FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK.
        DO TRANSACTION:
            FIND FIRST rline WHERE RECID(rline) = RECID(res-line)
                EXCLUSIVE-LOCK NO-WAIT NO-ERROR.
            IF AVAILABLE rline THEN
            DO:
              ASSIGN rline.resname = guest.NAME.
              FIND CURRENT rline NO-LOCK.
              RELEASE rline.
            END.
        END.
        FIND NEXT res-line WHERE res-line.active-flag LE 1
            AND res-line.resstatus NE 12 
            AND res-line.resname = "" NO-LOCK NO-ERROR.
    END.
END.

/* SY: check if there is new room sharer exists in the last 70 sec
   due to btn-chg. or current res-line was deleted thru mi-reservation,
   or the arrival guest has been checked-in in mk-resline.
   if yes then build new arl-list, otherwise only b1:refresh 
*/
IF NUM-ENTRIES(room, CHR(2)) GT 1 THEN
DO:
  ASSIGN
      do-it        = NO
      curr-resnr   = INTEGER(ENTRY(2, room, CHR(2)))
      curr-resline = INTEGER(ENTRY(3, room, CHR(2)))
      today-str    = STRING(TODAY)
      res-mode     = TRIM(ENTRY(4, room, CHR(2))) NO-ERROR
  .
  ASSIGN room = ENTRY(1, room, CHR(2)).

  FIND FIRST res-line WHERE res-line.resnr = curr-resnr
      AND res-line.reslinnr = curr-resline NO-LOCK NO-ERROR.

  IF NOT AVAILABLE res-line THEN do-it = YES.   /* deleted */
  ELSE 
  DO:    
    IF res-line.active-flag = 1 AND res-mode = "modify" THEN 
      do-it = YES. /* guest checked-in */
    ELSE
    FOR EACH res-line WHERE res-line.resnr = curr-resnr
      AND res-line.active-flag LE 1 NO-LOCK:
      reserve-str  = res-line.reserve-char.
      IF today-str = SUBSTR(reserve-str,1,8) THEN
      DO:
        ASSIGN
          reserve-str  = SUBSTR(reserve-str, 9)
          created-time = INTEGER(SUBSTR(reserve-str,1,2)) * 3600
                       + INTEGER(SUBSTR(reserve-str,4,2)) * 60
        .
        IF created-time GE (TIME - 70) THEN /* room sharer created */
        DO:
            do-it = YES.
            LEAVE.
        END.
      END.
    END.
  END.
END.
IF NOT do-it THEN RETURN.

RUN get-vipnrbl.p  
    (OUTPUT vipnr1, OUTPUT vipnr2, OUTPUT vipnr3, OUTPUT vipnr4,  
     OUTPUT vipnr5, OUTPUT vipnr6, OUTPUT vipnr7, OUTPUT vipnr8,  
     OUTPUT vipnr9).  
 
RUN disp-arlist1.  
  
/* SY 01 JUL 2017 */
IF grpFlag THEN RUN disp-arlist-group.  

PROCEDURE disp-arlist-group:  
DEF BUFFER arlbuff FOR arl-list.
    IF lname NE "" THEN lname = "*" + lname + "*".  
    ELSE RETURN.

    IF sorttype = 1 THEN  /* Reservation  */ 
    FOR EACH res-line WHERE   
        res-line.active-flag = 0 AND res-line.ankunft GE fdate1   
        AND res-line.ankunft LE fdate2   
        AND res-line.resstatus NE 9 AND res-line.resstatus NE 10  
        AND res-line.resstatus NE 99 NO-LOCK,
        FIRST gbuff WHERE gbuff.gastnr = res-line.gastnr NO-LOCK,  
        FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr   
        NO-LOCK,   
        FIRST reservation WHERE reservation.resnr = res-line.resnr   
          AND reservation.groupname MATCHES(lname) NO-LOCK,   
        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,   
        FIRST setup-list WHERE setup-list.nr = res-line.setup + 1   
        NO-LOCK BY res-line.name:  
        FIND FIRST arlbuff WHERE arlbuff.resnr = res-line.resnr
            AND arlbuff.reslinnr = res-line.reslinnr NO-ERROR.
        IF NOT AVAILABLE arlbuff THEN RUN create-it.  
    END.  
    ELSE IF sorttype = 2 THEN   /* In-house Guests SPEED SOFAR OK ********/   
    FOR EACH res-line WHERE   
        res-line.active-flag = 1 AND res-line.resstatus NE 12 
        AND res-line.resstatus NE 99  
        AND res-line.ankunft LE ci-date AND res-line.abreise GE ci-date,   
        FIRST gbuff WHERE gbuff.gastnr = res-line.gastnr NO-LOCK,  
        FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr   
        NO-LOCK,   
        FIRST reservation WHERE reservation.resnr = res-line.resnr  
          AND reservation.groupname MATCHES(lname) NO-LOCK,   
        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr,   
        FIRST setup-list WHERE setup-list.nr = res-line.setup + 1   
        NO-LOCK BY res-line.zinr  
        BY (res-line.kontakt-nr * res-line.resnr) BY res-line.resstatus BY res-line.NAME:  
        FIND FIRST arlbuff WHERE arlbuff.resnr = res-line.resnr
            AND arlbuff.reslinnr = res-line.reslinnr NO-ERROR.
        IF NOT AVAILABLE arlbuff THEN RUN create-it.  
    END.  
    ELSE IF sorttype = 3 THEN   /* Arrival TODAY */   
    FOR EACH res-line WHERE   
        res-line.active-flag = 0 AND res-line.ankunft = ci-date   
        AND res-line.resstatus NE 9 AND res-line.resstatus NE 10 
        AND res-line.resstatus NE 99 NO-LOCK,   
        FIRST gbuff WHERE gbuff.gastnr = res-line.gastnr NO-LOCK,  
        FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr   
        NO-LOCK,   
        FIRST reservation WHERE reservation.resnr = res-line.resnr  
          AND reservation.groupname MATCHES(lname) NO-LOCK,   
        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr,   
        FIRST setup-list WHERE setup-list.nr = res-line.setup + 1   
        NO-LOCK BY res-line.name BY res-line.zinr:  
        FIND FIRST arlbuff WHERE arlbuff.resnr = res-line.resnr
            AND arlbuff.reslinnr = res-line.reslinnr NO-ERROR.
        IF NOT AVAILABLE arlbuff THEN RUN create-it.  
    END.  
    ELSE IF sorttype = 4 THEN   /* Departure TODAY */   
    FOR EACH res-line WHERE   
        res-line.active-flag = 1 AND res-line.resstatus NE 12 
        AND res-line.resstatus NE 99
        AND res-line.abreise = fdate NO-LOCK,   
        FIRST gbuff WHERE gbuff.gastnr = res-line.gastnr NO-LOCK,  
        FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr   
          NO-LOCK,   
        FIRST reservation WHERE reservation.resnr = res-line.resnr  
          AND reservation.groupname MATCHES(lname) NO-LOCK,   
        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr,   
        FIRST setup-list WHERE setup-list.nr = res-line.setup + 1   
        NO-LOCK BY res-line.name BY res-line.zinr:  
        FIND FIRST arlbuff WHERE arlbuff.resnr = res-line.resnr
            AND arlbuff.reslinnr = res-line.reslinnr NO-ERROR.
        IF NOT AVAILABLE arlbuff THEN RUN create-it.  
    END.  
END.   

/*FDL June 28, 2023 => 937FC7*/
FOR EACH arl-list NO-LOCK BY arl-list.zinr 
    BY arl-list.sharer-no:
    CREATE b-arl-list.
    BUFFER-COPY arl-list TO b-arl-list.
END.

EMPTY TEMP-TABLE arl-list.

FOR EACH b-arl-list NO-LOCK:
    CREATE arl-list.
    BUFFER-COPY b-arl-list TO arl-list. 

    /*MASDOD 280623 Fixing ARL Data not display all*/
    resbemerk = b-arl-list.bemerk.
    resbemerk = REPLACE(resbemerk,CHR(10),"").
    resbemerk = REPLACE(resbemerk,CHR(13),"").
    resbemerk = REPLACE(resbemerk,"~n","").
    resbemerk = REPLACE(resbemerk,"\n","").
    resbemerk = REPLACE(resbemerk,"~r","").
    resbemerk = REPLACE(resbemerk,"~r~n","").
    resbemerk = REPLACE(resbemerk,CHR(10) + CHR(13),"").

    IF LENGTH(resbemerk) LT 3 THEN resbemerk = REPLACE(resbemerk,CHR(32),"").
    IF LENGTH(resbemerk) EQ ? THEN resbemerk = "".

    arl-list.bemerk = TRIM(resbemerk).
    resbemerk = "".

    /*MASDOD 280623 Fixing ARL Data not display all*/
    rescomment = b-arl-list.comments.
    rescomment = REPLACE(rescomment,CHR(10),"").
    rescomment = REPLACE(rescomment,CHR(13),"").
    rescomment = REPLACE(rescomment,"~n","").
    rescomment = REPLACE(rescomment,"\n","").
    rescomment = REPLACE(rescomment,"~r","").
    rescomment = REPLACE(rescomment,"~r~n","").
    rescomment = REPLACE(rescomment,CHR(10) + CHR(13),"").

    IF LENGTH(rescomment) LT 3 THEN rescomment = REPLACE(rescomment,CHR(32),"").
    IF LENGTH(rescomment) EQ ? THEN rescomment = "".

    arl-list.comments = TRIM(rescomment).
    rescomment = "".

END.
/*End FDL*/

/*FDL Sept 18, 2023 => Ticket 6222E1*/
IF excl-rmshare THEN
DO:
    FOR EACH arl-list WHERE arl-list.resstatus EQ 11 OR arl-list.resstatus EQ 13 NO-LOCK:
        DELETE arl-list.
    END.
END.

PROCEDURE disp-arlist1:  
DEFINE VARIABLE to-name     AS CHAR    INITIAL ""   NO-UNDO.   
DEFINE VARIABLE iGrpname    AS INTEGER INITIAL 0    NO-UNDO.  
  
  ASSIGN  
    iGrpname = INTEGER(grpFlag)  
    rmlen    = LENGTH(room)  
  .   
  IF lname NE "" THEN   
  DO:  
    IF SUBSTR(lname,1,1) = "*" THEN  
    DO:  
      IF SUBSTR(lname, LENGTH(lname), 1) NE "*" THEN  
          lname = lname + "*".  
    END.  
    ELSE to-name = get-toname(lname).   
  END.  
  
  IF sorttype = 1 THEN  /* Reservation  */ RUN disp-arriveA.   
  ELSE IF sorttype = 2 THEN   /* In-house Guests SPEED SOFAR OK ********/   
  DO:   
    IF last-sort = 1 THEN   
    DO:   
      IF room NE "" THEN   
      DO:   
        IF lname = "" THEN   
        FOR EACH res-line WHERE   
            active-flag = 1 AND resstatus NE 12 AND resstatus NE 99 
            AND (SUBSTR(res-line.zinr,1,INTEGER(rmlen))) GE (room)   
            AND res-line.ankunft LE ci-date AND res-line.abreise GE ci-date,   
            FIRST gbuff WHERE gbuff.gastnr = res-line.gastnr NO-LOCK,  
            FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr   
            NO-LOCK,   
            FIRST reservation WHERE reservation.resnr = res-line.resnr  
              AND LENGTH(reservation.groupname) GE iGrpname NO-LOCK,  
            FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,   
            FIRST setup-list WHERE setup-list.nr = res-line.setup + 1   
            NO-LOCK BY res-line.zinr  
            BY (res-line.kontakt-nr * res-line.resnr) BY res-line.resstatus BY res-line.NAME:  
            RUN create-it.  
        END.  
        ELSE IF lname NE "" AND SUBSTR(lname,1,1) NE "*" THEN   
        FOR EACH res-line WHERE   
            active-flag = 1 AND resstatus NE 12 AND resstatus NE 99
            AND (SUBSTR(res-line.zinr,1,INTEGER(rmlen))) GE (room)   
            /*AND res-line.name GE lname AND res-line.name LE to-name*/
            AND res-line.name MATCHES("*" + lname + "*")                            /*FDL Ticket 72FF79 | 0609D3*/
            AND res-line.ankunft LE ci-date AND res-line.abreise GE ci-date,   
            FIRST gbuff WHERE gbuff.gastnr = res-line.gastnr NO-LOCK,  
            FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr   
            NO-LOCK,   
            FIRST reservation WHERE reservation.resnr = res-line.resnr  
              AND LENGTH(reservation.groupname) GE iGrpname NO-LOCK,   
            FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr,   
            FIRST setup-list WHERE setup-list.nr = res-line.setup + 1   
            NO-LOCK BY res-line.zinr  
            BY (res-line.kontakt-nr * res-line.resnr) BY res-line.resstatus BY res-line.NAME:  
            RUN create-it.  
        END.  
        ELSE IF lname NE "" AND SUBSTR(lname,1,1) EQ "*" THEN   
        FOR EACH res-line WHERE   
            active-flag = 1 AND resstatus NE 12 AND resstatus NE 99  
            AND (SUBSTR(res-line.zinr,1,INTEGER(rmlen))) GE (room)   
            AND res-line.name MATCHES(lname)   
            AND res-line.ankunft LE ci-date AND res-line.abreise GE ci-date,   
            FIRST gbuff WHERE gbuff.gastnr = res-line.gastnr NO-LOCK,  
            FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr   
            NO-LOCK,   
            FIRST reservation WHERE reservation.resnr = res-line.resnr  
              AND LENGTH(reservation.groupname) GE iGrpname NO-LOCK,   
            FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr,   
            FIRST setup-list WHERE setup-list.nr = res-line.setup + 1   
            NO-LOCK BY res-line.zinr  
            BY (res-line.kontakt-nr * res-line.resnr) BY res-line.resstatus BY res-line.NAME:  
            RUN create-it.  
        END.  
      END.   
      ELSE IF room = "" THEN   
      DO:   
        IF lname = "" THEN   
        FOR EACH res-line WHERE   
            active-flag = 1 AND resstatus NE 12 AND resstatus NE 99
            AND (SUBSTR(res-line.zinr,1,INTEGER(rmlen))) GE (room)   
            AND res-line.ankunft LE ci-date AND res-line.abreise GE ci-date,   
            FIRST gbuff WHERE gbuff.gastnr = res-line.gastnr NO-LOCK,  
            FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr   
            NO-LOCK,   
            FIRST reservation WHERE reservation.resnr = res-line.resnr   
              AND LENGTH(reservation.groupname) GE iGrpname NO-LOCK,   
            FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr,   
            FIRST setup-list WHERE setup-list.nr = res-line.setup + 1   
            NO-LOCK BY (res-line.kontakt-nr * res-line.resnr) BY res-line.resstatus BY res-line.NAME:  
            RUN create-it.  
        END.  
        ELSE IF lname NE "" AND SUBSTR(lname,1,1) NE "*" THEN   
        FOR EACH res-line WHERE   
            active-flag = 1 AND resstatus NE 12 AND resstatus NE 99
            /*AND res-line.name GE lname AND res-line.name LE to-name*/
            AND res-line.name MATCHES(lname)                                /*FDL Ticket 72FF79 | 0609D3*/
            AND (SUBSTR(res-line.zinr,1,INTEGER(rmlen))) GE (room)   
            AND res-line.ankunft LE ci-date AND res-line.abreise GE ci-date,   
            FIRST gbuff WHERE gbuff.gastnr = res-line.gastnr NO-LOCK,  
            FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr   
            NO-LOCK,   
            FIRST reservation WHERE reservation.resnr = res-line.resnr  
              AND LENGTH(reservation.groupname) GE iGrpname NO-LOCK,   
            FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr,   
            FIRST setup-list WHERE setup-list.nr = res-line.setup + 1   
            NO-LOCK BY res-line.name:  
            RUN create-it.  
        END.  
        ELSE IF lname NE "" AND SUBSTR(lname,1,1) EQ "*" THEN   
        FOR EACH res-line WHERE   
            active-flag = 1 AND resstatus NE 12 AND resstatus NE 99
            AND res-line.name MATCHES(lname) AND (SUBSTR(res-line.zinr,1,   
            INTEGER(rmlen))) GE (room)   
            AND res-line.ankunft LE ci-date AND res-line.abreise GE ci-date,   
            FIRST gbuff WHERE gbuff.gastnr = res-line.gastnr NO-LOCK,  
            FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr   
            NO-LOCK,   
            FIRST reservation WHERE reservation.resnr = res-line.resnr  
              AND LENGTH(reservation.groupname) GE iGrpname NO-LOCK,   
            FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr,   
            FIRST setup-list WHERE setup-list.nr = res-line.setup + 1   
            NO-LOCK BY res-line.name:  
            RUN create-it.  
        END.  
      END.   
    END.   
    IF last-sort = 2 THEN RUN sqry2.   
    ELSE IF last-sort = 3 THEN RUN sqry3.   
    ELSE IF last-sort = 4 THEN RUN sqry4.   
    ELSE IF last-sort = 5 THEN RUN sqry5.   
  END.   
  ELSE IF sorttype = 3 THEN   /* Arrival TODAY */   
  DO:   
    IF last-sort = 1 THEN   
    DO:   
      IF lname = "" THEN   
      DO:   
        IF room = "" THEN   
        FOR EACH res-line WHERE   
            active-flag = 0 AND res-line.ankunft = ci-date   
            AND (SUBSTR(res-line.zinr,1,INTEGER(rmlen))) GE (room)   
            AND res-line.resstatus NE 9 AND res-line.resstatus NE 10
            AND res-line.resstatus NE 99
            NO-LOCK,   
            FIRST gbuff WHERE gbuff.gastnr = res-line.gastnr NO-LOCK,  
            FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr   
            NO-LOCK,   
            FIRST reservation WHERE reservation.resnr = res-line.resnr  
              AND LENGTH(reservation.groupname) GE iGrpname NO-LOCK,   
            FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr,   
            FIRST setup-list WHERE setup-list.nr = res-line.setup + 1   
            NO-LOCK /* BY res-line.zinr */  
            BY (res-line.kontakt-nr * res-line.resnr) BY res-line.resstatus BY res-line.NAME:  
            RUN create-it.  
        END.  
        ELSE IF room NE "" THEN   
        FOR EACH res-line WHERE   
            active-flag = 0 AND res-line.ankunft = ci-date   
            AND (SUBSTR(res-line.zinr,1,INTEGER(rmlen))) GE (room)   
            AND res-line.resstatus NE 9 AND res-line.resstatus NE 10  
            AND res-line.resstatus NE 99 NO-LOCK,   
            FIRST gbuff WHERE gbuff.gastnr = res-line.gastnr NO-LOCK,  
            FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr   
            NO-LOCK,   
            FIRST reservation WHERE reservation.resnr = res-line.resnr  
              AND LENGTH(reservation.groupname) GE iGrpname NO-LOCK,   
            FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr,   
            FIRST setup-list WHERE setup-list.nr = res-line.setup + 1   
            NO-LOCK BY res-line.zinr  
            BY (res-line.kontakt-nr * res-line.resnr) BY res-line.resstatus BY res-line.NAME:  
            RUN create-it.  
        END.  
      END.   
      ELSE IF lname NE "" AND SUBSTR(lname,1,1) NE "*" THEN   
      FOR EACH res-line WHERE   
          active-flag = 0 AND res-line.ankunft = ci-date   
          /*AND res-line.name GE lname AND res-line.name LE to-name*/
          AND res-line.name MATCHES("*" + lname + "*")                            /*FDL Ticket 72FF79 | 0609D3*/
          AND (SUBSTR(res-line.zinr,1,INTEGER(rmlen))) GE (room)   
          AND res-line.resstatus NE 9 AND res-line.resstatus NE 10 
          AND res-line.resstatus NE 99 NO-LOCK,   
          FIRST gbuff WHERE gbuff.gastnr = res-line.gastnr NO-LOCK,  
          FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr   
          NO-LOCK,   
          FIRST reservation WHERE reservation.resnr = res-line.resnr  
            AND LENGTH(reservation.groupname) GE iGrpname NO-LOCK,   
          FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr,   
          FIRST setup-list WHERE setup-list.nr = res-line.setup + 1   
          NO-LOCK BY res-line.name BY res-line.zinr:  
          RUN create-it.  
      END.  
      ELSE IF SUBSTR(lname,1,1) EQ "*" THEN   
      FOR EACH res-line WHERE   
          active-flag = 0 AND res-line.ankunft = ci-date   
          AND (SUBSTR(res-line.zinr,1,INTEGER(rmlen))) GE (room)   
          AND res-line.name MATCHES(lname)   
          AND res-line.resstatus NE 9 AND res-line.resstatus NE 10
          AND res-line.resstatus NE 99 NO-LOCK,   
          FIRST gbuff WHERE gbuff.gastnr = res-line.gastnr NO-LOCK,  
          FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr   
          NO-LOCK,   
          FIRST reservation WHERE reservation.resnr = res-line.resnr  
            AND LENGTH(reservation.groupname) GE iGrpname NO-LOCK,   
          FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr,   
          FIRST setup-list WHERE setup-list.nr = res-line.setup + 1   
          NO-LOCK BY res-line.name BY res-line.zinr:  
          RUN create-it.  
      END.  
    END.   
    ELSE IF last-sort = 2 THEN  RUN sqry2.   
    ELSE IF last-sort = 3 THEN RUN sqry3.   
    ELSE IF last-sort = 4 THEN RUN sqry4.   
    ELSE IF last-sort = 5 THEN RUN sqry5.   
  END.   
  ELSE IF sorttype = 4 THEN   /* Departure TODAY */   
  DO:   
    IF last-sort = 1 THEN   
    DO:   
      IF lname = "" THEN   
      DO:   
        IF room = "" THEN   
        FOR EACH res-line WHERE   
            active-flag = 1 AND res-line.resstatus NE 12
            AND res-line.resstatus NE 99
            AND res-line.abreise = fdate   
            AND (SUBSTR(res-line.zinr,1,INTEGER(rmlen))) GE (room)   
            NO-LOCK,   
            FIRST gbuff WHERE gbuff.gastnr = res-line.gastnr NO-LOCK,  
            FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr   
            NO-LOCK,   
            FIRST reservation WHERE reservation.resnr = res-line.resnr  
              AND LENGTH(reservation.groupname) GE iGrpname NO-LOCK,   
            FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr,   
            FIRST setup-list WHERE setup-list.nr = res-line.setup + 1   
            NO-LOCK BY res-line.zinr  
            BY (res-line.kontakt-nr * res-line.resnr) BY res-line.resstatus BY res-line.NAME:  
            RUN create-it.  
        END.  
        ELSE IF room NE "" THEN   
        FOR EACH res-line WHERE   
            active-flag = 1 AND res-line.resstatus NE 12 
            AND res-line.resstatus NE 99
            AND res-line.abreise = fdate   
            AND (SUBSTR(res-line.zinr,1,INTEGER(rmlen))) GE (room)   
            NO-LOCK,   
            FIRST gbuff WHERE gbuff.gastnr = res-line.gastnr NO-LOCK,  
            FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr   
            NO-LOCK,   
            FIRST reservation WHERE reservation.resnr = res-line.resnr   
              AND LENGTH(reservation.groupname) GE iGrpname NO-LOCK,   
            FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr,   
            FIRST setup-list WHERE setup-list.nr = res-line.setup + 1   
            NO-LOCK BY res-line.zinr  
            BY (res-line.kontakt-nr * res-line.resnr) BY res-line.resstatus BY res-line.NAME:  
            RUN create-it.  
        END.  
      END.   
      ELSE IF lname NE "" AND SUBSTR(lname,1,1) NE "*" THEN   
      FOR EACH res-line WHERE   
          active-flag = 1 AND res-line.resstatus NE 12 
          AND res-line.resstatus NE 99
          AND res-line.abreise = fdate   
          /*AND res-line.name GE lname AND res-line.name LE to-name*/
          AND res-line.name MATCHES("*" + lname + "*")                            /*FDL Ticket 72FF79 | 0609D3*/
          AND (SUBSTR(res-line.zinr,1,INTEGER(rmlen))) GE (room)   
          NO-LOCK,   
          FIRST gbuff WHERE gbuff.gastnr = res-line.gastnr NO-LOCK,  
          FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr   
          NO-LOCK,   
          FIRST reservation WHERE reservation.resnr = res-line.resnr  
            AND LENGTH(reservation.groupname) GE iGrpname NO-LOCK,   
          FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr,   
          FIRST setup-list WHERE setup-list.nr = res-line.setup + 1   
          NO-LOCK BY res-line.name BY res-line.zinr:  
          RUN create-it.  
      END.  
      ELSE IF SUBSTR(lname,1,1) EQ "*" THEN   
      FOR EACH res-line WHERE   
          active-flag = 1 AND res-line.resstatus NE 12  
          AND res-line.resstatus NE 99
          AND res-line.abreise = fdate   
          AND res-line.name MATCHES(lname)   
          AND (SUBSTR(res-line.zinr,1,INTEGER(rmlen))) GE (room)   
          NO-LOCK,   
          FIRST gbuff WHERE gbuff.gastnr = res-line.gastnr NO-LOCK,  
          FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr   
          NO-LOCK,   
          FIRST reservation WHERE reservation.resnr = res-line.resnr  
            AND LENGTH(reservation.groupname) GE iGrpname NO-LOCK,   
          FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr,   
          FIRST setup-list WHERE setup-list.nr = res-line.setup + 1   
          NO-LOCK BY res-line.name BY res-line.zinr:  
          RUN create-it.  
      END.  
    END.   
    ELSE IF last-sort = 2 THEN RUN sqry2.   
    ELSE IF last-sort = 3 THEN RUN sqry3.   
    ELSE IF last-sort = 4 THEN RUN sqry4.   
    ELSE IF last-sort = 5 THEN RUN sqry5.   
  END.   
   
  /*MT  
  ASSIGN  
    tot-rm  = 0   
    tot-pax = 0   
    tot-com = 0   
    tot-ch1 = 0   
    tot-ch2 = 0  
    tot-ch3 = 0  
    tot-kcard = 0  
  .   
  GET FIRST q1 NO-LOCK.   
  DO WHILE AVAILABLE res-line:   
    IF res-line.resstatus NE 11 AND res-line.resstatus NE 13 THEN   
      tot-rm = tot-rm + res-line.zimmeranz.   
    ASSIGN  
      tot-pax = tot-pax + res-line.erwachs * res-line.zimmeranz  
      tot-com = tot-com + res-line.gratis * res-line.zimmeranz   
      tot-ch1 = tot-ch1 + res-line.kind1 * res-line.zimmeranz   
      tot-ch2 = tot-ch2 + res-line.kind2 * res-line.zimmeranz   
      tot-ch3 = tot-ch3 + res-line.l-zuordnung[4] * res-line.zimmeranz  
      tot-kcard = tot-kcard + res-line.betrieb-gast  
    .   
    GET NEXT q1 NO-LOCK.   
  END.   
  GET FIRST q1 NO-LOCK.   
  DISP tot-rm tot-pax tot-com tot-ch1 tot-ch2 tot-ch3 tot-kcard  
      WITH FRAME f-reserve.   
   
  IF AVAILABLE res-line THEN   
  DO:   
    IF res-line.active-flag = 0 AND res-line.ankunft = ci-date   
      AND res-line.resstatus NE 9 AND res-line.resstatus NE 10 THEN   
      ENABLE btn-checkin WITH FRAME f-reserve.   
    FIND FIRST reservation WHERE reservation.resnr = res-line.resnr   
      /*and reservation.gastnr = res-line.gastnr*/ NO-LOCK NO-ERROR.   
    IF AVAILABLE reservation THEN   
    DO:   
      resname = reservation.name.   
      FIND FIRST guest WHERE guest.gastnr = reservation.gastnr NO-LOCK NO-ERROR.   
      address = guest.adresse1.   
      city = guest.wohnort + " " + guest.plz.   
      RUN disp-comments.   
    END.   
  END.   
  */  
  /*MTRUN check-message. */  
END.   
  
PROCEDURE disp-arriveA:   
DEFINE VARIABLE to-name     AS CHAR    INITIAL ""   NO-UNDO.   
DEFINE VARIABLE iGrpname    AS INTEGER INITIAL 0    NO-UNDO.  
  
  ASSIGN iGrpname = INTEGER(grpFlag).  
    
  IF lname NE "" AND SUBSTR(lname,1,1) NE "*" THEN   
    to-name = get-toname(lname).   
  
  DO:   
    IF last-sort = 1 THEN /********* SPEED OK *****************/   
    DO:   
      IF fdate1 = ? OR fdate2 = ? THEN   
      DO:   
        fdate1 = ci-date.   
        fdate2 = ci-date + 365.   
        /*MTDISP fdate1 fdate2 WITH FRAME f-reserve.*/  
      END.   

      IF lname EQ "" THEN   
      FOR EACH res-line WHERE   
          active-flag = 0 AND res-line.ankunft GE fdate1   
          AND res-line.ankunft LE fdate2   
          AND res-line.resstatus NE 9 AND res-line.resstatus NE 10 
          AND res-line.resstatus NE 99 NO-LOCK,   
          FIRST gbuff WHERE gbuff.gastnr = res-line.gastnr NO-LOCK,  
          FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr   
          NO-LOCK,   
          FIRST reservation WHERE reservation.resnr = res-line.resnr  
            AND LENGTH(reservation.groupname) GE iGrpname NO-LOCK,   
          FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,   
          FIRST setup-list WHERE setup-list.nr = res-line.setup + 1   
          NO-LOCK BY (res-line.kontakt-nr * res-line.resnr) BY res-line.resstatus BY res-line.NAME:  
          RUN create-it.
      END.  
      ELSE IF SUBSTR(lname,1,1) NE "*" AND lname NE "" THEN   
      FOR EACH res-line WHERE   
          active-flag = 0 AND res-line.ankunft GE fdate1   
          AND res-line.ankunft LE fdate2   
          AND res-line.resstatus NE 9 AND res-line.resstatus NE 10  
          AND res-line.resstatus NE 99
          /*AND res-line.name GE lname AND res-line.name LE to-name NO-LOCK,*/
          AND res-line.name MATCHES("*" + lname + "*") NO-LOCK,             /*FDL Ticket 72FF79 | 0609D3*/
          FIRST gbuff WHERE gbuff.gastnr = res-line.gastnr NO-LOCK,  
          FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr   
          NO-LOCK,   
          FIRST reservation WHERE reservation.resnr = res-line.resnr   
            AND LENGTH(reservation.groupname) GE iGrpname NO-LOCK,   
          FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,   
          FIRST setup-list WHERE setup-list.nr = res-line.setup + 1   
          NO-LOCK BY res-line.name:  
          RUN create-it.  
      END.  
      ELSE   
      FOR EACH res-line WHERE   
          active-flag = 0   
          AND res-line.name MATCHES(lname) AND res-line.ankunft GE fdate1   
          AND res-line.ankunft LE fdate2   
          AND res-line.resstatus NE 9 AND res-line.resstatus NE 10  
          AND res-line.resstatus NE 99 NO-LOCK,   
          FIRST gbuff WHERE gbuff.gastnr = res-line.gastnr NO-LOCK,  
          FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr   
          NO-LOCK,   
          FIRST reservation WHERE reservation.resnr = res-line.resnr   
            AND LENGTH(reservation.groupname) GE iGrpname NO-LOCK,   
          FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,   
          FIRST setup-list WHERE setup-list.nr = res-line.setup + 1   
          NO-LOCK BY res-line.name:  
          RUN create-it.  
      END.  
    END.   
    ELSE IF last-sort = 2 THEN  /****** Sort BY Reserved name ********/   
    DO:   
      IF fdate1 = ? OR fdate2 = ? THEN   
      DO:   
        fdate1 = ci-date.   
        fdate2 = ci-date + 365.   
        /*MTDISP fdate1 fdate2 WITH FRAME f-reserve.*/  
      END.   
      IF lname EQ "" THEN   
      FOR EACH res-line WHERE   
          active-flag = 0 AND res-line.ankunft GE fdate1   
          AND res-line.ankunft LE fdate2   
          AND res-line.resstatus NE 9 AND res-line.resstatus NE 10
          AND res-line.resstatus NE 99 NO-LOCK,   
          FIRST gbuff WHERE gbuff.gastnr = res-line.gastnr NO-LOCK,  
          FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr   
          NO-LOCK,   
          FIRST reservation WHERE reservation.resnr = res-line.resnr  
            AND LENGTH(reservation.groupname) GE iGrpname NO-LOCK,   
          FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,   
          FIRST setup-list WHERE setup-list.nr = res-line.setup + 1   
          NO-LOCK BY reservation.name BY res-line.l-zuordnung[5] BY res-line.resnr  
          BY (res-line.kontakt-nr * res-line.resnr) BY res-line.resstatus BY res-line.NAME:  
          RUN create-it.  
      END.  
      ELSE IF SUBSTR(lname,1,1) EQ "*" AND lname NE "" THEN  
      FOR EACH res-line WHERE   
          active-flag = 0 AND res-line.ankunft GE fdate1   
          AND res-line.ankunft LE fdate2   
          AND res-line.resstatus NE 9 AND res-line.resstatus NE 10 
          AND res-line.resstatus NE 99
          /*AND res-line.resname MATCHES(lname)*/ NO-LOCK,
          FIRST gbuff WHERE gbuff.gastnr = res-line.gastnr NO-LOCK,  
          FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr   
          NO-LOCK,   
          FIRST reservation WHERE reservation.resnr = res-line.resnr 
          AND LENGTH(reservation.groupname) GE iGrpname
          AND reservation.NAME MATCHES(lname) NO-LOCK,                      /*FDL Ticket 72FF79 | 0609D3*/
          FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,   
          FIRST setup-list WHERE setup-list.nr = res-line.setup + 1   
          NO-LOCK BY reservation.name BY res-line.l-zuordnung[5] BY res-line.resnr   
          BY (res-line.kontakt-nr * res-line.resnr) BY res-line.resstatus BY res-line.NAME:  
          RUN create-it.  
      END.  
      ELSE /*IF SUBSTR(lname,1,1) NE "*" THEN*/ 
      FOR EACH res-line WHERE   
          active-flag = 0 AND res-line.ankunft GE fdate1   
          AND res-line.ankunft LE fdate2   
          AND res-line.resstatus NE 9 AND res-line.resstatus NE 10  
          AND res-line.resstatus NE 99
          /*AND res-line.resname GE lname AND res-line.resname LE to-name*/ NO-LOCK,   
          FIRST gbuff WHERE gbuff.gastnr = res-line.gastnr NO-LOCK,  
          FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr   
          NO-LOCK,   
          FIRST reservation WHERE reservation.resnr = res-line.resnr 
          AND LENGTH(reservation.groupname) GE iGrpname
          AND reservation.NAME MATCHES("*" + lname + "*") NO-LOCK,          /*FDL Ticket 72FF79 | 0609D3*/ 
          FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,   
          FIRST setup-list WHERE setup-list.nr = res-line.setup + 1   
          NO-LOCK BY reservation.name BY res-line.l-zuordnung[5] BY res-line.resnr   
          BY (res-line.kontakt-nr * res-line.resnr) BY res-line.resstatus BY res-line.NAME:  
          RUN create-it.  
      END.  
    END.   
    ELSE IF last-sort = 3 THEN  /************* SPEED OK **************/   
    DO:   
      IF lresnr = 0 THEN   
      FOR EACH res-line WHERE active-flag = 0   
          AND res-line.ankunft GE ci-date   
          AND res-line.ankunft LE (ci-date + 30)   
          AND res-line.resstatus NE 9 AND res-line.resstatus NE 10 
          AND res-line.resstatus NE 99
          NO-LOCK,   
          FIRST gbuff WHERE gbuff.gastnr = res-line.gastnr NO-LOCK,  
          FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr   
          NO-LOCK,   
          FIRST reservation WHERE reservation.resnr = res-line.resnr 
          AND LENGTH(reservation.groupname) GE iGrpname NO-LOCK,  
          FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,   
          FIRST setup-list WHERE setup-list.nr = res-line.setup + 1   
          NO-LOCK   
          BY res-line.l-zuordnung[5] BY res-line.resnr  
          /*  BY (res-line.kontakt-nr * res-line.resnr) BY res-line.resstatus */  
          BY res-line.NAME:  
          RUN create-it.  
      END.  
      ELSE   
      FOR EACH res-line WHERE active-flag = 0   
          AND (res-line.resnr EQ lresnr OR res-line.l-zuordnung[5] = lresnr)   
          AND res-line.resstatus NE 9 AND res-line.resstatus NE 10
          AND res-line.resstatus NE 99 NO-LOCK,   
          FIRST gbuff WHERE gbuff.gastnr = res-line.gastnr NO-LOCK,  
          FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr   
          NO-LOCK,   
          FIRST reservation WHERE reservation.resnr = res-line.resnr 
          AND LENGTH(reservation.groupname) GE iGrpname NO-LOCK,  
          FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,   
          FIRST setup-list WHERE setup-list.nr = res-line.setup + 1   
          NO-LOCK   
          /*  BY res-line.l-zuordnung[5] BY res-line.resnr  
          BY (res-line.kontakt-nr * res-line.resnr) BY res-line.resstatus */  
          BY res-line.NAME:  
          RUN create-it.  
      END.  
    END.   
    ELSE IF last-sort = 4 THEN   
    DO:   
      IF (fdate1 EQ ?) OR (fdate2 EQ ?) THEN   
      DO:   
        fdate1 = ci-date.   
        fdate2 = ci-date + 365.   
        /*MTDISP fdate1 fdate2 WITH FRAME f-reserve.*/  
      END.   
      FOR EACH res-line WHERE   
          active-flag = 0 AND res-line.ankunft GE fdate1   
          AND res-line.ankunft LE fdate2   
          AND res-line.resstatus NE 9 AND res-line.resstatus NE 10
          AND res-line.resstatus NE 99 NO-LOCK,   
          FIRST gbuff WHERE gbuff.gastnr = res-line.gastnr NO-LOCK,  
          FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr   
          NO-LOCK,   
          FIRST reservation WHERE reservation.resnr = res-line.resnr 
          AND LENGTH(reservation.groupname) GE iGrpname NO-LOCK,  
          FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,   
          FIRST setup-list WHERE setup-list.nr = res-line.setup + 1   
          NO-LOCK BY res-line.ankunft BY reservation.NAME BY res-line.l-zuordnung[5]  
          BY res-line.resnr  
          BY (res-line.kontakt-nr * res-line.resnr) BY res-line.resstatus BY res-line.NAME:  
          RUN create-it.  
      END.  
    END.   
    ELSE IF last-sort = 5 THEN RUN sqry5.   
  END.   
  
  /*MT  
  ASSIGN  
    tot-rm  = 0   
    tot-pax = 0  
    tot-com = 0  
    tot-ch1 = 0   
    tot-ch2 = 0  
    tot-ch3 = 0  
    tot-kcard = 0  
  .   
  GET FIRST q1 NO-LOCK.   
  DO WHILE AVAILABLE res-line:   
    IF res-line.resstatus NE 11 AND res-line.resstatus NE 13 THEN   
      tot-rm = tot-rm + res-line.zimmeranz.   
    ASSIGN  
      tot-pax = tot-pax + res-line.erwachs * res-line.zimmeranz  
      tot-com = tot-com + res-line.gratis * res-line.zimmeranz   
      tot-ch1 = tot-ch1 + res-line.kind1 * res-line.zimmeranz   
      tot-ch2 = tot-ch2 + res-line.kind2 * res-line.zimmeranz   
      tot-ch3 = tot-ch3 + res-line.l-zuordnung[4] * res-line.zimmeranz  
      tot-kcard = tot-kcard + res-line.betrieb-gast  
    .   
    GET NEXT q1 NO-LOCK.   
  END.   
  GET FIRST q1 NO-LOCK.   
  DISP tot-rm tot-pax tot-com tot-ch1 tot-ch2 tot-ch3 tot-kcard  
      WITH FRAME f-reserve.   
  */  
END.   
  
PROCEDURE sqry2:   
DEFINE VARIABLE to-name     AS CHAR    INITIAL ""   NO-UNDO.   
DEFINE VARIABLE iGrpname    AS INTEGER INITIAL 0    NO-UNDO.  
  
  ASSIGN  
    iGrpname = INTEGER(grpFlag)  
    rmlen    = LENGTH(room)  
  .   
  IF lname NE "" AND SUBSTR(lname,1,1) NE "*" THEN   
      to-name = get-toname(lname).   
    
    
  IF sorttype = 2 THEN   
  DO:   
    IF lname = "" THEN   
    FOR EACH res-line WHERE   
        active-flag = 1 AND res-line.resstatus NE 12
        AND res-line.resstatus NE 99
        AND (SUBSTR(res-line.zinr,1,INTEGER(rmlen))) GE (room)   
        AND res-line.ankunft LE ci-date AND res-line.abreise GE ci-date   
        AND res-line.resname GE lname NO-LOCK,   
        FIRST gbuff WHERE gbuff.gastnr = res-line.gastnr NO-LOCK,  
        FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr   
        NO-LOCK,   
        FIRST reservation WHERE reservation.resnr = res-line.resnr   
          AND reservation.name GE lname  
          AND LENGTH(reservation.groupname) GE iGrpname NO-LOCK,   
        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr,   
        FIRST setup-list WHERE setup-list.nr = res-line.setup + 1   
        NO-LOCK BY reservation.name BY reservation.groupname   
        BY res-line.zinr  
        BY (res-line.kontakt-nr * res-line.resnr) BY res-line.resstatus BY res-line.NAME:  
        RUN create-it.  
    END.  
    ELSE IF lname NE "" AND SUBSTR(lname,1,1) NE "*" THEN   
    FOR EACH res-line WHERE   
        active-flag = 1 AND res-line.resstatus NE 12 
        AND res-line.resstatus NE 99
        AND (SUBSTR(res-line.zinr,1,INTEGER(rmlen))) GE (room)   
        AND res-line.ankunft LE ci-date AND res-line.abreise GE ci-date   
        /*AND res-line.resname GE lname AND res-line.resname LE to-name*/ NO-LOCK,   
        FIRST gbuff WHERE gbuff.gastnr = res-line.gastnr NO-LOCK,  
        FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr   
        NO-LOCK,   
        FIRST reservation WHERE reservation.resnr = res-line.resnr   
        /*AND reservation.name GE lname*/
        AND reservation.NAME MATCHES("*" + lname + "*")                     /*FDL Ticket 72FF79 | 0609D3*/
        AND LENGTH(reservation.groupname) GE iGrpname NO-LOCK,   
        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr,   
        FIRST setup-list WHERE setup-list.nr = res-line.setup + 1   
        NO-LOCK BY reservation.name BY reservation.groupname   
        BY res-line.zinr  
        BY (res-line.kontakt-nr * res-line.resnr) BY res-line.resstatus BY res-line.NAME:  
        RUN create-it.  
    END.  
    ELSE IF lname NE "" AND SUBSTR(lname,1,1) EQ "*" THEN   
    FOR EACH res-line WHERE   
        active-flag = 1 AND res-line.resstatus NE 12
        AND res-line.resstatus NE 99
        AND (SUBSTR(res-line.zinr,1,INTEGER(rmlen))) GE (room)   
        AND res-line.ankunft LE ci-date AND res-line.abreise GE ci-date   
        /*AND res-line.resname MATCHES (lname)*/ NO-LOCK,
        FIRST gbuff WHERE gbuff.gastnr = res-line.gastnr NO-LOCK,  
        FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr   
        NO-LOCK,   
        FIRST reservation WHERE reservation.resnr = res-line.resnr
          AND reservation.NAME MATCHES(lname)                                   /*FDL Ticket 72FF79 | 0609D3*/
          AND LENGTH(reservation.groupname) GE iGrpname NO-LOCK,   
        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr,   
        FIRST setup-list WHERE setup-list.nr = res-line.setup + 1   
        NO-LOCK BY reservation.name BY reservation.groupname   
        BY res-line.zinr  
        BY (res-line.kontakt-nr * res-line.resnr) BY res-line.resstatus BY res-line.NAME:  
        RUN create-it.  
    END.  
  END.   
  ELSE IF sorttype = 3 THEN   
  DO:   
    IF lname = "" THEN   
    DO:   
      IF room = "" THEN   
      FOR EACH res-line WHERE   
          active-flag = 0 AND res-line.ankunft EQ ci-date   
          AND res-line.resstatus NE 9 AND res-line.resstatus NE 10 
          AND res-line.resstatus NE 99 NO-LOCK,   
          FIRST gbuff WHERE gbuff.gastnr = res-line.gastnr NO-LOCK,  
          FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr   
          NO-LOCK,   
          FIRST reservation WHERE reservation.resnr = res-line.resnr   
            AND LENGTH(reservation.groupname) GE iGrpname NO-LOCK,   
          FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr,   
          FIRST setup-list WHERE setup-list.nr = res-line.setup + 1   
          NO-LOCK BY reservation.name BY reservation.resnr   
          BY res-line.zinr  
          BY (res-line.kontakt-nr * res-line.resnr) BY res-line.resstatus BY res-line.NAME:  
          RUN create-it.  
      END.  
      ELSE IF room NE "" THEN   
      FOR EACH res-line WHERE   
          active-flag = 0 AND res-line.ankunft EQ ci-date   
          AND res-line.resstatus NE 9 AND res-line.resstatus NE 10 
          AND res-line.resstatus NE 99
          AND (SUBSTR(res-line.zinr,1,INTEGER(rmlen))) GE (room)   
          NO-LOCK,   
          FIRST gbuff WHERE gbuff.gastnr = res-line.gastnr NO-LOCK,  
          FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr   
          NO-LOCK,   
          FIRST reservation WHERE reservation.resnr = res-line.resnr  
            AND LENGTH(reservation.groupname) GE iGrpname NO-LOCK,   
          FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr,   
          FIRST setup-list WHERE setup-list.nr = res-line.setup + 1   
          NO-LOCK BY res-line.zinr BY reservation.name   
           BY res-line.l-zuordnung[5] BY res-line.resnr   
          BY (res-line.kontakt-nr * res-line.resnr) BY res-line.resstatus BY res-line.NAME:  
          RUN create-it.  
      END.  
    END.   
    ELSE IF SUBSTR(lname,1,1) = "*" THEN   
    FOR EACH res-line WHERE   
        active-flag = 0 AND res-line.ankunft EQ ci-date   
        AND res-line.resstatus NE 9 AND res-line.resstatus NE 10 
        AND res-line.resstatus NE 99
        /*AND res-line.resname MATCHES(lname)*/   
        AND (SUBSTR(res-line.zinr,1,INTEGER(rmlen))) GE (room)   
        NO-LOCK,   
        FIRST gbuff WHERE gbuff.gastnr = res-line.gastnr NO-LOCK,  
        FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr   
        NO-LOCK,   
        FIRST reservation WHERE reservation.resnr = res-line.resnr  
          AND reservation.NAME MATCHES(lname)                                       /*FDL Ticket 72FF79 | 0609D3*/
          AND LENGTH(reservation.groupname) GE iGrpname NO-LOCK,   
        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr,   
        FIRST setup-list WHERE setup-list.nr = res-line.setup + 1   
        NO-LOCK BY reservation.name BY res-line.l-zuordnung[5] BY res-line.resnr   
        BY res-line.zinr  
        BY (res-line.kontakt-nr * res-line.resnr) BY res-line.resstatus BY res-line.NAME:  
        RUN create-it.  
    END.  
    ELSE IF SUBSTR(lname,1,1) NE "*" THEN   
    FOR EACH res-line WHERE   
        active-flag = 0 AND res-line.ankunft EQ ci-date   
        AND res-line.resstatus NE 9 AND res-line.resstatus NE 10
        AND res-line.resstatus NE 99
        /*AND res-line.resname GE lname AND res-line.resname LE to-name */
        AND (SUBSTR(res-line.zinr,1,INTEGER(rmlen))) GE (room)   
        NO-LOCK,   
        FIRST gbuff WHERE gbuff.gastnr = res-line.gastnr NO-LOCK,  
        FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr   
        NO-LOCK,   
        FIRST reservation WHERE reservation.resnr = res-line.resnr
          AND reservation.NAME MATCHES("*" + lname + "*")                           /*FDL Ticket 72FF79 | 0609D3*/ 
          AND LENGTH(reservation.groupname) GE iGrpname NO-LOCK,   
        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr,   
        FIRST setup-list WHERE setup-list.nr = res-line.setup + 1   
        NO-LOCK BY reservation.name BY res-line.l-zuordnung[5] BY res-line.resnr   
        BY res-line.zinr  
        BY (res-line.kontakt-nr * res-line.resnr) BY res-line.resstatus BY res-line.NAME:  
        RUN create-it.  
    END.  
  END.   
  ELSE IF sorttype = 4 THEN   
  DO:   
    IF lname = "" THEN   
    DO:   
      IF room = "" THEN   
      FOR EACH res-line WHERE   
          active-flag = 1 AND res-line.resstatus NE 12
          AND res-line.resstatus NE 99
          AND res-line.abreise EQ fdate   
          AND (SUBSTR(res-line.zinr,1,INTEGER(rmlen))) GE (room)   
          NO-LOCK,   
          FIRST gbuff WHERE gbuff.gastnr = res-line.gastnr NO-LOCK,  
          FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr   
          NO-LOCK,   
          FIRST reservation WHERE reservation.resnr = res-line.resnr   
            AND LENGTH(reservation.groupname) GE iGrpname NO-LOCK,   
          FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr,   
          FIRST setup-list WHERE setup-list.nr = res-line.setup + 1   
          NO-LOCK BY reservation.name BY reservation.groupname   
          BY res-line.zinr  
          BY (res-line.kontakt-nr * res-line.resnr) BY res-line.resstatus BY res-line.NAME:  
          RUN create-it.  
      END.  
      ELSE IF room NE "" THEN   
      FOR EACH res-line WHERE   
          active-flag = 1 AND res-line.resstatus NE 12
          AND res-line.resstatus NE 99
          AND res-line.abreise EQ fdate   
          AND (SUBSTR(res-line.zinr,1,INTEGER(rmlen))) GE (room)   
          NO-LOCK,   
          FIRST gbuff WHERE gbuff.gastnr = res-line.gastnr NO-LOCK,  
          FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr   
          NO-LOCK,   
          FIRST reservation WHERE reservation.resnr = res-line.resnr  
            AND LENGTH(reservation.groupname) GE iGrpname NO-LOCK,   
          FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr,   
          FIRST setup-list WHERE setup-list.nr = res-line.setup + 1   
          NO-LOCK BY res-line.zinr BY reservation.name   
          BY reservation.groupname  
          BY (res-line.kontakt-nr * res-line.resnr) BY res-line.resstatus BY res-line.NAME:  
          RUN create-it.  
      END.  
    END.   
    ELSE IF SUBSTR(lname,1,1) = "*" THEN   
    FOR EACH res-line WHERE   
        active-flag = 1 AND res-line.resstatus NE 12
        AND res-line.resstatus NE 99
        AND res-line.abreise EQ fdate   
        /*AND res-line.resname MATCHES (lname)*/
        AND (SUBSTR(res-line.zinr,1,INTEGER(rmlen))) GE (room)   
        NO-LOCK,   
        FIRST gbuff WHERE gbuff.gastnr = res-line.gastnr NO-LOCK,  
        FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr   
        NO-LOCK,   
        FIRST reservation WHERE reservation.resnr = res-line.resnr 
          AND reservation.NAME MATCHES(lname)                                       /*FDL Ticket 72FF79 | 0609D3*/
          AND LENGTH(reservation.groupname) GE iGrpname NO-LOCK,   
        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr,   
        FIRST setup-list WHERE setup-list.nr = res-line.setup + 1   
        NO-LOCK BY reservation.name BY reservation.groupname   
        BY res-line.zinr  
        BY (res-line.kontakt-nr * res-line.resnr) BY res-line.resstatus BY res-line.NAME:  
        RUN create-it.  
    END.  
    ELSE IF SUBSTR(lname,1,1) NE "*" THEN   
    FOR EACH res-line WHERE   
        active-flag = 1 AND res-line.resstatus NE 12
        AND res-line.resstatus NE 99
        AND res-line.abreise EQ fdate   
        /*AND res-line.resname GE lname AND res-line.resname LE to-name*/
        AND (SUBSTR(res-line.zinr,1,INTEGER(rmlen))) GE (room)   
        NO-LOCK,   
        FIRST gbuff WHERE gbuff.gastnr = res-line.gastnr NO-LOCK,  
        FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr   
        NO-LOCK,   
        FIRST reservation WHERE reservation.resnr = res-line.resnr
          AND reservation.NAME MATCHES("*" + lname + "*")                           /*FDL Ticket 72FF79 | 0609D3*/ 
          AND LENGTH(reservation.groupname) GE iGrpname NO-LOCK,   
        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr,   
        FIRST setup-list WHERE setup-list.nr = res-line.setup + 1   
        NO-LOCK BY reservation.name BY reservation.groupname   
        BY res-line.zinr  
        BY (res-line.kontakt-nr * res-line.resnr) BY res-line.resstatus BY res-line.NAME:  
        RUN create-it.  
    END.  
  END.   
    
END.   
   
PROCEDURE sqry3:   
DEFINE VARIABLE iGrpname    AS INTEGER INITIAL 0    NO-UNDO.  
  
  ASSIGN iGrpname = INTEGER(grpFlag).  
    
  IF sorttype = 2 THEN   
  DO:   
    IF lresnr = 0 THEN   
    FOR EACH res-line WHERE active-flag = 1   
        AND res-line.resstatus NE 12
        AND res-line.resstatus NE 99
        AND res-line.ankunft LE ci-date AND res-line.abreise GE ci-date,   
        FIRST gbuff WHERE gbuff.gastnr = res-line.gastnr NO-LOCK,  
        FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr   
        NO-LOCK,   
        FIRST reservation WHERE reservation.resnr = res-line.resnr  
          AND LENGTH(reservation.groupname) GE iGrpname NO-LOCK,   
        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr,   
        FIRST setup-list WHERE setup-list.nr = res-line.setup + 1   
        NO-LOCK BY res-line.l-zuordnung[5] BY res-line.resnr BY res-line.zinr  
        BY (res-line.kontakt-nr * res-line.resnr) BY res-line.resstatus BY res-line.NAME:  
        RUN create-it.  
    END.  
    ELSE   
    FOR EACH res-line WHERE active-flag = 1   
        AND res-line.resstatus NE 12
        AND res-line.resstatus NE 99
        AND (res-line.resnr EQ lresnr OR res-line.l-zuordnung[5] = lresnr) NO-LOCK,   
        FIRST gbuff WHERE gbuff.gastnr = res-line.gastnr NO-LOCK,  
        FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr   
        NO-LOCK,   
        FIRST reservation WHERE reservation.resnr = res-line.resnr   
          AND LENGTH(reservation.groupname) GE iGrpname NO-LOCK,   
        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr,   
        FIRST setup-list WHERE setup-list.nr = res-line.setup + 1   
        NO-LOCK BY res-line.l-zuordnung[5] BY res-line.resnr BY res-line.zinr  
        BY (res-line.kontakt-nr * res-line.resnr) BY res-line.resstatus BY res-line.NAME:  
        RUN create-it.  
    END.  
  END.   
  ELSE IF sorttype = 3 THEN   
  DO:   
    IF lresnr = 0 THEN   
    FOR EACH res-line WHERE   
        active-flag = 0 AND res-line.ankunft = ci-date   
        AND res-line.resstatus NE 9 AND res-line.resstatus NE 10 
        AND res-line.resstatus NE 99 NO-LOCK,   
        FIRST gbuff WHERE gbuff.gastnr = res-line.gastnr NO-LOCK,  
        FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr   
        NO-LOCK,   
        FIRST reservation WHERE reservation.resnr = res-line.resnr  
          AND LENGTH(reservation.groupname) GE iGrpname NO-LOCK,   
        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr,   
        FIRST setup-list WHERE setup-list.nr = res-line.setup + 1   
        NO-LOCK BY res-line.l-zuordnung[5] BY res-line.resnr  
        BY (res-line.kontakt-nr * res-line.resnr) BY res-line.resstatus BY res-line.NAME:  
        RUN create-it.  
    END.  
    ELSE   
    FOR EACH res-line WHERE   
        active-flag = 0 AND res-line.ankunft = ci-date   
        AND res-line.resstatus NE 9 AND res-line.resstatus NE 10
        AND res-line.resstatus NE 99
        AND (res-line.resnr = lresnr OR res-line.l-zuordnung[5] = lresnr) NO-LOCK,   
        FIRST gbuff WHERE gbuff.gastnr = res-line.gastnr NO-LOCK,  
        FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr   
        NO-LOCK,   
        FIRST reservation WHERE reservation.resnr = res-line.resnr  
          AND LENGTH(reservation.groupname) GE iGrpname NO-LOCK,   
        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr,   
        FIRST setup-list WHERE setup-list.nr = res-line.setup + 1   
        NO-LOCK BY res-line.l-zuordnung[5] BY res-line.resnr  
        BY (res-line.kontakt-nr * res-line.resnr) BY res-line.resstatus BY res-line.NAME:  
        RUN create-it.  
    END.  
  END.   
  ELSE IF sorttype = 4 THEN   
  DO:   
    IF lresnr = 0 THEN   
    FOR EACH res-line WHERE   
        active-flag = 1 AND res-line.resstatus NE 12
        AND res-line.resstatus NE 99
        AND res-line.abreise = fdate,   
        FIRST gbuff WHERE gbuff.gastnr = res-line.gastnr NO-LOCK,  
        FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr   
        NO-LOCK,   
        FIRST reservation WHERE reservation.resnr = res-line.resnr   
          AND LENGTH(reservation.groupname) GE iGrpname NO-LOCK,   
        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr,   
        FIRST setup-list WHERE setup-list.nr = res-line.setup + 1   
        NO-LOCK BY res-line.l-zuordnung[5] BY res-line.resnr  
        BY (res-line.kontakt-nr * res-line.resnr) BY res-line.resstatus BY res-line.NAME:  
        RUN create-it.  
    END.  
    ELSE   
    FOR EACH res-line WHERE   
        active-flag = 1 AND res-line.resstatus NE 12
        AND res-line.resstatus NE 99
        AND res-line.abreise = fdate   
        AND (res-line.resnr = lresnr OR res-line.l-zuordnung[5] = lresnr) NO-LOCK,   
        FIRST gbuff WHERE gbuff.gastnr = res-line.gastnr NO-LOCK,  
        FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr   
        NO-LOCK,   
        FIRST reservation WHERE reservation.resnr = res-line.resnr  
          AND LENGTH(reservation.groupname) GE iGrpname NO-LOCK,   
        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr,   
        FIRST setup-list WHERE setup-list.nr = res-line.setup + 1   
        NO-LOCK BY res-line.l-zuordnung[5] BY res-line.resnr  
        BY (res-line.kontakt-nr * res-line.resnr) BY res-line.resstatus BY res-line.NAME:  
        RUN create-it.  
    END.  
  END.   
    
END.   
   
PROCEDURE sqry4:   
DEFINE VARIABLE to-name     AS CHAR    INITIAL ""   NO-UNDO.   
DEFINE VARIABLE iGrpname    AS INTEGER INITIAL 0    NO-UNDO.  
  
  ASSIGN  
    iGrpname = INTEGER(grpFlag)  
    rmlen    = LENGTH(room)  
  .   
  IF lname NE "" AND SUBSTR(lname,1,1) NE "*" THEN   
      to-name = get-toname(lname).   
  
    
  IF sorttype = 2 THEN   
  DO:   
    IF fdate NE ? THEN   
    FOR EACH res-line WHERE active-flag = 1   
        AND res-line.resstatus NE 12
        AND res-line.resstatus NE 99 AND res-line.ankunft GE fdate   
        AND res-line.abreise GE ci-date,   
        FIRST gbuff WHERE gbuff.gastnr = res-line.gastnr NO-LOCK,  
        FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr   
        NO-LOCK,   
        FIRST reservation WHERE reservation.resnr = res-line.resnr  
          AND LENGTH(reservation.groupname) GE iGrpname NO-LOCK,   
        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr,   
        FIRST setup-list WHERE setup-list.nr = res-line.setup + 1   
        NO-LOCK BY res-line.ankunft BY reservation.NAME  
        BY (res-line.kontakt-nr * res-line.resnr) BY res-line.resstatus BY res-line.NAME:  
        RUN create-it.  
    END.  
    ELSE   
    FOR EACH res-line WHERE active-flag = 1   
        AND res-line.resstatus NE 12 
        AND res-line.resstatus NE 99 AND res-line.ankunft LE ci-date   
        AND res-line.abreise GE ci-date,   
        FIRST gbuff WHERE gbuff.gastnr = res-line.gastnr NO-LOCK,  
        FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr   
        NO-LOCK,   
        FIRST reservation WHERE reservation.resnr = res-line.resnr  
          AND LENGTH(reservation.groupname) GE iGrpname NO-LOCK,   
        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr,   
        FIRST setup-list WHERE setup-list.nr = res-line.setup + 1   
        NO-LOCK BY res-line.ankunft BY reservation.NAME  
        BY (res-line.kontakt-nr * res-line.resnr) BY res-line.resstatus BY res-line.NAME:  
        RUN create-it.  
    END.  
  END.   
  ELSE IF sorttype = 3 THEN   
  DO:   
    IF lname = "" THEN   
    DO:   
      IF room = "" THEN   
      FOR EACH res-line WHERE   
          active-flag = 0 AND res-line.ankunft = ci-date   
          AND res-line.resstatus NE 9 
          AND res-line.resstatus NE 99 AND res-line.resstatus NE 10   
          AND (SUBSTR(res-line.zinr,1,INTEGER(rmlen))) GE (room)   
          NO-LOCK,   
          FIRST gbuff WHERE gbuff.gastnr = res-line.gastnr NO-LOCK,  
          FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr   
          NO-LOCK,   
          FIRST reservation WHERE reservation.resnr = res-line.resnr  
            AND LENGTH(reservation.groupname) GE iGrpname NO-LOCK,   
          FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr,   
          FIRST setup-list WHERE setup-list.nr = res-line.setup + 1   
          NO-LOCK BY res-line.zinr  
          BY (res-line.kontakt-nr * res-line.resnr) BY res-line.resstatus BY res-line.NAME:  
          RUN create-it.  
      END.  
      ELSE IF room NE "" THEN   
      FOR EACH res-line WHERE   
          active-flag = 0 AND res-line.ankunft = ci-date   
          AND res-line.resstatus NE 9 AND res-line.resstatus NE 10  
          AND res-line.resstatus NE 99
          AND (SUBSTR(res-line.zinr,1,INTEGER(rmlen))) GE (room)   
          NO-LOCK,   
          FIRST gbuff WHERE gbuff.gastnr = res-line.gastnr NO-LOCK,  
          FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr   
          NO-LOCK,   
          FIRST reservation WHERE reservation.resnr = res-line.resnr  
            AND LENGTH(reservation.groupname) GE iGrpname NO-LOCK,   
          FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr,   
          FIRST setup-list WHERE setup-list.nr = res-line.setup + 1   
          NO-LOCK BY res-line.zinr  
          BY (res-line.kontakt-nr * res-line.resnr) BY res-line.resstatus BY res-line.NAME:  
          RUN create-it.  
      END.  
    END.   
    ELSE IF lname NE "" AND SUBSTR(lname,1,1) NE "*" THEN   
    FOR EACH res-line WHERE   
        active-flag = 0 AND res-line.ankunft = ci-date   
        AND res-line.resstatus NE 9 AND res-line.resstatus NE 10
        AND res-line.resstatus NE 99
        AND (SUBSTR(res-line.zinr,1,INTEGER(rmlen))) GE (room)   
        AND res-line.name GE lname   
        AND res-line.name LE to-name NO-LOCK,   
        FIRST gbuff WHERE gbuff.gastnr = res-line.gastnr NO-LOCK,  
        FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr   
        NO-LOCK,   
        FIRST reservation WHERE reservation.resnr = res-line.resnr  
          AND LENGTH(reservation.groupname) GE iGrpname NO-LOCK,   
        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr,   
        FIRST setup-list WHERE setup-list.nr = res-line.setup + 1   
        NO-LOCK BY res-line.name BY res-line.zinr:  
        RUN create-it.  
    END.  
    ELSE IF lname NE "" AND SUBSTR(lname,1,1) EQ "*" THEN   
    FOR EACH res-line WHERE   
        active-flag = 0 AND res-line.ankunft = ci-date   
        AND res-line.resstatus NE 9 AND res-line.resstatus NE 10 
        AND res-line.resstatus NE 99
        AND (SUBSTR(res-line.zinr,1,INTEGER(rmlen))) GE (room)   
        AND res-line.name MATCHES(lname) NO-LOCK,   
        FIRST gbuff WHERE gbuff.gastnr = res-line.gastnr NO-LOCK,  
        FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr   
        NO-LOCK,   
        FIRST reservation WHERE reservation.resnr = res-line.resnr  
          AND LENGTH(reservation.groupname) GE iGrpname NO-LOCK,   
        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr,   
        FIRST setup-list WHERE setup-list.nr = res-line.setup + 1   
        NO-LOCK BY res-line.name BY res-line.zinr:  
        RUN create-it.  
    END.  
  END.   
  ELSE IF sorttype = 4 THEN   
  DO:   
    IF lname = "" THEN   
    DO:   
      IF room = "" THEN   
      FOR EACH res-line WHERE   
          active-flag = 1 AND res-line.resstatus NE 12
          AND res-line.resstatus NE 99
          AND res-line.abreise = fdate   
          AND (SUBSTR(res-line.zinr,1,INTEGER(rmlen))) GE (room)   
          NO-LOCK,   
          FIRST gbuff WHERE gbuff.gastnr = res-line.gastnr NO-LOCK,  
          FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr   
          NO-LOCK,   
          FIRST reservation WHERE reservation.resnr = res-line.resnr  
            AND LENGTH(reservation.groupname) GE iGrpname NO-LOCK,   
          FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr,   
          FIRST setup-list WHERE setup-list.nr = res-line.setup + 1   
          NO-LOCK BY res-line.zinr  
          BY (res-line.kontakt-nr * res-line.resnr) BY res-line.resstatus BY res-line.NAME:  
          RUN create-it.  
      END.  
      ELSE IF room NE "" THEN   
      FOR EACH res-line WHERE   
          active-flag = 1 AND res-line.resstatus NE 12 
          AND res-line.resstatus NE 99
          AND res-line.abreise = fdate   
          AND (SUBSTR(res-line.zinr,1,INTEGER(rmlen))) GE (room)   
          NO-LOCK,   
          FIRST gbuff WHERE gbuff.gastnr = res-line.gastnr NO-LOCK,  
          FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr   
          NO-LOCK,   
          FIRST reservation WHERE reservation.resnr = res-line.resnr  
            AND LENGTH(reservation.groupname) GE iGrpname NO-LOCK,   
          FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr,   
          FIRST setup-list WHERE setup-list.nr = res-line.setup + 1   
          NO-LOCK BY res-line.zinr  
          BY (res-line.kontakt-nr * res-line.resnr) BY res-line.resstatus BY res-line.NAME:  
          RUN create-it.  
      END.  
    END.   
    ELSE IF lname NE "" AND SUBSTR(lname,1,1) NE "*" THEN   
    FOR EACH res-line WHERE   
        active-flag = 1 AND res-line.resstatus NE 12
        AND res-line.resstatus NE 99
        AND res-line.abreise = fdate   
        AND (SUBSTR(res-line.zinr,1,INTEGER(rmlen))) GE (room)   
        AND res-line.name GE lname AND res-line.name LE to-name NO-LOCK,   
        FIRST gbuff WHERE gbuff.gastnr = res-line.gastnr NO-LOCK,  
        FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr   
        NO-LOCK,   
        FIRST reservation WHERE reservation.resnr = res-line.resnr  
          AND LENGTH(reservation.groupname) GE iGrpname NO-LOCK,   
        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr,   
        FIRST setup-list WHERE setup-list.nr = res-line.setup + 1   
        NO-LOCK BY res-line.name BY res-line.zinr:  
        RUN create-it.  
    END.  
    ELSE IF lname NE "" AND SUBSTR(lname,1,1) EQ "*" THEN   
    FOR EACH res-line WHERE   
        active-flag = 1 AND res-line.resstatus NE 12
        AND res-line.resstatus NE 99
        AND res-line.abreise = fdate   
        AND (SUBSTR(res-line.zinr,1,INTEGER(rmlen))) GE (room)   
        AND res-line.name MATCHES(lname) NO-LOCK,   
        FIRST gbuff WHERE gbuff.gastnr = res-line.gastnr NO-LOCK,  
        FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr   
        NO-LOCK,   
        FIRST reservation WHERE reservation.resnr = res-line.resnr  
          AND LENGTH(reservation.groupname) GE iGrpname NO-LOCK,   
        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr,   
        FIRST setup-list WHERE setup-list.nr = res-line.setup + 1   
        NO-LOCK BY res-line.name BY res-line.zinr:  
        RUN create-it.  
    END.  
  END.   
    
END.   
   
PROCEDURE sqry5:   
  DEFINE VARIABLE iGrpname AS INTEGER INITIAL 0    NO-UNDO.  
  
  ASSIGN iGrpname = INTEGER(grpFlag).  
    
  IF sorttype = 1 THEN   
  DO:   
      IF (fdate1 EQ ?) OR (fdate2 EQ ?) THEN   
      DO:   
        fdate1 = ci-date.   
        fdate2 = ci-date + 365.   
        /*MTDISP fdate1 fdate2 WITH FRAME f-reserve.*/  
      END.   
      FOR EACH res-line WHERE   
          active-flag = 0 
          AND res-line.zinr = room
          /*AND res-line.ankunft GE fdate1   
          AND res-line.ankunft LE fdate2*/
          AND res-line.resstatus NE 9 AND res-line.resstatus NE 10
          AND res-line.resstatus NE 99
          NO-LOCK,   
          FIRST gbuff WHERE gbuff.gastnr = res-line.gastnr NO-LOCK,  
          FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr   
          NO-LOCK,   
          FIRST reservation WHERE reservation.resnr = res-line.resnr  
            AND LENGTH(reservation.groupname) GE iGrpname NO-LOCK,   
          FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,   
          FIRST setup-list WHERE setup-list.nr = res-line.setup + 1   
          NO-LOCK /*BY res-line.ankunft*/ BY res-line.zinr  
          BY (res-line.kontakt-nr * res-line.resnr) BY res-line.resstatus BY res-line.NAME:  
          RUN create-it.  
      END.  
  END.   
  ELSE IF sorttype = 2 THEN   
  DO:   
    IF fdate NE ? THEN   
    FOR EACH res-line WHERE active-flag = 1   
        AND res-line.resstatus NE 12
        AND res-line.resstatus NE 99 AND res-line.ankunft GE fdate   
        AND res-line.abreise GE ci-date  
        AND res-line.zinr GE room NO-LOCK,   
        FIRST gbuff WHERE gbuff.gastnr = res-line.gastnr NO-LOCK,  
        FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr   
        NO-LOCK,   
        FIRST reservation WHERE reservation.resnr = res-line.resnr  
          AND LENGTH(reservation.groupname) GE iGrpname NO-LOCK,   
        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr,   
        FIRST setup-list WHERE setup-list.nr = res-line.setup + 1   
        NO-LOCK BY res-line.zinr  
        BY (res-line.kontakt-nr * res-line.resnr) BY res-line.resstatus BY res-line.NAME:  
        RUN create-it.  
    END.  
    ELSE   
    FOR EACH res-line WHERE active-flag = 1   
        AND res-line.resstatus NE 12
        AND res-line.resstatus NE 99 AND res-line.ankunft LE ci-date   
        AND res-line.abreise GE ci-date  
        AND res-line.zinr GE room NO-LOCK,   
        FIRST gbuff WHERE gbuff.gastnr = res-line.gastnr NO-LOCK,  
        FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr   
        NO-LOCK,   
        FIRST reservation WHERE reservation.resnr = res-line.resnr  
          AND LENGTH(reservation.groupname) GE iGrpname NO-LOCK,   
        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr,   
        FIRST setup-list WHERE setup-list.nr = res-line.setup + 1   
        NO-LOCK BY res-line.zinr  
        BY (res-line.kontakt-nr * res-line.resnr) BY res-line.resstatus BY res-line.NAME:  
        RUN create-it.  
    END.  
  END.   
  ELSE IF sorttype = 3 THEN   
  FOR EACH res-line WHERE   
      active-flag = 0 AND res-line.ankunft EQ ci-date   
      AND res-line.resstatus NE 9 AND res-line.resstatus NE 10
      AND res-line.resstatus NE 99
      AND res-line.resname GE lname AND res-line.zinr GE room NO-LOCK,   
      FIRST gbuff WHERE gbuff.gastnr = res-line.gastnr NO-LOCK,  
      FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr NO-LOCK,   
      FIRST reservation WHERE reservation.resnr = res-line.resnr  
        AND LENGTH(reservation.groupname) GE iGrpname NO-LOCK,   
      FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr,   
      FIRST setup-list WHERE setup-list.nr = res-line.setup + 1   
      NO-LOCK BY res-line.zinr  
      BY (res-line.kontakt-nr * res-line.resnr) BY res-line.resstatus BY res-line.NAME:  
      RUN create-it.  
  END.  
  ELSE IF sorttype = 4 THEN   
  FOR EACH res-line WHERE   
      active-flag = 1 AND res-line.resstatus NE 12
      AND res-line.resstatus NE 99
      AND res-line.abreise EQ fdate AND res-line.resname GE lname   
      AND res-line.zinr GE room NO-LOCK,   
      FIRST gbuff WHERE gbuff.gastnr = res-line.gastnr NO-LOCK,  
      FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr   
      NO-LOCK,   
      FIRST reservation WHERE reservation.resnr = res-line.resnr  
        AND LENGTH(reservation.groupname) GE iGrpname NO-LOCK,   
      FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr,   
      FIRST setup-list WHERE setup-list.nr = res-line.setup + 1   
      NO-LOCK BY res-line.zinr  
      BY (res-line.kontakt-nr * res-line.resnr) BY res-line.resstatus BY res-line.NAME:  
      RUN create-it.  
  END.  
END.   
  
  
PROCEDURE create-it:  
    DEFINE VARIABLE loopi   AS INTEGER NO-UNDO.
    DEFINE VARIABLE loopj   AS INTEGER NO-UNDO.
    DEFINE VARIABLE loopk   AS INTEGER NO-UNDO.
    DEFINE VARIABLE loopl   AS INTEGER NO-UNDO.

    DEFINE VARIABLE str1    AS CHAR    NO-UNDO.
    DEFINE VARIABLE str2    AS CHAR    NO-UNDO.
    DEFINE VARIABLE web-com AS CHAR    NO-UNDO.
    DEFINE VARIABLE bday    AS DATE    NO-UNDO.

    DEF BUFFER bresline FOR res-line.
    
    FIND FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember NO-LOCK.
    CREATE arl-list.  
    ASSIGN  
    arl-list.resnr             = res-line.resnr  
    arl-list.reslinnr          = res-line.reslinnr  
    arl-list.voucher-nr        = res-line.voucher-nr  
    arl-list.grpflag           = reservation.grpflag  
    /*arl-list.verstat           = reservation.verstat*/
    arl-list.l-zuordnung2      = res-line.l-zuordnung[2]  
    arl-list.kontignr          = res-line.kontignr  
    arl-list.firmen-nr         = gbuff.firmen-nr  
    arl-list.steuernr          = gbuff.steuernr  
    arl-list.rsv-name          = reservation.name  
    arl-list.zinr              = res-line.zinr  
    arl-list.setup-list-char   = setup-list.CHAR  
    arl-list.resline-name      = res-line.name  
    arl-list.waehrung-wabkurz  = waehrung.wabkurz  
    arl-list.segmentcode       = reservation.segmentcode  
    arl-list.ankunft           = res-line.ankunft  
    arl-list.abreise           = res-line.abreise  
    arl-list.zimmeranz         = res-line.zimmeranz  
    arl-list.kurzbez           = zimkateg.kurzbez  
    arl-list.arrangement       = res-line.arrangement  
    arl-list.zipreis           = res-line.zipreis  
    arl-list.anztage           = res-line.anztage  
    arl-list.erwachs           = res-line.erwachs  
    arl-list.kind1             = res-line.kind1  
    arl-list.kind2             = res-line.kind2  
    arl-list.gratis            = res-line.gratis  
    arl-list.l-zuordnung4      = res-line.l-zuordnung[4]  
    arl-list.resstatus         = res-line.resstatus  
    arl-list.l-zuordnung3      = res-line.l-zuordnung[3]  
    arl-list.flight-nr         = res-line.flight-nr  
    arl-list.ankzeit           = res-line.ankzeit  
    arl-list.abreisezeit       = res-line.abreisezeit  
    arl-list.betrieb-gast      = res-line.betrieb-gast  
    arl-list.resdat            = reservation.resdat  
    arl-list.useridanlage      = reservation.useridanlage  
    arl-list.reserve-dec       = res-line.reserve-dec  
    arl-list.cancelled-id      = res-line.cancelled-id  
    arl-list.changed-id        = res-line.changed-id  
    arl-list.groupname         = reservation.groupname  
    arl-list.active-flag       = res-line.active-flag  
    arl-list.gastnr            = res-line.gastnr  
    arl-list.gastnrmember      = res-line.gastnrmember
    arl-list.karteityp         = gmember.karteityp
    arl-list.reserve-int       = res-line.reserve-int  
    arl-list.zikatnr           = res-line.zikatnr  
    arl-list.betrieb-gastmem   = res-line.betrieb-gastmem  
    arl-list.pseudofix         = res-line.pseudofix  
    arl-list.reserve-char      = res-line.reserve-char  
    arl-list.bemerk            = res-line.bemerk    
    arl-list.depositbez        = reservation.depositbez  
    arl-list.depositbez2       = reservation.depositbez2  
    arl-list.bestat-dat        = reservation.bestat-dat  
    arl-list.briefnr           = reservation.briefnr  
    arl-list.rsv-gastnr        = reservation.gastnr  
    arl-list.rsv-resnr         = reservation.resnr  
    arl-list.rsv-bemerk        = reservation.bemerk  
    arl-list.rsv-grpflag       = reservation.grpflag  
    arl-list.recid-resline     = RECID(res-line).  
    
    /*ITA 150322*/
    IF res-line.resstatus NE 11 AND res-line.resstatus NE 13 THEN DO:
        FIND FIRST bresline WHERE bresline.resnr = res-line.resnr
            AND bresline.reslinnr NE res-line.reslinnr
            AND bresline.kontakt-nr EQ res-line.reslinnr
            AND (bresline.resstatus EQ 11 OR bresline.resstatus EQ 13)
            USE-INDEX relinr_index NO-LOCK NO-ERROR.
        IF AVAILABLE bresline THEN ASSIGN arl-list.sharer-no = bresline.kontakt-nr.
    END.
    ELSE ASSIGN arl-list.sharer-no = res-line.kontakt-nr.

    /*FDL June 21, 2023 => 937FC7*/
    bday = DATE(MONTH(gmember.geburtdatum1),DAY(gmember.geburtdatum1), YEAR(TODAY)).
    IF bday EQ TODAY THEN arl-list.birthday-flag = YES.

    FIND FIRST master WHERE master.resnr = res-line.resnr 
        NO-LOCK NO-ERROR. 
    IF AVAILABLE master AND master.active THEN arl-list.verstat = 1. 
    ELSE arl-list.verstat = 0. 
    
    FIND FIRST messages WHERE messages.resnr = res-line.resnr 
      AND messages.reslinnr = res-line.reslinnr NO-LOCK NO-ERROR. 
    IF AVAILABLE messages THEN arl-list.resline-wabkurz = "M".

    IF AVAILABLE res-line THEN   
    DO:  
        FIND FIRST guest WHERE guest.gastnr = reservation.gastnr NO-LOCK NO-ERROR.   
        arl-list.address = guest.adresse1.   
        arl-list.city = guest.wohnort + " " + guest.plz.  
    END.  
    IF res-line.kontignr GT 0 THEN   
    DO:   
        FIND FIRST kontline WHERE kontline.kontignr = res-line.kontignr   
            AND kontline.betriebsnr = 0   
            AND kontline.kontstat = 1 NO-LOCK NO-ERROR.   
        IF AVAILABLE kontline THEN
        DO:
            arl-list.comments = "ALLOTMENT: " + kontline.kontcode + chr(10).
        END.
        ELSE
            arl-list.comments = "ALLOTMENT: ".
    END.   
    ELSE IF res-line.kontignr LT 0 THEN   
    DO:   
        FIND FIRST kontline WHERE kontline.kontignr = res-line.kontignr   
            AND kontline.betriebsnr = 1   
            AND kontline.kontstat = 1 NO-LOCK NO-ERROR.   
        IF AVAILABLE kontline THEN
        DO:
            arl-list.comments = "GLOBAL RES: " + kontline.kontcode + chr(10).
        END.
        ELSE
            arl-list.comments = "GLOBAL RES: ".
    END.   

    /*Naufal - fix bug remark tidak muncul*/
    IF reservation.bemerk NE "" THEN 
    DO:
        IF reservation.bemerk EQ ? THEN
            arl-list.comments = " ".
        ELSE
            arl-list.comments = reservation.bemerk + chr(10).
    END.
    ELSE
    DO:
        arl-list.comments = " ".
    END.    
    
    IF res-line.bemerk NE "" THEN 
    DO:
        IF res-line.bemerk EQ ? THEN
            arl-list.comments = arl-list.comments + " ".
        ELSE
            arl-list.comments = arl-list.comments + res-line.bemerk.
    END.
    ELSE
    DO:
        arl-list.comments = arl-list.comments + " ".
    END.    
  
    DO loop-i = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
        comment-str = ENTRY(loop-i, res-line.zimmer-wunsch, ";").
        IF SUBSTR(comment-str,1,8)   = "$OTACOM$" THEN
        DO:
            arl-list.comments = arl-list.comments + chr(10) + "---OTA COMMENT---"
                + CHR(10) + ENTRY(3, comment-str, "$OTACOM$"). 
        END.
        ELSE
        DO:
            arl-list.comments = arl-list.comments + " ".
        END.
    END.  
  
    IF AVAILABLE res-line THEN  
    DO:  
        FIND FIRST gentable WHERE gentable.KEY = "reservation"  
            AND gentable.number1 = res-line.resnr  
            AND gentable.number2 = res-line.reslinnr NO-LOCK NO-ERROR.  
        IF AVAILABLE gentable THEN ASSIGN arl-list.resnr-fgcol = 12.  
    END.  
  
    IF AVAILABLE res-line AND show-rate THEN   
    DO:   
        FIND FIRST mc-guest WHERE mc-guest.gastnr = res-line.gastnrmember  
            AND mc-guest.activeflag = YES NO-LOCK NO-ERROR.  
        IF AVAILABLE mc-guest THEN  
        DO:  
            ASSIGN arl-list.mc-str-fgcol = 15.   
            ASSIGN arl-list.mc-str-bgcol  = 6.   
        END.  
    END.  
  
    IF AVAILABLE res-line AND res-line.resstatus GE 11 THEN   
    DO:   
        IF res-line.l-zuordnung[3] = 0 THEN  
            ASSIGN arl-list.rsv-name-fgcol = 9.   
        ELSE  
        ASSIGN   
            arl-list.rsv-name-bgcol = 9  
            arl-list.rsv-name-fgcol = 15.  
    END.   
  
    IF AVAILABLE res-line AND   
        (res-line.betrieb-gastmem = vipnr1 OR   
        res-line.betrieb-gastmem = vipnr2 OR   
        res-line.betrieb-gastmem = vipnr3 OR   
        res-line.betrieb-gastmem = vipnr4 OR   
        res-line.betrieb-gastmem = vipnr5 OR   
        res-line.betrieb-gastmem = vipnr6 OR   
        res-line.betrieb-gastmem = vipnr7 OR   
        res-line.betrieb-gastmem = vipnr8 OR   
        res-line.betrieb-gastmem = vipnr9) THEN   

/* SY 02 JUL 2017 */
        ASSIGN  arl-list.reslin-name-fgcol = 12. 
/*
        ASSIGN   
            arl-list.zinr-fgcol            = 12  
            arl-list.reslin-name-fgcol     = 12   
            arl-list.ankunft-fgcol         = 12   
            arl-list.anztage-fgcol         = 12   
            arl-list.abreise-fgcol         = 12   
            arl-list.segmentcode-fgcol     = 12.  
*/
    FIND FIRST htparam WHERE htparam.paramnr = 496 NO-LOCK.  
    all-inclusive = ";" + htparam.fchar + ";".  
    IF AVAILABLE res-line AND   
        all-inclusive MATCHES ("*;" + res-line.arrangement + ";*") THEN  
        ASSIGN   
            arl-list.reslin-name-bgcol    = 2  
            arl-list.reslin-name-fgcol    = 15  
            arl-list.segmentcode-bgcol    = 2  
            arl-list.segmentcode-fgcol    = 15.  
  
    IF AVAILABLE res-line AND res-line.active-flag = 1 AND long-stay GT 0   
        AND (res-line.abreise - res-line.ankunft) GE long-stay   
        AND res-line.erwachs GT 0 THEN   
        /* SY 02 JUL 2017 */     
        ASSIGN arl-list.abreise-fgcol = 915. 
/*
        ASSIGN   
            arl-list.reslin-name-fgcol = 15  
            arl-list.reslin-name-bgcol = 9.   
*/  
    IF AVAILABLE res-line AND res-line.active-flag LE 1 AND   
        res-line.abreise = res-line.ankunft THEN   
        ASSIGN   
            arl-list.reslin-name-fgcol = 0  
            arl-list.reslin-name-bgcol = 14.   
  
    IF AVAILABLE res-line AND res-line.pseudofix THEN   
        ASSIGN   
            arl-list.reslin-name-bgcol = 12  
            arl-list.reslin-name-fgcol = 15.   
  
      IF AVAILABLE res-line THEN   /* Task Rerpot exists */
      DO: 
        done-flag = ?.
        FIND FIRST reslin-queasy WHERE reslin-queasy.key = "flag"   
          AND reslin-queasy.resnr = res-line.resnr   
          AND reslin-queasy.reslinnr = res-line.reslinnr   
          AND reslin-queasy.betriebsnr = 0 NO-LOCK NO-ERROR.   
        IF AVAILABLE reslin-queasy THEN   
        DO:   
          done-flag = YES.
          FOR EACH reslin-queasy WHERE reslin-queasy.key = "flag"   
            AND reslin-queasy.resnr = res-line.resnr   
            AND reslin-queasy.reslinnr = res-line.reslinnr   
            AND reslin-queasy.betriebsnr = 0 NO-LOCK:
            IF (reslin-queasy.char1 NE "" AND reslin-queasy.deci1 = 0) 
              THEN done-flag = NO.
            IF (reslin-queasy.char2 NE "" AND reslin-queasy.deci2 = 0) 
              THEN done-flag = NO.
            IF (reslin-queasy.char3 NE "" AND reslin-queasy.deci3 = 0) 
              THEN done-flag = NO.
            IF NOT done-flag THEN LEAVE.
          END.
/* SY 02 JUL 2017 */
          IF done-flag THEN arl-list.ankunft-fgcol = 915.
          ELSE arl-list.ankunft-fgcol = 115.
/*
          IF done-flag THEN
          ASSIGN   
              arl-list.zinr-bgcol = 9  
              arl-list.zinr-fgcol = 15
          .   
          ELSE  
          ASSIGN   
              arl-list.zinr-bgcol = 1  
              arl-list.zinr-fgcol = 15
          .   
*/
        END.   
  
        IF res-line.active-flag = 0 AND res-line.zinr NE ""   
           AND res-line.ankunft = ci-date THEN   
        DO:   
          FIND FIRST zimmer WHERE zimmer.zinr = res-line.zinr NO-LOCK.   
          IF zimmer.zistatus = 1 THEN   
          ASSIGN 
              arl-list.zinr-fgcol = 0   
              arl-list.zinr-bgcol = 11
          .   
          ELSE IF zimmer.zistatus = 2 THEN   
          DO:   
            ASSIGN 
                arl-list.zinr-fgcol = 0   
                arl-list.zinr-bgcol = 10
            .   
            /* queuing room */
            FIND FIRST queasy WHERE queasy.KEY = 162
                AND queasy.char1   = zimmer.zinr 
                AND queasy.number1 = 0 NO-LOCK NO-ERROR.
            IF AVAILABLE queasy THEN
            ASSIGN 
                arl-list.zinr-fgcol = 15   
                arl-list.zinr-bgcol = 6
            .   
          END.   
          ELSE IF zimmer.zistatus = 3 THEN   
          ASSIGN 
              arl-list.zinr-fgcol = 12   
              arl-list.zinr-bgcol = 14
          .   
        END.   
      END.   
      
    /* DODY - 09 AUG 2018 : REQUEST ARTOTEL - REPEATER GUEST COLOR */
    IF AVAILABLE res-line THEN
    DO:
        FIND FIRST guest WHERE guest.gastnr EQ res-line.gastnrmember NO-LOCK NO-ERROR.
        IF AVAILABLE guest THEN
        DO:
            IF guest.zimmeranz GE stay AND stay GT 0 THEN
            DO:
                ASSIGN
                    arl-list.reslin-name-fgcol = 15
                    arl-list.reslin-name-bgcol = 3
                .
            END.        
        END.                   
    END.

      /*ITA 090715*/
    DO loopi = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
        IF ENTRY(loopi,res-line.zimmer-wunsch, ";") = "WCI-flag" THEN DO:
            ASSIGN arl-list.webci = ENTRY(loopi,res-line.zimmer-wunsch, ";").
            LEAVE.
        END.
    END.

    IF arl-list.voucher-nr NE "" THEN ASSIGN arl-list.voucher-flag = "L".
    IF arl-list.kontignr GT 0 THEN ASSIGN arl-list.kontignr-flag = "A ".
    IF arl-list.webci NE "" THEN DO:
        DO loopj = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
            str1 = ENTRY(loopj,res-line.zimmer-wunsch, ";").
            IF str1 MATCHES "*WCI-req*" THEN 
            DO:
                str2 = ENTRY(2, str1, "=").
                DO loopk = 1 TO NUM-ENTRIES(str2, ","):
                    FIND FIRST queasy WHERE queasy.KEY = 160
                        AND queasy.number1 = INT(ENTRY(loopk, str2, ",")) NO-LOCK NO-ERROR.
                    IF AVAILABLE queasy THEN 
                    DO:
                        DO loopl = 1 TO NUM-ENTRIES(queasy.char1, ";") :
                            IF ENTRY(loopl, queasy.char1, ";") MATCHES "*en*" THEN
                            DO:
                                ASSIGN web-com = ENTRY(2, ENTRY(loopl, queasy.char1, ";"), "=") + ", " + web-com.
                                LEAVE.
                            END.
                        END.
                    END.
                END.
                ASSIGN arl-list.comments = "-WEB C/I PREFERENCE-" + CHR(10) + web-com + CHR(10) + arl-list.comments .
            END.
        END.
        ASSIGN arl-list.webci-flag = "W".

        FIND FIRST queasy WHERE queasy.KEY = 167 AND queasy.number1 = res-line.resnr  NO-LOCK NO-ERROR.
        IF AVAILABLE queasy THEN DO:
            IF arl-list.comments NE " " THEN
                ASSIGN arl-list.comments = arl-list.comments + CHR(10) + queasy.char3.
            ELSE ASSIGN arl-list.comments = "-WEB C/I PREFERENCE-" + CHR(10) + queasy.char3.
        END.
    END.
    IF arl-list.webci-flag EQ "" THEN
    DO:
        IF res-line.zimmer-wunsch MATCHES "*PCIFLAG*" THEN arl-list.webci-flag = "W".
    END.
END.  


