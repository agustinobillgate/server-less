/*FT 210514 perbaikan str apabila length lebih dr 120*/

DEFINE TEMP-TABLE out-list 
  FIELD seq   AS INTEGER INITIAL 0
  FIELD etage AS INTEGER 
  FIELD stat  AS INTEGER 
  FIELD i     AS INTEGER 
  FIELD flag  AS INTEGER 
  FIELD anz   AS INTEGER 
  FIELD name  AS CHAR FORMAT "x(4)" LABEL "Stat" 
  FIELD STR   AS CHAR FORMAT "x(120)" LABEL ""
  FIELD sum   AS INTEGER FORMAT ">>>" LABEL "Tot" 
  FIELD str1  AS CHAR
  FIELD room  AS CHARACTER
  FIELD pax   AS CHARACTER.

DEFINE BUFFER reslin1 FOR res-line.

DEF INPUT  PARAMETER pvILanguage     AS INTEGER NO-UNDO.
DEF OUTPUT PARAMETER ci-date         AS DATE.
DEF OUTPUT PARAMETER TABLE FOR out-list.
/*DEFINE VARIABLE pvILanguage     AS INTEGER NO-UNDO.
DEFINE VARIABLE ci-date         AS DATE.*/

DEFINE VARIABLE netage AS INTEGER NO-UNDO.
DEFINE VARIABLE nseq   AS INTEGER NO-UNDO.
DEFINE VARIABLE nsum   AS INTEGER NO-UNDO.
DEFINE VARIABLE i      AS INTEGER NO-UNDO.
DEFINE VARIABLE loop   AS INTEGER NO-UNDO.
DEFINE VARIABLE nstat  AS INTEGER NO-UNDO. 
DEFINE VARIABLE nstr   AS CHAR    NO-UNDO.

DEFINE BUFFER out-list-buff FOR out-list.

DEFINE VARIABLE stat AS CHAR FORMAT "x(2)" EXTENT 12 INITIAL 
  ["VC", "VU", "VD", "ED", "OD", "OC", "OO", "OM", "CO", "HU", "EA", "DnD"]. 
DEFINE VARIABLE tot-stat AS INTEGER EXTENT 12. 

{supertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "hk-countsheet". 

RUN htpdate.p (110, OUTPUT ci-date).
RUN create-list.                                     

PROCEDURE create-list: 
DEFINE VARIABLE reihe       AS INTEGER INITIAL 0.
DEFINE VARIABLE n           AS INTEGER. 
DEFINE VARIABLE from-etage  AS INTEGER INITIAL 9999. 
DEFINE VARIABLE anz-etage   AS INTEGER. 
DEFINE VARIABLE sum         AS INTEGER. 
DEFINE VARIABLE pax         AS INTEGER. 
DEFINE VARIABLE hu-flag     AS LOGICAL. 
DEFINE VARIABLE om-flag     AS LOGICAL. 

  FOR EACH zimmer NO-LOCK: 
    IF zimmer.etage GT anz-etage THEN anz-etage = zimmer.etage. 
    IF zimmer.etage LT from-etage THEN from-etage = zimmer.etage. 
  END.
  
  DO n = from-etage TO anz-etage: 
    FIND FIRST zimmer WHERE zimmer.etage = n NO-LOCK NO-ERROR.
    IF AVAILABLE zimmer THEN
    DO:
      CREATE out-list. 
      reihe = reihe + 1.
      ASSIGN out-list.seq = reihe
          out-list.str = ""
          out-list.stat = 9999.
      
      CREATE out-list. 
      reihe = reihe + 1.
      ASSIGN 
        out-list.seq = reihe
        out-list.str = translateExtended ("FLOOR",lvCAREA,"") + " " + STRING(n) 
        out-list.str1 = "FLOOR"
        out-list.stat = 9999.
      FOR EACH zimmer WHERE zimmer.etage = n 
        NO-LOCK BY zimmer.etage BY zimmer.zistatus BY (zimmer.zinr): 
        hu-flag = NO. 
        om-flag = NO. 
      
        IF zimmer.zistat GE 3 AND zimmer.zistat LE 5 THEN 
        DO: 
          FIND FIRST res-line WHERE res-line.active-flag = 1 
            AND res-line.zinr = zimmer.zinr 
            AND res-line.zipreis = 0 AND res-line.resstatus EQ 6 
            NO-LOCK NO-ERROR. 
          IF AVAILABLE res-line THEN 
          DO: 
            hu-flag = YES. 
            FIND FIRST reservation WHERE reservation.resnr = res-line.resnr 
              NO-LOCK. 
            FIND FIRST segment WHERE segment.segmentcode 
              = reservation.segmentcode NO-LOCK. 
            IF segment.betriebsnr NE 2  /* Compliment */ THEN 
            DO: 
              FIND FIRST out-list WHERE out-list.etage = zimmer.etage 
                AND out-list.stat = 8 AND out-list.flag = 0 NO-ERROR. 
              IF NOT AVAILABLE out-list THEN 
              DO: 
                CREATE out-list. 
                reihe = reihe + 1.
                ASSIGN 
                  out-list.seq = reihe
                  out-list.etage = zimmer.etage 
                  out-list.stat = 8 
                  out-list.name = stat[9]
                  out-list.flag = 0. 
              END. 
              /*FTELSE IF out-list.i = 10 THEN 
              DO: 
                out-list.flag = 1. 
                sum = out-list.anz. 
                CREATE out-list. 
                reihe = reihe + 1.
                ASSIGN 
                  out-list.seq = reihe
                  out-list.etage = zimmer.etage 
                  out-list.stat = 8 
                  out-list.anz = sum.
              END. */ 
              tot-stat[9] = tot-stat[9] + 1. 
              out-list.i = out-list.i + 1. 
              out-list.anz = out-list.anz + 1. 
              out-list.str = out-list.str + STRING(zimmer.zinr,"x(6)") /*MT 25/07/12 */
                + STRING(res-line.gratis,">>    ").
              out-list.room = out-list.room + STRING(zimmer.zinr,"x(6)").
              out-list.pax = out-list.pax + STRING(res-line.gratis,">>    ").
            END. 
            ELSE /* house use */ 
            DO: 
              FIND FIRST out-list WHERE out-list.etage = zimmer.etage 
                AND out-list.stat = 9 AND out-list.flag = 0 NO-ERROR. 
              IF NOT AVAILABLE out-list THEN 
              DO: 
                CREATE out-list. 
                reihe = reihe + 1.
                ASSIGN 
                  out-list.seq = reihe
                  out-list.etage = zimmer.etage 
                  out-list.stat = 9 
                  out-list.name = stat[10]
                  out-list.flag = 0. 
              END. 
              /*FTELSE IF out-list.i = 10 THEN 
              DO: 
                out-list.flag = 1. 
                sum = out-list.anz. 
                CREATE out-list. 
                reihe = reihe + 1.
                ASSIGN 
                  out-list.seq = reihe
                  out-list.etage = zimmer.etage 
                  out-list.stat = 9 
                  out-list.anz = sum. 
              END. */
              tot-stat[10] = tot-stat[10] + 1. 
              out-list.i = out-list.i + 1. 
              out-list.anz = out-list.anz + 1. 
              out-list.str = out-list.str + STRING(zimmer.zinr,"x(6)")  /*MT 25/07/12 */
                + STRING(res-line.gratis,">>    "). 
              out-list.room = out-list.room + STRING(zimmer.zinr,"x(6)").
              out-list.pax = out-list.pax + STRING(res-line.gratis,">>    ").
            END. 
          END. 
        END. 
        ELSE IF zimmer.zistat = 8 THEN DO:  /*ITA 250814*/
            hu-flag = NO. 
            om-flag = NO. 
            FIND FIRST res-line WHERE res-line.active-flag = 1 
            AND res-line.zinr = zimmer.zinr 
            NO-LOCK NO-ERROR.
          IF AVAILABLE res-line THEN 
          DO:
              hu-flag = YES. 
              FIND FIRST out-list WHERE out-list.etage = zimmer.etage 
                AND out-list.stat = 12 AND out-list.flag = 0 NO-ERROR.
              IF NOT AVAILABLE out-list THEN 
              DO: 
                CREATE out-list. 
                reihe = reihe + 1.
                ASSIGN 
                  out-list.seq = reihe
                  out-list.etage = zimmer.etage 
                  out-list.stat = 12
                  out-list.name = stat[12]. 
              END. 
              ELSE IF out-list.i = 10 THEN 
              DO: 
                out-list.flag = 1. 
                sum = out-list.anz. 
                CREATE out-list. 
                reihe = reihe + 1.
                ASSIGN 
                  out-list.seq = reihe
                  out-list.etage = zimmer.etage 
                  out-list.stat = 12
                  out-list.anz = sum. 
              END. 
              tot-stat[12] = tot-stat[12] + 1. 
              out-list.i = out-list.i + 1. 
              out-list.anz = out-list.anz + 1. 
              out-list.str = out-list.str + STRING(zimmer.zinr,"x(6)") 
                + STRING(res-line.erwach,">>    "). 
              out-list.room = out-list.room + STRING(zimmer.zinr,"x(6)").
              out-list.pax = out-list.pax + STRING(res-line.erwach,">>>   ").
             /*end*/
          END.
        END.
        ELSE IF zimmer.zistat GE 0 AND zimmer.zistat LE 2 THEN 
        DO: 
          FIND FIRST outorder WHERE outorder.betriebsnr GT 0 
            AND outorder.gespstart LE ci-date 
            AND outorder.gespende GE ci-date 
            AND outorder.zinr = zimmer.zinr NO-LOCK NO-ERROR. 
          IF AVAILABLE outorder THEN 
          DO: 
            om-flag = YES. 
            FIND FIRST out-list WHERE out-list.etage = zimmer.etage 
              AND out-list.stat = 7 AND out-list.flag = 0 NO-ERROR. 
            IF NOT AVAILABLE out-list THEN 
            DO: 
              CREATE out-list. 
              reihe = reihe + 1.
              ASSIGN 
                out-list.flag = 0
                out-list.seq = reihe
                out-list.etage = zimmer.etage 
                out-list.stat = 7 
                out-list.name = stat[8]. 
            END. 
            /*FTELSE IF out-list.i = 10 THEN 
            DO: 
              out-list.flag = 1. 
              sum = out-list.anz. 
              CREATE out-list. 
              reihe = reihe + 1.
              ASSIGN 
                out-list.seq = reihe
                out-list.etage = zimmer.etage 
                out-list.stat = 7 
                out-list.anz = sum. 
            END. */
            tot-stat[8] = tot-stat[8] + 1. 
            out-list.i = out-list.i + 1. 
            out-list.anz = out-list.anz + 1. 
            out-list.str = out-list.str + STRING(zimmer.zinr,"x(6)") + "      ". /*MT 25/07/12 */
            out-list.room = out-list.room + STRING(zimmer.zinr,"x(6)").
          END. 
        END. 
        IF NOT hu-flag AND NOT om-flag THEN 
        DO: 
          FIND FIRST out-list WHERE out-list.etage = zimmer.etage 
            AND out-list.stat = zimmer.zistatus AND out-list.flag = 0 NO-ERROR. 
          IF NOT AVAILABLE out-list THEN 
          DO: 
            CREATE out-list. 
            reihe = reihe + 1.
            ASSIGN 
              out-list.flag = 0
              out-list.seq = reihe
              out-list.etage = zimmer.etage 
              out-list.stat = zimmer.zistat 
              out-list.name = stat[zimmer.zistat + 1]. 
          END. 
          /*FTELSE IF out-list.i = 10 THEN 
          DO: 
            out-list.flag = 1. 
            sum = out-list.anz. 
            CREATE out-list. 
            reihe = reihe + 1.
            ASSIGN 
              out-list.seq = reihe
              out-list.etage = zimmer.etage 
              out-list.stat = zimmer.zistat 
              out-list.anz = sum. 
          END. */
          tot-stat[zimmer.zistat + 1] = tot-stat[zimmer.zistat + 1] + 1. 
          out-list.i = out-list.i + 1. 
          out-list.anz = out-list.anz + 1. 
          IF zimmer.zistat GE 3 AND zimmer.zistat LE 5 THEN 
          DO: 
            pax = 0. 
            FOR EACH res-line WHERE res-line.active-flag = 1 
              AND res-line.zinr = zimmer.zinr 
              AND res-line.resstatus NE 12 NO-LOCK: 
              pax = pax + res-line.erwachs. 
            END. 
            out-list.str = out-list.str + STRING(zimmer.zinr,"x(6)")    /*MT 25/07/12 */
              + STRING(pax,">>    "). 
            out-list.room = out-list.room + STRING(zimmer.zinr,"x(6)").
            out-list.pax = out-list.pax + STRING(pax,">>>   ").
          END. 
          ELSE
          DO: 
              out-list.str = out-list.str + STRING(zimmer.zinr,"x(6)") /*MT 25/07/12 */
                + "      ". 
              out-list.room = out-list.room + STRING(zimmer.zinr,"x(6)").
          END.
              
        END. 
      
        FIND FIRST reslin1 WHERE reslin1.active-flag = 0 AND (reslin1.resstatus = 1 OR
          reslin1.resstatus = 2 OR reslin1.resstatus = 3 OR reslin1.resstatus = 4)
          AND reslin1.ankunft = ci-date AND reslin1.zinr = zimmer.zinr
          NO-LOCK NO-ERROR.
        IF AVAILABLE reslin1 THEN
        DO:
            pax = 0.
            FIND FIRST out-list WHERE out-list.etage = zimmer.etage AND 
                out-list.flag = 0 AND out-list.NAME = "EA" NO-ERROR.
            IF NOT AVAILABLE out-list THEN
            DO: 
                CREATE out-list.
                reihe = reihe + 1.
                ASSIGN 
                    out-list.seq = reihe
                    out-list.flag  = 0
                    out-list.etage = zimmer.etage
                    out-list.stat  = 11
                    out-list.NAME  = "EA".
            END.
            /*FTELSE IF out-list.i = 10 THEN 
            DO: 
                out-list.flag = 1. 
                sum = out-list.anz. 
                CREATE out-list. 
                reihe = reihe + 1.
                ASSIGN 
                    out-list.seq = reihe
                    out-list.etage = zimmer.etage 
                    out-list.stat = 11
                    out-list.anz = sum. 
            END. */
            tot-stat[11] = tot-stat[11] + 1. 
            out-list.i = out-list.i + 1. 
            out-list.anz = out-list.anz + 1.
            FOR EACH reslin1 WHERE reslin1.active-flag = 0 AND (reslin1.resstatus = 1 OR
                reslin1.resstatus = 2 OR reslin1.resstatus = 3 OR reslin1.resstatus = 4
                OR reslin1.resstatus = 13) AND reslin1.zinr = zimmer.zinr 
                AND reslin1.ankunft = ci-date NO-LOCK:
                pax = pax + reslin1.erwachs.
            END.
            out-list.str = out-list.str + STRING(zimmer.zinr,"x(6)") /*MT 25/07/12 */
                + STRING(pax,">>    "). 
            out-list.room = out-list.room + STRING(zimmer.zinr,"x(6)").
            out-list.pax = out-list.pax + STRING(pax,">>>   ").
        END.
      END. /* FOR EACH zimmer */
    END. /* IF AVAILABLE zimmer */
  END. /* DO n ... */

  FOR EACH out-list WHERE out-list.flag = 0: 
    out-list.sum = out-list.anz. 
  END. 
  
  /*FT 210514*/
  FOR EACH out-list BY out-list.seq:
    IF LENGTH(out-list.str) GT 120 THEN
    DO:
      ASSIGN
        netage = out-list.etage
        nseq   = out-list.seq
        nsum = out-list.anz
        nstr = out-list.str
        out-list.str = SUBSTR(nstr,1,120)
        out-list.SUM = 0.
      loop = TRUNCATE ( LENGTH(nstr) / 120, 0).
      DO i = 1 TO loop:
         nseq = nseq + 1.
         CREATE out-list-buff.
         ASSIGN
           out-list-buff.seq = nseq
           out-list-buff.etage = netage
           out-list-buff.stat = nstat
           out-list-buff.str = SUBSTR(nstr, i * 120 + 1, (i + 1) * 120)
           out-list-buff.flag = 3.
         IF i = loop THEN out-list-buff.SUM = nsum.
      END.
      FOR EACH out-list-buff WHERE out-list-buff.seq GT (nseq - loop) AND out-list-buff.flag NE 3 :
        nseq = nseq + 1.
        out-list-buff.seq = nseq.
      END.
    END.
  END.

  reihe = nseq.
  
  CREATE out-list. 
  reihe = reihe + 1.
  ASSIGN out-list.seq = reihe.

  CREATE out-list. 
  reihe = reihe + 1.
  ASSIGN 
    out-list.seq = reihe
    out-list.str = translateExtended ("SUMMARY :",lvCAREA,"") + "   ". 
    out-list.room = translateExtended ("SUMMARY :",lvCAREA,"") + "   ".
  DO n = 1 TO 12: 
    IF tot-stat[n] NE 0 THEN 
    DO: 
      out-list.str = out-list.str + stat[n] + "=" + STRING(tot-stat[n]) + "   ". 
      out-list.room = out-list.room + stat[n] + "=" + STRING(tot-stat[n]) + "   ".
    END. 
  END. 
END. 
 

