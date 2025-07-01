DEFINE TEMP-TABLE emulation-list 
    FIELD emul-code LIKE printcod.emu
    .

DEFINE TEMP-TABLE t-printcod LIKE printcod.

DEFINE OUTPUT PARAMETER TABLE FOR emulation-list.

DEFINE VARIABLE emul AS CHAR INITIAL "".

RUN read-printcod1bl.p(2, "","","", OUTPUT TABLE t-printcod).

FOR EACH t-printcod NO-LOCK BY t-printcod.emu:
    IF emul NE t-printcod.emu THEN
    DO:
        CREATE emulation-list.
        ASSIGN
            emulation-list.emul-code = t-printcod.emu.

        emul = t-printcod.emu.
    END.
END.
