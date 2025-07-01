DEFINE TEMP-TABLE t-eg-cost LIKE eg-cost
    FIELD rec-id AS INT.


DEFINE OUTPUT PARAMETER TABLE FOR t-eg-cost.

FOR EACH t-eg-cost:
    DELETE t-eg-cost.
END.

FOR EACH eg-cost:
    CREATE t-eg-cost.
    BUFFER-COPY eg-cost TO t-eg-cost.
END.
