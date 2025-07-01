DEFINE TEMP-TABLE emulation-list 
    FIELD emul-code AS CHARACTER
    FIELD rec-id AS INTEGER.

DEFINE TEMP-TABLE t-printcod LIKE printcod.

DEFINE OUTPUT PARAMETER TABLE FOR emulation-list.

DEFINE VARIABLE emul AS CHAR INITIAL "".

															 

FOR EACH printcod NO-LOCK BY printcod.emu:
    IF emul NE printcod.emu THEN
    DO:
        CREATE emulation-list.
        ASSIGN
            emulation-list.emul-code = printcod.emu
            emulation-list.rec-id = RECID(printcod)

        emul = printcod.emu.
    END.
END.
