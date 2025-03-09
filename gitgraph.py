import os
import subprocess
import datetime
import json
import pyfiglet
import numpy as np
import matplotlib.pyplot as plt

BANNER = r"""
      ▗▄▄▖▄    ■             
     ▐▌   ▄ ▗▄▟▙▄▖           
     ▐▌▝▜▌█   ▐▌             
     ▝▚▄▞▘█   ▐▌             
              ▐▌             
                             
                             
 ▗▄▄▖ ▄▄▄ ▗▞▀▜▌▄▄▄▄  ▐▌      
▐▌   █    ▝▚▄▟▌█   █ ▐▌      
▐▌▝▜▌█         █▄▄▄▀ ▐▛▀▚▖   
▝▚▄▞▘          █     ▐▌ ▐▌   
               ▀             
                             
                             
 ▗▄▄▖█ ▄   ▄ ▄▄▄▄  ▐▌    ▄▄▄ 
▐▌   █ █   █ █   █ ▐▌   ▀▄▄  
▐▌▝▜▌█  ▀▀▀█ █▄▄▄▀ ▐▛▀▚▖▄▄▄▀ 
▝▚▄▞▘█ ▄   █ █     ▐▌ ▐▌     
        ▀▀▀  ▀            
"""

REPO_DIR = os.getcwd()
COMMIT_DIR = os.path.join(REPO_DIR, "h4x_commits")
LOG_FILE = "h4x0r_l0g.txt"
TRACKER_FILE = "commit_t1m3_tr4ck.json"
START_DATE = datetime.date.today() - datetime.timedelta(days=365)

print(BANNER)

if not os.path.exists(COMMIT_DIR):
    os.mkdir(COMMIT_DIR)

subprocess.run(["git", "update-index", "--assume-unchanged", LOG_FILE], check=False)

if os.path.exists(TRACKER_FILE):
    with open(TRACKER_FILE, "r") as f:
        committed_segments = set(json.load(f))
else:
    committed_segments = set()

def generate_commit_map(word):
    figlet_text = pyfiglet.Figlet(font="banner").renderText(word)
    lines = figlet_text.split("\n")

    commit_coords = []
    for y, line in enumerate(lines[:7]):  # Limit to 7 lines (GitHub's grid height)
        for x, char in enumerate(line[:52]):  # Limit to 52 weeks (GitHub's grid width)
            if char == "#":  # '#' in figlet output marks a commit
                commit_coords.append((x, y))

    return commit_coords

word = input("0xDEADBEEF > Enter the payload (word): ").strip().upper()
letter_coords = generate_commit_map(word)

# Show ASCII preview
figlet_preview = pyfiglet.Figlet(font="banner").renderText(word)
print(figlet_preview)

# Show GitHub commit preview as a scatter plot
fig, ax = plt.subplots(figsize=(10, 2))
ax.set_xlim(-1, 52)
ax.set_ylim(-1, 7)

for x, y in letter_coords:
    ax.scatter(x, y, color='green', s=100)

ax.set_xticks([])
ax.set_yticks([])
ax.set_frame_on(False)
plt.show()

# Ask for confirmation before committing
confirm = input("\n0xBADCAFE | Does this look correct? Type 'hack' to proceed: ").strip().lower()
if confirm != "hack":
    print("\n0xC001CAFE | Mission aborted. No changes committed.")
    exit()

with open(LOG_FILE, "a") as log:
    log.write(f"0xBADCAFE | Bootstrapping '{word}' into the time machine...\n")

commit_count = len(committed_segments)

for x, y in letter_coords:
    commit_date = START_DATE + datetime.timedelta(weeks=x, days=y)
    segment_id = f"{x}-{y}"

    if segment_id in committed_segments:
        continue

    commit_message = f"0xB16B00B5 | Infiltrating '{word}' - Sector ({x}, {y})"
    filename = os.path.join(COMMIT_DIR, f"h4x_commit_{commit_count+1}.txt")

    with open(filename, "w") as f:
        f.write(f"0xFEEDFACE | Payload drop '{word}' @ ({x}, {y})\n")

    subprocess.run(["git", "add", filename], check=True)
    subprocess.run(
        ["git", "commit", "-m", commit_message, "--date", commit_date.strftime("%Y-%m-%dT12:00:00")],
        check=True
    )

    with open(LOG_FILE, "a") as log:
        log.write(f"{commit_message} -> Time-travel commit on {commit_date}\n")

    committed_segments.add(segment_id)
    with open(TRACKER_FILE, "w") as f:
        json.dump(list(committed_segments), f)

    commit_count += 1

subprocess.run(["git", "fetch", "origin"], check=False)
subprocess.run(["git", "pull", "--rebase", "origin", "main"], check=False)
subprocess.run(["git", "push", "origin", "main"], check=True)

with open(LOG_FILE, "a") as log:
    log.write(f"0xC001CAFE | Mission complete! '{word}' now exists across spacetime.\n")

print(f"0xDEAD10CC | '{word}' has been deployed. Wait for GitHub to update the grid.")
