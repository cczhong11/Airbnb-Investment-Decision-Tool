import streamlit as st
import math

def main():
    st.title("Airbnb Investment Decision Tool (ﾉ◕ヮ◕)ﾉ*:･ﾟ✧")
    st.write("Let's figure out if that rental property is a smart move for you, bestie! uwu 💕")
    
    st.header("Property Details")
    purchase_price = st.number_input("Purchase Price ($):", value=500000.0, step=1000.0)
    down_payment_percent = st.number_input("Down Payment Percentage (e.g., 20 for 20%):", value=20.0, step=0.5)
    down_payment = purchase_price * (down_payment_percent / 100)
    
    monthly_rent = st.number_input("Expected Monthly Rent Income ($):", value=4500.0, step=50.0)
    vacancy_rate_percent = st.number_input("Expected Vacancy Rate (e.g., 5 for 5%):", value=4.0, step=0.5)
    vacancy_rate = vacancy_rate_percent / 100
    # Calculate annual gross rent adjusted for vacancy
    annual_gross_rent = monthly_rent * 12 * (1 - vacancy_rate)
    st.write(f"**Annual Gross Rent (after vacancy):** ${annual_gross_rent:.2f}")
    
    st.header("Operating Expenses")
    monthly_expenses = st.number_input("Monthly Operating Expenses (excluding mortgage, $):", value=200.0, step=10.0)
    property_tax_annual = st.number_input("Annual Property Tax ($):", value=1800.0, step=100.0)
    insurance_annual = st.number_input("Annual Insurance Cost ($):", value=2000.0, step=100.0)
    maintenance_annual = st.number_input("Annual Maintenance Cost ($):", value=5000.0, step=100.0)
    
    st.header("Airbnb Property Management (if applicable)")
    use_airbnb_pm = st.selectbox("Will you be using an Airbnb property manager?", ("yes", "no"))
    if use_airbnb_pm == "yes":
        pm_fee_percent = st.number_input("Airbnb PM Fee Percentage (e.g., 20 for 20%):", value=15.0, step=0.5)
        # Calculate Airbnb platform fee (3%)
        airbnb_platform_fee = annual_gross_rent * 0.03
        # Calculate amount after Airbnb platform fee (97%)
        amount_after_platform_fee = annual_gross_rent * 0.97
        # Calculate PM fee based on remaining amount
        annual_pm_fee = amount_after_platform_fee * (pm_fee_percent / 100)
        
        st.write(f"**Annual Airbnb Platform Fee (3%):** ${airbnb_platform_fee:.2f}")
        st.write(f"**Amount After Platform Fee:** ${amount_after_platform_fee:.2f}")
        st.write(f"**Annual Airbnb PM Fee ({pm_fee_percent}% of remaining):** ${annual_pm_fee:.2f}")
        
        # Add platform fee to total expenses
        annual_pm_fee += airbnb_platform_fee
    else:
        annual_pm_fee = 0.0

    st.header("Additional Expenses")
    # These extra inputs are based on industry guidelines for hidden rental expenses (see :contentReference[oaicite:0]{index=0}, :contentReference[oaicite:1]{index=1}, :contentReference[oaicite:2]{index=2})
    hoa_fees = st.number_input("Annual HOA Fees ($):", value=0.0, step=10.0)
    utilities = st.number_input("Annual Utilities Cost (if paid by landlord, $):", value=0.0, step=10.0)
    legal_accounting = st.number_input("Annual Legal & Accounting Fees ($):", value=0.0, step=10.0)
    marketing_screening = st.number_input("Annual Marketing & Tenant Screening Costs ($):", value=0.0, step=10.0)
    capex = st.number_input("Annual Capital Expenditures (CapEx) Reserve ($):", value=0.0, step=10.0)
    contingency = st.number_input("Annual Contingency Reserve ($):", value=0.0, step=10.0)
    
    # Sum all annual expenses
    annual_operating_expenses = (
        (monthly_expenses * 12)
        + property_tax_annual
        + insurance_annual
        + maintenance_annual
        + annual_pm_fee
        + hoa_fees
        + utilities
        + legal_accounting
        + marketing_screening
        + capex
        + contingency
    )
    st.write(f"**Total Annual Operating Expenses:** ${annual_operating_expenses:.2f}")
    st.write(f"**Total Monthly Operating Expenses:** ${annual_operating_expenses/12:.2f}")
    
    # Calculate NOI and Cap Rate
    noi = annual_gross_rent - annual_operating_expenses
    cap_rate = (noi / purchase_price) * 100 if purchase_price > 0 else 0
    st.write(f"**Net Operating Income (NOI):** ${noi:.2f} per year")
    st.write(f"**Cap Rate:** {cap_rate:.2f}%")
    
    st.header("Financing Options")
    use_mortgage = st.selectbox("Are you planning to use a mortgage?", ("yes", "no"))
    if use_mortgage == "yes":
        interest_rate = st.number_input("Annual Mortgage Interest Rate (%, e.g., 6.75 for 6.75%):", value=6.75, step=0.1)
        loan_term_years = st.number_input("Loan Term (years):", value=30, step=1)
        loan_amount = purchase_price - down_payment
        
        monthly_interest_rate = (interest_rate / 100) / 12
        number_of_payments = loan_term_years * 12
        
        if monthly_interest_rate != 0:
            mortgage_payment = loan_amount * (monthly_interest_rate * (1 + monthly_interest_rate) ** number_of_payments) / ((1 + monthly_interest_rate) ** number_of_payments - 1)
        else:
            mortgage_payment = loan_amount / number_of_payments
        
        annual_mortgage_payment = mortgage_payment * 12
        cash_flow = noi - annual_mortgage_payment
        cash_on_cash_return = (cash_flow / down_payment) * 100 if down_payment > 0 else 0
        
        st.write(f"**Annual Mortgage Payment:** ${annual_mortgage_payment:.2f}")
        st.write(f"**Estimated Annual Cash Flow:** ${cash_flow:.2f}")
        st.write(f"**Cash on Cash Return:** {cash_on_cash_return:.2f}%")
        
        if cash_on_cash_return >= 8:
            st.success("Yay! It looks like a solid investment opportunity! (≧◡≦) ♡")
        else:
            st.error("Hmm... The numbers seem a bit low. Maybe negotiate a better deal or revisit your expenses. (◕︵◕)")
    else:
        if cap_rate >= 8:
            st.success("Awesome! The property's Cap Rate looks promising! ☆*:.｡.o(≧▽≦)o.｡.:*☆")
        else:
            st.error("The Cap Rate is a bit low, so it might not be the best deal. Consider other options or re-evaluate the numbers. (╥﹏╥)")

if __name__ == "__main__":
    main()
