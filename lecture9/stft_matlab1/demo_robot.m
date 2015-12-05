
% Load signal
[x, fs] = wavread('author.wav');
N = length(x);

% Compute STFT
R = 512;
Nfft = 512;
X = stft(x, R, Nfft);

% Set phase to zero in STFT-domain
X2 = abs(X);

% Synthesize new signal ('robotic')
y2 = inv_stft(X2, R, N);

soundsc(y2, fs);
