DEFINE TEMP-TABLE t-h-bill      LIKE h-bill
    FIELD hbill-recid       AS INTEGER.

DEFINE INPUT PARAMETER case-type    AS INTEGER.
DEFINE INPUT PARAMETER rechNo       AS INTEGER.
DEFINE INPUT PARAMETER deptNo       AS INTEGER.
DEFINE OUTPUT PARAMETER TABLE FOR t-h-bill.


CASE case-type :
    WHEN 1 THEN
    DO:
        FIND FIRST h-bill WHERE h-bill.rechnr = rechNo
            AND h-bill.departement = deptNo NO-LOCK NO-ERROR.
        IF AVAILABLE h-bill THEN RUN cr-hbill.
    END.
END CASE.

PROCEDURE cr-hbill :
    CREATE t-h-bill.
    BUFFER-COPY h-bill TO t-h-bill.
    t-h-bill.hbill-recid = RECID(h-bill).
END.
