import sqlite3
import hashlib
import os

DB_PATH = "taxmind.db"


# ---------------------------------------------------------------------------
# Connection helper
# ---------------------------------------------------------------------------

def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


# ---------------------------------------------------------------------------
# Schema initialisation — called once on app startup
# ---------------------------------------------------------------------------

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id                INTEGER PRIMARY KEY AUTOINCREMENT,
            username          TEXT UNIQUE NOT NULL,
            password          TEXT NOT NULL,
            name              TEXT,
            employment_type   TEXT,
            income_bracket    TEXT,
            preferred_regime  TEXT DEFAULT 'new',
            language          TEXT DEFAULT 'en',
            setup_complete    INTEGER DEFAULT 0
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL,
            date        TEXT NOT NULL,
            description TEXT,
            amount      REAL NOT NULL,
            type        TEXT NOT NULL,
            category    TEXT
        )
    """)

    conn.commit()
    conn.close()


# ---------------------------------------------------------------------------
# Password hashing
# ---------------------------------------------------------------------------

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


# ---------------------------------------------------------------------------
# User operations
# ---------------------------------------------------------------------------

def create_user(username: str, password: str) -> bool:
    """Insert a new user. Returns True on success, False if username exists."""
    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username.strip(), hash_password(password))
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def authenticate_user(username: str, password: str):
    """Return the user Row if credentials match, else None."""
    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM users WHERE username = ? AND password = ?",
        (username.strip(), hash_password(password))
    ).fetchone()
    conn.close()
    return row


def get_user_by_id(user_id: int):
    conn = get_connection()
    row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    return row


def update_user_profile(user_id: int, name: str, employment_type: str,
                        income_bracket: str, preferred_regime: str,
                        language: str):
    conn = get_connection()
    conn.execute("""
        UPDATE users
        SET name = ?, employment_type = ?, income_bracket = ?,
            preferred_regime = ?, language = ?, setup_complete = 1
        WHERE id = ?
    """, (name, employment_type, income_bracket, preferred_regime,
          language, user_id))
    conn.commit()
    conn.close()


def update_user_language(user_id: int, language: str):
    conn = get_connection()
    conn.execute("UPDATE users SET language = ? WHERE id = ?", (language, user_id))
    conn.commit()
    conn.close()


# ---------------------------------------------------------------------------
# Transaction categorizer — rule-based keyword matching
# ---------------------------------------------------------------------------

CATEGORY_RULES = {
    "Food":          ["zomato", "swiggy", "restaurant", "cafe", "food"],
    "Transport":     ["uber", "ola", "rapido", "petrol", "fuel", "metro", "irctc"],
    "Shopping":      ["amazon", "flipkart", "myntra", "mall", "store"],
    "Utilities":     ["electricity", "water", "gas", "broadband", "wifi", "jio", "airtel"],
    "Health":        ["pharmacy", "hospital", "clinic", "medplus", "apollo"],
    "Entertainment": ["netflix", "spotify", "prime", "hotstar", "cinema", "pvr"],
    "Salary":        ["salary", "credited", "payroll"],
    "Investment":    ["mutual fund", "sip", "zerodha", "groww", "nps", "ppf"],
    "Loan/EMI":      ["emi", "loan", "repayment", "hdfc loan", "iciciloan"],
}


def categorize(description: str) -> str:
    if not description:
        return "Uncategorized"
    desc_lower = description.lower()
    for category, keywords in CATEGORY_RULES.items():
        for kw in keywords:
            if kw in desc_lower:
                return category
    return "Uncategorized"


# ---------------------------------------------------------------------------
# Transaction operations
# ---------------------------------------------------------------------------

def insert_transaction(user_id: int, date: str, description: str,
                       amount: float, txn_type: str):
    category = categorize(description)
    conn = get_connection()
    conn.execute("""
        INSERT INTO transactions (user_id, date, description, amount, type, category)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (user_id, date, description, amount, txn_type, category))
    conn.commit()
    conn.close()


def bulk_insert_transactions(user_id: int, rows: list[dict]):
    """
    rows: list of dicts with keys date, description, amount, type
    Returns count of rows inserted.
    """
    conn = get_connection()
    inserted = 0
    for row in rows:
        category = categorize(row.get("description", ""))
        conn.execute("""
            INSERT INTO transactions (user_id, date, description, amount, type, category)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            user_id,
            str(row.get("date", "")),
            str(row.get("description", "")),
            float(row.get("amount", 0)),
            str(row.get("type", "expense")),
            category
        ))
        inserted += 1
    conn.commit()
    conn.close()
    return inserted


def get_transactions(user_id: int, txn_type: str = None) -> list:
    conn = get_connection()
    if txn_type:
        rows = conn.execute(
            "SELECT * FROM transactions WHERE user_id = ? AND type = ? ORDER BY date DESC",
            (user_id, txn_type)
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM transactions WHERE user_id = ? ORDER BY date DESC",
            (user_id,)
        ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def seed_demo_data():
    """
    Insert a demo user (id=1) + 12 months of realistic transactions
    if the DB is empty. Safe to call on every startup — no duplicates.
    """
    conn = get_connection()
    cur = conn.cursor()

    # Demo user
    cur.execute("SELECT id FROM users WHERE id = 1")
    if not cur.fetchone():
        cur.execute("""
            INSERT INTO users (id, username, password, name, employment_type,
                               income_bracket, preferred_regime, language, setup_complete)
            VALUES (1, 'demo', 'demo', 'Arjun Mehta', 'Salaried',
                    '10L - 15L', 'new', 'en', 1)
        """)

    # Only seed transactions once
    cur.execute("SELECT COUNT(*) as cnt FROM transactions WHERE user_id = 1")
    if cur.fetchone()["cnt"] > 0:
        conn.close()
        return

    import random
    random.seed(42)

    months = [
        "2025-04", "2025-05", "2025-06", "2025-07", "2025-08", "2025-09",
        "2025-10", "2025-11", "2025-12", "2026-01", "2026-02", "2026-03",
    ]

    income_entries = [
        ("Salary credited - HDFC Payroll", 95000, "income"),
        ("Freelance project - TechCorp", 18000, "income"),
    ]

    expense_entries = [
        ("Zomato food order",         480,  "expense"),
        ("Amazon shopping",           1200, "expense"),
        ("Jio broadband recharge",    999,  "expense"),
        ("Uber ride to office",       320,  "expense"),
        ("Netflix subscription",      649,  "expense"),
        ("Apollo pharmacy",           860,  "expense"),
        ("Petrol refill",             1800, "expense"),
        ("Swiggy dinner",             620,  "expense"),
        ("SIP - Groww mutual fund",   5000, "expense"),
        ("Electricity bill MSEB",     1450, "expense"),
        ("Myntra clothing",           2200, "expense"),
        ("PVR cinema",                700,  "expense"),
        ("HDFC loan EMI",             8500, "expense"),
        ("Airtel mobile recharge",    399,  "expense"),
        ("Flipkart electronics",      3400, "expense"),
    ]

    rows = []
    for month in months:
        # Income (1-2 entries per month)
        for desc, base_amt, txn_type in income_entries[:1 if random.random() > 0.4 else 2]:
            amt = base_amt + random.randint(-3000, 3000)
            day = random.randint(1, 5)
            rows.append((1, f"{month}-{day:02d}", desc, amt, txn_type, categorize(desc)))

        # Expenses (8-12 random entries per month)
        sample = random.sample(expense_entries, k=random.randint(8, 12))
        for desc, base_amt, txn_type in sample:
            amt = round(base_amt * random.uniform(0.85, 1.2), 2)
            day = random.randint(1, 28)
            rows.append((1, f"{month}-{day:02d}", desc, amt, txn_type, categorize(desc)))

    cur.executemany("""
        INSERT INTO transactions (user_id, date, description, amount, type, category)
        VALUES (?, ?, ?, ?, ?, ?)
    """, rows)

    conn.commit()
    conn.close()


def get_monthly_totals(user_id: int) -> list[dict]:
    """
    Returns list of {month, income, expense} aggregated by YYYY-MM.
    """
    conn = get_connection()
    rows = conn.execute("""
        SELECT
            strftime('%Y-%m', date) AS month,
            SUM(CASE WHEN type = 'income'  THEN amount ELSE 0 END) AS income,
            SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END) AS expense
        FROM transactions
        WHERE user_id = ?
        GROUP BY month
        ORDER BY month
    """, (user_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]
