import pandas as pd
import streamlit as st
import io

def calc_emi(P, R, N):
    R = R / (12 * 100)
    emi = (P * R * (1+R)**N) / ((1+R)**N - 1)
    return emi

# 🖥️ Streamlit Page Configuration
st.set_page_config(page_title="EMI Calculator", page_icon="💰", layout="centered")

st.title("💰 EMI Calculator & Schedule Generator")
st.write("Enter your loan details below to view and download your amortization schedule.")

# 📥 Input Fields
col1, col2, col3 = st.columns(3)

with col1:
    P = st.number_input("Loan Amount (Principal)", min_value=0.0, value=100000.0, step=1000.0)
with col2:
    R = st.number_input("Interest Rate (%)", min_value=0.0, value=8.5, step=0.1)
with col3:
    N = st.number_input("Period (Months)", min_value=1, value=12, step=1)

# ⚙️ Process Logic
if st.button("Generate EMI Schedule", type="primary"):
    if P > 0 and R > 0 and N > 0:
        try:
            emi = calc_emi(P, R, N)
            balance = P
            monthly_rate = R / (12 * 100)

            schedule = []

            for month in range(1, N + 1):
                interest = balance * monthly_rate
                principal = emi - interest
                balance -= principal

                schedule.append([
                    month,
                    round(emi, 2),
                    round(interest, 2),
                    round(principal, 2),
                    round(balance if balance > 0 else 0, 2)
                ])

            # Create DataFrame
            df = pd.DataFrame(schedule, columns=[
                "Month", "EMI", "Interest", "Principal", "Balance"
            ])

            # 📊 Display Key Metrics
            st.success("Schedule generated successfully!")
            m_col1, m_col2 = st.columns(2)
            m_col1.metric("Monthly EMI", f"${round(emi, 2):,}")
            m_col2.metric("Total Payable Interest", f"${round((emi * N) - P, 2):,}")

            # 📈 Display the Interactive Table
            st.subheader("Amortization Schedule")
            st.dataframe(df, use_container_width=True)

            # 💾 Convert DataFrame to Excel in-memory for download
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='EMI Schedule')
            
            # Download Button
            st.download_button(
                label="📥 Download EMI Schedule as Excel",
                data=buffer.getvalue(),
                file_name="EMI_Schedule.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please ensure all inputs are greater than zero.")
