
-- Retrieve the hierarchy of a cost centre as it was on a specified date.
-- Replace the example cost centre and date with the desired values.

WITH RECURSIVE hierarchy AS (
    -- Start from the cost centre we want to look up.
    -- Only use a relationship that was already valid on the selected date.
    SELECT
        "Kustannuspaikka",
        "Emokustannuspaikka",
        "Voimassa alkaen",
        0 AS level
    FROM "Kustannuspaikkahierarkia"
    WHERE "Kustannuspaikka" = '10000'
      AND "Voimassa alkaen" <= '2021-07-01'

    UNION ALL

    -- Follow the parent relationship upwards, one level at a time.
    -- Each recursive step finds the parent of the previous cost centre.
    SELECT
        parent."Kustannuspaikka",
        parent."Emokustannuspaikka",
        parent."Voimassa alkaen",
        child.level + 1
    FROM "Kustannuspaikkahierarkia" AS parent
    JOIN hierarchy AS child
      ON parent."Kustannuspaikka" = child."Emokustannuspaikka"
    WHERE parent."Voimassa alkaen" <= '2021-07-01'

    -- Recursion stops when no matching parent relationship is found.
    -- Note: this query does not explicitly detect cycles or resolve
    -- conflicting parent relationships with the same effective date.
)
SELECT
    "Kustannuspaikka",
    "Emokustannuspaikka",
    level
FROM hierarchy
ORDER BY level;
