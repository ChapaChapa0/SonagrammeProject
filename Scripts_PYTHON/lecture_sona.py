# LIBRARIES
import numpy as np                        # fundamental package for scientific computing
import pyrealsense2 as rs                 # Intel RealSense cross-platform open-source API
import time
import pyaudio
import wave
import audioop
import sys
import math
import pickle
from imprint_f import compute_imprint
from imprint_f import compute_position
print("Environment Ready")
    

# MAIN
# Parameters
f = open("slices_base", "r")
p = pickle.load(f)
repertory = p[0]
window_w = p[1]
window_h = p[2]
step_downsample = p[3]  # Step for downsampling on LS
sigma = p[4]            # Amount of blur on LS
threshold = p[5]        # Threshold to compute LS
delay_time = 0.2        # Time between each iteration

# Realsense camera parameter
len_im = p[6]
wid_im = p[7]
exp = p[8]
gain = p[9]
dis_shift = p[10]

# Imprint
window_imp = p[11]
step_imp = p[12]
imprint_global = p[13]
size_imp = len(imprint_global)

# Close parameters file
f.close()


# INIT CAMERA
# Adjust exposure and gain
ctx = rs.context()
devices = ctx.query_devices()
for dev in devices:
    sensors = dev.query_sensors();
    for sens in sensors:
        if sens.is_depth_sensor():
            emit = sens.get_option(rs.option.emitter_enabled); # Get emitter status
            sens.set_option(rs.option.exposure, exp); # Set exposure
            sens.set_option(rs.option.gain, gain) # Set gain
            sens.set_option(rs.option.emitter_enabled, dis_shift) # Disable emitter
pipe = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, len_im, wid_im, rs.format.rgb8, 30) #1280 * 720 ou 640 * 480
config.enable_stream(rs.stream.depth, len_im, wid_im, rs.format.z16, 30) #1280 * 720 ou 640 * 480
profile = pipe.start(config)

# Discard first frames
for i in range (0,5):
    frameset = pipe.wait_for_frames()

# INIT AUDIO
# Audio path
audio_path = repertory + 'empreintes.wav'

# Open the wav file in read-only mode
wave_file = wave.open(audio_path,"rb")
p = pyaudio.PyAudio()

# Audio parameters
file_format = p.get_format_from_width(wave_file.getsampwidth())
nb_channels = wave_file.getnchannels()
width = wave_file.getsampwidth()
framerate = wave_file.getframerate()
nb_frames = wave_file.getnframes()
time_wave = float(nb_frames) / float(framerate)
time_pixel = time_wave / size_imp

# Open the data stream
stream = p.open(format = file_format,
                channels = nb_channels,
                rate = framerate,
                output = True)


# Init acceleration parameters
speed = 1.0
new_fr = framerate

# Init data flow block
chunk_size = int(math.ceil(framerate * delay_time))
data = "init"

# LOOP
old_k = -1
reverse = False

# Pause
raw_input("Press enter...")
time.sleep(2)

while len(data) > 0:

    start = time.time()
    
    # Get new frames
    frameset = pipe.wait_for_frames()

    # Get arrays of depth data
    depth_frame = frameset.get_depth_frame()
    depth = np.asanyarray(depth_frame.get_data()).astype(np.uint16)

    # Compute LS
    depth0 = np.transpose(depth[window_h[0]: window_h[1]])
    depth0 = np.transpose(depth0[window_w[0]:window_w[1]])
    imprint = compute_imprint(depth0, step_downsample, sigma, threshold)
        
    # Find imprint position on global imprint
    k_min = compute_position(imprint_global, imprint, window_imp, step_imp)

    # Deduce if lecture is over
    if k_min > size_imp - step_imp[0]:
        data = ""
    # Repeat last buffer if same LS found
    elif old_k > k_min - step_imp[1]:
        speed = 1.0
        chunk_size = int(math.ceil(framerate * delay_time * speed))
    # Else continue lecture
    else:
        speed = ((k_min - old_k) * time_pixel) / delay_time
        chunk_size = int(math.ceil(framerate * delay_time * speed))
        data = wave_file.readframes(chunk_size)

    # Sleep
    end = time.time()
    computing_time = start - end
    if computing_time < delay_time:
        time.sleep(delay_time - computing_time)

    # Play sound according to new speed
    new_fr = int(round(framerate / speed))
    modified_data = audioop.ratecv(data, width, nb_channels, framerate, new_fr, None)[0]
    stream.write(modified_data)
    
    old_k = k_min
    
# Stop data flow
stream.stop_stream()
stream.close()

# Close PyAudio
p.terminate()

# Close file stream
wave_file.close()

# Close streaming pipe
pipe.stop()