import io
import pandas as pd

def generate_sample_excel(template_type: str) -> io.BytesIO:
    """
    Generates sample Excel file in memory for internal, external, co, or po templates.
    """
    template_type = template_type.lower()
    
    if template_type == "internal":
        data = {
            "Roll No": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            "Marks": [34, 27, 42, 18, 45, 39, 48, 22, 30, 41]
        }
    elif template_type == "external":
        data = {
            "Roll No": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            "Marks": [56, 61, 72, 49, 85, 68, 91, 52, 64, 78]
        }
    elif template_type == "co":
        data = {
            "CO Number": ["CO1", "CO2", "CO3", "CO4"],
            "Statement": [
                "Understand core programming concepts and object-oriented paradigms",
                "Design and develop structured database applications using SQL",
                "Apply modern web development tools and RESTful API architectures",
                "Analyze and optimize algorithmic performance and software efficiency"
            ]
        }
    elif template_type == "po":
        data = {
            "PO Number": ["PO1", "PO2", "PO3", "PO4"],
            "Statement": [
                "Engineering Knowledge: Apply knowledge of mathematics and computer science fundamentals",
                "Problem Analysis: Identify, formulate, and analyze complex engineering problems",
                "Modern Tool Usage: Create, select, and apply appropriate IT techniques and resources",
                "Communication Skills: Communicate effectively on complex engineering activities"
            ]
        }
    else:
        raise ValueError(f"Unknown template type '{template_type}'. Must be one of: internal, external, co, po.")

    df = pd.DataFrame(data)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="SampleData")
    
    output.seek(0)
    return output
