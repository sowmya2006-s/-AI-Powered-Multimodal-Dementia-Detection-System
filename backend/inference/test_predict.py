from predict_voice import predict_mfcc
import os

# Create a dummy MFCC file for testing if one doesn't exist, or use a real one if available.
# Ideally we should use a real generated one.
# For now, let's look for one in the dataset folder to copy or valid path.

# Let's assume we want to test with a file. 
# We'll use a placeholder path, but the user verification step will likely involve a real file.
# I'll update this script to be robust.

def test():
    # Attempt to find a real sample file from the dataset we just built
    dataset_path = "../../datasets/voice_mfcc/dementia"
    sample_file = None
    if os.path.exists(dataset_path):
        files = os.listdir(dataset_path)
        if files:
            sample_file = os.path.join(dataset_path, files[0])
            print(f"Testing with actual sample: {sample_file}")

    if not sample_file:
        print("No sample file found in datasets. Please provide a path.")
        return

    try:
        prob = predict_mfcc(sample_file)

        print(f"Dementia Probability: {prob:.4f}")

        if prob < 0.4:
            print("Risk Level: LOW")
        elif prob < 0.7:
            print("Risk Level: MEDIUM")
        else:
            print("Risk Level: HIGH")
            
    except Exception as e:
        print(f"Test failed: {e}")

if __name__ == "__main__":
    test()
