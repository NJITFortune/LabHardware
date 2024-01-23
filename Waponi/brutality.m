clear; 
% close all;

speclen = 2000;
rango = 50;

[data, Fs] = audioread('~/Downloads/WaponiBraziltmp/CAMPINARANA_20231214_031200.wav');
data = data - mean(data);
tim = 1/Fs:1/Fs:length(data)/Fs;

sp = fftmachine(data,Fs,20000);
sp.fftdata = detrend(sp.fftdata);
sp.fftdata = sp.fftdata - min(sp.fftdata) + 0.0000001;
scalnum = floor(length(sp.fftdata)/speclen);
sp.fftfreq = sp.fftfreq(1:scalnum:end);
sp.fftdata = sp.fftdata(1:scalnum:end);

[pks,pspidx] = findpeaks(sp.fftdata, "MinPeakWidth", 5);

[pks, pksidx] = sort(pks, 'descend');
pspidx = pspidx(pksidx);

figure(11); clf; 
semilogy(sp.fftfreq, sp.fftdata)
hold on;
semilogy(sp.fftfreq(pspidx), sp.fftdata(pspidx), 'r.', 'MarkerSize', 16);
semilogy(sp.fftfreq(pspidx(1)), sp.fftdata(pspidx(1)), 'g.', 'MarkerSize', 32);


parfor j = 1:10

fd(:,j) = bandpass(data,[sp.fftfreq(pspidx(j))-rango, sp.fftfreq(pspidx(j))+rango], Fs);
%figure(j); clf
%    subplot(211); specgram(fd,1024,Fs,[], 1000);
%    subplot(212); plot(tim, fd); xlim([tim(1), tim(end)])

end


%%

aFE = audioFeatureExtractor(SampleRate=Fs, ...
    Window=hamming(round(0.01*Fs),"periodic"), ...
    OverlapLength=round(0.005*Fs), ...
    barkSpectrum=true, ...
    spectralCentroid=true, zerocrossrate=true, shortTimeEnergy=true, ...
    spectralKurtosis=true, ...
    spectralEntropy=true);

i = info(aFE);

features = extract(aFE,fd(:,3));

figure(27); clf;
subplot(211); yyaxis('right'); plot(features(:,i.shortTimeEnergy)); hold on; yyaxis('left'); plot(features(:,i.zerocrossrate))

subplot(212); plot(tim, fd(:,3))


