%% lab2_practice.m
% This is a lab2 practice script for doing assignments 3 ~ 9.

%%

clc
clear
%% Sinusoid wave

N = 4000;
x = zeros(N, 1);        % all zeros
x(1) = 1;               % first value is 1

Fs = 8000;              % sampling frequency ( sample / second )
F1 = 400;               % frequency ( cycles / second )
f1 = F1/Fs;             % normalized frequency ( cycles / sample )
om1 = 2 * pi * f1;
r = 0.999;
a = [1 -2*r*cos(om1) r^2 0 0];
b = 1;
y = filter(b, a, x);

%% Zero-Pole diagram
subplot(121)
zplane(b,a)
legend('second order zplane')
subplot(122)
zplane(b,a)
legend('fourth order zplane')

%%
subplot(211)
plot(y)
legend('figure2 sin wave')
subplot(212)
stem(y)
legend('figure2 sin wave stems')

%% Listen the sound
soundsc(y)



%%