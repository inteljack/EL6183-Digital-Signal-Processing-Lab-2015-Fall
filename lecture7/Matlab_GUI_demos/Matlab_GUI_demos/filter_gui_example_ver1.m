function filter_gui_example_ver1

N = 500;
n = 1:N;
x = sin(5*pi*n/N) + randn(1, N);        % Input signal

figure(1)
clf
line_handle = plot(n, x);
title('Noisy data', 'fontsize', 12 )
xlabel('Time')
box off
xlim([0, N]);
ylim([-3 3])

drawnow;

slider_handle = uicontrol('Style', 'slider', ...
    'Min', 0, 'Max', 1,...
    'Value', 1, ...
    'SliderStep', [0.02 0.05], ...
    'Position', [5 5 200 20], ...           % [left, bottom, width, height]
    'Callback',  {@fun1, line_handle, x}    );

end


function fun1(hObject, eventdata, line_handle, x)

fc = get(hObject, 'Value');  % fc : cut-off frequency

fc = max(0.01, fc);         % minimum value
fc = min(0.99, fc);         % maximum value

[b, a] = butter(2, fc);     % Order-2 Butterworth filter
y = filtfilt(b, a, x);

set(line_handle, 'ydata',  y);        % Update data in figure

title( sprintf('Output of LPF. Cut-off frequency = %.3f', fc), 'fontsize', 12 )

end

