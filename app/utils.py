import os

UPLOADS_DIR = os.path.join( "uploads")
RESULTS_DIR = os.path.join( "results")

os.makedirs(UPLOADS_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)



