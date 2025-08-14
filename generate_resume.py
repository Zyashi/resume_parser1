from fpdf import FPDF

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", "B", 16)

# Name
pdf.cell(0, 10, "John Doe", ln=True)

# Contact
pdf.set_font("Arial", "", 12)
pdf.cell(0, 10, "Email: johndoe@example.com", ln=True)
pdf.cell(0, 10, "Phone: +1 234 567 890", ln=True)
pdf.cell(0, 10, "", ln=True)

# Education
pdf.set_font("Arial", "B", 14)
pdf.cell(0, 10, "Education", ln=True)
pdf.set_font("Arial", "", 12)
pdf.multi_cell(0, 8, "B.Tech in Computer Science, XYZ University, 2021\nM.Tech in AI, ABC University, 2023")
pdf.cell(0, 10, "", ln=True)

# Skills
pdf.set_font("Arial", "B", 14)
pdf.cell(0, 10, "Skills", ln=True)
pdf.set_font("Arial", "", 12)
pdf.multi_cell(0, 8, "Python, Java, C++, SQL, HTML, CSS, JavaScript, Flask, Django")

# Experience
pdf.set_font("Arial", "B", 14)
pdf.cell(0, 10, "Experience", ln=True)
pdf.set_font("Arial", "", 12)
pdf.multi_cell(0, 8, "Software Developer Intern at TechCorp (2022-2023)\nWorked on web applications using Flask and Django.")

# Save PDF
pdf.output("sample_resume.pdf")
print("Sample resume generated: sample_resume.pdf")
