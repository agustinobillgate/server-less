/*USAGE QUEASY KEY = 173 (A/P Voucher Approval)
  number1 = lief-nr (SupplierNo)
  number2 = VoucherNo
  number3 = RECID
  char1 = UID List
  char2 = SupplierName
  
  Remarks:
  UID -> User ID -> UserInit(bediener.userinit)*/

DEFINE TEMP-TABLE       t-queasy        LIKE queasy.

DEFINE INPUT PARAMETER  inpOp           AS INTEGER.
DEFINE INPUT PARAMETER  inpInt          AS INTEGER.
DEFINE INPUT PARAMETER  inpChar         AS CHARACTER.
DEFINE OUTPUT PARAMETER TABLE FOR t-queasy.

DEFINE VARIABLE p-786           AS CHARACTER.
DEFINE VARIABLE i               AS INTEGER.
DEFINE VARIABLE j               AS INTEGER.
DEFINE VARIABLE sumUser         AS INTEGER.
DEFINE VARIABLE sumAppr         AS INTEGER.

CASE inpOp:
    WHEN 1 THEN /*Read A/P Voucher approval per-supplier*/
    DO:
        FIND FIRST htparam WHERE paramnr = 786 NO-LOCK.
        IF AVAILABLE htparam AND htparam.fchar NE "" THEN DO:
            p-786 = htparam.fchar.
            DO i = 1 TO NUM-ENTRIES(p-786,";"):
                IF TRIM(ENTRY(i, p-786, ";")) NE "" THEN sumUser = sumUser + 1.
            END.
            FOR EACH queasy WHERE queasy.KEY = 173 AND queasy.number1 = inpInt NO-LOCK:
                sumAppr = 0.
                i = 0.
                j = 0.
                DO i = 1 TO NUM-ENTRIES(p-786, ";"):
                    DO j = 1 TO NUM-ENTRIES(queasy.char1, ";"):
                        IF (TRIM(ENTRY(i, p-786, ";")) EQ TRIM(ENTRY(j, queasy.char1, ";"))) 
                            AND (TRIM(ENTRY(i, p-786, ";")) NE ""
                            OR TRIM(ENTRY(j, queasy.char1, ";")) NE "") THEN DO:
                            sumAppr = sumAppr + 1.
                            LEAVE.
                        END.
                    END.
                END.
                IF sumAppr < sumUser THEN DO:
                    CREATE t-queasy.
                    BUFFER-COPY queasy TO t-queasy.
                    ASSIGN t-queasy.number3 = RECID(queasy).
                END.
            END.
        END.
    END.
    WHEN 2 THEN /*Read all A/P Voucher approval, which not been fully approved Per-UID*/
    DO:
        DEFINE VARIABLE tTot-Debt       AS DECIMAL NO-UNDO.
        DEFINE VARIABLE uidAvailable    AS LOGICAL INITIAL NO NO-UNDO.
        FIND FIRST htparam WHERE paramnr = 786 NO-LOCK.
        IF AVAILABLE htparam AND htparam.fchar NE "" THEN DO:
            p-786 = htparam.fchar.
            DO i = 1 TO NUM-ENTRIES(p-786, ";"):
                IF ENTRY(i, p-786, ";") = inpChar THEN do:
                    uidAvailable = YES.
                    LEAVE.
                END.
            END.
            IF uidAvailable THEN
                FOR EACH queasy WHERE queasy.KEY = 173 NO-LOCK:
                    uidAvailable = NO.
                    tTot-Debt = 0.
                    DO i = 1 TO NUM-ENTRIES(queasy.char1, ";"):
                        IF ENTRY(i, queasy.char1, ";") = inpChar THEN DO:
                            uidAvailable = YES.
                            LEAVE.
                        END.
                    END.
                    IF NOT uidAvailable THEN DO:
                        CREATE t-queasy.
                        BUFFER-COPY queasy TO t-queasy.
                        ASSIGN 
                            t-queasy.number3 = RECID(queasy).
                            t-queasy.char2 = ";;;;".  /*queasy.char2 = supplierName;docuNr;TotalAmount;duedate*/
                        FOR EACH l-kredit WHERE l-kredit.lief-nr = queasy.number1 
                            AND l-kredit.rechnr = queasy.number2, 
                            FIRST l-lieferant WHERE l-lieferant.lief-nr = queasy.number1:
                            IF l-kredit.opart = 2 THEN DO:
                                DELETE t-queasy.
                                LEAVE.
                            END.
                            ELSE DO:
                                IF AVAILABLE l-lieferant THEN
                                    ASSIGN
                                        ENTRY(1, t-queasy.char2, ";") = l-lieferant.firma.

                                ENTRY(2, t-queasy.char2, ";") = l-kredit.lscheinnr.
                                ENTRY(4, t-queasy.char2, ";") = STRING(l-kredit.rgdatum + l-kredit.ziel, "99/99/99").
                                IF l-kredit.zahlkonto = 0 THEN DO:      
                                    tTot-Debt = tTot-debt + l-kredit.netto.    
                                END.
                                ELSE DO:
                                    tTot-Debt = tTot-debt + l-kredit.saldo. 
                                END.
                            END.
                        END.
                        IF AVAILABLE t-queasy THEN ENTRY(3, t-queasy.char2, ";") = STRING(tTot-Debt, "->>>,>>>,>>>,>>9.99").
                    END.
                END.
        END.
    END.
END CASE.
