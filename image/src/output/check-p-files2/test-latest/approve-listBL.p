DEFINE TEMP-TABLE approve-list
    FIELD datum     AS DATE                          COLUMN-LABEL "Date"
    FIELD zeit      AS CHAR     FORMAT "x(8)"        COLUMN-LABEL "Time"
    FIELD keywrd    AS CHAR     FORMAT "x(8)"        COLUMN-LABEL "Keyword"
    FIELD usrid     AS CHAR     FORMAT "x(2)"        COLUMN-LABEL "ID"
    FIELD billno    AS INTEGER  FORMAT ">>>,>>>,>>9" COLUMN-LABEL "BillNo"
    FIELD gastnr    AS INTEGER  FORMAT ">>>,>>>,>>9" COLUMN-LABEL "GuestNo"
    FIELD resnr     AS INTEGER  FORMAT ">>>,>>9"     COLUMN-LABEL "ResNo"
    FIELD reslinnr  AS INTEGER  FORMAT ">9"          COLUMN-LABEL "RL"
    FIELD gname     AS CHAR     FORMAT "x(36)"       COLUMN-LABEL "Customer Name"
    FIELD remarks   AS CHAR     FORMAT "x(36)"       COLUMN-LABEL "Info"
    FIELD keystr    AS CHAR     FORMAT "x(16)"       COLUMN-LABEL "Keyword"
    FIELD outstand  AS DECIMAL
    FIELD crlimit   AS DECIMAL 
    FIELD max-comp  AS INTEGER
    FIELD com-rm    AS INTEGER
    FIELD pswd      AS CHAR  
    FIELD bl-recid  AS INTEGER
    FIELD trecid    AS INTEGER
    FIELD karteityp AS INT.

DEF OUTPUT PARAMETER TABLE FOR approve-list.

RUN create-list.

PROCEDURE create-list:
DEF VAR srecid AS INTEGER NO-UNDO.
    FOR EACH approve-list:
        DELETE approve-list.
    END.
    FOR EACH queasy WHERE queasy.KEY = 36 AND queasy.logi1 = NO 
        AND queasy.betriebsnr = 0 NO-LOCK BY queasy.date1
        BY queasy.number1:
        CREATE approve-list.
        ASSIGN
            datum   = date1
            keywrd  = char1
            zeit    = STRING(number1, "HH:MM:SS")
            usrid   = ENTRY(1, char2, ";")
            keywrd  = char1
            trecid  = RECID(queasy) NO-ERROR.

        CASE char1:
          WHEN "RSV" THEN
            ASSIGN
            keystr      = "Reservation"
            pswd        = ENTRY(3, char3, ";")
            outstand    = DECIMAL(ENTRY(4, char3, ";"))
            crlimit     = DECIMAL(ENTRY(5, char3, ";"))
            remarks     = ENTRY(2, char3, ";")
            gastnr      = INTEGER(ENTRY(1, char3, ";")) NO-ERROR.
          WHEN "CI" THEN
            ASSIGN
            keystr = "Check In"
            gastnr      = INTEGER(ENTRY(1, char3, ";"))
            resnr       = INTEGER(ENTRY(2, char3, ";"))
            reslinnr    = INTEGER(ENTRY(3, char3, ";"))
            pswd        = ENTRY(5, char3, ";")
            outstand    = DECIMAL(ENTRY(6, char3, ";"))
            crlimit     = DECIMAL(ENTRY(7, char3, ";"))NO-ERROR.
          WHEN "CO" THEN
            ASSIGN
            keystr      = "Check Out"
            gastnr      = INTEGER(ENTRY(1, char3, ";"))
            resnr       = INTEGER(ENTRY(2, char3, ";"))
            reslinnr    = INTEGER(ENTRY(3, char3, ";"))
            pswd        = ENTRY(5, char3, ";")
            outstand    = DECIMAL(ENTRY(6, char3, ";"))
            crlimit     = DECIMAL(ENTRY(7, char3, ";")) NO-ERROR.
          WHEN "COMP" THEN
            ASSIGN
            keystr      = "Compliment"
            gastnr      = INTEGER(ENTRY(1, char3, ";"))
            max-comp    = INTEGER(ENTRY(2, char3, ";"))
            com-rm      = INTEGER(ENTRY(3, char3, ";"))
            pswd        = ENTRY(5, char3, ";")
            outstand    = DECIMAL(ENTRY(6, char3, ";"))
            crlimit     = DECIMAL(ENTRY(7, char3, ";")) NO-ERROR.
          WHEN "AR" THEN
            ASSIGN
            keystr = "Account Receivable"
            pswd        = ENTRY(3, char3, ";")
            outstand    = DECIMAL(ENTRY(4, char3, ";"))
            crlimit     = DECIMAL(ENTRY(5, char3, ";"))
            gastnr      = INTEGER(ENTRY(1, char3, ";")) NO-ERROR.
          WHEN "CL" THEN
            ASSIGN
            keystr      = "Credit Limit"
            pswd        = ENTRY(3, char3, ";")
            outstand    = DECIMAL(ENTRY(4, char3, ";"))
            crlimit     = DECIMAL(ENTRY(5, char3, ";"))
            gastnr      = INTEGER(ENTRY(1, char3, ";")) NO-ERROR.
          WHEN "POS" THEN
          DO:
            ASSIGN
            keystr      = "Misc Item"
            pswd        = ENTRY(3, char3, ";")
            remark      = ENTRY(2, char3, ";") NO-ERROR.
          END.
          WHEN "VOID" THEN
          DO:
            ASSIGN
              keystr      = "VOID Item"
              pswd        = ENTRY(3, char3, ";")
              remark      = ENTRY(2, char3, ";") 
              srecid      = INTEGER(ENTRY(4, char3, ";")) NO-ERROR.
            FIND FIRST bill-line WHERE RECID(bill-line) = srecid NO-LOCK NO-ERROR.
            IF AVAILABLE bill-line THEN
            DO:
              FIND FIRST bill WHERE bill.rechnr = bill-line.rechnr NO-LOCK.
              FIND FIRST guest WHERE guest.gastnr = bill.gastnr NO-LOCK.
              ASSIGN
                approve-list.gastnr = guest.gastnr
                approve-list.gname = guest.NAME + " " + guest.vorname1 + 
                  guest.anredefirma
                approve-list.billno = bill.rechnr
                approve-list.bl-recid = srecid
              . 
            END.
          END.
        END CASE.

        IF queasy.char1 = "POS" THEN
        DO:
          FIND FIRST hoteldpt WHERE hoteldpt.num = 
            INTEGER(ENTRY(4, char3, ";")) NO-LOCK NO-ERROR.
          IF AVAILABLE hoteldpt THEN
          ASSIGN approve-list.gname = hoteldpt.depart.
        END.
        ELSE
        DO:
          FIND FIRST guest WHERE guest.gastnr = approve-list.gastnr USE-INDEX gastnr_index
            NO-LOCK NO-ERROR.
          IF AVAILABLE guest THEN
            ASSIGN
              approve-list.gname = guest.NAME + " " + guest.vorname1 + guest.anredefirma
              approve-list.karteityp = guest.karteityp. 

        END.
    END.
END.
