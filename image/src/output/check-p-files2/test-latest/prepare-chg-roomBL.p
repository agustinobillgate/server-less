
DEFINE TEMP-TABLE braum     LIKE bk-raum
    FIELD rmflag AS LOGICAL.
DEFINE TEMP-TABLE bset   LIKE bk-rset.
DEFINE TEMP-TABLE bsetup LIKE bk-setup.
DEFINE TEMP-TABLE bfunc  LIKE bk-func.
DEFINE TEMP-TABLE breser LIKE bk-reser.

DEF OUTPUT PARAMETER TABLE FOR braum.
DEF OUTPUT PARAMETER TABLE FOR bset.
DEF OUTPUT PARAMETER TABLE FOR bsetup.
DEF OUTPUT PARAMETER TABLE FOR bfunc.
DEF OUTPUT PARAMETER TABLE FOR breser.

DEFINE VARIABLE bill-date AS DATE NO-UNDO.

FIND FIRST htparam WHERE htparam.paramnr EQ 110 NO-LOCK.
bill-date = htparam.fdate.

FOR EACH bk-raum NO-LOCK:
    CREATE braum.
    BUFFER-COPY bk-raum TO braum.
END.

FOR EACH bk-rset NO-LOCK:
    CREATE bset.
    BUFFER-COPY bk-rset TO bset.
END.

FOR EACH bk-setup NO-LOCK:
    CREATE bsetup.
    BUFFER-COPY bk-setup TO bsetup.
END.

FOR EACH bk-func NO-LOCK:
    CREATE bfunc.
    BUFFER-COPY bk-func TO bfunc.
END.
/* FDL Comment - make not responding | Ticket A93F56
FOR EACH bk-reser NO-LOCK:
    CREATE breser.
    BUFFER-COPY bk-reser TO breser.
END.
*/
/*FDL July 22, 2024 - Ticket A93F56*/
FOR EACH bk-reser WHERE bk-reser.datum GE bill-date NO-LOCK:
    CREATE breser.
    BUFFER-COPY bk-reser TO breser.
END.


 /*MT
FIND FIRST bk-reser WHERE bk-reser.veran-nr = resnr 
  AND bk-reser.veran-resnr = reslinnr NO-LOCK NO-ERROR. 
curr-date = bk-reser.datum.
IF AVAILABLE bk-reser THEN
DO:
    avail-bk-reser = YES.
    FIND FIRST bk-raum WHERE bk-raum.raum = bk-reser.raum NO-LOCK.
    b = (((bk-raum.vorbereit + 0.1) * 2) + 1) / 60.
    begin = bk-reser.von-i - b.
    k = (((bk-raum.vorbereit + 0.1) * 2 ) + 1) / 60.
    ending = bk-reser.bis-i + k.
    FOR EACH braum:
        IF bk-reser.raum NE braum.raum THEN
        DO:
            i = i + 1.
        END.
        ELSE LEAVE.
    END.
   
    DISP b1 WITH FRAME frame1.
    b1:SELECT-ROW(i).
   
    
    FIND FIRST bk-rset WHERE bk-rset.raum = bbraum.raum NO-LOCK NO-ERROR.
    FIND FIRST bk-setup WHERE bk-setup.setup-id = bk-rset.setup-id NO-LOCK NO-ERROR.
    IF AVAILABLE bk-rset THEN
    DO:
        avail-bk-rset = YES.
        FOR EACH bset NO-LOCK, 
            FIRST broom WHERE broom.raum = bk-reser.raum 
            AND bset.raum = bk-reser.raum NO-LOCK, 
            FIRST bsetup WHERE bsetup.setup-id = bset.setup-id NO-LOCK 
            BY bset.raum:
            CREATE q2-list.
            ASSIGN
            q2-list.bezeich  = bsetup.bezeich
            q2-list.personen = bset.personen.
        END.

        FIND FIRST bk-func WHERE bk-func.veran-nr = resnr 
            AND bk-func.raeume[1] = bbraum.raum NO-LOCK NO-ERROR.
        IF AVAILABLE bk-func THEN
        DO: 
            IF bk-func.tischform[1] NE "" THEN
            DO:
                FOR EACH bset NO-LOCK, 
                  FIRST broom WHERE broom.raum = bk-reser.raum 
                    AND bset.raum = bk-reser.raum NO-LOCK, 
                  FIRST bsetup WHERE bsetup.setup-id = bset.setup-id NO-LOCK :
                    IF bsetup.bezeich NE bk-func.tischform[1] THEN
                    DO:
                        d = d + 1.
                    END.
                    ELSE LEAVE.

                    action = 1.
                    /*MT
                    DISP b2 WITH FRAME frame1.
                    ENABLE btn-exit WITH FRAME frame1.
                    */
                END.
            END.
            ELSE 
            DO:
                action = 2.
                /*MT
                APPLY "entry" TO b2.
                b2:DESELECT-FOCUSED-ROW().
                DISABLE btn-exit WITH FRAME frame1.
                */
            END.
        END.
        ELSE 
        DO:
            action = 3.
             /*MT
             APPLY "entry" TO b2.
             */
        END.
    END.
    ELSE
    DO:
        avail-bk-rset = NO.
         FOR EACH bset NO-LOCK ,
             FIRST broom WHERE broom.raum = bbraum.raum 
             AND bset.raum = bbraum.raum  NO-LOCK,
             FIRST bsetup WHERE bsetup.setup-id = bset.setup-id NO-LOCK 
             BY bset.raum:
             CREATE q2-list.
             ASSIGN
             q2-list.bezeich  = bsetup.bezeich
             q2-list.personen = bset.personen.
         END.
         /*MT
         OPEN QUERY q2 FOR EACH bset NO-LOCK , 
                    FIRST broom WHERE broom.raum = braum.raum AND bset.raum = braum.raum  NO-LOCK, 
                    FIRST bsetup WHERE bsetup.setup-id = bset.setup-id NO-LOCK 
                    BY bset.raum.
         HIDE MESSAGE NO-PAUSE.
         MESSAGE translateExtended ("Please Assign Table Setup For Room ",lvCAREA,"") + braum.bezeich 
         + translateExtended (" First",lvCAREA,"")
         VIEW-AS ALERT-BOX INFORMATION. 
         DISABLE btn-exit WITH FRAME frame1.
         */
    END. 
END.
ELSE
DO:
    avail-bk-reser = NO.
    RETURN.
END.*/
