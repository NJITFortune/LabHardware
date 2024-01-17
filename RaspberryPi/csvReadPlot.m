
[filename, pathname] = uigetfile('*.csv');

data = csvread(fullfile(pathname,filename),1);

timestepDiv = 1000000000;

% Get time stamps in seconds
tims = (data(:,1) - data(1,1)) / timestepDiv;

% Filter outliers in the distance data
dist = medfilt1(data(:,2), 5);

% Filter outliers in the strength data
strn = medfilt1(data(:,3), 5);

figure(1); clf

ax(1) = subplot(211); plot(tims, dist, '.');
ax(2) = subplot(212); plot(tims, strn, '.');

linkaxes(ax,'x');