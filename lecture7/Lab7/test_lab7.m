%%

clc
clear

N = 500;
n = 1:N;
x = sin(5*pi*n/N) + 0.5*randn(1, N);        % Input signal

fc = 0.2;
[b, a] = butter(2, 2*fc);  
[H,om] = freqz(b,a,10000);
figure(1)
plot(om, abs(H))


%% three knob tone
clear
clc

G = 0.94;
Q = 0.999;
fc = 0.2;  % w = 2*pi*f
wc = 2*pi*fc;
B = wc/Q
Gsq = sqrt(G);
tanB = tan(B/2);

a = [Gsq+G*tanB -2*Gsq*cos(wc) Gsq-G*tanB];
b = [Gsq+tanB -2*Gsq*cos(wc) Gsq-tanB];
[H,om] = freqz(b,a,10000);
figure(1)
zplane(b,a)
figure(2)
plot(om, abs(H))