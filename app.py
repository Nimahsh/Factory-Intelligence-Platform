
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

OEE_loc = BASE_DIR / "FirstSeason2026.xlsx"
address_code = BASE_DIR / "Code_map.xlsx"
address_code1 = BASE_DIR / "Kind_map.xlsx"

# ---------------- PRODUCT MAP ---------------- #
Product_map= {
    1116359 : { "line_name" : "Ocme 1" , "line_speed" : 100 , "Target_Pr" : 0.85,"name" : "1.35Kg Ladan" , "Weight" : 1350 , "Pack" : 8},
    1113143 : { "line_name" : "Ocme 1" , "line_speed" : 120 , "Target_Pr" : 0.85,"name" : "0.810Kg Ladan" , "Weight" : 810 , "Pack" : 12},
    1215357 : { "line_name" : "Ocme 1" , "line_speed" : 100 , "Target_Pr" : 0.85,"name" : "1.35Kg Almas" , "Weight" : 1350 , "Pack" : 8},
    1215141 : { "line_name" : "Ocme 1" , "line_speed" : 120 , "Target_Pr" : 0.85,"name" : "0.810Kg Almas" , "Weight" : 810 , "Pack" : 12},
    1116360 : { "line_name" : "Ocme 2" , "line_speed" : 170 , "Target_Pr" : 0.85,"name" : "1.35Kg Ladan" , "Weight" : 1350 , "Pack" : 8},
    1215296 : { "line_name" : "Ocme 2" , "line_speed" : 170 , "Target_Pr" : 0.85,"name" : "1.35Kg Frying" , "Weight" : 1350 , "Pack" : 8},
    1113478 : { "line_name" : "Ocme 3" , "line_speed" : 166 , "Target_Pr" : 0.72,"name" : "1.62Kg Ladan" , "Weight" : 1620 , "Pack" : 6},
    1215660 : { "line_name" : "Ocme 3" , "line_speed" : 166 , "Target_Pr" : 0.72,"name" : "1.62Kg Almas" , "Weight" : 1620 , "Pack" : 6},
    1215661 : { "line_name" : "Ocme 3" , "line_speed" : 166 , "Target_Pr" : 0.72,"name" : "1.62Kg Frying" , "Weight" : 1620 , "Pack" : 6},
    1118472 : { "line_name" : "Ocme 3" , "line_speed" : 166 , "Target_Pr" : 0.72,"name" : "1.62Kg Corn" , "Weight" : 1620 , "Pack" : 6},
    1113140 : { "line_name" : "Serac 2" , "line_speed" : 205 , "Target_Pr" : 0.85,"name": "0.810Kg Ladan", "Weight": 810, "Pack": 12},
    1215138 : { "line_name" : "Serac 2" , "line_speed" : 205 , "Target_Pr" : 0.85,"name": "0.810Kg Frying", "Weight": 810, "Pack": 12},
    1317072 : { "line_name" : "Serac 2" , "line_speed" : 240 , "Target_Pr" : 0.85,"name": "0.675Kg Nastaran", "Weight": 675, "Pack": 12},
    1113144 : { "line_name" : "Serac 2" , "line_speed" : 37 , "Target_Pr" : 0.85,"name" : "0.810Kg Ladan" , "Weight" : 810 , "Pack" : 12},
    1113142 : { "line_name" : "Serac 2" , "line_speed" : 37 , "Target_Pr" : 0.85,"name" : "0.810Kg Ladan" , "Weight" : 810 , "Pack" : 12},
    1113410 : { "line_name" : "Kosheshkaran" , "line_speed" : 37 , "Target_Pr" : 0.85,"name": "2.7Kg Ladan", "Weight": 2700, "Pack": 4},
    1215404 : { "line_name" : "Kosheshkaran" , "line_speed" : 37 , "Target_Pr" : 0.85,"name": "2.7Kg Almas", "Weight": 2700, "Pack": 4},
}

#--------------- Titles ----------------#
st.set_page_config(page_title="OEE Dashboard",layout="wide")
st.markdown("""
<div style='text-align:center;padding-bottom:20px;'>

<h1>
🏭 Manufacturing Intelligence Platform
</h1>

<p style='font-size:18px;color:#9ca3af'>
AI Powered Production Analytics
</p>

<p style='font-size:18px;color:#9ca3af'>
Data-Driven Management
</p>

</div>
""",
unsafe_allow_html=True)
st.divider()

def center_table(df):
    return (
        df.style
        .set_properties(**{'text-align': 'center'})
        .set_table_styles([
            {'selector': 'th',
             'props': [('text-align', 'center')]}
        ])
    )

# ---------------- LOAD DATA ---------------- #

@st.cache_data
def load_data(OEE_loc):
    return pd.read_excel(OEE_loc)

df = load_data(OEE_loc)
import jdatetime

def jalali_to_gregorian(x):

    x = str(int(x))

    year = int(x[:4])

    month = int(x[4:6])

    day = int(x[6:8])

    return jdatetime.date(
        year,
        month,
        day
    ).togregorian()

df["Date_Jalali"] = df["Date"].astype(str)

df["Date_Gregorian"] = df["Date_Jalali"].apply(jalali_to_gregorian)

df["Date_Gregorian"] = pd.to_datetime(df["Date_Gregorian"])

df["Line"] = df["Line"].astype(str)

df["Shift"] = df["Shift"].astype(str)
# -----------------------------------------------------------------------------
# ---------------- RAW DATA ---------------- #
# code_replace = {
#         1113140: 1113142,
#         1113144: 1113142
#     }

# ----------------Date FILTER ---------------- #

st.sidebar.subheader("Liquid Packaging Team")

st.sidebar.title("⚙️Filters")
period = st.sidebar.selectbox(

    "📅 Time Period",

    [

        "Last Day",

        "Last 7 Days",

        "Last Month",

        "Last Quarter",

        "Custom"

    ]

)
all_lines = ["All"] + sorted(df["Line"].unique())

Selected_line = st.sidebar.selectbox(

    "🏭 Line",

    all_lines

)
all_shift = ["All"] + sorted(df["Shift"].unique())

Selected_shift = st.sidebar.selectbox(

    "🌙 Shift",

    all_shift
)

df["Product Name"] = df["Product Code"].map(

    lambda x: Product_map.get(x, {}).get("name", "Unknown")

)
all_products = [

    "All Products"

] + sorted(df["Product Name"].unique())

Selected_product = st.sidebar.selectbox(

    "📦 Product",

    all_products

)
today = df["Date_Gregorian"].max()
if period == "Last Day":

    start_date = today - pd.Timedelta(days=0)

    end_date = today

elif period == "Last 7 Days":

    start_date = today - pd.Timedelta(days=6)

    end_date = today

elif period == "Last Month":

    start_date = today - pd.Timedelta(days=30)

    end_date = today

elif period == "Last Quarter":

    start_date = today - pd.Timedelta(days=90)

    end_date = today

else:

    start_date = st.sidebar.date_input(
        "From",
        value=df["Date_Gregorian"].min(),
        min_value=df["Date_Gregorian"].min(),
        max_value=df["Date_Gregorian"].max()
    )

    end_date = st.sidebar.date_input(
        "To",
        value=df["Date_Gregorian"].max(),
        min_value=df["Date_Gregorian"].min(),
        max_value=df["Date_Gregorian"].max()
    )

df_filtered = df.copy()
df_filtered = df_filtered[(df_filtered["Date_Gregorian"] >= pd.to_datetime(start_date))&(df_filtered["Date_Gregorian"] <= pd.to_datetime(end_date))]
import jdatetime

start_j = jdatetime.date.fromgregorian(date=start_date)
end_j = jdatetime.date.fromgregorian(date=end_date)

col1,col2,col3,col4 = st.columns(4)

with col2:

    st.markdown(f"""
    ### 📅 From

    **{start_date.strftime("%d %b %Y")}**

    <span style='color:#22C55E;font-size:18px'>
    {start_j.strftime("%Y/%m/%d")}
    </span>

    """, unsafe_allow_html=True)

with col3:

    st.markdown(f"""
    ### 📅 To

    **{end_date.strftime("%d %b %Y")}**

    <span style='color:#22C55E;font-size:18px'>
    {end_j.strftime("%Y/%m/%d")}
    </span>

    """, unsafe_allow_html=True)
# st.write(df_filtered.shape)
if Selected_line != "All":
    df_filtered = df_filtered[df_filtered["Line"] == Selected_line]

if Selected_shift != "All":
    df_filtered = df_filtered[df_filtered["Shift"] == Selected_shift]

if Selected_product != "All Products":
    df_filtered = df_filtered[df_filtered["Product Name"] == Selected_product]
st.sidebar.divider()
st.sidebar.caption("Manufacturing Intelligence Platform")
st.sidebar.caption("Version 1.0")



# ---------------- ONLY IF ONE LINE SELECTED ---------------- #
code_replace = {
        1113140: 1113142,
        1113144: 1113142
    }
df_filtered["Product Code"] = (
        df_filtered["Product Code"]
        .replace(code_replace))


if Selected_line == "All":

    # st.dataframe(df_filtered , hide_index=True)
    # df_filtered = df_filtered[df_filtered["Product"] >= 0]
    # st.dataframe(df_filtered, hide_index=True)
    df_filtered ["Target Product"] = (df_filtered["Line Speed"] * df_filtered["Time"] * df_filtered["Product Code"].map(lambda x: Product_map[x]["Weight"]))/1000000
    df_filtered ["Production (Ton)"]= (df_filtered["Product"] * (df_filtered["Product Code"].map(lambda x: Product_map[x]["Weight"]))* (df_filtered["Product Code"].map(lambda x: Product_map[x]["Pack"])))/1000000
    # st.dataframe(df_filtered.round(2), hide_index=True)
    df_filtered_Pr = df_filtered.groupby("Line",as_index=False).agg(Total_Time = ("Time" , "sum") ,Total_Plan=("Plan" , "sum") ,Total_ChangePlan=("Change Plan" , "sum"),Total_Production_Ton=("Production (Ton)" , "sum"),Total_Target_Plan=("Target Product" , "sum"))
    # st.dataframe(df_filtered_Pr)
    df_filtered_Pr["Plan Coverage"]=(df_filtered_Pr["Total_Production_Ton"]/df_filtered_Pr["Total_Plan"])*100
    df_filtered_Pr["Pr%"] = (df_filtered_Pr["Total_Production_Ton"]/df_filtered_Pr["Total_Target_Plan"])*100

    st.subheader("🏭 Production Overview")
    st.dataframe(df_filtered_Pr.round(2), hide_index=True )

    best_line = df_filtered_Pr.loc[
        df_filtered_Pr["Pr%"].idxmax(),
        "Line"
    ]

    Lowest_Pr = df_filtered_Pr.loc[
        df_filtered_Pr["Pr%"].idxmin(),
        "Line"
    ]

    total_plan_coverage = (df_filtered_Pr["Total_Production_Ton"].sum()/df_filtered_Pr["Total_Plan"].sum())*100

    st.divider()
    k1, k2, k3, k4, k5 = st.columns(5)
    st.divider()
    k1.metric("Highest Pr", best_line)
    k2.metric("Lowest Pr", Lowest_Pr)
    k3.metric("Total Pr", f"{(df_filtered_Pr['Total_Production_Ton'].sum()/df_filtered_Pr['Total_Target_Plan'].sum())*100:.2f}%")
    k4.metric("Total Plan Coverage",f"{ total_plan_coverage:.2f}%")
    k5.metric("Total Production",f"{df_filtered_Pr['Total_Production_Ton'].sum():.2f}")

    st.subheader("🏆 Line Performance Ranking")
    fig = px.bar(
        df_filtered_Pr.sort_values("Pr%", ascending=False),
        x="Line",
        y="Pr%",
        color="Pr%",
        text="Pr%"
    )

    fig.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside",
        textfont_size=16)

    fig.update_layout(
        template="plotly_dark",
        height=450,
        yaxis_title="Performance (%)",
        xaxis_title="Line")
    st.plotly_chart(
        fig,
        use_container_width=True)

    st.divider()

    df_filtered_Pr["Share%"] = (
                                       df_filtered_Pr["Total_Production_Ton"]
                                       / df_filtered_Pr["Total_Production_Ton"].sum()
                               ) * 100
    st.subheader("📈 Plan Coverage Ranking")
    fig_plan = px.bar(
        df_filtered_Pr.sort_values("Plan Coverage", ascending=False),
        x="Line",
        y="Plan Coverage",
        color="Plan Coverage",
        text="Plan Coverage"
    )

    fig_plan.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside",
        textfont_size=16)

    fig_plan.update_layout(
        template="plotly_dark",
        height=450,
        yaxis_title="Plan Coverage (%)",
        xaxis_title="Line")

    st.plotly_chart(
        fig_plan,
        use_container_width=True
    )
    st.divider()

    df_filtered_Pr["Share%"] = (
                                       df_filtered_Pr["Total_Production_Ton"]
                                       / df_filtered_Pr["Total_Production_Ton"].sum()
                               ) * 100

    # st.dataframe(df_filtered_Pr)
    st.subheader("🏭­ Production Share By Line")

    fig_prod = px.bar(
        df_filtered_Pr.sort_values("Total_Production_Ton", ascending=False),
        x="Line",
        y="Total_Production_Ton",
        color="Total_Production_Ton",
        text="Total_Production_Ton",

    )

    fig_prod.update_traces(
        texttemplate="%{text:.1f}",
        textposition="outside",
        textfont_size=16,


    )


    fig_prod.update_layout(
        template="plotly_dark",
        height=450,
        yaxis_title="Production (Ton)",
        xaxis_title="Line")

    st.plotly_chart(
        fig_prod,
        use_container_width=True)

#--------------------------------------------------
    st.divider()
    st.subheader("🎯 Performance vs Plan Coverage")

    fig_scatter = px.scatter(

        df_filtered_Pr,

        x="Plan Coverage",

        y="Pr%",

        size="Total_Production_Ton",

        color="Line",

        text="Line",

        custom_data=[
            "Line",
            "Total_Production_Ton",
            "Total_Time",
            "Share%"
        ]

    )

    fig_scatter.update_traces(

        hovertemplate=

        "<b>🏭­ %{customdata[0]}</b><br><br>"

        +

        "📈 Performance : %{y:.1f}%<br>"

        +

        "🎯 Plan Coverage : %{x:.1f}%<br>"

        +

        "📦 Production : %{customdata[1]:.1f} Ton<br>"

        +
        "📊 Share : %{customdata[3]:.1f}%<br>"

        +

        "⏱ Working Time : %{customdata[2]:.0f} min"

        +

        "<extra></extra>"

    )
    fig_scatter.update_traces(
            textposition="top center"
        )

    fig_scatter.update_layout(
            template="plotly_dark",
            height=600,
            xaxis_title="Plan Coverage (%)",
            yaxis_title="Performance (%)",
            hoverlabel = dict(

            bgcolor="#111827",

            bordercolor="#22C55E",

            font_size=17,

            font_family="Segoe UI",

            font_color="white"
            )
    )
    st.plotly_chart(
            fig_scatter,
            use_container_width=True
        )

# --------------------------------------Selected_line != "All" ---------------------------------------------------

if Selected_line != "All":

    Lines_df = df_filtered
    Lines_df["Target Ton"] = (Lines_df["Line Speed"]* Lines_df["Time"]* Lines_df["Product Code"].map(lambda x: Product_map[x]["Weight"])) / 1000000
    # st.subheader("Nima0")
    # st.dataframe(Lines_df)
    Line_Plan = Lines_df.groupby("Product Code", as_index=False).agg(Total_Production=("Product", "sum"),Working_Time=("Time", "sum"),Line_Speed=("Line Speed", "mean"),
        Total_Plan=("Plan", "sum"),
        Total_Chang_Plan=("Change Plan", "sum"),Total_Target_Plan=("Target Ton", "sum"),
    )

    # st.subheader("Nima1")
    # st.dataframe(Line_Plan)
    Line_Plan["Product Name"] = Line_Plan["Product Code"].map(lambda x: Product_map.get(x, {}).get("name", "Unknown Product"))

    Line_Plan["Production (Ton)"] = (Line_Plan["Total_Production"]*Line_Plan["Product Code"].map(lambda x: Product_map[x]["Weight"])* Line_Plan["Product Code"].map(lambda x: Product_map[x]["Pack"])) / 1_000_000

    Line_Plan["Plan Coverage"] =(Line_Plan["Production (Ton)"] / Line_Plan["Total_Plan"]) * 100
    # st.subheader("Nima2")
    # st.dataframe(Line_Plan)

    # ---------------- SHOW TABLE ---------------- #
    # ---------------- Average Speed Table ---------------- #

    Line_Plan["Pr%"] = (Line_Plan["Production (Ton)"] /(Line_Plan["Total_Target_Plan"])) * 100
    Line_Plan["Share%"] = (Line_Plan["Production (Ton)"] / Line_Plan["Production (Ton)"].sum())*100
    col1 = ["Product Name", "Working_Time", "Line_Speed", "Production (Ton)", "Plan Coverage" , "Pr%" , "Share%"]
    display_Line_Plan = Line_Plan[col1]

    st.subheader("Production Overview")

    st.markdown("This section presents an overview of the production performance for the selected reporting period. The analysis includes total production volume, production share by product, plan coverage, and operational performance (PR%) for each product category.")
    st.dataframe(display_Line_Plan[col1].round(1), hide_index=True)
    # st.subheader("Line_Plan Overview")
    # st.dataframe(Line_Plan.round(1), hide_index=True)

    Line_Plan["Effective Speed"] = (Line_Plan["Pr%"] / 100) * Line_Plan["Line_Speed"]

    Line_AvSpeed = Line_Plan[["Product Name", "Line_Speed", "Effective Speed"]].copy()

    Line_AvSpeed["Speed Loss(b/min)"]=(Line_AvSpeed["Effective Speed"]-(Line_AvSpeed["Line_Speed"]*Line_Plan["Product Code"].map(lambda x: Product_map[x]["Target_Pr"])))


    st.subheader("⚡Effective Speed")
    st.dataframe(Line_AvSpeed.round(1),use_container_width=True ,hide_index=True)

    Line_SpeedDi = Lines_df[Lines_df["Line Speed"] > 0]
    Line_SpeedDi = Line_SpeedDi[Line_SpeedDi["Product"] > 0]
    # st.dataframe(Line_SpeedDi.round(1), hide_index=True)
    colsSpeedDi = ["Date_Jalali"] + ["Product Code"] + ["Shift"] + ["Line Speed"] + ["Time"] + ["Product"]
    Line_SpeedDi = Line_SpeedDi[colsSpeedDi].copy()
    # st.dataframe(Line_SpeedDi.round(1), hide_index=True)
    Line_SpeedDi.rename(columns={"Product": "Bottle"}, inplace=True)
    Line_SpeedDi["Bottle"] = (Line_SpeedDi["Bottle"] * Line_SpeedDi["Product Code"].map(lambda x: Product_map[x]["Pack"])).round(2)
    Line_SpeedDi["Product Code"] = Line_SpeedDi["Product Code"].map(lambda x: Product_map[x]["name"])
    Line_SpeedDi.rename(columns={"Product Code": "Product Name"}, inplace=True)

    Line_Shift_in_Month = Line_SpeedDi["Shift"].count()


    Line_PR = (Line_Plan["Production (Ton)"].sum() / Line_Plan["Total_Target_Plan"].sum())* 100


    # ---------------- KPI ---------------- #
    total_ton = Line_Plan["Production (Ton)"].sum()
    total_plan = Line_Plan["Total_Plan"].sum()
    total_time = Line_Plan["Working_Time"].sum()
    plan_coverage = (total_ton / total_plan) * 100


    col1, col2, col3 ,col4 ,col5 , col6 = st.columns(6)
    col2.metric("Total Working Time", f"{total_time:.0f}")
    col3.metric("Production (Ton)", f"{total_ton:.1f}")
    col4.metric("Plan Coverage %", f"{plan_coverage:.1f}")
    col5.metric("Line Performance%", f"{Line_PR:.1f}")


    # ---------------- SHIFT Stability ---------------- #
    Line_SpeedDi["PR%"] = (Line_SpeedDi["Bottle"] / (Line_SpeedDi["Time"] * Line_SpeedDi["Line Speed"])) * 100

    Line_SpeedDi["Actual Speed"] = (Line_SpeedDi["PR%"]* Line_SpeedDi["Line Speed"]/ 100)
    # st.subheader("Actual Speed DataFrame - Line_SpeedDi")
    # st.dataframe(Line_SpeedDi.round(2), hide_index=True)

    Line_SpeedDi["Stability"] = np.where(
        (
            ((Line_SpeedDi["Line Speed"] == Line_SpeedDi["Line Speed"]) &
             (Line_SpeedDi["Actual Speed"] >= Line_SpeedDi["Line Speed"]*0.8))
        ) |
        (
            ((Line_SpeedDi["Line Speed"] == 166) &
             (Line_SpeedDi["Actual Speed"] >= Line_SpeedDi["Line Speed"]*0.67))
        )
        ,
        "Stable Shift",
        "Unstable Shift"
    )
    # st.subheader('Stability DataFrame - Line_SpeedDi', False)
    # st.dataframe(Line_SpeedDi.round(2), hide_index=True)


    Line_Stability = (
        Line_SpeedDi
        .groupby(["Product Name", "Stability"])
        .size()
        .unstack(fill_value=0)
        .reindex(columns=["Stable Shift", "Unstable Shift"], fill_value=0)
    )

    Line_Stability.columns.name = None
    Line_Stability["Total Shift"] = (Line_Stability["Stable Shift"] + Line_Stability["Unstable Shift"])

    Line_Stability["Stable Shift%"] = (Line_Stability["Stable Shift"]/Line_Stability["Total Shift"])*100

    Line_Stability["Unstable Shift%"] = (Line_Stability["Unstable Shift"]/Line_Stability["Total Shift"])*100

    Line_Stability = Line_Stability.reset_index()
    cols_stability = ["Product Name"] + ["Total Shift"] + ["Stable Shift"] + ["Unstable Shift"] + ["Stable Shift%"] + ["Unstable Shift%"]
    Line_Stability = Line_Stability[cols_stability]


    Line_Std = Line_SpeedDi.groupby("Product Name", as_index=False).agg(Av_Speed=("Actual Speed", "mean"),Standard_Deviation=("Actual Speed", "std"))
    Line_Std["%STD"] = (
                               Line_Std["Standard_Deviation"] /
                               Line_Std["Av_Speed"]
                       ) * 100

    Line_Std = Line_Std.dropna(subset=["%STD"])
    if Line_Std.empty:

        st.subheader("📈 Shift Stability Analysis")

        st.info("""
        ℹ️ Not enough observations to calculate speed variability.

        Please select **All Shifts** or a wider date range.
        """)

    else:
        col1 , col2 = st.columns(2)
        with col1:
            st.subheader("Shift Stability Analysis")
            st.markdown("")
            st.dataframe(Line_Stability.round(1), hide_index=True)

            st.subheader("Coefficient of variation (%STD)")
            st.markdown("Line speed variability was evaluated using the coefficient of variation (%STD)"
                    "to quantify speed fluctuations during production. Higher values indicate unstable operating behavior"
                    " and increased process variability, while lower values represent more consistent production performance."
                    " Note: %STD = Line speed fluctuation coefficient")
            st.dataframe(Line_Std.round(1),hide_index=True)

    # ---------------- STD CHART ---------------- #
        with col2:
            fig = go.Figure()
            fig.add_trace(
                go.Scatter(
                    x=Line_Std["Product Name"],
                    y=Line_Std["%STD"],
                    mode="lines+markers+text",
                    text=[f"{x:.1f}%" for x in Line_Std["%STD"]],
                    textposition="top center",
                    line=dict(width=4),
                    marker=dict(size=12),
                    name="Speed Variation"
                )
            )
            # Green Zone
            fig.add_hrect(
                y0=0,
                y1=10,
                fillcolor="green",
                opacity=0.15,
                line_width=0
            )
            # Warning Zone
            fig.add_hrect(
                y0=10,
                y1=20,
                fillcolor="yellow",
                opacity=0.12,
                line_width=0)
            fig.add_hrect(
                y0=20,
                y1=50,
                fillcolor="red",
                opacity=0.12,
                line_width=0
            )
            fig.add_hline(
                y=30,
                line_dash="dash",
                annotation_text="Critical Limit"
            )
            fig.update_layout(
                title=f"Line Speed Variation Analysis - {Selected_line}",
                template="plotly",
                height=550,
                paper_bgcolor="#0B1120",
                plot_bgcolor="#111827",
                font=dict(
                    color="white",
                    size=16
                ),
                xaxis_title="Product Name",
                yaxis_title="Coefficient of Variation (%)",
                hovermode="x unified"
            )
            st.plotly_chart(fig, use_container_width=True)
            Line_Std = Line_Std.dropna(subset=["%STD"])
            if not Line_Std.empty:
                Lowest_Variation = Line_Std.loc[
                    Line_Std["%STD"].idxmax(),
                    "Product Name"
                ]
                worst_std = Line_Std["%STD"].max()
        st.warning(
            f"AI Insight: Highest speed variability detected in "
            f"{Lowest_Variation} ({worst_std:.1f}%). "
            f"This product shows the highest process instability and may require investigation."
        )
        Stable_percent = (Line_Stability["Stable Shift"].sum() / Line_Stability["Total Shift"].sum()) * 100
        best_product = Line_Plan.loc[Line_Plan["Pr%"].idxmax(),"Product Name"]
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("All Shifts",f"{Line_Shift_in_Month:.0f}")
        with col2:
            st.metric("Stable Shifts",f"{Stable_percent.round(1)}")
        with col3:
            st.metric("Stable Product",f"{Line_Std.loc[Line_Std["%STD"].idxmin(),"Product Name"]}")
        with col4:
            st.metric("Best Performance",f"{best_product}")


df_stoppage = pd.read_excel(address_code)
stoppage_map = {
    row["Code"]: {
        "Kind": row["Kind"],
        "Machine": row["Machine"],
        "Issue": row["Issue"],
        "Type": row["Type"]
    }
    for _, row in df_stoppage.iterrows()
}
if Selected_line != "All":
    df_kind = pd.read_excel(address_code1)
    Kind_map = {
        row["Stoppage Kind"]: {
            "Stop": row["Stop"],}
        for _, row in df_kind.iterrows()}
    # st.subheader("Line_df - DataFrame")
    # st.dataframe(Lines_df , hide_index=True)
    Line_Stoppages = Lines_df.groupby("Code", as_index=False).agg(Stoppage_Minute=("Minute", "sum"),Stoppage_Count=("Count", "sum")).sort_values(by="Stoppage_Minute", ascending=False)
    Line_Stoppages["Symbol of Stoppages"] = Line_Stoppages["Code"].map(lambda x: stoppage_map[x]["Kind"])
    Line_Stoppages["Reason"] = Line_Stoppages["Code"].map(lambda x: stoppage_map[x]["Machine"])
    Line_Stoppages["Comment"] = Line_Stoppages["Code"].map(lambda x: stoppage_map[x]["Issue"])
    # Line_Stoppages["Type"] = Line_Stoppages["Code"].map(lambda x: stoppage_map[x]["Type"])
    Line_Stoppages["Classification"] = Line_Stoppages["Symbol of Stoppages"].map(lambda x: Kind_map[x]["Stop"])
    Ignored_codes = ["OET01", "OET02", "OET03", "OET04", "OET05", "OET06", "OET09", "OET10", "OET44", "OET45", "OET46"]
    Line_Stoppages = Line_Stoppages[~Line_Stoppages["Code"].isin(Ignored_codes)]
    # st.subheader("Line Stoppages - DataFrame")
    # st.dataframe(Line_Stoppages , hide_index=True)
    Line_Stoppages_Detail = Line_Stoppages.copy()

    # st.subheader("Line Stoppages - DataFrame - Classification Base")
    Line_Stoppages= Line_Stoppages.groupby("Classification", as_index=False).agg(Stoppage_Minute=("Stoppage_Minute", "sum")).sort_values(by="Stoppage_Minute", ascending=False)
    total_loss = Line_Stoppages["Stoppage_Minute"].sum()
    Line_Stoppages["Share%"] = (Line_Stoppages["Stoppage_Minute"]/total_loss) * 100
    st.subheader("Classification of Stoppages")
    st.dataframe(Line_Stoppages.round(1) , hide_index=True)
    total_loss = Line_Stoppages["Stoppage_Minute"].sum()

    # -----------------------------------------------------------------------------------------------------------------
    st.subheader("🏭Where Did We Lose Time?")
    

    colors = px.colors.qualitative.Plotly
    fig = go.Figure()
    for i, row in Line_Stoppages.reset_index(drop=True).iterrows():
        fig.add_trace(
            go.Bar(
            x=[row["Classification"]],
            y=[row["Stoppage_Minute"]],
            name=row["Classification"],
            text=[round(row["Stoppage_Minute"])],
            textposition="inside",
            marker_color=colors[i % len(colors)],
            width=0.75
            )
        )
        fig.update_layout(
            template="plotly_dark",
            height=400,
            barmode="overlay",
            bargap=0.15,
            showlegend=True,
            legend_title_text="Classification",
            xaxis_title="Classification",
            yaxis_title="Stoppage Minute",
            xaxis_tickangle=-25
        )
        st.plotly_chart(
            fig,
            use_container_width=True,
            key="classification_chart"
        )
        if len(Line_Stoppages) >= 2:
            top2 = Line_Stoppages.head(2)
            share = top2["Share%"].sum()
            st.success(
                f"""
                🤖  AI Insight: 
                Total stoppages time is equal to {total_loss.round(0)} minutes
                , {share:.1f}% of all losses originated from {top2.iloc[0]['Classification']} and {top2.iloc[1]['Classification']}.
                """)

    #----------------------------------------------------------------

        selected_class = st.selectbox("🔍 Explore Classification",Line_Stoppages["Classification"])

        detail_df = Line_Stoppages_Detail[Line_Stoppages_Detail["Classification"] == selected_class]

        st.subheader(f"Details of {selected_class}: ")

        # st.dataframe(detail_df.sort_values("Stoppage_Minute",ascending=False),hide_index=True)

        reason_df = (detail_df.groupby("Reason", as_index=False).agg(Minute=("Stoppage_Minute", "sum")).sort_values( "Minute",ascending=False))

        fig2 = px.bar(
            reason_df,

            y="Reason",
            x="Minute",

            orientation="h",

            text="Minute",

            color="Minute"
        )

        fig2.update_layout(
            template="plotly_dark",
            height=400,
            showlegend=False
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

        top_reason = reason_df.iloc[0]

        share_reason = (top_reason["Minute"]/reason_df["Minute"].sum())*100

        st.info(
            f"""
        🤖 AI Insight
    
        Inside {selected_class},
    
        {top_reason['Reason']} is the dominant source of downtime.
    
        Impact:
        {share_reason:.1f}% of all losses in this category.
    
        Recommended focus:
        Investigate this issue first.
        """
        )

        with st.expander("📋 View Raw Stoppage Data"):

            st.dataframe(detail_df.sort_values("Stoppage_Minute",ascending=False),hide_index=True)

        
        equipment_df = (
            Line_Stoppages_Detail
            .groupby("Reason", as_index=False)
            .agg(Stoppage_Minute=("Stoppage_Minute", "sum"))
            .sort_values("Stoppage_Minute", ascending=False)
        )

        st.subheader("🏭 Which Reason Hurt Us Most?")
        equipment_df = (
            Line_Stoppages_Detail
            .groupby("Reason", as_index=False)
            .agg(Stoppage_Minute=("Stoppage_Minute", "sum"))
            .sort_values("Stoppage_Minute", ascending=False)
        )
        colors = px.colors.qualitative.Plotly
        fig = go.Figure()
        for i, row in equipment_df.reset_index(drop=True).iterrows():
            fig.add_trace(
                go.Bar(
                    x=[row["Reason"]],
                    y=[row["Stoppage_Minute"]],
                    name=row["Reason"],
                    text=[round(row["Stoppage_Minute"])],
                    textposition="inside",
                    marker_color=colors[i % len(colors)],
                    width=0.75
                )
            )
            fig.update_layout(
                template="plotly_dark",
                height=430,
                barmode="overlay",bargap=0.15,
                showlegend=True,
                legend_title_text="Reason",
                xaxis_title="Reason",
                yaxis_title="Stoppage Minute",
                xaxis_tickangle=-35
            )
            st.plotly_chart(
                fig,
                use_container_width=True,
                key="equipment_reason_chart"
            )
            selected_machine = st.selectbox(
                "🔍 Explore Equipment",
                equipment_df["Reason"]
            )
            machine_detail = Line_Stoppages_Detail[
            Line_Stoppages_Detail["Reason"] == selected_machine
            ]
            machine_loss = (
                machine_detail
                .groupby("Classification", as_index=False)
                .agg(Minute=("Stoppage_Minute", "sum"))
                .sort_values("Minute", ascending=False)
            )
            fig2 = px.bar(
                machine_loss,
                y="Classification",
                x="Minute",
                orientation="h",
                text="Minute",
                color="Minute"
            )
            fig2.update_layout(
                template="plotly_dark",
                height=400,
                showlegend=False
            )
            st.plotly_chart(
                fig2,
                use_container_width=True
            )
            with st.expander("📋 View Raw Stoppage Data"):
                st.dataframe(machine_detail.sort_values("Stoppage_Minute",ascending=False),hide_index=True)
