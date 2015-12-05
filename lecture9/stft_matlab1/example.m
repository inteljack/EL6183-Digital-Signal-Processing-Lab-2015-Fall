%% STFT example
% Verify perfect reconstruction and display STFT (spectrogram)
%
% EL 7133 - Ivan Selesnick

%% Load signal

load mtlb       % load mtlb, Fs (sampling frequency)

x = mtlb';      % convert to row vector

N = length(x);

%% Compute STFT

R = 512;                % R : frame length
Nfft = 1024;            % Nfft : length of FFT 

X = stft(x, R, Nfft);   % forward STFT

y = inv_stft(X, R, N);  % inverse STFT

err = max(abs(x - y));  % reconstruction error

fprintf('Reconstruction error = %d\n', err);


%% Display STFT
% Display in dB

dB = @(x) 20*log10(abs(x));

figure(1)
clf

subplot(3, 1, 1)
plot((1:N)/Fs, x)
xlim([0 N/Fs])
xlabel('Time (sec)')
title('Signal')

subplot(3, 1, [2 3])
Clim = [-40 0] + max(dB(X(:)));         % Clim : color limits
imagesc([0 N/Fs], [0 Fs/2], dB(X(1:Nfft/2, :)), Clim)
xlim([0 N/Fs])
axis xy
xlabel('Time (sec)')
ylabel('Frequency (Hz)')
str = sprintf('Short-time Fourier Transform [ R = %d, Nfft = %d ]', R, Nfft);
title(str)

orient landscape
print -dpdf example

