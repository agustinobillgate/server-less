/*DEF TEMP-TABLE t-res-history LIKE res-history.*/

/* Custom for VHP Web based only */
DEF TEMP-TABLE t-res-history LIKE res-history
    FIELD gname     AS CHAR
    FIELD zinr      AS CHAR
    FIELD ankunft   AS DATE
    FIELD abreise   AS DATE
    FIELD grpname   AS CHAR
    FIELD wa-time   AS CHAR
    FIELD ack       AS LOGICAL
    FIELD res       AS CHAR.
/* End of custom */

DEF INPUT PARAMETER case-type   AS INTEGER  NO-UNDO.
DEF INPUT PARAMETER int1        AS INTEGER  NO-UNDO.
DEF INPUT PARAMETER int2        AS INTEGER  NO-UNDO.
DEF INPUT PARAMETER int3        AS INTEGER  NO-UNDO.
DEF INPUT PARAMETER datum1      AS DATE     NO-UNDO.
DEF INPUT PARAMETER char1       AS CHAR     NO-UNDO.
DEF INPUT PARAMETER char2       AS CHAR     NO-UNDO.
DEF OUTPUT PARAMETER TABLE FOR t-res-history.

/* Custom for VHP Web based only */
DEF VAR ct      AS CHAR NO-UNDO.
DEF VAR st      AS CHAR NO-UNDO.
DEF VAR curr-i  AS INT NO-UNDO.
/* End of custom */

CASE case-type:
    WHEN 1 THEN
    DO:
        FIND FIRST res-history WHERE res-history.nr = int1
            AND res-history.betriebsnr NE int2 USE-INDEX bediener-time-date_ix
            NO-LOCK NO-ERROR.
        IF AVAILABLE res-history THEN
        DO:
            CREATE t-res-history.
            BUFFER-COPY res-history TO t-res-history.
        END.
    END.
    WHEN 2 THEN /* Wake Up Call used by vhpif-pabx */
    DO:
        FIND FIRST res-history WHERE 
            res-history.resnr    = int1 AND
            res-history.reslinnr = int2 AND
            res-history.zeit     = int3 AND
            res-history.datum    = datum1
            AND res-history.action = "Wake Up Call"
            NO-LOCK NO-ERROR.
        IF AVAILABLE res-history THEN
        DO:
            FIND CURRENT res-history EXCLUSIVE-LOCK.
            ASSIGN res-history.aenderung = res-history.aenderung
                   + " Stat: ACK" + ";".
            FIND CURRENT res-history NO-LOCK.
            CREATE t-res-history.
            BUFFER-COPY res-history TO t-res-history. 
        END.
    END.
    WHEN 3 THEN /* Wake Up Call used by telop-wacallUI */
    DO:
        FOR EACH res-history WHERE 
            res-history.resnr    = int1 AND
            res-history.zeit     = int3 AND
            res-history.datum    = datum1
            AND res-history.action = "Wake Up Call" NO-LOCK:
            CREATE t-res-history.
            BUFFER-COPY res-history TO t-res-history. 
        END.
    END.
    WHEN 4 THEN /* Wake Up Call used by telop-wacallUI */
    DO:
        FOR EACH res-history WHERE 
            res-history.zeit     GE 0 AND
            res-history.datum    GE TODAY - 1
            AND res-history.action = "Wake Up Call" NO-LOCK:
            CREATE t-res-history.
            BUFFER-COPY res-history TO t-res-history. 
            FIND FIRST res-line WHERE res-line.resnr = res-history.resnr
                AND res-line.reslinnr = res-history.reslinnr
                NO-LOCK.
            FIND FIRST reservation WHERE reservation.resnr
                = res-history.resnr NO-LOCK.
            /*ASSIGN t-res-history.aenderung = t-res-history.aenderung
                + "Name: " + res-line.name + ";"
                + "C/I : " + STRING(res-line.ankunft) + ";"
                + "C/O : " + STRING(res-line.abreise) + ";"
            .
            IF reservation.groupname NE "" THEN
            ASSIGN t-res-history.aenderung = t-res-history.aenderung
                + "Grp : " + reservation.groupname + ";".*/
            /* Custom for VHP Web based only */
            ASSIGN t-res-history.gname = res-line.name
                t-res-history.zinr = res-line.zinr
                t-res-history.ankunft = res-line.ankunft
                t-res-history.abreise = res-line.abreise
                .
            IF reservation.groupname NE "" THEN
            ASSIGN t-res-history.grpname = reservation.groupname.

            ct = TRIM(ENTRY(1, t-res-history.aenderung, ";")).
            IF ct MATCHES ("*CANCEL*") THEN t-res-history.wa-time = "CANCEL". 
            DO curr-i = 2 TO NUM-ENTRIES(t-res-history.aenderung, ";"):
                ASSIGN
                    ct = TRIM(ENTRY(curr-i, t-res-history.aenderung, ";"))
                    st = SUBSTR(ct, 1, 5)
                .
                CASE st:
                    WHEN "STAT:" THEN
                    DO:
                        IF TRIM(SUBSTR(ct, 6)) = "ACK" THEN
                          t-res-history.ack = YES.
                    END.
                    WHEN "DayD:" THEN
                          t-res-history.res = TRIM(SUBSTR(ct, 6)).
                END CASE.
            END.
            /* End of custom */
        END.
    END.
    WHEN 5 THEN /* Wake Up Call used by vhpif-pabx neax-wakeup */
    DO:
    DEF VARIABLE rmNo    AS CHAR NO-UNDO INIT "".
    DEF VARIABLE wa-time AS CHAR NO-UNDO.
      FIND FIRST nebenst WHERE nebenst.nebenstelle = char1 
        AND nebenst.nebst-type = 0 
        AND nebenst.zinr NE "" NO-LOCK NO-ERROR.
      IF AVAILABLE nebenst THEN rmNo = nebenst.zinr.
      ELSE
      DO:
        FIND FIRST zimmer WHERE zimmer.nebenstelle = char1 
          NO-LOCK NO-ERROR.
        IF NOT AVAILABLE zimmer THEN
          FIND FIRST zimmer WHERE zimmer.zinr = char1 NO-LOCK NO-ERROR.
        IF AVAILABLE zimmer THEN rmNo = zimmer.zinr.
      END.
      IF rmNo NE "" THEN
      DO:
          wa-time = SUBSTR(char2, 1, 2) + ":" + SUBSTR(char2, 3, 2).
          FIND FIRST res-line WHERE res-line.resstatus = 6
              AND res-line.zinr = rmNo NO-LOCK NO-ERROR.
          IF NOT AVAILABLE res-line THEN
          FIND FIRST res-line WHERE res-line.resstatus = 13
              AND res-line.l-zuordnung[3] = 0
              AND res-line.zinr = rmNo NO-LOCK NO-ERROR.
          IF AVAILABLE res-line THEN
          DO:
              FIND FIRST res-history WHERE 
                  res-history.action   = "Wake Up Call"    AND
                  res-history.resnr    = res-line.resnr    AND
                  res-history.reslinnr = res-line.reslinnr AND
                  res-history.datum    = datum1 - 1        AND
                  res-history.aenderung MATCHES ("* " + res-line.zinr + ";*") AND
                  res-history.aenderung MATCHES ("*" + wa-time + ";*")
                  EXCLUSIVE-LOCK NO-ERROR.
              IF NOT AVAILABLE res-history THEN
              FIND FIRST res-history WHERE 
                  res-history.action   = "Wake Up Call"    AND
                  res-history.resnr    = res-line.resnr    AND
                  res-history.reslinnr = res-line.reslinnr AND
                  res-history.datum    = datum1            AND
                  res-history.aenderung MATCHES ("* " + res-line.zinr + ";*") AND
                  res-history.aenderung MATCHES ("*" + wa-time + ";*")
                  EXCLUSIVE-LOCK NO-ERROR.
              IF AVAILABLE res-history THEN
              DO:
                CASE int1:
                    WHEN 1 THEN res-history.aenderung = 
                      res-history.aenderung + "DayD: Answer" + ";". 
                    WHEN 2 THEN res-history.aenderung = 
                      res-history.aenderung + "DayD: Busy" + ";". 
                    WHEN 3 THEN res-history.aenderung = 
                      res-history.aenderung + "DayD: No Answer" + ";". 
                    WHEN 4 THEN res-history.aenderung = 
                      res-history.aenderung + "DayD: Block" + ";". 
                    WHEN 5 THEN res-history.aenderung = 
                      res-history.aenderung + "DayD: Call Termination" + ";". 
                END CASE.
                FIND CURRENT res-history NO-LOCK.
              END.
                  
          END.
      END.
    END.

END CASE.

