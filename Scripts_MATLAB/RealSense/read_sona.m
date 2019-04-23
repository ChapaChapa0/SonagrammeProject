% clear;
close all;

% Load and init parameters
load('slices_base');
pas_t = 10;

% Init

% Adjust camera parameters
ctx = realsense.context();ty
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
            sens.set_option(realsense.option.emitter_enabled, 0) % Disable emitter
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

% Loop
condition = 1;
iteration = 0;
old_i = 0;
resDepth = {};
resColor = {};
resLS = {};
res_i = {};
resScore = {};
while iteration < 20
%     disp('Press a key !')
    pause(0.5);
    
    tic
    
    % Get color and depth frames
    fs = pipe.wait_for_frames();
    
    % Get color values from color frame
    colorFrame = fs.get_color_frame();
    colorData = colorFrame.get_data();
    color = permute(reshape(colorData',[3,imWidth, imHeight]),[3 2 1]);
    
    lColor = mean(color(laserPos,:,:));
    %     if norm(lColor(:)) > distMin
    if 1
        % Get depth values from depth frame
        depthFrame = fs.get_depth_frame();
        depthData = depthFrame.get_data();
        depth = double(transpose(reshape(depthData, [imWidth,imHeight]))) .* depthScale; % Reshape and scale depth in meters
        depth2 = depth(windowH(1):windowH(2), windowW(1):windowW(2));

        % Computing LS
        LS0 = calcul_LS(depth2, pas, sigma, seuil);
        
        % Searching for the audio extract corresponding to this slice in our base
        i_min = 0;
        score_min = Inf;
        
        windowT = time_window(LS_base, old_i, pas_t);
        for i = 1:windowT(1):windowT(2)
            LS1 = LS_base{i};
            masque = abs(LS1 - LS0);
            score = mean(mean(masque));
            
            % Sauvegarde du meilleur score :
            if score < score_min
                i_min = i;
                score_min = score;
            end
        end
        
        i_min
        score_min
        
        % We can now play the extract corresponding to this slice
        if i_min >= old_i
            sound0 = char(AS_base(i_min));
        else
            sound0 = char(AS_base(i_min));
        end
        old_i = i_min;
        [signal,f_ech] = audioread(sound0);
        if iteration > 0
            stop(player);
        end
        player = audioplayer(signal,f_ech);
            play(player);
        iteration = iteration + 1;
    else
        if iteration > 0
            stop(player);
        end
        condition = 0;
    end
    
    timeElapsed = toc;
    
    resDepth{end + 1} = depth;
    resColor{end + 1} = color;
    resLS{end + 1} = LS0;
    res_i{end + 1} = i_min;
    resScore{end + 1} = score_min;
end

pipe.stop();

save('res','resLS','res_i','resDepth','resColor','resScore','LS_base','baseDepth','baseDepthFrames','baseColor');

% pcl_obj = realsense.pointcloud();
% points = pcl_obj.calculate(depthFrame);
% vertices = points.get_vertices();
% figure;
% pcshow(vertices);

% data = points.get_data();