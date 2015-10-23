%% demo03: Modulation property of Z-transform and DTFT
% Example using IIR filter 

%% Define IIR filter 

K = 3;
[b, a] = cheby2(K, 30, 0.6);

Nfft = 64;
H = fft(b, Nfft) ./ fft(a, Nfft);
f = (0:Nfft-1)/Nfft;
om = 2*pi*f;

figure(1)
clf
subplot(2, 1, 1)
zplane(b, a)
title('H(z)   [Z Transform]')

subplot(2, 1, 2)
plot(om - pi, fftshift(abs(H)))
title('|H(\omega)|   [Frequency response]')
xlabel('\omega')
xlim([-pi pi])

%% Modulation
% Complex exponential modulation

I = sqrt(-1);
s = exp( I * 0.1 * pi * (0:K) );   

b2 = b .* s;
a2 = a .* s;
% filter coefficients are complex !

H2 = fft(b2, Nfft) ./ fft(a2, Nfft);    % frequency response

figure(2)
clf
subplot(2, 1, 1)
zplane(b2, a2)
title('H2(z)   [Z Transform]')

subplot(2, 1, 2)
plot(om - pi, fftshift(abs(H2)))
title('|H2(\omega)|   [Frequency response]')
xlabel('\omega')
xlim([-pi pi])
ylim([0 1.2])

print -dpdf demo03



