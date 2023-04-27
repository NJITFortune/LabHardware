function out = f2time(userfilespec)

iFiles = dir(userfilespec);

%% Cycle through every file in the directory

for k = 1:length(iFiles)

    [a, Fs] = audioread(iFiles(k).name]);

end

