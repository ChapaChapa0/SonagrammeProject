clear;
close all;

% Parameters
imWidth = 640;  % 1280 ou 640
imHeight = 480; % 720 ou 480
dWidth = 1280; % 1280 ou 640
dHeight = 720; % 720 ou 480
windowW = [261,390];
windowH = [101, 480];
laserPos = 220;
distMin = 100;
nb_fs = 5;
pas = 2;
sigma = 1.5;
seuil = 0.55;

% Realsense camera parameter
exp = 5000;
gain = 16;

% Compute parameters for LS
nb_rows_S = windowW(2) - windowW(1) + 1;
nb_columns_S = windowH(2) - windowH(1) + 1;

% Init

% Adjust parameters
ctx = realsense.context();
devices = ctx.query_devices();
for i = 1:length(devices)
    dev = devices{i};
    sensors = dev.query_sensors();
    sensors = sensors{1};
    for j = 1:length(sensors)
        sens = sensors{j};
        if sens.is('depth_sensor')
            emit = sens.get_option(realsense.option.emitter_enabled); % Get emitter status
            sens.set_option(realsense.option.exposure, exp); % Set exposure
            sens.set_option(realsense.option.gain, gain) % Set gain
        end
    end
end

% Change configuration
config = realsense.config();
config.enable_stream(realsense.stream.color, imWidth, imHeight, realsense.format.rgb8, 30)
config.enable_stream(realsense.stream.depth, imWidth, imHeight);

% Start streaming
pipe = realsense.pipeline();
profile = pipe.start(config);

% Get streaming device's
dev = profile.get_device();

% Get depth image parameters
depthSensor = dev.first('depth_sensor');
depthScale = depthSensor.get_depth_scale();

% We discard the first couple frames to allow the camera time to settle
for i = 1:5
    fs = pipe.wait_for_frames();
end

disp('Environnement ready')

% Loop
condition = 1;
iteration = 0;
baseDepthFrames = {};
baseDepth = {};
baseColor = {};
LS_base = {};
while iteration < 5
    disp('Press a key !')
    pause;
    
    % Get sets of color and depth frames
    fs = pipe.wait_for_frames();
    
    % Get color values from color frame
    colorFrame = fs.get_color_frame();
    colorData = colorFrame.get_data();
    color = permute(reshape(colorData',[3,imWidth, imHeight]),[3 2 1]);
    
    lColor = mean(color(laserPos,:,:));
    %     if norm(lColor(:)) > distMin
    if 1
        l_depth = {};
        for i = 1:nb_fs
            % Get sets of color and depth frames
            fs = pipe.wait_for_frames();
            
            % Get depth values from depth frame
            depthFrame = fs.get_depth_frame();
            depthData = depthFrame.get_data();
            depth = double(transpose(reshape(depthData, [imWidth,imHeight]))) .* depthScale; % Reshape and scale depth in meters
            depth2 = depth(windowH(1):windowH(2), windowW(1):windowW(2));
            l_depth{end + 1} = depth2;
        end
        post_depth = post_processing_depth(l_depth);
        
        % Computing LS
        LS = calcul_LS(post_depth, pas, sigma, seuil);
        
        LS_base{end + 1} = LS;
        iteration = iteration + 1;
        
        baseDepth{end + 1} = depth;
        baseDepthFrames{end + 1} = depthFrame;
        baseColor{end + 1} = color;
    else
        condition = 0; % End of the loop
    end
end

pipe.stop();

% We create the audio slices according to the number of slices saved
AS_base = {};
AE_base = {};
nb_S = length(LS_base);
audio_path = 'C:\Users\Hatem\Documents\Paul\Scripts_MATLAB\Audio\empreintes_2.wav';
[signal, f_ech] = audioread(audio_path);
size_slice = floor(length(signal) / nb_S);

for i = 1:nb_S
    slice_signal = signal((i-1) * size_slice + 1 : end);
    eclis_signal = flipud(signal(1 : (i-1) * size_slice + 1));
    slice_path = ['C:\Users\Hatem\Documents\Paul\Scripts_MATLAB\Audio\Slices\slice', num2str(i), '.wav'];
    eclis_path = ['C:\Users\Hatem\Documents\Paul\Scripts_MATLAB\Audio\Seclis\eclis', num2str(i), '.wav'];
    AS_base{end+1} = slice_path;
    AE_base{end+1} = eclis_path;
    audiowrite(slice_path, slice_signal, f_ech)
    audiowrite(eclis_path, eclis_signal, f_ech)
end

save('slices_base','imWidth','imHeight','dWidth','dHeight','windowW','windowH','laserPos','distMin','pas','sigma','seuil', ...
    'nb_rows_S','nb_columns_S','LS_base','AS_base','AE_base','exp','gain','baseDepth','baseDepthFrames','baseColor');
