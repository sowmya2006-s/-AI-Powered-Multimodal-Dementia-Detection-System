import timm
import torch
import threading
import time

def create_model():
    print("Starting model creation...")
    try:
        model = timm.create_model('swin_tiny_patch4_window7_224', pretrained=True)
        print("Success! Model created.")
    except Exception as e:
        print(f"Error: {e}")

thread = threading.Thread(target=create_model)
thread.start()
thread.join(timeout=30)

if thread.is_alive():
    print("TIMEOUT: Model creation hung for 30 seconds.")
else:
    print("Done.")
