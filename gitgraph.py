import os
import subprocess
import datetime
import json
import numpy as np
from PIL import Image, ImageDraw, ImageFont

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
LOG_FILE = "h4x0r_l0g.txt"
TRACKER_FILE = "commit_t1m3_tr4ck.json"
START_DATE = datetime.date.today() - datetime.timedelta(days=365)

print(BANNER)

# Ensure logs & tracker file are ignored by Git
subprocess.run(["git", "update-index", "--skip-worktree", LOG_FILE, TRACKER_FILE], check=False)

if os.path.exists(TRACKER_FILE):
    with open(TRACKER_FILE, "r") as f:
        committed_segments = set(json.load(f))
else:
    committed_segments = set()

def generate_letter_matrix(word):
    font = ImageFont.load_default()
    img_size = (len(word) * 6, 7)
    img = Image.new("1", img_size, 0)
    draw = ImageDraw.Draw(img)
    draw.text((0, 0), word.upper(), fill=1, font=font, encoding="utf-8")
    matrix = np.array(img)
    return [(x, y) for y in range(matrix.shape[0]) for x in range(matrix.shape[1]) if matrix[y, x] == 1]

word = input("0xDEADBEEF > Enter the payload (word): ").strip().upper()
letter_coords = generate_letter_matrix(word)

with open(LOG_FILE, "a") as log:
    log.write(f"0xBADCAFE | Bootstrapping '{word}' into the time machine...\n")

commit_count = len(committed_segments)

for x, y in letter_coords:
    commit_date = START_DATE + datetime.timedelta(weeks=x, days=y)
    segment_id = f"{x}-{y}"

    if segment_id in committed_segments:
        continue

    commit_message = f"0xB16B00B5 | Infiltrating '{word}' - Sector ({x}, {y})"
    filename = f"h4x_commit_{commit_count+1}.txt"

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

# Auto-fix potential push issues (fetch before pushing)
subprocess.run(["git", "fetch", "origin"], check=False)
subprocess.run(["git", "pull", "--rebase", "origin", "main"], check=False)
subprocess.run(["git", "push", "origin", "main"], check=True)

with open(LOG_FILE, "a") as log:
    log.write(f"0xC001CAFE | Mission complete! '{word}' now exists across spacetime.\n")

print(f"0xDEAD10CC | '{word}' has been deployed. Wait for GitHub to update the grid.")
