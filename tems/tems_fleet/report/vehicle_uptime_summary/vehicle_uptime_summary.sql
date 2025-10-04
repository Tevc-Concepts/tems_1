SELECT v.name AS "Vehicle:Link/Vehicle:150",
    v.uptime_hours AS "Uptime Hours:Float:120",
    v.downtime_hours AS "Downtime Hours:Float:120",
    CASE
        WHEN COALESCE(v.uptime_hours, 0) + COALESCE(v.downtime_hours, 0) = 0 THEN 0
        ELSE ROUND(
            (
                COALESCE(v.uptime_hours, 0) / (
                    COALESCE(v.uptime_hours, 0) + COALESCE(v.downtime_hours, 0)
                )
            ) * 100,
            2
        )
    END AS "Availability %:Percent:120"
FROM `tabVehicle` v
ORDER BY Availability % DESC;