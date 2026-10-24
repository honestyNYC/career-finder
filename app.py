import csv
import streamlit as st

st.set_page_config(page_title="Off the List")

# ---------- Load careers from the spreadsheet ----------
careers = []
with open("careers.csv", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        if row["tags"] == "":
            row["tags"] = []
        else:
            row["tags"] = row["tags"].split(";")
        row["keywords"] = row["keywords"].split(";")
        careers.append(row)

# Education levels, lowest to highest
career_levels = {
    "No diploma required": 0,
    "High school diploma or GED": 1,
    "Certificate (under 2 years)": 2,
    "Associate degree": 3,
    "Bachelor's degree": 4,
    "Master's degree": 5,
}
my_levels = {
    "Still in school": 0,
    "No diploma yet": 0,
    "GED or high school diploma": 1,
    "Certificate or trade program": 2,
    "Associate degree": 3,
    "Bachelor's degree": 4,
    "Master's or higher": 5,
}
all_needs = ["No degree required", "Paid training", "Remote-friendly",
             "Active work", "Start in under 2 years"]

# ---------- Home ----------
st.title("Off the List")
st.caption("CAREER DISCOVERY · Explore careers first. Job hunting comes later.")
st.write("Tell us who you are. We'll suggest paths that fit, explain why, and show how to start.")

text = st.text_area("1. Tell us about you",
                    placeholder="I love fixing things, I like being outside, and I want to help my community...")
my_ed = st.selectbox("2. What's your education so far?", list(my_levels),
                     index=None, placeholder="Choose one")
needs = st.multiselect("3. What do you need? (optional)", all_needs)

# ---------- Results ----------
if st.button("Find my careers →", type="primary"):
    typed = text.lower()

    # Count keyword matches for each area
    area_hits = {}
    for c in careers:
        area = c["area"]
        if area not in area_hits:
            hits = []
            for word in c["keywords"]:
                if word in typed:
                    hits.append(word)
            area_hits[area] = hits

    ranked = sorted(area_hits, key=lambda a: len(area_hits[a]), reverse=True)
    top = []
    for area in ranked:
        if len(area_hits[area]) > 0 and len(top) < 2:
            top.append(area)

    if len(top) == 0:
        st.warning("Write a little more about what you like, like fixing things, helping people, or being outside.")
    else:
        st.header("Career paths worth exploring")
        st.caption("These are paths to explore, not job openings.")

        for i, area in enumerate(top):
            st.subheader("Match #" + str(i + 1) + ": " + area)
            st.write("Because you mentioned: " + ", ".join(area_hits[area]))

            # Score each career in this area
            area_careers = []
            for c in careers:
                if c["area"] == area:
                    met = []
                    for need in needs:
                        if need in c["tags"]:
                            met.append(need)
                    can_start = False
                    if my_ed is not None:
                        can_start = career_levels[c["education_needed"]] <= my_levels[my_ed]
                    c["met"] = met
                    c["can_start"] = can_start
                    c["score"] = len(met)
                    if can_start:
                        c["score"] = c["score"] + 10
                    area_careers.append(c)

            area_careers.sort(key=lambda c: c["score"], reverse=True)

            for c in area_careers:
                with st.container(border=True):
                    st.markdown("#### " + c["title"])
                    st.write(c["one_liner"])

                    if c["median_pay"].startswith("[CHECK]"):
                        st.write("**Pay:** Varies (no official number yet)")
                    else:
                        st.write("**Pay:**", c["median_pay"].replace("$", "\\$"), "median per year")

                    if my_ed is None:
                        st.write("**Education needed:**", c["education_needed"])
                    elif c["can_start"]:
                        st.markdown(":green[**✓ You can start this with what you have**]")
                    else:
                        st.markdown(":orange[**You'd need first:** " + c["education_needed"] + "]")

                    if len(c["met"]) > 0:
                        st.markdown(":green[✓ " + " · ".join(c["met"]) + "]")

                    with st.expander("See full profile"):
                        st.write("**A normal workday:**", c["normal_day"])
                        st.write("**Education & training:**", c["training"])
                        st.write("**One challenge to consider:**", c["challenge"])
                        st.success("**Your first step:** " + c["first_step"])

st.divider()
st.caption("Pay is the U.S. median from the Bureau of Labor Statistics (May 2025). Check bls.gov/ooh for details.")
