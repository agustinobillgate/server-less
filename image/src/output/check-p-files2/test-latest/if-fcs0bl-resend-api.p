/***************************************************************************************
**   Business Logic for FCS0 API Interface - Resend Function
**   Descript       : Business Logic program for resending failed interface data
**   Created        : BLY
**   Notes          : Resend interface data with $FCS0$ flag only
***************************************************************************************/

/* */
DEFINE INPUT PARAMETER p-resend         AS INTEGER          NO-UNDO.
DEFINE INPUT PARAMETER p-irecid         AS INTEGER          NO-UNDO.
DEFINE OUTPUT PARAMETER p-status        AS CHARACTER        NO-UNDO.


/* Local 
DEFINE VARIABLE p-irecid    AS INTEGER      NO-UNDO INIT 5036849.
DEFINE VARIABLE p-resend    AS INTEGER      NO-UNDO INIT 1.
DEFINE VARIABLE p-status    AS CHARACTER    NO-UNDO.
*/


DEFINE VARIABLE v-count                 AS INTEGER          NO-UNDO.

/*single resend*/
IF p-resend EQ 1 THEN
DO :
    FIND FIRST INTERFACE WHERE RECID(INTERFACE) EQ p-irecid
        EXCLUSIVE-LOCK NO-ERROR.

    IF AVAILABLE INTERFACE THEN
    DO:
        IF INTERFACE.KEY EQ 38 /*AND*/ OR
            INTERFACE.nebenstelle MATCHES "*$FCS0$*" AND
            (INTERFACE.parameters NE "modify" OR
             (INTERFACE.parameters EQ "modify" AND INTERFACE.zinr NE "")) THEN
        DO:
            ASSIGN
                INTERFACE.nebenstelle = ""
                INTERFACE.intdate = TODAY
                v-count = 1
                p-status = "SUCCESS: Data berhasil di resend"
                .
        END.
        ELSE 
            p-status = "ERROR: Data tidak ditemukan".
    END.
END.
ELSE IF p-resend EQ 2 THEN
DO:
    FOR EACH INTERFACE WHERE
        INTERFACE.KEY EQ 38 AND
        INTERFACE.nebenstelle MATCHES "*$FCS0$*" AND
        (INTERFACE.parameters NE "modify" OR
         INTERFACE.parameters EQ "modify" AND INTERFACE.zinr NE "")
        EXCLUSIVE-LOCK:

        ASSIGN
            INTERFACE.nebenstelle = ""
            INTERFACE.intdate = TODAY
            v-count = v-count + 1
            .
    END.
    IF v-count > 0 THEN
        p-status = "SUCCESS: " + STRING(v-count) + " data berhasil di resend".
    ELSE
        p-status = "INFO: Tidak ada data yang perlu di resend".

    RETURN STRING(v-count).
END.


/* MESSAGE "p-status: " p-status          */
/*     VIEW-AS ALERT-BOX INFO BUTTONS OK. */
