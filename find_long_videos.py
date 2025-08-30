import os
import cv2
from tqdm import tqdm

def get_video_duration(video_path):
    """
    Calculates the duration of a video in seconds using OpenCV.

    Args:
        video_path (str): The full path to the video file.

    Returns:
        float: The duration of the video in seconds, or 0.0 if unable to read.
    """
    try:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"Warning: Could not open video file {video_path}")
            return 0.0

        # Get total number of frames and frames per second (FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        
        # Release the video capture object
        cap.release()

        # Avoid division by zero
        if fps > 0:
            return total_frames / fps
        else:
            return 0.0
            
    except Exception as e:
        print(f"An error occurred with {video_path}: {e}")
        return 0.0

def main():
    """
    Main function to find and list videos longer than a set threshold.
    """
    # --- Configuration ---
    # IMPORTANT: Change this to the path of your PROCESSED video data folder
    root_dir = "Gen_preprocessed_data/NonViolence/default" 
    duration_threshold = 3.0 # seconds
    # --- End Configuration ---
    
    video_extensions = ('.mp4', '.avi', '.mov', '.mpg', '.mpeg', '.mkv', '.wmv')
    long_videos = []

    # --- Collect all video files first ---
    all_video_paths = []
    print(f"Scanning for videos in '{root_dir}'...")
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.lower().endswith(video_extensions):
                all_video_paths.append(os.path.join(subdir, file))

    if not all_video_paths:
        print("No video files found in the specified directory.")
        return

    # --- Process videos with a progress bar ---
    print(f"Checking durations for {len(all_video_paths)} videos...")
    for video_path in tqdm(all_video_paths, desc="Processing videos"):
        duration = get_video_duration(video_path)
        if duration > duration_threshold:
            long_videos.append((video_path, duration))

    # --- Print the results ---
    print("\n--- Scan Complete ---")
    if long_videos:
        print(f"Found {len(long_videos)} videos longer than {duration_threshold} seconds:")
        for path, dur in sorted(long_videos):
            print(f" - {path} ({dur:.2f}s)")
    else:
        print(f"No videos were found longer than {duration_threshold} seconds.")

if __name__ == "__main__":
    main()