# Food Delivery Orders Analysis
# Questions: How many orders per day? What sells most? When are the busy hours?
# How fast are our deliveries?

import pandas as pd
import matplotlib.pyplot as plt

# 1. Load the data
df = pd.read_csv("orders.csv")
df.columns = df.columns.str.strip()
df["date"] = pd.to_datetime(df["date"])           # turn text into real dates
df["weekday"] = df["date"].dt.day_name().str[:3]   # Mon, Tue, ...

# 2. Prepare the numbers for each chart
orders_per_day = df.groupby("date").size()                      # chart 1
items = df.groupby("item")["quantity"].sum().sort_values()      # chart 2

week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
busy = df.pivot_table(index="weekday", columns="hour",
                      values="order_id", aggfunc="count").reindex(week).fillna(0)  # chart 3
# chart 4 uses df["delivery_minutes"] directly

# 3. Print a few answers
print("Total orders:", len(df))
print("Most popular item:", items.index[-1])
print("Average delivery time:", round(df["delivery_minutes"].mean(), 1), "minutes")
print("Share delivered within 30 min:",
      round((df["delivery_minutes"] <= 30).mean() * 100), "%")

# 4. Draw each chart and save it as its own image

# Chart 1: line chart - daily order volume
fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(orders_per_day.index, orders_per_day.values, marker="o", color="#2a9d8f")
ax.set_title("Daily Order Volume")
ax.set_ylabel("Orders")
ax.tick_params(axis="x", rotation=30)
plt.tight_layout()
plt.savefig("1_daily_order_volume.png", dpi=120)
plt.close()

# Chart 2: horizontal bar chart - popular menu items
fig, ax = plt.subplots(figsize=(9, 5))
ax.barh(items.index, items.values, color="#e07a1f")
ax.set_title("Popular Menu Items")
ax.set_xlabel("Units sold")
plt.tight_layout()
plt.savefig("2_popular_menu_items.png", dpi=120)
plt.close()

# Chart 3: heatmap - peak ordering hours
fig, ax = plt.subplots(figsize=(9, 5))
img = ax.imshow(busy.values, cmap="YlOrRd", aspect="auto")
ax.set_xticks(range(len(busy.columns)))
ax.set_xticklabels(busy.columns)
ax.set_yticks(range(len(busy.index)))
ax.set_yticklabels(busy.index)
ax.set_xlabel("Hour of day (24h)")
ax.set_title("Peak Ordering Hours")
fig.colorbar(img, ax=ax, label="Orders")
plt.tight_layout()
plt.savefig("3_peak_ordering_hours.png", dpi=120)
plt.close()

# Chart 4: histogram - delivery time efficiency
fig, ax = plt.subplots(figsize=(9, 5))
ax.hist(df["delivery_minutes"], bins=12, color="#264653", edgecolor="white")
ax.axvline(30, color="red", linestyle="--", label="30 min target")
ax.set_title("Delivery Time Efficiency")
ax.set_xlabel("Delivery time (minutes)")
ax.set_ylabel("Orders")
ax.legend()
plt.tight_layout()
plt.savefig("4_delivery_time_histogram.png", dpi=120)
plt.close()

print("Saved 4 chart images")
