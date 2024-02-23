% automagicbrut.m

% Pick folder with videos to crop 
    myfolder = uigetdir;
    myfolder = [myfolder, '/*.wav'];
% Get all files in folder
    iFiles = dir(myfolder);
    
tic
for j = 1:length(iFiles)

    fprintf("File %i of %i, %s \n", j, length(iFiles), iFiles(j).name);
    [data, dataFs] = audioread(fullfile(iFiles(j).folder, iFiles(j).name));

    theSoundBoxer(data, dataFs, iFiles(j).folder, iFiles(j).name);

end
toc