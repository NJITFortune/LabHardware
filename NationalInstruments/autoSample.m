%% Script to do automated sampling from tanks

%% USER SETTINGS

deviceID = "Dev1";
sampleRate = 10000;          % 10 kHz
recordDuration = 300;        % 5 minutes (sec)
repeatInterval = 1800;       % 30 minutes (sec)
outputFolder = "D:\DAQ_Data";  % CHANGE THIS

channelIDs   = 0:15;

channelNames = { ...
    'EOD1','EOD2','Stim','Ref',...
    'Ch5','Ch6','Ch7','Ch8',...
    'Ch9','Ch10','Ch11','Ch12',...
    'Ch13','Ch14','Ch15','Ch16'};

%% Create DAQ Object
dq = daq("ni");
dq.Rate = sampleRate;

for k = 1:length(channelIDs)
    ch = addinput(dq, deviceID, "ai" + channelIDs(k), "Voltage");
    ch.Name = channelNames{k};
end

fprintf("DAQ ready.\n");

%% Continuous 30-minute cycle loop
while true

    startTime = datetime("now");
    filename = datestr(startTime,'yyyy-mm-dd_HH-MM-SS');
    fullpath = fullfile(outputFolder, filename + ".mat");

    fprintf("Recording started: %s\n", filename);

    % ---- Acquire full 5-minute block ----
    data = read(dq, seconds(recordDuration), ...
                "OutputFormat","Matrix");

    % ---- Save file ----
    save(fullpath, "data", "sampleRate", ...
         "channelNames", "startTime", "-v7.3");

    fprintf("Recording saved: %s\n", filename);

    % ---- Wait remaining time to reach 30 min ----
    elapsed = seconds(datetime("now") - startTime);
    pause(max(0, repeatInterval - elapsed));

end
