import os
import subprocess
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

def process_video(video_path, class_name, output_dir):
    """
    Processes a single video file by converting it to a standard format.
    """
    filename = os.path.basename(video_path)
    filename_no_ext = os.path.splitext(filename)[0]
    
    output_class_dir = os.path.join(output_dir, class_name)
    os.makedirs(output_class_dir, exist_ok=True)
    output_path = os.path.join(output_class_dir, f"{filename_no_ext}.mp4")

    # The FFmpeg command to be executed
    command = [
        'ffmpeg',
        '-i', video_path,
        # <<< MODIFIED LINE >>>
        # This new scale filter ensures the output width is always an even number.
        '-vf', "fps=30,scale='trunc(oh*a/2)*2':480",
        # <<< END MODIFICATION >>>
        '-c:v', 'libx264',
        '-an',
        '-y', 
        '-loglevel', 'error',
        output_path
    ]
    
    try:
        subprocess.run(command, check=True)
        return (output_path, True)
    except subprocess.CalledProcessError as e:
        print(f"Error processing {video_path}: {e}")
        return (output_path, False)

# The 'main' function remains exactly the same.
def main():
    # ... (no changes needed in the main function) ...
    # --- Configuration ---
    data_dir = "/Users/asthaparekh/MinorProject/dataset/punch"
    output_dir = "/Users/asthaparekh/MinorProject/Gen_preprocessed_data/Punch"
    max_workers = os.cpu_count()
    # --- End Configuration ---
    
    os.makedirs(output_dir, exist_ok=True)
    tasks = []
    print("Scanning for video files to standardize...")
    video_extensions = ('.mp4', '.avi', '.mov', '.mpg', '.mpeg', '.mkv', '.wmv')

    # Since you have a nested structure, let's adjust the scanner
    for root, dirs, files in os.walk(data_dir):
        for filename in files:
            if filename.lower().endswith(video_extensions):
                video_path = os.path.join(root, filename)
                # Determine class_name from the directory structure
                # This part might need adjustment based on your exact folder layout
                relative_path = os.path.relpath(root, data_dir)
                class_name = relative_path.split(os.sep)[0] if relative_path != '.' else 'default'
                tasks.append((video_path, class_name, output_dir))
    
    if not tasks:
        print("No video files found to process. Check your `data_dir` path.")
        return

    print(f"Found {len(tasks)} videos to standardize. Starting conversion...")
    successful_conversions = 0
    failed_conversions = 0
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(process_video, *task) for task in tasks]
        pbar = tqdm(as_completed(futures), total=len(tasks), desc="Standardizing Videos")
        for future in pbar:
            _, success = future.result()
            if success:
                successful_conversions += 1
            else:
                failed_conversions += 1

    print("\n--- Standardization Complete ---")
    print(f"Successfully converted: {successful_conversions}")
    print(f"Failed conversions: {failed_conversions}")
    print(f"Standardized dataset is ready in: {output_dir}")

if __name__ == '__main__':
    main()