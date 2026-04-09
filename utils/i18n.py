import streamlit as st

STRINGS = {
    "en": {
        # General
        "app_title":            "TaxMind AI",
        "app_subtitle":         "Indian Tax Planning for FY 2026",
        "logout":               "Logout",
        "save":                 "Save",
        "submit":               "Submit",
        "cancel":               "Cancel",
        "success":              "Success",
        "error":                "Error",
        "language_label":       "Language",

        # Auth
        "login":                "Login",
        "signup":               "Sign Up",
        "username":             "Username",
        "password":             "Password",
        "login_btn":            "Login",
        "signup_btn":           "Create Account",
        "invalid_credentials":  "Invalid username or password.",
        "username_taken":       "Username already exists. Please choose another.",
        "signup_success":       "Account created. Complete your profile to continue.",

        # Profile wizard
        "wizard_title":         "Complete Your Profile",
        "wizard_subtitle":      "This helps TaxMind personalise your tax advice.",
        "full_name":            "Full Name",
        "employment_type":      "Employment Type",
        "income_bracket":       "Annual Income Bracket",
        "preferred_regime":     "Preferred Tax Regime",
        "wizard_save":          "Save and Continue",
        "wizard_saved":         "Profile saved.",

        # Dashboard
        "dashboard_title":      "Tax Calculator",
        "gross_income_label":   "Gross Annual Income (Rs.)",
        "calculate_btn":        "Calculate Tax",
        "tax_breakdown":        "Tax Computation",
        "gross_income":         "Gross Income",
        "standard_deduction":   "Standard Deduction",
        "taxable_income":       "Taxable Income",
        "tax_before_rebate":    "Tax Before Rebate",
        "rebate_87a":           "Rebate u/s 87A",
        "tax_after_rebate":     "Tax After Rebate",
        "cess":                 "Health & Education Cess (4%)",
        "total_tax_payable":    "Total Tax Payable",
        "slab_breakdown":       "Slab-wise Breakdown",
        "export_pdf":           "Download PDF",
        "export_csv":           "Download CSV",
        "regime_label":         "Tax Regime",

        # AI Advisor
        "advisor_title":        "AI Tax Advisor",
        "advisor_placeholder":  "Ask a tax question...",
        "advisor_thinking":     "Thinking...",
        "advisor_error":        "Unable to reach AI. Check your API key.",

        # Expenses
        "expenses_title":       "Expense Tracker",
        "no_expenses":          "No expense records found. Add transactions in Upload Data.",
        "category":             "Category",
        "total_amount":         "Total Amount (Rs.)",
        "expense_chart_title":  "Spend by Category",

        # GST / ITR
        "gst_itr_title":        "GST and ITR Tips",

        # Predictive Planning
        "planning_title":       "Predictive Tax Planning",
        "no_data_planning":     "No transaction data found. Add income and expense records first.",
        "projected_income":     "Projected Annual Income",
        "projected_tax":        "Projected Tax Payable",

        # Upload
        "upload_title":         "Upload and Manage Data",
        "manual_entry":         "Manual Entry",
        "csv_upload":           "CSV Upload",
        "date_label":           "Date",
        "description_label":    "Description",
        "amount_label":         "Amount (Rs.)",
        "type_label":           "Transaction Type",
        "add_transaction":      "Add Transaction",
        "transaction_added":    "Transaction recorded.",
        "upload_csv":           "Upload CSV File",
        "csv_success":          "{n} transactions imported successfully.",
        "csv_error":            "CSV must contain columns: date, description, amount, type",

        # Pricing
        "pricing_title":        "Pricing Plans",

        # Why TaxMind
        "why_title":            "Why TaxMind AI",
    },

    "hi": {
        # General
        "app_title":            "TaxMind AI",
        "app_subtitle":         "FY 2026 ke liye Indian Tax Planning",
        "logout":               "Logout",
        "save":                 "Sauven",
        "submit":               "Jama Karen",
        "cancel":               "Raddh Karen",
        "success":              "Safal",
        "error":                "Galti",
        "language_label":       "Bhasha",

        # Auth
        "login":                "Login",
        "signup":               "Naya Khata",
        "username":             "Upayogkarta Naam",
        "password":             "Password",
        "login_btn":            "Login Karen",
        "signup_btn":           "Khata Banayein",
        "invalid_credentials":  "Upayogkarta naam ya password galat hai.",
        "username_taken":       "Yeh naam pehle se maujood hai. Koi doosra naam chunen.",
        "signup_success":       "Khata ban gaya. Aage badhne ke liye apna vivran poora karen.",

        # Profile wizard
        "wizard_title":         "Apna Vivran Poora Karen",
        "wizard_subtitle":      "Yeh TaxMind ko aapki salah behtar banane mein madad karta hai.",
        "full_name":            "Poora Naam",
        "employment_type":      "Rozgaar Prakar",
        "income_bracket":       "Varshik Aay Shreni",
        "preferred_regime":     "Pasandida Tax Vyavastha",
        "wizard_save":          "Sauven aur Aage Baddhen",
        "wizard_saved":         "Vivran saur liya gaya.",

        # Dashboard
        "dashboard_title":      "Tax Calculator",
        "gross_income_label":   "Kul Varshik Aay (Rs.)",
        "calculate_btn":        "Tax Gainen",
        "tax_breakdown":        "Tax Ganana",
        "gross_income":         "Kul Aay",
        "standard_deduction":   "Standard Katoti",
        "taxable_income":       "Karyog Aay",
        "tax_before_rebate":    "Chhoot se Pehle Tax",
        "rebate_87a":           "Dhara 87A ke Tahat Chhoot",
        "tax_after_rebate":     "Chhoot ke Baad Tax",
        "cess":                 "Swasthya aur Shiksha Cess (4%)",
        "total_tax_payable":    "Kul Deya Tax",
        "slab_breakdown":       "Slab Anusaar Vivran",
        "export_pdf":           "PDF Download Karen",
        "export_csv":           "CSV Download Karen",
        "regime_label":         "Tax Vyavastha",

        # AI Advisor
        "advisor_title":        "AI Tax Salahkaar",
        "advisor_placeholder":  "Koi tax sawaal poochhen...",
        "advisor_thinking":     "Soch raha hoon...",
        "advisor_error":        "AI tak pahunch nahi. API key jaanchen.",

        # Expenses
        "expenses_title":       "Kharcha Tracker",
        "no_expenses":          "Koi kharcha nahi mila. Upload Data mein transaction jooden.",
        "category":             "Shreni",
        "total_amount":         "Kul Rashi (Rs.)",
        "expense_chart_title":  "Shreni Anusaar Kharcha",

        # GST / ITR
        "gst_itr_title":        "GST aur ITR Salah",

        # Predictive Planning
        "planning_title":       "Bhavishy Tax Yojana",
        "no_data_planning":     "Koi transaction data nahi mila. Pehle aay aur kharcha jooden.",
        "projected_income":     "Anumaanit Varshik Aay",
        "projected_tax":        "Anumaanit Deya Tax",

        # Upload
        "upload_title":         "Data Upload aur Prabandhan",
        "manual_entry":         "Haath se Darz Karen",
        "csv_upload":           "CSV Upload",
        "date_label":           "Tarikh",
        "description_label":    "Vivran",
        "amount_label":         "Rashi (Rs.)",
        "type_label":           "Lenden Prakar",
        "add_transaction":      "Transaction Jooden",
        "transaction_added":    "Transaction darz kar liya gaya.",
        "upload_csv":           "CSV File Upload Karen",
        "csv_success":          "{n} transactions safaltapoorvak import hue.",
        "csv_error":            "CSV mein yeh columns honee chahiye: date, description, amount, type",

        # Pricing
        "pricing_title":        "Muulya Yojanaen",

        # Why TaxMind
        "why_title":            "TaxMind AI Kyun",
    },
}


def t(key: str, **kwargs) -> str:
    """
    Return the UI string for the given key in the current session language.
    Falls back to English if the key is missing in the selected language.
    Supports format kwargs: t("csv_success", n=50)
    """
    lang = st.session_state.get("language", "en")
    lang_dict = STRINGS.get(lang, STRINGS["en"])
    value = lang_dict.get(key, STRINGS["en"].get(key, key))
    if kwargs:
        value = value.format(**kwargs)
    return value
