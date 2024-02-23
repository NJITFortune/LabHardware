[filename, pathname] = uigetfile('*.csv');

Fs = 250;

data = csvread(fullfile(pathname,filename),1);

timestepDiv = 1000000000;

% Get time stamps in seconds
tims = (data(:,1) - data(1,1)) / timestepDiv;

x = data(:,2); y = data(:,3); z = data(:,4);

[Xdata, utim] = resample(x, tims, Fs);
[Ydata, ~] = resample(y, tims, 250);
[Zdata, ~] = resample(z, tims, 250);

figure(1); clf;
    plot(utim, [Xdata, Ydata, Zdata], '.-');

fX = fftMaker(Xdata - mean(Xdata), Fs);
fY = fftMaker(Ydata - mean(Ydata), Fs);
fZ = fftMaker(Zdata - mean(Zdata), Fs);

figure(2); clf;
    plot(fX.freq, [fX.pwr, fY.pwr, fZ.pwr]);
    xlim([0 25]);

function out = fftMaker(data, Fs)
% Compute the FFT (Fast Fourier Transform)
% out = fftmachine(data, Fs);
% Where out is a strucutre with freq and pwr

L = length(data);

NFFT = 2^nextpow2(L); % Next power of 2 from length of the data

fftdata = fft(data,NFFT)/L;

% We use only half of the data, hence fftdata(1:round(end/2));
% And we take the absolute value of the real component and filter
% that so that it is smooth

out.pwr = 2*abs(fftdata(1:(NFFT/2)+1));

% Now we need to generate the X values - which are the frequencies

out.freq = Fs/2*linspace(0,1,NFFT/2+1);

% Sometimes the rounding makes it so that the lengths of the
% data and the frequency values are off by one.  Let us correct that.

minlen = min([length(out.freq) length(out.pwr)]);
out.fftfreq = out.freq(1:minlen);
out.fftdata = out.pwr(1:minlen);

end