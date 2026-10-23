import streamlit as st

careers = {
    "People & Care": [
        {"title": "Medical Assistant",
         "what": "Helps doctors with patients: vitals, scheduling, records.",
         "pay": "$40k–$50k",
         "start": "6–12 month certificate program"},
        {"title": "Social Worker",
         "what": "Connects people and families with support and resources.",
         "pay": "$50k–$65k",
         "start": "Bachelor's in social work (BSW)"},
    ],
    "Business & Money": [
        {"title": "Real Estate Agent",
         "what": "Helps people buy, sell, and rent homes.",
         "pay": "$40k–$100k+ (commission)",
         "start": "State license course and exam"},
        {"title": "Bookkeeper",
         "what": "Tracks a business's money coming in and going out.",
         "pay": "$40k–$55k",
         "start": "Certificate or on-the-job training"},
    ],
    "Tech & Data": [
        {"title": "IT Support Specialist",
         "what": "Fixes computer and network problems for people.",
         "pay": "$45k–$65k",
         "start": "CompTIA A+ certification"},
        {"title": "Data Analyst",
         "what": "Turns data into answers that help businesses decide.",
         "pay": "$65k–$100k",
         "start": "Learn Excel, SQL, and Python"},
    ],
    "Creative": [
        {"title": "Graphic Designer",
         "what": "Creates logos, ads, and social media visuals.",
         "pay": "$45k–$70k",
         "start": "Build a portfolio; learn Canva or Adobe"},
        {"title": "Video Editor",
         "what": "Cuts and polishes videos for creators and brands.",
         "pay": "$45k–$75k",
         "start": "Learn Premiere or CapCut; post your work"},
    ],
    "Hands-On & Trades": [
        {"title": "Electrician",
         "what": "Installs and repairs wiring in homes and buildings.",
         "pay": "$50k–$90k",
         "start": "Paid apprenticeship"},
        {"title": "HVAC Technician",
         "what": "Installs and fixes heating and cooling systems.",
         "pay": "$45k–$70k",
         "start": "Trade school or apprenticeship"},
    ],
}

questions = [
    ["Do you like helping or taking care of people?", ["People & Care"]],
    ["Do you enjoy working with numbers or money?", ["Business & Money", "Tech & Data"]],
    ["Do you like drawing, writing, or making videos?", ["Creative"]],
    ["Do you like fixing or building things with your hands?", ["Hands-On & Trades"]],
    ["Would you enjoy convincing people or making deals?", ["Business & Money"]],
    ["Do you like solving puzzles or figuring out how things work?", ["Tech & Data"]],
    ["Do you prefer being active over sitting at a desk all day?", ["Hands-On & Trades", "People & Care"]],
    ["Do you like coming up with new ideas?", ["Creative", "Business & Money"]],
]

st.title("Career Finder")
st.write("Answer each question to see which careers fit you.")

answers = []
for i in range(len(questions)):
    choice = st.radio(questions[i][0], ["Yes", "Maybe", "No"],
                      index=None, horizontal=True, key=i)
    answers.append(choice)

if st.button("See my results"):
    if None in answers:
        st.warning("Answer every question first!")
    else:
        scores = {"People & Care": 0, "Business & Money": 0, "Tech & Data": 0,
                  "Creative": 0, "Hands-On & Trades": 0}
        points_for = {"Yes": 2, "Maybe": 1, "No": 0}

        for i in range(len(questions)):
            points = points_for[answers[i]]
            for c in questions[i][1]:
                scores[c] += points

        ranked = sorted(scores, key=scores.get, reverse=True)
        cutoff = scores[ranked[1]]
        top = []
        for cat in ranked:
            if scores[cat] >= cutoff and scores[cat] > 0:
                top.append(cat)

        if len(top) == 0:
            st.info("No matches yet. Try answering yes to a few!")
        else:
            for i, cat in enumerate(top):
                st.header("Match #" + str(i + 1) + ": " + cat +
                          " (" + str(scores[cat]) + " points)")
                for job in careers[cat]:
                    st.subheader(job["title"])
                    st.write("**What you do:**", job["what"])
                    st.write("**Pay:**", job["pay"])
                    st.write("**How to start:**", job["start"])
