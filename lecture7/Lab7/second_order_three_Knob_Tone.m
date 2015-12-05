function second_order_three_Knob_Tone

N = 500;
n = 1:N;
x = sin(5*pi*n/N) + 0.5*randn(1, N);        % Input signal

G = 1;
Q = 10;
fc = 0.1;  % w = 2*pi*f
wc = 2*pi*fc;
B = wc/Q;
Gsq = sqrt(G);
tanB = tan(B/2);

b = [Gsq+G*tanB -2*Gsq*cos(wc) Gsq-G*tanB];
a = [Gsq+tanB -2*Gsq*cos(wc) Gsq-tanB];
% [b, a] = butter(2, 2*fc);
y = filtfilt(b, a, x);
[H,om] = freqz(b,a,10000);


f1 = figure(1);
clf
line(n, x, 'marker', '.', 'linestyle', 'none', 'markersize', 10, 'color', [1 1 1]*0.5)
line_handle = line(n, y, 'linewidth', 2, 'color', 'black');
legend('Noisy data', 'Filtered data')
title( sprintf('Output of LPF. Cut-off frequency = %.3f (normalized)', fc) )
xlabel('Time')
box off
xlim([0, N]);
ylim([-3 3])

drawnow;

slider_handle = uicontrol(f1, ...
    'Style', 'slider', ...
    'Min', 0, 'Max', 0.2, ...
    'Value', fc, ...
    'SliderStep', [0.02 0.05], ...
    'units', 'normalized', ...
    'Position', [0.2 0.15 0.6 0.05], ...
    'Callback',  {@fun1, line_handle, fc,G,Q}  );

end


% callback function fun1

function fun1(hObject, eventdata, line_handle, fc,G,Q)


fc = get(hObject, 'Value');     % cut-off frequency

fc = max(0.01, fc);             % minimum value
fc = min(0.49, fc);             % maximum value
G = 1;
Q = 10;
wc = 2*pi*fc;
B = wc/Q;
Gsq = sqrt(G);
tanB = tan(B/2);

a = [Gsq+G*tanB -2*Gsq*cos(wc) Gsq-G*tanB];
b = [Gsq+tanB -2*Gsq*cos(wc) Gsq-tanB];
% [b, a] = butter(2, 2*fc);       % Order-2 Butterworth filter (multiply fc by 2 due to non-conventional Matlab convention)
% y = filtfilt(b, a, x);

set(line_handle, 'ydata',  y);

title( sprintf('Output of LPF. Cut-off frequency = %.3f (normalized)', fc) )

end

