eo medidas básicas con DAX
- [ ] Diseño dashboards con visualizaciones estándar

### **Intermedio** ✅
- [ ] Optimizo modelo de datos con relaciones
- [ ] Uso time intelligence en DAX
- [ ] Implemento filtros y slicers avanzados
- [ ] Configuro actualización automática de datos

### **Avanzado** ✅
- [ ] Optimizo performance para datasets grandes
- [ ] Uso DirectQuery y Live Connection
- [ ] Implemento Row Level Security
- [ ] Integro con Azure services

---

## 🚨 **ERRORES COMUNES Y SOLUCIONES**

### **Performance Lento**
```
❌ Problema: Dashboard tarda mucho en cargar

✅ Soluciones:
1. Usar DirectQuery solo cuando necesario
2. Reducir cardinalidad en relaciones
3. Usar medidas en lugar de columnas calculadas
4. Implementar agregaciones automáticas
5. Limitar datos con filtros en Power Query
```

### **Memoria Insuficiente**
```
❌ Problema: "Cannot load model, insufficient memory"

✅ Soluciones:
1. Eliminar columnas innecesarias en Power Query
2. Usar tipos de datos más eficientes
3. Implementar particiones en Azure
4. Usar Power BI Premium para datasets grandes
5. Considerar Azure Analysis Services
```

### **Relaciones Incorrectas**
```
❌ Problema: Totales incorrectos en visualizaciones

✅ Soluciones:
1. Verificar cardinalidad de relaciones
2. Usar claves únicas en tablas de dimensión
3. Evitar relaciones bidireccionales innecesarias
4. Configurar dirección de filtro cruzado correcta
```

### **Actualización de Datos Falla**
```
❌ Problema: "Data source error" en actualización

✅ Soluciones:
1. Verificar credenciales del gateway
2. Comprobar conectividad de red
3. Optimizar consultas en Power Query
4. Configurar timeout adecuado
5. Usar autenticación de servicio cuando sea posible
```

---

## 🔗 **INTEGRACIÓN CON OTRAS HERRAMIENTAS**

### **Power BI + Python**
```python
# Script Python en Power BI
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans

# Power BI pasa data automáticamente como 'dataset'
df = dataset.copy()

# Clustering de clientes
features = ['total_spent', 'frequency', 'recency']
X = df[features].fillna(0)

kmeans = KMeans(n_clusters=4, random_state=42)
df['cluster'] = kmeans.fit_predict(X)

# Power BI espera resultado en variable 'dataset'
dataset = df
```

### **Power BI + R**
```r
# Script R en Power BI
library(forecast)

# Forecasting de ventas
ts_data <- ts(dataset$sales, frequency=12)
forecast_model <- auto.arima(ts_data)
forecast_result <- forecast(forecast_model, h=12)

# Crear dataframe con predicciones
dataset <- data.frame(
  period = 1:12,
  forecast = as.numeric(forecast_result$mean),
  lower = as.numeric(forecast_result$lower[,2]),
  upper = as.numeric(forecast_result$upper[,2])
)
```

### **Power BI + Azure Machine Learning**
```dax
-- Integración con Azure ML
ML Prediction = 
EVALUATE
SUMMARIZECOLUMNS(
    Customers[CustomerID],
    "Churn Probability",
    [AzureML Churn Model]
)

-- Configurar en Power Query
let
    Source = AzureML.Models("https://your-workspace.azureml.net/webservices/your-service"),
    InvokeFunction = Source("your-api-key"),
    Result = InvokeFunction(YourInputTable)
in
    Result
```

---

## 📈 **CASOS DE USO AVANZADOS**

### **Real-time Dashboard**
```
Configuración Streaming:
1. Crear streaming dataset en Power BI Service
2. Obtener Push URL
3. Enviar datos vía REST API

POST https://api.powerbi.com/beta/datasets/{dataset-id}/rows
{
  "rows": [
    {
      "timestamp": "2024-01-15T10:30:00Z",
      "metric": "sales",
      "value": 1500,
      "location": "Madrid"
    }
  ]
}

Visualización:
- Actualización automática cada 1 segundo
- Tiles optimizados para streaming
- Alertas automáticas por thresholds
```

### **Embedded Analytics**
```javascript
// Embeder Power BI en aplicación web
var models = window['powerbi-client'].models;

var config = {
    type: 'report',
    id: 'your-report-id',
    embedUrl: 'https://app.powerbi.com/reportEmbed?reportId=your-report-id',
    accessToken: 'your-access-token',
    tokenType: models.TokenType.Embed,
    settings: {
        filterPaneEnabled: false,
        navContentPaneEnabled: false
    }
};

// Embed report
var reportContainer = document.getElementById('reportContainer');
var report = powerbi.embed(reportContainer, config);
```

### **Row Level Security (RLS)**
```dax
-- Tabla de seguridad
Security = 
ADDCOLUMNS(
    VALUES(Users[Email]),
    "AllowedRegions", 
    SWITCH(
        Users[Email],
        "manager@company.com", "All",
        "sales.north@company.com", "North",
        "sales.south@company.com", "South",
        "None"
    )
)

-- Filtro RLS en tabla de ventas
[Region] = 
IF(
    LOOKUPVALUE(Security[AllowedRegions], Security[Email], USERNAME()) = "All",
    [Region],
    IF(
        LOOKUPVALUE(Security[AllowedRegions], Security[Email], USERNAME()) = [Region],
        [Region],
        BLANK()
    )
)
```

---

## 🎪 **PROYECTO COMPLETO: ANALYTICS DE E-COMMERCE**

### **1. Arquitectura de Datos**
```
Fuentes:
- Transacciones (SQL Server)
- Inventario (Azure SQL)
- Clientes (CRM API)
- Productos (Excel)
- Web Analytics (Google Analytics)

Pipeline:
Azure Data Factory → Azure Data Lake → Power BI
```

### **2. Modelo Dimensional**
```
Tablas de Hechos:
- FactSales (TransactionID, CustomerID, ProductID, Date, Quantity, Amount)
- FactInventory (ProductID, Date, StockLevel, ReorderPoint)

Dimensiones:
- DimCustomer (CustomerID, Name, Segment, Location)
- DimProduct (ProductID, Name, Category, Brand, Cost)
- DimDate (Date, Year, Quarter, Month, Week, DayOfWeek)
- DimGeography (LocationID, Country, State, City, Region)
```

### **3. Power Query Avanzado**
```m
// Función para limpiar datos de ventas
CleanSalesData = (Source as table) as table =>
let
    // Filtrar fechas válidas
    FilteredDates = Table.SelectRows(Source, each [OrderDate] <> null and [OrderDate] >= #date(2020,1,1)),
    
    // Limpiar montos
    CleanedAmounts = Table.ReplaceValue(FilteredDates, null, 0, Replacer.ReplaceValue, {"Amount"}),
    
    // Categorizar clientes
    AddCustomerSegment = Table.AddColumn(CleanedAmounts, "CustomerSegment", 
        each if [TotalSpent] > 10000 then "VIP"
        else if [TotalSpent] > 5000 then "Premium" 
        else if [TotalSpent] > 1000 then "Regular"
        else "New"),
    
    // Calcular métricas
    AddMetrics = Table.AddColumn(AddCustomerSegment, "ProfitMargin", 
        each ([Amount] - [Cost]) / [Amount])
in
    AddMetrics

// Aplicar función
TransformedSales = CleanSalesData(RawSalesData)
```

### **4. DAX Measures Suite**
```dax
-- Revenue Metrics
Total Revenue = SUM(FactSales[Amount])
Revenue LY = CALCULATE([Total Revenue], SAMEPERIODLASTYEAR(DimDate[Date]))
Revenue Growth % = DIVIDE([Total Revenue] - [Revenue LY], [Revenue LY])

-- Customer Metrics  
New Customers = 
CALCULATE(
    DISTINCTCOUNT(FactSales[CustomerID]),
    FILTER(
        ALL(DimDate),
        DimDate[Date] >= CALCULATE(MIN(FactSales[OrderDate])) &&
        DimDate[Date] <= MAX(DimDate[Date])
    )
)

Customer Lifetime Value = 
DIVIDE(
    [Total Revenue],
    [Total Customers]
)

-- Product Metrics
Top Products = 
IF(
    RANKX(ALL(DimProduct[ProductName]), [Total Revenue], , DESC) <= 20,
    [Total Revenue],
    BLANK()
)

Inventory Turnover = 
DIVIDE(
    [Cost of Goods Sold],
    [Average Inventory Value]
)

-- Advanced Analytics
Basket Analysis = 
CALCULATE(
    AVERAGEX(
        VALUES(FactSales[TransactionID]),
        DISTINCTCOUNT(FactSales[ProductID])
    )
)

Seasonal Index = 
DIVIDE(
    [Total Revenue],
    CALCULATE(
        [Total Revenue],
        ALL(DimDate[Month])
    ) / 12
)
```

### **5. Dashboard Executive**
```
Executive Dashboard:

┌─────────────────────────────────────────────────────┐
│ Header: Company Logo + Refresh Time                 │
├─────────────────────────────────────────────────────┤
│ KPI Cards Row:                                      │
│ [Revenue] [Growth%] [Orders] [New Customers] [AOV]  │
├─────────────────┬───────────────────────────────────┤
│ Revenue Trend   │ Top 10 Products                   │
│ (Line + Bars)   │ (Horizontal Bar)                  │
├─────────────────┼───────────────────────────────────┤
│ Customer Cohort │ Inventory Levels                  │
│ (Matrix)        │ (Gauge + Table)                   │
├─────────────────┼───────────────────────────────────┤
│ Geographic Map  │ Category Performance              │
│ (Revenue by     │ (Treemap)                         │
│  Region)        │                                   │
└─────────────────┴───────────────────────────────────┘

Interactivity:
- Cross-filtering entre visualizaciones
- Drill-through a details
- Bookmarks para diferentes vistas
- Sync slicers en todas las páginas
```

---

## 💡 **TIPS DE PRODUCTIVIDAD**

### **Shortcuts Útiles**
```
Ctrl + S: Guardar
Ctrl + C/V: Copiar/Pegar visualizaciones
Ctrl + D: Duplicar página
Ctrl + G: Agrupar objetos
Alt + F4: Cerrar Power BI
F5: Actualizar datos
Ctrl + Click: Selección múltiple
```

### **Templates y Themes**
```
Crear Theme Custom:
1. Formato → Cambiar tema → Personalizar tema actual
2. Definir colores corporativos
3. Configurar fuentes estándar
4. Exportar como .JSON
5. Aplicar en futuros reportes

Template Structure:
- Página 1: Executive Summary
- Página 2: Sales Analysis  
- Página 3: Customer Analysis
- Página 4: Product Analysis
- Página 5: Operational Metrics
```

### **Best Practices**
```
Diseño:
✅ Máximo 7 visualizaciones por página
✅ Colores consistentes con marca
✅ Títulos descriptivos y claros
✅ Espaciado uniforme
✅ Responsive design

Performance:
✅ Usar medidas en lugar de columnas calculadas
✅ Limitar filas en tablas (top 100)
✅ Evitar visualizaciones innecesarias
✅ Optimizar relaciones del modelo
✅ Usar agregaciones cuando sea posible

Governance:
✅ Naming conventions consistentes
✅ Documentar fórmulas DAX complejas
✅ Versioning de reportes
✅ Backup regular de archivos .pbix
✅ Testing antes de publicar
```

**💡 Tip Final: Power BI es más poderoso cuando se combina con una buena arquitectura de datos. ¡Invierte tiempo en diseñar el modelo correcto desde el inicio!**
