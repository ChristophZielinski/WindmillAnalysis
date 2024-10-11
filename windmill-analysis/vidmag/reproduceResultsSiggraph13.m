clear;

dataDir = './data';

resultsDir = 'ResultsSIGGRAPH2013/';
mkdir(resultsDir);
defaultPyrType = 'halfOctave'; % Half octave pyramid is default as discussed in paper
scaleAndClipLargeVideos = true; % With this enabled, approximately 4GB of memory is used

% Uncomment to use octave bandwidth pyramid: speeds up processing,
% but will produce slightly different results
%defaultPyrType = 'octave'; 

% Uncomment to process full video sequences (uses about 16GB of memory)
%scaleAndClipLargeVideos = false;

%% Amplify parameters and call of function
inFile = fullfile(dataDir, '1.mp4');
samplingRate = 24; % Hz
loCutoff = 0.2;    % Hz
hiCutoff = 0.25;    % Hz
alpha = 100;    
sigma = 5;         % Pixels
temporalFilter = @FIRWindowBP; 
pyrType = defaultPyrType;
if (scaleAndClipLargeVideos)
    phaseAmplify(inFile, alpha, loCutoff, hiCutoff, samplingRate, resultsDir,'sigma', sigma,'pyrType', pyrType,'temporalFilter', temporalFilter,'scaleVideo', 2/3);
else
    phaseAmplify(inFile, alpha, loCutoff, hiCutoff, samplingRate, resultsDir,'sigma', sigma,'pyrType', pyrType,'temporalFilter', temporalFilter, 'scaleVideo', 1);
end  
% The sequence is very large. To save on CPU time, we set
% pyramid type to 'octave'. If you have the resources or time, feel free to change it
% to 'halfOctave'
