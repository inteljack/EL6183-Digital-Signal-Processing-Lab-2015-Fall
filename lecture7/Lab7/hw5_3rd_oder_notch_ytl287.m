%% Notch filtering of DC gain equals to 1
% Design a third order notch filter that satisfied the following:
% Null out at 0.1 pi radius/sample (0.05 cycles/sample)
% Modulous of the poles is 0.9
% Should be normalized

%% Initialization
clc
clear

%% A second order filter before normalization H1(z)
w = 0.7*pi;                 % The null out frequency
r = 0.9;                    % modulous of 0.9
b1 = [1 -2*cos(w) 1];        % filter coefficients
a1 = [1 -2*r*cos(w) r^2];    % filter coefficients

%plot properties
[H1,om1]=freqz(b1,a1,10000);    % Generate frequency response of 10000 points

figure(1)
subplot(2,1,1)
zplane(b1,a1)
title('pole-zero diagram');

subplot(2,1,2)
plot(om1/pi,abs(H1));
grid on

%% Design a normalization filter H2(z) for H1(z)
% Given that the magnitude of the H1(-1) is 1.11
% new filter H(z) is H1(z)*H2(z) 

beta = polyval(b1,-1)/polyval(a1,-1);         % Which is aproximately 1.11
p = 0.999;                                      % p should < 1, otherwise k = 0
z1 = ((1+p)-((1-p)*beta))/((1+p)+((1-p)*beta));
k = (1-p)/(1-z1);

b2 = k.*[1 -z1];    % filter coefficients
a2 = [1 -p];    % filter coefficients
[H2,om2]=freqz(b2,a2,10000);    % Generate frequency response of 10000 points

%  plot the properties of H2(z)
figure(2)
subplot(2,1,1)
zplane(b2,a2)
title('pole-zero diagram of normalize filter');

subplot(2,1,2)
plot(om2/pi,abs(H2));
ylim([0,1.2])
grid on

%% Apply and plot the cascade of two filters H1(z) and H2(z)
b = conv(b1,b2);
a = conv(a1,a2);

[H,om]=freqz(b,a,10000);    % Generate frequency response of 10000 points

figure(3)
subplot(2,1,1)
zplane(b,a)
title('pole-zero diagram-third order filter');

subplot(2,1,2)
plot(om/pi,abs(H));
ylim([0,1.2])
grid on


