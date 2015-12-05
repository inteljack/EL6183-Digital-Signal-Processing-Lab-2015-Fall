
flip = @(x) x(end:-1:1)

% x = 1
[x,Fs] = audioread('chirp.wav')
a = [5 -4 3 -2 1]
b = flip(a)
y = filter(b, a, x)
[H, om] = freqz(b, a);
subplot(4,1,1)
plot(om,abs(H))

% LFO

t = [0:0.1:8];
A = 1;
f = 1;
y = A*sin(2*pi*f*t); % w = 2*pi*f
ynew = 1 + y
subplot(4,1,2)
plot(t,ynew)

% ouput

Id = ones(size(H));

H = exp(- 1j * y * om);  % frequency response of delay system

subplot(4,1,3)
xlabel('phasor - frequency response')
plot(om, abs(Id + H))
subplot(4,1,4)
xlabel('phasor - phase')
plot(om, unwrap(angle(H))/pi)



