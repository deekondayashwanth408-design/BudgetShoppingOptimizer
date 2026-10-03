import streamlit as st


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Budget Shopping Optimizer",
    page_icon="🛒",
    layout="wide"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.stApp {
    background-color: #f5f7fb;
}

.main-title {
    font-size: 42px;
    font-weight: 800;
    text-align: center;
    color: #172033;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    color: #6b7280;
    font-size: 18px;
    margin-bottom: 25px;
}

.section-title {
    font-size: 25px;
    font-weight: 700;
    color: #172033;
    margin-top: 10px;
}

.info-card {
    background-color: white;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #e5e7eb;
    margin-bottom: 15px;
}

.footer {
    text-align: center;
    color: #6b7280;
    font-size: 14px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🛒 Budget Shopping Optimizer</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Intelligent product selection using Sorting, Greedy and 0/1 Knapsack'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


# ============================================================
# DEFAULT PRODUCTS
# ============================================================

default_products = [
    {
        "name": "Laptop Stand",
        "price": 2500,
        "utility": 80
    },
    {
        "name": "Wireless Mouse",
        "price": 1200,
        "utility": 60
    },
    {
        "name": "Keyboard",
        "price": 1800,
        "utility": 75
    },
    {
        "name": "Headphones",
        "price": 3000,
        "utility": 90
    },
    {
        "name": "USB Hub",
        "price": 1000,
        "utility": 55
    },
    {
        "name": "Webcam",
        "price": 2200,
        "utility": 70
    }
]


# ============================================================
# INITIALIZE PRODUCTS
# ============================================================

if "products" not in st.session_state:

    st.session_state.products = default_products.copy()


# ============================================================
# REMOVE DUPLICATE PRODUCTS
# ============================================================

unique_products = []
existing_names = set()

for product in st.session_state.products:

    product_name = product["name"].strip().lower()

    if product_name not in existing_names:

        unique_products.append(product)

        existing_names.add(product_name)


st.session_state.products = unique_products


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header("⚙️ Optimization Settings")


# ============================================================
# BUDGET RANGE
# ============================================================

st.sidebar.markdown("### 📊 Set Budget Range")


# Minimum Budget

min_budget = st.sidebar.number_input(
    "Minimum Budget (₹)",
    min_value=100,
    max_value=100000,
    value=500,
    step=500,
    key="min_budget"
)


# Maximum Budget

max_budget = st.sidebar.number_input(
    "Maximum Budget (₹)",
    min_value=1000,
    max_value=1000000,
    value=50000,
    step=500,
    key="max_budget"
)


# ============================================================
# CHECK BUDGET RANGE
# ============================================================

if min_budget >= max_budget:

    st.sidebar.error(
        "⚠️ Minimum budget must be less than maximum budget."
    )

    budget = int(min_budget)

else:

    # --------------------------------------------------------
    # ENTER BUDGET
    # --------------------------------------------------------

    budget = st.sidebar.number_input(
        "💰 Enter Your Budget (₹)",
        min_value=int(min_budget),
        max_value=int(max_budget),
        value=int(
            min(
                max(
                    10000,
                    min_budget
                ),
                max_budget
            )
        ),
        step=500,
        key="budget_input"
    )


# ============================================================
# SHOW CURRENT BUDGET
# ============================================================

if min_budget < max_budget:

    st.sidebar.success(
        f"Current Budget: ₹{budget:,}"
    )


# ============================================================
# SIDEBAR INFORMATION
# ============================================================

st.sidebar.divider()

st.sidebar.markdown("""
### 📌 How It Works

**Price**  
Money required to purchase the product.

**Utility**  
Benefit or value provided by the product.

**Utility / Price**  
Value obtained for every rupee spent.

The system finds a combination of products that maximizes
utility without exceeding the selected budget.
""")


# ============================================================
# ADD NEW PRODUCT
# ============================================================

st.markdown(
    '<div class="section-title">➕ Add New Product</div>',
    unsafe_allow_html=True
)

st.write(
    "Enter the product details and add them to your catalog."
)


# ============================================================
# ADD PRODUCT FORM
# ============================================================

with st.form(
    "add_product_form",
    clear_on_submit=True
):

    col1, col2, col3 = st.columns(3)

    with col1:

        product_name = st.text_input(
            "Product Name",
            placeholder="Example: Smart Watch"
        )

    with col2:

        product_price = st.number_input(
            "Price (₹)",
            min_value=1,
            value=1000,
            step=100
        )

    with col3:

        product_utility = st.number_input(
            "Utility Value",
            min_value=1,
            value=50,
            step=5
        )

    add_product = st.form_submit_button(
        "➕ Add Product",
        use_container_width=True
    )


# ============================================================
# ADD PRODUCT LOGIC
# ============================================================

if add_product:

    clean_name = product_name.strip()

    if clean_name == "":

        st.error(
            "⚠️ Please enter a product name."
        )

    else:

        duplicate = False

        for product in st.session_state.products:

            if (
                product["name"].strip().lower()
                == clean_name.lower()
            ):

                duplicate = True
                break


        if duplicate:

            st.warning(
                f"⚠️ '{clean_name}' already exists in the catalog."
            )

        else:

            new_product = {
                "name": clean_name,
                "price": int(product_price),
                "utility": int(product_utility)
            }

            st.session_state.products.append(
                new_product
            )

            st.success(
                f"✅ {clean_name} added successfully!"
            )


# ============================================================
# PRODUCT CATALOG
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">🛍️ Product Catalog</div>',
    unsafe_allow_html=True
)

st.write(
    "Products available for optimization."
)


products = st.session_state.products


# ============================================================
# CALCULATE UTILITY / PRICE
# ============================================================

for product in products:

    product["ratio"] = (
        product["utility"]
        / product["price"]
    )


# ============================================================
# PRODUCT TABLE HEADER
# ============================================================

header = st.columns(
    [3, 2, 2, 2, 1]
)

header[0].markdown("**Product**")
header[1].markdown("**Price**")
header[2].markdown("**Utility**")
header[3].markdown("**Utility / Price**")
header[4].markdown("**Action**")


# ============================================================
# DISPLAY PRODUCTS
# ============================================================

product_to_delete = None

for index, product in enumerate(products):

    columns = st.columns(
        [3, 2, 2, 2, 1]
    )

    columns[0].write(
        product["name"]
    )

    columns[1].write(
        f"₹{product['price']:,}"
    )

    columns[2].write(
        product["utility"]
    )

    columns[3].write(
        f"{product['ratio']:.4f}"
    )

    if columns[4].button(
        "🗑️",
        key=f"delete_product_{index}"
    ):

        product_to_delete = index


# ============================================================
# DELETE PRODUCT
# ============================================================

if product_to_delete is not None:

    deleted_name = (
        st.session_state.products[
            product_to_delete
        ]["name"]
    )

    st.session_state.products.pop(
        product_to_delete
    )

    st.success(
        f"🗑️ {deleted_name} removed from the catalog."
    )

    st.rerun()


# ============================================================
# GREEDY ALGORITHM
# ============================================================

def greedy_algorithm(items, budget):

    selected = []

    total_cost = 0

    total_utility = 0

    # Sort by Utility / Price

    sorted_items = sorted(
        items,
        key=lambda x:
            x["utility"] / x["price"],
        reverse=True
    )

    # Select products

    for item in sorted_items:

        if (
            total_cost + item["price"]
            <= budget
        ):

            selected.append(item)

            total_cost += item["price"]

            total_utility += item["utility"]

    return (
        selected,
        total_cost,
        total_utility
    )


# ============================================================
# 0/1 KNAPSACK ALGORITHM
# ============================================================

def knapsack_algorithm(items, budget):

    n = len(items)

    # Dynamic Programming table

    dp = [
        [0] * (budget + 1)
        for _ in range(n + 1)
    ]

    # Build DP table

    for i in range(1, n + 1):

        price = items[i - 1]["price"]

        utility = items[i - 1]["utility"]

        for current_budget in range(
            budget + 1
        ):

            if price <= current_budget:

                dp[i][current_budget] = max(

                    dp[i - 1][current_budget],

                    utility
                    + dp[
                        i - 1
                    ][
                        current_budget - price
                    ]
                )

            else:

                dp[i][current_budget] = (
                    dp[i - 1][current_budget]
                )


    # Find selected products

    selected = []

    current_budget = budget

    for i in range(
        n,
        0,
        -1
    ):

        if (
            dp[i][current_budget]
            !=
            dp[i - 1][current_budget]
        ):

            selected.append(
                items[i - 1]
            )

            current_budget -= (
                items[i - 1]["price"]
            )


    selected.reverse()


    # Calculate totals

    total_cost = sum(
        item["price"]
        for item in selected
    )

    total_utility = sum(
        item["utility"]
        for item in selected
    )

    return (
        selected,
        total_cost,
        total_utility
    )


# ============================================================
# OPTIMIZE BUTTON
# ============================================================

st.divider()

if st.button(
    "🚀 OPTIMIZE MY SHOPPING",
    use_container_width=True,
    key="optimize_button"
):

    # ========================================================
    # GREEDY
    # ========================================================

    (
        greedy_selected,
        greedy_cost,
        greedy_utility
    ) = greedy_algorithm(
        products,
        budget
    )


    # ========================================================
    # KNAPSACK
    # ========================================================

    (
        knapsack_selected,
        knapsack_cost,
        knapsack_utility
    ) = knapsack_algorithm(
        products,
        budget
    )


    # ========================================================
    # RESULT
    # ========================================================

    st.divider()

    st.markdown(
        '<div class="section-title">'
        '📊 Optimization Result'
        '</div>',
        unsafe_allow_html=True
    )

    st.write("")


    total_cost = knapsack_cost

    total_utility = knapsack_utility

    remaining_budget = (
        budget - total_cost
    )


    # ========================================================
    # METRICS
    # ========================================================

    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            "💰 Budget",
            f"₹{budget:,}"
        )


    with col2:

        st.metric(
            "💳 Total Cost",
            f"₹{total_cost:,}"
        )


    with col3:

        st.metric(
            "⭐ Total Utility",
            total_utility
        )


    with col4:

        st.metric(
            "💵 Remaining",
            f"₹{remaining_budget:,}"
        )


    # ========================================================
    # BUDGET UTILIZATION
    # ========================================================

    st.write("")

    if budget > 0:

        budget_used = (
            total_cost / budget
        ) * 100

        st.subheader(
            "📊 Budget Utilization"
        )

        st.progress(
            min(
                budget_used / 100,
                1.0
            )
        )

        st.write(
            f"**{budget_used:.1f}%** "
            "of your budget is being used."
        )


    # ========================================================
    # RECOMMENDED PRODUCTS
    # ========================================================

    st.subheader(
        "🛒 Recommended Shopping List"
    )


    if len(knapsack_selected) == 0:

        st.warning(
            "No products can be purchased within this budget."
        )

    else:

        for item in knapsack_selected:

            st.success(
                f"✓ {item['name']}  |  "
                f"₹{item['price']:,}  |  "
                f"Utility: {item['utility']}"
            )


    # ========================================================
    # ALGORITHM COMPARISON
    # ========================================================

    st.divider()

    st.markdown(
        '<div class="section-title">'
        '⚔️ Algorithm Comparison'
        '</div>',
        unsafe_allow_html=True
    )

    st.write("")


    col1, col2 = st.columns(2)


    # ========================================================
    # GREEDY RESULT
    # ========================================================

    with col1:

        st.markdown(
            '<div class="info-card">',
            unsafe_allow_html=True
        )

        st.subheader(
            "🟢 Greedy Algorithm"
        )

        st.write(
            f"**Total Cost:** "
            f"₹{greedy_cost:,}"
        )

        st.write(
            f"**Total Utility:** "
            f"{greedy_utility}"
        )

        st.write(
            f"**Remaining Budget:** "
            f"₹{budget - greedy_cost:,}"
        )

        st.write(
            "**Selected Products:**"
        )

        for item in greedy_selected:

            st.write(
                f"✓ {item['name']}"
            )

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )


    # ========================================================
    # KNAPSACK RESULT
    # ========================================================

    with col2:

        st.markdown(
            '<div class="info-card">',
            unsafe_allow_html=True
        )

        st.subheader(
            "🔵 0/1 Knapsack"
        )

        st.write(
            f"**Total Cost:** "
            f"₹{knapsack_cost:,}"
        )

        st.write(
            f"**Total Utility:** "
            f"{knapsack_utility}"
        )

        st.write(
            f"**Remaining Budget:** "
            f"₹{budget - knapsack_cost:,}"
        )

        st.write(
            "**Selected Products:**"
        )

        for item in knapsack_selected:

            st.write(
                f"✓ {item['name']}"
            )

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )


    # ========================================================
    # UTILITY COMPARISON
    # ========================================================

    st.divider()

    st.subheader(
        "📈 Utility Comparison"
    )

    utility_chart = {
        "Greedy": greedy_utility,
        "0/1 Knapsack": knapsack_utility
    }

    st.bar_chart(
        utility_chart
    )


    # ========================================================
    # COST COMPARISON
    # ========================================================

    st.subheader(
        "💰 Cost Comparison"
    )

    cost_chart = {
        "Greedy": greedy_cost,
        "0/1 Knapsack": knapsack_cost
    }

    st.bar_chart(
        cost_chart
    )


    # ========================================================
    # DECISION EXPLANATION
    # ========================================================

    st.subheader(
        "💡 Decision Explanation"
    )

    st.info(
        f"""
        The system evaluated **{len(products)} products**
        using a budget of **₹{budget:,}**.

        The **0/1 Knapsack algorithm** selected
        **{len(knapsack_selected)} products** with a total utility
        of **{knapsack_utility}** while spending
        **₹{knapsack_cost:,}**.

        The **Greedy algorithm** selected
        **{len(greedy_selected)} products** with a total utility
        of **{greedy_utility}**.

        The system compares both approaches to demonstrate how
        different algorithms solve the same budget-constrained
        optimization problem.
        """
    )


    # ========================================================
    # ALGORITHM EXPLANATION
    # ========================================================

    st.divider()

    st.subheader(
        "📚 How the Algorithms Work"
    )


    tab1, tab2, tab3 = st.tabs(
        [
            "🔵 0/1 Knapsack",
            "🟢 Greedy",
            "🔄 Sorting"
        ]
    )


    # ========================================================
    # KNAPSACK
    # ========================================================

    with tab1:

        st.markdown("""
        ### 0/1 Knapsack

        Each product has two choices:

        **1 → Select the product**

        **0 → Do not select the product**

        Dynamic Programming is used to find the combination
        that maximizes total utility without exceeding the
        available budget.

        **Time Complexity: O(n × B)**

        n = number of products

        B = available budget
        """)


    # ========================================================
    # GREEDY
    # ========================================================

    with tab2:

        st.markdown("""
        ### Greedy Algorithm

        The Greedy algorithm calculates:

        **Utility / Price**

        Products with a higher utility per rupee are considered
        first.

        The algorithm is simple and fast, but its result can
        differ from the 0/1 Knapsack solution because it makes
        decisions based on the current best ratio.
        """)


    # ========================================================
    # SORTING
    # ========================================================

    with tab3:

        st.markdown("""
        ### Sorting

        Products are ranked according to:

        **Utility / Price**

        Higher ratio = higher priority for the Greedy algorithm.

        Sorting makes the product selection process easier to
        understand.
        """)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown(
    '<div class="footer">'
    'Budget Shopping Optimizer | '
    'Python • Streamlit • Data Structures & Algorithms'
    '</div>',
    unsafe_allow_html=True
)