
flip = @(x) x(end:-1:1)
figure(1)


% LFO

t = [1:0.0156555772:9];
A = 0.8;
f = 0.8;
yy = A*sin(2*pi*f*t);

% x = 1
[x,Fs] = audioread('author.wav');
a = [5 -4 3 -2 1];
b = flip(a);
y = filter(b, a, x);
[H, om] = freqz(b, a);
subplot(4,1,1)
plot(om,abs(H))



% ynew = 1 + yy
subplot(4,1,2)
plot(t,yy)
Id = ones(size(H));

H = exp(- 1j * 10 * (om));

subplot(4,1,3)
xlabel('phasor - frequency response')
om = om +yy';
plot(om, abs(Id + H))


subplot(4,1,4)
xlabel('phasor - phase')
plot(om, unwrap(angle(H))/pi)


soundsc(y)




