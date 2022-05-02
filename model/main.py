from tracker import ObjectTracker

def main_script():
    model = ObjectTracker(cv2_tracker='csrt', fps_out=24, video_path=r'data/input.mkv', initial_cond=r'data/initial_conditions.json')

    model.run_model(display=False, out_video_path = 'data/video_tracking.avi')

if __name__ == "__main__":
    main_script()


