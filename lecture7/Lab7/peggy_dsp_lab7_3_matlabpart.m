
[x,Fs] = audioread('100_300_8s.wav')

c = 0.6
b = [conj(c) -1]
a = [-1 c]
y = filter(b, a, x)
[H, om] = freqz(y);

% See that |H(om)| = 1

figure(1) % amplitude
plot(om, 20*log(abs(H)))
