%% This code needs Matlab2015a to run
function lab7_2_ytl287
G = 0.47;
Q = 0.9;
fc = 0.15;  % w = 2*pi*f
wc = 2*pi*fc;
B = wc/Q;
Gsq = sqrt(G);
tanB = tan(B/2);

a = [Gsq+G*tanB -2*Gsq*cos(wc) Gsq-G*tanB];
b = [Gsq+tanB -2*Gsq*cos(wc) Gsq-tanB];
[H,om] = freqz(b,a,10000);

f1 = figure(1)
plot(om/pi, abs(H))

f1 = figure(1);
clf
% line(n, x, 'marker', '.', 'linestyle', 'none', 'markersize', 10, 'color', [1 1 1]*0.5)
line_handle = line(om/pi, abs(H), 'linewidth', 2, 'color', 'black');
legend('frequency response')
title( sprintf('Output of LPF. Cut-off frequency = %.3f (normalized)', fc) )
% xlabel('Time')
box off
% xlim([0, N]);
ylim([1 3]);

drawnow;

slider_handle = uicontrol(f1, ...
    'Style', 'slider', ...
    'Tag','sliderfc', ...
    'Min', 0, 'Max', 0.5, ...
    'UserData', struct('fc',fc,'G',G,'Q',Q), ...
    'SliderStep', [0.02 0.05], ...
    'units', 'normalized', ...
    'Position', [0.2 0.61 0.6 0.03], ...
    'Callback',  {@fun1, line_handle}  );

slider_handle2 = uicontrol(f1, ...
    'Style', 'slider', ...
    'Tag','sliderG', ...
    'Min', 0, 'Max', 0.999, ...
    'UserData', struct('fc',fc,'G',G,'Q',Q), ...
    'SliderStep', [0.02 0.05], ...
    'units', 'normalized', ...
    'Position', [0.2 0.68 0.6 0.03], ...
    'Callback',  {@fun2, line_handle}  );

slider_handle3 = uicontrol(f1, ...
    'Style', 'slider', ...
    'Tag','sliderQ', ...
    'Min', 0, 'Max', 2.999, ...
    'UserData', struct('fc',fc,'G',G,'Q',Q), ...
    'SliderStep', [0.02 0.05], ...
    'units', 'normalized', ...
    'Position', [0.2 0.75 0.6 0.03], ...
    'Callback',  {@fun3, line_handle}  );

txt = uicontrol('Style','text',...
    'Position', [450 250 25 20],...
    'String','fc');
txt = uicontrol('Style','text',...
    'Position', [450 280 25 20],...
    'String','G');
txt = uicontrol('Style','text',...
    'Position', [450 310 25 20],...
    'String','Q');
end


% callback function fun1 for fc adjustment

function fun1(hObject, eventdata, line_handle)
h1 = findobj('Tag','sliderG');
h2 = findobj('Tag','sliderQ');
hObject.UserData.G = h1.UserData.G;
hObject.UserData.Q = h2.UserData.Q;

fc = hObject.Value
hObject.UserData.fc = fc;
G = hObject.UserData.G;
Q = hObject.UserData.Q;
% hObject.UserData = data;
% fc = get(hObject, 'Value');     % cut-off frequency
% fc = max(0.01, fc);             % minimum value
% fc = min(0.49, fc);             % maximum value

wc = 2*pi*fc;
B = wc/Q;
Gsq = sqrt(G);
tanB = tan(B/2);

a = [Gsq+G*tanB -2*Gsq*cos(wc) Gsq-G*tanB];
b = [Gsq+tanB -2*Gsq*cos(wc) Gsq-tanB];
[H,om] = freqz(b,a,10000);

set(line_handle, 'ydata', abs(H));

title( sprintf('Output of LPF. Cut-off frequency = %.3f (normalized)', fc) )

end

% callback function fun2 for Gain adjustment

function fun2(hObject, eventdata, line_handle)
h1 = findobj('Tag','sliderfc');
h2 = findobj('Tag','sliderQ');
hObject.UserData.fc = h1.UserData.fc;
hObject.UserData.Q = h2.UserData.Q;

G = hObject.Value
hObject.UserData.G = G;

fc = hObject.UserData.fc;
Q = hObject.UserData.Q;

wc = 2*pi*fc;
B = wc/Q;
Gsq = sqrt(G);
tanB = tan(B/2);

a = [Gsq+G*tanB -2*Gsq*cos(wc) Gsq-G*tanB];
b = [Gsq+tanB -2*Gsq*cos(wc) Gsq-tanB];
[H,om] = freqz(b,a,10000);

set(line_handle, 'ydata', abs(H));

title( sprintf('Output of LPF. Cut-off frequency = %.3f (normalized)', fc) )

end


% callback function fun3 for Q adjustment

function fun3(hObject, eventdata, line_handle)
h1 = findobj('Tag','sliderfc');
h2 = findobj('Tag','sliderG');
hObject.UserData.fc = h1.UserData.fc;
hObject.UserData.G = h2.UserData.G;

Q = hObject.Value
hObject.UserData.Q = Q;

fc = hObject.UserData.fc;
G = hObject.UserData.G;


wc = 2*pi*fc;
B = wc/Q;
Gsq = sqrt(G);
tanB = tan(B/2);

a = [Gsq+G*tanB -2*Gsq*cos(wc) Gsq-G*tanB];
b = [Gsq+tanB -2*Gsq*cos(wc) Gsq-tanB];
[H,om] = freqz(b,a,10000);

set(line_handle, 'ydata', abs(H));

title( sprintf('Output of LPF. Cut-off frequency = %.3f (normalized)', fc) )

end