```sql
-- Inner join eficiente (Spark optimiza automáticamente)
SELECT 
    s.customer_id,
    s.amount,
    c.customer_name,
    c.segment
FROM sales s
INNER JOIN customers c ON s.customer_id = c.customer_id
WHERE s.sale_date >= '2024-01-01';

-- Broadcast join para tablas pequeñas (<200MB)
SELECT /*+ BROADCAST(categories) */
    p.product_name,
    p.price,
    c.category_name
FROM products p
INNER JOIN categories c ON p.category_id = c.category_id;
```

### **Left Join con Optimización**
```sql
-- Left join para análisis de completitud
SELECT 
    c.customer_id,
    c.customer_name,
    COALESCE(SUM(s.amount), 0) as total_spent,
    COUNT(s.sale_id) as total_orders
FROM customers c
LEFT JOIN sales s ON c.customer_id = s.customer_id
    AND s.sale_date >= '2024-01-01'
GROUP BY c.customer_id, c.customer_name
ORDER BY total_spent DESC;
```

### **Join con Múltiples Tablas**
```sql
-- Join complejo optimizado
SELECT 
    c.customer_name,
    p.product_name,
    s.amount,
    s.sale_date,
    cat.category_name
FROM sales s
INNER JOIN customers c ON s.customer_id = c.customer_id
INNER JOIN products p ON s.product_id = p.product_id
INNER JOIN categories cat ON p.category_id = cat.category_id
WHERE s.sale_date BETWEEN '2024-01-01' AND '2024-12-31'
ORDER BY s.sale_date DESC
LIMIT 10000;
```

---

## 📅 **FUNCIONES DE TIEMPO PARA BIG DATA**

### **Extracción de Componentes de Fecha**
```sql
-- Componentes básicos de fecha
SELECT 
    sale_date,
    YEAR(sale_date) as year,
    MONTH(sale_date) as month,
    DAY(sale_date) as day,
    DAYOFWEEK(sale_date) as day_of_week,
    QUARTER(sale_date) as quarter,
    WEEKOFYEAR(sale_date) as week_number
FROM sales
LIMIT 100;

-- Formateo de fechas
SELECT 
    sale_date,
    DATE_FORMAT(sale_date, 'yyyy-MM') as year_month,
    DATE_FORMAT(sale_date, 'yyyy-MM-dd') as date_only,
    DATE_FORMAT(sale_date, 'EEEE') as day_name
FROM sales;
```

### **Operaciones Temporales**
```sql
-- Rangos de fechas
SELECT *
FROM sales 
WHERE sale_date >= DATE_SUB(CURRENT_DATE(), 30)  -- Últimos 30 días
  AND sale_date < CURRENT_DATE();

-- Truncado de fechas para agregaciones
SELECT 
    DATE_TRUNC('month', sale_date) as month,
    COUNT(*) as sales_count,
    SUM(amount) as monthly_revenue
FROM sales 
WHERE YEAR(sale_date) = 2024
GROUP BY DATE_TRUNC('month', sale_date)
ORDER BY month;

-- Diferencias de tiempo
SELECT 
    customer_id,
    sale_date,
    LAG(sale_date) OVER (PARTITION BY customer_id ORDER BY sale_date) as prev_sale,
    DATEDIFF(sale_date, LAG(sale_date) OVER (PARTITION BY customer_id ORDER BY sale_date)) as days_between_purchases
FROM sales
ORDER BY customer_id, sale_date;
```

---

## 🪟 **WINDOW FUNCTIONS PARA ANÁLISIS AVANZADO**

### **Ranking y Numeración**
```sql
-- Ranking de ventas por región
SELECT 
    region,
    customer_id,
    amount,
    ROW_NUMBER() OVER (PARTITION BY region ORDER BY amount DESC) as rank_in_region,
    RANK() OVER (PARTITION BY region ORDER BY amount DESC) as rank_with_ties,
    DENSE_RANK() OVER (PARTITION BY region ORDER BY amount DESC) as dense_rank
FROM sales
WHERE sale_date >= '2024-01-01';

-- Top N por grupo
SELECT *
FROM (
    SELECT 
        region,
        customer_id,
        amount,
        ROW_NUMBER() OVER (PARTITION BY region ORDER BY amount DESC) as rn
    FROM sales
    WHERE sale_date >= '2024-01-01'
) ranked
WHERE rn <= 5;  -- Top 5 por región
```

### **Funciones de Ventana Móvil**
```sql
-- Moving averages y sumas acumulativas
SELECT 
    sale_date,
    amount,
    AVG(amount) OVER (
        ORDER BY sale_date 
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) as moving_avg_7_days,
    SUM(amount) OVER (
        ORDER BY sale_date 
        ROWS UNBOUNDED PRECEDING
    ) as cumulative_sum
FROM daily_sales
ORDER BY sale_date;

-- Lead y Lag para comparaciones
SELECT 
    customer_id,
    sale_date,
    amount,
    LAG(amount) OVER (PARTITION BY customer_id ORDER BY sale_date) as prev_amount,
    LEAD(amount) OVER (PARTITION BY customer_id ORDER BY sale_date) as next_amount,
    amount - LAG(amount) OVER (PARTITION BY customer_id ORDER BY sale_date) as change_from_prev
FROM sales
ORDER BY customer_id, sale_date;
```

### **Percentiles y Distribuciones**
```sql
-- Percentiles para identificar outliers
SELECT 
    region,
    PERCENTILE_APPROX(amount, 0.25) as q1,
    PERCENTILE_APPROX(amount, 0.5) as median,
    PERCENTILE_APPROX(amount, 0.75) as q3,
    PERCENTILE_APPROX(amount, 0.95) as p95
FROM sales 
GROUP BY region;

-- Identificar outliers
WITH quartiles AS (
    SELECT 
        region,
        PERCENTILE_APPROX(amount, 0.25) as q1,
        PERCENTILE_APPROX(amount, 0.75) as q3
    FROM sales 
    GROUP BY region
)
SELECT s.*
FROM sales s
JOIN quartiles q ON s.region = q.region
WHERE s.amount > q.q3 + 1.5 * (q.q3 - q.q1)  -- Outliers superiores
   OR s.amount < q.q1 - 1.5 * (q.q3 - q.q1);  -- Outliers inferiores
```

---

## 🔍 **ANÁLISIS AVANZADO CON SQL**

### **Análisis de Cohortes**
```sql
-- Análisis de retención de clientes
WITH first_purchase AS (
    SELECT 
        customer_id,
        MIN(sale_date) as first_purchase_date,
        DATE_TRUNC('month', MIN(sale_date)) as cohort_month
    FROM sales
    GROUP BY customer_id
),
monthly_activity AS (
    SELECT 
        s.customer_id,
        DATE_TRUNC('month', s.sale_date) as activity_month
    FROM sales s
    GROUP BY s.customer_id, DATE_TRUNC('month', s.sale_date)
)
SELECT 
    fp.cohort_month,
    ma.activity_month,
    DATEDIFF(ma.activity_month, fp.cohort_month) / 30 as period_number,
    COUNT(DISTINCT fp.customer_id) as customers
FROM first_purchase fp
JOIN monthly_activity ma ON fp.customer_id = ma.customer_id
GROUP BY fp.cohort_month, ma.activity_month
ORDER BY fp.cohort_month, ma.activity_month;
```

### **RFM Analysis (Recency, Frequency, Monetary)**
```sql
-- Segmentación RFM
WITH customer_metrics AS (
    SELECT 
        customer_id,
        DATEDIFF(CURRENT_DATE(), MAX(sale_date)) as recency,
        COUNT(*) as frequency,
        SUM(amount) as monetary
    FROM sales
    WHERE sale_date >= DATE_SUB(CURRENT_DATE(), 365)  -- Último año
    GROUP BY customer_id
),
rfm_scores AS (
    SELECT 
        customer_id,
        recency,
        frequency,
        monetary,
        NTILE(5) OVER (ORDER BY recency DESC) as r_score,
        NTILE(5) OVER (ORDER BY frequency) as f_score,
        NTILE(5) OVER (ORDER BY monetary) as m_score
    FROM customer_metrics
)
SELECT 
    customer_id,
    CONCAT(r_score, f_score, m_score) as rfm_segment,
    CASE 
        WHEN r_score >= 4 AND f_score >= 4 AND m_score >= 4 THEN 'Champions'
        WHEN r_score >= 3 AND f_score >= 3 AND m_score >= 3 THEN 'Loyal Customers'
        WHEN r_score >= 3 AND f_score <= 2 THEN 'Potential Loyalists'
        WHEN r_score <= 2 AND f_score >= 3 THEN 'At Risk'
        WHEN r_score <= 2 AND f_score <= 2 THEN 'Lost Customers'
        ELSE 'Others'
    END as customer_segment
FROM rfm_scores;
```

### **Análisis de Tendencias**
```sql
-- Crecimiento mes a mes
WITH monthly_sales AS (
    SELECT 
        DATE_TRUNC('month', sale_date) as month,
        SUM(amount) as monthly_revenue
    FROM sales
    GROUP BY DATE_TRUNC('month', sale_date)
)
SELECT 
    month,
    monthly_revenue,
    LAG(monthly_revenue) OVER (ORDER BY month) as prev_month_revenue,
    (monthly_revenue - LAG(monthly_revenue) OVER (ORDER BY month)) / 
    LAG(monthly_revenue) OVER (ORDER BY month) * 100 as growth_rate_percent
FROM monthly_sales
ORDER BY month;
```

---

## 🛠️ **OPTIMIZACIÓN PARA BIG DATA**

### **Particionado y Filtros Eficientes**
```sql
-- Usar filtros de partición cuando sea posible
SELECT *
FROM sales_partitioned
WHERE year = 2024 AND month = 12  -- Filtra por particiones
  AND region = 'North';

-- Evitar funciones en WHERE (impiden uso de índices)
-- ❌ Malo
SELECT * FROM sales WHERE YEAR(sale_date) = 2024;

-- ✅ Bueno  
SELECT * FROM sales WHERE sale_date >= '2024-01-01' AND sale_date < '2025-01-01';
```

### **Hints para Optimización**
```sql
-- Broadcast join para tablas pequeñas
SELECT /*+ BROADCAST(small_table) */
    large.column1,
    small.column2
FROM large_table large
JOIN small_table small ON large.id = small.id;

-- Repartition hint para mejor distribución
SELECT /*+ REPARTITION(10) */
    region,
    COUNT(*)
FROM large_table
GROUP BY region;

-- Coalesce para reducir archivos de salida
SELECT /*+ COALESCE(1) */
    *
FROM processed_data
ORDER BY date;
```

### **Manejo de Datos Grandes**
```sql
-- Sampling para desarrollo y testing
SELECT *
FROM large_table 
TABLESAMPLE (10 PERCENT)  -- Solo 10% de los datos
WHERE sale_date >= '2024-01-01';

-- LIMIT con ORDER BY puede ser costoso
-- ❌ Evitar en tablas muy grandes sin partición
SELECT * FROM huge_table ORDER BY date DESC LIMIT 100;

-- ✅ Mejor usar filtros específicos
SELECT * FROM huge_table 
WHERE date >= DATE_SUB(CURRENT_DATE(), 7)
ORDER BY date DESC;
```

---

## 📊 **ANÁLISIS ESTADÍSTICO CON SQL**

### **Estadísticas Descriptivas**
```sql
-- Estadísticas completas
SELECT 
    region,
    COUNT(*) as count,
    AVG(amount) as mean,
    STDDEV(amount) as std_dev,
    MIN(amount) as min_val,
    MAX(amount) as max_val,
    PERCENTILE_APPROX(amount, 0.25) as q1,
    PERCENTILE_APPROX(amount, 0.5) as median,
    PERCENTILE_APPROX(amount, 0.75) as q3
FROM sales
GROUP BY region;

-- Distribución de frecuencias
SELECT 
    CASE 
        WHEN amount < 100 THEN '0-99'
        WHEN amount < 500 THEN '100-499'
        WHEN amount < 1000 THEN '500-999'
        ELSE '1000+'
    END as amount_bucket,
    COUNT(*) as frequency,
    COUNT(*) * 100.0 / SUM(COUNT(*)) OVER () as percentage
FROM sales
GROUP BY 
    CASE 
        WHEN amount < 100 THEN '0-99'
        WHEN amount < 500 THEN '100-499'
        WHEN amount < 1000 THEN '500-999'
        ELSE '1000+'
    END
ORDER BY amount_bucket;
```

### **Correlaciones Simples**
```sql
-- Correlación entre variables numéricas
WITH stats AS (
    SELECT 
        AVG(price) as avg_price,
        AVG(quantity) as avg_quantity,
        COUNT(*) as n
    FROM sales
),
correlation_calc AS (
    SELECT 
        SUM((price - s.avg_price) * (quantity - s.avg_quantity)) as numerator,
        SQRT(SUM(POWER(price - s.avg_price, 2))) as price_std,
        SQRT(SUM(POWER(quantity - s.avg_quantity, 2))) as quantity_std
    FROM sales
    CROSS JOIN stats s
)
SELECT 
    numerator / (price_std * quantity_std) as correlation_coefficient
FROM correlation_calc;
```

---

## 🚀 **CASOS DE USO COMUNES**

### **Dashboard de Ventas en Tiempo Real**
```sql
-- KPIs principales
SELECT 
    'Today' as period,
    COUNT(*) as total_orders,
    SUM(amount) as total_revenue,
    AVG(amount) as avg_order_value,
    COUNT(DISTINCT customer_id) as unique_customers
FROM sales 
WHERE DATE(sale_date) = CURRENT_DATE()

UNION ALL

SELECT 
    'Yesterday' as period,
    COUNT(*) as total_orders,
    SUM(amount) as total_revenue,
    AVG(amount) as avg_order_value,
    COUNT(DISTINCT customer_id) as unique_customers
FROM sales 
WHERE DATE(sale_date) = DATE_SUB(CURRENT_DATE(), 1);
```

### **Análisis de Productos Más Vendidos**
```sql
-- Top productos por diferentes métricas
SELECT 
    p.product_name,
    SUM(s.quantity) as total_quantity_sold,
    SUM(s.amount) as total_revenue,
    COUNT(DISTINCT s.customer_id) as unique_buyers,
    AVG(s.amount / s.quantity) as avg_unit_price
FROM sales s
JOIN products p ON s.product_id = p.product_id
WHERE s.sale_date >= DATE_SUB(CURRENT_DATE(), 30)
GROUP BY p.product_id, p.product_name
ORDER BY total_revenue DESC
LIMIT 20;
```

### **Análisis de Geografía de Ventas**
```sql
-- Ventas por región con comparación temporal
WITH current_period AS (
    SELECT 
        region,
        SUM(amount) as current_revenue
    FROM sales 
    WHERE sale_date >= DATE_SUB(CURRENT_DATE(), 30)
    GROUP BY region
),
previous_period AS (
    SELECT 
        region,
        SUM(amount) as previous_revenue
    FROM sales 
    WHERE sale_date >= DATE_SUB(CURRENT_DATE(), 60)
      AND sale_date < DATE_SUB(CURRENT_DATE(), 30)
    GROUP BY region
)
SELECT 
    c.region,
    c.current_revenue,
    COALESCE(p.previous_revenue, 0) as previous_revenue,
    (c.current_revenue - COALESCE(p.previous_revenue, 0)) / 
    COALESCE(p.previous_revenue, 1) * 100 as growth_percentage
FROM current_period c
LEFT JOIN previous_period p ON c.region = p.region
ORDER BY c.current_revenue DESC;
```

---

## 🎯 **EJEMPLO COMPLETO: ANÁLISIS DE TRANSPORTE**

```sql
-- Análisis completo del sistema de transporte
WITH trip_metrics AS (
    SELECT 
        vehicle_type,
        DATE_TRUNC('hour', trip_start_time) as hour,
        COUNT(*) as trip_count,
        AVG(distance_km) as avg_distance,
        AVG(fare_amount) as avg_fare,
        AVG(duration_minutes) as avg_duration,
        SUM(fare_amount) as total_revenue
    FROM trips
    WHERE trip_date >= DATE_SUB(CURRENT_DATE(), 7)  -- Última semana
    GROUP BY vehicle_type, DATE_TRUNC('hour', trip_start_time)
),
peak_hours AS (
    SELECT 
        hour,
        SUM(trip_count) as total_trips,
        RANK() OVER (ORDER BY SUM(trip_count) DESC) as hour_rank
    FROM trip_metrics
    GROUP BY hour
),
efficiency_metrics AS (
    SELECT 
        vehicle_type,
        AVG(fare_amount / distance_km) as revenue_per_km,
        AVG(fare_amount / duration_minutes) as revenue_per_minute
    FROM trips
    WHERE distance_km > 0 AND duration_minutes > 0
    GROUP BY vehicle_type
)
SELECT 
    tm.vehicle_type,
    tm.hour,
    tm.trip_count,
    tm.avg_distance,
    tm.avg_fare,
    tm.total_revenue,
    ph.hour_rank,
    em.revenue_per_km,
    em.revenue_per_minute,
    CASE 
        WHEN ph.hour_rank <= 3 THEN 'Peak Hour'
        WHEN ph.hour_rank <= 8 THEN 'Medium Hour'
        ELSE 'Low Hour'
    END as hour_category
FROM trip_metrics tm
JOIN peak_hours ph ON tm.hour = ph.hour
JOIN efficiency_metrics em ON tm.vehicle_type = em.vehicle_type
ORDER BY tm.vehicle_type, tm.hour;
```

---

## 🚨 **ERRORES COMUNES Y SOLUCIONES**

### **Performance Issues**
```sql
-- ❌ Evitar: Cartesian product accidental
SELECT * FROM table1, table2;  -- Sin JOIN condition

-- ✅ Correcto: JOIN explícito
SELECT * FROM table1 t1 
JOIN table2 t2 ON t1.id = t2.id;

-- ❌ Evitar: COUNT(*) en tablas enormes sin filtros
SELECT COUNT(*) FROM billion_row_table;

-- ✅ Mejor: APPROX_COUNT_DISTINCT o muestreo
SELECT APPROX_COUNT_DISTINCT(id) FROM billion_row_table;
```

### **Manejo de NULLs**
```sql
-- Comparaciones seguras con NULLs
SELECT *
FROM sales 
WHERE COALESCE(discount, 0) > 0;  -- Trata NULL como 0

-- Joins con posibles NULLs
SELECT s.*, c.customer_name
FROM sales s
LEFT JOIN customers c ON s.customer_id = c.customer_id
WHERE c.customer_id IS NOT NULL OR s.amount > 1000;
```

---

## 📋 **CHECKLIST DE COMPETENCIAS SQL BIG DATA**

### **Básico** ✅
- [ ] Escribo queries básicas con filtros eficientes
- [ ] Uso agregaciones simples (SUM, COUNT, AVG)
- [ ] Entiendo diferencia entre INNER/LEFT/RIGHT JOINs
- [ ] Manejo funciones básicas de fecha

### **Intermedio** ✅
- [ ] Uso window functions para rankings y moving averages
- [ ] Escribo CTEs (Common Table Expressions) complejas
- [ ] Optimizo queries con hints de Spark
- [ ] Identifico y soluciono problemas de performance

### **Avanzado** ✅
- [ ] Implemento análisis estadísticos complejos
- [ ] Creo análisis de cohortes y RFM
- [ ] Optimizo para datasets de TB+
- [ ] Combino SQL con programación (UDFs)

**💡 Tip Final: En Big Data, siempre piensa en particiones, distribución y minimizar shuffles!**
