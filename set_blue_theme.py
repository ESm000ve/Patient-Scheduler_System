import os

folder = ".streamlit"
file_path = os.path.join(folder, "config.toml")

# We set primaryColor to Electric Blue (#0099FF)
# This changes the Progress Bar and Focus highlights automatically
config_content = """
[theme]
base="dark"
primaryColor="#0099FF"
backgroundColor="#000000"
secondaryBackgroundColor="#1A1A1A"
textColor="#FFFFFF"
font="sans serif"
"""

if not os.path.exists(folder):
    os.makedirs(folder)

with open(file_path, "w") as f:
    f.write(config_content)
    print("✅ Theme synced to Electric Blue!")