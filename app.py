
import streamlit as st
import pandas as pd
from pathlib import Path 
data_file = Path("data") / "Table S1.xlsx"
df = pd.read_excel(data_file)
st.set_page_config(
    page_title="NanoQuest",
    page_icon="🧬",
    layout="wide"
)
st.sidebar.title("🧬 NanoQuest")
st.sidebar.caption("Nanomaterial Research Platform")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Overview",
        "🔬 Nanomaterial Dataset",
        "📊 Research Analytics",
        "📚 Literature Explorer",
        "⚖️ Material Comparison",
    ]
)

st.sidebar.divider()
st.sidebar.info("Research support prototype")
st.title("🧬 NanoQuest")
st.subheader("AI-Assisted Nanomaterial Research Platform")

st.write(
    "Explore published research on nanomaterials "
    "for antimicrobial applications."
)
st.markdown("""
<style>
.stApp {
    background-color: #0b1120;
    color: #e5edf7;
}
[data-testid="stMetric"] {
    background: #172337;
    border: 1px solid #263750;
    padding: 18px;
    border-radius: 12px;
}
h1, h2, h3 {
    color: #62e6c5;
}
</style>
""", unsafe_allow_html=True)

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Research Focus", "Nanomaterials")

with col2:
    st.metric("Application", "Antimicrobial")

with col3:
    st.metric("Platform Status", "Prototype")

st.subheader("🔬 Research Modules")

st.info(
    "Nanomaterial Explorer: Search and study published "
    "nanomaterial research."
)

st.info(
    "Research Analytics: Explore experimental data "
    "using charts and comparisons."
)

st.info(
    "Literature Explorer: Trace findings back to "
    "their original research sources."
)

st.caption(
    "NanoQuest | Research support prototype. "
    "Not intended for clinical decision-making."
)


if page == "🔬 Nanomaterial Dataset":
    st.header("Nanomaterial Research Dataset")

    if data_file.exists():
        df = pd.read_excel(data_file)
        st.success(f"Dataset loaded: {len(df)} rows")

        search = st.text_input("Search nanomaterial")

        if search:
            mask = df.astype(str).apply(
                lambda col: col.str.contains(
                    search, case=False, na=False
                )
            ).any(axis=1)
            st.dataframe(df[mask], width="stretch")
        else:
            st.dataframe(df.head(100), width="stretch")
    else:
        st.error("Table S1.xlsx not found in data folder.")

# Research Analytics
if page == "📊 Research Analytics":

    st.header("📊 Research Analytics")
    st.write("Explore patterns in nanomaterial research data.")

    # Interactive Research Filters
    st.subheader("🔎 Explore Research Data")

    col1, col2 = st.columns(2)

    with col1:
        materials = ["All"] + sorted(
            df["materials"].dropna().astype(str).unique().tolist()
        )
        selected_material = st.selectbox(
            "Select Nanomaterial", materials
        )

    with col2:
        strains = ["All"] + sorted(
            df["bacterial strain"].dropna().astype(str).unique().tolist()
        )
        selected_strain = st.selectbox(
            "Select Bacterial Strain", strains
        )

    filtered_df = df.copy()

    if selected_material != "All":
        filtered_df = filtered_df[
            filtered_df["materials"].astype(str) == selected_material
        ]

    if selected_strain != "All":
        filtered_df = filtered_df[
            filtered_df["bacterial strain"].astype(str) == selected_strain
        ]

    st.write(f"Matching records: {len(filtered_df)}")
    st.dataframe(filtered_df, width="stretch")

    # Summary Metrics
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Experiments", len(df))

    with col2:
        st.metric("Unique Materials", df["materials"].nunique())

    with col3:
        st.metric("Bacterial Strains", df["bacterial strain"].nunique())

    st.divider()

    # Chart 1: Material Distribution
    st.subheader("🧪 Top 10 Nanomaterials")

    material_counts = filtered_df["materials"].value_counts().head(10)
    st.bar_chart(material_counts)

    st.divider()

    # Chart 2: Particle Size
    st.subheader("📏 Nanomaterial Size Distribution")

    size_data = pd.to_numeric(filtered_df["size"], errors="coerce").dropna()

    if not size_data.empty:
        st.bar_chart(size_data.value_counts().sort_index())
    else:
        st.info("No numeric size data available.")

    st.divider()

    # Chart 3: Concentration
    st.subheader("🧫 Concentration Distribution")

    concentration_data = pd.to_numeric(
        filtered_df["concentration"], errors="coerce"
    ).dropna()

    if not concentration_data.empty:
        st.bar_chart(concentration_data.value_counts().sort_index())
    else:
        st.info("No numeric concentration data available.")

    st.divider()

    # Chart 4: MIC
    st.subheader("🔬 MIC Values")

    mic_data = pd.to_numeric(filtered_df["MIC"], errors="coerce").dropna()

    if not mic_data.empty:
        st.bar_chart(mic_data.value_counts().sort_index())
    else:
        st.info("No numeric MIC data available.")

    st.divider()

    # Chart 5: Bacterial Strains
    st.subheader("🦠 Research by Bacterial Strain")

    strain_counts = df["bacterial strain"].value_counts().head(10)
    st.bar_chart(strain_counts)
# Literature Explorer
if page == "📚 Literature Explorer":

    st.header("📚 Literature Explorer")
    st.write("Explore research references from the dataset.")

    search_doi = st.text_input("Search by DOI")

    literature_df = df[df["DOI"].notna()].copy()

    if search_doi:
        literature_df = literature_df[
            literature_df["DOI"].astype(str).str.contains(
                search_doi, case=False, na=False
            )
        ]

    st.write(f"Matching references: {len(literature_df)}")

    st.dataframe(
        literature_df[["materials", "bacterial strain", "DOI"]],
        width="stretch"
    )

# Material Comparison
if page == "⚖️ Material Comparison":

    st.header("⚖️ Nanomaterial Comparison")
    st.write(
        "Compare average recorded properties of two nanomaterials."
    )

    material_list = sorted(
        df["materials"].dropna().astype(str).unique().tolist()
    )

    if len(material_list) >= 2:

        col1, col2 = st.columns(2)

        with col1:
            material_a = st.selectbox(
                "Select first material",
                material_list,
                key="material_a"
            )

        with col2:
            material_b = st.selectbox(
                "Select second material",
                material_list,
                index=1,
                key="material_b"
            )

        properties = [
            "size",
            "concentration",
            "MIC",
            "bandgap",
            "predicted formation energy",
            "standard electrode potential",
            "Fermi level"
        ]

        available = [
            col for col in properties if col in df.columns
        ]

        if material_a == material_b:
            st.warning("Please select two different materials.")

        else:
            rows_a = df[
                df["materials"].astype(str) == material_a
            ]
            rows_b = df[
                df["materials"].astype(str) == material_b
            ]

            comparison = []

            for prop in available:
                values_a = pd.to_numeric(
                    rows_a[prop], errors="coerce"
                ).dropna()

                values_b = pd.to_numeric(
                    rows_b[prop], errors="coerce"
                ).dropna()

                comparison.append({
                    "Property": prop,
                    material_a: round(values_a.mean(), 4)
                    if not values_a.empty else None,
                    material_b: round(values_b.mean(), 4)
                    if not values_b.empty else None
                })

            st.subheader("Average Property Comparison")
            st.caption(
                "Values are averages of available numeric records, "
                "not AI predictions."
            )
            st.dataframe(
                pd.DataFrame(comparison),
                width="stretch",
                hide_index=True
            )
            st.subheader("📊 Visual Comparison")

            chart_df = pd.DataFrame(comparison).set_index("Property")

            st.bar_chart(chart_df)
            st.write(f"Records for first material: {len(rows_a)}")
            st.write(f"Records for second material: {len(rows_b)}")

    else:
        st.info("At least two distinct materials are needed.")
