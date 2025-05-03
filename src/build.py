# build.py
import re

with open("your_script.py", "r") as f:
    code = f.read()

# Remove the machine lock block
clean_code = re.sub(
    r"# === MACHINE LOCK ===.*?# === END LOCK ===",
    "",
    code,
    flags=re.DOTALL
)

with open("dist/clean_version.py", "w") as f:
    f.write(clean_code)

print("✅ Clean version created in /dist")