DEFINE INPUT PARAMETER resnr AS INTEGER.
DEFINE OUTPUT PARAMETER split-bill AS LOGICAL INIT NO.

FOR EACH bill WHERE bill.resnr = resnr NO-LOCK.
    IF bill.reslinnr GT 1 THEN split-bill = YES.
    ELSE split-bill = NO.
END.
