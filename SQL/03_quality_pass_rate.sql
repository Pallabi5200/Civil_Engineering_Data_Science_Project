SELECT 
    p.project_name, 
    COUNT(*) AS total_tests,
    SUM(CASE WHEN ql.cube_test_result_mpa >= 40.0 THEN 1 ELSE 0 END) AS passed_tests,
    SUM(CASE WHEN ql.cube_test_result_mpa < 40.0 THEN 1 ELSE 0 END) AS failed_tests,
    ROUND(SUM(CASE WHEN ql.cube_test_result_mpa >= 40.0 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS pass_rate_pct,
    ROUND(AVG(ql.cube_test_result_mpa), 2) AS avg_strength_mpa
FROM Projects p 
JOIN Field_Quality_Logs AS ql ON p.project_id = ql.project_id
GROUP BY p.project_name;
