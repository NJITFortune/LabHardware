clear; 

% User settings
makeplots = 1;
speclen = 2000;
rango = 50;
numFreqBands = 8;

if makeplots == 1; close all; end

% Load the data
[data, Fs] = audioread('~/Downloads/WaponiBraziltmp/CAMPINARANA_20231214_031200.wav');
data = data - mean(data); % remove any DC offset
tim = 1/Fs:1/Fs:length(data)/Fs; % Make time stamps

% Calculate the overall spectrum so that we can automatically look at bands
sp = fftmachine(data,Fs,20000);
    sp.fftdata = detrend(sp.fftdata);
    sp.fftdata = sp.fftdata - min(sp.fftdata) + 0.0000001;

scalnum = floor(length(sp.fftdata)/speclen);
    sp.fftfreq = sp.fftfreq(1:scalnum:end);
    sp.fftdata = sp.fftdata(1:scalnum:end);

[pks, pspidx] = findpeaks(sp.fftdata, "MinPeakWidth", 5);
    [pks, pksidx] = sort(pks, 'descend');
    pspidx = pspidx(pksidx);
    listOfFreqs = sp.fftfreq(pspidx);
    listOfFreqs = listOfFreqs(1:numFreqBands);

% Plot the spectrum
figure(11); clf; hold on;
    semilogy(sp.fftfreq, sp.fftdata)
    semilogy(sp.fftfreq(pspidx), sp.fftdata(pspidx), 'r.', 'MarkerSize', 16);
    semilogy(sp.fftfreq(pspidx(1)), sp.fftdata(pspidx(1)), 'g.', 'MarkerSize', 32);

% Do the frequency filtering for each band, and plot if needed    
if makeplots == 1
    for j = numFreqBands:-1:1
        fd(:,j) = bandpass(data,[sp.fftfreq(pspidx(j))-rango, sp.fftfreq(pspidx(j))+rango], Fs);
        figure(j); clf
            subplot(211); specgram(fd(:,j),1024,Fs,[], 1000);
            subplot(212); plot(tim, fd(:,j)); xlim([tim(1), tim(end)])
    end
else
    parfor j = 1:10
        fd(:,j) = bandpass(data,[sp.fftfreq(pspidx(j))-rango, sp.fftfreq(pspidx(j))+rango], Fs);
    end
end

%% Extract features from the filtered data to identify signals

for entryNum = numFreqBands:-1:1
smoothConstant = 0.040;

% Use audioFeatureExtractor to get some features
aFE = audioFeatureExtractor(SampleRate=Fs, ...
    Window = hamming(round(0.01*Fs),"periodic"), ...
    OverlapLength = round(0.009*Fs), ...
    barkSpectrum = true, ... 
    shortTimeEnergy = true, ...
    spectralKurtosis = true); 

     % spectralCentroid = true, ... % zerocrossrate = true, 
     % linearSpectrum, melSpectrum, erbSpectrum, mfcc, mfccDelta
     % mfccDeltaDelta, gtcc, gtccDelta, gtccDeltaDelta, spectralCrest, spectralDecrease
     % spectralEntropy, spectralFlatness, spectralFlux, spectralRolloffPoint, spectralSkewness, spectralSlope
     % spectralSpread, harmonicRatio, zerocrossrate, shortTimeEnergy

iaFE = info(aFE);
features = extract(aFE,fd(:, entryNum));

% Make a separate time base for these data

    fFs = length(features(:,iaFE.shortTimeEnergy))/tim(end);
    ttim = 1/fFs:1/fFs:length(features(:,iaFE.shortTimeEnergy))/fFs;

% Export these features for use in detecting events

    maxBark = max(features(:,iaFE.barkSpectrum)');
    shortEnergy = features(:,iaFE.shortTimeEnergy);
    specKurt = movmean(features(:,iaFE.spectralKurtosis), round(fFs * smoothConstant));

    aEnv = movmean(abs(fd(:, entryNum)), round(Fs * 0.020));
    aEnv = aEnv - mean(aEnv);
    aEnv = aEnv * max(fd(:, entryNum)) / max(aEnv);

    aEnv = resample(aEnv, tim, fFs);
    %length(aEnv)
    %length(ttim)

% Find a threshold for each 
hiThreshScalar = 0.70;

    mm = median(maxBark);
    pm = hiThreshScalar * mean(findpeaks(maxBark, "SortStr", "descend", "NPeaks", 4));
        tm = (mm+pm)/2;
    ms = median(shortEnergy);
    ps = hiThreshScalar * mean(findpeaks(shortEnergy, "SortStr", "descend", "NPeaks", 4));
        ts = (ms+ps)/2;
    mk = median(specKurt);
    pk = hiThreshScalar * mean(findpeaks(specKurt, "SortStr", "descend", "NPeaks", 4));
        tk = (mk+pk)/2;
    me = median(aEnv);
    pe = hiThreshScalar * mean(findpeaks(aEnv, "SortStr", "descend", "NPeaks", 4));
        te = (me+pe)/2;

% Detect potential items

zz = zeros(1,length(ttim));
    candidates = zz;

    candidates(maxBark > tm) = 1;
    candidates(shortEnergy > ts) = 1;
    candidates(specKurt > tk) = 1;
    candidates(aEnv > te) = 1;

% Refine items

gapFiller = 0.250;
gapCount = round(fFs * gapFiller);

    dd = diff(candidates);
    startIDXs = find(dd == 1);
    endIDXs = find(dd == -1);
length(startIDXs)
length(endIDXs)
    for jj = 1:length(startIDXs)-1
        nextEnd = endIDXs(find(endIDXs > startIDXs(jj), 1, "first"));
        if startIDXs(jj+1) - nextEnd < gapCount
            candidates(nextEnd:startIDXs(jj+1)) = 1;
        end
    end

% Zero out the band if too many or too much time was highlighted

    if length(find(candidates == 1)) > 0.5 * length(candidates)
        candidates(candidates == 1) = 0;
    end

    if length(find(diff(candidates) == 1)) > 30
        candidates(candidates == 1) = 0;
    end

    candida(:,entryNum) = candidates;

% Plot the data
    if makeplots == 1
        figure(30+entryNum); clf;
        aaa(1) = subplot(411); 
            yyaxis('right'); plot(ttim, maxBark); hold on; yline(mm, 'r'); yline((mm+pm)/2, 'm');
            yyaxis('left'); plot(ttim, shortEnergy); yline(ms, 'c'); yline((ms+ps)/2, 'g');
        aaa(2) = subplot(412); 
            yyaxis('right'); plot(ttim, specKurt); hold on; yline(mk, 'r'); yline((mk+pk)/2, 'm');
            yyaxis('left'); plot(ttim, aEnv); yline(me, 'c'); yline((me+pe)/2, 'g');
        % aaa(3) = subplot(513); 
        %     yyaxis('right'); plot(ttim, features(:,iaFE.spectralKurtosis)); hold on; yyaxis('left'); plot(ttim, features(:,iaFE.spectralEntropy))
        % aaa(4) = subplot(514); 
        %     yyaxis('right'); plot(ttim, features(:,iaFE.harmonicRatio)); hold on; yyaxis('left'); plot(ttim, features(:,iaFE.spectralCrest))
        aaa(3) = subplot(413); plot(tim, fd(:,entryNum))
            hold on; plot(ttim, aEnv);
            plot(ttim, 0.2 * candidates, 'LineWidth', 3);
        aaa(4) = subplot(414); specgram(fd(:,entryNum), 512, Fs, [], 500); clim([-10 20]); colormap('HOT');
    
        linkaxes(aaa,'x')
    end


end

%% Make final output

figure(100); clf; hold on;
set(gcf, 'renderer', 'painters');
orient(gcf,'landscape')
set(gcf, 'Position', [70 800 800 400])
specgram(data,1024,Fs,[], 1000); colormap('HOT')

yrang = 200;
xpad = 0.100;
sylcount = 0;

for k = 1:numFreqBands

    if sum(candida(:,k)) > 3
    cc = diff(candida(:,k));
    starts = find(cc == 1); ends = find(cc == -1);
        
        for kk = 1:length(starts)
            nextEnd = find(ends > starts(kk), 1, 'first');
            if isempty(nextEnd) 
                ends(end+1) = length(ttim); 
                nextEnd = find(ends > starts(kk), 1, 'first');
            end
        sylcount = sylcount+1;
    minx = max([1/fFs, ttim(starts(kk))-xpad]);
    maxx = min([ttim(end), ttim(ends(nextEnd))+xpad]);

plot([minx, maxx, maxx, minx, minx], [listOfFreqs(k)-yrang, listOfFreqs(k)-yrang, listOfFreqs(k)+yrang, listOfFreqs(k)+yrang, listOfFreqs(k)-yrang], 'g-');
text(ttim(starts(kk)), listOfFreqs(k)+yrang, num2str(sylcount), 'Color', 'White', 'FontWeight', 'bold');
        end

    end

end
clim([-20 35]);
ylim([0 Fs/4]);
xlim([0 tim(end)]);
fprintf('Found %i candidates. \n', sylcount);