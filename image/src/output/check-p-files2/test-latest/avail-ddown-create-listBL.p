.
DEFINE TEMP-TABLE rlist
    FIELD resnr                 AS CHAR LABEL "ResNo"
    FIELD zinr                  LIKE res-line.zinr
    FIELD ankunft               LIKE res-line.ankunft
    FIELD abreise               LIKE res-line.abreise
    FIELD zimmeranz             LIKE res-line.zimmeranz
    FIELD resstatus             LIKE res-line.resstatus
    FIELD zipreis               LIKE res-line.zipreis
    FIELD erwachs               LIKE res-line.erwachs
    FIELD kind1                 LIKE res-line.kind1
    FIELD gratis                LIKE res-line.gratis
    FIELD NAME                  LIKE res-line.NAME
    FIELD rsvName               AS CHAR FORMAT "x(24)" LABEL "Reserved Name"
    FIELD confirmed             AS LOGICAL INITIAL NO
    FIELD sleeping              AS LOGICAL INITIAL YES
    FIELD bezeich               AS CHAR FORMAT "x(15)"
    FIELD res-status            AS CHAR FORMAT "x(15)"
.

DEF INPUT PARAMETER pvILanguage AS INTEGER  NO-UNDO.
DEF INPUT PARAMETER curr-zikat  AS INTEGER  NO-UNDO.
DEF INPUT PARAMETER datum       AS DATE     NO-UNDO.
DEF OUTPUT PARAMETER TABLE FOR rlist.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "availability_ddownUI". 

DEFINE VARIABLE stat-list AS CHAR EXTENT 13 FORMAT "x(9)"  NO-UNDO.
stat-list[1]  = translateExtended ("Guaranted",lvCAREA,""). 
stat-list[2]  = translateExtended ("6 PM",lvCAREA,""). 
stat-list[3]  = translateExtended ("Tentative",lvCAREA,""). 
stat-list[4]  = translateExtended ("WaitList",lvCAREA,""). 
stat-list[5]  = translateExtended ("OralConform",lvCAREA,""). 
stat-list[6]  = translateExtended ("Inhouse",lvCAREA,""). 
stat-list[7]  = "". 
stat-list[8]  = translateExtended ("Departed",lvCAREA,""). 
stat-list[9]  = translateExtended ("Cancelled",lvCAREA,""). 
stat-list[10] = translateExtended ("NoShow",lvCAREA,""). 
stat-list[11] = translateExtended ("ShareRes",lvCAREA,""). 
stat-list[12] = translateExtended ("Extra Bill",lvCAREA,""). 
stat-list[13] = translateExtended ("RmSharer",lvCAREA,""). 


RUN create-list.

PROCEDURE create-list: 
DEFINE VARIABLE do-it AS LOGICAL NO-UNDO.
DEFINE BUFFER rbuff FOR res-line.
DEFINE VAR tot-pax               AS INTEGER.
DEFINE VAR tot-adult             AS INTEGER.
DEFINE VAR tot-ch1               AS INTEGER.
DEFINE VAR tot-ch2               AS INTEGER.
DEFINE VAR tot-compli            AS INTEGER.
DEFINE VAR tot-nights            AS INTEGER.
DEFINE VAR tot-qty               AS DECIMAL.

    FOR EACH rlist :
        DELETE rlist.
    END.

    ASSIGN 
    tot-pax         = 0
    tot-adult       = 0
    tot-ch1         = 0
    tot-compli      = 0
    tot-qty         = 0
    .

    FOR EACH res-line WHERE res-line.active-flag LE 1
      AND res-line.resstatus NE 12
      AND res-line.zikatnr = curr-zikat
      AND NOT res-line.ankunft GT datum
      AND NOT res-line.abreise LE datum
      AND res-line.l-zuordnung[3] = 0 NO-LOCK 
      BY res-line.resnr BY res-line.kontakt-nr:

        CREATE rlist.
        ASSIGN
            rlist.resnr         = STRING(res-line.resnr)
            rlist.zinr          = res-line.zinr
            rlist.NAME          = res-line.NAME
            rlist.ankunft       = res-line.ankunft
            rlist.abreise       = res-line.abreise
            rlist.zimmeranz     = res-line.zimmeranz
            rlist.zipreis       = res-line.zipreis
            rlist.erwachs       = res-line.erwachs
            rlist.kind1         = res-line.kind1
            rlist.gratis        = res-line.gratis
            rlist.res-status    = stat-list[res-line.resstatus].
        .
      
      IF res-line.zinr NE "" THEN
      DO:
        FIND FIRST zimmer WHERE zimmer.zinr = res-line.zinr NO-LOCK NO-ERROR.
        IF AVAILABLE zimmer AND NOT zimmer.sleeping THEN rlist.sleeping = NO.
      END.
      IF res-line.resstatus = 11 OR res-line.resstatus = 13 THEN
      DO:
        FIND FIRST rbuff WHERE rbuff.resnr = INT(res-line.resnr)
            AND rbuff.reslinnr = res-line.kontakt-nr NO-LOCK NO-ERROR.
        IF AVAILABLE rbuff THEN
          rlist.confirmed = (rbuff.resstatus LE 2 OR rbuff.resstatus = 5
          OR rbuff.resstatus = 6). 
        ELSE rlist.confirmed = YES.
      END.
      FIND FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK.
      rlist.rsvName = guest.NAME + ", " + guest.anredefirma. 
      FIND FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK NO-ERROR.
      IF AVAILABLE zimkateg THEN rlist.bezeich = zimkateg.bezeich.    

      ASSIGN
          tot-pax        = tot-pax + res-line.zimmeranz
          tot-adult      = tot-adult + (res-line.erwachs * res-line.zimmeranz)
          tot-ch1        = tot-ch1 + (res-line.kind1 * res-line.zimmeranz) 
          tot-compli     = tot-compli + (res-line.gratis * res-line.zimmeranz)
          tot-qty        = tot-qty + res-line.zipreis
       .
    END.
    
    IF tot-pax NE 0 THEN
    DO:
    CREATE rlist.
        ASSIGN
         rlist.rsvName          = "T O T A L"
         rlist.zimmeranz        = tot-pax
         rlist.ankunft          = ?
         rlist.abreise          = ?
         rlist.erwachs          = tot-adult
         rlist.kind1            = tot-ch1
         rlist.gratis           = tot-compli
         rlist.zipreis          = tot-qty
    .
    END.
END.
