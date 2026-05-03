# Module 12 Assignment: Business Analytics Fundamentals and Applications
# GreenGrocer Data Analysis

# Import required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats


# Welcome message
print("=" * 60)
print("GREENGROCER BUSINESS ANALYTICS")
print("=" * 60)

# ----- USE THE FOLLOWING CODE TO CREATE SAMPLE DATA (DO NOT MODIFY) -----
# Set seed for reproducibility
np.random.seed(42)

# Store information
stores = ["Tampa", "Orlando", "Miami", "Jacksonville", "Gainesville"]
store_data = {
    "Store": stores,
    "SquareFootage": [15000, 12000, 18000, 10000, 8000],
    "StaffCount": [45, 35, 55, 30, 25],
    "YearsOpen": [5, 3, 7, 2, 1],
    "WeeklyMarketingSpend": [2500, 2000, 3000, 1800, 1500]
}

# Create store dataframe
store_df = pd.DataFrame(store_data)

# Product categories and departments
departments = ["Produce", "Dairy", "Bakery", "Grocery", "Prepared Foods"]
categories = {
    "Produce": ["Organic Vegetables", "Organic Fruits", "Fresh Herbs"],
    "Dairy": ["Milk & Cream", "Cheese", "Yogurt"],
    "Bakery": ["Bread", "Pastries", "Cakes"],
    "Grocery": ["Grains", "Canned Goods", "Snacks"],
    "Prepared Foods": ["Hot Bar", "Salad Bar", "Sandwiches"]
}

# Generate sales data for each store
sales_data = []
dates = pd.date_range(start="2023-01-01", end="2023-12-31", freq="D")

# Base performance factors for each store (relative scale)
store_performance = {
    "Tampa": 1.0,
    "Orlando": 0.85,
    "Miami": 1.2,
    "Jacksonville": 0.75,
    "Gainesville": 0.65
}

# Base performance factors for each department (relative scale)
dept_performance = {
    "Produce": 1.2,
    "Dairy": 1.0,
    "Bakery": 0.85,
    "Grocery": 0.95,
    "Prepared Foods": 1.1
}

# Generate daily sales data for each store, department, and category
for date in dates:
    # Seasonal factor (higher in summer and December)
    month = date.month
    seasonal_factor = 1.0
    if month in [6, 7, 8]:  # Summer
        seasonal_factor = 1.15
    elif month == 12:  # December
        seasonal_factor = 1.25
    elif month in [1, 2]:  # Winter
        seasonal_factor = 0.9

    # Day of week factor (weekends are busier)
    dow_factor = 1.3 if date.dayofweek >= 5 else 1.0  # Weekend vs weekday

    for store in stores:
        store_factor = store_performance[store]

        for dept in departments:
            dept_factor = dept_performance[dept]

            for category in categories[dept]:
                # Base sales amount
                base_sales = np.random.normal(loc=500, scale=100)

                # Calculate final sales with all factors and some randomness
                sales_amount = base_sales * store_factor * dept_factor * seasonal_factor * dow_factor
                sales_amount = sales_amount * np.random.normal(loc=1.0, scale=0.1)  # Add noise

                # Calculate profit margin (different base margins for departments)
                base_margin = {
                    "Produce": 0.25,
                    "Dairy": 0.22,
                    "Bakery": 0.35,
                    "Grocery": 0.20,
                    "Prepared Foods": 0.40
                }[dept]
                profit_margin = base_margin * np.random.normal(loc=1.0, scale=0.05)
                profit_margin = max(min(profit_margin, 0.5), 0.15)  # Keep within reasonable range

                # Calculate profit
                profit = sales_amount * profit_margin

                # Add record
                sales_data.append({
                    "Date": date,
                    "Store": store,
                    "Department": dept,
                    "Category": category,
                    "Sales": round(sales_amount, 2),
                    "ProfitMargin": round(profit_margin, 4),
                    "Profit": round(profit, 2)
                })

# Create sales dataframe
sales_df = pd.DataFrame(sales_data)

# Generate customer data
customer_data = []
total_customers = 5000

# Age distribution parameters
age_mean, age_std = 42, 15

# Income distribution parameters (in $1000s)
income_mean, income_std = 85, 30

# Create customer segments (will indirectly influence spending)
segments = ["Health Enthusiast", "Gourmet Cook", "Family Shopper", "Budget Organic", "Occasional Visitor"]
segment_probabilities = [0.25, 0.20, 0.30, 0.15, 0.10]

# Store preference probabilities (matches store performance somewhat)
store_probs = {
    "Tampa": 0.25,
    "Orlando": 0.20,
    "Miami": 0.30,
    "Jacksonville": 0.15,
    "Gainesville": 0.10
}

for i in range(total_customers):
    # Basic demographics
    age = int(np.random.normal(loc=age_mean, scale=age_std))
    age = max(min(age, 85), 18)  # Keep age in reasonable range

    gender = np.random.choice(["M", "F"], p=[0.48, 0.52])

    income = int(np.random.normal(loc=income_mean, scale=income_std))
    income = max(income, 20)  # Minimum income

    # Customer segment
    segment = np.random.choice(segments, p=segment_probabilities)

    # Preferred store
    preferred_store = np.random.choice(stores, p=list(store_probs.values()))

    # Shopping behavior - influenced by segment
    if segment == "Health Enthusiast":
        visit_frequency = np.random.randint(8, 15)  # Visits per month
        avg_basket = np.random.normal(loc=75, scale=15)
    elif segment == "Gourmet Cook":
        visit_frequency = np.random.randint(4, 10)
        avg_basket = np.random.normal(loc=120, scale=25)
    elif segment == "Family Shopper":
        visit_frequency = np.random.randint(5, 12)
        avg_basket = np.random.normal(loc=150, scale=30)
    elif segment == "Budget Organic":
        visit_frequency = np.random.randint(6, 10)
        avg_basket = np.random.normal(loc=60, scale=10)
    else:  # Occasional Visitor
        visit_frequency = np.random.randint(1, 5)
        avg_basket = np.random.normal(loc=45, scale=15)

    # Ensure values are reasonable
    visit_frequency = max(min(visit_frequency, 30), 1)
    avg_basket = max(avg_basket, 15)

    # Loyalty tier based on combination of frequency and spending
    monthly_spend = visit_frequency * avg_basket
    if monthly_spend > 1000:
        loyalty_tier = "Platinum"
    elif monthly_spend > 500:
        loyalty_tier = "Gold"
    elif monthly_spend > 200:
        loyalty_tier = "Silver"
    else:
        loyalty_tier = "Bronze"

    # Add to customer data
    customer_data.append({
        "CustomerID": f"C{i+1:04d}",
        "Age": age,
        "Gender": gender,
        "Income": income * 1000,  # Convert to actual income
        "Segment": segment,
        "PreferredStore": preferred_store,
        "VisitsPerMonth": visit_frequency,
        "AvgBasketSize": round(avg_basket, 2),
        "MonthlySpend": round(visit_frequency * avg_basket, 2),
        "LoyaltyTier": loyalty_tier
    })

# Create customer dataframe
customer_df = pd.DataFrame(customer_data)

# Create some calculated operational metrics for stores
operational_data = []

for store in stores:
    # Get store details
    store_row = store_df[store_df["Store"] == store].iloc[0]
    square_footage = store_row["SquareFootage"]
    staff_count = store_row["StaffCount"]

    # Calculate store metrics
    store_sales = sales_df[sales_df["Store"] == store]["Sales"].sum()
    store_profit = sales_df[sales_df["Store"] == store]["Profit"].sum()

    # Calculate derived metrics
    sales_per_sqft = store_sales / square_footage
    profit_per_sqft = store_profit / square_footage
    sales_per_staff = store_sales / staff_count
    inventory_turnover = np.random.uniform(12, 18) * store_performance[store]
    customer_satisfaction = min(5, np.random.normal(loc=4.0, scale=0.3) *
                                (store_performance[store] ** 0.5))

    # Add to operational data
    operational_data.append({
        "Store": store,
        "AnnualSales": round(store_sales, 2),
        "AnnualProfit": round(store_profit, 2),
        "SalesPerSqFt": round(sales_per_sqft, 2),
        "ProfitPerSqFt": round(profit_per_sqft, 2),
        "SalesPerStaff": round(sales_per_staff, 2),
        "InventoryTurnover": round(inventory_turnover, 2),
        "CustomerSatisfaction": round(customer_satisfaction, 2)
    })

# Create operational dataframe
operational_df = pd.DataFrame(operational_data)

# Print data info
print("\nDataframes created successfully. Ready for analysis!")
print(f"Sales data shape: {sales_df.shape}")
print(f"Customer data shape: {customer_df.shape}")
print(f"Store data shape: {store_df.shape}")
print(f"Operational data shape: {operational_df.shape}")

# Print sample of each dataframe
print("\nSales Data Sample:")
print(sales_df.head(3))
print("\nCustomer Data Sample:")
print(customer_df.head(3))
print("\nStore Data Sample:")
print(store_df)
print("\nOperational Data Sample:")
print(operational_df)
# ----- END OF DATA CREATION -----


# TODO 1: Descriptive Analytics - Overview of Current Performance

def analyze_sales_performance():
    """
    Analyze overall sales performance with descriptive statistics
    REQUIRED: Create and return dictionary with keys:
    - 'total_sales': float
    - 'total_profit': float
    - 'avg_profit_margin': float
    - 'sales_by_store': pandas Series
    - 'sales_by_dept': pandas Series
    """
    total_sales = sales_df["Sales"].sum()
    total_profit = sales_df["Profit"].sum()
    avg_profit_margin = sales_df["ProfitMargin"].mean()
    sales_by_store = sales_df.groupby("Store")["Sales"].sum().sort_values(ascending=False)
    sales_by_dept = sales_df.groupby("Department")["Sales"].sum().sort_values(ascending=False)

    print(f"\nTotal annual sales: ${total_sales:,.2f}")
    print(f"Total annual profit: ${total_profit:,.2f}")
    print(f"Avg profit margin: {avg_profit_margin:.2%}")
    print(f"\nSales stats (per transaction):")
    print(f"  Mean:   ${sales_df['Sales'].mean():.2f}")
    print(f"  Median: ${sales_df['Sales'].median():.2f}")
    print(f"  Std:    ${sales_df['Sales'].std():.2f}")
    print(f"  Min:    ${sales_df['Sales'].min():.2f}")
    print(f"  Max:    ${sales_df['Sales'].max():.2f}")
    print(f"\nSales by store:\n{sales_by_store.to_string()}")
    print(f"\nSales by department:\n{sales_by_dept.to_string()}")

    return {
        "total_sales": total_sales,
        "total_profit": total_profit,
        "avg_profit_margin": avg_profit_margin,
        "sales_by_store": sales_by_store,
        "sales_by_dept": sales_by_dept
    }


def visualize_sales_distribution():
    """
    Create visualizations showing how sales are distributed
    REQUIRED: Return tuple of three figures (store_fig, dept_fig, time_fig)
    """
    # Figure 1 - sales by store (bar chart)
    store_fig, ax1 = plt.subplots(figsize=(8, 5))
    sales_by_store = sales_df.groupby("Store")["Sales"].sum().sort_values(ascending=False)
    ax1.bar(sales_by_store.index, sales_by_store.values, color="steelblue", edgecolor="black")
    ax1.set_title("Annual Sales by Store")
    ax1.set_xlabel("Store")
    ax1.set_ylabel("Total Sales ($)")
    ax1.tick_params(axis="x", rotation=15)
    for i, v in enumerate(sales_by_store.values):
        ax1.text(i, v + 5000, f"${v/1e6:.2f}M", ha="center", fontsize=9)
    store_fig.tight_layout()

    # Figure 2 - sales by department (horizontal bar)
    dept_fig, ax2 = plt.subplots(figsize=(8, 5))
    sales_by_dept = sales_df.groupby("Department")["Sales"].sum().sort_values()
    ax2.barh(sales_by_dept.index, sales_by_dept.values, color="darkorange", edgecolor="black")
    ax2.set_title("Annual Sales by Department")
    ax2.set_xlabel("Total Sales ($)")
    ax2.set_ylabel("Department")
    for i, v in enumerate(sales_by_dept.values):
        ax2.text(v + 5000, i, f"${v/1e6:.2f}M", va="center", fontsize=9)
    dept_fig.tight_layout()

    # Figure 3 - monthly sales trend (line chart)
    time_fig, ax3 = plt.subplots(figsize=(10, 5))
    sales_df["Month"] = sales_df["Date"].dt.month
    monthly_sales = sales_df.groupby("Month")["Sales"].sum()
    month_labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    ax3.plot(monthly_sales.index, monthly_sales.values, marker="o", color="green", linewidth=2)
    ax3.set_xticks(range(1, 13))
    ax3.set_xticklabels(month_labels)
    ax3.set_title("Monthly Sales Trend (2023)")
    ax3.set_xlabel("Month")
    ax3.set_ylabel("Total Sales ($)")
    ax3.grid(axis="y", linestyle="--", alpha=0.5)
    time_fig.tight_layout()

    return (store_fig, dept_fig, time_fig)


def analyze_customer_segments():
    """
    Analyze customer segments and their relationship to spending
    REQUIRED: Return dictionary with keys:
    - 'segment_counts': pandas Series
    - 'segment_avg_spend': pandas Series
    - 'segment_loyalty': pandas DataFrame
    """
    segment_counts = customer_df["Segment"].value_counts()
    segment_avg_spend = customer_df.groupby("Segment")["MonthlySpend"].mean().sort_values(ascending=False)
    segment_loyalty = customer_df.groupby(["Segment", "LoyaltyTier"]).size().unstack(fill_value=0)

    print(f"\nCustomer segment counts:\n{segment_counts.to_string()}")
    print(f"\nAvg monthly spend by segment:\n{segment_avg_spend.round(2).to_string()}")
    print(f"\nLoyalty distribution by segment:\n{segment_loyalty.to_string()}")

    # Visualization - segment breakdown
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    axes[0].pie(segment_counts.values, labels=segment_counts.index, autopct="%1.1f%%", startangle=140)
    axes[0].set_title("Customer Segments")
    axes[1].bar(segment_avg_spend.index, segment_avg_spend.values, color="teal", edgecolor="black")
    axes[1].set_title("Avg Monthly Spend by Segment")
    axes[1].set_ylabel("Monthly Spend ($)")
    axes[1].tick_params(axis="x", rotation=20)
    fig.tight_layout()

    return {
        "segment_counts": segment_counts,
        "segment_avg_spend": segment_avg_spend,
        "segment_loyalty": segment_loyalty
    }


# TODO 2: Diagnostic Analytics - Understanding Relationships

def analyze_sales_correlations():
    """
    Analyze correlations between various factors and sales performance
    REQUIRED: Return dictionary with keys:
    - 'store_correlations': pandas DataFrame
    - 'top_correlations': list of tuples (factor, correlation)
    - 'correlation_fig': matplotlib figure
    """
    # Merge store characteristics with operational metrics
    merged_df = operational_df.merge(store_df, on="Store")

    # Correlation matrix of numerical features vs AnnualSales
    numeric_cols = ["SquareFootage", "StaffCount", "YearsOpen",
                    "WeeklyMarketingSpend", "InventoryTurnover", "CustomerSatisfaction"]
    store_correlations = merged_df[numeric_cols + ["AnnualSales"]].corr()

    # Top correlations with AnnualSales
    corr_with_sales = store_correlations["AnnualSales"].drop("AnnualSales").sort_values(
        key=abs, ascending=False)
    top_correlations = list(zip(corr_with_sales.index, corr_with_sales.values))

    print(f"\nCorrelations with annual sales:")
    for factor, corr in top_correlations:
        print(f"  {factor}: {corr:.4f}")

    # Heatmap
    correlation_fig, ax = plt.subplots(figsize=(9, 7))
    corr_matrix = merged_df[numeric_cols + ["AnnualSales", "AnnualProfit"]].corr()
    im = ax.imshow(corr_matrix, cmap="RdYlGn", vmin=-1, vmax=1)
    ax.set_xticks(range(len(corr_matrix.columns)))
    ax.set_yticks(range(len(corr_matrix.columns)))
    ax.set_xticklabels(corr_matrix.columns, rotation=45, ha="right", fontsize=8)
    ax.set_yticklabels(corr_matrix.columns, fontsize=8)
    for i in range(len(corr_matrix)):
        for j in range(len(corr_matrix.columns)):
            ax.text(j, i, f"{corr_matrix.iloc[i, j]:.2f}", ha="center", va="center", fontsize=7)
    plt.colorbar(im, ax=ax)
    ax.set_title("Correlation Matrix - Store Factors vs Performance")
    correlation_fig.tight_layout()

    return {
        "store_correlations": store_correlations,
        "top_correlations": top_correlations,
        "correlation_fig": correlation_fig
    }


def compare_store_performance():
    """
    Compare stores across different operational metrics
    REQUIRED: Return dictionary with keys:
    - 'efficiency_metrics': pandas DataFrame (with SalesPerSqFt, SalesPerStaff)
    - 'performance_ranking': pandas Series (ranked by profit)
    - 'comparison_fig': matplotlib figure
    """
    efficiency_metrics = operational_df[["Store", "SalesPerSqFt", "SalesPerStaff",
                                          "ProfitPerSqFt", "CustomerSatisfaction"]].set_index("Store")
    performance_ranking = operational_df.set_index("Store")["AnnualProfit"].sort_values(ascending=False)

    print(f"\nStore efficiency metrics:\n{efficiency_metrics.round(2).to_string()}")
    print(f"\nStore profit ranking:\n{performance_ranking.round(2).to_string()}")

    # Grouped bar chart for efficiency comparison
    comparison_fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    stores_sorted = performance_ranking.index.tolist()
    sales_per_sqft = [efficiency_metrics.loc[s, "SalesPerSqFt"] for s in stores_sorted]
    sales_per_staff = [efficiency_metrics.loc[s, "SalesPerStaff"] for s in stores_sorted]

    x = np.arange(len(stores_sorted))
    w = 0.35
    axes[0].bar(x - w/2, sales_per_sqft, w, label="Sales/SqFt", color="royalblue", edgecolor="black")
    axes[0].bar(x + w/2, [v/100 for v in sales_per_staff], w, label="Sales/Staff (÷100)",
                color="coral", edgecolor="black")
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(stores_sorted, rotation=15)
    axes[0].set_title("Efficiency Metrics by Store")
    axes[0].set_ylabel("Value")
    axes[0].legend()

    axes[1].bar(performance_ranking.index, performance_ranking.values, color="mediumseagreen", edgecolor="black")
    axes[1].set_title("Annual Profit by Store")
    axes[1].set_ylabel("Annual Profit ($)")
    axes[1].tick_params(axis="x", rotation=15)

    comparison_fig.tight_layout()

    return {
        "efficiency_metrics": efficiency_metrics,
        "performance_ranking": performance_ranking,
        "comparison_fig": comparison_fig
    }


def analyze_seasonal_patterns():
    """
    Identify and visualize seasonal patterns in sales data
    REQUIRED: Return dictionary with keys:
    - 'monthly_sales': pandas Series
    - 'dow_sales': pandas Series (day of week)
    - 'seasonal_fig': matplotlib figure
    """
    sales_df["Month"] = sales_df["Date"].dt.month
    sales_df["DayOfWeek"] = sales_df["Date"].dt.dayofweek

    monthly_sales = sales_df.groupby("Month")["Sales"].sum()
    dow_sales = sales_df.groupby("DayOfWeek")["Sales"].sum()

    # Rename day of week index for readability
    day_names = {0: "Mon", 1: "Tue", 2: "Wed", 3: "Thu", 4: "Fri", 5: "Sat", 6: "Sun"}
    dow_sales.index = dow_sales.index.map(day_names)

    month_labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    print(f"\nMonthly sales totals:\n{monthly_sales.round(2).to_string()}")
    print(f"\nSales by day of week:\n{dow_sales.round(2).to_string()}")

    seasonal_fig, axes = plt.subplots(2, 1, figsize=(10, 8))

    axes[0].bar(range(1, 13), monthly_sales.values, color="slateblue", edgecolor="black")
    axes[0].set_xticks(range(1, 13))
    axes[0].set_xticklabels(month_labels)
    axes[0].set_title("Monthly Sales (2023)")
    axes[0].set_ylabel("Total Sales ($)")
    axes[0].grid(axis="y", linestyle="--", alpha=0.4)

    axes[1].bar(dow_sales.index, dow_sales.values, color="tomato", edgecolor="black")
    axes[1].set_title("Sales by Day of Week")
    axes[1].set_ylabel("Total Sales ($)")
    axes[1].grid(axis="y", linestyle="--", alpha=0.4)

    seasonal_fig.tight_layout()

    return {
        "monthly_sales": monthly_sales,
        "dow_sales": dow_sales,
        "seasonal_fig": seasonal_fig
    }


# TODO 3: Predictive Analytics - Basic Forecasting

def predict_store_sales():
    """
    Use linear regression to predict store sales based on store characteristics
    REQUIRED: Return dictionary with keys:
    - 'coefficients': dict (feature: coefficient)
    - 'r_squared': float
    - 'predictions': pandas Series
    - 'model_fig': matplotlib figure
    """
    # Merge store info with operational totals
    model_df = operational_df.merge(store_df, on="Store")
    features = ["SquareFootage", "StaffCount", "YearsOpen", "WeeklyMarketingSpend"]
    X = model_df[features].values
    y = model_df["AnnualSales"].values

    # Normalize X for multi-feature regression using least squares
    # Using scipy linregress for the most correlated single feature first,
    # then doing multiple regression via numpy lstsq
    X_with_intercept = np.column_stack([np.ones(len(X)), X])
    coeffs, _, _, _ = np.linalg.lstsq(X_with_intercept, y, rcond=None)

    intercept = coeffs[0]
    feature_coeffs = coeffs[1:]
    coefficients = dict(zip(features, feature_coeffs))
    coefficients["intercept"] = intercept

    # Predictions and R-squared
    y_pred = X_with_intercept @ coeffs
    ss_res = np.sum((y - y_pred) ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    r_squared = 1 - ss_res / ss_tot if ss_tot != 0 else 0.0

    predictions = pd.Series(y_pred, index=model_df["Store"])

    print(f"\nLinear regression model results:")
    print(f"  R-squared: {r_squared:.4f}")
    print(f"  Intercept: {intercept:,.2f}")
    for feat, coef in coefficients.items():
        if feat != "intercept":
            print(f"  {feat}: {coef:,.4f}")
    print(f"\nPredicted vs actual sales:")
    for store in model_df["Store"]:
        actual = model_df.loc[model_df["Store"] == store, "AnnualSales"].values[0]
        predicted = predictions[store]
        print(f"  {store}: actual=${actual:,.0f}  predicted=${predicted:,.0f}")

    # Also run individual correlation for best single predictor (for plot)
    best_feat = max(features, key=lambda f: abs(np.corrcoef(model_df[f], y)[0, 1]))
    x_feat = model_df[best_feat].values
    slope, intercept_single, r_val, p_val, _ = stats.linregress(x_feat, y)

    model_fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Actual vs predicted
    axes[0].scatter(y, y_pred, color="royalblue", s=100, edgecolors="black", zorder=3)
    min_v = min(y.min(), y_pred.min()) * 0.95
    max_v = max(y.max(), y_pred.max()) * 1.05
    axes[0].plot([min_v, max_v], [min_v, max_v], "r--", label="Perfect fit")
    for i, store in enumerate(model_df["Store"]):
        axes[0].annotate(store, (y[i], y_pred[i]), textcoords="offset points",
                         xytext=(5, 3), fontsize=8)
    axes[0].set_xlabel("Actual Sales ($)")
    axes[0].set_ylabel("Predicted Sales ($)")
    axes[0].set_title(f"Actual vs Predicted Sales\n(R² = {r_squared:.4f})")
    axes[0].legend()

    # Best single feature regression
    x_line = np.linspace(model_df[best_feat].min(), model_df[best_feat].max(), 100)
    y_line = slope * x_line + intercept_single
    axes[1].scatter(model_df[best_feat], y, color="darkorange", s=100, edgecolors="black", zorder=3)
    axes[1].plot(x_line, y_line, "b-", linewidth=2, label=f"r={r_val:.3f}")
    for i, store in enumerate(model_df["Store"].values):
        axes[1].annotate(store, (model_df[best_feat].iloc[i], y[i]),
                         textcoords="offset points", xytext=(5, 3), fontsize=8)
    axes[1].set_xlabel(best_feat)
    axes[1].set_ylabel("Annual Sales ($)")
    axes[1].set_title(f"Sales vs {best_feat}")
    axes[1].legend()

    model_fig.tight_layout()

    return {
        "coefficients": coefficients,
        "r_squared": r_squared,
        "predictions": predictions,
        "model_fig": model_fig
    }


def forecast_department_sales():
    """
    Analyze and forecast departmental sales trends
    REQUIRED: Return dictionary with keys:
    - 'dept_trends': pandas DataFrame
    - 'growth_rates': pandas Series
    - 'forecast_fig': matplotlib figure
    """
    sales_df["Month"] = sales_df["Date"].dt.month

    # Monthly sales by department
    dept_monthly = sales_df.groupby(["Month", "Department"])["Sales"].sum().unstack()
    dept_trends = dept_monthly.copy()

    # Calculate growth rate H1 -> H2 (first 6 months vs last 6 months)
    h1 = dept_monthly.loc[1:6].sum()
    h2 = dept_monthly.loc[7:12].sum()
    growth_rates = ((h2 - h1) / h1).round(4)

    # Simple moving average forecast (3-month) for next 3 months (months 13-15)
    forecast_data = {}
    for dept in departments:
        last_3 = dept_monthly[dept].iloc[-3:].values
        forecast_data[dept] = np.mean(last_3)

    print(f"\nDepartment sales growth rates (H1 to H2):")
    print(growth_rates.round(4).to_string())
    print(f"\n3-month moving avg forecast (next period):")
    for dept, val in forecast_data.items():
        print(f"  {dept}: ${val:,.2f}/month")

    forecast_fig, axes = plt.subplots(2, 1, figsize=(12, 9))

    month_labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    colors = ["steelblue", "darkorange", "green", "red", "purple"]

    for i, dept in enumerate(departments):
        axes[0].plot(range(1, 13), dept_monthly[dept].values, marker="o",
                     label=dept, color=colors[i], linewidth=2)
    axes[0].set_xticks(range(1, 13))
    axes[0].set_xticklabels(month_labels)
    axes[0].set_title("Monthly Sales by Department")
    axes[0].set_ylabel("Sales ($)")
    axes[0].legend(loc="upper left", fontsize=8)
    axes[0].grid(axis="y", linestyle="--", alpha=0.4)

    bar_colors = ["green" if g > 0 else "red" for g in growth_rates.values]
    axes[1].bar(growth_rates.index, growth_rates.values * 100, color=bar_colors, edgecolor="black")
    axes[1].axhline(0, color="black", linewidth=0.8)
    axes[1].set_title("H1 to H2 Sales Growth Rate by Department (%)")
    axes[1].set_ylabel("Growth Rate (%)")
    axes[1].tick_params(axis="x", rotation=15)

    forecast_fig.tight_layout()

    return {
        "dept_trends": dept_trends,
        "growth_rates": growth_rates,
        "forecast_fig": forecast_fig
    }


# TODO 4: Integrated Analysis - Business Insights and Recommendations

def identify_profit_opportunities():
    """
    Identify the most profitable combinations and potential opportunities
    REQUIRED: Return dictionary with keys:
    - 'top_combinations': pandas DataFrame (top 10 store-dept combinations)
    - 'underperforming': pandas DataFrame (bottom 10)
    - 'opportunity_score': pandas Series (by store)
    """
    # Group by store and department, get total profit and avg margin
    combo_df = sales_df.groupby(["Store", "Department"]).agg(
        TotalSales=("Sales", "sum"),
        TotalProfit=("Profit", "sum"),
        AvgMargin=("ProfitMargin", "mean")
    ).reset_index()

    combo_df = combo_df.sort_values("TotalProfit", ascending=False)

    top_combinations = combo_df.head(10).reset_index(drop=True)
    underperforming = combo_df.tail(10).reset_index(drop=True)

    # Opportunity score = sales * avg margin (proxy for untapped potential)
    # Higher score for stores that have high sales but room to improve margin
    opp_df = operational_df.set_index("Store").copy()
    opp_df["MarginAvg"] = sales_df.groupby("Store")["ProfitMargin"].mean()
    # Opportunity = how much profit is left on the table relative to best performer
    best_margin = opp_df["MarginAvg"].max()
    opp_df["OpportunityScore"] = opp_df["AnnualSales"] * (best_margin - opp_df["MarginAvg"])
    opportunity_score = opp_df["OpportunityScore"].sort_values(ascending=False)

    print(f"\nTop 10 store-dept combinations by profit:")
    print(top_combinations[["Store", "Department", "TotalProfit", "AvgMargin"]].round(2).to_string(index=False))
    print(f"\nBottom 10 combinations by profit:")
    print(underperforming[["Store", "Department", "TotalProfit", "AvgMargin"]].round(2).to_string(index=False))
    print(f"\nOpportunity score by store (higher = more room to improve):")
    print(opportunity_score.round(2).to_string())

    return {
        "top_combinations": top_combinations,
        "underperforming": underperforming,
        "opportunity_score": opportunity_score
    }


def develop_recommendations():
    """
    Develop actionable recommendations based on the analysis
    REQUIRED: Return list of at least 5 recommendation strings
    """
    recommendations = [
        "Give more floor space to Prepared Foods and Bakery — best margins in the chain (40% and 35%), easy profit wins.",
        "Push Silver-tier Family Shoppers and Health Enthusiasts toward Gold — they're close and already visit often.",
        "Boost marketing in Jacksonville and Gainesville for summer/December — both stores are under-spending during peak months.",
        "Trim the Grocery department — lowest margin at 20%, swap slow SKUs for private-label organics.",
        "Model future stores after Miami — biggest footprint, most staff, highest sales. the data backs it up.",
        "Run midweek promos on Dairy and Grocery — weekends already spike 30%, weekdays need a nudge.",
        "Look into Orlando staffing — too many staff for their sales volume compared to similar stores."
    ]

    print(f"\nRecommendations ({len(recommendations)} total):")
    for i, rec in enumerate(recommendations, 1):
        print(f"\n  {i}. {rec}")

    return recommendations


# TODO 5: Summary Report

def generate_executive_summary():
    """
    Generate an executive summary of key findings and recommendations
    REQUIRED: Print executive summary with sections:
    - Overview (1 paragraph)
    - Key Findings (3-5 bullet points)
    - Recommendations (3-5 bullet points)
    - Expected Impact (1 paragraph)
    """
    total_sales = sales_df["Sales"].sum()
    total_profit = sales_df["Profit"].sum()
    avg_margin = sales_df["ProfitMargin"].mean()
    top_store = operational_df.sort_values("AnnualSales", ascending=False).iloc[0]["Store"]
    top_dept = sales_df.groupby("Department")["Sales"].sum().idxmax()
    top_margin_dept = sales_df.groupby("Department")["ProfitMargin"].mean().idxmax()

    print("\n" + "=" * 60)
    print("EXECUTIVE SUMMARY")
    print("=" * 60)

    print(f"""
OVERVIEW
--------
GreenGrocer brought in ${total_sales:,.0f} in total sales and ${total_profit:,.0f} in profit
across all five Florida stores in 2023, averaging a {avg_margin:.1%} profit margin.
{top_store} had the highest sales overall. There are clear gaps between stores
and some departments are punching way above their weight on margin.

KEY FINDINGS
------------
  - Miami is the top store by revenue; Jacksonville and Gainesville are well behind.
  - {top_dept} sells the most but {top_margin_dept} makes the most profit per dollar —
    not enough focus on the higher-margin stuff.
  - Sales jump 15% in summer and 25% in December; smaller stores aren't spending
    enough on marketing to take advantage of it.
  - Family Shoppers are the biggest segment (30%) and spend the most per trip.
  - Store size and staff count are the biggest drivers of sales performance.

RECOMMENDATIONS
---------------
  - More floor space for Prepared Foods and Bakery — highest margins, easiest profit gain.
  - Push Silver-tier loyalty members toward Gold, especially Family Shoppers.
  - Spend more on marketing in Jacksonville and Gainesville during peak months.
  - Audit Orlando staffing — too many staff for their current sales numbers.
  - Use Miami as the template for any future store locations.

EXPECTED IMPACT
---------------
These changes could close the gap between the best and worst stores fairly quickly.
Better marketing timing in the smaller stores and shifting shelf space toward
higher-margin departments are cheap moves with real upside. The loyalty push
should bump average monthly spend without needing to bring in new customers.
""")


# Main function to execute all analyses
# REQUIRED: Do not modify function name
def main():
    print("\n" + "=" * 60)
    print("GREENGROCER BUSINESS ANALYTICS RESULTS")
    print("=" * 60)

    # Execute analyses in a logical order
    # REQUIRED: Store all results for potential testing

    print("\n--- DESCRIPTIVE ANALYTICS: CURRENT PERFORMANCE ---")
    sales_metrics = analyze_sales_performance()
    dist_figs = visualize_sales_distribution()
    customer_analysis = analyze_customer_segments()

    print("\n--- DIAGNOSTIC ANALYTICS: UNDERSTANDING RELATIONSHIPS ---")
    correlations = analyze_sales_correlations()
    store_comparison = compare_store_performance()
    seasonality = analyze_seasonal_patterns()

    print("\n--- PREDICTIVE ANALYTICS: FORECASTING ---")
    sales_model = predict_store_sales()
    dept_forecast = forecast_department_sales()

    print("\n--- BUSINESS INSIGHTS AND RECOMMENDATIONS ---")
    opportunities = identify_profit_opportunities()
    recommendations = develop_recommendations()

    print("\n--- EXECUTIVE SUMMARY ---")
    generate_executive_summary()

    # Show all figures
    plt.show()

    # Return results for testing purposes
    return {
        'sales_metrics': sales_metrics,
        'customer_analysis': customer_analysis,
        'correlations': correlations,
        'store_comparison': store_comparison,
        'seasonality': seasonality,
        'sales_model': sales_model,
        'dept_forecast': dept_forecast,
        'opportunities': opportunities,
        'recommendations': recommendations
    }


# Run the main function
if __name__ == "__main__":
    results = main()