%%
% 
% clc
% clear
% 
% N = 500;
% n = 1:N;
% x = sin(5*pi*n/N) + 0.5*randn(1, N);        % Input signal
% 
% fc = 0.2;
% [b, a] = butter(2, 2*fc);  
% [H,om] = freqz(b,a,10000);
% figure(1)
% plot(om, abs(H))
% 

%% three knob tone

function filter_gui_example_ver1

G = 1;
B = pi/4;
wc = pi/2;
Gsq = sqrt(G);
tanB = tan(B/2);

a = [Gsq+G*tanB -2*Gsq*cos(wc) Gsq-G*tanB];
b = [Gsq+tanB -2*Gsq*cos(wc) Gsq-tanB];
[H,om] = freqz(b,a);
f = om/pi;

fig = figure(1);

setappdata(fig,'gain',G);
setappdata(fig,'bandwidth',B);
setappdata(fig,'centerfreqz',wc);

clf
subplot(2,1,1);
line_handle.axes1 = plot(f,-20*log(abs(H)));
title('Filter frequency response', 'fontsize', 12 );
xlabel('Frequency (cycles/sample)')
ylabel('Magnitude(dB)')
xlim([0, 1]);
ylim([-30 30]);
box off

line_handle.axes2 = subplot(2,1,2);
zplane(b,a);



drawnow;

%% gain
slider_handle_gain = uicontrol('Parent', fig,'Style', 'slider', ...
    'Min', 0.25, 'Max', 4,...
    'Value', 1, ...
    'SliderStep', [0.05 0.1], ...
    'Position', [5 5 100 15], ...           % [left, bottom, width, height]
    'Callback', {@fun_gain,line_handle}   );

% bandwidth
slider_handle2_B = uicontrol('Parent', fig,'Style', 'slider', ...
    'Min', 0, 'Max', pi/2,...
    'Value', pi/4, ...
    'SliderStep', [0.01*pi 0.03*pi], ...
    'Position', [5 20 100 15], ...           % [left, bottom, width, height]
    'Callback', {@fun_bandwidth,line_handle}   );


%  cutoff freq

slider_handle_wc = uicontrol('Parent', fig,'Style', 'slider', ...
    'Min', 0, 'Max', pi,...
    'Value', pi/2, ...
    'SliderStep', [0.02*pi 0.05*pi], ...
    'Position', [5 35 100 15], ...           % [left, bottom, width, height]
    'Callback', {@fun_freq,line_handle}   );

  
end
%%gain

function fun_gain(hObject, eventdata, line_handle)

G = get(hObject, 'Value');

G = max(0.25, G);         % minimum value
G = min(4, G);         % maximum value

fig = get(hObject,'Parent');
B = getappdata(fig,'bandwidth');
wc = getappdata(fig,'centerfreqz');

Gsq = sqrt(G);
tanB = tan(B/2);

a = [Gsq+G*tanB -2*Gsq*cos(wc) Gsq-G*tanB];
b = [Gsq+tanB -2*Gsq*cos(wc) Gsq-tanB];
[H,om] = freqz(b,a);



set(line_handle.axes1,'ydata',-20*log(abs(H)));
line_handle.axes2 = zplane(b,a);

title( sprintf('freq:%.2f, gain:%3f,bandwidth:%3f',wc,G,B) )

setappdata(fig,'gain',G);
end

%%bandwidth
function fun_bandwidth(hObject, eventdata, line_handle)

B = get(hObject, 'Value');

B = max(0.01*pi, B);         % minimum value
B = min(0.99*pi/2, B);         % maximum value

fig = get(hObject,'Parent');
G = getappdata(fig,'gain');
wc = getappdata(fig,'centerfreqz');



Gsq = sqrt(G);
tanB = tan(B/2);

a = [Gsq+G*tanB -2*Gsq*cos(wc) Gsq-G*tanB];
b = [Gsq+tanB -2*Gsq*cos(wc) Gsq-tanB];
[H,om] = freqz(b,a);

set(line_handle.axes1,'ydata',-20*log(abs(H)));
line_handle.axes2 = zplane(b,a);

title( sprintf('freq:%.2f, gain:%3f,bandwidth:%3f',wc,G,B) )
setappdata(fig,'bandwidth',B);
end


%% center_freq

function fun_freq(hObject, eventdata, line_handle)

wc = get(hObject, 'Value');

wc = max(0.01*pi, wc);         % minimum value
wc = min(0.99*pi, wc);         % maximum value

fig = get(hObject,'Parent');
B = getappdata(fig,'bandwidth');
G = getappdata(fig,'gain');



Gsq = sqrt(G);
tanB = tan(B/2);

a = [Gsq+G*tanB -2*Gsq*cos(wc) Gsq-G*tanB];
b = [Gsq+tanB -2*Gsq*cos(wc) Gsq-tanB];
[H,om] = freqz(b,a);

set(line_handle.axes1,'ydata',-20*log(abs(H)));
line_handle.axes2 = zplane(b,a);

title( sprintf('freq:%.2f, gain:%3f,bandwidth:%3f',wc,G,B) )
setappdata(fig,'centerfreqz',wc);
end
