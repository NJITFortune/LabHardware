function theSoundBoxer(a, Fs, filepath, filename)

[~, basefilename, ~] = fileparts(filename);

% %% Read Data and prep
% clear
% % [a,Fs] = audioread('/Volumes/Extreme SSD/WaponiData/Campinarana 2 canopy/Data/CAMPINARANA2_20231213_190000.wav');
% % [a,Fs] = audioread('/Volumes/Extreme SSD/WaponiData/Campinarana 2 canopy/Data/CAMPINARANA2_20231213_212000.wav');
% [a,Fs] = audioread('/Volumes/Extreme SSD/WaponiData/Campinarana 2 canopy/Data/CAMPINARANA2_20231213_230600.wav');

%     cutOffFreq = 5000;
%     [bb,aa] = butter(9, cutOffFreq / (Fs/2), 'low'); % Strong lowpass filter
%     c = filtfilt(bb,aa,a); % This is the filtering step

    cutOffFreqs = [20000, 50000];
    [bb,aa] = butter(9, [cutOffFreqs(1)/(Fs/2), cutOffFreqs(2)/(Fs/2)], 'bandpass'); % Strong lowpass filter
    c = filtfilt(bb,aa,a); % This is the filtering step


    rc = c(1:2:end); % Half the sample rate
    fFs = Fs/2; % This is the reduced sample rate (should be an integer!)
    tim = 1/fFs:1/fFs:length(rc)/fFs; % Make time steps so that we can select ranges.

%% Extract Frequency spectra

windowSize = 1; % Duration over which the FFT is calculated in seconds
stepsize = 0.5; % How much time for a step.

numWins = (floor((tim(end) - windowSize) / stepsize)); % How many windows in our sample?

% For each window
for j=numWins:-1:1

    % Select the time window
    startTim(j) = (j-1) * stepsize;
    tt = find(tim > startTim(j) & tim < startTim(j)+windowSize);
        if startTim(j)+windowSize > tim(end)
            fprintf('Oops \n');
        end

    % Calculate the FFT and put it into an array
    ptm = fftmachine(rc(tt) - mean(rc(tt)), fFs, 50);
    sampdat(:,j) = ptm.fftdata;

end

basePower = mean(sampdat'); % Take the mean of the FFTs across the sample.
    % THIS IS A SERIOUS LIMITATION OF THE METHOD.  A sample with a ton of
    % calls from a particular species will have an elevated baseline and
    % therefore may detect fewer (or none!) of that species calls.
baseFreq = ptm.fftfreq; % These are our frequencies

%% Detect signals

multiThresh = 3; % How many times the amplitude of the baseline?

% We only do this over our frequency range of interest.
lowestFreq = 10000;
highestFreq = 30000;
numWindowsAboveThresh = 20; % This is a minimum spectrum above the threshold

ff = find(baseFreq > lowestFreq & baseFreq < highestFreq); % Select our frequency range (indices)

listofwinners = []; % Indices of the samples that are above threhsold

for j = length(startTim):-1:1

    divPwr(:,j) = sampdat(:,j) ./ basePower';

    if ~isempty(find(divPwr(ff,j) > multiThresh, 1))
        aboveThreshIDXs = find(divPwr(ff,j) > multiThresh);
        if length(aboveThreshIDXs) > numWindowsAboveThresh
            length(aboveThreshIDXs);
            listofwinners(end+1) = j;            
            freqRange{length(listofwinners)} = [baseFreq(aboveThreshIDXs(1)), baseFreq(aboveThreshIDXs(end))];  
        end
    end

end

listofwinners = listofwinners(end:-1:1);
freqRange = flip(freqRange);

%% Review

figure(2); clf; 
    set(gcf, "Position", [500 700 1400 600]);
    specgram(rc, 1024, fFs, [], 1000); colormap('HOT'); ylim([lowestFreq highestFreq]);
    hold on; 
    % for j=1:length(freqRange) 
    %     plot([startTim(listofwinners(j)) startTim(listofwinners(j))], [freqRange{j}], 'g', 'LineWidth', 4); 
    % end

% Combine and box

togetherness = diff(listofwinners);

box(1).startTim = startTim(listofwinners(1)); box(1).endTim = startTim(listofwinners(1)) + windowSize;
box(1).minFreq = freqRange{1}(1); box(1).peakFreq = freqRange{1}(2);

for j = 1:length(togetherness)
    if togetherness(j) == 1
        box(end).minFreq = min([box(end).minFreq, freqRange{j+1}(1)]);
        box(end).peakFreq = max([box(end).peakFreq, freqRange{j+1}(2)]);
        box(end).endTim = startTim(listofwinners(j+1)) + windowSize;
    else
        box(end).endTim = startTim(listofwinners(j)) + windowSize;
        box(end).minFreq = min([box(end).minFreq, freqRange{j}(1)]); 
        box(end).peakFreq = max([box(end).peakFreq, freqRange{j}(2)]);
        box(end+1).startTim = startTim(listofwinners(j+1));
        box(end).endTim = startTim(listofwinners(j)) + windowSize;
        box(end).minFreq = freqRange{j+1}(1); 
        box(end).peakFreq = freqRange{j+1}(2);
    end
end

for j = 1:length(box)

    freqPad = 100;
    timPad = 1;

        ymin = max([0, box(j).minFreq - freqPad]);
        ymax = min([fFs/2, box(j).peakFreq + freqPad]);
        xmin = max([0, box(j).startTim - timPad]);
        xmax = min([tim(end), box(j).endTim + timPad]);


    figure(2); 
        plot([xmin, xmin, xmax, xmax, xmin], [ymin ymax ymax ymin ymin], 'm', 'LineWidth', 3);
        text(xmin,ymax,num2str(j), "FontSize", 14, "Color", "White", "FontWeight","bold");

end

    mkdir(fullfile(filepath, "/cutfiles/", basefilename));
    fprintf("     Making dir: %s \n", fullfile(filepath, "/cutfiles/", basefilename));
    drawnow; saveas(gcf,fullfile(filepath, "/cutfiles", basefilename, strcat("/", basefilename, ".jpg")));

%% Go for it?

% yn = input('Yes (1) or No (anything else)? \n');
% 
% if yn == 1

    % Cut out the parts from the file and save them.

    for j = 1:length(box)

       xmin = max([0, box(j).startTim - timPad]);
       xmax = min([tim(end), box(j).endTim + timPad]);

       newfullpathfile = fullfile(filepath, "/cutfiles", basefilename, strcat("/", basefilename, "_", num2str(xmin*10), "-", num2str(xmax*10), ".wav"));
       
       if ~isempty(rc(tim > xmin & tim < xmax))
           audiowrite(newfullpathfile, rc(tim > xmin & tim < xmax), fFs);
       end

    end

% end

