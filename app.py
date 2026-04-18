import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from wordcloud import WordCloud

# -------------------------------
# Load cleaned dataset
# -------------------------------
df = pd.read_csv("data/cleaned_poll_data.csv")

# -------------------------------
# Dashboard Title
# -------------------------------
st.title("📊 Poll Results Visualizer")
st.write("Analyze survey responses using interactive visualizations")

# -------------------------------
# Sidebar Filters
# -------------------------------
st.sidebar.header("Filter Responses")

selected_tools = st.sidebar.multiselect(
    "Select Preferred Tool(s):",
    options=df["Preferred Tool"].unique(),
    default=df["Preferred Tool"].unique()
)

filtered_df = df[df["Preferred Tool"].isin(selected_tools)]

# -------------------------------
# Show Raw Data
# -------------------------------
st.subheader("📄 Raw Data Preview")
st.dataframe(filtered_df)

# -------------------------------
# Bar Chart - Preferred Tool Votes
# -------------------------------
st.subheader("📌 Preferred Tool Votes")
tool_counts = filtered_df["Preferred Tool"].value_counts()
st.bar_chart(tool_counts)

# -------------------------------
# Satisfaction Rating Histogram
# -------------------------------
st.subheader("⭐ Satisfaction Ratings Distribution")

fig1, ax1 = plt.subplots(figsize=(8, 4))
sns.histplot(
    filtered_df["Satisfaction (1-5)"],
    bins=5,
    kde=True,
    color="skyblue",
    ax=ax1
)

ax1.set_xlabel("Satisfaction Rating")
ax1.set_ylabel("Frequency")
ax1.set_title("Distribution of Satisfaction Ratings")

st.pyplot(fig1)

# -------------------------------
# Average Satisfaction by Tool
# -------------------------------
st.subheader("📈 Average Satisfaction by Tool")

avg_satisfaction = filtered_df.groupby("Preferred Tool")["Satisfaction (1-5)"].mean()
st.bar_chart(avg_satisfaction)

# -------------------------------
# Word Cloud for Feedback
# -------------------------------
st.subheader("☁ Feedback Word Cloud")

feedback_text = " ".join(filtered_df["Feedback"].astype(str))

if feedback_text.strip():
    wordcloud = WordCloud(
        width=800,
        height=400,
        background_color="white"
    ).generate(feedback_text)

    fig2, ax2 = plt.subplots(figsize=(10, 5))
    ax2.imshow(wordcloud, interpolation="bilinear")
    ax2.axis("off")

    st.pyplot(fig2)
else:
    st.warning("No feedback text available for word cloud.")

# -------------------------------
# Summary Insights
# -------------------------------
st.subheader("📊 Summary Insights")

total_responses = len(filtered_df)
most_preferred = filtered_df["Preferred Tool"].value_counts().idxmax()
average_rating = filtered_df["Satisfaction (1-5)"].mean()

st.write(f"**Total Responses:** {total_responses}")
st.write(f"**Most Preferred Tool:** {most_preferred}")
st.write(f"**Average Satisfaction Rating:** {average_rating:.2f}")

# -------------------------------
# Footer
# -------------------------------
st.markdown("---")
st.write("Poll Results Visualizer Dashboard built with Streamlit")