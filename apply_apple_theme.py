import os

folder = ".streamlit"
file_path = os.path.join(folder, "config.toml")

# The "Cupertino Dark" Palette
# Base: Pure Black
# Cards: Dark Grey (#1c1c1e is Apple's standard secondary background)
# Primary: iOS Blue (#0A84FF)
config_content = """
[theme]
base="dark"
primaryColor="#0A84FF"
backgroundColor="#000000"
secondaryBackgroundColor="#1c1c1e"
textColor="#FFFFFF"
font="sans serif"
"""

if not os.path.exists(folder):
    os.makedirs(folder)

with open(file_path, "w") as f:
    f.write(config_content)
    print("✅ Apple-style theme applied!")