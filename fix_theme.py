import os

# Define the folder and file path
folder = ".streamlit"
file_path = os.path.join(folder, "config.toml")

# The content that forces the Dark Teal Theme
config_content = """
[theme]
base="dark"
primaryColor="#00C9A7"
backgroundColor="#0E1117"
secondaryBackgroundColor="#262730"
textColor="#FAFAFA"
font="sans serif"
"""

# Create the folder if it doesn't exist
if not os.path.exists(folder):
    os.makedirs(folder)
    print(f"Created folder: {folder}")

# Write the file
with open(file_path, "w") as f:
    f.write(config_content)
    print(f"Created file: {file_path}")
    print("SUCCESS! Your theme is now forced to Dark Mode.")