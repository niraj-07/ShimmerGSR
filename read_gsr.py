import pyxdf
import matplotlib.pyplot as plt
import os

# Make sure the file path is correct
file_path = r'C:/LabData/sub-P001/ses-S001/gsr/sub-P001_ses-S001_task-Default_run-001_gsr.xdf'

def load_and_plot_gsr(path):
    if not os.path.exists(path):
        print(f"Error: File not found at {path}")
        return
    
    try:
        data, header = pyxdf.load_xdf(path)
    except Exception as e:
        print(f"Error loading XDF file: {e}")
        return

    gsr_stream = None
    for stream in data:
        
        if stream['info']['name'][0] == 'ShimmerGSR':
            gsr_stream = stream
            print("Found 'ShimmerGSR' stream.")
            break


    if gsr_stream:
        y_data = gsr_stream['time_series'][:, 0]
        x_timestamps = gsr_stream['time_stamps']

        print(f"Loaded {len(y_data)} data points.")

        plt.figure(figsize=(12, 5))
        plt.plot(x_timestamps, y_data)
        
        plt.title('Shimmer GSR Data')
        plt.xlabel('Time (LSL Timestamp)')
        plt.ylabel('GSR (kOhms)')
        plt.show() 
        
    else:
        print("Error: Could not find a stream named 'ShimmerGSR' in the file.")


if __name__ == '__main__':
    load_and_plot_gsr(file_path)