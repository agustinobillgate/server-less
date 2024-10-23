/* SY 25 JUL 2017 
bediener.mapi-profile will be used at setup-userUI.p 
*/

DEFINE TEMP-TABLE t-bediener LIKE bediener.
DEFINE TEMP-TABLE dept-list
    FIELD deptNo AS INTEGER
.

DEFINE INPUT PARAMETER case-type AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER TABLE FOR t-bediener.
DEFINE OUTPUT PARAMETER success-flag AS LOGICAL INIT NO.

/* SY JUL 25 2017 */
DEF BUFFER kbuff FOR kellner.

FIND FIRST t-bediener NO-ERROR.
/* SY JUL 25 2017 */
IF NOT AVAILABLE t-bediener THEN RETURN.

CASE case-type:
    WHEN 1 THEN
    DO:
        CREATE bediener.
        BUFFER-COPY t-bediener TO bediener.
        FIND CURRENT bediener NO-LOCK. /* SY JUL 25 2017 */
        ASSIGN success-flag = YES.
    END.
    WHEN 2 THEN
    DO:
        FIND FIRST bediener WHERE bediener.userinit = t-bediener.userinit EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE bediener THEN
        DO:
            BUFFER-COPY t-bediener TO bediener.
            FIND CURRENT bediener NO-LOCK. /* SY */
            ASSIGN success-flag = YES.
        END.
    END.
    /* SY JUL 25 2017 */
    WHEN 3 THEN     /* btn-chg in setup-userUI */
    DO:
    DEF VARIABLE prevName AS CHAR NO-UNDO.
        FIND FIRST bediener WHERE bediener.nr = t-bediener.nr EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE bediener THEN
        DO:
            ASSIGN prevName = bediener.username.
            BUFFER-COPY t-bediener TO bediener.
            FIND CURRENT bediener NO-LOCK.
            IF prevName NE t-bediener.username THEN
            DO:
                FIND FIRST kellner WHERE 
                    kellner.kellner-nr = INTEGER(bediener.userinit)
                    NO-LOCK NO-ERROR.
                DO WHILE AVAILABLE kellner:
                    FIND FIRST kbuff WHERE RECID(kbuff) = RECID(kellner)
                        EXCLUSIVE-LOCK.
                    ASSIGN kbuff.kellnername = t-bediener.username.
                    FIND CURRENT kbuff NO-LOCK.
                    RELEASE kbuff.
                    FIND NEXT kellner WHERE 
                        kellner.kellner-nr = INTEGER(bediener.userinit)
                        NO-LOCK NO-ERROR.
                END.
            END.
            RUN update-kellner.
            ASSIGN success-flag = YES.
        END.
    END.
    /* SY JUL 25 2017  used in btn-del setup-userUI*/
    WHEN 4 THEN
    DO:
    DEF VARIABLE existFlag AS LOGICAL NO-UNDO INIT NO.
        FIND FIRST bediener WHERE bediener.nr = t-bediener.nr NO-ERROR.
        IF NOT AVAILABLE bediener THEN RETURN.
        
        FIND FIRST bill-line NO-LOCK NO-ERROR.
        existFlag = AVAILABLE bill-line.
        existFlag = AVAILABLE bill-line.
        IF NOT existFlag THEN
        DO:
            FIND FIRST h-bill-line NO-ERROR.
            existFlag = AVAILABLE h-bill-line.
        END.
        IF NOT existFlag THEN
        DO:
            FIND FIRST reservation NO-LOCK NO-ERROR.
            existFlag = AVAILABLE reservation.
        END.
        FIND CURRENT bediener EXCLUSIVE-LOCK.
        IF existFlag THEN 
        DO:    
            ASSIGN bediener.flag = 1.
            FIND CURRENT bediener NO-LOCK.
        END.
        ELSE 
        DO:    
            FIND FIRST kellner WHERE kellner.kellner-nr = 
                INTEGER(bediener.userinit) NO-LOCK NO-ERROR.
            DO WHILE AVAILABLE kellner:
                FIND FIRST artikel WHERE artikel.artnr = kellner.kumsatz-nr 
                    AND artikel.departement = kellner.departement
                    EXCLUSIVE-LOCK NO-ERROR.
                IF AVAILABLE artikel THEN
                DO:
                    DELETE artikel.
                    RELEASE artikel.
                END.
                FIND FIRST kbuff WHERE kbuff.kcredit-nr = kellner.kcredit-nr
                    AND RECID(kbuff) NE RECID(kellner) NO-LOCK NO-ERROR.
                IF NOT AVAILABLE kbuff THEN
                DO:
                    FIND FIRST artikel WHERE artikel.departement = 0
                        AND artikel.artnr = kellner.kcredit-nr
                        EXCLUSIVE-LOCK NO-ERROR.
                    IF AVAILABLE artikel THEN
                    DO:
                        DELETE artikel.
                        RELEASE artikel.
                    END.
                END.
                FIND FIRST kbuff WHERE RECID(kbuff) = RECID(kellner)
                    EXCLUSIVE-LOCK.
                DELETE kbuff.
                RELEASE kbuff.
                FIND NEXT kellner WHERE kellner.kellner-nr = 
                    INTEGER(bediener.userinit) NO-LOCK NO-ERROR.
            END.
            DELETE bediener.
            success-flag = YES.
        END.
        RELEASE bediener.
    END.
    WHEN 5 THEN /* btn-add in setup-userUI */
    DO:
    DEF VARIABLE ct         AS CHAR    NO-UNDO.
    DEF VARIABLE curr-i     AS INTEGER NO-UNDO.
    DEF VARIABLE st         AS CHAR    NO-UNDO.
    DEF VARIABLE curr-j     AS INTEGER NO-UNDO.
    DEF VARIABLE deptnr     AS INTEGER NO-UNDO.
    DEF VARIABLE mKey       AS LOGICAL NO-UNDO.
    DEF VARIABLE CRartNo    AS INTEGER NO-UNDO.
    DEF VARIABLE TOartNo    AS INTEGER NO-UNDO.
      FOR EACH t-bediener:
        CREATE bediener.
        BUFFER-COPY t-bediener TO bediener.
        FIND CURRENT bediener NO-LOCK.
        ct = t-bediener.mapi-profile.
        DO curr-i = 1 TO NUM-ENTRIES(t-bediener.mapi-profile, ";"):
          ct = TRIM(ENTRY(curr-i, t-bediener.mapi-profile, ";")).
          IF ct NE "" THEN
          CASE SUBSTR(ct,1,2):
              WHEN "$1" THEN .
              WHEN "$2" THEN
              DO:
                  ct = SUBSTR(ct, 3).
                  DO curr-j = 1 TO NUM-ENTRIES(ct, ","):
                      st = TRIM(ENTRY(curr-j, ct, ",")).
                      IF st NE "" THEN
                      DO:
                          ASSIGN
                              deptnr = INTEGER(ENTRY(1, st, "/"))
                              mKey   = INTEGER(ENTRY(2, st, "/")) = 1
                          .
                          
                          FIND FIRST artikel WHERE artikel.departement = 0
                              AND artikel.artart = 1
                              AND SUBSTR(artikel.bezeich,1,4) 
                              = "CR" + STRING(deptnr,"99") NO-LOCK NO-ERROR.
                          IF AVAILABLE artikel THEN CRartNo = artikel.artnr.
                          ELSE RUN create-CRartikel(deptnr, OUTPUT CRartNo).
                          
                          FIND FIRST artikel WHERE artikel.departement = deptnr
                              AND artikel.artart = 1
                              AND artikel.bezeich = "T/O-" + bediener.userinit
                              NO-LOCK NO-ERROR.
                          IF AVAILABLE artikel THEN TOartNo = artikel.artnr.
                          ELSE RUN create-TOartikel(deptnr, bediener.userinit, OUTPUT TOartNo).
                          
                          CREATE kellner.
                          ASSIGN 
                              kellner.kellner-nr   = INTEGER(bediener.userinit)
                              kellner.departement  = deptnr
                              kellner.kellnername  = bediener.username
                              kellner.kumsatz-nr   = TOartNo
                              kellner.kcredit-nr   = CRartNo
                              kellner.masterkey    = mKey
                          .
                          RELEASE kellner.
                      END.
                  END.
              END.
          END CASE.
        END.
      END.
      ASSIGN success-flag = YES.
    END.
END CASE.

PROCEDURE update-kellner:
DEF VARIABLE ct AS CHAR NO-UNDO.
DEF VARIABLE curr-i     AS INTEGER NO-UNDO.
DEF VARIABLE st         AS CHAR    NO-UNDO.
DEF VARIABLE curr-j     AS INTEGER NO-UNDO.
DEF VARIABLE deptnr     AS INTEGER NO-UNDO.
DEF VARIABLE mKey       AS LOGICAL NO-UNDO.
DEF VARIABLE CRartNo    AS INTEGER NO-UNDO.
DEF VARIABLE TOartNo    AS INTEGER NO-UNDO.
DEF BUFFER   kbuff      FOR kellner.
    ct = bediener.mapi-profile.
    DO curr-i = 1 TO NUM-ENTRIES(bediener.mapi-profile, ";"):
      ct = TRIM(ENTRY(curr-i, bediener.mapi-profile, ";")).
      IF ct NE "" THEN
      CASE SUBSTR(ct,1,2):
          WHEN "$1" THEN .
          WHEN "$2" THEN
          DO:
              ct = SUBSTR(ct, 3).
              DO curr-j = 1 TO NUM-ENTRIES(ct, ","):
                  st = TRIM(ENTRY(curr-j, ct, ",")).
                  IF st NE "" THEN
                  DO:
                    ASSIGN
                        deptnr = INTEGER(ENTRY(1, st, "/"))
                        mKey   = INTEGER(ENTRY(2, st, "/")) = 1
                    .
                    CREATE dept-list.
                    ASSIGN dept-list.deptNo = deptnr.
                    FIND FIRST kellner WHERE kellner.departement = deptnr
                        AND kellner.kellner-nr = INTEGER(bediener.userinit)
                        NO-LOCK NO-ERROR.
                    IF AVAILABLE kellner AND kellner.masterkey NE mKey THEN
                    DO:
                        FIND CURRENT kellner EXCLUSIVE-LOCK.
                        ASSIGN kellner.masterkey = mKey.
                        FIND CURRENT kellner NO-LOCK.
                    END.
                    ELSE IF NOT AVAILABLE kellner THEN
                    DO:
                      FIND FIRST artikel WHERE artikel.departement = 0
                          AND artikel.artart = 1
                          AND SUBSTR(artikel.bezeich,1,4) 
                          = "CR" + STRING(deptnr,"99") NO-LOCK NO-ERROR.
                      IF AVAILABLE artikel THEN CRartNo = artikel.artnr.
                      ELSE RUN create-CRartikel(deptnr, OUTPUT CRartNo).

                      FIND FIRST artikel WHERE artikel.departement = deptnr
                          AND artikel.artart = 1
                          AND artikel.bezeich = "T/O-" + bediener.userinit
                          NO-LOCK NO-ERROR.
                      IF AVAILABLE artikel THEN TOartNo = artikel.artnr.
                      ELSE RUN create-TOartikel(deptnr, bediener.userinit, OUTPUT CRartNo).

                      CREATE kellner.
                      ASSIGN 
                          kellner.departement  = deptnr
                          kellner.kellner-nr   = INTEGER(bediener.userinit)
                          kellner.kellnername  = bediener.username
                          kellner.kumsatz-nr   = TOartNo
                          kellner.kcredit-nr   = CRartNo
                          kellner.masterkey    = mKey
                      .
                      RELEASE kellner.
                    END.
                  END.
              END.
              FOR EACH kellner WHERE kellner.kellner-nr 
                  = INTEGER(bediener.userinit) NO-LOCK:
                  FIND FIRST dept-list WHERE dept-list.deptNo
                      = kellner.departement NO-ERROR.
                  IF NOT AVAILABLE dept-list THEN
                  DO:
                      FIND FIRST h-journal WHERE 
                          h-journal.kellner-nr = kellner.kellner-nr AND
                          h-journal.departement = kellner.departement
                          NO-LOCK NO-ERROR.
                      IF NOT AVAILABLE h-journal THEN
                      DO:
                          FIND FIRST kbuff WHERE RECID(kbuff) = RECID(kellner)
                              EXCLUSIVE-LOCK.
                          DELETE kbuff.
                          RELEASE kbuff.
                      END.
                  END.
              END.
          END.
      END CASE.
    END.

END.

/* SY JUL 25 2017 */
PROCEDURE create-CRartikel: 
DEF INPUT  PARAMETER deptnr     AS INTEGER NO-UNDO.
DEF OUTPUT PARAMETER artNo      AS INTEGER NO-UNDO INIT 0.

    artNo = 3000 + deptnr.
    FIND FIRST artikel WHERE artikel.departement = 0
        AND artikel.artnr = artNo NO-LOCK NO-ERROR.
    DO WHILE AVAILABLE artikel:
        artNo = artNo + 1.
        FIND NEXT artikel WHERE artikel.departement = 0
            AND artikel.artnr = artNo NO-LOCK NO-ERROR.
    END.
    FIND FIRST hoteldpt WHERE hoteldpt.num = deptnr NO-LOCK.
    CREATE artikel.
    ASSIGN
        artikel.departement = 0
        artikel.artnr       = artNo
        artikel.bezeich     = "CR" + STRING(hoteldpt.num,"99") + "-" 
                            + CAPS(hoteldpt.depart)
        artikel.artart      = 1
        artikel.activeflag  = YES
    .
END.

/* SY JUL 25 2017 */
PROCEDURE create-TOartikel:
DEF INPUT  PARAMETER deptnr     AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER userinit   AS CHAR    NO-UNDO.
DEF OUTPUT PARAMETER artNo      AS INTEGER NO-UNDO INIT 0.

    artNo = 3000 + deptnr.
    FIND FIRST artikel WHERE artikel.departement = deptnr
        AND artikel.artnr = artNo NO-LOCK NO-ERROR.
    DO WHILE AVAILABLE artikel:
        artNo = artNo + 1.
        FIND NEXT artikel WHERE artikel.departement = deptnr
            AND artikel.artnr = artNo NO-LOCK NO-ERROR.
    END.
    CREATE artikel.
    ASSIGN
        artikel.departement = deptnr
        artikel.artnr       = artNo
        artikel.bezeich     = "T/O" + "-" + userinit
        artikel.artart      = 1
        artikel.activeflag  = YES
    .
END.
