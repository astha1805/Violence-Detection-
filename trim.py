import os
import subprocess
import glob

def trim_videos(input_dir="non_violence", output_dir="non_violence_4s", clip_duration=4):
    """
    Trims all videos in a directory to a specified duration using FFmpeg.

    Args:
        input_dir (str): The folder containing the original videos.
        output_dir (str): The folder where the trimmed videos will be saved.
        clip_duration (int): The desired duration of the clips in seconds.
    """
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}")

    # Define the video extensions to look for
    video_extensions = ["*.mp4", "*.avi", "*.mov", "*.mkv"]
    
    # Get a list of all video files in the input directory
    video_files = []
    for ext in video_extensions:
        video_files.extend(glob.glob(os.path.join(input_dir, ext)))

    if not video_files:
        print(f"No video files found in '{input_dir}'. Please check the path.")
        return

    print(f"Found {len(video_files)} videos to process...")

    # Loop through each video file
    for infile in video_files:
        base_filename = os.path.basename(infile)
        outfile = os.path.join(output_dir, base_filename)
        
        print(f"Clipping '{infile}' to {clip_duration} seconds -> '{outfile}'")
        
        # Construct the FFmpeg command as a list of arguments
        command = [
            'ffmpeg',
            '-i', infile,          # Input file
            '-ss', '00:00:00',     # Start time
            '-t', str(clip_duration), # Duration to clip
            outfile,               # Output file
            '-y'                   # Overwrite output file if it exists
        ]
        
        # Execute the command
        try:
            # We use DEVNULL to hide the verbose FFmpeg output
            subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError as e:
            print(f"!!! Failed to process {infile}. FFmpeg might have encountered an error: {e}")
        except FileNotFoundError:
            print("!!! FFmpeg not found. Please make sure it's installed and in your system's PATH.")
            return

    print(f"\nClipping complete! Check the '{output_dir}' folder.")

if __name__ == '__main__':
    # --- Configuration ---
    INPUT_FOLDER = "Gen_preprocessed_data/NonViolence/default"
    OUTPUT_FOLDER = "Gen_preprocessed_data/NonViolence_trimmed"
    DURATION_SECONDS = 4
    # ---------------------
    
    trim_videos(input_dir=INPUT_FOLDER, output_dir=OUTPUT_FOLDER, clip_duration=DURATION_SECONDS)