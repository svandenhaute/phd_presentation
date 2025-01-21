import cv2
import os

def extract_frames(video_path, output_folder):
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Open the video file
    video = cv2.VideoCapture(video_path)
    
    # Check if video opened successfully
    if not video.isOpened():
        print("Error: Could not open video file")
        return
    
    # Get frame count for naming
    frame_count = 0
    
    while True:
        # Read next frame
        success, frame = video.read()
        
        # Break if no frame was read
        if not success:
            break
        
        # Save frame as image
        frame_path = os.path.join(output_folder, f"frame_{frame_count:04d}.jpg")
        cv2.imwrite(frame_path, frame)
        
        frame_count += 1
        
        # Optional: Print progress
        if frame_count % 100 == 0:
            print(f"Extracted {frame_count} frames")
    
    # Release video capture object
    video.release()
    print(f"Finished extracting {frame_count} frames")

# Example usage
video_path = "images/movie/movie.mp4"
output_folder = "images/movie"
extract_frames(video_path, output_folder)
