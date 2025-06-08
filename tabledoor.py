import streamlit as st
import pandas as pd
import numpy as np

# Standard sizes (in inches)
STANDARD_SIZES = [12, 24, 30, 36, 42, 48, 54, 60, 72, 84, 96, 108, 120, 132]

def nearest_standard_size(inches):
    for s in STANDARD_SIZES:
        if inches <= s:
            return s
    return STANDARD_SIZES[-1]

st.title("🚪 Multiple Doors and windows Price Estimator")

st.markdown("### Enter data for each door below:")

# Default sample data
default_data = pd.DataFrame({
    "Length (cm)": [210.0],
    "Width (cm)": [90.0],
    "Horizontal Frames": [2],
    "Vertical Frames": [2],
    "Extra Horizontal Frames": [1],
    "Frame Size": ["5*2.5"],
    "Kol Price": [150.0],
    "Labour Cost": [300.0],
    "Sqft Price": [80.0],
    "Quantity": [1]
})

edited_df = st.data_editor(default_data, num_rows="dynamic", use_container_width=True)

# Store results
results = []

for index, row in edited_df.iterrows():
    try:
        # Convert to inches and adjust to nearest standard size
        length_in = round(row["Length (cm)"] / 2.54)
        width_in = round((row["Width (cm)"] / 2.54) + 6)

        adj_length = nearest_standard_size(length_in)
        adj_width = nearest_standard_size(width_in)

        # Frame size
        f1, f2 = map(float, row["Frame Size"].lower().split("*"))
        f1, f2 = round(f1, 2), round(f2, 2)
        frame_area = round(f1 * f2, 2)

        # Extra horizontal frame width
        extra_hf = row["Extra Horizontal Frames"]
        width_of_extra = round(adj_width / (extra_hf + 1), 2) if extra_hf > 0 else 0

        # Kol calculations
        length_kol = (
            (adj_length * row["Vertical Frames"]) +
            (adj_width * row["Horizontal Frames"]) +
            (width_of_extra * extra_hf)
        ) / 28
        length_kol = round(length_kol, 2)

        volume_kol = round((length_kol * frame_area) / 12, 2)

        # Grill cost
        sqft = (row["Length (cm)"] * row["Width (cm)"]) / 900
        grill_cost = round(sqft * row["Sqft Price"], 2)

        # Total pricing
        price = volume_kol * row["Kol Price"] + row["Labour Cost"] + grill_cost
        total_price = round(price * row["Quantity"], 2)

        results.append({
            "Door #": index + 1,
            "Adj. Length (in)": adj_length,
            "Adj. Width (in)": adj_width,
            "Length Kol": length_kol,
            "Volume Kol": volume_kol,
            "Grill Cost": grill_cost,
            "Unit Price (₹)": round(price, 2),
            "Quantity": row["Quantity"],
            "Total Price (₹)": total_price
        })

    except Exception as e:
        st.error(f"❌ Error in row {index + 1}: {e}")

# Show results
if results:
    st.markdown("### 📊 Results for Each Door")
    result_df = pd.DataFrame(results)
    st.dataframe(result_df, use_container_width=True)

    grand_total = result_df["Total Price (₹)"].sum()
    st.markdown(f"### 🧾 **Grand Total: ₹ {grand_total:,.2f}**")
