import streamlit as st

st.set_page_config(page_title="AVTRME Investor Simulator", layout="centered")

st.title("AVTRME Investor Return Simulator")
st.caption("All Volatility Trading & Risk Management Engine — Capital Projection Tool")

# Core Inputs
capital = st.slider(
    "Initial Investment ($)",
    min_value=1000,
    max_value=100000,
    value=30000,
    step=1000
)

annual_return = st.slider(
    "Hypothetical Annual Return (%)",
    min_value=-30,
    max_value=30,
    value=8,
    step=1
)

years = st.radio(
    "Investment Period",
    options=[1, 3, 5, 10],
    format_func=lambda x: f"{x} Year{'s' if x > 1 else ''}",
    horizontal=True
)

# Optional Tax & Inflation Controls
st.subheader("Optional Adjustments")
opt_col1, opt_col2 = st.columns(2)

with opt_col1:
    include_tax = st.toggle("Include Capital Gains Tax", value=False)
    tax_rate = (
        st.slider("Estimated Tax Rate (%)", min_value=0, max_value=50, value=15, step=1)
        if include_tax
        else 0
    )

with opt_col2:
    include_inflation = st.toggle("Adjust for Inflation", value=False)
    inflation_rate = (
        st.slider("Annual Inflation Rate (%)", min_value=0.0, max_value=15.0, value=2.5, step=0.5)
        if include_inflation
        else 0.0
    )

# Calculations
gross_ending_capital = capital * ((1 + annual_return / 100) ** years)
gross_profit = gross_ending_capital - capital

# Apply tax only on positive gains
tax_amount = max(0.0, gross_profit) * (tax_rate / 100)
after_tax_ending_capital = gross_ending_capital - tax_amount

# Adjust for inflation (Real Purchasing Power)
real_ending_capital = after_tax_ending_capital / ((1 + inflation_rate / 100) ** years)

final_profit_loss = real_ending_capital - capital
final_total_return = ((real_ending_capital / capital) - 1) * 100

st.divider()

# Display Metrics
col1, col2, col3 = st.columns(3)
capital_label = "Real Ending Capital" if include_inflation else "Projected Ending Capital"

col1.metric(capital_label, f"${real_ending_capital:,.0f}")
col2.metric("Net Profit / Loss", f"${final_profit_loss:+,.0f}")
col3.metric("Net Total Return", f"{final_total_return:+.2f}%")

# Breakdown summary when toggles are active
if include_tax or include_inflation:
    breakdown_parts = [f"**Gross Ending Value:** ${gross_ending_capital:,.0f}"]
    if include_tax:
        breakdown_parts.append(f"**Estimated Tax:** -${tax_amount:,.0f} ({tax_rate}%)")
    if include_inflation:
        inflation_erosion = after_tax_ending_capital - real_ending_capital
        breakdown_parts.append(f"**Inflation Impact:** -${inflation_erosion:,.0f} ({inflation_rate}%/yr)")
    st.caption(" | ".join(breakdown_parts))

# Dynamic Disclaimer
active_items = []
if include_tax:
    active_items.append("capital gains tax at exit")
if include_inflation:
    active_items.append("annual inflation discounting")

excluded_items = ["advisory fees", "withdrawals"]
if not include_tax:
    excluded_items.append("taxes")
if not include_inflation:
    excluded_items.append("inflation")

included_text = f" Includes {' and '.join(active_items)}." if active_items else ""
st.info(
    f"Assumes a constant annual return compounded annually.{included_text} "
    f"Excludes {', '.join(excluded_items)}. Educational simulation only—not a guarantee of future returns."
)
