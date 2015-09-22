%% read_sin01.m
%
% View parameters, plot waveform, compute and display spectrum

%%

clear

%% Load .wav file 

[x, Fs, nbits, opts] = wavread('sin01_mono.wav');

whos

%%

Fs
nbits
opts.fmt

%%

soundsc(x, Fs)

%% Plot waveform

figure(1)
clf
plot(x)
xlabel('Time (sample)')

%% Time axis in seconds

N = length(x);
t = (1:N)/Fs;

figure(1)
clf
plot(t, x)
xlabel('Time (sec)')

%% Zoom in to 50 msec

xlim(0.4 + [0 0.050])

%% Distribution of samples

xs = sort(x);

figure(1)
clf
plot(xs)

%% See quantization

xlim([0 100])

%% What is the quantization increment ?

% select subset of xs
xs2 = xs(1:100);

plot(xs2)

%%

% Remove duplicates
xs2 = unique(xs2)

%%

% Quantization size is 1 / 2^15
d = diff(xs2)

%%
% The value is 1/2^15

1 / 2^15


%% Frequency spectrum
% Use Fast Fourier Transform (FFT)

% Use power of 2 for FFT efficiency
N = length(x)
Nfft = 2^ceil(log2(N))  % power of 2 greater than signal length

%% Compute Fourier transform 

X = fft(x, Nfft);   
k = 0:Nfft-1;      % FFT index

figure(1)
clf
plot(k, abs(X))
xlabel('FFT index')
title('Spectrum')

%% Center dc

X2 = fftshift(X);
k2 = -Nfft/2 : Nfft/2-1;

figure(1)
clf
plot(k2, abs(X2))
xlabel('FFT index')
title('Spectrum')

%% Normalized frequency
% Normalized frequency is in units of [cycles per sample]

fn = ( -Nfft/2 : Nfft/2-1 ) / Nfft;

figure(1)
clf
plot(fn, abs(X2))
xlabel('Frequency (cycles/sample)')
title('Spectrum')

%% Frequency in Hz

f = ( -Nfft/2 : Nfft/2-1 ) / Nfft * Fs;

figure(1)
clf
plot(f, abs(X2))
xlabel('Frequency (cycles/second, i.e. Hz)')
title('Spectrum')

%%
% Zoom to frequency band [0 500] Hz

xlim([0 500])

%%
% Zoom y-axis.
% Notice the sidelobes

ylim([0 100])


%% Fourier transform in dB

X_dB = 20*log10(abs(X2));

figure(1)
clf
plot(f, X_dB)
xlabel('Frequency (cycles/second, i.e. Hz)')
title('Spectrum (dB)')

xlim([0 Fs/2])
grid

%%
% Zoom to frequency band [0 500] Hz

xlim([0 500])



%% Increase FFT length
% Use Fast Fourier Transform (FFT) with zero-padding

% Use power of 2 for FFT efficiency
N = length(x)
Nfft_2 = 4 * 2^ceil(log2(N))  

%% Compute Fourier transform 

X_2 = fft(x, Nfft_2);   
X_2_dB = 20*log10(abs(fftshift(X_2)));
f_2 = ( -Nfft_2/2 : Nfft_2/2-1 ) / Nfft_2 * Fs;

figure(2)
clf
plot(f_2, X_2_dB)
xlabel('Frequency (cycles/second, i.e. Hz)')
title('Spectrum (dB)')

xlim([0 500])
grid

% Question: What is the spacing between the nulls? 
% How is it related to the length of the signal x?

%% Compare the two computed Fourier transforms
% They look different!

figure(3)
clf

plot(f_2, X_2_dB, f, X_dB, 'r--')
str1 = sprintf('Nfft = %d', Nfft)
str2 = sprintf('Nfft = %d', Nfft_2)
legend(str2, str1)
xlim([0 500])

%%
% Zoom to frequency band [240 280] Hz

xlim([240 280])

%%
% User markers to clarify

figure(3)
clf

plot(f_2, X_2_dB, f, X_dB, 'ro-')
xlim([240 280])
legend(str2, str1)













