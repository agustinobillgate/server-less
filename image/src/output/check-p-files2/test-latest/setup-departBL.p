DEFINE TEMP-TABLE dept-list   LIKE hoteldpt
    FIELD dpttype AS CHAR.
DEFINE TEMP-TABLE depart-list LIKE dept-list.

DEFINE INPUT  PARAMETER icase AS INTEGER NO-UNDO.
DEFINE INPUT  PARAMETER TABLE FOR depart-list.
DEFINE OUTPUT PARAMETER TABLE FOR dept-list.
DEFINE OUTPUT PARAMETER success-flag AS LOGICAL NO-UNDO INIT YES.

DEFINE VARIABLE counter  AS INTEGER NO-UNDO.
DEFINE VARIABLE del-flag AS LOGICAL NO-UNDO INIT NO.
DEFINE BUFFER bdept FOR hoteldpt.

DEFINE VARIABLE curr-num AS INTEGER NO-UNDO.

IF icase = 1 THEN DO: /*for add and chg*/

    FIND FIRST depart-list NO-ERROR.
    IF AVAILABLE depart-list THEN 
    DO:
        FIND FIRST hoteldpt WHERE hoteldpt.num = depart-list.num 
            NO-LOCK NO-ERROR.
        IF NOT AVAILABLE hoteldpt THEN DO:
            CREATE hoteldpt.
            BUFFER-COPY depart-list TO hoteldpt.
        END.
        ELSE IF AVAILABLE hoteldpt THEN 
        DO:
            FIND CURRENT hoteldpt EXCLUSIVE-LOCK.
            ASSIGN hoteldpt.depart    = depart-list.depart
                   hoteldpt.departtyp = depart-list.departtyp.
            RUN adjust-hoteldpt-num.
            FIND CURRENT hoteldpt NO-LOCK.
            RELEASE hoteldpt.
        END.
    END.

    /*banquet*/
    FIND FIRST hoteldpt WHERE hoteldpt.departtyp = 4 NO-LOCK NO-ERROR.
    IF AVAILABLE hoteldpt THEN DO:
        FIND FIRST htparam WHERE htparam.paramnr = 900 NO-LOCK NO-ERROR.
        IF AVAILABLE htparam THEN DO:
            FIND CURRENT htparam EXCLUSIVE-LOCK.
            ASSIGN htparam.finteger = hoteldpt.num.
            FIND CURRENT htparam NO-LOCK.
            RELEASE htparam.
        END.
    END.
    ELSE DO:
        FIND FIRST htparam WHERE htparam.paramnr = 900 NO-LOCK NO-ERROR.
        IF AVAILABLE htparam THEN DO:
            FIND CURRENT htparam EXCLUSIVE-LOCK.
            ASSIGN htparam.finteger = 0.
            FIND CURRENT htparam NO-LOCK.
            RELEASE htparam.
        END.
    END.

    /*laundry*/
    FIND FIRST hoteldpt WHERE hoteldpt.departtyp = 3 NO-LOCK NO-ERROR.
    IF AVAILABLE hoteldpt THEN DO:
        FIND FIRST htparam WHERE htparam.paramnr = 1081 NO-LOCK NO-ERROR.
        IF AVAILABLE htparam THEN DO:
            FIND CURRENT htparam EXCLUSIVE-LOCK.
            ASSIGN htparam.finteger = hoteldpt.num.
            FIND CURRENT htparam NO-LOCK.
            RELEASE htparam.
        END.
    END.
    ELSE DO:
        FIND FIRST htparam WHERE htparam.paramnr = 1081 NO-LOCK NO-ERROR.
        IF AVAILABLE htparam THEN DO:
            FIND CURRENT htparam EXCLUSIVE-LOCK.
            ASSIGN htparam.finteger = 0.
            FIND CURRENT htparam NO-LOCK.
            RELEASE htparam.
        END.
    END.

    /*minibar*/
    FIND FIRST hoteldpt WHERE hoteldpt.departtyp = 2 NO-LOCK NO-ERROR.
    IF AVAILABLE hoteldpt THEN 
    DO:
        FIND FIRST htparam WHERE htparam.paramnr = 570 NO-LOCK NO-ERROR.
        IF AVAILABLE htparam THEN DO:
            FIND CURRENT htparam EXCLUSIVE-LOCK.
            ASSIGN htparam.finteger = hoteldpt.num.
            FIND CURRENT htparam NO-LOCK.
            RELEASE htparam.
        END.
        FIND FIRST htparam WHERE htparam.paramnr = 949 NO-LOCK NO-ERROR.
        IF AVAILABLE htparam THEN DO:
            FIND CURRENT htparam EXCLUSIVE-LOCK.
            ASSIGN htparam.finteger = hoteldpt.num.
            FIND CURRENT htparam NO-LOCK.
            RELEASE htparam.
        END.
    END.
    ELSE 
    DO:
        FIND FIRST htparam WHERE htparam.paramnr = 570 NO-LOCK NO-ERROR.
        IF AVAILABLE htparam THEN DO:
            FIND CURRENT htparam EXCLUSIVE-LOCK.
            ASSIGN htparam.finteger = 0.
            FIND CURRENT htparam NO-LOCK.
            RELEASE htparam.
        END.
        FIND FIRST htparam WHERE htparam.paramnr = 949 NO-LOCK NO-ERROR.
        IF AVAILABLE htparam THEN DO:
            FIND CURRENT htparam EXCLUSIVE-LOCK.
            ASSIGN htparam.finteger = 0.
            FIND CURRENT htparam NO-LOCK.
            RELEASE htparam.
        END.
    END.

    /*Drugstore*/
    FIND FIRST hoteldpt WHERE hoteldpt.departtyp = 5 NO-LOCK NO-ERROR.
    IF AVAILABLE hoteldpt THEN DO:
        FIND FIRST htparam WHERE htparam.paramnr = 1082 NO-LOCK NO-ERROR.
        IF AVAILABLE htparam THEN DO:
            FIND CURRENT htparam EXCLUSIVE-LOCK.
            ASSIGN htparam.finteger = hoteldpt.num.
            FIND CURRENT htparam NO-LOCK.
            RELEASE htparam.
        END.
    END.
    ELSE DO:
        FIND FIRST htparam WHERE htparam.paramnr = 1082 NO-LOCK NO-ERROR.
        IF AVAILABLE htparam THEN DO:
            FIND CURRENT htparam EXCLUSIVE-LOCK.
            ASSIGN htparam.finteger = 0.
            FIND CURRENT htparam NO-LOCK.
            RELEASE htparam.
        END.
    END.

    FOR EACH hoteldpt :
        CREATE dept-list.
        BUFFER-COPY hoteldpt TO dept-list.
    END.
END.
ELSE IF icase = 2 THEN /* delete */
DO: 
    FIND FIRST depart-list NO-ERROR.
    IF AVAILABLE depart-list THEN 
    DO:
        FIND FIRST umsatz WHERE umsatz.departement = depart-list.num
            NO-LOCK NO-ERROR.
        IF AVAILABLE umsatz THEN
        DO:
            success-flag = NO.
            RETURN.
        END.
        FIND FIRST hoteldpt WHERE hoteldpt.num = depart-list.num NO-LOCK NO-ERROR.
        IF AVAILABLE hoteldpt THEN DO:
            FIND CURRENT hoteldpt EXCLUSIVE-LOCK.
            DELETE hoteldpt.
            RELEASE hoteldpt.
        END.
    END.
    
    /*banquet*/
    FIND FIRST hoteldpt WHERE hoteldpt.departtyp = 4 NO-LOCK NO-ERROR.
    IF AVAILABLE hoteldpt THEN DO:
        FIND FIRST htparam WHERE htparam.paramnr = 900 NO-LOCK NO-ERROR.
        IF AVAILABLE htparam THEN DO:
            FIND CURRENT htparam EXCLUSIVE-LOCK.
            ASSIGN htparam.finteger = hoteldpt.num.
            FIND CURRENT htparam NO-LOCK.
            RELEASE htparam.
        END.
    END.
    ELSE DO:
        FIND FIRST htparam WHERE htparam.paramnr = 900 NO-LOCK NO-ERROR.
        IF AVAILABLE htparam THEN DO:
            FIND CURRENT htparam EXCLUSIVE-LOCK.
            ASSIGN htparam.finteger = 0.
            FIND CURRENT htparam NO-LOCK.
            RELEASE htparam.
        END.
    END.

    /*laundry*/
    FIND FIRST hoteldpt WHERE hoteldpt.departtyp = 3 NO-LOCK NO-ERROR.
    IF AVAILABLE hoteldpt THEN DO:
        FIND FIRST htparam WHERE htparam.paramnr = 1081 NO-LOCK NO-ERROR.
        IF AVAILABLE htparam THEN DO:
            FIND CURRENT htparam EXCLUSIVE-LOCK.
            ASSIGN htparam.finteger = hoteldpt.num.
            FIND CURRENT htparam NO-LOCK.
            RELEASE htparam.
        END.
    END.
    ELSE DO:
        FIND FIRST htparam WHERE htparam.paramnr = 1081 NO-LOCK NO-ERROR.
        IF AVAILABLE htparam THEN DO:
            FIND CURRENT htparam EXCLUSIVE-LOCK.
            ASSIGN htparam.finteger = 0.
            FIND CURRENT htparam NO-LOCK.
            RELEASE htparam.
        END.
    END.

    /*minibar*/
    FIND FIRST hoteldpt WHERE hoteldpt.departtyp = 2 NO-LOCK NO-ERROR.
    IF AVAILABLE hoteldpt THEN 
    DO:
        FIND FIRST htparam WHERE htparam.paramnr = 570 NO-LOCK NO-ERROR.
        IF AVAILABLE htparam THEN DO:
            FIND CURRENT htparam EXCLUSIVE-LOCK.
            ASSIGN htparam.finteger = hoteldpt.num.
            FIND CURRENT htparam NO-LOCK.
            RELEASE htparam.
        END.
        FIND FIRST htparam WHERE htparam.paramnr = 949 NO-LOCK NO-ERROR.
        IF AVAILABLE htparam THEN DO:
            FIND CURRENT htparam EXCLUSIVE-LOCK.
            ASSIGN htparam.finteger = hoteldpt.num.
            FIND CURRENT htparam NO-LOCK.
            RELEASE htparam.
        END.
    END.
    ELSE 
    DO:
        FIND FIRST htparam WHERE htparam.paramnr = 570 NO-LOCK NO-ERROR.
        IF AVAILABLE htparam THEN DO:
            FIND CURRENT htparam EXCLUSIVE-LOCK.
            ASSIGN htparam.finteger = 0.
            FIND CURRENT htparam NO-LOCK.
            RELEASE htparam.
        END.
        FIND FIRST htparam WHERE htparam.paramnr = 949 NO-LOCK NO-ERROR.
        IF AVAILABLE htparam THEN DO:
            FIND CURRENT htparam EXCLUSIVE-LOCK.
            ASSIGN htparam.finteger = 0.
            FIND CURRENT htparam NO-LOCK.
            RELEASE htparam.
        END.
    END.

    /*Drugstore*/
    FIND FIRST hoteldpt WHERE hoteldpt.departtyp = 5 NO-LOCK NO-ERROR.
    IF AVAILABLE hoteldpt THEN DO:
        FIND FIRST htparam WHERE htparam.paramnr = 1082 NO-LOCK NO-ERROR.
        IF AVAILABLE htparam THEN DO:
            FIND CURRENT htparam EXCLUSIVE-LOCK.
            ASSIGN htparam.finteger = hoteldpt.num.
            FIND CURRENT htparam NO-LOCK.
            RELEASE htparam.
        END.
    END.
    ELSE DO:
        FIND FIRST htparam WHERE htparam.paramnr = 1082 NO-LOCK NO-ERROR.
        IF AVAILABLE htparam THEN DO:
            FIND CURRENT htparam EXCLUSIVE-LOCK.
            ASSIGN htparam.finteger = 0.
            FIND CURRENT htparam NO-LOCK.
            RELEASE htparam.
        END.
    END.

    FOR EACH hoteldpt :
        CREATE dept-list.
        BUFFER-COPY hoteldpt TO dept-list.
    END.
END.

PROCEDURE adjust-hoteldpt-num:
DEF VARIABLE dept-code AS INTEGER NO-UNDO INIT 1.
DEF BUFFER htlbuff FOR hoteldpt.
    CASE hoteldpt.departtyp:
        WHEN 2 THEN hoteldpt.num = 10. /* Minibar   */
        WHEN 3 THEN hoteldpt.num = 20. /* Laundry   */
        WHEN 4 THEN hoteldpt.num = 11. /* Banquet   */
        WHEN 5 THEN hoteldpt.num = 15. /* Drugstore */
        WHEN 7 THEN hoteldpt.num = 14. /* Spa       */
        WHEN 8 THEN hoteldpt.num = 16. /* Boutique  */
        OTHERWISE IF hoteldpt.num GE 10 THEN
        REPEAT:
            FIND FIRST htlbuff WHERE htlbuff.num = dept-code
                NO-LOCK NO-ERROR.
            IF NOT AVAILABLE htlbuff THEN
            DO:
                hoteldpt.num = dept-code.
                LEAVE.
            END.
            dept-code = dept-code + 1.
        END.
    END CASE.

END.

