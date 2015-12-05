function filter_gui_example_ver2_modified

N = 500;
n = 1:N;
x = sin(5*pi*n/N) + 0.5*randn(1, N);        % Input signal

fc = 0.1;
[b, a] = butter(2, 2*fc);       
y = filtfilt(b, a, x);

f1 = figure(1);
clf
subplot(2,1,1)
line(n, x, 'marker', '.', 'linestyle', 'none', 'markersize', 10, 'color', [1 1 1]*0.5)
line_handle1 = line(n, y, 'linewidth', 2, 'color', 'black');
legend('Noisy data', 'Filtered data')
title( sprintf('Output of LPF. Cut-off frequency = %.3f (normalized)', fc) )
xlabel('Time')
box off
xlim([0, N]);
ylim([-3 3])

subplot(2,1,2)   % make the figure position at subplot 1
line(n, x, 'marker', '.', 'linestyle', 'none', 'markersize', 10, 'color', [1 1 1]*0.5)
line_handle2 = line(n, y, 'linewidth', 2, 'color', 'black');
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
    'Position', [0.2 0.625 0.6 0.03], ...
    'Callback',  {@fun1, line_handle1, x}  );

slider_handle2 = uicontrol(f1, ...
    'Style', 'slider', ...
    'Min', 0, 'Max', 0.2, ...
    'Value', fc, ...
    'SliderStep', [0.02 0.05], ...
    'units', 'normalized', ...
    'Position', [0.2 0.15 0.6 0.03], ...
    'Callback',  {@fun1, line_handle2, x}  );
end


% callback function fun1

function fun1(hObject, eventdata, line_handle, x)


fc = get(hObject, 'Value');     % cut-off frequency

fc = max(0.01, fc);             % minimum value
fc = min(0.49, fc);             % maximum value

[b, a] = butter(2, 2*fc);       % Order-2 Butterworth filter (multiply fc by 2 due to non-conventional Matlab convention)
y = filtfilt(b, a, x);

set(line_handle, 'ydata',  y);

title( sprintf('Output of LPF. Cut-off frequency = %.3f (normalized)', fc) )

end

