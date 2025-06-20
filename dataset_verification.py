import pandas as pd
from pydub import AudioSegment
from pydub.playback import play

# Config
metadata_file = '/Users/jamesshortland/PycharmProjects/Masters_Final/freesound_dataset/metadata.csv'
folder_path = '/Users/jamesshortland/PycharmProjects/Masters_Final/freesound_dataset/'
batch_size = 50

# Load data
df = pd.read_csv(metadata_file)

# Filter unverified clips
unverified_df = df[df['verified'].astype(str) == 'False']
total_batches = (len(unverified_df) + batch_size - 1) // batch_size

print(f"\nTotal unverified clips: {len(unverified_df)}")
print(f"Processing in {total_batches} batches of {batch_size} clips each.\n")

# Main loop
for batch_num in range(total_batches):
    batch_start = batch_num * batch_size
    batch_end = min(batch_start + batch_size, len(unverified_df))
    print(f"\n=== Batch {batch_num + 1}/{total_batches} === Clips {batch_start + 1} to {batch_end}")

    batch_df = unverified_df.iloc[batch_start:batch_end]

    for idx, row in batch_df.iterrows():
        clip_filename = row['filepath']
        label = row['label']
        clip_full_path = folder_path + label + '/' + clip_filename

        print(f"\nClip: {clip_full_path} | Label: {label}")

        try:
            sound = AudioSegment.from_file(clip_full_path)
            play(sound)
        except Exception as e:
            print(f"Error playing clip: {e}")
            continue

        verified = input("Is this correct? (Y/N): ").strip().lower()

        # Update the original df using the filename (not full path!)
        df.loc[df['filepath'] == clip_filename, 'verified'] = 'True' if verified == 'y' else 'No Match'

    # Save progress
    df.to_csv(metadata_file, index=False)
    print(f"\nBatch {batch_num + 1} complete. Progress saved.")

    # Ask if user wants to continue
    cont = input("\nContinue to next batch? (Y/N): ").strip().lower()
    if cont != 'y':
        print("Stopping verification. You can resume later.")
        break

print("\n Verification complete. Well done!")
