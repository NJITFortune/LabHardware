%% Script to do automated sampling from tanks

%% USER SETTINGS

deviceID = "Dev1";
sampleRate = 10000;           % 10 kHz
recordDuration = 300;         % 5 minutes (seconds)
repeatInterval = 1800;        % 30 minutes (seconds)

outputFolder = "C:\Users\lab\data"; 

% ----- USER CHANNEL NAMES (edit as needed) -----
channelIDs   = 0:15;  % Up to 16 channels

channelNames = { ...
    'EOD1','EOD2','Stim','Ref',...
    'Ch5','Ch6','Ch7','Ch8',...
    'Ch9','Ch10','Ch11','Ch12',...
    'Ch13','Ch14','Ch15','Ch16'};

%% Create DataAcquisition Object
dq = daq("ni");
dq.Rate = sampleRate;

for k = 1:length(channelIDs)
    ch = addinput(dq, deviceID, "ai" + channelIDs(k), "Voltage");
    ch.Name = channelNames{k};
end

fprintf("DAQ ready. Waiting to start...\n");

%% Main Loop
while true

    startTime = datetime("now");
    filename = datestr(startTime, 'yyyy-mm-dd_HH-MM-SS');
    fullpath = fullfile(outputFolder, filename + ".mat");

    fprintf("Starting recording: %s\n", filename);

    % Create writable MAT file
    m = matfile(fullpath, 'Writable', true);

    totalSamples = sampleRate * recordDuration;
    chunkSize = sampleRate;  % write 1-second chunks
    samplesWritten = 0;

    % Preallocate on disk
    m.data(totalSamples, length(channelIDs)) = 0;

    lh = addlistener(dq, "DataAvailable", @(src,event) writeChunk(event));

    start(dq, "continuous");

    tic;
    while toc < recordDuration
        pause(0.5);
    end

    stop(dq);
    delete(lh);

    fprintf("Finished recording: %s\n", filename);

    % Wait remaining time to reach 30 minutes
    elapsed = seconds(datetime("now") - startTime);
    pause(max(0, repeatInterval - elapsed));

end

%% Data Writing Function
function writeChunk(event)
    persistent idx mfile totalSamplesLocal

    if isempty(idx)
        idx = 1;
        mfile = evalin('base', 'm');
        totalSamplesLocal = evalin('base', 'totalSamples');
    end

    newData = event.Data;
    n = size(newData,1);

    if idx + n - 1 <= totalSamplesLocal
        mfile.data(idx:idx+n-1, :) = newData;
        idx = idx + n;
    end

    if idx > totalSamplesLocal
        idx = [];
    end
end
